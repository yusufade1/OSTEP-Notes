---
type: concept
source: "OSTEP Ch. 39: Interlude: Files and Directories"
tags:
  - file-system
  - api
  - persistence
related:
  - "[[read() and write() Access Data sequentially]]"
  - "[[Files are Named Sequences of Bytes]]"
  - "[[Device Interface Exposes Registers for Status Command and Data]]"
prerequisites:
  - "[[Files are Named Sequences of Bytes]]"
---

> [!SUMMARY]
> The `open()` system call is the entry point for file access. It takes a pathname and flags (e.g., read-only, create if missing, truncate) and returns a file descriptor. This descriptor is a private, per-process integer handle used for subsequent operations, decoupling the filename resolution from data access.

To access a file, a process must first **open** it.

```c
#include <fcntl.h>
int fd = open("foo", O_CREAT | O_WRONLY | O_TRUNC, S_IRUSR | S_IWUSR);
```

### Key Parameters
1.  **Pathname:** The name of the file to open (e.g., `"foo"`).
2.  **Flags:** Control the behavior.
    *   `O_CREAT`: Create the file if it doesn't exist.
    *   `O_WRONLY`: Open for writing only.
    *   `O_TRUNC`: If the file exists, truncate it (delete contents) to size 0.
3.  **Mode:** Permissions to use if creating the file (e.g., User Read/Write).

### The File Descriptor
On success, `open()` returns a **file descriptor (fd)**.
*   **Integer Handle:** It's just a small integer (e.g., 3).
*   **Per-Process Scope:** The fd is an index into the process's **open file table**.
*   **Capability:** Possessing the fd grants the capability to read/write the file without re-checking permissions or re-traversing the directory path.

Standard descriptors:
*   0: Standard Input (stdin)
*   1: Standard Output (stdout)
*   2: Standard Error (stderr)
