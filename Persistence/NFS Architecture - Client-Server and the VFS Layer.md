---
type: concept
source: "OSTEP Ch. 49: Sun's Network File System (NFS)"
tags:
  - persistence
  - distributed-systems
  - nfs
  - architecture
related:
  - "[[Distributed FS - Chapter Overview]]"
  - "[[Stateless Protocol Design in NFS]]"
prerequisites:
  - "[[Distributed FS - Chapter Overview]]"
---

# NFS Architecture - Client-Server and the VFS Layer

> [!SUMMARY]
> NFS employs a classic client-server architecture where multiple client machines access a central server's disk over a network. To make this network access transparent to applications, NFS utilizes the **Virtual File System (VFS)** layer, allowing remote files to appear and behave like local files in the standard Unix directory tree.

The primary goal of NFS is **transparency**: a user running `ls` or `grep` should not know (or care) that the files are physically located on a machine in another room.

## The Client-Server Split
*   **The Client**: Runs the application. When the app makes a system call (like `read()`), the client's OS intercepts it and turns it into an NFS RPC (Remote Procedure Call) to the server.
*   **The Server**: Receives RPCs, performs the actual I/O on its local disk, and sends the results back to the client.

## The VFS Layer: The Great Abstraction
Unix systems use a **Virtual File System (VFS)** to support multiple file system types (like VSFS, FFS, and NFS) simultaneously. 
1.  An application calls a generic function like `open()`.
2.  The VFS determines that the path `/home/yusuf/file.txt` belongs to an NFS mount.
3.  VFS dispatches the call to the **NFS Client** module.
4.  The NFS Client communicates with the **NFS Server** over the network.
5.  On the server, the NFS Server module makes its own calls to its local VFS (which might be using FFS) to get the data.

## Why VFS Matters
Without the VFS, every application would need to be rewritten to handle network protocols. With VFS, the NFS client can implement the standard file system interface, making the network completely "pluggable." The application remains oblivious to whether the data is coming from a local SATA cable or a 10GbE network link.

## Connections
- Provides the structural foundation for the [[Stateless Protocol Design in NFS]].
- Uses the same system call interface described in [[The open() System Call Creates and Accesses Files]].
