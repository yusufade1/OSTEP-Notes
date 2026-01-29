---
type: concept
source: "OSTEP Ch. 50: The Andrew File System (AFS)"
tags:
  - persistence
  - distributed-systems
  - afs
  - consistency
related:
  - "[[AFS Architecture - Whole-File Caching on Local Disk]]"
  - "[[AFS Callbacks - Server-Initiated Cache Invalidation]]"
prerequisites:
  - "[[AFS Architecture - Whole-File Caching on Local Disk]]"
---

# AFS Consistency Model - Session Semantics and Last-Writer-Wins

> [!SUMMARY]
> AFS provides a consistency model known as **session semantics**. Unlike local file systems where writes are immediately visible to all processes, AFS modifications are only visible to other clients after the modifying client closes the file. If multiple clients modify the same file simultaneously, the version stored by the client that closes the file **last** will overwrite all previous changes.

Session semantics are a direct consequence of AFS's whole-file caching architecture. Since all work happens on a local copy, the server only sees the final result of a "session."

## How Session Semantics Work
*   **Opening**: When a client opens a file, it is guaranteed to get the latest version that was available on the server at that moment.
*   **Writing**: While the file is open, all writes go to the local disk. No other client on the network can see these writes.
*   **Closing**: When the client closes the file, the entire file is sent to the server. Only at this point do the changes become "visible" to the rest of the world.

## The Last-Writer-Wins Conflict
Because AFS works with whole files rather than individual blocks, it does not support concurrent updates to different parts of the same file. 
Consider this scenario:
1.  Client A and Client B both open the same 1GB file.
2.  Client A changes the first 10 bytes and closes the file at 12:00 PM.
3.  Client B changes the last 10 bytes and closes the file at 12:01 PM.
4.  The server now has Client B's version. Client A's changes are **lost**, even though they were to a different part of the file.

This is the **Last-Writer-Wins** policy. While it seems dangerous, it is acceptable for the types of collaborative environments (like universities) AFS was designed for, where users rarely edit the same file at the exact same time.

## Comparison to NFS
*   **NFS**: Tries to provide something closer to local Unix semantics, where writes are flushed periodically (but not always immediately) and might be visible to others within a few seconds.
*   **AFS**: Provides a much cleaner, though more restrictive, "all-or-nothing" consistency model that is easier for users to reason about.

## Connections
- Result of the [[AFS Architecture - Whole-File Caching on Local Disk|whole-file caching]] design.
- Complemented by the [[AFS Callbacks - Server-Initiated Cache Invalidation|callback]] mechanism which ensures that the *next* open gets the latest closed version.
