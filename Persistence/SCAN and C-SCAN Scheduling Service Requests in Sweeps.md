---
type: atomic
source: OSTEP Ch. 37
tags: [scheduling, disk-scheduling, algorithm, persistence]
related: [[SSTF Scheduling Prioritizes Shortest Seek Time]], [[SPTF Scheduling Considers Both Seek and Rotation]]
prerequisites: [[SSTF Scheduling Prioritizes Shortest Seek Time]]
---

> [!SUMMARY]
> SCAN (Elevator) and C-SCAN (Circular SCAN) address SSTF's starvation problem by moving the disk arm in a predictable sweep pattern across the disk. SCAN services requests in both directions, while C-SCAN services only in one direction to provide more uniform wait times.

### SCAN (Elevator Algorithm)
**SCAN** moves the disk arm back and forth across the disk surface, servicing requests in its path.
*   **Behavior:** It sweeps from one end to the other, processing matching requests. Upon reaching the edge, it reverses direction.
*   **Pros:** Prevents starvation (every request is guaranteed service within two sweeps).
*   **Cons:** Requests arriving just behind the head must wait for the arm to reach the end and come back (high variance in response time).

**Example Trace (Queue: 10, 22, 20, 2, 40 | Head: 25 | Dir: Increasing):**
1.  Sweep Up: $25 	o 40$.
2.  Reverse at 40 (assuming no requests $>40$).
3.  Sweep Down: $40 	o 22 	o 20 	o 10 	o 2$.
**Order:** 25, 40, 22, 20, 10, 2.

### C-SCAN (Circular SCAN)
**C-SCAN** restricts scanning to a single direction (e.g., outer to inner).
*   **Behavior:** The arm sweeps across the disk servicing requests. When it reaches the end, it immediately returns to the start *without* servicing requests on the return trip.
*   **Pros:** Provides more uniform wait times (the "circular" property treats all cylinders equally).
*   **Cons:** The "flyback" seek (return to start) is wasted time, though usually fast.

**Example Trace (Same Queue | Head: 25 | Dir: Increasing):**
1.  Sweep Up: $25 	o 40$.
2.  Reach End, Jump to 0 (logical start).
3.  Sweep Up: $0 	o 2 	o 10 	o 20 	o 22$.
**Order:** 25, 40, 2, 10, 20, 22.

### Comparison
SCAN favors the middle tracks (visited twice per full cycle), while C-SCAN treats all tracks equally, avoiding the bias against edge tracks.
