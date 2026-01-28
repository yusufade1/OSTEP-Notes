---
type: atomic
source: OSTEP Ch. 39
tags: [file-system, api, persistence]
related: [[read() and write() Access Data sequentially]], [[The open() System Call Creates and Accesses Files]]
prerequisites: [[read() and write() Access Data sequentially]]
---

> [!SUMMARY]
> The `lseek()` system call enables random access to file data by manually repositioning the implicit file offset. It allows a process to skip over data or return to a previous position without closing and reopening the file.

While `read()` and `write()` naturally process files sequentially, some applications (like databases) need to jump to specific locations. `lseek()` provides this capability.

### The API
```c
off_t lseek(int fd, off_t offset, int whence);
```

### The `whence` Parameter
The behavior depends on how the new position is defined:
1.  **`SEEK_SET`**: Set the offset to `offset` bytes from the **beginning** of the file.
    *   `lseek(fd, 100, SEEK_SET)` moves to byte 100.
2.  **`SEEK_CUR`**: Set the offset to its **current** location plus `offset`.
    *   `lseek(fd, 10, SEEK_CUR)` skips forward 10 bytes.
3.  **`SEEK_END`**: Set the offset to the **size of the file** plus `offset`.
    *   `lseek(fd, 0, SEEK_END)` moves to the end (useful for appending or checking file size).

### Note on "Seeking"
The term "seek" here refers to the logical file offset in the OS structure. It does *not* necessarily imply a physical disk seek (moving the disk arm), though a subsequent read from the new location likely will.
