---
type: mechanism
source: "OSTEP Ch. 20: Paging: Smaller Tables"
tags:
  - virtualization
  - memory
  - paging
  - page-tables
  - fragmentation
related:
  - "[[Linear Page Tables Waste Memory for Large Address Spaces]]"
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
  - "[[Multi-Level Page Tables Save Space Through Demand Allocation]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Linear Page Tables Waste Memory for Large Address Spaces]]"
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
---

# Larger Pages Reduce Table Size but Increase Internal Fragmentation

> [!SUMMARY]
> Using larger page sizes directly reduces the number of page table entries needed. Doubling the page size halves the page count and thus halves the page table. However, larger pages waste more memory within each page when allocations do not align to page boundaries—trading the external fragmentation problem of segmentation for worse internal fragmentation.

## The Math: Page Size vs Table Entries

For a 32-bit address space:

| Page Size | Pages Needed | PTE Count | Table Size (4-byte PTEs) |
|-----------|--------------|-----------|--------------------------|
| 4 KB      | 2^20         | 1M        | 4 MB                     |
| 16 KB     | 2^18         | 256K      | 1 MB                     |
| 4 MB      | 2^10         | 1K        | 4 KB                     |

With 4 MB "huge pages," the [[Linear Page Tables Waste Memory for Large Address Spaces|page table shrinks from 4 MB to 4 KB]]—a dramatic improvement. Many architectures support multiple page sizes: x86-64 offers 4 KB, 2 MB, and 1 GB pages.

## The Internal Fragmentation Cost

The downside is waste within each page. If a process allocates 5 KB with 4 MB pages, it receives one 4 MB page but uses only 5 KB—wasting 99.87% of the page.

```
4 MB Page
+------------------------+
|  used (5 KB)           |
+------------------------+
|                        |
|  wasted (4091 KB)      |  <- internal fragmentation
|                        |
+------------------------+
```

Small allocations become extremely wasteful. Even with typical allocations, the expected waste per segment averages half a page. With 4 MB pages, that means 2 MB wasted per distinct memory region.

## When Large Pages Make Sense

Large pages are beneficial when:

1. **Memory-intensive workloads**: Databases and scientific computing allocate gigabytes. A 1 GB allocation with 4 MB pages wastes at most 4 MB (0.4%).
2. **TLB coverage**: Each [[The TLB Caches Address Translations for Fast Access|TLB entry]] covers more memory. A 64-entry TLB covers 256 KB with 4 KB pages but 256 MB with 4 MB pages.
3. **Fewer page faults**: Large contiguous mappings mean fewer entries to manage during I/O.

## When Large Pages Hurt

Large pages are harmful when:

1. **Small allocations dominate**: Shell scripts, configuration tools, and many utilities allocate small buffers. Large pages waste most of each allocation.
2. **Mixed workloads**: A system running both databases and small utilities cannot choose a single optimal page size.
3. **Memory pressure**: When memory is scarce, the inability to reclaim part of a large page limits flexibility.

## Modern Hybrid Approach

Systems do not choose a single page size. Instead, they use small pages by default and offer large pages for specific allocations:

- **Linux huge pages**: Processes explicitly request 2 MB or 1 GB pages via mmap flags
- **Transparent huge pages**: The kernel automatically promotes contiguous small-page regions to large pages

This gives applications the best of both: small pages for flexibility, large pages where beneficial. The page table structure must accommodate multiple sizes, typically using [[Multi-Level Page Tables Save Space Through Demand Allocation|multi-level tables]] with entries that can describe either a page or a pointer to a sub-table.
