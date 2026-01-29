---
type: mechanism
source: "OSTEP Ch. 18: Paging: Introduction"
tags:
  - virtualization
  - memory
  - paging
  - segmentation
  - fragmentation
related:
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
  - "[[Segmentation Generalizes Base-and-Bounds with Multiple Segments]]"
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
---

# Paging Eliminates External Fragmentation Through Fixed-Size Units

> [!SUMMARY]
> Paging's use of fixed-size pages and frames makes external fragmentation impossible—any free frame can satisfy any page allocation because all frames are interchangeable. This uniformity simplifies OS memory management, eliminates the need for complex allocation algorithms, and makes memory utilization predictable despite some internal fragmentation.

## Why Fragmentation Disappears

Recall [[External Fragmentation Wastes Memory Between Variable-Sized Segments|external fragmentation]] with segmentation: three 10 KB holes could not satisfy a 25 KB request because no single contiguous region was large enough. With paging, that same request becomes "allocate 7 pages" (28 KB at 4 KB per page). Any 7 free frames work—they need not be adjacent:

```
Segmentation view:          Paging view:
+-----------+               +--+--+--+--+--+--+--+--+
| 10KB free | Can't fit     |F |  |  |F |F |F |  |F | <- 5 scattered
|           | 25KB segment  +--+--+--+--+--+--+--+--+    free frames
+-----------+               Any 5 frames satisfy
| allocated |               a 5-page request
+-----------+
| 10KB free |
+-----------+
```

The physical layout is irrelevant—each page maps independently via the [[The Page Table Stores Virtual-to-Physical Mappings|page table]].

## Simplified Free-Space Management

With segmentation, the OS needed sophisticated allocation algorithms ([[Best-Fit Allocation Minimizes Wasted Space but Requires Full Search|best-fit]], [[First-Fit and Next-Fit Trade Search Time for Simplicity|first-fit]], etc.) to minimize fragmentation. With paging, the free-frame list is trivial:

```c
// Segmentation: search for best-fitting hole
node_t* find_best_fit(size_t request) {
    // complex search, coalescing, splitting...
}

// Paging: grab any frame
frame_t allocate_frame() {
    return free_list_pop();  // O(1), any frame works
}
```

No searching, no splitting, no coalescing. The OS maintains a simple list (or bitmap) of free frames and hands out any available frame. This simplicity reduces bugs and improves performance.

## The Trade-Off: Bounded Internal Fragmentation

Paging introduces internal fragmentation: a 25 KB allocation uses 28 KB (7 × 4 KB pages), wasting 3 KB inside the last page. This waste is bounded:

- **Worst case**: one page minus one byte per allocation
- **Average case**: half a page per allocation

With 4 KB pages, average waste is 2 KB per distinct allocation—acceptable for most workloads. Contrast this with external fragmentation, which can grow unboundedly as memory churns through allocations and deallocations.

## Flexibility for the OS

Fixed-size units give the OS powerful capabilities:

**Sparse address spaces**: A process can have virtual pages 0 and 1,000,000 mapped while all pages in between are invalid. Only the mapped pages consume physical frames.

**Easy sharing**: Two processes can map the same physical frame by having their [[Page Table Entries Contain PFN and Control Bits|PTEs]] point to it. This enables shared libraries—read-only code pages are shared across all processes using that library.

**Demand paging**: The OS can load pages on-demand rather than bringing the entire address space into memory. Invalid PTEs (present=0) trigger page faults, letting the OS fetch pages from disk as needed.

## Historical Context

Paging replaced segmentation as the dominant memory management technique because its uniformity made systems simpler and more predictable. While segmentation offered elegant logical grouping (code, data, stack as distinct segments), the external fragmentation problem proved too costly. All major operating systems today (Linux, Windows, macOS) use paging as their primary memory management mechanism.
