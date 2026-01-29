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
  - "[[mkdir() Creates New Directories]]"
prerequisites:
  - "[[Directories Map Names to Inode Numbers]]"
---

> [!SUMMARY]
> The `readdir()` system call (along with `opendir()` and `closedir()`) allows applications to iterate through the contents of a directory. It abstracts the underlying storage format of directory entries, providing a sequence of `dirent` structures that contain the name and inode number of each file. This interface is essential because directory data structures vary widely between file system implementations.

Because directory formats vary (e.g., simple linear lists, complex B-trees), the OS provides an abstract iterator API rather than raw read access to directory bytes.

### The API Flow
Iterating a directory involves three steps:
1.  **Open:** `DIR *dp = opendir(".")` creates an iterator object for the directory.
2.  **Iterate:** `readdir(dp)` returns the next entry or `NULL` when finished.
3.  **Close:** `closedir(dp)` releases the resources associated with the iterator.

```c
#include <dirent.h>
DIR *dp = opendir(".");
struct dirent *d;
while ((d = readdir(dp)) != NULL) {
    printf("%lu %s\n", d->d_ino, d->d_name);
}
closedir(dp);
```

### The `dirent` Structure
The standard guarantees at least two fields in the returned structure:
1.  **`d_name`:** The filename (null-terminated string).
2.  **`d_ino`:** The inode number.

### Practical Considerations
*   **Ordering:** The order of returned entries is not guaranteed (it depends on the internal file system layout).
*   **Special Entries:** The iteration always includes `.` (current) and `..` (parent). Recursive algorithms (like a directory walker) must explicitly check for and skip these names to avoid infinite recursion loops.
*   **Concurrency:** If a directory is modified (files added/removed) while iterating, the behavior depends on the specific implementation.