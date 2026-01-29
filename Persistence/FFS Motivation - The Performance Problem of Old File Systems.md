---
type: mechanism
source: "OSTEP Ch. 41: Locality and The Fast File System"
tags:
  - file-system
  - performance
  - fragmentation
  - ffs
  - persistence
related:
  - "[[FFS Cylinder Groups Improve Locality]]"
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
  - "[[VSFS File Read Path Traces Inode to Data]]"
prerequisites:
  - "[[VSFS File Read Path Traces Inode to Data]]"
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
---

> [!SUMMARY]
> Before the Berkeley Fast File System (FFS), the original Unix File System (UFS) suffered from extreme performance degradation as disks aged. By treating the disk as a flat array of blocks without considering physical geometry, it created a "locality-blind" environment where related data blocks were scattered across the platter, causing throughput to drop to a tiny fraction of the disk's potential.

The primary motivation for FFS was the abysmal performance of the original "Old" Unix File System. While simple to implement, the old system failed to account for the physical realities of hard disk drives—specifically that seeks are expensive and locality is paramount for performance.

### The Locality Problem
In the old file system, the disk was partitioned into fixed regions: all inodes were at the beginning of the disk, and all data blocks followed. This separation meant that even a simple task like reading a single file required a long seek from the inode table to the data region. As the file system grew and files were created and deleted, the data blocks of a single file would become scattered (fragmented) across the disk. Eventually, reading a file was more like a random I/O workload than a sequential one.

### Fragmentation and Block Size
The old file system used small blocks (typically 512 bytes). This was efficient for storage (minimizing internal fragmentation) but disastrous for performance. Each 512-byte transfer required its own I/O operation. Even if blocks were somewhat contiguous, the overhead of managing many small transfers prevented the system from ever reaching the disk's peak transfer rates.

### Performance Degradation
The most famous observation regarding the old file system was that its performance was "good when new" but "bad when old." As free space became fragmented, the allocator would pick any available block, regardless of where the disk arm was currently positioned. Measurements showed that throughput could drop from a theoretical maximum down to roughly 2-4% of the disk's bandwidth. FFS was designed to fix this by making the file system "disk aware."
