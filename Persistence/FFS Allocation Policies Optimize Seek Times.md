---
type: atomic
source: OSTEP Ch. 41
tags: [file-system, implementation, allocation, persistence]
related: [[FFS Cylinder Groups Improve Locality]], [[Directories Map Names to Inode Numbers]], [[FFS Large File Exception Prevents Single Group Saturation]]
prerequisites: [[FFS Cylinder Groups Improve Locality]]
---

> [!SUMMARY]
> FFS employs distinct placement policies for directories and files to balance locality with capacity. Directories are spread across cylinder groups to distribute metadata load, while files are allocated in the *same* group as their parent directory to ensure that reading a directory and its contents involves minimal seeking.

Having cylinder groups is only useful if the file system uses them intelligently. FFS defined two key policies:

### 1. Placing Directories
**Goal:** Distribute metadata evenly across the disk so no single group fills up.
**Policy:** Find the cylinder group with a low number of allocated directories and a high number of free inodes. Put the new directory there.
*   **Effect:** The directory tree is spread out. `/home/user` might be in Group 10, while `/home/user/docs` might be in Group 55.

### 2. Placing Files
**Goal:** Maximize data locality (keep bits close to their name).
**Policy:** Allocate the file's inode and data blocks in the **same** cylinder group as the directory containing the file.
*   **Effect:** Reading `/home/user/foo.txt` is fast. The inode for the directory, the directory data (mapping `foo.txt`), the inode for `foo.txt`, and the data for `foo.txt` are likely all in the same physical region.

### The Conflict
These policies balance "clumping" (files near parents) with "spreading" (directories far from each other), achieving high performance for common access patterns like `ls -l` or `grep -r`.
