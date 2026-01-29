---
type: concept
source: "OSTEP Ch. 39: Interlude: Files and Directories"
tags:
  - file-system
  - api
  - abstraction
  - persistence
related:
  - "[[Directories Map Names to Inode Numbers]]"
  - "[[File Metadata describes File Attributes]]"
  - "[[The open() System Call Creates and Accesses Files]]"
prerequisites:
  - "[[File Systems - Chapter Overview]]"
---

> [!SUMMARY]
> A file is the fundamental unit of storage in an operating system, modeled simply as a linear array of bytes. To the OS, the content is opaque; it does not enforce structure (like records or fields). Each file is uniquely identified by a low-level integer name called an inode number, while users refer to files by human-readable pathnames.

The **file** is the primary abstraction used to virtualize storage devices. While the disk is physically a collection of fixed-size sectors, the OS presents a view of named, variable-size data containers.

### The Byte Stream Model
In Unix-like systems (and OSTEP's model), a file is just a **sequence of bytes**.
*   **No Structure:** The OS doesn't know if a file is a text document, a JPEG image, or a compiled binary. It simply stores and retrieves the bytes as requested.
*   **Interpretation:** The meaning of the data is determined entirely by the application reading it.

### Naming
Files have two names:
1.  **Inode Number:** The low-level name used by the OS (e.g., `1024`). It points to the metadata structure (inode) describing the file.
2.  **Pathname:** The high-level, human-readable name (e.g., `/home/user/notes.txt`). The file system's directory structure is responsible for mapping these pathnames to the underlying inode numbers.

### Persistence
Unlike memory, data written to a file **persists** across system crashes and power cycles. This durability is achieved by writing the data to non-volatile storage media (hard drives, SSDs).
