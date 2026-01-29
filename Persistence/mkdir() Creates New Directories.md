---
type: concept
source: "OSTEP Ch. 39: Interlude: Files and Directories"
tags:
  - file-system
  - api
  - directory
  - persistence
related:
  - "[[Directories Map Names to Inode Numbers]]"
  - "[[readdir() Iterates Over Directory Entries]]"
  - "[[rmdir() Removes Empty Directories]]"
prerequisites:
  - "[[Directories Map Names to Inode Numbers]]"
---

> [!SUMMARY]
> The `mkdir()` system call allows users to create new directories. Unlike creating regular files with `open()`, `mkdir()` enforces the specific structure of directory entries, automatically initializing the mandatory `.` (self) and `..` (parent) links to maintain the consistency of the file system tree.

Directories cannot be written to as byte streams by user applications; they must be manipulated structurally by the operating system to ensure the integrity of the filesystem hierarchy. Allowing user-level programs to write raw bytes to a directory could result in corrupted filesystem metadata and circular links.

### The API
```c
int mkdir(const char *pathname, mode_t mode);
```
*   **pathname:** The name of the new directory to be created.
*   **mode:** The access permissions (e.g., read, write, execute) for the new directory.

### Internal OS Operations
When a user calls `mkdir("foo")`, the file system must coordinate several low-level updates:
1.  **Allocate Inode:** The OS searches the inode bitmap for a free inode, marks it as used, and initializes it as a directory.
2.  **Add Entry to Parent:** The OS reads the parent directory's data blocks, finds space for a new entry, and writes the name "foo" along with the newly allocated inode number.
3.  **Initialize Directory Blocks:** The OS allocates a data block for the new directory and initializes it with two mandatory entries:
    *   `.` (dot), which points to the directory's own inode number.
    *   `..` (dot-dot), which points to the parent directory's inode number.

### Atomic Creation and Consistency
This structural setup is designed to be atomic from the perspective of the application. By initializing the `.` and `..` entries immediately, the OS ensures that the new directory is a valid node in the filesystem tree from the moment it is visible in the parent. If a crash occurs mid-update, the OS must use mechanisms like journaling to prevent a partially initialized directory from appearing, which would lead to orphans or "dead ends" in the directory traversal process.
