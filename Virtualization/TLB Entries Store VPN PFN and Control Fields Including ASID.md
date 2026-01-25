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
  - "[[TLB Hits Bypass Memory While Misses Consult the Page Table]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
  - "[[Context Switches Require TLB Flush or ASID Tagging]]"
  - "[[Virtual Addresses Split into VPN and Offset]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The TLB Caches Address Translations for Fast Access]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
---

# TLB Entries Store VPN PFN and Control Fields Including ASID

> [!SUMMARY]
> Each TLB entry contains not just a translation (VPN → PFN) but also control fields for validity, protection, and process identification. The valid bit indicates whether the entry is usable. Protection bits enforce read/write/execute permissions. The Address Space Identifier (ASID) tags entries by process, enabling TLB sharing across context switches.

## Anatomy of a TLB Entry

A typical TLB entry layout:

```
+---------+--------+-------+-----+-----+-------+---------+
|   VPN   |  PFN   | Valid | Prot| Ref | Dirty |  ASID   |
+---------+--------+-------+-----+-----+-------+---------+
   tag      data    status  R/W/X              process ID
```

Unlike the [[Page Table Entries Contain PFN and Control Bits|page table entry]] which is indexed by VPN, TLB entries store the VPN explicitly as a "tag" because the TLB is fully associative—any entry can hold any translation.

## VPN and PFN: The Translation

The **virtual page number** (VPN) is the tag used for lookup. When the CPU accesses address `0x1234_5678` with 4 KB pages, it extracts VPN = `0x12345` and searches for a TLB entry with that tag.

The **physical frame number** (PFN) is the translation result. If VPN `0x12345` maps to PFN `0x7ABCD`, the physical address becomes `0x7ABCD_678` (PFN concatenated with the original offset).

## Valid Bit

The **valid bit** indicates whether this TLB entry contains a usable translation. An invalid entry might:

- Be empty (never filled or recently evicted)
- Correspond to an unmapped virtual page
- Have been invalidated by the OS

On access to an entry with valid=0, the TLB reports a miss, triggering miss handling.

## Protection Bits

TLB entries cache the page's protection information:

- **Read (R)**: Page can be read
- **Write (W)**: Page can be written
- **Execute (X)**: Page contains executable code
- **User/Supervisor (U)**: Page accessible in user mode

On every access, the hardware compares the requested operation against these bits. Writing to a read-only page triggers a protection fault—even if the VPN matches.

## ASID: Address Space Identifier

The **ASID** field tags each entry with a process identifier. This is crucial for multi-process systems. Without ASIDs, VPN `0x1000` from process A would conflict with VPN `0x1000` from process B—both have the same tag but map to different physical frames.

With ASIDs, the lookup matches (VPN, ASID) pairs:

```
TLB lookup: (VPN = 0x1000, ASID = 5)
Entry 0: (VPN = 0x1000, ASID = 3, PFN = 0x2000) → No match (ASID differs)
Entry 1: (VPN = 0x1000, ASID = 5, PFN = 0x9000) → Match!
```

ASIDs enable [[Context Switches Require TLB Flush or ASID Tagging|TLB entries to persist across context switches]]—entries from other processes simply do not match.

## Global Bit

Some pages are mapped identically in all processes—kernel pages, for instance. The **global bit** (G) tells the hardware to ignore the ASID when matching. A global entry with VPN `0xC000_0000` matches regardless of the current process's ASID, avoiding redundant entries for shared kernel mappings.

## Dirty and Reference Bits

Like page table entries, TLB entries often include:

- **Dirty (D)**: Set when the page is written (for write-back tracking)
- **Reference (R)**: Set when the page is accessed (for replacement policies)

These bits may be maintained in the TLB and periodically written back to the page table, or the page table may be the authoritative source with the TLB copying on fill.

