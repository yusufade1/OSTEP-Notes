---
type: mechanism
source: "OSTEP Ch. 20: Paging: Smaller Tables"
tags:
  - virtualization
  - memory
  - paging
  - page-tables
  - data-structures
related:
  - "[[Linear Page Tables Waste Memory for Large Address Spaces]]"
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Virtual Addresses Split into VPN and Offset]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
  - "[[The TLB Caches Address Translations for Fast Access]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Linear Page Tables Waste Memory for Large Address Spaces]]"
  - "[[Virtual Addresses Split into VPN and Offset]]"
---

# Multi-Level Page Tables Save Space Through Demand Allocation

> [!SUMMARY]
> Multi-level page tables divide the page table itself into page-sized chunks, using a page directory to track which chunks exist. Invalid directory entries indicate entire regions of unmapped address space—no second-level table is allocated. This trades one extra memory access per translation for dramatic space savings when address spaces are sparse.

## The Key Insight

A [[Linear Page Tables Waste Memory for Large Address Spaces|linear page table]] wastes space because it allocates entries for unused virtual pages. Multi-level tables observe: **if a large region is unmapped, we need not store its entries at all**.

The structure splits the VPN into multiple indices:
1. **Page Directory Index**: selects which page-table chunk
2. **Page Table Index**: selects entry within that chunk
3. **Offset**: unchanged, selects byte within page

## Two-Level Example: 14-bit Address Space

Consider a simple 14-bit address space with 64-byte pages:

- Total address space: 2^14 = 16 KB
- Page size: 64 bytes = 2^6
- VPN bits: 14 - 6 = 8 bits → 256 virtual pages
- Split VPN into: 4-bit page directory index + 4-bit page table index

```
14-bit Virtual Address
+------+------+--------+
| PDI  | PTI  | Offset |
| 4 b  | 4 b  |  6 b   |
+------+------+--------+
```

### Worked Translation Example

Translate virtual address `0x3A5B` (binary: `11 1010 0101 1011`):

1. **Extract fields**:
   - PDI = `1110` = 14
   - PTI = `1001` = 9
   - Offset = `011011` = 27

2. **Walk the structure**:
   ```
   Page Directory (16 entries)
   Index  Entry
   ...
   14  -> [valid=1, points to PT at frame 100]
   ...

   Page Table at frame 100 (16 entries)
   Index  Entry
   ...
   9   -> [valid=1, PFN=55]
   ...
   ```

3. **Compute physical address**:
   - PFN = 55
   - Physical address = (55 × 64) + 27 = 3520 + 27 = **3547** = `0xDDB`

## Space Savings

With 256 virtual pages and 4-byte [[Page Table Entries Contain PFN and Control Bits|PTEs]], a linear table needs 1 KB. With two levels:

- Page directory: 16 entries × 4 bytes = 64 bytes
- Each page table chunk: 16 entries × 4 bytes = 64 bytes

If only code (pages 0-15) and stack (pages 240-255) are mapped:
- Directory: 64 bytes (always present)
- Two page table chunks: 2 × 64 = 128 bytes
- **Total: 192 bytes** vs 1 KB linear

The savings scale dramatically: a 32-bit system with mostly unmapped regions might use 100 KB instead of 4 MB.

## The Time-Space Trade-Off

Multi-level tables add indirection. On a [[The TLB Caches Address Translations for Fast Access|TLB miss]], the hardware must:
1. Read the page directory entry
2. Read the page table entry
3. Access the actual data

Two memory accesses before reaching data (three total). Deeper hierarchies (x86-64 uses 4 levels) add more. The TLB makes this tolerable—hits bypass all levels.

## Why Page-Sized Chunks

Each page table chunk fits exactly in one page (e.g., 1024 4-byte entries in 4 KB). This means:
- The OS allocates page table chunks from the same free list as data pages
- No internal fragmentation within page table memory
- Clean memory management—page tables are just another use of physical frames
