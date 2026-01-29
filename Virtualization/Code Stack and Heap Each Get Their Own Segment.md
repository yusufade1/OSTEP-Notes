---
type: mechanism
source: "OSTEP Ch. 16: Segmentation"
tags:
  - virtualization
  - memory
  - segmentation
  - address-space-layout
related:
  - "[[Segmentation Generalizes Base-and-Bounds with Multiple Segments]]"
  - "[[Stack and Heap Occupy Opposite Ends of the Address Space]]"
  - "[[The Segment Table Maps Segment Numbers to Base-Bounds Pairs]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Segmentation Generalizes Base-and-Bounds with Multiple Segments]]"
  - "[[Stack and Heap Occupy Opposite Ends of the Address Space]]"
---

# Code Stack and Heap Each Get Their Own Segment

> [!SUMMARY]
> In a segmented address space, the three logical regions—code, heap, and stack—become independent segments, each with its own base, bounds, growth direction, and protection bits. The code segment is typically read-execute and shared across processes running the same program. The heap grows upward (positive direction). The stack grows downward (negative direction), requiring special hardware support to compute physical addresses correctly.

## Three Segments, Three Policies

The [[Stack and Heap Occupy Opposite Ends of the Address Space|virtual address space layout]] maps naturally onto three segments with distinct properties:

| Segment | Protection     | Growth     | Typical Use                |
|---------|---------------|------------|----------------------------|
| Code    | Read + Execute | None (fixed) | Program instructions       |
| Heap    | Read + Write   | Positive    | Dynamic allocations (malloc)|
| Stack   | Read + Write   | Negative    | Local variables, return addresses |

Each segment is placed independently in physical memory. The code segment for `/bin/ls` might sit at physical address 80 KB, while its heap starts at 200 KB and its stack at 512 KB—no contiguity required.

## Growth Direction Matters

The heap and stack grow in opposite directions. The hardware needs a **grows-positive** bit in each segment descriptor to translate addresses correctly:

- **Heap (grows positive):** offset goes from 0 upward. Physical address = base + offset. Bounds check: offset < bounds.
- **Stack (grows negative):** offset goes from the maximum virtual address downward. The hardware must compute the physical address as: physical = base + (offset - max_segment_size). The bounds check also inverts—the offset must be *above* the limit, not below.

For a stack segment with base 28 KB and bounds 2 KB (meaning 2 KB of allocated stack):

```
max_segment_size = 4 KB (maximum the segment could grow to)
virtual offset = 3 KB (near top of segment)
physical = 28 KB + (3 KB - 4 KB) = 27 KB
```

The negative growth arithmetic is often the trickiest part of segmentation for students—the key insight is that the hardware subtracts to account for the stack growing "backward."

## Code Sharing

Because the code segment is read-execute (never modified at runtime), multiple processes running the same program can point their code segment base to the **same physical region**. This is an efficiency gain: 100 instances of a shell share one physical copy of the shell binary. The [[The Segment Table Maps Segment Numbers to Base-Bounds Pairs|segment table]] for each process still has its own entry for code, but the base values are identical, and the protection bits prevent writes.

## Relationship to Base-and-Bounds

Where [[Base-and-Bounds Provides Dynamic Relocation|base-and-bounds]] uses a single register pair for the entire address space, segmentation uses three (or more) pairs. This means three bounds checks per context, three base registers to save during [[Context Switch Saves and Restores Process State|context switches]], and a slightly more complex translation path—but the memory savings from eliminating unused gaps typically outweighs this overhead.
