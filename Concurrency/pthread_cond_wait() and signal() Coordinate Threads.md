---
type: atomic
source: OSTEP Ch. 27
tags: [concurrency, condition-variables, api, pthreads]
related:
  - [[pthread_mutex_lock() and unlock() Protect Critical Sections]]
  - [[pthread_join() Waits for Thread Completion]]
  - [[Critical Sections Require Mutual Exclusion]]
prerequisites:
  - [[pthread_mutex_lock() and unlock() Protect Critical Sections]]
---

> [!SUMMARY]
> Condition variables allow threads to signal one another about changes in shared state. The `pthread_cond_wait()` function puts a calling thread to sleep until a condition is met, while `pthread_cond_signal()` wakes up a waiting thread. These primitives are essential for coordinating actions, such as in producer-consumer scenarios, and must always be used in conjunction with a mutex.

# Signaling with Condition Variables

While mutexes prevent concurrent access, **condition variables** allow threads to wait for a specific condition to become true (e.g., "queue is not empty"). Polling a variable (spinning) wastes CPU cycles; condition variables allow a thread to sleep until notified.

The key functions are:

```c
int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex);
int pthread_cond_signal(pthread_cond_t *cond);
```

### The Wait Protocol

The `pthread_cond_wait()` function is unique because it takes **both** the condition variable and a mutex. Its behavior is atomic but involves three steps:
1.  It releases the mutex (which the caller *must* hold).
2.  It puts the calling thread to sleep.
3.  When the thread wakes up (after a signal), it re-acquires the mutex before returning.

This design ensures the thread does not hold the lock while sleeping (which would block everyone else), but holds it again immediately upon waking to safely check the shared state.

### The Signal Protocol

The `pthread_cond_signal()` function wakes up **one** thread waiting on the condition variable. If multiple threads are waiting, only one is chosen. `pthread_cond_broadcast()` wakes up **all** waiting threads.

### The "While Loop" Rule

When waiting for a condition, you should always use a `while` loop, not an `if` statement. Even after waking up, the state might have changed again before the thread runs, or the wakeup might be "spurious."

**Correct Pattern:**
```c
pthread_mutex_lock(&lock);
while (ready == 0) {
    pthread_cond_wait(&cond, &lock);
}
// Do work...
pthread_mutex_unlock(&lock);
```

### Example: Parent Waiting for Child

This example shows a parent thread waiting for a child to signal "done":

```c
#include <pthread.h>
#include <stdio.h>

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int done = 0;

void thr_exit() {
    pthread_mutex_lock(&lock);
    done = 1;
    pthread_cond_signal(&cond); // Signal state change
    pthread_mutex_unlock(&lock);
}

void *child(void *arg) {
    printf("child running
");
    thr_exit();
    return NULL;
}

void thr_join() {
    pthread_mutex_lock(&lock);
    while (done == 0) { // Always use a while loop
        pthread_cond_wait(&cond, &lock);
    }
    pthread_mutex_unlock(&lock);
}

int main() {
    pthread_t p;
    pthread_create(&p, NULL, child, NULL);
    thr_join();
    printf("parent: end
");
    return 0;
}
```

This ensures the parent only proceeds after `done` is set to 1, regardless of whether the child runs before or after `thr_join()` is called.
