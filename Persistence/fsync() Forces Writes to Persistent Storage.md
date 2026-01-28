---
type: atomic
source: OSTEP Ch. 39
tags: [file-system, api, reliability, persistence]
related: [[read() and write() Access Data sequentially]], [[Crash Consistency and Journaling]]
prerequisites: [[read() and write() Access Data sequentially]]
---

> [!SUMMARY]
> The `fsync()` system call forces all modified data and metadata for a specific file to be flushed from the OS memory buffer to the physical storage device. This is crucial for applications like databases that require strong durability guarantees, as standard `write()` calls may only update volatile memory.

When a process calls `write()`, the data is usually just copied into a buffer in the OS's memory (page cache). The OS writes it to disk later ("write-back caching") for performance. However, if the system crashes before that write occurs, the data is lost.

### Ensuring Durability
To guarantee that data is safely on the disk platter (or flash), an application must call `fsync()`.

```c
int fd = open("db.log", O_CREAT | O_WRONLY, S_IRUSR | S_IWUSR);
write(fd, buffer, size);
fsync(fd); // Blocks until disk acknowledges the write
close(fd);
```

### Scope
*   **Data and Metadata:** `fsync()` flushes not just the file contents but also essential metadata (like file size) required to access that data.
*   **Directory Sync:** Creating a file updates the *directory*. To ensure a newly created file persists after a crash, you often need to `fsync()` the **parent directory** as well.

### Performance Cost
`fsync()` is expensive because it forces a physical disk I/O and waits for it to complete. Frequent use destroys the performance benefits of write buffering.
