---
type: overview
source: "OSTEP Ch. 42: Crash Consistency: FSCK and Journaling"
tags:
  - file-system
  - crash-consistency
  - journaling
  - persistence
  - chapter-overview
related:
  - "[[Persistence MOC]]"
  - "[[VSFS File Write Path Involves Allocation and Metadata Updates]]"
  - "[[Log-Structured File Systems - Chapter Overview]]"
prerequisites:
  - "[[VSFS File Write Path Involves Allocation and Metadata Updates]]"
---

> [!SUMMARY]
> Crash consistency is the challenge of ensuring that a file system remains in a valid state after an unexpected power failure or system crash. This chapter explores the failure modes of traditional file systems and the modern mechanisms—fsck and journaling—used to guarantee data integrity.

# The Problem
*   **[[The Crash Consistency Problem Arises from Partial Disk Updates]]**: Why multi-block updates are risky and how they can lead to corruption.
*   **[[Crash Scenarios Involve Mismatched Metadata and Data Updates]]**: A taxonomy of what happens when specific blocks fail to reach the disk.

# Traditional Recovery
*   **[[fsck Recovers File System Integrity via Post-Crash Scanning]]**: The historical approach of "audit and repair" after a crash, and why it doesn't scale.

# Modern Solution: Journaling
*   **[[Journaling Provides Crash Consistency via Write-Ahead Logging]]**: The core principle of writing to a log before the main file system.
*   **[[Journal Structure Organizes Transactions with Transaction Blocks]]**: How the log is formatted for atomicity.
*   **[[Journal Checkpointing Reclaims Log Space After Successful Writes]]**: Managing the circular log buffer.

# Optimizations
*   **[[Metadata-Only Journaling Optimizes Performance by Excluding Data Blocks]]**: Balancing speed and consistency.
*   **[[Ordered Journaling Protects Data Integrity by Sequencing Data Writes]]**: The standard Linux approach to ensuring users never see stale data.
