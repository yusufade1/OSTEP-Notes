---
type: atomic
source: OSTEP Ch. 27
tags: [concurrency, events, performance]
related: [[Event-Based Concurrency Relies on an Event Loop], [The select() and poll() API Monitors File Descriptors], [Asynchronous I/O Enables Non-Blocking Operations]]
prerequisites: [[Event-Based Concurrency Relies on an Event Loop]]
---

> [!SUMMARY]
> The primary rule of event-based programming is "no blocking calls." Because the system runs in a single thread, any operation that blocks the execution (like synchronous disk I/O) halts the entire event loop, causing the application to become unresponsive to all other clients and events.

# The Golden Rule: No Blocking

In a multi-threaded server, if one thread issues a blocking I/O request (like reading a file from disk), the operating system simply puts that thread to sleep and switches to another. The system remains responsive because other threads can continue to serve requests. This is the **implicit scheduling** benefit of threads.

In an **event-based system**, this safety net disappears. The application logic runs on a single thread—the event loop. If an event handler issues a blocking call, the entire process is suspended.

## The Consequences of Blocking

Imagine a web server handling 1,000 concurrent connections. 999 of them are simple memory lookups, but one request requires reading a large file from a slow disk.
1. The event loop picks up the file-read request.
2. The handler calls `read()`, which blocks waiting for the disk arm to move.
3. The entire application sleeps.
4. The other 999 clients receive no response, even though their requests are trivial, because the event loop cannot cycle to process them.

This creates a **head-of-line blocking** problem where the latency of every request is coupled to the latency of the slowest operation currently executing.

## Avoiding the Block

To maintain responsiveness, event-based applications must strictly avoid standard blocking system calls.
*   **Network I/O:** Sockets must be set to non-blocking mode (`O_NONBLOCK`). If a read would block, it returns an error (`EAGAIN`) instead, allowing the loop to retry later.
*   **Disk I/O:** This is trickier. Standard file I/O in Unix often blocks even with non-blocking flags. This limitation necessitates the use of specialized **Asynchronous I/O (AIO)** interfaces to truly overlap computation with disk operations.

This constraint fundamentally changes how code is written. Linear, procedural code ("read file, then send data") must be broken apart into non-blocking chunks, often leading to more complex code structures.
