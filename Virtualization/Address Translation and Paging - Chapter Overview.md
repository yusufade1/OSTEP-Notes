---
type: overview
source: "OSTEP Ch. 15-16, 18-20: Address Translation & Paging"
tags:
  - virtualization
  - memory
  - paging
  - tlb
related:
  - "[[Virtualization MOC]]"
  - "[[Address Translation Maps Virtual Addresses to Physical Addresses]]"
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[The TLB Caches Address Translations for Fast Access]]"
prerequisites:
  - "[[Memory - Chapter Overview]]"
---

# Address Translation & Paging - Chapter Overview

> [!SUMMARY]
> These chapters cover the hardware and software mechanisms that enable efficient memory virtualization. Starting with simple **base-and-bounds**, we progress through **segmentation** to the modern standard: **paging**. We explore how the **TLB** makes paging fast and how **multi-level page tables** keep the memory overhead manageable.


## Key Mechanisms

- **[[Address Translation Maps Virtual Addresses to Physical Addresses]]** — The fundamental mechanism where hardware transforms virtual addresses into physical ones.
- **[[Base-and-Bounds Provides Dynamic Relocation]]** — The simplest translation mechanism using two registers.
- **[[Segmentation Generalizes Base-and-Bounds with Multiple Segments]]** — Reducing internal fragmentation by allowing different parts of the address space (code/stack/heap) to be placed independently.
- **[[Paging Divides Memory into Fixed-Size Pages and Frames]]** — Solving external fragmentation by using fixed-size units.
- **[[The TLB Caches Address Translations for Fast Access]]** — A hardware cache that makes paging performance viable.
- **[[Multi-Level Page Tables Save Space Through Demand Allocation]]** — Managing large, sparse address spaces without wasting physical memory.

## Chapter Questions

1. Why is hardware support (MMU) essential for address translation?
2. How does paging solve the external fragmentation problem of segmentation?
3. What happens to the TLB during a context switch?
4. How do multi-level page tables trade off speed for space?
