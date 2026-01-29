---
type: mechanism
source: "OSTEP Ch. 38: Redundant Disk Arrays (RAID)"
tags:
  - raid
  - storage
  - performance
  - persistence
related:
  - "[[RAID Uses Redundancy to Improve Performance and Reliability]]"
  - "[[RAID-1 Mirroring Guarantees Reliability at High Cost]]"
prerequisites:
  - "[[RAID Uses Redundancy to Improve Performance and Reliability]]"
---

> [!SUMMARY]
> RAID-0, or "striping," spreads data blocks across all available disks in a round-robin fashion without any redundancy. It offers the maximum possible capacity and performance but provides zero reliability; a single disk failure results in total data loss.

**RAID-0** is not technically "redundant," as it includes no mechanism to recover from failures. Its sole focus is performance and capacity.

### Striping Mechanism
Data is divided into blocks (chunks). These chunks are distributed across the $N$ disks in the array.
*   **Chunk 0** goes to Disk 0.
*   **Chunk 1** goes to Disk 1.
*   **Chunk N** goes to Disk 0 (wrapping around).

This parallelism allows the system to read or write to all disks simultaneously.

### Analysis
Given $N$ disks with capacity $B$, sequential speed $S$, and random speed $R$:

1.  **Capacity:** $N \times B$.
    *   No space is wasted on parity or mirrors. Utilization is 100%.
2.  **Reliability:** 0 failures tolerated.
    *   If *any* disk fails, the entire volume is corrupted because parts of files are missing.
    *   The failure rate is roughly $N$ times that of a single disk.
3.  **Performance:**
    *   **Sequential Read:** $N \times S$. (Full parallelism)
    *   **Sequential Write:** $N \times S$. (Full parallelism)
    *   **Random Read:** $N \times R$. (Independent seeks)
    *   **Random Write:** $N \times R$. (Independent seeks)

### Use Cases
RAID-0 is suitable for temporary data, scratch spaces, or high-performance computing tasks where speed is critical and data can be easily regenerated or restored from backup.
