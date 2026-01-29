---
type: mechanism
source: "OSTEP Ch. 30: Condition Variables"
tags:
  - concurrency
  - synchronization
  - condition-variables
related:
  - "[[Critical Sections Require Mutual Exclusion]]"
  - "[[pthread_cond_wait() and signal() Coordinate Threads]]"
  - "[[Always Use While Loops with Condition Variables]]"
prerequisites:
  - "[[Critical Sections Require Mutual Exclusion]]"
  - "[[Lock Design Goals - Mutual Exclusion Fairness and Performance]]"
---

> [!SUMMARY]
> Condition variables provide a mechanism for threads to sleep until a specific condition becomes true, avoiding the inefficiency of busy waiting. By atomically releasing a lock and putting the calling thread to sleep, they enable efficient coordination between threads waiting for state changes.

## The Need for Waiting

In concurrent programming, threads often need to check whether a specific condition is true before proceeding. For example, a parent thread might need to wait for a child to complete, or a consumer might need to wait for a buffer to be non-empty. Using a shared variable and spinning (busy waiting) is inefficient because it wastes CPU cycles checking the variable repeatedly.

A **condition variable** is an explicit queue that threads can put themselves on when some state of execution (i.e., some condition) is not as desired. Another thread, when it changes the state, can then wake one (or more) of those waiting threads so they can continue.

## The Condition Variable API

The POSIX threads (pthreads) library provides two primary operations for condition variables:

- `wait(cond, mutex)`: Releases the mutex and puts the calling thread to sleep. When the thread wakes up, it re-acquires the mutex before returning.
- `signal(cond)`: Wakes up at least one thread waiting on the condition variable.

A key requirement is that the `wait()` call **must** be made while holding the mutex. This ensures that the check of the condition and the act of going to sleep are atomic with respect to other threads. If the mutex were released *before* calling wait, a race condition could occur where a signal arrives between the release and the sleep, causing the waiter to miss the signal and sleep forever.

## Example: Parent Waiting for Child

Consider a parent thread waiting for a child to exit. Using a condition variable `c` and a mutex `m`:

```c
int done = 0;
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t c = PTHREAD_COND_INITIALIZER;

void thr_exit() {
    pthread_mutex_lock(&m);
    done = 1;
    pthread_cond_signal(&c);
    pthread_mutex_unlock(&m);
}

void thr_join() {
    pthread_mutex_lock(&m);
    while (done == 0)
        pthread_cond_wait(&c, &m);
    pthread_mutex_unlock(&m);
}
```

In this pattern:
1. `thr_join` acquires the lock and checks `done`.
2. If `done` is 0, it calls `wait`, which releases the lock and sleeps.
3. `thr_exit` runs, acquires the lock, sets `done` to 1, and signals.
4. The signal moves the waiting thread from the condition queue to the ready queue.
5. `thr_join` wakes, re-acquires the lock, checks `done` (now 1), and proceeds.

This approach is both correct (no race conditions) and efficient (no busy waiting).
