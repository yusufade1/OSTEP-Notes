---
type: atomic
source: OSTEP Ch. 5
tags:
  - virtualization
  - processes
  - api
  - design
related:
  - "[[fork() Creates a Child by Copying Parent]]"
  - "[[exec() Replaces the Process Image]]"
  - "[[wait() Synchronizes Parent and Child]]"
  - "[[A Process is a Running Program]]"
prerequisites:
  - "[[fork() Creates a Child by Copying Parent]]"
  - "[[exec() Replaces the Process Image]]"
  - "[[wait() Synchronizes Parent and Child]]"
---

# Process API Design Philosophy

> [!SUMMARY]
> Unix separates process creation into three distinct calls—`fork()`, `exec()`, and `wait()`—rather than providing a single "spawn" operation. This separation is a deliberate design choice that creates a window between fork and exec where the child process can manipulate its own state (file descriptors, environment, working directory). This window enables I/O redirection, pipes, and other shell features without complicating the process creation API itself.

## The Separation Principle

Why not a single `CreateProcess(program, args)` call like Windows? Because separating creation from transformation gives the child a moment to configure itself:

1. **`fork()`** — Create a copy of the current process
2. *(manipulation window)* — Modify file descriptors, environment, signals, etc.
3. **`exec()`** — Replace the process image with the target program

The manipulation window is where the power lies. The child can reconfigure itself without the parent's involvement and without `exec()` needing parameters for every possible configuration.

## I/O Redirection Example

When the shell encounters `wc file.txt > output.txt`, it implements redirection by manipulating file descriptors between fork and exec:

```c
int rc = fork();
if (rc == 0) {
    // Child: close stdout and open output file
    close(STDOUT_FILENO);
    open("output.txt", O_CREAT | O_WRONLY | O_TRUNC, S_IRWXU);
    // Now fd 1 (stdout) points to output.txt
    char *args[] = {"wc", "file.txt", NULL};
    execvp(args[0], args);
}
```

The `wc` program writes to stdout as normal—it has no idea its output goes to a file. The redirection is invisible to the executed program, achieved entirely through the fork-exec separation.

## Pipes Use the Same Pattern

The Unix pipe (`cmd1 | cmd2`) connects the stdout of one process to the stdin of another using `pipe()`, `fork()`, and `exec()`:

1. Create a pipe (two connected file descriptors)
2. Fork two children
3. First child: redirect stdout to pipe write end, exec `cmd1`
4. Second child: redirect stdin to pipe read end, exec `cmd2`

No special "pipe" parameter is needed in the process API—it composes naturally from the existing primitives.

## Contrast with Monolithic APIs

Windows' `CreateProcess()` takes over a dozen parameters to cover the configurations that Unix handles in the fork-exec window. Adding a new configuration option in Windows requires extending the API; in Unix, the child simply calls the relevant system call between fork and exec.

This composability is a hallmark of the Unix philosophy: simple, orthogonal primitives that combine to enable complex behavior. Each call does one thing well, and together they form a flexible process creation framework.

## Other Useful Calls

Beyond the core three, the process API includes:

- **`kill()`** — Send signals to processes (SIGTERM, SIGINT, SIGSTOP, etc.)
- **`signal()`** — Register handlers for incoming signals
- **`getpid()`/`getppid()`** — Query own PID or parent's PID

These calls, combined with fork-exec-wait, give user programs comprehensive control over process lifecycle and communication.
