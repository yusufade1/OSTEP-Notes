---
type: atomic
source: OSTEP Ch. 28
tags: [concurrency, locks, scheduling, context-switch]
related: [[Spin Locks rely on Busy Waiting]], [[Queue-Based Locks Put Waiting Threads to Sleep]]
prerequisites: [[Spin Locks rely on Busy Waiting]]
---

> [!SUMMARY]
> Yielding locks improve upon basic spin locks by voluntarily giving up the CPU when the lock is held. Instead of spinning and wasting a full time slice, the waiting thread calls `sched_yield()`, allowing other threads (potentially the lock holder) to run.

# Yielding Locks Avoid Spinning but Incur Context Switches

The problem with simple spin locks is waste: on a single-CPU system, if thread A holds the lock and gets preempted, thread B will spin for its entire time slice doing nothing useful.

## The Approach
We can modify the spin loop to yield the processor.

```c
void lock(lock_t *lock) {
    while (TestAndSet(&lock->flag, 1) == 1)
        sched_yield(); // give up the CPU
}
```

`sched_yield()` is a system call that moves the caller from the **running** state to the **ready** state. The OS scheduler then picks another process to run.

## Trade-offs
*   **Pros:** Ideally, if we yield, the scheduler might pick the thread holding the lock, allowing it to finish and release the lock sooner. This avoids the "spin for nothing" problem.
*   **Cons:**
    *   **Context Switch Cost:** Yielding isn't free. It involves saving state, trapping into the kernel, and restoring state. If the critical section is extremely short, the cost of switching might exceed the cost of spinning.
    *   **Starvation:** A thread might yield, wake up, find the lock still held, and yield again indefinitely if other threads keep beating it to the lock. Yielding does not guarantee fairness.

While better than pure spinning on a single CPU, yielding locks still rely on the scheduler's behavior and don't explicitly coordinate waiting.
