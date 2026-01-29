---
type: mechanism
source: "OSTEP Ch. 43: Log-structured File Systems"
tags:
  - file-system
  - lfs
  - metadata
  - persistence
related:
  - "[[VSFS Inode Structure and Block Pointers]]"
  - "[[LFS Write Buffering Groups Small Updates into Large Segments]]"
  - "[[The Checkpoint Region Points to the Current Inode Map in LFS]]"
prerequisites:
  - "[[VSFS Inode Structure and Block Pointers]]"
  - "[[LFS Write Buffering Groups Small Updates into Large Segments]]"
---

# The Inode Map Tracks the Location of Inodes in LFS

> [!SUMMARY]
> In LFS, inodes are no longer stored in fixed locations; they are written to the end of the log alongside data blocks. To find the current version of an inode, LFS introduces the **Inode Map (imap)**—a data structure that maps an inode number to its current on-disk physical address, providing the necessary indirection for a moving file system.

In traditional file systems like VSFS or FFS, finding an inode is easy because they are stored in fixed "inode tables" at known disk offsets. In LFS, however, every time a file is updated, a new version of its inode is written to the end of the log. This creates a "moving target" problem: if the inode is always moving, how does the OS find it?

## The Imap Solution
The **Inode Map** is an array where the $i$-th entry contains the disk address of inode $i$. By consulting the imap, the OS can find the most recent version of any inode. 

> [!VISUAL]+ Inferred: Indirection Layer
> Traditional FS: `Inode Number` → `Fixed Disk Address`
> LFS: `Inode Number` → `Inode Map (imap)` → `Moving Disk Address`

## Where is the Imap Stored?
If the imap were stored in a fixed location on disk, updating it would require a random write every time a segment is flushed, defeating the purpose of LFS. Therefore, LFS stores the imap **in the log itself**. 

When LFS writes a segment of data and inodes, it also writes the updated piece of the imap that tracks those inodes. This means the imap itself is also constantly moving across the disk.

## Efficiency and Caching
To avoid a disk read every time a file is accessed, the OS keeps the entire Inode Map in memory. When the file system is mounted, the OS reads the imap from disk once, and subsequently, all lookups are fast memory accesses. Only when the OS needs to find the *latest* pieces of the imap after a reboot does it need a bootstrap mechanism.

## Handling Large Files
For large files, LFS uses the same pointer structure as VSFS (direct, indirect, double-indirect blocks). The key difference is that when a data block at the end of a large file is updated, the OS must also write:
1.  The new **data block**.
2.  The new **indirect block** (pointing to the new data block).
3.  The new **inode** (pointing to the new indirect block).
4.  The new **imap piece** (pointing to the new inode).

This "recursive update" ensures that every modified part of the tree is eventually captured in the sequential log.

## Connections
- Replaces the fixed-location assumption of [[VSFS Inode Structure and Block Pointers]].
- Relies on [[The Checkpoint Region Points to the Current Inode Map in LFS]] to find the start of the imap chain.
- Is updated during every [[LFS Write Buffering Groups Small Updates into Large Segments|segment write]].
