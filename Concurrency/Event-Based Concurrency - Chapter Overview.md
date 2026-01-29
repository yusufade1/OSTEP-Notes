---
type: overview
source: "OSTEP Ch. 33: Event-based Concurrency (Advanced)"
tags:
  - concurrency
  - events
  - async-io
  - overview
related:
  - "[[Concurrency MOC]]"
  - "[[Threads - Chapter Overview]]"
prerequisites:
  - "[[Threads - Chapter Overview]]"
  - "[[IO and Storage - Chapter Overview]]"
---

# Event-Based Concurrency - Chapter Overview

> [!SUMMARY]
> Event-based concurrency offers an alternative to multi-threading. Instead of multiple threads running in parallel, a single-threaded **event loop** processes a queue of events, using non-blocking operations to maintain high performance without the complexity of locks and race conditions.


## Key Concepts

*   **[[Event-Based Concurrency Relies on an Event Loop]]**: The core "wait-for-event, handle-event" architecture.
*   **[[The select() and poll() API Monitors File Descriptors]]**: The system calls that enable efficient event detection.
*   **[[Blocking Calls Freeze Event-Based Systems]]**: Why every operation in an event-based system must be asynchronous.
*   **[[Manual Stack Management Complicates Event-Based Programming]]**: The challenge of "stack ripping" when converting synchronous code to event-driven code.
*   **[[Asynchronous I-O Enables Non-Blocking Operations]]**: The hardware and OS support that makes event-based systems scale.

## Summary
Event-based systems avoid many of the pitfalls of threads (like race conditions and deadlocks) by being single-threaded. However, they introduce their own challenges, such as the difficulty of utilizing multi-core hardware and the complexity of managing state across asynchronous callbacks. They are widely used in modern web servers and UI frameworks.