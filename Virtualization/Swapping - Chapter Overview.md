---
type: overview
source: "OSTEP Ch. 21-22: Swapping"
tags:
  - virtualization
  - memory
  - swapping
related:
  - "[[Virtualization MOC]]"
  - "[[Swap Space Extends Memory Beyond Physical Limits]]"
  - "[[Page Faults Trigger the Swap Mechanism]]"
  - "[[LRU Approximates Optimal by Evicting Least Recently Used Pages]]"
prerequisites:
  - "[[Address Translation and Paging - Chapter Overview]]"
---

# Swapping - Chapter Overview

> [!SUMMARY]
> These chapters explore how the OS uses secondary storage (disk) to provide the illusion of a memory space larger than physical RAM. We cover the mechanisms for **swapping** pages in and out, and the **replacement policies** used to decide which pages to evict when memory is full.


## Key Concepts

- **[[Swap Space Extends Memory Beyond Physical Limits]]** — Reserved space on disk used to hold pages that don't fit in physical memory.
- **[[The Present Bit Distinguishes Memory-Resident from Swapped Pages]]** — The mechanism in the page table entry that tells the hardware if a page is in RAM or on disk.
- **[[Page Faults Trigger the Swap Mechanism]]** — The exception handling flow that brings missing pages from disk into memory.
- **[[Optimal Page Replacement Sets the Theoretical Lower Bound]]** — The unreachable goal of evicting the page that will be accessed furthest in the future.
- **[[LRU Approximates Optimal by Evicting Least Recently Used Pages]]** — A practical policy based on the principle of temporal locality.
- **[[The Clock Algorithm Approximates LRU with a Reference Bit]]** — An efficient hardware-supported implementation of LRU.

## Chapter Questions

1. Why is swapping called "the final step" in memory virtualization?
2. What happens to a process while a page fault is being handled?
3. Why is LRU generally better than FIFO for page replacement?
4. What is thrashing, and how does the OS detect it?
