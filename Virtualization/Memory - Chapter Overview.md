---
type: overview
source: "OSTEP Ch. 13-14, 17: Memory Management"
tags:
  - virtualization
  - memory
related:
  - "[[Virtualization MOC]]"
  - "[[The Address Space Abstracts Physical Memory for Each Process]]"
  - "[[malloc and free Manage Heap Memory Dynamically]]"
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
prerequisites: []
---

# Memory - Chapter Overview

> [!SUMMARY]
> These chapters introduce **memory virtualization**: the OS gives each process the illusion of its own private address space. We cover the address space abstraction, the memory API (`malloc`/`free`), and the mechanisms for **free-space management** that allow the allocator to manage variable-sized memory regions efficiently.


## Key Concepts

- **[[The Address Space Abstracts Physical Memory for Each Process]]** — The logical view of memory presented to applications.
- **[[Memory Virtualization Goals - Transparency Efficiency and Protection]]** — Core design requirements for memory isolation.
- **[[malloc and free Manage Heap Memory Dynamically]]** — The standard C library interface for heap allocation.
- **[[The Free List Data Structure Tracks Available Memory Regions]]** — How the allocator keeps track of available chunks.
- **[[Splitting and Coalescing Keep the Free List Efficient]]** — Mechanisms for managing chunk fragmentation.
- **[[Best-Fit Allocation Minimizes Wasted Space but Requires Full Search]]** — Common strategies for choosing a free block.

## Chapter Questions

1. Why does the address space place stack and heap at opposite ends?
2. What is the difference between internal and external fragmentation?
3. How does coalescing prevent the free list from being overwhelmed by tiny fragments?
4. What are the trade-offs between first-fit and best-fit allocation?