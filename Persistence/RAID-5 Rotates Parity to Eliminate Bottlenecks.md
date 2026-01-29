---
type: mechanism
source: "OSTEP Ch. 38: Redundant Disk Arrays (RAID)"
tags:
  - raid
  - storage
  - parity
  - persistence
related:
  - "[[RAID Uses Redundancy to Improve Performance and Reliability]]"
  - "[[RAID-4 Uses a Dedicated Parity Disk]]"
prerequisites:
  - "[[RAID-4 Uses a Dedicated Parity Disk]]"
---

> [!SUMMARY]
> RAID-5 improves upon RAID-4 by rotating the parity blocks across all disks in the array rather than storing them on a single dedicated disk. This eliminates the parity disk bottleneck, allowing random writes to be parallelized, while maintaining the same capacity efficiency and single-disk fault tolerance.

**RAID-5** is the most common parity-based RAID level because it solves the random write performance issue of RAID-4.

### Rotated Parity Mechanism
Like RAID-4, it uses XOR parity. However, the location of the parity block changes for each stripe (row).
*   **Stripe 0:** Parity on Disk 3.
*   **Stripe 1:** Parity on Disk 2.
*   **Stripe 2:** Parity on Disk 1.
*   **Stripe 3:** Parity on Disk 0.
This distribution ensures that the write load for parity updates is spread evenly across all disks.

### Analysis
Given $N$ disks with capacity $B$, sequential speed $S$, and random speed $R$:

1.  **Capacity:** $(N-1) \times B$.
    *   Same efficiency as RAID-4. One disk's worth of space is used for parity.
2.  **Reliability:** 1 failure tolerated.
    *   Identical to RAID-4. Rebuilds are slow and intensive (the "write hole" risk).
3.  **Performance:**
    *   **Sequential Read:** $(N-1) \times S$. We read data chunks from all disks.
    *   **Sequential Write:** $(N-1) \times S$.
    *   **Random Read:** $N \times R$. Since parity is distributed, all $N$ disks contain data and can service read requests.
    *   **Random Write:** $\frac{N \times R}{4}$.
        *   We still have the 4-operation overhead (Read old data, Read old parity, Write new data, Write new parity).
        *   *However*, because parity is on different disks for different stripes, multiple random writes can happen in parallel on different disks.

### Trade-offs
RAID-5 offers the best balance of high capacity and decent general-purpose performance. Its main weakness is the "write penalty" (4 I/Os per logical write) compared to RAID-0 or RAID-1.
