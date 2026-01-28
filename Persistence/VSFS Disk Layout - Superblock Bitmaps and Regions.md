---
type: atomic
source: OSTEP Ch. 40
tags: [file-system, implementation, vsfs, persistence]
related: [[VSFS Inode Structure and Block Pointers]], [[VSFS Free Space Tracking with Bitmaps]], [[File Systems - Chapter Overview]]
prerequisites: [[File Systems - Chapter Overview]]
---

> [!SUMMARY]
> The Very Simple File System (VSFS) organizes the disk into fixed-size blocks. The layout is divided into distinct regions: a superblock containing global metadata, bitmaps for tracking free inodes and data blocks, an inode table storing per-file metadata, and a data region holding the actual file contents.

To implement a file system, we must map logical structures (files, directories) to physical disk blocks. VSFS uses a simple, rigid layout.

### The Block View
The disk is viewed as a linear array of blocks, typically 4 KB each.
*   **Total Blocks:** If the partition is 64 blocks, we address them as 0..63.

### The Regions
1.  **Superblock (Block 0):** Contains critical information about the file system itself, such as the total number of blocks, number of inodes, and the file system type. If this is corrupt, the volume is unmountable.
2.  **Bitmaps (Blocks 1-2):**
    *   **Inode Bitmap (Block 1):** Tracks which inodes are allocated (1) or free (0).
    *   **Data Bitmap (Block 2):** Tracks which data blocks are allocated or free.
3.  **Inode Table (Blocks 3-7):** A reserved region to store inodes. If an inode is 256 bytes and a block is 4 KB, each block holds 16 inodes. 5 blocks = 80 inodes total.
4.  **Data Region (Blocks 8-63):** The largest portion, used to store user file data and directory entries.

### ASCII Layout Diagram
```text
[S] [i] [d] [I I I I I] [D D D D D D D D ...]
 ^   ^   ^   ^           ^
 |   |   |   |           +-- Data Region (User content)
 |   |   |   +-- Inode Table (Metadata)
 |   |   +-- Data Bitmap
 |   +-- Inode Bitmap
 +-- Superblock
```
This static partitioning is simple but inflexible (e.g., you can run out of inodes while having plenty of data space).
