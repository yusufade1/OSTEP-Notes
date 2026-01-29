---
type: overview
source: "OSTEP Ch. 43: Log-structured File Systems"
tags:
  - file-system
  - lfs
  - persistence
  - chapter-overview
related:
  - "[[Persistence MOC]]"
  - "[[Crash Consistency - Chapter Overview]]"
  - "[[FFS Motivation - The Performance Problem of Old File Systems]]"
prerequisites:
  - "[[Crash Consistency - Chapter Overview]]"
  - "[[VSFS Disk Layout - Superblock Bitmaps and Regions]]"
---

> [!SUMMARY]
> Log-structured File Systems (LFS) rethink file system design by treating the entire disk as a sequential log. By buffering all updates—including data and metadata—into large segments and writing them contiguously, LFS transforms small random writes into high-performance sequential I/O, overcoming the update-in-place limitations of traditional file systems.

## The Motivation for a New Design
The shift toward LFS was driven by changing technology trends: increasing system memory (which absorbs most read traffic) and the growing gap between CPU speeds and disk seek times.
*   **[[LFS Motivation - Sequential Writes Outperform Random Writes]]:** Why the "update-in-place" approach of FFS and VSFS became a bottleneck and how LFS addresses it.

## The LFS Write Mechanism
LFS does not overwrite blocks; it always appends new data to the end of the log.
*   **[[LFS Write Buffering Groups Small Updates into Large Segments]]:** How LFS uses memory to aggregate writes before committing them to disk in efficient, multi-megabyte chunks.

## Solving the "Finding Inodes" Problem
Because LFS never overwrites, inodes move on every update. This requires a new level of indirection.
*   **[[The Inode Map Tracks the Location of Inodes in LFS]]:** The data structure that maps inode numbers to their current on-disk addresses.
*   **[[The Checkpoint Region Points to the Current Inode Map in LFS]]:** A fixed location on disk used to bootstrap the file system and find the latest inode map after a crash.

## Managing Free Space
Since LFS is a log, it eventually runs out of space at the end of the disk. It must reclaim space from "holes" left by deleted or overwritten files.
*   **[[LFS Garbage Collection Reclaims Space by Cleaning Segments]]:** The mechanism of segment cleaning, where the OS reads old segments, identifies live data, and writes it forward to the new end of the log.
