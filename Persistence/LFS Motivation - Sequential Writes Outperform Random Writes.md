---
type: concept
source: "OSTEP Ch. 43: Log-structured File Systems"
tags:
  - file-system
  - lfs
  - performance
  - persistence
related:
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
  - "[[FFS Motivation - The Performance Problem of Old File Systems]]"
  - "[[LFS Write Buffering Groups Small Updates into Large Segments]]"
prerequisites:
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
  - "[[FFS Motivation - The Performance Problem of Old File Systems]]"
---

# LFS Motivation - Sequential Writes Outperform Random Writes

> [!SUMMARY]
> The Log-structured File System (LFS) is motivated by the massive performance gap between sequential and random disk I/O. As system memory grows and caches absorb most read requests, the primary performance bottleneck for file systems becomes write traffic, which LFS optimizes by transforming all updates into a single sequential stream.

LFS was developed at a time when two technology trends became clear: system memory was increasing rapidly, and the performance gap between random and sequential disk access was widening. These trends suggested that the "update-in-place" strategy used by traditional file systems like FFS was fundamentally limited.

## The Shift to Write-Heavy Workloads
Because larger amounts of RAM allow the OS to cache a significant portion of the file system's data, most read requests are satisfied from memory (the page cache). Consequently, the traffic that actually reaches the disk is dominated by writes. In a traditional file system, even a small file update requires multiple random I/O operations:
1.  **Data block write**
2.  **Inode update** (at a different location)
3.  **Bitmap update** (at yet another location)
4.  **Directory update** (if a new file is created)

This "scattered" I/O prevents the disk from ever reaching its peak transfer rate, as the disk arm must constantly seek and wait for rotation between each small write.

## Sequentiality as the Solution
The core idea of LFS is to ignore the physical "location" of files on the disk and instead treat the entire disk as a sequential log. When the OS needs to write data, it buffers all pending updates—including data blocks, inodes, and bitmaps—and writes them all at once in a contiguous block. 

By writing sequentially, LFS utilizes nearly 100% of the disk's available bandwidth. While a random write might achieve only a few hundred kilobytes per second due to seek overhead, a sequential write can achieve the full multi-megabyte-per-second capability of the drive.

## Limitations of Update-in-Place
Traditional file systems perform **update-in-place**: they write data to a specific block and, if that data is modified, they overwrite that same block. This requires the file system to keep metadata (like inodes) in fixed locations to make them easy to find. LFS abandons this fixed-location model, accepting the complexity of finding data that is constantly moving in exchange for the massive performance gains of sequential writing.

## Connections
- Exploits the hardware reality described in [[Disk Access Time Depends on Seek Rotation and Transfer]].
- Solves the fragmentation and seek problems that motivated [[FFS Motivation - The Performance Problem of Old File Systems]].
- Leads to the need for [[LFS Write Buffering Groups Small Updates into Large Segments]] to ensure sequentiality.
