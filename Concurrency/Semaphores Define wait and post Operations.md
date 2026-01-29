---
type: mechanism
source: OSTEP Ch. 25
tags:
  - concurrency
  - synchronization
  - semaphores
  - api
related:
  - "[[Binary Semaphores Act as Mutual Exclusion Locks]]"
  - "[[Semaphores Can Order Threads Like Condition Variables]]"
  - "[[Critical Sections Require Mutual Exclusion]]"
prerequisites:
  - "[[Critical Sections Require Mutual Exclusion]]"
---

> [!SUMMARY]
> A **semaphore** is a synchronization primitive consisting of an integer value that is manipulated atomically by two operations: `sem_wait()` and `sem_post()`. It generalizes locks and condition variables, capable of handling both mutual exclusion and ordering.

## The Semaphore Object

A semaphore is an object with an integer value. We manipulate it with two routines, defined by the POSIX standard as:

```c
#include <semaphore.h>
sem_t s;
sem_init(&s, 0, 1); // Initialize to 1
```

The third argument to `sem_init` is the initial value, which determines the semaphore's behavior.

## The Operations

The two primary operations are `sem_wait()` and `sem_post()`.

1.  **`sem_wait()`**: Decrements the semaphore value. If the value becomes negative, the calling thread is put to sleep (blocked).
2.  **`sem_post()`**: Increments the semaphore value. If there are threads waiting (value ≤ 0), it wakes one of them.

### Conceptual Implementation

We can visualize the logic (though the actual implementation is atomic) as follows:

```c
int sem_wait(sem_t *s) {
    decrement_and_test(s->value);
    if (s->value < 0) {
        // block the thread
    }
    return 0;
}

int sem_post(sem_t *s) {
    increment_and_test(s->value);
    if (s->value <= 0) {
        // wake one waiting thread
    }
    return 0;
}
```

## Key Properties

*   **Atomicity**: The increment/decrement and the check/sleep/wake actions are performed atomically.
*   **Negative Value**: The absolute value of a negative semaphore count equals the number of waiting threads.
*   **No Value Access**: You generally cannot read the current value of the semaphore directly; you only interact via wait and post.

By adjusting the initial value and the usage pattern, semaphores can act as **locks** (mutual exclusion) or **condition variables** (ordering).
