---
type: mechanism
source: "OSTEP Ch. 50: The Andrew File System (AFS)"
tags:
  - persistence
  - distributed-systems
  - afs
  - consistency
related:
  - "[[AFS Architecture - Whole-File Caching on Local Disk]]"
  - "[[NFS Cache Consistency - Attribute Cache and Flush-on-Close]]"
prerequisites:
  - "[[AFS Architecture - Whole-File Caching on Local Disk]]"
---

# AFS Callbacks - Server-Initiated Cache Invalidation

> [!SUMMARY]
> AFS ensures cache consistency using a **callback** mechanism. When a client fetches a file, the server promises to notify that client if the file is modified by someone else. This "stateful" approach eliminates the need for clients to constantly poll the server for changes, drastically reducing network traffic and providing a more consistent view of the file system than NFS.

In NFS, clients must frequently ask the server "Has this file changed?" (polling). In AFS, the server takes on the responsibility of informing the clients (callback).

## How Callbacks Work
1.  **Callback Establishment**: When Client A fetches `file.txt`, the server adds Client A to a list of machines that have a "callback" on that file.
2.  **Modification**: Client B opens, modifies, and closes `file.txt`. The server receives the new version.
3.  **Invalidation**: The server looks at its list and sends a "callback break" message to Client A (and any other client with the file cached).
4.  **Re-fetch**: Client A marks its local copy of `file.txt` as invalid. The next time Client A tries to open the file, it will see the invalid mark and fetch the new version from the server.

## Statefulness and Reliability
Unlike the [[Stateless Protocol Design in NFS|stateless NFS server]], an AFS server is **stateful**—it must remember which clients have which files. 
This introduces a new failure mode: if the server crashes, it might lose its list of callbacks. To handle this:
*   Clients periodically send "heartbeats" to the server.
*   If a client cannot reach the server, it must assume all its callbacks have expired and re-verify every file on the next access.
*   When the server reboots, it can send a message to all clients telling them to invalidate their caches (a "clean slate" approach).

## Efficiency Gains
Callbacks are the primary reason AFS scales better than NFS. In a system with thousands of clients, polling (NFS) creates a "thundering herd" of metadata requests that can overwhelm a server. With callbacks (AFS), the server only communicates with clients when something actually changes.

## Connections
- Solves the "stale cache" problem described in [[NFS Cache Consistency - Attribute Cache and Flush-on-Close]].
- Relies on the stateful server model, contrasting with the [[Stateless Protocol Design in NFS]].
