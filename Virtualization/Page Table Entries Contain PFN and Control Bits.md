---
type: atomic
source: OSTEP Ch. 18
tags:
  - virtualization
  - memory
  - paging
  - hardware
related:
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[Virtual Addresses Split into VPN and Offset]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[User Mode and Kernel Mode Provide Dual Protection Levels]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
---

# Page Table Entries Contain PFN and Control Bits

> [!SUMMARY]
> Each page table entry (PTE) holds more than just the physical frame number (PFN). Control bits track validity, access permissions, modification status, and whether the page has been recently accessed. These bits enable the hardware to enforce protection and help the OS implement policies like demand paging and page replacement.

## Anatomy of a Page Table Entry

A typical 32-bit PTE layout:

```
31                  12 11  9 8 7 6 5 4 3 2 1 0
+----------------------+----+-+-+-+-+-+-+-+-+-+
|         PFN          |    |G|P|D|A|C|W|U|R|V|
+----------------------+----+-+-+-+-+-+-+-+-+-+
     20 bits                   control bits
```

The PFN occupies the high-order bits (20 bits if frames are 4 KB in a 32-bit physical space). The remaining bits encode control information.

## Essential Control Bits

**Valid bit (V)**: Indicates whether this mapping exists. If V=0, accessing this page triggers a fault. Invalid entries represent unmapped portions of the address space—for example, the gap between heap and stack that paging does not allocate.

**Protection bits (R, W, X or U/S)**: Control read, write, and execute permissions. A code page might be R+X (readable, executable, but not writable). A stack page is R+W. Attempting a disallowed access causes a protection fault. The user/supervisor bit (U) distinguishes pages accessible in [[User Mode and Kernel Mode Provide Dual Protection Levels|user mode]] from kernel-only pages.

**Dirty bit (D)**: Set by hardware when the page is written. The OS checks this before evicting a page—if dirty, the page must be written back to disk; if clean, it can simply be discarded. This optimization avoids unnecessary disk writes.

**Reference/Accessed bit (A)**: Set by hardware when the page is read or written. The OS periodically clears this bit and uses it to approximate which pages are "recently used." This information drives page replacement policies (e.g., clock algorithm approximating LRU).

**Present bit (P)**: In systems with swapping, indicates whether the page is currently in physical memory. P=0 with V=1 means the page exists but has been swapped to disk—accessing it triggers a page fault so the OS can load it back.

## How Hardware Uses These Bits

On each memory access, the memory management unit (MMU):

1. Looks up the PTE using the VPN
2. Checks V—if invalid, raise segmentation fault
3. Checks P—if not present, raise page fault (for OS to handle)
4. Checks protection bits against the access type—if disallowed, raise protection fault
5. Sets A (and D if writing)
6. Extracts PFN and forms physical address

All of this happens transparently, preserving the [[Memory Virtualization Goals - Transparency Efficiency and Protection|virtualization goals]] of transparency and protection.

## Example: x86 PTE

The x86 architecture uses a 32-bit PTE with:
- Bits 0: Present
- Bit 1: Read/Write (0=read-only, 1=writable)
- Bit 2: User/Supervisor
- Bit 5: Accessed
- Bit 6: Dirty
- Bits 12-31: PFN (assuming 4 KB pages)

This real-world structure shows how the abstract concepts map to actual hardware implementations.
