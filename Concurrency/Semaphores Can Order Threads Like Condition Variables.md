---
type: atomic
source: OSTEP Ch. 25
tags: [concurrency, synchronization, semaphores, ordering]
related: [[Semaphores Define wait and post Operations]], [[Condition Variables Allow Threads to Sleep and Wake]], [[pthread_join() Waits for Thread Completion]]
prerequisites: [[Semaphores Define wait and post Operations]]
---

> [!SUMMARY]
> Semaphores can be used to enforce **ordering** between threads. By initializing a semaphore to **0**, a thread calling `sem_wait()` will block until another thread calls `sem_post()`, effectively waiting for a signal or event completion.

## Initializing for Ordering

To use a semaphore for ordering (similar to a Condition Variable or `pthread_join`), we initialize it to 0:

```c
sem_t s;
sem_init(&s, 0, 0); // Value = 0
```

## Usage Pattern: Parent Waits for Child

Suppose a parent thread wants to wait for a child thread to finish execution:

```c
void *child(void *arg) {
    printf("child
");
    sem_post(&s); // Signal completion
    return NULL;
}

int main(int argc, char *argv[]) {
    sem_init(&s, 0, 0);
    printf("parent: begin
");
    pthread_t c;
    pthread_create(&c, NULL, child, NULL);
    sem_wait(&s); // Wait for child
    printf("parent: end
");
    return 0;
}
```

### Trace: Parent Waits

1.  **Parent creates Child**.
2.  **Parent calls `sem_wait(&s)`**:
    *   Value becomes -1 (0 -> -1).
    *   Parent blocks.
3.  **Child runs**:
    *   Prints "child".
    *   **Child calls `sem_post(&s)`**:
        *   Value becomes 0 (-1 -> 0).
        *   Wakes the Parent.
4.  **Parent wakes**:
    *   Returns from `sem_wait`.
    *   Prints "parent: end".

### Trace: Child Runs First

1.  **Child runs immediately**:
    *   Prints "child".
    *   **Child calls `sem_post(&s)`**:
        *   Value becomes 1 (0 -> 1).
        *   No one waiting.
2.  **Parent runs**:
    *   **Parent calls `sem_wait(&s)`**:
        *   Value becomes 0 (1 -> 0).
        *   Returns immediately (child already finished).

This versatility allows semaphores to replace both locks and condition variables in many scenarios.
