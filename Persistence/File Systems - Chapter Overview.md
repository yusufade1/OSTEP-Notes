---
type: overview
source: "OSTEP Ch. 39: Interlude: Files and Directories"
tags:
  - file-system
  - api
  - persistence
  - chapter-overview
related:
  - "[[Persistence MOC]]"
  - "[[IO and Storage - Chapter Overview]]"
  - "[[The Address Space Abstracts Physical Memory for Each Process]]"
prerequisites:
  - "[[IO and Storage - Chapter Overview]]"
---

> [!SUMMARY]
> The file system provides a persistent, named view of storage, abstracting physical disk blocks into files and directories. This chapter covers the fundamental API used to create, access, and manage these objects, including the `open()`, `read()`, `write()`, and `fsync()` system calls for files, and `mkdir()`, `readdir()`, and `rmdir()` for directories.

### Core Abstractions
The virtualization of storage relies on two key abstractions:
*   **[[Files are Named Sequences of Bytes]]:** Linear arrays of bytes that persist across reboots. The OS provides no structure to the data; it is just a stream of bytes to be interpreted by applications.
*   **[[Directories Map Names to Inode Numbers]]:** Special files that store a list of (name, inode number) pairs, creating the hierarchical namespace we use to organize data.

### The File API
Interacting with files involves a sequence of system calls:
*   **[[The open() System Call Creates and Accesses Files]]:** Returns a file descriptor, a capability used for subsequent operations.
*   **[[read() and write() Access Data sequentially]]:** Read from or write to the current offset, which the OS updates automatically.
*   **[[lseek() Repositions the File Offset]]:** Allows random access within a file.
*   **[[fsync() Forces Writes to Persistent Storage]]:** Ensures data is physically written to the disk, critical for database reliability.

### The Directory API
Directories are manipulated differently than files:
*   **[[mkdir() Creates New Directories]]:** Creates a new directory entry.
*   **[[readdir() Iterates Over Directory Entries]]:** Reads the contents (name, inode) of a directory.
*   **[[rmdir() Removes Empty Directories]]:** Deletes a directory if it contains no files.

### Metadata and Links
*   **[[File Metadata describes File Attributes]]:** Accessed via `stat()`, this includes permissions, size, and modification times.
*   **[[Hard Links vs Symbolic Links]]:** Two ways to create multiple names for the same file, with different behaviors regarding deletion and cross-filesystem linking.
