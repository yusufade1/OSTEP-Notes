---
type: mechanism
source: "OSTEP Ch. 40: File System Implementation"
tags:
  - file-system
  - implementation
  - directory
  - persistence
related:
  - "[[Directories Map Names to Inode Numbers]]"
  - "[[VSFS Inode Structure and Block Pointers]]"
prerequisites:
  - "[[Directories Map Names to Inode Numbers]]"
---

> [!SUMMARY]
> In VSFS, a directory is stored exactly like a regular file. The directory's inode points to data blocks, but instead of user content, those blocks contain a list of directory entries. Each entry consists of the file name, the inode number, and the record length (to handle deletion gaps).

To the disk, a directory looks just like a file. It has an inode (type=`directory`) and data blocks. The "magic" is in how the data in those blocks is interpreted.

### Entry Format
A simple linear list of entries might look like this structure:

```c
struct dir_entry {
    char name[252];  // File name
    int  inode;      // Inode number
    int  rec_len;    // Total bytes for this entry
    int  str_len;    // Actual name length
};
```

### Storing Data
If a directory contains `file.txt` (inode 10), the data block holds:
`[ "file.txt", 10, ... ]`

### Handling Deletion
When a file is removed from a directory:
1.  The entry is *not* physically shifted (which would be slow).
2.  Instead, the `inode` field is set to 0 (indicating unused) OR the `rec_len` of the *previous* entry is increased to cover the gap.
3.  Future insertions can reuse the space if the new entry fits.

This is why `readdir()` iterates entries: it scans the data blocks, parsing these structures and skipping empty slots.
