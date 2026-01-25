---
type: atomic
source: OSTEP Ch. 19
tags:
  - virtualization
  - memory
  - paging
  - hardware
  - tlb
related:
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
  - "[[Virtual Addresses Split into VPN and Offset]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
---

# The TLB Caches Address Translations for Fast Access

> [!SUMMARY]
> The Translation Lookaside Buffer (TLB) is a small, fast hardware cache that stores recently used virtual-to-physical address mappings. Without a TLB, every memory access would require first consulting the page table in memory—doubling access time. The TLB exploits spatial and temporal locality to make the common case (translation cache hit) extremely fast.

## The Performance Problem

Paging introduces a critical performance issue. Each memory reference now requires *two* memory accesses:

1. Access the page table to translate VPN → PFN
2. Access the actual data at the physical address

This would effectively halve memory performance—an unacceptable cost. The hardware solution is the TLB.

## What the TLB Does

The TLB is part of the chip's memory management unit (MMU). It stores a small number of frequently used [[Virtual Addresses Split into VPN and Offset|address translations]]—typically 32 to 1024 entries. On each memory access:

1. Extract the VPN from the virtual address
2. Check if the TLB contains an entry for this VPN
3. If **TLB hit**: use the cached PFN immediately—no memory access needed for translation
4. If **TLB miss**: consult the [[The Page Table Stores Virtual-to-Physical Mappings|page table]] in memory, update the TLB, then retry

A TLB hit costs a few CPU cycles. A TLB miss costs dozens to hundreds of cycles (memory access latency). The goal is to hit almost always.

## Why TLBs Work: Locality

Programs exhibit strong **locality of reference**:

- **Temporal locality**: If an address was accessed recently, it will likely be accessed again soon
- **Spatial locality**: If an address was accessed, nearby addresses will likely be accessed soon

A loop accessing an array touches the same pages repeatedly (temporal). Sequential access stays within pages for many iterations (spatial). With 4 KB pages and a 32-entry TLB, a program looping over a 128 KB array achieves excellent hit rates—32 pages cover the working set.

## TLB Hit Rates in Practice

Consider accessing a 10-element array, each element 4 bytes, on a system with 16-byte pages:

```
Array: [a0][a1][a2][a3][a4][a5][a6][a7][a8][a9]
Pages:  |--- page 0 ---|--- page 1 ---|-- page 2 --|
```

- Access a[0]: TLB miss (page 0 loaded)
- Access a[1], a[2], a[3]: TLB hits (same page)
- Access a[4]: TLB miss (page 1 loaded)
- Access a[5], a[6], a[7]: TLB hits
- Access a[8]: TLB miss (page 2 loaded)
- Access a[9]: TLB hit

Result: 3 misses, 7 hits = **70% hit rate** even with this tiny example. Larger pages and larger TLBs yield hit rates exceeding 99% for typical workloads.

## The TLB as a Fully Associative Cache

Unlike CPU data caches, TLBs are typically **fully associative**: any translation can go in any slot. This maximizes flexibility but requires checking all entries in parallel (using parallel hardware comparators). The small size makes this feasible.

