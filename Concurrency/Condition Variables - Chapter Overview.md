---
type: overview
source: "OSTEP Ch. 30: Condition Variables"
tags:
  - concurrency
  - synchronization
  - condition-variables
  - overview
related:
  - "[[Concurrency MOC]]"
  - "[[Locks - Chapter Overview]]"
prerequisites:
  - "[[Locks - Chapter Overview]]"
---

# Condition Variables - Chapter Overview

> [!SUMMARY]
> While locks provide mutual exclusion, they do not provide a way for threads to wait for a specific condition to become true (e.g., waiting for a queue to have data). **Condition Variables** provide this signaling mechanism, allowing threads to sleep efficiently until another thread signals that the state has changed.


## Key Concepts

*   **[[Condition Variables Allow Threads to Sleep and Wake]]**: The fundamental `wait()` and `signal()` operations.
*   **[[Always Use While Loops with Condition Variables]]**: Why Mesa-style semantics require re-checking conditions after waking.
*   **[[Producer-Consumer Problem Solved with Condition Variables]]**: The classic synchronization challenge and its bounded-buffer solution.
*   **[[Covering Conditions Use Broadcast to Wake All Threads]]**: Using `broadcast()` to handle complex dependencies where multiple threads might be able to proceed.

## Summary
Condition variables are always used in conjunction with a lock. The lock ensures mutual exclusion when checking or changing the shared state, while the condition variable allows the thread to release the lock and sleep atomically when the condition is not met. Mastering the combination of locks and condition variables is essential for building complex concurrent systems.