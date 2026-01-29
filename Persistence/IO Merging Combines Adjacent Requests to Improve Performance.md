---
type: mechanism
source: "OSTEP Ch. 37: Hard Disk Drives"
tags:
  - optimization
  - io
  - persistence
related:
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
  - "[[Device Drivers Abstract Hardware Details from the OS]]"
prerequisites:
  - "[[Disk Access Time Depends on Seek Rotation and Transfer]]"
---

> [!SUMMARY]
> I/O Merging is an optimization technique where the OS scheduler combines multiple pending requests for adjacent disk sectors into a single, larger request. This reduces the number of distinct I/O commands sent to the device, minimizing command overhead and improving throughput.

Before sending requests to the disk scheduler, the operating system can perform a high-level optimization known as **merging**.

### The Logic
When a process issues a request to read blocks, it often breaks large logical operations into smaller physical block requests.
*   **Scenario:** A queue contains request **A** (read blocks 33-34) and request **B** (read block 35).
*   **Action:** The scheduler notices that 33, 34, and 35 are contiguous. It collapses them into a single request: **Read blocks 33-35**.

### Benefits
1.  **Reduced Overhead:** Sending a command to the device controller takes CPU time and bus bandwidth. Sending one command is cheaper than two.
2.  **Better Disk Performance:** A single long sequential read allows the disk to stream data continuously without gaps or potential re-arbitration.

Merging typically happens in the **I/O Elevator** (software queue) within the OS kernel before the request is dispatched to the device driver.
