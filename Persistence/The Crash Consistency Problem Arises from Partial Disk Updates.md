---
type: atomic
source: OSTEP Ch. 42
tags: [file-system, crash-consistency, persistence]
related:
  - [[VSFS File Write Path Involves Allocation and Metadata Updates]]
  - [[Journaling Provides Crash Consistency via Write-Ahead Logging]]
  - [[fsck Recovers File System Integrity via Post-Crash Scanning]]
prerequisites:
  - [[VSFS File Write Path Involves Allocation and Metadata Updates]]
---

> [!SUMMARY]
> The crash consistency problem occurs when a system crash or power failure interrupts a multi-block file system update, leaving the on-disk data structures in an inconsistent state.

A fundamental challenge for any file system is maintaining consistent on-disk structures in the face of unexpected system interruptions. A simple operation from the user's perspective, such as appending a single data block to an existing file, is actually a complex multi-step process for the operating system. In a typical implementation like the Very Simple File System (VSFS), this append requires updating three distinct on-disk structures: the data bitmap (to mark the new block as used), the inode (to update the file size and add the new pointer), and the data block itself.

Because disks can only guarantee that a single sector write is atomic, the operating system cannot ensure that all three blocks are written simultaneously. If a power loss or kernel panic occurs while these writes are being issued to the disk, only a subset of them may actually persist. This leads to the "Crash Consistency Problem": the on-disk state no longer reflects a valid or consistent file system.

For instance, if only the data block is written, the file system remains consistent but the data is lost (or "phantom"). However, if only the inode is updated, it will point to a block that is still marked as free in the bitmap, creating a serious inconsistency. If that block is later assigned to a new file, the first file's pointer will point to the second file's data, leading to corruption. The goal of crash recovery mechanisms is to ensure that despite such interruptions, the file system can be restored to a sensible, consistent state where all metadata correctly describes the allocated data.
