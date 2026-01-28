---
type: atomic
source: OSTEP Ch. 42
tags: [file-system, crash-consistency, persistence]
related:
  - [[The Crash Consistency Problem Arises from Partial Disk Updates]]
  - [[VSFS File Write Path Involves Allocation and Metadata Updates]]
prerequisites:
  - [[The Crash Consistency Problem Arises from Partial Disk Updates]]
---

> [!SUMMARY]
> Partial writes during a file system update lead to various crash scenarios, each resulting in specific types of inconsistency between inodes, bitmaps, and data blocks.

When appending a block to a file, the OS must update the Inode (I), Bitmap (B), and Data block (D). If a crash occurs, any combination of these may have reached the disk. Excluding the "all or none" cases, we have several problematic scenarios:

1. **Only the Data Block (D) is written:** While the data is on disk, neither the inode nor the bitmap knows about it. From the file system's perspective, no change occurred. This is "consistent" but the write was lost.
2. **Only the Inode (I) is written:** The inode points to a block (D), but the bitmap (B) says D is free. If we read the file, we get "garbage" data. Worse, if we later allocate a new file, the OS might give it block D, leading to two inodes pointing to the same block.
3. **Only the Bitmap (B) is written:** The bitmap says block D is used, but no inode points to it. This results in a **space leak**; block D is effectively lost to the system until a repair tool like `fsck` scans the entire disk.
4. **Inode (I) and Bitmap (B) are written, but not Data (D):** The metadata is consistent—the file thinks it has the block, and the bitmap confirms it is allocated. However, the data at that location is old or garbage, leading to a "point to garbage" inconsistency.
5. **Inode (I) and Data (D) are written, but not Bitmap (B):** Similar to the "Only Inode" case, the file points to the correct data, but the bitmap says the block is free. This is highly dangerous as the block can be overwritten by a subsequent allocation.

These scenarios demonstrate why the order of writes and the atomicity of the group of writes are critical. Traditional file systems often relied on specific write ordering to minimize damage, but modern systems use journaling to ensure atomicity.
