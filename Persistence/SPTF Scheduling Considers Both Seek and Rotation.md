---
type: mechanism
source: "OSTEP Ch. 37: Hard Disk Drives"
tags:
  - scheduling
  - disk-scheduling
  - algorithm
  - persistence
related:
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
  - "[[SSTF Scheduling Prioritizes Shortest Seek Time]]"
prerequisites:
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
---

> [!SUMMARY]
> Shortest Positioning Time First (SPTF), also known as Shortest Access Time First (SATF), improves upon SSTF by considering both seek time and rotational latency. By selecting the request that can be serviced in the minimum total time, SPTF achieves higher throughput than seek-only algorithms.

Standard scheduling algorithms like SSTF and SCAN focus solely on **seek time** (track distance). However, **rotational latency** is often comparable to or greater than seek time in modern drives.

### The Mechanism
**SPTF** calculates the total positioning time ($T_{seek} + T_{rotation}$) for every pending request and selects the minimum.
*   **Awareness:** The disk controller (or OS, if hardware details are exposed) must know the exact current angular position of the disk head and the sector mapping.
*   **Greedy Approach:** Like SSTF, it is a greedy algorithm and can suffer from starvation, often solved by aging requests (Weights).

### Why It Matters
Consider the head is at **Track 10**.
*   **Request A:** Track 10 (Seek 0), but the sector is on the opposite side of the platter (Wait 1/2 rotation).
*   **Request B:** Track 11 (Short seek), and the sector is just about to pass under the head (Near 0 wait).

SSTF would choose **A** (Distance 0).
SPTF would choose **B** (Total time: small seek + small wait < long wait).

In modern drives with high RPM and fast seeks, rotational latency is a significant component, making SPTF strictly superior to SSTF for throughput.
