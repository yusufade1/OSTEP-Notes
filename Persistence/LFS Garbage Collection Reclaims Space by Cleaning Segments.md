---
type: mechanism
source: "OSTEP Ch. 43: Log-structured File Systems"
tags:
  - file-system
  - lfs
  - garbage-collection
  - performance
  - persistence
related:
  - "[[LFS Write Buffering Groups Small Updates into Large Segments]]"
  - "[[The Inode Map Tracks the Location of Inodes in LFS]]"
  - "[[FFS Motivation - The Performance Problem of Old File Systems]]"
prerequisites:
  - "[[LFS Write Buffering Groups Small Updates into Large Segments]]"
  - "[[The Inode Map Tracks the Location of Inodes in LFS]]"
---

# LFS Garbage Collection Reclaims Space by Cleaning Segments

> [!SUMMARY]
> Because LFS never overwrites data in place, old versions of files and metadata remain on the disk as "dead" space. To reclaim this space, LFS employs **Garbage Collection (segment cleaning)**, a process that reads old segments, identifies the live blocks, and compacts them into new segments, thereby creating large, contiguous free regions for future writes.

In a traditional file system, deleting a file simply involves marking its blocks as free in a bitmap. In LFS, since the system is a continuous log, it eventually reaches the end of the disk. To continue writing, LFS must turn fragmented "holes" in old segments into large, contiguous empty segments.

## The Cleaning Mechanism
The LFS **cleaner** (a background process) works in three steps:
1.  **Read**: Select a few "dirty" segments that contain some dead data.
2.  **Filter**: Determine which blocks in those segments are still **live** (the latest version) and which are **dead** (overwritten or deleted).
3.  **Write**: Append the live blocks to the current head of the log (just like a normal write) and mark the old segments as entirely free.

## Determining Block Liveness
To determine if a block is live without searching the entire file system, LFS includes a **Segment Summary Block** at the start of every segment. This block records the inode number and the file offset (block index) for every data block in the segment.
To check liveness for a block $B$:
1.  Look up its inode $I$ and offset $O$ in the summary block.
2.  Check the current [[The Inode Map Tracks the Location of Inodes in LFS|Inode Map]] to find the current location of inode $I$.
3.  Read inode $I$ and see if it still points to disk address $B$ for offset $O$.
4.  If it does, the block is live; if it points elsewhere, the block is dead.

## The Policy Question: What to Clean?
Cleaning is not free; it consumes I/O bandwidth. LFS must decide which segments to clean to minimize this overhead. 
*   **Hot data** changes frequently. Cleaning a "hot" segment early is wasteful because its blocks will likely become dead again soon. 
*   **Cold data** rarely changes. LFS benefits from cleaning cold segments even if they have many live blocks, because once compacted, those blocks will stay live for a long time, "freeing up" the remaining space permanently.
The famous **cost-benefit policy** suggests cleaning "cold" segments sooner than "hot" segments to maximize the stability of free space.

## The Write Cost of LFS
The efficiency of LFS is often measured by its **write cost**—the ratio of total I/O (including cleaning) to the amount of new data written. In the best case (writing to a fresh disk), the cost is 1.0. In a full system with heavy random updates, the cost increases because the cleaner must constantly move live data around.

## Connections
- Competes for bandwidth with [[LFS Write Buffering Groups Small Updates into Large Segments]].
- Solves the fragmentation issues that [[FFS Motivation - The Performance Problem of Old File Systems]] handled via bitmaps.
- Relies on the indirection provided by [[The Inode Map Tracks the Location of Inodes in LFS]].
