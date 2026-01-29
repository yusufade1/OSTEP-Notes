---
type: mechanism
source: "OSTEP Ch. 42: Crash Consistency: FSCK and Journaling"
tags:
  - file-system
  - crash-consistency
  - journaling
related:
  - "[[Metadata-Only Journaling Optimizes Performance by Excluding Data Blocks]]"
  - "[[Log-Structured File Systems - Chapter Overview]]"
prerequisites:
  - "[[Metadata-Only Journaling Optimizes Performance by Excluding Data Blocks]]"
---

> [!SUMMARY]
> Ordered journaling ensures that user data is physically written to disk before its associated metadata is committed to the journal, preventing files from pointing to stale or sensitive data after a crash.

Ordered journaling is the most common default mode for modern journaling file systems like Ext4. It is an evolution of metadata-only journaling designed to solve the problem of "garbage data" that occurs when metadata is updated before the actual data blocks reach the disk.

In ordered journaling, the OS follows a strict sequence of operations for every update:
1.  **Data Write:** The user data blocks are written to their final locations in the file system.
2.  **Journal Metadata Write:** The metadata changes (inode, inode bitmap, etc.) are written to the log's transaction block.
3.  **Journal Commit:** The transaction's commit block is written to the log.
4.  **Checkpointing:** The metadata changes are eventually written to their permanent locations in the main file system.

By ensuring that step 1 (data) completes before step 3 (commit), the system guarantees that no metadata will ever point to a block that hasn't been initialized with the new data. If a crash occurs between step 1 and step 3, the transaction is discarded during recovery; the data is on disk, but the metadata still points to the old version (or no version) of the file, which is a consistent state. If a crash occurs after step 3, the metadata is replayed from the journal, and we know the data is already in place.

This approach provides a "best of both worlds" result: we avoid the double-writing of user data (unlike full journaling) while maintaining the guarantee that users will never see uninitialized or stale data from other files (unlike raw metadata-only journaling). It effectively uses write-ordering to protect data integrity while using journaling to protect metadata consistency.
