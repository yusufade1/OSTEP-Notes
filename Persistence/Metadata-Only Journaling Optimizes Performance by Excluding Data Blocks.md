---
type: atomic
source: OSTEP Ch. 42
tags: [file-system, crash-consistency, journaling]
related:
  - [[Journaling Provides Crash Consistency via Write-Ahead Logging]]
  - [[Ordered Journaling Protects Data Integrity by Sequencing Data Writes]]
prerequisites:
  - [[Journaling Provides Crash Consistency via Write-Ahead Logging]]
---

> [!SUMMARY]
> Metadata-only journaling (or "ordered" journaling) reduces write overhead by only logging file system metadata, while handling user data through careful write ordering.

While "full" journaling (logging both metadata and user data) provides the strongest consistency guarantees, it comes with a significant performance penalty: every data block must be written twice—once to the journal and once to the main file system. To double the write traffic is often unacceptable for high-performance workloads.

**Metadata-only journaling** is a common optimization where the OS only writes metadata (inodes, bitmaps, directory entries) to the journal. User data is written directly to its final location in the data region. This significantly reduces the amount of data written to the log, as metadata is typically much smaller than the actual file contents.

However, metadata-only journaling introduces a new risk. If the OS journals the metadata (saying "this file now owns block 1000") but the user data hasn't reached block 1000 yet when a crash occurs, the file system will be consistent after recovery (the metadata is correct), but the file will contain **garbage data** (whatever was previously at block 1000). This is particularly dangerous if block 1000 previously belonged to a sensitive file (like `/etc/shadow`), as it could lead to information leakage.

To prevent this, most modern file systems (like Linux Ext3/Ext4) use a specific flavor of metadata journaling called **Ordered Journaling**. In this mode, the OS ensures that the user data is written to the disk *before* the corresponding metadata is committed to the journal. This sequencing ensures that if the metadata commit succeeds, the data is guaranteed to be there, and if it fails, the metadata remains unchanged, preserving both consistency and privacy.
