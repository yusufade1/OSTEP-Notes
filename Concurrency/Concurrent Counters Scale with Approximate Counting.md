---
type: mechanism
source: "OSTEP Ch. 29: Locked Data Structures"
tags:
  - concurrency
  - data-structures
  - performance
related:
  - "[[Critical Sections Require Mutual Exclusion]]"
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
  - "[[Lock Design Goals - Mutual Exclusion Fairness and Performance]]"
prerequisites:
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
---

> [!SUMMARY]
> Concurrent counters illustrate the trade-off between implementation simplicity and scalability. While a simple counter protected by a single lock ensures correctness, it becomes a severe bottleneck on multicore systems. **Approximate counting** (or sloppy counters) solves this by decoupling local updates from the global count, allowing threads to run in parallel with minimal synchronization.

## The Scalability Bottleneck

A thread-safe counter is the simplest concurrent data structure to build. You simply wrap a standard integer increment operation in a critical section using a mutex.

```c
typedef struct __counter_t {
    int value;
    pthread_mutex_t lock;
} counter_t;

void increment(counter_t *c) {
    pthread_mutex_lock(&c->lock);
    c->value++;
    pthread_mutex_unlock(&c->lock);
}
```

While correct, this approach fails dramatically in performance. As the number of threads increases, contention for the single lock grows. On a machine with 4 CPUs, four threads updating a single counter will spend most of their time waiting for the lock rather than doing work. The performance doesn't just plateau; it often degrades due to context switching overhead. This is a classic example of **lack of scalability**: adding more hardware resources (CPUs) does not improve throughput.

## Approximate (Sloppy) Counting

To address this, operating systems and high-performance applications use **approximate counters** (often called sloppy counters). The idea is to give each CPU core its own local counter and lock, plus a single global counter and lock.

When a thread running on CPU 0 wants to increment the counter, it acquires the local lock for CPU 0 and increments the local value. This happens in parallel with a thread on CPU 1 updating its own local counter. Because they are updating different memory locations protected by different locks, there is no contention.

## Global Synchronization

However, if a thread needs to read the total value, the local counts must be propagated to the global counter. This happens periodically based on a threshold value called **S**.

- When a local counter reaches `S` (or `-S`), the thread acquires the global lock, adds the local value to the global counter, and resets the local counter to zero.
- A smaller `S` means the global counter is more accurate but performance suffers (more global locking).
- A larger `S` means high performance (rare global locking) but the global count may lag significantly behind the true value.

This pattern demonstrates a fundamental principle in concurrency: **perfect accuracy often costs performance**. By allowing the read operation to be slightly "sloppy" (approximate), we gain massive scalability for the frequent write operations. This technique is widely used in OS kernel statistics (e.g., tracking allocated pages or network packets) where exact instantaneous precision is less important than low overhead.
