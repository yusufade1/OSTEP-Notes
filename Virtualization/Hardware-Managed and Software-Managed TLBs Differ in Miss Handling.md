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
  - "[[The Page Table Stores Virtual-to-Physical Mappings]]"
  - "[[System Calls Transfer Control via Trap and Return-from-Trap]]"
  - "[[User Mode and Kernel Mode Provide Dual Protection Levels]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[TLB Hits Bypass Memory While Misses Consult the Page Table]]"
---

# Hardware-Managed and Software-Managed TLBs Differ in Miss Handling

> [!SUMMARY]
> When a TLB miss occurs, something must look up the translation in the page table and fill the TLB. In hardware-managed TLBs (x86, ARM), the CPU itself walks the page table automatically. In software-managed TLBs (MIPS, SPARC, RISC-V), the CPU raises a trap and the OS fills the TLB. Each approach trades hardware complexity for software flexibility.

## Hardware-Managed TLBs

In architectures like x86, the hardware "knows" the page table format. On a TLB miss:

1. The CPU fetches the page table base address from a special register (e.g., CR3 on x86)
2. The CPU walks the page table structure automatically (handling multi-level tables)
3. The CPU extracts the PFN and protection bits from the PTE
4. The CPU installs the translation in the TLB
5. The CPU retries the faulting instruction

All of this happens without invoking the OS. The page table walk takes tens of cycles, but the OS is not involved—this is pure hardware.

**Advantage**: Lower latency for TLB misses; no trap overhead.

**Disadvantage**: The page table format is fixed by hardware. The OS cannot use custom page table structures or perform custom actions on miss.

## Software-Managed TLBs

In architectures like MIPS, SPARC, and RISC-V, the hardware only checks the TLB—it does not know how to walk the page table. On a TLB miss:

1. The CPU raises a **TLB miss exception** (similar to a [[System Calls Transfer Control via Trap and Return-from-Trap|trap]])
2. The CPU jumps to a dedicated miss handler address
3. The OS handler looks up the translation in any data structure it chooses
4. The OS installs the translation using special privileged instructions
5. The OS returns from the trap, retrying the instruction

## MIPS TLB Miss Handler Example

OSTEP provides this simplified MIPS assembly for a TLB miss handler:

```asm
TLBMissHandler:
    # Get the VPN from the faulting address (BadVAddr register)
    mfc0  %k0, %badvaddr
    srl   %k0, %k0, 22          # Shift right to get VPN (for 4MB pages)
    sll   %k0, %k0, 2           # Multiply by 4 (PTE size)

    # Add page table base to get PTE address
    addu  %k0, %k0, %PTBASE     # Assume PTBASE is page table base

    # Load the PTE
    lw    %k1, 0(%k0)           # k1 = PTE contents

    # Write the translation to the TLB
    mtc0  %k1, %entrylo         # Put PTE in EntryLo register
    tlbwr                       # Write random TLB entry

    # Return from exception
    eret
```

The handler uses kernel registers (`%k0`, `%k1`) that are reserved for trap handlers. The `tlbwr` instruction writes to a randomly selected TLB slot. The entire handler fits in a few instructions—critical because TLB misses are frequent.

## Trade-offs Between Approaches

| Aspect | Hardware-Managed | Software-Managed |
|--------|-----------------|-----------------|
| Miss latency | Lower (no trap) | Higher (trap + handler) |
| Flexibility | Fixed PT format | Any data structure |
| Hardware complexity | Higher | Lower |
| OS complexity | Lower | Higher |

**Software TLBs enable flexibility**: The OS can use hash tables, inverted page tables, or any structure. It can perform custom actions on miss (e.g., counting for profiling). RISC architectures historically favored this to keep hardware simple.

**Hardware TLBs are faster**: Modern x86 processors walk multi-level page tables in hardware, even handling 5-level page tables for large address spaces. The fixed format is a worthwhile trade-off for lower miss latency.

