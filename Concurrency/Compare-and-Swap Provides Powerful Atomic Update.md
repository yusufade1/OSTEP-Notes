---
type: atomic
source: OSTEP Ch. 28
tags: [concurrency, locks, hardware, atomic-instruction]
related: [[Test-and-Set Instruction Enables Atomic Locking]], [[Ticket Locks Ensure Fairness with Fetch-and-Add]]
prerequisites: [[Critical Sections Require Mutual Exclusion]]
---

> [!SUMMARY]
> Compare-and-Swap (CAS) is a powerful hardware atomic instruction that updates a memory location only if it currently holds an expected value. It is more versatile than Test-and-Set and forms the basis for lock-free synchronization as well as mutual exclusion locks.

# Compare-and-Swap Provides Powerful Atomic Update

The **Compare-and-Swap** (CAS) instruction is a generalized synchronization primitive available on many modern architectures (e.g., `cmpxchg` on x86, SPARC, etc.).

## The Instruction
CAS takes three arguments: a pointer to a memory location, an expected value, and a new value.

```c
int CompareAndSwap(int *ptr, int expected, int new) {
    int actual = *ptr;
    if (actual == expected)
        *ptr = new;
    return actual;
}
```

Atomically, it checks if `*ptr` equals `expected`. If so, it updates `*ptr` to `new`. Regardless of the outcome, it returns the `actual` value that was at the memory location.

## Building a Lock with CAS
A spin lock built with CAS looks very similar to one using Test-and-Set:

```c
void lock(lock_t *lock) {
    while (CompareAndSwap(&lock->flag, 0, 1) == 1)
        ; // spin
}
```
Here, we expect the flag to be 0 (free). If it is, we set it to 1 (held). If it is already 1, the CAS fails (returns 1), and we spin.

## Advantages
While for simple locks CAS behaves similarly to Test-and-Set, its power lies in **lock-free synchronization**. Because it can check a value before changing it, algorithms can perform optimistic updates: read a value, compute a new one, and try to CAS it in. If the value changed in the meantime, the CAS fails, and the algorithm can retry. This enables wait-free data structures that are immune to some deadlock scenarios.
