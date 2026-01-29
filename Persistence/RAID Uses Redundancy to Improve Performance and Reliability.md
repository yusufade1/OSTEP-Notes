---
type: mechanism
source: "OSTEP Ch. 38: Redundant Disk Arrays (RAID)"
tags:
  - raid
  - storage
  - reliability
  - performance
  - persistence
related:
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
  - "[[RAID-0 Striping Maximizes Performance but Lowers Reliability]]"
  - "[[RAID-1 Mirroring Guarantees Reliability at High Cost]]"
prerequisites:
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
---

> [!SUMMARY]
> RAID (Redundant Array of Inexpensive/Independent Disks) combines multiple physical disks into a single logical unit to improve performance, capacity, and reliability. By using techniques like striping, mirroring, and parity, RAID systems trade off cost and complexity against data protection and speed.

A **RAID** system appears to the operating system as a single, large, fast, and reliable disk. Internally, it is a complex system consisting of multiple disks, memory, and a processor (in hardware RAID) or software logic (in software RAID) that manages data distribution.

### Core Goals
1.  **Performance:** Parallelizing I/O across multiple disks allows for higher throughput (bandwidth) and more operations per second (IOPS).
2.  **Capacity:** Combining disks creates a larger logical volume than any single disk could offer.
3.  **Reliability:** Storing redundant information ensures that data survives the failure of one or more physical disks.

### Analysis Methodology
To evaluate different RAID levels, we assess three key metrics relative to a system with $N$ disks, each with capacity $B$, sequential throughput $S$, and random throughput $R$.

1.  **Capacity:** How much useful storage is available?
    *   Ideal: $N \times B$.
    *   Real: Less, due to redundancy overhead.
2.  **Reliability:** How many disk failures can the system tolerate?
    *   Typically 0 (no protection) to 1 or 2 failures.
3.  **Performance:**
    *   **Sequential Read/Write:** Throughput for large, contiguous transfers.
    *   **Random Read/Write:** Throughput for small, scattered requests.
    *   **Latency:** Time to complete a single request.

This framework allows us to objectively compare designs like RAID-0 (striping), RAID-1 (mirroring), and RAID-5 (parity).
