---
type: atomic
source: OSTEP Ch. 39
tags: [file-system, api, metadata, persistence]
related: [[Directories Map Names to Inode Numbers]], [[Files are Named Sequences of Bytes]]
prerequisites: [[Files are Named Sequences of Bytes]]
---

> [!SUMMARY]
> File systems store metadata—information *about* a file—separate from the file's content. This metadata, stored in a structure called an inode, includes the file's size, permissions, owner, timestamps, and block locations. The `stat()` system call allows applications to retrieve this information without reading the file itself.

To the user, a file is a name and some data. To the file system, a file is an **inode** (index node).

### The Inode
The inode is the persistent on-disk structure that describes a file. It typically contains:
*   **Type:** Is it a regular file, directory, or symbolic link?
*   **Size:** Number of bytes in the file.
*   **Blocks:** Number of disk blocks allocated.
*   **Protection:** Permissions (Read/Write/Execute) for Owner, Group, and Others.
*   **Time:** Access time (`atime`), modification time (`mtime`), and change time (`ctime`).
*   **Links:** Reference count (number of hard links).

### The `stat()` API
Applications use `stat()` to inspect this metadata.

```c
struct stat sb;
stat("foo.txt", &sb);
printf("Size: %ld
", sb.st_size);
printf("Inode: %ld
", sb.st_ino);
```

### Note on Filenames
Crucially, the **filename is NOT stored in the inode**. The filename lives in the *directory* entry that points to the inode. This separation allows a single file (inode) to have multiple names (hard links).
