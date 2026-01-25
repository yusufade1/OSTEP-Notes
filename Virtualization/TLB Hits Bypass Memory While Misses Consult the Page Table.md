---
type: atomic
source: OSTEP Ch. 19
tags:
  - virtualization
  - memory
  - paging
  - tlb
  - hardware
related:
  - "[[The TLB Caches Address Translations for Fast Access]]"
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
  - "[[Virtual Addresses Split into VPN and Offset]]"
  - "[[Hardware-Managed and Software-Managed TLBs Differ in Miss Handling]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The TLB Caches Address Translations for Fast Access]]"
---

# TLB Hits Bypass Memory While Misses Consult the Page Table

> [!SUMMARY]
> The TLB hit/miss algorithm determines how every memory access is translated. On a TLB hit, the hardware extracts the physical frame number directly from the cache—no memory access needed. On a miss, the system must walk the page table in memory, install the translation in the TLB, and retry. The hit path is fast (a few cycles); the miss path is slow (dozens to hundreds of cycles).

## The TLB Control Flow Algorithm

Every memory access executes the following logic in hardware:

```
1. Extract VPN from virtual address
2. Search TLB for entry with matching VPN
3. If TLB HIT:
   a. Check protection bits (valid, read/write/execute)
   b. If protection violation → raise exception
   c. Extract PFN, combine with offset → physical address
   d. Access memory at physical address
4. If TLB MISS:
   a. Handle miss (hardware or software, see related note)
   b. Update TLB with new translation
   c. Retry the instruction (go to step 1)
```

The critical insight: steps 3a-3d happen entirely in hardware and take only a few cycles. Step 4 is the slow path.

## TLB Hit: The Fast Path

When the VPN is found in the TLB:

1. **Parallel lookup**: Hardware checks all TLB entries simultaneously using content-addressable memory (CAM)
2. **Protection check**: The matching entry's protection bits are compared against the access type (read/write/execute)
3. **PFN extraction**: The physical frame number from the TLB entry is concatenated with the offset from the original virtual address
4. **Memory access**: The physical address goes to the memory subsystem

This entire sequence adds only 1-3 cycles to the memory access latency. The translation is effectively free.

## TLB Miss: The Slow Path

When the VPN is not in the TLB, the system must fetch the translation from the [[The Page Table Stores Virtual-to-Physical Mappings|page table]]:

1. **Page table walk**: Traverse the page table structure in memory to find the PTE
2. **Validity check**: If the [[Page Table Entries Contain PFN and Control Bits|PTE]] is invalid, raise a segmentation fault
3. **TLB update**: Install the translation (VPN → PFN + protection bits) in the TLB
4. **Eviction if needed**: If the TLB is full, select a victim entry to replace
5. **Retry**: Re-execute the original instruction—now it will hit in the TLB

The page table walk may require one memory access (single-level page table) or multiple (multi-level page tables). Each access costs 50-100+ nanoseconds on modern systems.

## Protection Faults vs. Page Faults

Two types of exceptions can occur during TLB lookup:

**Protection fault**: TLB entry exists but the access violates permissions (e.g., writing to a read-only page). The OS terminates the process or delivers SIGSEGV.

**Page fault** (present bit = 0): The translation exists but the page is not in physical memory (swapped to disk). The OS loads the page from disk, updates the PTE, and retries—a topic covered in swapping/demand paging.

## Why Retry Works

After a TLB miss is handled, the instruction is re-executed from the beginning. This seems wasteful, but it simplifies the hardware: the TLB miss handler does not need to "complete" the memory access itself. It simply fills the TLB and returns. The retry is transparent to software—the program never knows the miss occurred.

