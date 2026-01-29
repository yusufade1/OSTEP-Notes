---
type: mechanism
source: "OSTEP Ch. 20: Paging: Smaller Tables"
tags:
  - virtualization
  - memory
  - paging
  - segmentation
  - page-tables
related:
  - "[[Linear Page Tables Waste Memory for Large Address Spaces]]"
  - "[[Multi-Level Page Tables Save Space Through Demand Allocation]]"
  - "[[Segmentation Generalizes Base-and-Bounds with Multiple Segments]]"
  - "[[The Segment Table Maps Segment Numbers to Base-Bounds Pairs]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Linear Page Tables Waste Memory for Large Address Spaces]]"
  - "[[Segmentation Generalizes Base-and-Bounds with Multiple Segments]]"
---

# Hybrid Paging and Segmentation Combines Both Approaches

> [!SUMMARY]
> A hybrid scheme uses segmentation at the top level (code, heap, stack each have their own page table) and paging within each segment. This avoids allocating page table entries for the huge unmapped gap between heap and stack. The segment base register points to a page table rather than to data, and bounds limit page table size to actual segment usage.

## The Problem with Pure Paging

A pure linear page table has entries for every virtual page, including the vast unmapped region between heap and stack. Consider a process with:

- Code: pages 0-9 (40 KB)
- Heap: pages 10-20 (44 KB)
- Stack: pages 1,000,000-1,000,010 (44 KB at top of address space)

A linear table needs 1 million entries even though only 31 pages are used.

## Hybrid Structure

Instead of one page table for the entire address space, maintain a separate page table per segment:

```
Segment Registers (3 pairs)
Segment    Base (→ page table)    Bounds (page table size)
-------    -------------------    ----------------------
Code       0x1000 (PT_code)       10 entries
Heap       0x2000 (PT_heap)       11 entries
Stack      0x3000 (PT_stack)      11 entries
```

Each base register points to that segment's page table. Bounds indicate how many valid entries exist.

## Address Translation

The virtual address format includes a segment selector:

```
Virtual Address
+-----+----------+--------+
| Seg | VPN      | Offset |
| 2b  | 12b      | 12b    |
+-----+----------+--------+
```

Translation steps:
1. Use segment bits to select which (base, bounds) pair
2. Check VPN against bounds (protection)
3. Index into that segment's page table at `base + VPN × sizeof(PTE)`
4. Extract PFN and combine with offset

## Space Savings

With the example above:
- Code page table: 10 × 4 = 40 bytes
- Heap page table: 11 × 4 = 44 bytes
- Stack page table: 11 × 4 = 44 bytes
- **Total: 128 bytes** plus segment registers

Compare to 4 MB for a linear table spanning the same virtual address range.

## Trade-Offs

**Advantages over pure paging**:
- No table entries for unmapped regions
- Each segment's table sized to actual usage
- Clean separation of segment concerns

**Disadvantages**:
- Reintroduces [[External Fragmentation Wastes Memory Between Variable-Sized Segments|external fragmentation]]—segment page tables are variable-sized allocations in kernel memory
- More complex address translation hardware
- Segments must still manage growth (heap expands → page table grows)

## External Fragmentation Returns

If the code segment's page table needs 40 bytes and heap's needs 44 bytes, the kernel allocates variable-sized chunks. Over time, as segments grow and shrink, kernel memory fragments. This is less severe than data-level fragmentation (page tables are smaller and change less frequently), but the problem resurfaces.

## Historical Context

The Multics system and early Intel 386 processors used hybrid paging-segmentation. The complexity led most systems to prefer pure multi-level paging—the [[Multi-Level Page Tables Save Space Through Demand Allocation|multi-level approach]] achieves similar space savings without the external fragmentation problem, since all page table chunks are identically sized.
