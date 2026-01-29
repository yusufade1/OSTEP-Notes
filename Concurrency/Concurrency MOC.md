---
type: moc
tags:
  - concurrency
related:
  - "[[Virtualization MOC]]"
  - "[[Persistence MOC]]"
prerequisites: []
source: "OSTEP Book"
---

# Concurrency

> [!SUMMARY]
> The OS and user programs must correctly manage multiple threads of execution sharing the same address space.


## Threads
The fundamental abstraction for shared-memory parallelism.
- [[Threads - Chapter Overview]] — Introduction to thread concepts, race conditions, and critical sections.
- [[Thread vs Process - Shared Address Space]] — Understanding how threads differ from processes in memory layout.
- [[Why Use Threads - Parallelism and Responsiveness]] — The primary motivations for multi-threaded design.
- [[Race Conditions lead to Non-Deterministic Behavior]] — The core danger of shared-memory concurrency.
- [[Critical Sections Require Mutual Exclusion]] — The conceptual solution to the race condition problem.

## Synchronization
Mechanisms for coordinating thread execution and protecting shared state.
- [[Locks - Chapter Overview]] — Building mutual exclusion primitives from hardware support.
- [[Condition Variables - Chapter Overview]] — Signaling and waiting mechanisms for efficient thread coordination.
- [[Semaphores - Chapter Overview]] — A unified primitive for both locks and signaling.
- [[Binary Semaphores Act as Mutual Exclusion Locks]] — Practical application of semaphores for mutual exclusion.
- [[Producer-Consumer Problem Solved with Condition Variables]] — A classic example of thread synchronization.

## Bugs & Patterns
Common pitfalls and alternative concurrency models.
- [[Concurrency Bugs - Chapter Overview]] — Categorization and prevention of deadlock and non-deadlock bugs.
- [[Event-Based Concurrency - Chapter Overview]] — An alternative to threads based on a single-threaded event loop.
- [[Deadlock Occurs When Threads Wait on Each Other Circularly]] — Understanding the four necessary conditions for deadlock.
- [[The select() and poll() API Monitors File Descriptors]] — The foundation of efficient event-driven systems.
- [[Atomicity Violation Bugs Require Locks for Protection]] — Identifying and fixing common non-deadlock concurrency errors.