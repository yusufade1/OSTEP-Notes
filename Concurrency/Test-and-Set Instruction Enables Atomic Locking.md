---
type: mechanism
source: "OSTEP Ch. 28: Locks"
tags:
  - concurrency
  - locks
  - hardware
  - atomic-instruction
related:
  - "[[Spin Locks rely on Busy Waiting]]"
  - "[[Compare-and-Swap Provides Powerful Atomic Update]]"
prerequisites:
  - "[[Critical Sections Require Mutual Exclusion]]"
---

> [!SUMMARY]
> The Test-and-Set instruction (also known as atomic exchange) is a hardware primitive that atomically returns the old value of a memory location and updates it to a new value (typically 1). It enables the construction of simple spin locks by turning the "test if free, then set to busy" logic into a single atomic step.

# Test-and-Set Instruction Enables Atomic Locking

To build a working lock, we need hardware support. Standard load and store instructions are insufficient because an interrupt could occur between checking a lock's flag and setting it, leading to a race condition where two threads both believe they acquired the lock.

## The Instruction
The **Test-and-Set** instruction (often called `xchg` on x86) performs the following operation atomically:

```c
int TestAndSet(int *old_ptr, int new) {
    int old = *old_ptr; // fetch old value
    *old_ptr = new;     // store 'new' into old_ptr
    return old;         // return the old value
}
```

Importantly, the hardware guarantees that this entire sequence executes as an indivisible unit. No interrupt or other processor activity can interleave between the fetch and the store.

## Building a Spin Lock
We can build a lock using a simplified version where we always set the value to 1 (LOCKED).

```c
void lock(lock_t *lock) {
    // try to update flag to 1; if it was already 1, keep spinning
    while (TestAndSet(&lock->flag, 1) == 1)
        ; // spin
}
```

*   **Case 1: Lock is Free (0).** `TestAndSet` reads 0, sets it to 1, and returns 0. The loop condition `0 == 1` is false, so the thread breaks the loop and enters the critical section.
*   **Case 2: Lock is Held (1).** `TestAndSet` reads 1, sets it to 1 (no change), and returns 1. The loop condition `1 == 1` is true, so the thread spins.

This primitive was one of the earliest hardware solutions to the concurrency problem and remains a fundamental building block for synchronization.
