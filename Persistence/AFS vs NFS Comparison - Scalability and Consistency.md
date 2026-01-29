---
type: concept
source: "OSTEP Ch. 50: The Andrew File System (AFS)"
tags:
  - persistence
  - distributed-systems
  - afs
  - nfs
  - comparison
related:
  - "[[NFS Architecture - Client-Server and the VFS Layer]]"
  - "[[AFS Architecture - Whole-File Caching on Local Disk]]"
  - "[[AFS Callbacks - Server-Initiated Cache Invalidation]]"
  - "[[NFS Cache Consistency - Attribute Cache and Flush-on-Close]]"
prerequisites:
  - "[[NFS Architecture - Client-Server and the VFS Layer]]"
  - "[[AFS Architecture - Whole-File Caching on Local Disk]]"
---

# AFS vs NFS Comparison - Scalability and Consistency

> [!SUMMARY]
> NFS and AFS represent two different trade-offs in distributed file system design. NFS prioritizes simplicity and statelessness, making it robust but difficult to scale. AFS prioritizes scalability and performance through whole-file caching and stateful callbacks, at the cost of more complex server management and a less flexible consistency model.

| Feature | NFS (v2) | AFS (v2) |
|---|---|---|
| **Caching Unit** | Blocks (8 KB) | Whole Files |
| **Cache Location** | Memory (RAM) | Local Disk |
| **Server State** | Stateless | Stateful (Callbacks) |
| **Consistency** | Attribute Polling (Loose) | Callbacks (Stronger) |
| **Scalability** | Low to Moderate | High (Thousands of clients) |
| **Failure Recovery** | Simple (Retries) | Complex (Callback re-validation) |
| **Update Strategy** | Flush-on-close + Periodic | Flush-on-close (Session semantics) |

## Scalability: The Winning Edge for AFS
The most significant difference is how the two systems scale.
*   **NFS** servers spend a huge amount of time handling metadata requests (`GETATTR`, `LOOKUP`) because clients are constantly polling to see if their caches are stale. As you add clients, the server becomes the bottleneck.
*   **AFS** servers are only contacted when a file is first opened or finally closed. The callback mechanism ensures that clients stay silent unless a file they care about changes. This allows a single AFS server to support an order of magnitude more clients than an NFS server.

## Consistency: Different Philosophies
*   **NFS** offers "eventual" consistency that is difficult to predict (the 30-60 second attribute cache window).
*   **AFS** offers "session semantics." While you don't see updates *during* a session, you are guaranteed to see the latest version when you *begin* a session (open).

## Performance: Network vs. Disk
*   **NFS** performance is heavily dependent on network latency for every block access.
*   **AFS** performance is dependent on local disk latency. While the initial "fetch" of a large file might be slow, subsequent access is as fast as a local file system.

## Connections
- Summarizes the architectural differences between [[NFS Architecture - Client-Server and the VFS Layer]] and [[AFS Architecture - Whole-File Caching on Local Disk]].
- Explains why AFS needs the [[AFS Callbacks - Server-Initiated Cache Invalidation]] mechanism.
