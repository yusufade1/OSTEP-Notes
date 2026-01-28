---
type: atomic
source: OSTEP Ch. 42
tags: [file-system, crash-consistency, recovery]
related:
  - [[The Crash Consistency Problem Arises from Partial Disk Updates]]
  - [[Journaling Provides Crash Consistency via Write-Ahead Logging]]
prerequisites:
  - [[The Crash Consistency Problem Arises from Partial Disk Updates]]
---

> [!SUMMARY]
> The File System Checker (`fsck`) is a system utility that restores consistency by scanning all on-disk metadata after a crash and repairing discovered discrepancies.

In early file systems, the primary solution to the crash consistency problem was the `fsck` tool. Rather than preventing inconsistencies, `fsck` allows them to happen and then fixes them before the file system is mounted again. It operates by performing several passes over the disk:

*   **Superblock Check:** Verifies that the file system size and other global parameters are sane.
*   **Free Block Check:** Scans all inodes to determine which blocks are actually in use. It then compares this to the bitmaps. If an inode points to a block marked free, it updates the bitmap. If a block is marked used but no inode points to it, it marks it free.
*   **Inode State Check:** Checks for corrupted inodes or invalid types.
*   **Inode Links Check:** Verifies the link count for every inode by traversing the entire directory tree. If the counted links don't match the inode's internal count, it corrects the inode.
*   **Directory Checks:** Ensures that directories don't contain pointers to deleted inodes and that the hierarchy is correctly formed.

While effective, the main drawback of `fsck` is its **performance**. Because it must scan the entire disk—including every inode and every directory—the time it takes to run grows linearly with the size of the disk. On modern multi-terabyte drives, a full `fsck` can take hours or even days, which is unacceptable for systems requiring high availability. This limitation led to the development of journaling, which allows for near-instantaneous recovery regardless of disk size.
