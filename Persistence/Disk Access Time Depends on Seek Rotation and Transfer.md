---
type: mechanism
source: "OSTEP Ch. 37: Hard Disk Drives"
tags:
  - performance
  - hard-disk
  - latency
  - persistence
related:
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
  - "[[SSTF Scheduling Prioritizes Shortest Seek Time]]"
  - "[[SPTF Scheduling Considers Both Seek and Rotation]]"
prerequisites:
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
---

> [!SUMMARY]
> Disk I/O time is determined by three mechanical and electronic components: seek time (moving the arm), rotational latency (waiting for the sector), and transfer time (reading the data). The total access time is the sum of these delays, with seek and rotation dominating performance for random workloads.

Understanding disk performance requires analyzing the mechanical steps required to satisfy an I/O request. The total time ($T_{I/O}$) can be expressed as:

$$ T_{I/O} = T_{seek} + T_{rotation} + T_{transfer} $$

### Seek Time
**Seek time** is the time required to move the disk arm to the correct track. This is a mechanical operation involving acceleration, coasting, deceleration, and settling.
*   **Settling time** is significant; the head must stabilize over the track before reading.
*   Average seek time is typically one-third of the time for a full stroke (full sweep), usually 4-10 ms.

### Rotational Latency
Once the head is on the correct track, it must wait for the target sector to rotate under the head.
*   **Rotational latency** depends on the RPM.
*   Average latency is half the time of a full rotation ($T_{rotation} = \frac{1}{2} \times \frac{60}{RPM}$).
*   For a 7200 RPM drive, a full rotation takes ~8.3 ms, so average latency is ~4.15 ms.

### Transfer Time
**Transfer time** is the time to actually read or write the data as it passes under the head. This is the fastest component, determined by the drive's data rate and the size of the request.

$$ T_{transfer} = \frac{\text{Size of Request}}{\text{Transfer Rate}} $$

### The Disk Cache (Track Buffer)
Drives include a small amount of RAM (e.g., 64 MB) called the **disk cache** or **track buffer**.
*   **Read-ahead:** When reading a sector, the drive often reads the entire track into the cache, anticipating spatial locality.
*   **Write buffering:** Writes can be acknowledged once placed in RAM (write-back, dangerous on power loss) or only after hitting the platter (write-through, safer but slower).
