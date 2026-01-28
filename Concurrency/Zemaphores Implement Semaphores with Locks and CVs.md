---
type: atomic
source: OSTEP Ch. 25
tags: [concurrency, synchronization, semaphores, implementation]
related: [[Semaphores Define wait and post Operations]], [[Condition Variables Allow Threads to Sleep and Wake]], [[Lock Design Goals - Mutual Exclusion Fairness and Performance]]
prerequisites: [[Semaphores Define wait and post Operations]], [[Condition Variables Allow Threads to Sleep and Wake]]
---

> [!SUMMARY]
> A **Zemaphore** is a custom implementation of a semaphore built using a **lock** (for mutual exclusion of the counter) and a **condition variable** (for waiting and signaling). This exercise demonstrates that locks and condition variables are sufficient to build other synchronization primitives.

## The Structure

A semaphore needs an integer value, a lock to protect it, and a condition variable to manage waiting threads.

```c
typedef struct __Zem_t {
    int value;
    pthread_cond_t cond;
    pthread_mutex_t lock;
} Zem_t;

void Zem_init(Zem_t *s, int value) {
    s->value = value;
    pthread_cond_init(&s->cond, NULL);
    pthread_mutex_init(&s->lock, NULL);
}
```

## The Implementation

### `wait()`

Decrements the value. If the value becomes negative, we wait.
*Note: The OSTEP implementation differs slightly from the POSIX definition. POSIX blocks if value goes < 0. Here, we wait if value <= 0 *before* decrementing, or check value after.*

Let's use the definition that matches the behavior: **Wait if value is 0 or less.**

```c
void Zem_wait(Zem_t *s) {
    pthread_mutex_lock(&s->lock);
    while (s->value <= 0) {
        pthread_cond_wait(&s->cond, &s->lock);
    }
    s->value--;
    pthread_mutex_unlock(&s->lock);
}
```

### `post()`

Increments the value and signals a waiter.

```c
void Zem_post(Zem_t *s) {
    pthread_mutex_lock(&s->lock);
    s->value++;
    pthread_cond_signal(&s->cond);
    pthread_mutex_unlock(&s->lock);
}
```

## Difference from POSIX

This implementation (Wait-then-Decrement) keeps the value non-negative.
*   **POSIX**: Value can be negative (absolute value = num waiters).
*   **Zemaphore**: Value is always $\ge 0$. Waiters are queued on the CV, not counted in the integer itself explicitly.

Both achieve the same synchronization semantics.
