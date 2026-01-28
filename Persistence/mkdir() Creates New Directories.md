---
type: atomic
source: OSTEP Ch. 39
tags: [file-system, api, directory, persistence]
related: [[Directories Map Names to Inode Numbers]], [[readdir() Iterates Over Directory Entries]], [[rmdir() Removes Empty Directories]]
prerequisites: [[Directories Map Names to Inode Numbers]]
---

> [!SUMMARY]
> The `mkdir()` system call allows users to create new directories. Unlike creating regular files with `open()`, `mkdir()` enforces the specific structure of directory entries, automatically initializing the mandatory `.` (self) and `..` (parent) links to maintain the consistency of the file system tree.

Directories cannot be written to as byte streams; they must be manipulated structurally.

### The API
```c
int mkdir(const char *pathname, mode_t mode);
```
*   **pathname:** The name of the new directory.
*   **mode:** The access permissions.

### What Happens
When `mkdir("foo")` is called:
1.  **Allocate Inode:** The file system finds a free inode and marks it as a directory type.
2.  **Add Entry:** An entry `("foo", inode_number)` is added to the **parent** directory.
3.  **Initialize Content:** The new directory is initialized with two entries:
    *   `.` pointing to itself.
    *   `..` pointing to the parent directory.

This atomic setup ensures the tree structure is never left in an invalid state where a directory lacks a link back to its parent.
