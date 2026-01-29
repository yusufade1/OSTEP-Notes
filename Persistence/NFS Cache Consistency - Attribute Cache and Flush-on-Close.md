---
type: concept
source: "OSTEP Ch. 49: Sun's Network File System (NFS)"
tags:
  - persistence
  - distributed-systems
  - nfs
  - caching
  - consistency
related:
  - "[[NFS Architecture - Client-Server and the VFS Layer]]"
  - "[[Stateless Protocol Design in NFS]]"
prerequisites:
  - "[[NFS Architecture - Client-Server and the VFS Layer]]"
---

# NFS Cache Consistency - Attribute Cache and Flush-on-Close

> [!SUMMARY]
> To improve performance, NFS clients cache file data and metadata (attributes) locally. This introduces the **cache consistency problem**: how to ensure that a client does not see "stale" data if another client has modified the file on the server. NFS addresses this using two heuristic policies: **flush-on-close** and an **attribute cache** with time-based expiration.

Without caching, every `read()` and `write()` would require a network round-trip, making the system prohibitively slow. However, distributed caching without a central controller (impossible in a stateless design) leads to consistency challenges.

## The Two Sub-problems
1.  **Update Visibility**: When Client A writes to a file, when do those changes reach the server so that Client B can see them?
2.  **Stale Cache**: When Client B reads a file, how does it know its local cache is still valid?

## Solution 1: Flush-on-Close (Close-to-Open)
NFSv2 implements **flush-on-close** semantics. When an application calls `close()` on a file, the NFS client must flush all dirty (modified) blocks to the server before the call returns.
*   This ensures that the server always has the latest version of a file once a client is "done" with it.
*   If Client B then calls `open()` (or more precisely, `LOOKUP`), it should theoretically see Client A's changes.

## Solution 2: The Attribute Cache
To check if a cached file is stale, the client must compare the file's modification time on the server with its local version. To avoid doing a network `GETATTR` on every single access, NFS uses an **attribute cache**.
*   The client caches file attributes (like `mtime`) for a short period (typically 3 to 60 seconds).
*   During this window, the client assumes its cache is valid.
*   If the window expires, the client makes a `GETATTR` RPC to the server. If the server's `mtime` is newer, the client invalidates its local cache.

## The "Window of Vulnerability"
NFS's consistency is **loose**. Because of the attribute cache timeout, Client B might continue to see old data for up to 60 seconds after Client A has closed the file. This is a trade-off: NFS prioritizes performance and simplicity (statelessness) over strict consistency. For most general-purpose workloads, this "eventual consistency" is acceptable, but it can lead to surprising behavior for applications that require immediate updates.

## Connections
- Caching is implemented within the [[NFS Architecture - Client-Server and the VFS Layer]].
- The lack of a "callback" mechanism (which would provide better consistency) is a direct result of the [[Stateless Protocol Design in NFS]].
