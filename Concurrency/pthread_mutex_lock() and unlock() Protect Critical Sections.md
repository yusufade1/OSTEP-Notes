---
type: mechanism
source: "OSTEP Ch. 27: Interlude: Thread API"
tags:
  - concurrency
  - locks
  - api
  - pthreads
related:
  - "[[Critical Sections Require Mutual Exclusion]]"
  - "[[Race Conditions lead to Non-Deterministic Behavior]]"
  - "[[Thread Creation and Execution Model]]"
prerequisites:
  - "[[Critical Sections Require Mutual Exclusion]]"
---

> [!SUMMARY]
> The `pthread_mutex_lock()` and `pthread_mutex_unlock()` functions provide mutual exclusion in the POSIX threading API. By surrounding critical sections with these calls, developers ensure that only one thread can execute a piece of code at a time, preventing race conditions. Correct usage requires proper initialization and ensuring every lock is eventually paired with an unlock.

# Mutual Exclusion with Mutexes

To prevent race conditions when accessing shared data, POSIX threads use **mutexes** (short for mutual exclusion). A mutex acts as a lock: before accessing a critical section, a thread must acquire the lock, and after finishing, it must release it.

The core API consists of:

```c
#include <pthread.h>

int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);
```

### Initialization

Before a mutex can be used, it must be initialized. There are two ways to do this:

1.  **Static Initialization**: For global or static locks, use the macro `PTHREAD_MUTEX_INITIALIZER`.
    ```c
    pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
    ```
2.  **Dynamic Initialization**: For locks allocated at runtime (e.g., on the heap), use `pthread_mutex_init()`. This approach allows setting attributes and requires `pthread_mutex_destroy()` when done.
    ```c
    int rc = pthread_mutex_init(&lock, NULL);
    assert(rc == 0);
    // ... use lock ...
    pthread_mutex_destroy(&lock);
    ```

### Locking and Unlocking

When `pthread_mutex_lock()` is called:
*   If the mutex is free, the calling thread acquires it and proceeds.
*   If the mutex is already held by another thread, the calling thread **blocks** (sleeps) until the lock becomes available.

When `pthread_mutex_unlock()` is called:
*   The lock is released.
*   If other threads are waiting for this lock, one of them is woken up to acquire it.

### Example Usage

The following example shows how to protect a shared counter using a wrapper function for safety:

```c
#include <pthread.h>
#include <assert.h>

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
int counter = 0; // Shared resource

void Pthread_mutex_lock(pthread_mutex_t *m) {
    int rc = pthread_mutex_lock(m);
    assert(rc == 0);
}

void Pthread_mutex_unlock(pthread_mutex_t *m) {
    int rc = pthread_mutex_unlock(m);
    assert(rc == 0);
}

void *mythread(void *arg) {
    Pthread_mutex_lock(&lock);
    counter = counter + 1; // Critical section
    Pthread_mutex_unlock(&lock);
    return NULL;
}
```

### Common Pitfalls
*   **Forgetting to Unlock**: If a thread returns or errors out before unlocking, the lock remains held forever, causing other threads to deadlock.
*   **Double Locking**: Locking a mutex you already hold usually results in a deadlock (depending on lock type).
*   **Unlocking Not Held**: Unlocking a mutex that the current thread does not hold is undefined behavior.
