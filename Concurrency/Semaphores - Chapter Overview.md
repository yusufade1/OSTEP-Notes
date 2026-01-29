---
type: overview
source: "OSTEP Ch. 31: Semaphores"
tags:
  - concurrency
  - synchronization
  - semaphores
  - overview
related:
  - "[[Concurrency MOC]]"
  - "[[Condition Variables - Chapter Overview]]"
prerequisites:
  - "[[Condition Variables - Chapter Overview]]"
---

# Semaphores - Chapter Overview

> [!SUMMARY]
> **Semaphores** are a powerful and unified synchronization primitive that can be used to implement both mutual exclusion (like locks) and ordering (like condition variables). Developed by Edsger Dijkstra, semaphores use an integer value to manage access to shared resources.


## Key Concepts

*   **[[Semaphores Define wait and post Operations]]**: The core `sem_wait()` and `sem_post()` interface.
*   **[[Binary Semaphores Act as Mutual Exclusion Locks]]**: Using a semaphore with an initial value of 1 to protect critical sections.
*   **[[Semaphores Can Order Threads Like Condition Variables]]**: Using semaphores to make one thread wait for another's completion.
*   **[[Reader-Writer Locks Allow Multiple Readers]]**: A specialized synchronization pattern implemented with semaphores to improve performance for read-heavy workloads.
*   **[[The Dining Philosophers Problem Illustrates Deadlock]]**: A classic thought experiment used to test the robustness of synchronization strategies.
*   **[[Zemaphores Implement Semaphores with Locks and CVs]]**: Understanding the relationship between semaphores and other primitives.

## Summary
A semaphore is essentially an integer that can be manipulated only through atomic operations. Its value represents the number of units of a resource available. Because of their versatility, semaphores can solve almost any synchronization problem, though they require careful management to avoid subtle bugs like deadlock.