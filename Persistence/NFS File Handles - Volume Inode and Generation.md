---
type: mechanism
source: "OSTEP Ch. 49: Sun's Network File System (NFS)"
tags:
  - persistence
  - distributed-systems
  - nfs
  - metadata
related:
  - "[[Stateless Protocol Design in NFS]]"
  - "[[Directories Map Names to Inode Numbers]]"
prerequisites:
  - "[[Stateless Protocol Design in NFS]]"
---

# NFS File Handles - Volume Inode and Generation

> [!SUMMARY]
> An NFS **file handle** is a unique identifier that allows a client to reference a file on the server without needing a stateful file descriptor. It consists of three primary components: a volume identifier, an inode number, and a generation number, which together ensure that the client can uniquely and safely identify any file in the server's export list.

In a local file system, applications use a `file descriptor` (an integer) to refer to an open file. Because the NFS server is stateless and doesn't "open" files, the client must provide a full identifier with every request.

## Components of a File Handle
An NFSv2 file handle is typically a 32-byte opaque identifier containing:
1.  **Volume Identifier**: Identifies which disk partition or exported file system on the server the file resides on.
2.  **Inode Number**: The local identifier for the file within that volume, used by the server's local file system (like FFS) to find the data.
3.  **Generation Number**: A critical safety feature. If an inode number is reused (e.g., file A is deleted and file B is created with the same inode), the generation number is incremented. This prevents a client with a "stale" handle to file A from accidentally reading or writing to file B.

## Obtaining a Handle: The LOOKUP Call
Clients don't "open" files; they "look them up." 
*   An application calls `open("foo.txt")`.
*   The NFS client sends a `LOOKUP` RPC to the server, providing the handle of the parent directory and the name "foo.txt".
*   The server returns the file handle for "foo.txt".
*   The client stores this handle and uses it for all future `READ` or `WRITE` calls for that file.

## Why Inode Numbers Aren't Enough
If NFS used only inode numbers, it would be vulnerable to **file handle stale-ness**. Since the server is stateless, it doesn't know if a client still thinks Inode 1234 is "my_project.c". If the server deletes that file and assigns Inode 1234 to "my_secrets.txt", a simple inode-based request would return secret data to the wrong client. The **generation number** detects this mismatch, allowing the server to return an `ESTALE` error.

## Connections
- Replaces the `file descriptor` concept in the [[Stateless Protocol Design in NFS]].
- Bridges the network request to the local structures described in [[Directories Map Names to Inode Numbers]].
