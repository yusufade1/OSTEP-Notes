---
type: mechanism
source: "OSTEP Ch. 20: Paging: Smaller Tables"
tags:
  - virtualization
  - memory
  - paging
  - page-tables
related:
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[The TLB Caches Address Translations for Fast Access]]"
  - "[[Multi-Level Page Tables Save Space Through Demand Allocation]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
---

# Linear Page Tables Waste Memory for Large Address Spaces

> [!SUMMARY]
> A simple linear page table contains one entry per virtual page, making its size proportional to the virtual address space—not to how much memory the process actually uses. For 32-bit address spaces with 4 KB pages, each process requires a 4 MB page table even if it only uses a tiny fraction of its address space. This overhead is unacceptable when running many processes.

## The Size Calculation

Consider a typical 32-bit system with 4 KB (2^12 byte) pages:

- Virtual address space: 2^32 bytes = 4 GB
- Number of virtual pages: 2^32 / 2^12 = 2^20 = 1,048,576 pages
- Size of each [[Page Table Entries Contain PFN and Control Bits|page table entry]]: 4 bytes
- **Total page table size**: 2^20 × 4 = 4 MB per process

With 100 processes, that is 400 MB of memory devoted solely to page tables—memory that cannot hold application data or code.

## The Sparse Address Space Problem

The waste is particularly egregious because most processes use only a small portion of their address space:

```
Virtual Address Space (32-bit)
+------------------+ 0xFFFFFFFF
|     stack        | <- a few KB to MB
+------------------+
|                  |
|    UNMAPPED      | <- vast empty region
|    (no pages)    |
|                  |
+------------------+
|      heap        | <- a few KB to MB
+------------------+
|      code        | <- a few KB to MB
+------------------+ 0x00000000
```

A small program might use 1 MB total (256 pages), yet its linear page table has 1 million entries. Over 99.97% of entries are marked invalid—wasted space tracking nothing.

## Why Linear Tables Exist

The linear design is conceptually simple: VPN directly indexes the array. Hardware extracts the VPN from the [[Virtual Addresses Split into VPN and Offset|virtual address]], multiplies by entry size, and adds to the page table base register:

```
PTE address = PTBR + (VPN × sizeof(PTE))
```

This single multiplication enables fast lookup. The [[The TLB Caches Address Translations for Fast Access|TLB]] handles the common case, so the hardware only consults the page table on misses.

## The Core Trade-Off

Linear page tables trade space for time:
- **Time**: O(1) lookup—a single indexed array access
- **Space**: O(virtual address space)—wastes memory on unused regions

For 32-bit systems, the 4 MB overhead was painful but tolerable. For 64-bit address spaces, linear tables are impossible—2^52 pages at 8 bytes each would require 32 petabytes per process.

## Solutions Overview

Three main approaches reduce page table memory:

1. **Larger pages**: Fewer pages means fewer entries, but wastes memory within each page
2. **Multi-level page tables**: Only allocate table portions that map used memory
3. **Inverted page tables**: One entry per physical frame instead of per virtual page

Each trades complexity for space efficiency, and modern systems often combine techniques.
