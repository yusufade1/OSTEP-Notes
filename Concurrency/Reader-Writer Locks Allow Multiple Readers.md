---
type: atomic
source: OSTEP Ch. 25
tags: [concurrency, synchronization, semaphores, locks, patterns]
related: [[Binary Semaphores Act as Mutual Exclusion Locks]], [[Critical Sections Require Mutual Exclusion]], [[Semaphores Define wait and post Operations]]
prerequisites: [[Binary Semaphores Act as Mutual Exclusion Locks]]
---

> [!SUMMARY]
> **Reader-Writer Locks** allow multiple threads to read a data structure concurrently for performance, while ensuring exclusive access for writers. This is implemented using semaphores by tracking the number of active readers and locking out writers only when the first reader enters.

## The Problem

Standard mutexes are conservative: they prevent *anyone* from entering a critical section. However, for data structures that are read often but written rarely (e.g., a cache or database), this serialization is inefficient. We want:
*   **Multiple Readers**: Allowed simultaneously.
*   **Writers**: Must be exclusive (no other writers, no readers).

## Implementation

We use a struct with two semaphores and a counter:

```c
typedef struct _rwlock_t {
    sem_t lock;      // Protects the 'readers' counter
    sem_t writelock; // Prevents writers from entering
    int readers;     // Count of active readers
} rwlock_t;

void rwlock_init(rwlock_t *rw) {
    sem_init(&rw->lock, 0, 1);
    sem_init(&rw->writelock, 0, 1);
    rw->readers = 0;
}
```

### The Reader

The reader acquires the `writelock` *only if* it is the first reader. It releases it *only if* it is the last reader.

```c
void rwlock_acquire_readlock(rwlock_t *rw) {
    sem_wait(&rw->lock);
    rw->readers++;
    if (rw->readers == 1) // First reader acquires writelock
        sem_wait(&rw->writelock);
    sem_post(&rw->lock);
}

void rwlock_release_readlock(rwlock_t *rw) {
    sem_wait(&rw->lock);
    rw->readers--;
    if (rw->readers == 0) // Last reader releases writelock
        sem_post(&rw->writelock);
    sem_post(&rw->lock);
}
```

### The Writer

The writer simply acquires the `writelock`, which ensures no other writers and no readers are present.

```c
void rwlock_acquire_writelock(rwlock_t *rw) {
    sem_wait(&rw->writelock);
}

void rwlock_release_writelock(rwlock_t *rw) {
    sem_post(&rw->writelock);
}
```

## Fairness Issue

This simple implementation favors readers. If readers keep arriving, a writer might starve because `readers` never drops to 0. Solving this requires more complex logic (e.g., a "waiting writer" flag to block new readers).
