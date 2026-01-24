---
type: atomic
source: OSTEP Ch. 16
tags:
  - virtualization
  - memory
  - segmentation
  - segment-table
related:
  - "[[Segmentation Generalizes Base-and-Bounds with Multiple Segments]]"
  - "[[Code Stack and Heap Each Get Their Own Segment]]"
  - "[[Hardware Registers Enable Efficient Address Translation]]"
  - "[[The OS Manages Memory at Process Creation and Context Switch]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Segmentation Generalizes Base-and-Bounds with Multiple Segments]]"
---

# The Segment Table Maps Segment Numbers to Base-Bounds Pairs

> [!SUMMARY]
> The segment table is the hardware data structure that stores per-segment translation information for each process. Each entry contains a base address, bounds (limit), growth direction, and protection bits. The top bits of a virtual address select a segment table entry, and the remaining bits become the offset within that segment. The OS populates the segment table on process creation and saves/restores it during context switches.

## Segment Table Structure

Each entry in the segment table contains:

```
+---------------------------------------------------+
| Base (physical start) | Bounds | Dir | Protection |
+---------------------------------------------------+
|  32 KB                | 2 KB   |  +  |  RX        |  <- Code
|  34 KB                | 3 KB   |  +  |  RW        |  <- Heap
|  28 KB                | 2 KB   |  -  |  RW        |  <- Stack
+---------------------------------------------------+
```

- **Base:** Physical start address of the segment.
- **Bounds:** Maximum valid offset (or segment length).
- **Dir (grows-positive):** 1 if the segment grows toward higher addresses, 0 for the stack's negative growth.
- **Protection:** Read, write, and execute bits controlling access permissions.

With coarse-grained segmentation (3 segments), only 2 bits are needed for the segment selector. [[Coarse-Grained vs Fine-Grained Segmentation Trade Flexibility for Simplicity|Fine-grained]] systems use more bits, supporting dozens or hundreds of segments.

## Address Decomposition

For a 14-bit virtual address space with a 2-bit segment number:

```
Virtual Address (14 bits):
+--------+------------------+
| Seg(2) |   Offset (12)    |
+--------+------------------+

Example: 0x1A04
Binary: 01 101000000100
Seg = 01 (Heap), Offset = 0xA04 = 2564
```

The hardware extracts the segment number, indexes into the table, reads the base and bounds, and computes:

```
if grows_positive:
    if offset >= bounds: trap(SEGFAULT)
    physical = base + offset
else:  # stack grows negative
    if offset < (max_seg_size - bounds): trap(SEGFAULT)
    physical = base + (offset - max_seg_size)
```

## Hardware vs. Software Responsibilities

The segment table lives in [[Hardware Registers Enable Efficient Address Translation|hardware registers]] (for small tables with 3-4 segments) or in memory with a segment table base register (for larger tables). The OS is responsible for:

1. **Process creation:** Allocating physical memory for each segment and populating the table entries.
2. **Context switch:** Saving the current process's segment registers and loading the next process's values—the same save/restore pattern as [[The OS Manages Memory at Process Creation and Context Switch|base-and-bounds context switching]], but repeated for each segment.
3. **Segment growth:** When a heap `sbrk()` call requests more memory, the OS allocates additional physical space and updates the bounds field.
4. **Process termination:** Freeing all physical memory associated with the process's segments and reclaiming their regions for the free list.

## The Segmentation Fault

The name "segmentation fault" originates directly from this mechanism. When the offset exceeds the segment's bounds (or violates protection bits), the hardware raises a fault. The OS typically responds by terminating the offending process—the same behavior seen with [[Base-and-Bounds Provides Dynamic Relocation|simple bounds violations]], but now checked per-segment rather than for the entire address space.
