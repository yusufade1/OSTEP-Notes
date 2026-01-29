---
type: overview
source: "OSTEP Ch. 32: Common Concurrency Problems"
tags:
  - concurrency
  - debugging
  - deadlock
  - overview
related:
  - "[[Concurrency MOC]]"
  - "[[Locks - Chapter Overview]]"
  - "[[Scheduling - Chapter Overview]]"
prerequisites:
  - "[[Locks - Chapter Overview]]"
  - "[[Semaphores - Chapter Overview]]"
---

# Concurrency Bugs - Chapter Overview

> [!SUMMARY]
> Writing correct concurrent programs is difficult. This chapter categorizes the common types of bugs that occur in multi-threaded software, focusing on **deadlock** and **non-deadlock** bugs, and explores strategies for prevention and avoidance.


## Key Concepts

### Non-Deadlock Bugs
*   **[[Atomicity Violation Bugs Require Locks for Protection]]**: When a code region that should be atomic is interrupted by another thread.
*   **[[Order Violation Bugs Require Condition Variables for Enforcement]]**: When the expected execution order of two threads is flipped.

### Deadlock
*   **[[Deadlock Occurs When Threads Wait on Each Other Circularly]]**: The fundamental "deadly embrace" where no thread can make progress.
*   **[[Deadlock Prevention Breaks One of the Four Necessary Conditions]]**: Strategies for ensuring deadlock is physically impossible.
*   **[[Deadlock Avoidance Uses Knowledge to Sidestep Unsafe States]]**: Using scheduling (like the Banker's Algorithm) to avoid potential deadlocks.
*   **[[Livelock Occurs When Threads Actively Impede Each Other]]**: A state where threads keep running but make no progress.

## Summary
Concurrency bugs are often non-deterministic, making them difficult to find and fix. By understanding the four necessary conditions for deadlock (Mutual Exclusion, Hold-and-wait, No Preemption, and Circular Wait), developers can design systems that are structurally immune to these failures.