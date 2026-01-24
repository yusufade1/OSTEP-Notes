---
type: atomic
source: OSTEP Ch. 5
tags:
  - virtualization
  - processes
  - api
related:
  - "[[fork() Creates a Child by Copying Parent]]"
  - "[[A Process is a Running Program]]"
  - "[[wait() Synchronizes Parent and Child]]"
  - "[[Process API Design Philosophy]]"
prerequisites:
  - "[[fork() Creates a Child by Copying Parent]]"
---

# exec() Replaces the Process Image

> [!SUMMARY]
> The `exec()` family of system calls transforms the current process into an entirely different program. It loads a new executable into the calling process's address space—replacing its code, data, stack, and heap—then starts executing at the new program's entry point. The PID remains the same, open files are preserved (unless marked close-on-exec), but everything else is replaced. A successful `exec()` never returns.

## The Mechanism

When a process calls `exec()`, the OS performs these steps:

1. **Loads** the specified executable's code and static data into the process's address space, overwriting the existing contents
2. **Reinitializes** the stack and heap for the new program
3. **Sets** the program counter to the new program's entry point
4. **Preserves** the process's PID and open file descriptors

The key insight: `exec()` does **not** create a new process. It repurposes the existing one. The process that called `exec()` is gone—replaced entirely by the new program.

## exec() Variants

The `exec()` family includes several variants, differing in how they accept arguments and find the executable:

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    // After fork(), in the child:
    char *args[] = {"wc", "exec.c", NULL};
    execvp(args[0], args);

    // This line only runs if exec fails
    printf("exec failed\n");
    exit(1);
}
```

Common variants:
- **`execvp(file, argv)`** — searches PATH for `file`, passes argument vector
- **`execv(path, argv)`** — uses exact path, passes argument vector
- **`execl(path, arg0, arg1, ..., NULL)`** — uses exact path, passes arguments as list
- **`execlp(file, arg0, arg1, ..., NULL)`** — searches PATH, passes arguments as list
- **`execve(path, argv, envp)`** — the underlying system call; also sets environment

The naming convention: `v` = vector (array), `l` = list, `p` = search PATH, `e` = environment.

## Never Returns on Success

A successful `exec()` call never returns—there is nothing to return *to*, since the calling program's code has been replaced. If `exec()` does return, it means something went wrong (e.g., the executable was not found, or permissions were denied). This is why code after `exec()` is typically just error handling.

## The fork-exec Pattern

The combination of `fork()` followed by `exec()` is the standard Unix idiom for running a new program:

1. Parent calls [[fork() Creates a Child by Copying Parent|fork()]] to create a child
2. Child calls `exec()` to become the desired program
3. Parent calls [[wait() Synchronizes Parent and Child|wait()]] to await completion

This separation is not accidental—it creates a window between fork and exec where the child can manipulate its own file descriptors, enabling I/O redirection, pipes, and other shell features without any special mechanism in `exec()` itself.
