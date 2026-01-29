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
  - "[[RAID-5 Rotates Parity to Eliminate Bottlenecks]]"
prerequisites:
  - "[[RAID Uses Redundancy to Improve Performance and Reliability]]"
---

> [!SUMMARY]
> RAID-4 uses block-level striping across data disks and stores parity information on a single, dedicated parity disk. While this improves capacity compared to mirroring and allows recovery from single-disk failures, the dedicated parity disk becomes a bottleneck for random writes, severely limiting performance.

**RAID-4** attempts to balance the performance of striping with the cost-efficiency of parity-based redundancy.

### Parity Mechanism
Data is striped across $N-1$ disks. The $N$th disk is the **parity disk**.
Parity is calculated using XOR: $P = D_0 \oplus D_1 \oplus D_2 \dots$
If any disk fails, the missing block can be reconstructed by XORing the remaining blocks and the parity.

### Analysis
Given $N$ disks with capacity $B$, sequential speed $S$, and random speed $R$:

1.  **Capacity:** $(N-1) \times B$.
    *   Only one disk's worth of capacity is lost, regardless of array size. Much cheaper than RAID-1.
2.  **Reliability:** 1 failure tolerated.
    *   If any one disk (data or parity) fails, the system continues to function. Two failures cause data loss.
3.  **Performance:**
    *   **Sequential Read:** $(N-1) \times S$. The parity disk does not participate in reads.
    *   **Sequential Write:** $(N-1) \times S$. Full stripe writes allow parity to be calculated on the fly and written in parallel.
    *   **Random Read:** $(N-1) \times R$. All data disks can service requests independently.
    *   **Random Write:** $\frac{R}{2}$ (approx). **The Bottleneck.**
        *   Every random write updates a data block *and* the parity block.
        *   Since all parity blocks live on one disk, *every* write must touch that single disk. The parity disk serializes all writes.

### The Small Write Problem
Updating a single block in RAID-4 involves 4 I/O operations (Read-Modify-Write):
1.  Read old data.
2.  Read old parity.
3.  Compute new parity ($P_{new} = P_{old} \oplus D_{old} \oplus D_{new}$).
4.  Write new data.
5.  Write new parity.
This heavy overhead, combined with the single parity disk bottleneck, makes RAID-4 rare in practice.
