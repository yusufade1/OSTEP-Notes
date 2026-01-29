---
type: mechanism
source: "OSTEP Ch. 41: Locality and The Fast File System"
tags:
  - file-system
  - implementation
  - efficiency
  - ffs
  - persistence
related:
  - "[[FFS Motivation - The Performance Problem of Old File Systems]]"
  - "[[VSFS Inode Structure and Block Pointers]]"
prerequisites:
  - "[[FFS Motivation - The Performance Problem of Old File Systems]]"
---

> [!SUMMARY]
> To improve performance, FFS increased the base block size (e.g., from 512 bytes to 4 KB or 8 KB). However, this larger size caused significant **internal fragmentation** for small files. FFS solved this with **sub-block allocation** (or fragments), allowing the system to divide a single block into smaller units (e.g., 1 KB) to store multiple small files or the tails of larger files efficiently.

One of the key performance upgrades in FFS was increasing the file system block size. Larger blocks allow for more data to be transferred per I/O operation and reduce the overhead of metadata (fewer block pointers needed for large files). However, moving from 512-byte blocks to 4 KB or 8 KB blocks created a massive storage efficiency problem: internal fragmentation.

### The Fragmentation Problem
If a file system uses 4 KB blocks, a file that is only 100 bytes still consumes an entire 4 KB block. In a typical Unix system with many small files, this can lead to nearly 50% of the disk space being wasted as "slack space" within blocks.

### The Fragment Solution
FFS introduced **fragments** (often 1 KB in an 8 KB block system). The file system can allocate these sub-blocks to small files.
*   **Initial Allocation:** A small file starts by being allocated one or more fragments.
*   **Copy-on-Growth:** As the file grows, FFS continues to allocate fragments until the file reaches a full block's worth of data (e.g., 8 fragments).
*   **Promotion:** Once the file is large enough, FFS finds a full block, copies the data from the fragments into that block, and frees the fragments for other small files to use.

### Implementation Complexity
This optimization introduced significant complexity to the OS. The `write()` system call had to handle the logic of copying data from fragments to full blocks when files grew. Despite the complexity, sub-block optimization was essential for making large-block file systems practical for general-purpose computing where small files are common.
