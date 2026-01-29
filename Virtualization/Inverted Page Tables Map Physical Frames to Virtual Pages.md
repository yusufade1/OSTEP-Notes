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
  - "[[Multi-Level Page Tables Save Space Through Demand Allocation]]"
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
  - "[[The TLB Caches Address Translations for Fast Access]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Linear Page Tables Waste Memory for Large Address Spaces]]"
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
---

# Inverted Page Tables Map Physical Frames to Virtual Pages

> [!SUMMARY]
> An inverted page table has one entry per physical frame rather than one entry per virtual page. Since physical memory is typically much smaller than the combined virtual address spaces of all processes, this dramatically reduces table size. The trade-off is that lookups require searching the table (often via hash table) rather than direct indexing by VPN.

## The Inversion

[[The Page Table Stores Virtual-to-Physical Mappings|Traditional page tables]] answer: "Given VPN, which PFN?" with direct indexing.

Inverted tables answer the reverse: "For each PFN, which (process, VPN) owns it?"

```
Traditional Page Table (per process)
VPN    PFN
0  ->  47
1  ->  23
2  ->  99
...

Inverted Page Table (system-wide)
PFN    Process ID    VPN
0      P1            12
1      P2            0
2      P1            5
...
```

## Space Advantage

Consider a system with 64-bit virtual addresses and 4 GB physical memory:

- **Traditional**: Each process needs 2^52 entries (for 4 KB pages in a 64-bit space)—impossible
- **Inverted**: 4 GB / 4 KB = 1 million entries total, regardless of process count

With 1 million 8-byte entries, the inverted table uses only 8 MB system-wide. This is constant regardless of how many processes run or how large their virtual address spaces are.

## The Search Problem

The inverted table cannot be indexed by VPN—the VPN does not determine the entry location. On a [[The TLB Caches Address Translations for Fast Access|TLB miss]], the system must find which PFN (if any) maps the requested (process ID, VPN) pair.

Linear search is O(frames)—far too slow with millions of frames. Solutions include:

### Hash Tables

Hash the (process ID, VPN) pair to find candidate entries:

```
hash_index = hash(pid, vpn) % table_size
```

The hash table entry either contains the mapping or points to a chain of entries that hashed to the same slot. Average lookup: O(1). Worst case (many collisions): O(chain length).

### Example Lookup

Process P1 accesses VPN 5:

1. Compute `hash(P1, 5) = 1000`
2. Look at entry 1000: `{pid=P1, vpn=5, pfn=42}` → match!
3. Return PFN 42

If entry 1000 held a different mapping, follow the collision chain until finding the match or reaching the end (page fault).

## Trade-Offs

| Aspect | Per-Process Table | Inverted Table |
|--------|-------------------|----------------|
| Space | Proportional to virtual space | Proportional to physical memory |
| Lookup | O(1) index | O(1) average hash, O(n) worst |
| Shared pages | Each process has an entry | Single entry, multiple processes via extra structure |
| Implementation | Simple array | Hash table + collision handling |

## Sharing Complexity

Sharing a physical frame between processes is awkward. The inverted table has one entry per frame, so it can only record one (pid, vpn) pair. Solutions include:

- **Chain of sharing processes**: Each entry links to processes sharing that frame
- **Separate sharing table**: Track sharing relationships outside the inverted table

## Historical Use

The IBM PowerPC architecture used inverted page tables. The technique is less common in modern x86/ARM systems, which prefer [[Multi-Level Page Tables Save Space Through Demand Allocation|multi-level tables]]. However, inverted tables remain relevant for systems with very large virtual address spaces relative to physical memory.
