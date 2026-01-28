---
type: atomic
source: OSTEP Ch. 39
tags: [file-system, api, directory, persistence]
related: [[mkdir() Creates New Directories]], [[Directories Map Names to Inode Numbers]]
prerequisites: [[Directories Map Names to Inode Numbers]]
---

> [!SUMMARY]
> The `rmdir()` system call removes a directory from the file system. A critical constraint is that the directory must be empty (containing only `.` and `..`) before it can be removed. This simple rule prevents the creation of orphaned subtrees (files disconnected from the root) and simplifies the implementation of tree traversal and reference counting.

Removing a directory is safer than removing a file because of a key restriction.

### The API
```c
int rmdir(const char *pathname);
```

### The Empty Constraint
`rmdir()` fails with `ENOTEMPTY` if the directory contains any user files or subdirectories.
*   **Why?** If you deleted a non-empty directory, all files inside it would become **orphans**: they would still exist on disk (allocated inodes), but there would be no path from the root to reach them. They would be effectively lost to the user but still consuming space.

### Recursive Deletion
Commands like `rm -rf` are not system calls. They are user-space programs that:
1.  Recursively descend the tree.
2.  Unlink all files in the leaves.
3.  Call `rmdir()` on the now-empty directories as they unwind the recursion.
