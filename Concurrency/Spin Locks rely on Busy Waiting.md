---
type: mechanism
source: "OSTEP Ch. 28: Locks"
tags:
  - concurrency
  - locks
  - spin-lock
related:
  - "[[Lock Design Goals - Mutual Exclusion Fairness and Performance]]"
  - "[[Test-and-Set Instruction Enables Atomic Locking]]"
prerequisites:
  - "[[Critical Sections Require Mutual Exclusion]]"
---

> [!SUMMARY]
> A spin lock is the simplest lock implementation where a thread waiting to acquire the lock repeatedly checks a condition in a loop ("spins") until the lock becomes available. While low-overhead for short waits on multiprocessors, it wastes CPU cycles and performs poorly on single processors.

# Spin Locks rely on Busy Waiting

A spin lock is built around the concept of **busy waiting**. Instead of giving up the CPU when a lock is held by another thread, the requestor simply loops (spins), repeatedly checking if the lock is free.

## Mechanism
The most basic implementation uses a shared flag variable. However, a simple load-check-store sequence is not atomic and fails to provide mutual exclusion. Correct spin locks require hardware support, such as the **Test-and-Set** or **Compare-and-Swap** instructions, to atomically update the lock state.

```c
typedef struct {
    int flag;
} lock_t;

void init(lock_t *lock) {
    lock->flag = 0;
}

void lock(lock_t *lock) {
    while (TestAndSet(&lock->flag, 1) == 1)
        ; // spin-wait (do nothing)
}

void unlock(lock_t *lock) {
    lock->flag = 0;
}
```

## Analysis
*   **Correctness:** With atomic instructions, spin locks correctly enforce mutual exclusion.
*   **Fairness:** Simple spin locks are generally unfair. A thread running on a faster core or simply getting lucky might acquire the lock before a thread that has been waiting longer, potentially leading to starvation.
*   **Performance:**
    *   *Single CPU:* Disaster. If the thread holding the lock is preempted, the spinning thread will waste its entire time slice doing nothing useful, checking a value that cannot change until the holder runs again.
    *   *Multiple CPUs:* Effective. If the critical section is short, the spinning thread avoids the high cost of a context switch (sleeping and waking up) and can proceed almost immediately once the lock is released.

Because of this performance characteristic, spin locks are commonly used in operating system kernels for short critical sections but are rarely appropriate for user-level code where the OS scheduler controls execution.
