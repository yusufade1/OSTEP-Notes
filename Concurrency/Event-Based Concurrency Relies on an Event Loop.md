---
type: mechanism
source: "OSTEP Ch. 27: Interlude: Thread API"
tags:
  - concurrency
  - events
  - architecture
related:
  - "[[Thread vs Process - Shared Address Space]]"
  - "[[Why Use Threads - Parallelism and Responsiveness]]"
  - "[[The select() and poll() API Monitors File Descriptors]]"
prerequisites:
  - "[[Thread vs Process - Shared Address Space]]"
  - "[[System Calls Transfer Control via Trap and Return-from-Trap]]"
---

> [!SUMMARY]
> Event-based concurrency organizes a program as a central loop that processes events from a queue. Unlike threaded concurrency, which relies on the operating system to schedule tasks, event-based systems give the application full control over scheduling, typically using a single thread to handle all requests sequentially.

# The Event Loop Model

Event-based concurrency offers a fundamentally different approach to building concurrent applications compared to the traditional multi-threaded model. In a threaded system, the developer creates multiple threads of execution, and the operating system scheduler decides which thread runs at any given moment. This introduces overhead from context switching and requires complex synchronization mechanisms like locks to protect shared state.

In contrast, an **event-based system** typically runs in a single thread. The core of the application is a simple loop, often called the **event loop**, which waits for something interesting to happen (an "event") and then processes it. The pseudo-code for a generic event loop is strikingly simple:

```c
while (1) {
    events = getEvents();
    for (e in events) {
        processEvent(e);
    }
}
```

## Control and Scheduling

In this model, the application itself acts as the scheduler. When an event occurs—such as a network packet arriving or a file becoming ready for reading—the system processes the event to completion before moving on to the next one. This provides strict control over the execution order, which can be advantageous for optimizing data locality and flow control.

Because there is only one thread running at a time, **race conditions** and **locking** are largely unnecessary for in-memory data structures. If a handler is modifying a global list, no other handler can interrupt it, ensuring atomic updates implicitly. This simplifies the development of complex logic that would otherwise require fine-grained locking in a multi-threaded environment.

## Comparison with Threads

While threads offer a natural programming model for blocking operations (the OS just switches to another thread), event-based systems must avoid blocking at all costs. If the single event loop blocks waiting for a disk I/O, the entire system grinds to a halt. This constraint forces event-based applications to use non-blocking I/O APIs and asynchronous programming patterns, which can be more difficult to reason about.

However, event-based systems often scale better for I/O-bound workloads. They avoid the memory overhead of maintaining a stack for every thread and the CPU overhead of frequent context switches. This makes them popular for high-performance servers like **Node.js** and **Nginx**, which need to handle thousands of concurrent connections efficiently.
