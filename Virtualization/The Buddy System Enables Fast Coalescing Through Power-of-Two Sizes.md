---
type: atomic
source: OSTEP Ch. 17
tags:
  - virtualization
  - memory
  - free-space-management
  - allocation-strategy
related:
  - "[[Splitting and Coalescing Keep the Free List Efficient]]"
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[Best-Fit Allocation Minimizes Wasted Space but Requires Full Search]]"
  - "[[Slab Allocators Pre-Allocate Fixed-Size Object Caches]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Splitting and Coalescing Keep the Free List Efficient]]"
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
---

# The Buddy System Enables Fast Coalescing Through Power-of-Two Sizes

> [!SUMMARY]
> The buddy system restricts all allocations to power-of-two sizes and maintains separate free lists for each size class. When memory is freed, the allocator checks if the freed block's "buddy" (the adjacent block of the same size that it was split from) is also free. If so, they coalesce into a larger block. This structural constraint makes coalescing O(1) but introduces internal fragmentation from rounding up requests.

## Structure and Allocation

Memory is organized into power-of-two sized blocks. For a 64 KB heap:

```
Level 0: [64 KB]
Level 1: [32 KB] [32 KB]
Level 2: [16 KB] [16 KB] [16 KB] [16 KB]
...
```

Allocation proceeds by finding the smallest size class that fits the request, splitting larger blocks as needed:

```
Request: 7 KB
  Smallest fit: 8 KB (round up to power of two)
  Free lists: 64[1], 32[0], 16[0], 8[0]

  No 8 KB block → split 16 KB? No 16 KB → split 32 KB? No 32 KB → split 64 KB

  Split 64 KB → two 32 KB blocks
  Split 32 KB → two 16 KB blocks
  Split 16 KB → two 8 KB blocks
  Allocate one 8 KB block

  Result: 8 KB allocated, 8+16+32 KB free across lists
```

## Buddy Relationship

Two blocks are buddies if:
1. They are the same size
2. They were created by splitting the same parent block
3. They differ only in one bit of their address

For a block at address A of size S, its buddy is at address `A XOR S`:

```
Block at 0x0000, size 16 KB → buddy at 0x0000 XOR 0x4000 = 0x4000
Block at 0x4000, size 16 KB → buddy at 0x4000 XOR 0x4000 = 0x0000
```

This relationship is computable from the address alone—no metadata search required.

## Fast Coalescing

When a block is freed, the allocator:
1. Computes the buddy address via XOR
2. Checks if the buddy is free (O(1) with appropriate data structure)
3. If free, removes buddy from its free list, coalesces, and recursively checks the parent's buddy

```
Free 8 KB at 0x2000:
  Buddy at 0x2000 XOR 0x2000 = 0x0000
  Is 0x0000 (8 KB) free? Yes
  Coalesce → 16 KB at 0x0000

  Buddy at 0x0000 XOR 0x4000 = 0x4000
  Is 0x4000 (16 KB) free? Yes
  Coalesce → 32 KB at 0x0000

  Continue recursively...
```

## Trade-off Analysis

| Factor | Buddy System Behavior |
|--------|----------------------|
| **Allocation time** | O(log N) splits worst case |
| **Coalescing time** | O(log N) recursive merges |
| **Internal fragmentation** | Up to 50% (request rounded up) |
| **External fragmentation** | Minimal (same-size blocks coalesce) |
| **Data structure** | Separate free list per size class |

**The trade-off**: The buddy system trades internal fragmentation (wasted space inside allocated blocks) for efficient coalescing and reduced external fragmentation. A 9 KB request wastes 7 KB of its 16 KB allocation, but the structural constraint ensures that blocks can always be reunited with their buddies.

## Usage

The Linux kernel uses a buddy allocator for managing physical page frames. The [[Slab Allocators Pre-Allocate Fixed-Size Object Caches|slab allocator]] is layered on top to handle smaller, fixed-size kernel objects efficiently, combining buddy's coalescing strength with slab's common-case optimization.
