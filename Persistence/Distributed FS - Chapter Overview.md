---
type: overview
source: "OSTEP Ch. 48-50: Distributed File Systems"
tags:
  - persistence
  - distributed-systems
  - nfs
  - afs
  - chapter-overview
related:
  - "[[Persistence MOC]]"
  - "[[File Systems - Chapter Overview]]"
prerequisites:
  - "[[File Systems - Chapter Overview]]"
  - "[[The open() System Call Creates and Accesses Files]]"
---

# Distributed File Systems - Chapter Overview

> [!SUMMARY]
> Distributed file systems enable multiple client machines to access and share files stored on a central server. This section explores the two classic approaches to distributed storage: Sun's **Network File System (NFS)**, which emphasizes statelessness and simple crash recovery, and the **Andrew File System (AFS)**, which focuses on scalability through aggressive whole-file caching.

## The Network File System (NFS)
Developed by Sun Microsystems, NFSv2 became the industry standard for distributed storage by prioritizing a simple, stateless protocol design.
*   **[[NFS Architecture - Client-Server and the VFS Layer]]:** How NFS integrates into the OS using a virtual file system to hide network latency.
*   **[[Stateless Protocol Design in NFS]]:** The philosophy of "no server-side state" and its impact on reliability.
*   **[[NFS File Handles - Volume Inode and Generation]]:** The unique identifier used to reference files across the network.
*   **[[Idempotent Operations Enable Simple Crash Recovery in NFS]]:** How repeating operations safely allows NFS to handle network and server failures without complex recovery logic.
*   **[[NFS Cache Consistency - Attribute Cache and Flush-on-Close]]:** The challenges of client-side caching and the "stale data" problem.

## The Andrew File System (AFS)
Designed for massive scalability, AFS uses whole-file caching to reduce server load and network traffic.
*   **[[AFS Architecture - Whole-File Caching on Local Disk]]:** The unique approach of moving entire files to the client's disk for local access.
*   **[[AFS Callbacks - Server-Initiated Cache Invalidation]]:** The stateful mechanism that ensures cache consistency without constant polling.
*   **[[AFS Consistency Model - Session Semantics and Last-Writer-Wins]]:** Understanding how AFS handles concurrent updates and visibility.
*   **[[AFS vs NFS Comparison - Scalability and Consistency]]:** A detailed breakdown of the trade-offs between the two most influential distributed file systems.

## Connections
- Extends the local file system concepts from [[File Systems - Chapter Overview]] across a network.
- Adapts the naming and access patterns of [[The open() System Call Creates and Accesses Files]] for remote environments.
