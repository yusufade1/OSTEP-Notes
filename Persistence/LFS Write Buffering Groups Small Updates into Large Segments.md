---
type: mechanism
source: "OSTEP Ch. 43: Log-structured File Systems"
tags:
  - file-system
  - lfs
  - buffering
  - performance
  - persistence
related:
  - "[[LFS Motivation - Sequential Writes Outperform Random Writes]]"
  - "[[The Inode Map Tracks the Location of Inodes in LFS]]"
  - "[[LFS Garbage Collection Reclaims Space by Cleaning Segments]]"
prerequisites:
  - "[[LFS Motivation - Sequential Writes Outperform Random Writes]]"
---

# LFS Write Buffering Groups Small Updates into Large Segments

> [!SUMMARY]
> LFS avoids the overhead of random writes by collecting multiple file system updates in an in-memory buffer until they form a large, contiguous unit called a segment. By writing these multi-megabyte segments to the disk in a single sequential operation, LFS ensures the disk arm moves as little as possible, achieving near-peak bandwidth.

To achieve high performance, LFS must ensure that it writes to the disk in large chunks. If it wrote every small update (like a single 4KB block) immediately, it would still suffer from the seek and rotational delays it aims to avoid.

## The Role of the Segment
A **segment** is the fundamental unit of write management in LFS. Typically ranging from 512 KB to 2 MB in size, a segment contains everything needed to update the file system:
*   **Data blocks** for one or more files.
*   **Inodes** for the files being updated.
*   **Indirect blocks** (if files are large).
*   **Inode map pieces** (to track the new inode locations).

By grouping these diverse blocks into a single segment, LFS transforms what would have been dozens of random writes into a single, massive sequential write.

## Why Large Buffers Matter
The effectiveness of LFS depends on the "effective bandwidth" it can extract from the drive. If $T_{seek}$ is the time to seek to the start of a write and $R$ is the peak transfer rate, the time to write $D$ bytes is $T = T_{seek} + D/R$. 
To approach the peak rate $R$, the transfer time $D/R$ must be much larger than the seek time $T_{seek}$. This is why LFS uses megabyte-sized segments; a 2 MB segment takes enough time to transfer that the initial seek cost becomes negligible.

## Write Buffering Logic
The OS maintains the "current segment" in memory. Applications calling `write()` have their data copied into this buffer.

```c
// Conceptual LFS write buffering
void lfs_write(block_id, data) {
    if (current_segment_full()) {
        flush_segment_to_disk(current_segment);
        start_new_segment();
    }
    append_to_buffer(current_segment, data);
    update_inode_in_buffer(block_id);
}
```

## The Crash-Consistency Trade-off
While buffering improves performance, it introduces a window of vulnerability. If the system crashes before a segment is flushed to disk, the buffered updates are lost. LFS handles this by using a [[The Checkpoint Region Points to the Current Inode Map in LFS|checkpoint region]] and logging techniques to ensure that the on-disk state remains consistent, even if the most recent few seconds of updates are lost.

## Connections
- Enabled by [[LFS Motivation - Sequential Writes Outperform Random Writes]].
- Creates the need for [[The Inode Map Tracks the Location of Inodes in LFS]] because inodes move with every segment flush.
- Segments eventually become "dirty," requiring [[LFS Garbage Collection Reclaims Space by Cleaning Segments]].
