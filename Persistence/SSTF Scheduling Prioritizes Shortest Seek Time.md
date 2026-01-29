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
  - "[[SCAN and C-SCAN Scheduling Service Requests in Sweeps]]"
  - "[[SPTF Scheduling Considers Both Seek and Rotation]]"
prerequisites:
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
---

> [!SUMMARY]
> Shortest Seek Time First (SSTF) orders disk I/O requests by selecting the request closest to the current head position. This minimizes seek distance and improves throughput compared to FIFO, but it can lead to starvation for distant requests if a steady stream of nearby requests arrives.

**Shortest Seek Time First (SSTF)** applies the "shortest job first" principle to disk scheduling. By always choosing the pending request with the minimum seek distance from the current head position, SSTF reduces the average seek time.

### Mechanism
Given a queue of I/O requests identified by track number, SSTF calculates the distance ($|Current - Target|$) for all pending requests and selects the minimum.

### Worked Example
**Queue (Tracks):** 10, 22, 20, 2, 40
**Head Start:** 25

**Trace:**
1.  **Start at 25:**
    *   Distances: 10 (15), 22 (3), 20 (5), 2 (23), 40 (15).
    *   **Select 22.** Move 25 → 22 (Seek: 3).
2.  **At 22:**
    *   Distances: 10 (12), 20 (2), 2 (20), 40 (18).
    *   **Select 20.** Move 22 → 20 (Seek: 2).
3.  **At 20:**
    *   Distances: 10 (10), 2 (18), 40 (20).
    *   **Select 10.** Move 20 → 10 (Seek: 10).
4.  **At 10:**
    *   Distances: 2 (8), 40 (30).
    *   **Select 2.** Move 10 → 2 (Seek: 8).
5.  **At 2:**
    *   Distances: 40 (38).
    *   **Select 40.** Move 2 → 40 (Seek: 38).

**Total Seek Distance:** $3 + 2 + 10 + 8 + 38 = 61$.
(Contrast with FIFO: $25 \to 10 \to 22 \to 20 \to 2 \to 40$ would be $15 + 12 + 2 + 18 + 38 = 85$).

### The Starvation Problem
While efficient, SSTF is not fair. If the head is servicing requests on inner tracks (e.g., 10-20) and new requests continually arrive for that region, a request for an outer track (e.g., 100) may never be serviced. This phenomenon is known as **starvation**.
