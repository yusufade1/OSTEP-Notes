---
type: mechanism
source: "OSTEP Ch. 30: Condition Variables"
tags:
  - concurrency
  - synchronization
  - condition-variables
  - patterns
related:
  - "[[Condition Variables Allow Threads to Sleep and Wake]]"
  - "[[Always Use While Loops with Condition Variables]]"
  - "[[Concurrent Queues Use Two Locks for Head and Tail]]"
prerequisites:
  - "[[Always Use While Loops with Condition Variables]]"
---

> [!SUMMARY]
> The producer-consumer problem requires synchronizing access to a bounded buffer so producers wait when full and consumers wait when empty. The correct solution uses two separate condition variables and while-loops to prevent race conditions and ensure the correct threads are woken.

## The Problem

In the producer-consumer (or bounded buffer) problem, producer threads generate data items and place them in a buffer, while consumer threads grab items from the buffer and process them. The requirements are:
1.  **Mutual Exclusion:** Only one thread can access the buffer at a time.
2.  **Synchronization:** Consumers must wait if the buffer is empty; producers must wait if the buffer is full.

## The Broken Solution: One Condition Variable

A common mistake is using a single condition variable (e.g., `cond`) for both conditions.

Consider a buffer of size 1.
1.  Consumer $C_1$ waits because the buffer is empty.
2.  Producer $P_1$ fills the buffer and signals $C_1$ (but $C_1$ doesn't run yet).
3.  Producer $P_2$ tries to fill, finds it full, and waits on `cond`.
4.  $C_1$ runs, consumes the item, and signals `cond`.
5.  $C_1$'s signal *should* wake $P_2$. But if there was another consumer $C_2$ waiting, $C_1$ might wake $C_2$ instead.
6.  $C_2$ wakes, finds the buffer empty, and goes back to sleep.
7.  Now everyone is asleep ($P_2$ waiting for space, $C_1$ working, $C_2$ waiting for data), but the buffer is empty and $P_2$ could fill it. This is a deadlock.

## The Correct Solution: Two Condition Variables

To fix this, we need two condition variables: `empty` (to signal that the buffer is not full) and `fill` (to signal that the buffer is not empty).

```c
int loops; // must be initialized
int buffer[MAX];
int fill_ptr = 0;
int use_ptr = 0;
int count = 0;

void put(int value) {
    buffer[fill_ptr] = value;
    fill_ptr = (fill_ptr + 1) % MAX;
    count++;
}

int get() {
    int tmp = buffer[use_ptr];
    use_ptr = (use_ptr + 1) % MAX;
    count--;
    return tmp;
}

cond_t empty, fill;
mutex_t mutex;

void *producer(void *arg) {
    int i;
    for (i = 0; i < loops; i++) {
        Pthread_mutex_lock(&mutex);
        while (count == MAX)
            Pthread_cond_wait(&empty, &mutex);
        put(i);
        Pthread_cond_signal(&fill);
        Pthread_mutex_unlock(&mutex);
    }
}

void *consumer(void *arg) {
    int i;
    for (i = 0; i < loops; i++) {
        Pthread_mutex_lock(&mutex);
        while (count == 0)
            Pthread_cond_wait(&fill, &mutex);
        int tmp = get();
        Pthread_cond_signal(&empty);
        Pthread_mutex_unlock(&mutex);
        printf("%d\n", tmp);
    }
}
```

In this correct pattern:
- Producers wait on `empty` (wait for space) and signal `fill` (announce data).
- Consumers wait on `fill` (wait for data) and signal `empty` (announce space).
- Separation of concerns ensures a consumer never accidentally wakes another consumer when a producer is needed (and vice versa).
