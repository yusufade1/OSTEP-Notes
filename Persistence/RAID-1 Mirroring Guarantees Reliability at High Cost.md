---
type: mechanism
source: "OSTEP Ch. 38: Redundant Disk Arrays (RAID)"
tags:
  - raid
  - storage
  - reliability
  - persistence
related:
  - "[[RAID Uses Redundancy to Improve Performance and Reliability]]"
  - "[[RAID-0 Striping Maximizes Performance but Lowers Reliability]]"
prerequisites:
  - "[[RAID Uses Redundancy to Improve Performance and Reliability]]"
---

> [!SUMMARY]
> RAID-1, or "mirroring," keeps an identical copy of every data block on a separate disk. This provides excellent reliability and read performance but halves the effective capacity and requires all writes to be sent to both disks, limiting write performance to the speed of the slower disk.

**RAID-1** prioritizes data safety above all else. In a typical configuration with pairs of disks, every write to the primary disk is simultaneously written to the mirror.

### Mirroring Mechanism
Disks are paired. If we have blocks 0, 1, 2, 3:
*   **Disk 0:** Holds Block 0, Block 2...
*   **Disk 1:** Holds Block 0 (copy), Block 2 (copy)...
(Usually combined with striping as RAID-10, but the core concept is the copy).

### Analysis
Given $N$ disks (where $N$ is even) with capacity $B$, sequential speed $S$, and random speed $R$:

1.  **Capacity:** $\frac{N \times B}{2}$.
    *   We lose 50% of storage to redundancy. This is the most expensive RAID level per terabyte.
2.  **Reliability:** 1 failure per mirrored pair.
    *   In a pure RAID-1 mirror of two disks, one can fail.
    *   Ideally, up to $N/2$ disks can fail (if they are the "right" ones, i.e., one from each pair), but in the worst case (both disks in a pair), data is lost.
3.  **Performance:**
    *   **Sequential Read:** $N \times S$ (Peak). We can read different blocks from both mirrors simultaneously.
    *   **Sequential Write:** $\frac{N \times S}{2}$. We must write every bit twice. Throughput is limited by the number of pairs.
    *   **Random Read:** $N \times R$. Requests can be load-balanced across mirrors.
    *   **Random Write:** $\frac{N \times R}{2}$. Every logical write requires two physical writes.

### Use Cases
RAID-1 is used for operating system drives, transaction logs, and critical databases where data loss is unacceptable and recovery speed (instant failover) is important.
