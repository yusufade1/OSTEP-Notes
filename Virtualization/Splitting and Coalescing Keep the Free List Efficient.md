---
type: algorithm
source: "OSTEP Ch. 17: Free-Space Management"
tags:
  - virtualization
  - memory
  - free-space-management
  - allocation
related:
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
  - "[[malloc and free Manage Heap Memory Dynamically]]"
  - "[[Best-Fit Allocation Minimizes Wasted Space but Requires Full Search]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
---

# Splitting and Coalescing Keep the Free List Efficient

> [!SUMMARY]
> Splitting divides a free chunk when an allocation request is smaller than the available region, returning the requested portion and keeping the remainder on the free list. Coalescing merges adjacent free chunks when memory is freed, preventing the free list from fragmenting into many tiny unusable pieces. Together, these mechanisms are fundamental to every free-space allocator.

## Splitting: Allocating From Larger Chunks

When a request for N bytes arrives and only larger chunks are available, the allocator must **split** a chunk:

```
Before allocation (request: 10 bytes):
Free list: [addr: 0, size: 30] → [addr: 50, size: 20]

After splitting first chunk:
Allocated: [addr: 0, size: 10]
Free list: [addr: 10, size: 20] → [addr: 50, size: 20]
```

The allocator carves out exactly the requested size and returns the leftover to the free list. Without splitting, the allocator could only satisfy requests that exactly match available chunk sizes—clearly impractical.

Splitting does have a cost: it reduces average chunk size over time. Repeated splits without corresponding merges create many small fragments, reducing the allocator's ability to satisfy large requests.

## Coalescing: Merging Adjacent Free Regions

When memory is freed, the allocator checks if the newly freed region is adjacent to existing free chunks. If so, it **coalesces** them into a single larger chunk:

```
Before free (freeing [addr: 20, size: 10]):
Free list: [addr: 0, size: 20] → [addr: 30, size: 30]

Observation: New chunk [20, 10] is adjacent to [0, 20] and [30, 30]

After coalescing:
Free list: [addr: 0, size: 60]  (merged all three)
```

Without coalescing, freed memory would accumulate as isolated small chunks even when they form contiguous physical regions. The free list would grow unboundedly, searches would slow, and large allocations would fail despite sufficient total free memory.

## Implementation Trade-offs

**Immediate vs. deferred coalescing**: Some allocators coalesce immediately on every free (simple but potentially expensive). Others defer coalescing until allocation fails or a threshold is reached (batches work but may delay reclaiming large contiguous regions).

**Finding neighbors**: Coalescing requires knowing if adjacent regions are free. Simple free lists must search the entire list to find neighbors—O(n) per free. More sophisticated structures (boundary tags, sorted lists) reduce this cost at the expense of metadata overhead.

## Why Both Are Necessary

Splitting alone leads to fragmentation. Coalescing alone cannot operate without prior splits. The two mechanisms work in tension: splits increase the chunk count, coalescing decreases it. A healthy allocator maintains balance, ensuring the free list contains reasonably-sized chunks. This balance depends heavily on the [[Best-Fit Allocation Minimizes Wasted Space but Requires Full Search|allocation strategy]] chosen—whether best-fit, first-fit, or others—since the choice affects which chunks get split and how fragmentation develops over time.
