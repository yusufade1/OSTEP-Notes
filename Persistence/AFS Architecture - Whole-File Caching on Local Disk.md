---
type: concept
source: "OSTEP Ch. 50: The Andrew File System (AFS)"
tags:
  - persistence
  - distributed-systems
  - afs
  - architecture
related:
  - "[[Distributed FS - Chapter Overview]]"
  - "[[NFS Architecture - Client-Server and the VFS Layer]]"
  - "[[AFS Callbacks - Server-Initiated Cache Invalidation]]"
prerequisites:
  - "[[Distributed FS - Chapter Overview]]"
---

# AFS Architecture - Whole-File Caching on Local Disk

> [!SUMMARY]
> The Andrew File System (AFS) is a distributed file system designed for extreme scalability. Unlike NFS, which caches individual blocks, AFS caches **entire files** on the client's local disk. This strategy minimizes server interaction, as subsequent reads and writes happen at local disk speeds without any network traffic until the file is closed.

AFS was developed at Carnegie Mellon University with the goal of supporting thousands of workstations with a small number of servers. Its core architecture is built around the "Venus" client-side cache manager.

## Whole-File Caching
When a client application opens a file:
1.  **Fetch**: If the file is not in the local cache, Venus fetches the *entire* file from the server and stores it on the client's local disk.
2.  **Local Access**: All subsequent `read()` and `write()` operations from the application are redirected to the local cached copy.
3.  **Flush**: When the application calls `close()`, if the file was modified, Venus sends the entire modified file back to the server.

## Benefits for Scalability
By caching the entire file, AFS shifts the I/O load from the server to the client's local disk.
*   **Reduced Server Load**: The server is only involved during `open` (fetch) and `close` (store). In between, the server does nothing, even if the application performs millions of I/O operations.
*   **Performance**: Once the file is fetched, the application experiences local-disk performance, which is typically much faster than network-based I/O.
*   **Availability**: AFS can continue to operate in a "disconnected" mode for already-cached files if the network or server goes down temporarily.

## The Vice/Venus Model
The architecture is divided into two parts:
*   **Vice**: The server-side process that manages the central repository of files and handles fetch/store requests.
*   **Venus**: The client-side cache manager that intercepts file system calls and manages the local disk cache.

## Connections
- Contrasts with the block-based caching in [[NFS Architecture - Client-Server and the VFS Layer]].
- Enables the efficiency managed by [[AFS Callbacks - Server-Initiated Cache Invalidation]].
- Dictates the [[AFS Consistency Model - Session Semantics and Last-Writer-Wins]].
