---
type: atomic
source: OSTEP Ch. 27
tags: [concurrency, events, api, unix]
related: [[Event-Based Concurrency Relies on an Event Loop], [Blocking Calls Freeze Event-Based Systems], [System Calls Transfer Control via Trap and Return-from-Trap]]
prerequisites: [[Event-Based Concurrency Relies on an Event Loop]]
---

> [!SUMMARY]
> The `select()` and `poll()` system calls are the foundation of event-based servers, allowing a process to monitor multiple file descriptors simultaneously. They enable the event loop to efficiently determine which I/O sources are ready for reading or writing without checking them one by one in a busy loop.

# Monitoring I/O with select() and poll()

To build an event-based server, the operating system must provide a way to receive events. Historically, the `select()` and `poll()` system calls filled this role on Unix systems. These interfaces allow a program to inspect the status of a set of file descriptors (sockets, pipes, or files) to see which ones are ready for an I/O operation.

Instead of trying to read from a socket and blocking if no data is there, an event-based server asks the OS: "Here is a list of 100 sockets. Wake me up when any one of them has data."

## The select() Interface

The `select()` system call uses sets of file descriptors (`fd_set`) to track what to check. A simple usage pattern looks like this:

```c
#include <sys/select.h>

int main() {
    fd_set readFDs;
    FD_ZERO(&readFDs);
    
    // Add file descriptors to the set
    int fd = open_network_socket();
    FD_SET(fd, &readFDs);

    while (1) {
        // Wait for an event
        // The first arg is max_fd + 1
        int rc = select(fd + 1, &readFDs, NULL, NULL, NULL);

        // Check if our fd is ready
        if (FD_ISSET(fd, &readFDs)) {
            // Read data without blocking
            process_data(fd);
        }
    }
}
```

When `select()` returns, it modifies the `readFDs` set to indicate which descriptors actually have data ready. The application then iterates through the set to process the active connections.

## Limitations and Evolution

While `select()` and `poll()` enabled the first generation of event-driven servers, they have scalability limits. Both require the application to pass the entire list of descriptors to the kernel on every call, and the kernel must scan the entire list. As the number of connections grows into the thousands, this $O(N)$ behavior becomes a bottleneck.

Modern operating systems provide optimized replacements like `epoll` (Linux) and `kqueue` (BSD/macOS). These interfaces maintain state in the kernel, so the application only needs to register a descriptor once and receives a list of only the *active* events, avoiding the linear scan. However, the fundamental concept remains the same: the OS notifies the event loop exactly when and where work needs to be done.
