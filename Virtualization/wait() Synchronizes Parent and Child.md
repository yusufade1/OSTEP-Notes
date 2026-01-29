---
type: mechanism
source: "OSTEP Ch. 5: Interlude: Process API"
tags:
  - virtualization
  - processes
  - api
  - synchronization
related:
  - "[[fork() Creates a Child by Copying Parent]]"
  - "[[Process States - Ready Running and Blocked]]"
  - "[[Process API Design Philosophy]]"
prerequisites:
  - "[[fork() Creates a Child by Copying Parent]]"
  - "[[Process States - Ready Running and Blocked]]"
---
# wait() Synchronizes Parent and Child

> [!SUMMARY]
> The `wait()` system call allows a parent process to block until one of its child processes terminates. It provides synchronization between parent and child, making execution order deterministic when needed. Without `wait()`, the parent and child run concurrently with no guaranteed ordering. The call also retrieves the child's exit status, enabling error propagation across process boundaries.

## The Mechanism

When a parent calls `wait()`, the OS:

1. **Suspends** the parent (moves it to the blocked state) if no child has yet terminated
2. **Resumes** the parent when a child exits, returning the child's PID
3. **Passes back** the child's exit status through a pointer argument

If the child has already finished before the parent calls `wait()`, the call returns immediately—the child exists as a **zombie** process until reaped.

## Code Example

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int rc = fork();
    if (rc < 0) {
        fprintf(stderr, "fork failed\n");
        exit(1);
    } else if (rc == 0) {
        // child
        printf("child (pid:%d)\n", (int) getpid());
    } else {
        // parent
        int status;
        int wc = wait(&status);
        printf("parent of %d (wc:%d) (pid:%d)\n",
               rc, wc, (int) getpid());
    }
    return 0;
}
```

With `wait()`, the output is now **deterministic**: the child's print always appears before the parent's, because the parent blocks until the child finishes.

## waitpid() for Finer Control

The `waitpid()` variant offers more precise control over which child to wait for:

```c
int wc = waitpid(child_pid, &status, options);
```

- **`child_pid`**: Wait for a specific child (or -1 for any child)
- **`status`**: Stores exit information, decoded with macros like `WIFEXITED()` and `WEXITSTATUS()`
- **`options`**: Flags like `WNOHANG` (return immediately if no child has exited)

## Exit Status Semantics

The status value encodes how the child terminated:

- `WIFEXITED(status)` — true if child exited normally
- `WEXITSTATUS(status)` — the exit code (0-255) the child passed to `exit()`
- `WIFSIGNALED(status)` — true if child was killed by a signal
- `WTERMSIG(status)` — the signal number that killed the child

This mechanism lets the parent distinguish between successful completion, error exits, and abnormal termination.

## Zombies and Orphans

Two edge cases arise from parent-child lifecycle mismatches:

- **Zombie:** A child has exited but the parent has not yet called `wait()`. The process table entry persists so the exit status remains available. Zombies consume a slot in the process table until reaped.
- **Orphan:** The parent exits before the child. The child is re-parented to `init` (PID 1), which periodically calls `wait()` to reap orphaned children.

These mechanisms ensure every process's exit status can be collected and that no process table entries leak indefinitely.
