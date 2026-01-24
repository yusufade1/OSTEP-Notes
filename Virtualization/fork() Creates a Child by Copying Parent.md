---
type: atomic
source: OSTEP Ch. 5
tags:
  - virtualization
  - processes
  - api
related:
  - "[[A Process is a Running Program]]"
  - "[[exec() Replaces the Process Image]]"
  - "[[wait() Synchronizes Parent and Child]]"
  - "[[Process API Design Philosophy]]"
prerequisites:
  - "[[A Process is a Running Program]]"
  - "[[Process States - Ready Running and Blocked]]"
---

# fork() Creates a Child by Copying Parent

> [!SUMMARY]
> The `fork()` system call creates a new process by duplicating the calling process. The child is an almost-exact copy of the parent—same code, same data, same open files—but receives its own address space and a different return value from `fork()`. The parent receives the child's PID; the child receives 0. This asymmetric return value is the only way each process knows its identity.

## The Mechanism

When a process calls `fork()`, the OS creates a new child process that is a near-duplicate of the parent:

- The child gets a **copy** of the parent's address space (code, stack, heap, data)
- The child gets copies of the parent's **open file descriptors**
- The child gets its own **PID** (process ID)
- Execution continues in **both** processes from the point of the `fork()` call

The critical distinction: `fork()` is called once but returns **twice**—once in the parent and once in the child.

## Return Value Semantics

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    printf("hello (pid:%d)\n", (int) getpid());
    int rc = fork();
    if (rc < 0) {
        // fork failed
        fprintf(stderr, "fork failed\n");
        exit(1);
    } else if (rc == 0) {
        // child (new process)
        printf("child (pid:%d)\n", (int) getpid());
    } else {
        // parent goes down this path (rc = child's pid)
        printf("parent of %d (pid:%d)\n", rc, (int) getpid());
    }
    return 0;
}
```

The return value creates a fork in control flow:
- **Negative value:** Error—the fork failed (e.g., process table full)
- **Zero:** This is the child process
- **Positive value:** This is the parent process; the value is the child's PID

## Non-Determinism

After `fork()`, either the parent or child may run next—the scheduler decides. This means the output order of the two `printf` calls above is **non-deterministic**. This is a first encounter with concurrency: two processes sharing similar code, running in an order determined by the OS scheduler.

## Copy Semantics

The child receives a **copy** of the parent's memory, not shared access. Changes the child makes to variables do not affect the parent, and vice versa. In practice, most operating systems implement this efficiently using **copy-on-write (COW)**: pages are shared read-only until one process modifies a page, at which point a private copy is made.

## Why fork() Alone Is Not Enough

Creating an exact copy of the parent is rarely the end goal. Typically, a process forks to then run a *different* program via [[exec() Replaces the Process Image]]. The separation of creation (fork) from program loading (exec) is a deliberate design choice that enables powerful patterns like I/O redirection.
