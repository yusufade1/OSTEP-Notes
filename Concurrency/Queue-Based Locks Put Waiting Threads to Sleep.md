---
type: atomic
source: OSTEP Ch. 28
tags: [concurrency, locks, sleeping, solaris]
related: [[Yielding Locks Avoid Spinning but Incur Context Switches]], [[Two-Phase Locks Combine Spinning and Sleeping]]
prerequisites: [[Critical Sections Require Mutual Exclusion]]
---

> [!SUMMARY]
> Queue-based locks solve the starvation problem of spin and yield locks by explicitly managing a queue of waiting threads. Using OS primitives like `park()` and `unpark()`, a lock can put a waiting thread to sleep and wake explicitly the next thread in line when the lock is released.

# Queue-Based Locks Put Waiting Threads to Sleep

Neither spinning nor yielding guarantees fairness. To strictly control who gets the lock next and avoid starvation, we need an explicit queue. This requires OS support to suspend and resume specific threads.

## Park and Unpark
We use two Solaris-style primitives:
*   `park()`: Puts the calling thread to sleep.
*   `unpark(threadID)`: Wakes up a specific thread identified by `threadID`.

## Implementation
We need a `guard` (a simple spin lock) to protect the lock's internal queue.

```c
typedef struct {
    int flag;
    int guard;
    queue_t *q;
} lock_t;

void lock(lock_t *m) {
    while (TestAndSet(&m->guard, 1) == 1)
        ; // acquire guard
    if (m->flag == 0) {
        m->flag = 1; // acquire lock
        m->guard = 0;
    } else {
        queue_add(m->q, gettid());
        m->guard = 0;
        park(); // sleep
    }
}

void unlock(lock_t *m) {
    while (TestAndSet(&m->guard, 1) == 1)
        ; // acquire guard
    if (queue_empty(m->q))
        m->flag = 0; // release lock
    else
        unpark(queue_remove(m->q)); // wake next
    m->guard = 0;
}
```

## The Set-park Race
There is a subtle race condition in the code above: a thread could release the `guard` and be about to call `park()`, but before it sleeps, another thread calls `unlock()` and tries to `unpark()` it. The unpark happens before the park, so the thread effectively "misses" the wakeup and sleeps forever. Solaris solves this with a system call `setpark()`, which signals "I am about to park". If `unpark` is called between `setpark` and `park`, the `park` returns immediately.
