---
type: atomic
source: OSTEP Ch. 16
tags:
  - virtualization
  - memory
  - segmentation
  - granularity
related:
  - "[[Segmentation Generalizes Base-and-Bounds with Multiple Segments]]"
  - "[[The Segment Table Maps Segment Numbers to Base-Bounds Pairs]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The Segment Table Maps Segment Numbers to Base-Bounds Pairs]]"
---

# Coarse-Grained vs Fine-Grained Segmentation Trade Flexibility for Simplicity

> [!SUMMARY]
> Segmentation systems vary in how many segments they support. Coarse-grained segmentation uses a small number of large segments (typically code, heap, and stack), requiring only a few bits in the virtual address for segment selection. Fine-grained segmentation supports many smaller segments (per-function, per-array), enabling more precise memory sharing and protection at the cost of larger segment tables and more complex hardware.

## Coarse-Grained Segmentation

The simplest segmentation systems divide the address space into just three or four segments. A 2-bit segment selector suffices:

```
Seg 00 → Code
Seg 01 → Heap
Seg 10 → Stack
Seg 11 → (unused or extra data)
```

The hardware needs only 3-4 sets of base-bounds registers—fast to check, small to save during [[Context Switch Saves and Restores Process State|context switches]]. This is the approach used in early systems like the PDP and the design OSTEP describes throughout its segmentation chapter.

**Advantages:**
- Simple hardware: a few dedicated registers per segment.
- Fast context switch: only 3-4 register pairs to save/restore.
- Easy for the compiler: it knows exactly which segment each reference belongs to.

**Limitations:**
- The segments are still large and variable-sized—if the heap is 100 KB, that entire region must be contiguous in physical memory.
- Sharing is limited to entire segments (e.g., share all code or none of it).
- Internal waste can still occur within a segment (unused heap space up to the bounds).

## Fine-Grained Segmentation

Systems like Multics and the Intel x86 (in segmented mode) supported hundreds or thousands of segments. Each function, array, or data structure could have its own segment:

```
Seg 0  → main() code         (512 bytes, RX)
Seg 1  → helper() code       (256 bytes, RX)
Seg 2  → global_array        (4 KB, RW)
Seg 3  → user_input_buffer   (1 KB, RW)
...
Seg 47 → stack               (8 KB, RW, grows negative)
```

This enables fine-grained **sharing** (share one function without sharing the whole code segment) and **protection** (make one array read-only while another is writable).

**Advantages:**
- Precise sharing: two processes can share a single function's segment.
- Precise protection: each object can have tailored access permissions.
- Smaller segments mean each one is easier to place in physical memory.

**Limitations:**
- The [[The Segment Table Maps Segment Numbers to Base-Bounds Pairs|segment table]] grows large—it must be stored in memory rather than registers, adding a memory reference on every access (similar to the page table problem that TLBs solve).
- The compiler must manage segment assignments, complicating the toolchain.
- [[External Fragmentation Wastes Memory Between Variable-Sized Segments|External fragmentation]] worsens with many variable-sized segments, since each creates potential gaps.

## Why Coarse Won (Historically)

Most real systems converged on coarse segmentation or abandoned segmentation entirely. Fine-grained segmentation's complexity—both in hardware and in compiler support—proved harder to manage than the fixed-size approach of [[Address Translation Maps Virtual Addresses to Physical Addresses|paging]]. Modern x86 processors retain segment registers for backward compatibility but operate in a "flat" mode where all segments span the entire address space, effectively disabling segmentation in favor of paging.
