---
type: atomic
source: OSTEP Ch. 18
tags:
  - virtualization
  - memory
  - paging
  - data-structures
related:
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
  - "[[Virtual Addresses Split into VPN and Offset]]"
  - "[[Address Translation Maps Virtual Addresses to Physical Addresses]]"
  - "[[The Segment Table Maps Segment Numbers to Base-Bounds Pairs]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
---

# The Page Table Stores Virtual-to-Physical Mappings

> [!SUMMARY]
> The page table is a per-process data structure that maps virtual page numbers (VPNs) to physical frame numbers (PFNs). Indexed by VPN, each entry records which physical frame holds that virtual page plus control information. The page table replaces the segment table and enables flexible, non-contiguous physical allocation.

## Structure: An Array Indexed by VPN

The simplest page table is a linear array with one entry per virtual page:

```
Page Table for Process P
Index (VPN)    Entry (PTE)
-----------    -----------
    0      ->  [frame 7, valid=1, prot=RX]
    1      ->  [frame 3, valid=1, prot=RW]
    2      ->  [frame -, valid=0]          <- unmapped
    3      ->  [frame 5, valid=1, prot=RW]
```

To translate virtual page 1, the hardware looks up entry 1 and finds frame 3. The offset within the page stays the same—only the page/frame number changes.

## Per-Process Page Tables

Each process has its own page table, so the same virtual address (e.g., page 0) can map to different physical frames in different processes. This provides [[The Address Space Abstracts Physical Memory for Each Process|address space isolation]]—process A's page 0 and process B's page 0 occupy completely separate physical memory.

During a [[Context Switch Saves and Restores Process State|context switch]], the OS updates a hardware register (the **page table base register**) to point to the new process's page table. The CPU then uses the new mappings for all subsequent memory accesses.

## Where Page Tables Live

Page tables themselves reside in memory—typically in kernel-managed physical frames. A 32-bit address space with 4 KB pages has 2^20 = 1 million pages, requiring a 1-million-entry page table. If each [[Page Table Entries Contain PFN and Control Bits|page table entry]] is 4 bytes, that is 4 MB per process. This size motivates more sophisticated structures like multi-level page tables (explored in later chapters).

## Comparison to Segmentation

The [[The Segment Table Maps Segment Numbers to Base-Bounds Pairs|segment table]] had a few entries (code, heap, stack) with base-bounds pairs. The page table has many entries (one per page) but each entry is simpler—just a frame number and flags. The trade-off:

| Aspect | Segment Table | Page Table |
|--------|---------------|------------|
| Entries | Few (3-8) | Many (thousands to millions) |
| Entry contents | Base + bounds | Frame number + bits |
| Allocation granularity | Variable | Fixed |
| Fragmentation | External | Internal (bounded) |

## Translation Overview

The hardware translation flow:
1. Extract VPN from [[Virtual Addresses Split into VPN and Offset|virtual address]]
2. Use VPN to index into page table
3. Read the [[Page Table Entries Contain PFN and Control Bits|PTE]] and check validity
4. Combine PFN with offset to form physical address

This happens on every memory access, making page table lookup performance critical—hence the importance of [[Address Translation Maps Virtual Addresses to Physical Addresses|translation caches (TLBs)]] covered in subsequent chapters.
