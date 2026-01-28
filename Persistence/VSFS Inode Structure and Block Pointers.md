---
type: atomic
source: OSTEP Ch. 40
tags: [file-system, implementation, inode, persistence]
related: [[VSFS Disk Layout - Superblock Bitmaps and Regions]], [[File Metadata describes File Attributes]]
prerequisites: [[VSFS Disk Layout - Superblock Bitmaps and Regions]]
---

> [!SUMMARY]
> The inode (index node) is the on-disk structure that represents a specific file. It contains metadata (permissions, size) and a multi-level index of block pointers. VSFS uses a set of direct pointers for small files and an indirect pointer (pointing to a block of pointers) to support larger files, balancing efficient access with capacity.

An **inode** is a fixed-size structure (e.g., 256 bytes) identified by its index in the Inode Table.

### Metadata Content
The inode stores everything *except* the filename and the data content:
*   **Mode:** File type (regular, dir) and permissions (rwx).
*   **Size:** Current file size in bytes.
*   **Links:** Reference count (for hard links).
*   **Time:** Access/Modify/Change timestamps.

### Block Pointers (The Index)
The critical job of the inode is to map logical file offsets to physical disk blocks. VSFS uses an imbalanced tree structure:
1.  **Direct Pointers:** The first 12 pointers in the inode point directly to data blocks.
    *   *Capacity:* $12 	imes 4	ext{ KB} = 48	ext{ KB}$.
    *   *Speed:* Accessing small files requires only fetching the inode.
2.  **Indirect Pointer:** The 13th pointer points to a **data block** that contains *more* pointers (e.g., 1024 pointers in a 4 KB block).
    *   *Capacity:* $1024 	imes 4	ext{ KB} = 4	ext{ MB}$.
    *   *Speed:* Requires two disk reads (inode + pointer block) to find data.
3.  **Double Indirect Pointer:** Points to a block of indirect pointers (supporting GB-sized files).

This design relies on the assumption that most files are small (handled by direct pointers), while still allowing rare large files to exist.
