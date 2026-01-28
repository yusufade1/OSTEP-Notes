---
type: atomic
source: OSTEP Ch. 27
tags: [concurrency, io, async]
related: [[Blocking Calls Freeze Event-Based Systems], [The select() and poll() API Monitors File Descriptors], [Event-Based Concurrency Relies on an Event Loop]]
prerequisites: [[Blocking Calls Freeze Event-Based Systems], [System Calls Transfer Control via Trap and Return-from-Trap]]
---

> [!SUMMARY]
> Asynchronous I/O (AIO) allows an application to issue an I/O request and return immediately, without waiting for the operation to complete. This enables a single-threaded event loop to overlap computation with slow disk operations, preventing system freezes that would occur with standard blocking I/O.

# Overlapping Work with Asynchronous I/O

The standard Unix `read()` and `write()` system calls are synchronous: you ask the OS to do something, and your program waits until it's done. For an event-based system, waiting is fatal. **Asynchronous I/O** solves this by separating the *issuing* of a request from its *completion*.

## How AIO Works

An asynchronous interface generally provides a `submit_request` function that returns control to the caller immediately.
1.  **Issue:** The application constructs a description of the I/O (e.g., "read 4KB from file X into buffer Y") and submits it to the OS.
2.  **Overlap:** The OS (or a hardware controller) begins the transfer. Meanwhile, the application continues running, processing other events in the loop.
3.  **Complete:** When the I/O finishes, the OS notifies the application—often by placing a "completion event" into the same queue the event loop is monitoring, or by triggering a signal.

## The Interface Complexity

While conceptually simple, AIO interfaces are often complex to use. The POSIX AIO standard (`aio_read`) uses a control block structure (`struct aiocb`) to describe requests:

```c
struct aiocb my_aiocb;
memset(&my_aiocb, 0, sizeof(struct aiocb));
my_aiocb.aio_fildes = fd;
my_aiocb.aio_buf = buffer;
my_aiocb.aio_nbytes = BUFF_SIZE;
my_aiocb.aio_offset = 0;

// Issue the read - returns immediately
int ret = aio_read(&my_aiocb);
```

Checking for completion typically requires polling `aio_error()` or waiting for a signal. Modern Linux systems prefer **io_uring**, a high-performance ring-buffer interface that batches submission and completion, minimizing the system call overhead that plagued earlier AIO implementations.

By using AIO, an event-driven web server can issue a disk read for Client A, immediately process a network packet for Client B, and then handle the completion of Client A's read when the data finally arrives—all within a single thread.
