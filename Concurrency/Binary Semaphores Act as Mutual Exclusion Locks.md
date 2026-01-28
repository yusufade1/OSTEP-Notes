---
type: atomic
source: OSTEP Ch. 25
tags: [concurrency, synchronization, semaphores, locks]
related: [[Semaphores Define wait and post Operations]], [[pthread_mutex_lock() and unlock() Protect Critical Sections]], [[Critical Sections Require Mutual Exclusion]]
prerequisites: [[Semaphores Define wait and post Operations]]
---

> [!SUMMARY]
> A **binary semaphore** is a semaphore initialized to **1**. Used in this way, `sem_wait()` acts as a lock (mutex acquire) and `sem_post()` acts as an unlock (mutex release), providing mutual exclusion for critical sections.

## Initializing for Mutual Exclusion

To use a semaphore as a lock, we initialize it to 1:

```c
sem_t m;
sem_init(&m, 0, 1); // Value = 1
```

## Usage Pattern

The usage mirrors that of a standard mutex:

```c
sem_wait(&m);
// critical section
sem_post(&m);
```

### Trace: Two Threads

Consider two threads, T0 and T1.

1.  **T0 calls `sem_wait(&m)`**:
    *   Semaphore value becomes 0 (1 -> 0).
    *   Since value >= 0, T0 returns immediately and enters the critical section.
2.  **T1 calls `sem_wait(&m)`**:
    *   Semaphore value becomes -1 (0 -> -1).
    *   Since value < 0, T1 is put to sleep.
3.  **T0 calls `sem_post(&m)`**:
    *   Semaphore value becomes 0 (-1 -> 0).
    *   Since value <= 0 (there is a waiter), T0 wakes T1.
4.  **T1 wakes up**:
    *   T1 returns from `sem_wait` and enters the critical section.
5.  **T1 calls `sem_post(&m)`**:
    *   Semaphore value becomes 1 (0 -> 1).
    *   No one is waiting, so no one is woken.

## Equivalence to Locks

When used this way, the binary semaphore is functionally equivalent to a mutex lock (`pthread_mutex_lock` / `pthread_mutex_unlock`). However, locks are generally strictly owner-based (only the thread that locked it can unlock it), whereas semaphores do not track ownership, allowing for more flexible (but dangerous) patterns.
