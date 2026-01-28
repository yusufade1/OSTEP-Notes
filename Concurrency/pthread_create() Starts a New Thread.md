---
type: atomic
source: OSTEP Ch. 27
tags: [concurrency, threads, api, pthreads]
related:
  - [[Thread Creation and Execution Model]]
  - [[pthread_join() Waits for Thread Completion]]
  - [[A Process is a Running Program]]
prerequisites:
  - [[Thread Creation and Execution Model]]
---

> [!SUMMARY]
> The `pthread_create()` function is the primary mechanism for launching new threads in the POSIX threading API. It initializes a new thread structure, sets up its stack, and begins executing a specified function. This function serves as the entry point for parallel execution within a process, utilizing `void *` pointers to enable generic argument passing.

# Thread Creation with pthread_create()

In the POSIX threads (pthreads) standard, creating a thread is done via the `pthread_create()` function. Unlike a simple function call, which executes synchronously on the current stack, this function spawns a new independent execution context that runs concurrently with the caller.

The function signature requires four arguments:

```c
#include <pthread.h>

int pthread_create(pthread_t *thread,
                   const pthread_attr_t *attr,
                   void *(*start_routine)(void*),
                   void *arg);
```

### Arguments Breakdown

1.  **`thread`**: A pointer to a `pthread_t` structure. The library uses this to store the unique identifier of the newly created thread. This identifier is essential for subsequent operations like waiting for the thread to finish.
2.  **`attr`**: A pointer to `pthread_attr_t` used to specify thread attributes (e.g., stack size, scheduling priority). Passing `NULL` applies system defaults, which is sufficient for most use cases.
3.  **`start_routine`**: A function pointer indicating where the new thread should begin execution. This function must match a specific signature: it takes a `void *` as input and returns a `void *`.
4.  **`arg`**: A single argument to be passed to the start routine. Because it is a `void *`, it can point to any data type (an integer, a struct, etc.), allowing flexibility in what data the thread receives.

### The Power of Void Pointers

The use of `void *` for both the argument and return value enables a generic API without C++ templates. To pass simple data like an integer, programmers often cast it directly to `void *` (though this relies on the pointer size being at least as large as the integer). For complex data, a pointer to a heap-allocated structure is typically passed.

### Example Usage

Here is a simple example of creating a thread that prints a message:

```c
#include <pthread.h>
#include <stdio.h>
#include <assert.h>

void *mythread(void *arg) {
    int *value = (int *) arg;
    printf("Thread started with value: %d
", *value);
    return NULL;
}

int main() {
    pthread_t p;
    int arg_value = 100;
    
    // Create the thread, passing &arg_value
    int rc = pthread_create(&p, NULL, mythread, &arg_value);
    assert(rc == 0); // Always check return codes!
    
    // In a real program, we would wait here
    return 0;
}
```

Correctly managing the lifecycle of the data passed in `arg` is critical; if `arg_value` were on the stack of a function that returned before the thread ran, the thread would access invalid memory.
