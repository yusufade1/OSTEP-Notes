---
type: mechanism
source: "OSTEP Ch. 18: Paging: Introduction"
tags:
  - virtualization
  - memory
  - paging
  - address-translation
related:
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[Page Table Entries Contain PFN and Control Bits]]"
  - "[[Address Translation Maps Virtual Addresses to Physical Addresses]]"
  - "[[The Segment Table Maps Segment Numbers to Base-Bounds Pairs]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Paging Divides Memory into Fixed-Size Pages and Frames]]"
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
---

# Virtual Addresses Split into VPN and Offset

> [!SUMMARY]
> Every virtual address naturally decomposes into two parts: the virtual page number (VPN) identifying which page, and the offset identifying the byte within that page. The hardware uses the VPN to look up the physical frame number (PFN) in the page table, then combines the PFN with the unchanged offset to form the physical address.

## The Address Split

For a system with page size P:
- **Offset**: the low-order bits (log₂(P) bits) specify the position within the page
- **VPN**: the remaining high-order bits identify which page

With 4 KB (2^12 byte) pages and 32-bit addresses:
```
31                    12 11                    0
+------------------------+----------------------+
|         VPN            |       Offset         |
|      (20 bits)         |      (12 bits)       |
+------------------------+----------------------+
```

The 12-bit offset indexes any byte within the 4096-byte page. The 20-bit VPN can address 2^20 = ~1 million pages, covering a 4 GB virtual space.

## Worked Example: 16-Bit Address Space

Consider a smaller system:
- 16-bit virtual addresses (64 KB address space)
- 4 KB pages (12-bit offset)
- Therefore: 4-bit VPN (16 pages)

**Virtual address 0x3A5B (15,451 decimal):**
```
Binary: 0011 1010 0101 1011
             |         |
        +----+    +----+
        |         |
      VPN=3    Offset=0xA5B (2,651)
```

The VPN is 3 (bits 15-12), and the offset is 0xA5B (bits 11-0).

**Page table lookup:**
```
VPN    PFN
---    ---
 0      5
 1      2
 2      -   (invalid)
 3      7   <- our entry
```

VPN 3 maps to PFN 7.

**Physical address formation:**
```
Physical address = PFN << 12 | Offset
                 = 7 << 12 | 0xA5B
                 = 0x7000 | 0xA5B
                 = 0x7A5B (31,323 decimal)
```

The translation replaces the VPN with the PFN while preserving the offset exactly:

```
Virtual:   0011 | 1010 0101 1011
             ^VPN=3    offset
                  ↓
Physical:  0111 | 1010 0101 1011
             ^PFN=7    same offset
```

## Why the Offset Stays Unchanged

Pages and frames are the same size—this is the fundamental invariant of paging. Byte 500 within virtual page 3 is byte 500 within physical frame 7. The translation only changes which block of memory is accessed, not the position within that block.

This contrasts with [[The Segment Table Maps Segment Numbers to Base-Bounds Pairs|segmentation]], where the offset is added to a base address (potentially with bounds checking). In paging, the offset passes through unchanged—the page/frame number is simply swapped.

## Hardware Implementation

The MMU performs this split on every memory reference:
1. Mask and shift to extract VPN from virtual address
2. Index into [[The Page Table Stores Virtual-to-Physical Mappings|page table]] with VPN
3. Read [[Page Table Entries Contain PFN and Control Bits|PTE]], check validity and permissions
4. Concatenate PFN with original offset to produce physical address

This happens in hardware for speed, but conceptually is a simple array lookup plus bit manipulation.
