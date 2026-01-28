---
type: atomic
source: OSTEP Ch. 42
tags: [file-system, crash-consistency, journaling]
related:
  - [[Journal Structure Organizes Transactions with Transaction Blocks]]
  - [[Journal Checkpointing Reclaims Log Space After Successful Writes]]
  - [[fsck Recovers File System Integrity via Post-Crash Scanning]]
  - [[Log-Structured File Systems - Chapter Overview]]
prerequisites:
  - [[The Crash Consistency Problem Arises from Partial Disk Updates]]
---

> [!SUMMARY]
> Journaling (or Write-Ahead Logging) ensures crash consistency by writing a summary of intended changes to a dedicated log before updating the main file system structures.

Journaling is the modern solution to the crash consistency problem, adopted by file systems like Linux Ext3/Ext4 and Windows NTFS. The core idea is simple: before making any changes to the "real" file system on disk, the OS first writes a description of the update to a small, dedicated area of the disk called the **journal** (or log).

This process transforms a multi-block update into a sequence of steps that can be recovered after a crash. Typically, the journaled update involves three phases:
1.  **Journal Write:** The metadata and data blocks of the transaction are written to the log.
2.  **Journal Commit:** A special commit block is written to the log, marking the transaction as complete.
3.  **Checkpoint:** The changes are written to their final locations in the file system (the "checkpointing" phase).

If a crash occurs during the **Journal Write**, the transaction is incomplete and is simply ignored during recovery. If a crash occurs during **Checkpointing**, the system sees the completed **Commit** block in the journal and "replays" the transaction, ensuring all changes reach their final destination. This recovery process is extremely fast because the system only needs to scan the small journal, not the entire disk. 

By ensuring that the log is written and committed *before* the main file system is touched, the system guarantees that it can always reach a consistent state. If the log is complete, we redo the work; if it is incomplete, we discard it. In either case, the file system remains consistent.
