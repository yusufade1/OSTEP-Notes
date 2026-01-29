---
type: mechanism
source: "OSTEP Ch. 27: Interlude: Thread API"
tags:
  - concurrency
  - threads
  - api
  - pthreads
related:
  - "[[pthread_create() Starts a New Thread]]"
  - "[[Process API Design Philosophy]]"
  - "[[Thread Creation and Execution Model]]"
prerequisites:
  - "[[pthread_create() Starts a New Thread]]"
---

> [!SUMMARY]
> The `pthread_join()` function is the synchronization primitive used to wait for a thread to complete its execution. It blocks the calling thread until the target thread terminates, serving a role similar to `wait()` in the process API. Additionally, it allows retrieval of the return value passed back by the exiting thread.

# Waiting for Completion with pthread_join()

Once a thread is created, the main thread (or another thread) often needs to wait for it to finish its task before proceeding. This is achieved using `pthread_join()`. Without this mechanism, the main program might exit before the worker threads complete, effectively killing them mid-execution.

The function signature is:

```c
int pthread_join(pthread_t thread, void **value_ptr);
```

### Arguments Breakdown

1.  **`thread`**: The `pthread_t` identifier of the thread to wait for. This must be a joinable thread (not detached) that was initialized via `pthread_create()`.
2.  **`value_ptr`**: A pointer to a pointer (double pointer) used to retrieve the return value of the thread. Since the thread's start routine returns a `void *`, `pthread_join` needs a place to store that `void *`. If the return value is not needed, `NULL` can be passed.

### Blocking Behavior

When `pthread_join()` is called, the calling thread enters a **blocked** state. It yields the CPU and does not return until the specified thread has finished running. This creates a synchronization point in the program's execution flow.

### Retrieving Return Values

Just as `pthread_create` uses `void *` to pass arguments in, threads use `void *` to return values. This allows returning simple integers (by casting) or pointers to complex structures.

**Crucial Warning:** Never return a pointer to something allocated on the thread's own stack. When the thread returns, its stack is deallocated, and the pointer becomes a "dangling pointer," leading to undefined behavior. Always return pointers to heap-allocated memory or global/static data.

### Example Usage

This example shows creating a thread, waiting for it, and retrieving a result:

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

typedef struct { int a; int b; } myarg_t;
typedef struct { int x; int y; } myret_t;

void *mythread(void *arg) {
    myarg_t *args = (myarg_t *) arg;
    // Allocate return structure on the heap
    myret_t *rvals = malloc(sizeof(myret_t));
    rvals->x = args->a;
    rvals->y = args->b;
    return (void *) rvals;
}

int main() {
    pthread_t p;
    myarg_t args = { 10, 20 };
    
    pthread_create(&p, NULL, mythread, &args);
    
    myret_t *rvals;
    // Wait for thread and get the pointer to its return value
    pthread_join(p, (void **) &rvals);
    
    printf("returned %d %d\n", rvals->x, rvals->y);
    free(rvals); // Clean up the heap memory allocated by the thread
    return 0;
}
```

This pattern ensures safe data transfer between the dying thread and the joining thread.
