---
type: concept
source: "OSTEP Ch. 39: Interlude: Files and Directories"
tags:
  - file-system
  - api
  - metadata
  - persistence
related:
  - "[[Directories Map Names to Inode Numbers]]"
  - "[[File Metadata describes File Attributes]]"
prerequisites:
  - "[[Directories Map Names to Inode Numbers]]"
---

> [!SUMMARY]
> Links provide mechanisms to create multiple names for a file. **Hard links** connect a filename directly to an inode; deleting a hard link simply decrements a reference count, and the file data remains until the count hits zero. **Symbolic (soft) links** are special files that contain a pathname to another file; deleting the target leaves the link "dangling."

Unix file systems offer two ways to link names to data.

### Hard Links (`link()`)
A hard link is simply another directory entry pointing to the *same* inode number.
*   **Creation:** `link("/old", "/new")` makes `/new` point to the inode of `/old`.
*   **Inode:** Both names share the exact same inode. They are indistinguishable.
*   **Deletion:** `unlink("/old")` removes the name and decrements the inode's **reference count**. The file data is freed only when the count reaches 0.
*   **Limitations:** Cannot link to directories (cycles!) and cannot cross file system boundaries (inodes are local to a volume).

### Symbolic Links (`symlink()`)
A symbolic link (soft link) is a file of a special type.
*   **Creation:** `symlink("/target", "/link")`.
*   **Content:** The file's data is literally the string `"/target"`.
*   **Indirection:** When the OS opens a symlink, it reads the content and redirects the access to that path.
*   **Dangling Links:** If `/target` is deleted, `/link` remains but points nowhere.
*   **Flexibility:** Can point to directories and across file systems.
