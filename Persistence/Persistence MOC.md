---
type: moc
tags:
  - persistence
related:
  - "[[Virtualization MOC]]"
  - "[[Concurrency MOC]]"
prerequisites: []
source: "OSTEP Book"
---

# Persistence

> [!SUMMARY]
> The OS manages I/O devices and file systems to store data reliably beyond the lifetime of any single process.


## I/O & Storage
The hardware layer and its immediate management.
- [[IO and Storage - Chapter Overview]] — Introduction to I/O architecture, interrupts, and DMA.
- [[Disk Geometry Defines the Physical Structure of Hard Drives]] — How physical platters and tracks dictate disk performance.
- [[RAID - Chapter Overview]] — Strategies for combining multiple disks for performance and reliability.
- [[RAID Uses Redundancy to Improve Performance and Reliability]] — The core trade-offs of RAID systems.
- [[Flash-Based SSDs - Chapter Overview]] — The unique challenges and benefits of semiconductor-based storage.
- [[Flash Memory Basics - Pages Blocks and Erasure Asymmetry]] — The fundamental hardware constraints of flash memory.

## File Systems
Abstractions for naming, organizing, and protecting persistent data.
- [[File Systems - Chapter Overview]] — The fundamental API for files and directories.
- [[VSFS Disk Layout - Superblock Bitmaps and Regions]] — The implementation of a simple, on-disk file system.
- [[Crash Consistency - Chapter Overview]] — How journaling and fsck protect against power loss.
- [[Journaling Provides Crash Consistency via Write-Ahead Logging]] — The primary mechanism for ensuring file system integrity.
- [[Log-Structured File Systems - Chapter Overview]] — A write-optimized design that treats the disk as a log.
- [[The Inode Map Tracks the Location of Inodes in LFS]] — The indirection mechanism that enables a moving file system.
- [[Data Integrity and Protection - Chapter Overview]] — Mechanisms like checksums and scrubbing for detecting silent corruption.
- [[Checksums Enable Detection of Data Corruption]] — Using mathematical summaries to verify data integrity.

## Distributed FS
Sharing files across a network.
- [[Distributed FS - Chapter Overview]] — Introduction to the challenges of remote file access.
- [[NFS Architecture - Client-Server and the VFS Layer]] — The design of Sun's stateless network file system.
- [[Stateless Protocol Design in NFS]] — How NFS achieves robustness through simplicity.
- [[AFS Architecture - Whole-File Caching on Local Disk]] — Carnegie Mellon's scalable distributed file system.
- [[AFS Callbacks - Server-Initiated Cache Invalidation]] — Managing cache consistency at scale.
- [[AFS vs NFS Comparison - Scalability and Consistency]] — Trade-offs between the two major distributed storage philosophies.