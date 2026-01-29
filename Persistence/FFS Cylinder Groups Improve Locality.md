---
type: mechanism
source: "OSTEP Ch. 41: Locality and The Fast File System"
tags:
  - file-system
  - implementation
  - locality
  - performance
  - persistence
related:
  - "[[VSFS Disk Layout - Superblock Bitmaps and Regions]]"
  - "[[FFS Allocation Policies Optimize Seek Times]]"
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
  - "[[FFS Motivation - The Performance Problem of Old File Systems]]"
prerequisites:
  - "[[VSFS Disk Layout - Superblock Bitmaps and Regions]]"
---

> [!SUMMARY]
> The original Unix file system treated the disk as a single uniform array of blocks, leading to severe fragmentation and long seek times as data spread randomly over time. The Berkeley Fast File System (FFS) addressed this by dividing the disk into smaller, independent regions called **cylinder groups**. By placing related data (like a file's inode and its content) within the same group, FFS minimizes disk arm movement.

The "Old" Unix file system (similar to VSFS) had a major performance problem: it didn't care about **locality**.
*   **The Problem:** Inodes were at the start of the disk; data was at the end. Reading a file required a long seek from inode to data. Over time, free space became fragmented, scattering file blocks across the entire platter.
*   **Performance:** Throughput dropped to ~2% of the disk's bandwidth.

### Cylinder Groups
FFS partitions the disk into $N$ **cylinder groups** (similar to block groups in Ext2/3/4).
*   **Structure:** Each group contains a copy of the superblock (for redundancy), per-group inode/data bitmaps, a region for inodes, and a data region.
*   **Goal:** A cylinder group is essentially a mini-filesystem. FFS tries to allocate a file's metadata and data within the *same* group.
*   **Result:** Seeks are effectively restricted to the small physical range of a single group, significantly reducing seek time.
