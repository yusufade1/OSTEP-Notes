---
type: concept
source: "OSTEP Ch. 44: Flash-based SSDs"
tags:
  - persistence
  - ssd
  - performance
  - reliability
related:
  - "[[The Flash Translation Layer Manages SSD Mapping and Wear]]"
  - "[[Flash Memory Basics - Pages Blocks and Erasure Asymmetry]]"
prerequisites:
  - "[[The Flash Translation Layer Manages SSD Mapping and Wear]]"
---

# SSD Performance Characteristics and Wear Leveling

> [!SUMMARY]
> SSD performance is defined by near-zero seek times for reads, but its write performance is complicated by the overhead of garbage collection and erasure. To maintain drive reliability, the FTL must also perform **wear leveling**, ensuring that write operations are spread across all physical blocks to prevent any single cell from reaching its endurance limit prematurely.

The semiconductor nature of SSDs allows for performance profiles that are vastly different from mechanical hard drives, but they come with a finite lifespan that must be managed by the device's firmware.

## Random vs. Sequential Performance
*   **Reads**: Because there are no moving parts, the "random read" performance of an SSD is nearly identical to its "sequential read" performance. There is no seek or rotational delay.
*   **Writes**: Sequential writes are fast because the FTL can fill blocks efficiently. Random writes can be slow because they trigger frequent garbage collection and metadata updates in the FTL.

## Write Amplification
A key metric for SSDs is **Write Amplification (WA)**. This occurs when a single logical write from the OS results in multiple physical writes on the flash (due to garbage collection moving live data). 
$WA = \frac{\text{Physical Writes to Flash}}{\text{Logical Writes from OS}}$
High write amplification reduces both the performance and the lifespan of the drive.

## The Wear-Out Problem
Every flash cell has a finite number of **Program/Erase (P/E) cycles** before it can no longer reliably store data (ranging from 1,000 to 100,000 cycles depending on the flash type). If a file system frequently updated the same block (like a superblock or root directory), that physical cell would quickly wear out, rendering the entire drive useless even if the rest of the cells were pristine.

## Wear Leveling
To prevent premature failure, the FTL performs **wear leveling**:
*   **Dynamic Wear Leveling**: The FTL picks the least-worn available block when writing new data.
*   **Static Wear Leveling**: The FTL occasionally moves "cold" data (data that never changes) from a lightly-worn block to a heavily-worn block. This frees up the "fresh" block to be used for more frequent "hot" writes.

By distributing the "pain" of writing across all available blocks, the SSD ensures that the drive remains functional until the total capacity for writes across the entire device is exhausted.

## Connections
- Addresses the physical limitations of [[Flash Memory Basics - Pages Blocks and Erasure Asymmetry]].
- Is managed internally by [[The Flash Translation Layer Manages SSD Mapping and Wear]].
