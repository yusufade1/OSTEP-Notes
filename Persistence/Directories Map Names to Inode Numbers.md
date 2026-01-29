---
type: concept
source: "OSTEP Ch. 39: Interlude: Files and Directories"
tags:
  - file-system
  - api
  - directory
  - persistence
related:
  - "[[Files are Named Sequences of Bytes]]"
  - "[[readdir() Iterates Over Directory Entries]]"
  - "[[Hard Links vs Symbolic Links]]"
prerequisites:
  - "[[Files are Named Sequences of Bytes]]"
---

> [!SUMMARY]
> A directory is a special type of file whose contents are a list of (entry name, inode number) pairs. This mapping allows the file system to organize files into a hierarchical tree structure. Unlike regular files, directories cannot be written to directly by users; they must be modified using specific system calls like `mkdir` or `rmdir` to ensure structural integrity.

While a file holds user data, a **directory** holds the file system's structure. It transforms the flat list of inodes into the hierarchical tree users interact with.

### Directory Content
Conceptually, a directory is a table of mappings:

| Name | Inode Number |
| :--- | :--- |
| `.` | 5 (Current directory) |
| `..` | 2 (Parent directory) |
| `foo` | 12 |
| `bar` | 13 |

*   **Mapping:** The key function is to map a human-readable name (`foo`) to a low-level identifier (`12`).
*   **Special Entries:**
    *   `.` (dot): Refers to the directory itself.
    *   `..` (dot-dot): Refers to the parent directory.

### Structural Integrity
Because the directory structure defines the file system tree, the OS treats directories as **special files**.
*   **Read-Only (Sort of):** Users can read directory contents (using `ls` or `readdir`), but they cannot open a directory and write arbitrary bytes to it.
*   **Controlled Updates:** To add or remove entries, users must use specific APIs (`mkdir`, `unlink`, `rename`). This prevents users from accidentally creating cycles or disconnecting parts of the tree (creating "orphaned" inodes).
