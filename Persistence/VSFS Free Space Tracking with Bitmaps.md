---
type: mechanism
source: "OSTEP Ch. 40: File System Implementation"
tags:
  - file-system
  - implementation
  - allocation
  - persistence
related:
  - "[[VSFS Disk Layout - Superblock Bitmaps and Regions]]"
  - "[[Splitting and Coalescing Keep the Free List Efficient]]"
prerequisites:
  - "[[VSFS Disk Layout - Superblock Bitmaps and Regions]]"
---

> [!SUMMARY]
> VSFS manages free space using bitmaps: one for inodes and one for data blocks. A bitmap is a compact array of bits where each bit represents the state of a corresponding object (0 for free, 1 for allocated). This structure allows for fast allocation and easy identification of contiguous free blocks.

Unlike memory managers that often use free lists (linked lists of free chunks), file systems like VSFS often use **bitmaps**.

### The Mechanism
*   **Inode Bitmap:** If bit $N$ is 0, then the $N$-th inode in the Inode Table is free.
*   **Data Bitmap:** If bit $M$ is 0, then the $M$-th block in the Data Region is free.

### Advantages
1.  **Space Efficiency:** A single 4 KB block can track $4096 \times 8 = 32,768$ blocks. For a 4 KB block size, one bitmap block covers 128 MB of disk space.
2.  **Contiguity:** Bitmaps make it easy to find a *sequence* of free blocks (e.g., looking for a run of 0s). This helps in keeping large files contiguous on disk, improving sequential read performance.

### Allocation logic
When creating a file:
1.  Read inode bitmap.
2.  Find first 0 bit.
3.  Set to 1.
4.  Write bitmap back to disk.
5.  Use the corresponding inode index.
(Similar process for allocating data blocks when writing to the file).
