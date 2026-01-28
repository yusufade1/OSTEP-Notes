---
type: atomic
source: OSTEP Ch. 39
tags: [file-system, api, persistence]
related: [[The open() System Call Creates and Accesses Files]], [[lseek() Repositions the File Offset]]
prerequisites: [[The open() System Call Creates and Accesses Files]]
---

> [!SUMMARY]
> The `read()` and `write()` system calls allow processes to access file data sequentially. The operating system maintains a current file offset for each open file; reading or writing advances this offset automatically, enabling simple loops to process entire files.

Once a file is open, `read()` and `write()` are the primary methods for data transfer.

### The API
```c
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
```
*   **fd:** The file descriptor returned by `open()`.
*   **buf:** Pointer to the buffer in memory to read into or write from.
*   **count:** The number of bytes to transfer.
*   **Return:** The number of bytes actually transferred (or -1 on error).

### Sequential Access and the Offset
The OS tracks a **current file offset** for each open file.
1.  **Starts at 0:** When a file is opened, the offset is typically 0 (beginning).
2.  **Auto-Update:** If you read $N$ bytes, the OS updates the offset: `offset += N`.
3.  **Next Call:** The next `read()` starts from the new offset.

### Example: Reading a File
```c
int fd = open("foo", O_RDONLY);
char buffer[100];
while (read(fd, buffer, sizeof(buffer)) > 0) {
    // Process buffer
}
close(fd);
```
This loop naturally reads the file from start to finish without needing manual pointer arithmetic.
