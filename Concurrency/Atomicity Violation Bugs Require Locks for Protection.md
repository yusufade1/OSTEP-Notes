---
type: atomic
source: OSTEP Ch. 26
tags: [concurrency, bugs, locks]
related:
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
  - "[[Critical Sections Require Mutual Exclusion]]"
  - "[[Race Conditions lead to Non-Deterministic Behavior]]"
prerequisites:
  - "[[Lock Design Goals - Mutual Exclusion Fairness and Performance]]"
---

> [!SUMMARY]
> Atomicity violation bugs occur when a sequence of instructions that should be executed atomically is interrupted by another thread, leading to inconsistent state. These are often fixed by surrounding the critical section with a lock.

An **atomicity violation** is one of the most common concurrency bugs. It happens when a programmer intends for a code snippet to run as a single, indivisible unit (a critical section), but fails to enforce this atomicity during execution.

### The Problem
Consider this example from a MySQL bug reported in OSTEP. Two threads access a shared structure `proc_info`:

**Thread 1:**
```c
if (thd->proc_info) {
    fputs(thd->proc_info, ...);
}
```

**Thread 2:**
```c
thd->proc_info = NULL;
```

Thread 1 checks if `proc_info` is non-NULL. However, before it can call `fputs`, the scheduler might switch to Thread 2, which sets `proc_info` to `NULL`. When Thread 1 resumes, it passes a `NULL` pointer to `fputs`, causing a crash. The assumption that the check and the use are atomic was violated.

### The Solution
The fix is to enforce atomicity using synchronization primitives, typically locks. By wrapping the check and the usage in a lock, we ensure that no other thread can modify the state in between.

**Fixed Code:**
```c
pthread_mutex_lock(&proc_info_lock);
if (thd->proc_info) {
    fputs(thd->proc_info, ...);
}
pthread_mutex_unlock(&proc_info_lock);
```

In this corrected version, Thread 1 holds the lock for the entire duration of the check-and-use sequence. If Thread 2 tries to acquire the lock to set the pointer to `NULL`, it must wait until Thread 1 releases it. This eliminates the race window and preserves the logical atomicity of the operation. Identifying these regions where multiple memory accesses must happen together is key to preventing this class of bugs.
