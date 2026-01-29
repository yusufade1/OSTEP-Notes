---
type: mechanism
source: "OSTEP Ch. 40: File System Implementation"
tags:
  - file-system
  - implementation
  - performance
  - persistence
related:
  - "[[fsync() Forces Writes to Persistent Storage]]"
  - "[[VSFS Free Space Tracking with Bitmaps]]"
prerequisites:
  - "[[VSFS File Read Path Traces Inode to Data]]"
---

> [!SUMMARY]
> Writing to a file is significantly more complex than reading because it involves allocation. Creating a new file or appending data requires updating the data bitmap (to mark blocks used), the inode bitmap (if new file), the inode itself (size, timestamps, block pointers), and the parent directory (if new file), in addition to writing the actual data.

Writing a new file `/foo/bar` involves 5 separate I/O operations for a single data block write.

### The Write Sequence
Assume the file `bar` has just been created (open has completed). We now write 4 KB.
1.  **Read Data Bitmap:** The FS must find a free block. It reads the bitmap.
2.  **Write Data Bitmap:** It sets the bit to 1 (allocated) and writes the bitmap back to disk.
3.  **Read Inode:** It reads the file's inode to update it.
4.  **Write Inode:** It updates the inode with the new block pointer and new file size, then writes it back.
5.  **Write Data:** Finally, it writes the user's data to the newly allocated block.

### The Crash Consistency Problem
This sequence highlights a major reliability risk. If the power fails after step 2 (bitmap updated) but before step 5 (data written), the file system thinks the block is used, but it contains garbage (or belongs to no file). This **inconsistency** is the motivation for journaling.
