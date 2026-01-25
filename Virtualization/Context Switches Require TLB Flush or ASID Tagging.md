---
type: atomic
source: OSTEP Ch. 19
tags:
  - virtualization
  - memory
  - paging
  - tlb
  - context-switch
  - scheduling
related:
  - "[[The TLB Caches Address Translations for Fast Access]]"
  - "[[TLB Entries Store VPN PFN and Control Fields Including ASID]]"
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges]]"
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[TLB Entries Store VPN PFN and Control Fields Including ASID]]"
  - "[[Context Switch Saves and Restores Process State]]"
---

# Context Switches Require TLB Flush or ASID Tagging

> [!SUMMARY]
> When switching between processes, the TLB contains translations from the old process that are invalid for the new one. Two solutions exist: flush the entire TLB (simple but costly) or tag entries with Address Space Identifiers (ASIDs) so entries from different processes coexist safely. ASIDs reduce context switch overhead but add hardware complexity.

## The Problem: Stale Translations

Each process has its own [[The Page Table Stores Virtual-to-Physical Mappings|page table]] and address space. Virtual address `0x1000` in process A might map to physical frame `0x5000`, while the same virtual address in process B maps to frame `0x9000`.

If a [[Context Switch Saves and Restores Process State|context switch]] from A to B leaves A's TLB entries intact, B might use A's translation—accessing A's physical memory instead of its own. This is both a correctness and security disaster.

## Solution 1: TLB Flush

The simplest approach: invalidate all TLB entries on every context switch.

```
context_switch(A → B):
    save A's registers to PCB
    flush_tlb()           # Invalidate all entries
    load B's page table base register
    restore B's registers from PCB
```

After the flush, B starts with an empty TLB and incurs compulsory misses for every page it touches until the TLB warms up.

**Advantage**: Simple hardware—no ASID support needed.

**Disadvantage**: Every context switch causes a burst of TLB misses. With frequent switches (e.g., time-sharing with small time slices), this becomes significant overhead.

## Solution 2: ASID Tagging

With [[TLB Entries Store VPN PFN and Control Fields Including ASID|ASIDs]], each TLB entry is tagged with the process that owns it. The hardware lookup matches (VPN, ASID), not just VPN.

```
context_switch(A → B):
    save A's registers to PCB
    set_current_ASID(B.asid)   # Change ASID register
    load B's page table base register
    restore B's registers from PCB
    # TLB entries from A remain but won't match B's lookups
```

Now A's entries (with ASID=A) remain in the TLB but cannot match B's accesses (which require ASID=B). If B switches back to A later, A's entries are still valid—no refill needed.

## ASID Size and Wraparound

ASID fields are typically small—8 bits (256 values) is common. With more than 256 processes, the OS must recycle ASIDs:

1. When a new process needs an ASID, check if all are in use
2. If so, pick a victim ASID currently assigned to a sleeping process
3. Flush all TLB entries with that ASID
4. Assign the freed ASID to the new process

This is rare in practice—most systems have fewer than 256 active processes in a scheduling window.

## Impact on Scheduling Performance

TLB handling interacts with scheduling decisions. The cost of context switches noted in scheduling chapters includes TLB overhead:

| Approach | Context Switch Cost | TLB State After |
|----------|--------------------:|-----------------|
| TLB flush | Higher | Empty (cold) |
| ASID tagging | Lower | Preserved (warm) |

This contributes to [[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges|cache affinity]]—running a process on the same CPU preserves both TLB entries and CPU cache contents. MQMS (multi-queue multiprocessor scheduling) exploits this by keeping processes on their assigned CPUs.

## Kernel Entries: The Global Bit

Kernel pages are mapped identically in all processes (the upper portion of each address space). Rather than duplicating kernel entries for every ASID, the **global bit** (G) tells hardware to ignore ASID matching. Global entries persist across all context switches, keeping kernel translations warm.

