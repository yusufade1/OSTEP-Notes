---
type: atomic
source: OSTEP Ch. 40
tags: [file-system, implementation, performance, persistence]
related: [[The open() System Call Creates and Accesses Files]], [[VSFS Inode Structure and Block Pointers]]
prerequisites: [[VSFS Inode Structure and Block Pointers]]
---

> [!SUMMARY]
> Reading a file `/foo/bar` involves a recursive traversal. The file system starts at the root inode (known location), reads its data to find the entry `foo`, reads `foo`'s inode and data to find `bar`, and finally reads `bar`'s inode to access the user data. This path highlights the high I/O cost of pathname resolution.

To read the file `/foo/bar`, the file system performs many disk I/Os just to find the file.

### Step 1: Open (Pathname Resolution)
1.  **Read Root Inode:** The FS knows the root is usually Inode 2. It reads Inode 2.
2.  **Read Root Data:** Uses Inode 2's pointers to read the root directory's data block. Scans for entry `"foo"`. Found Inode 44.
3.  **Read Inode 44:** Reads the inode for `foo` (a directory).
4.  **Read `foo` Data:** Uses Inode 44's pointers to read `foo`'s content. Scans for entry `"bar"`. Found Inode 55.
5.  **Read Inode 55:** Reads the inode for `bar`.
6.  **Check Permissions:** Verifies access.
7.  **Return FD:** Returns a file descriptor pointing to Inode 55.

### Step 2: Read (Data Access)
1.  **Update Time:** Accessing Inode 55 updates its `atime` (a write to the inode block!).
2.  **Locate Block:** Uses Inode 55's pointers to find the data block for offset 0.
3.  **Read Data:** Reads the actual data block.
4.  **Update Offset:** In memory, updates the file descriptor's offset.

**Total I/O:** Opening a file deep in a tree can generate dozens of reads, motivating the need for caching (dentries).
