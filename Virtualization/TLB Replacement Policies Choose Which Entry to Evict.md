---
type: mechanism
source: "OSTEP Ch. 19: Paging: Faster Translations (TLBs)"
tags:
  - virtualization
  - memory
  - paging
  - tlb
  - replacement-policy
related:
  - "[[The TLB Caches Address Translations for Fast Access]]"
  - "[[TLB Hits Bypass Memory While Misses Consult the Page Table]]"
  - "[[Hardware-Managed and Software-Managed TLBs Differ in Miss Handling]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[MLFQ Basic Rules - Priority Queues with Feedback]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The TLB Caches Address Translations for Fast Access]]"
  - "[[TLB Hits Bypass Memory While Misses Consult the Page Table]]"
---

# TLB Replacement Policies Choose Which Entry to Evict

> [!SUMMARY]
> When the TLB is full and a new translation must be inserted, a replacement policy selects which existing entry to evict. Common policies include random replacement (simple, unpredictable), LRU (keeps recently used entries, complex), and pseudo-LRU approximations. For small TLBs, random performs surprisingly well; for larger TLBs, LRU variants provide modest improvement.

## The Replacement Problem

TLBs are small—typically 32 to 1024 entries. When a TLB miss occurs and all entries are occupied, one must be evicted to make room. The replacement policy determines which entry to sacrifice. A good policy evicts entries unlikely to be used soon; a bad policy evicts entries that will be needed immediately (causing another miss).

## Random Replacement

The simplest policy: pick a random entry to evict.

```
on TLB miss:
    victim = random() % TLB_SIZE
    TLB[victim] = new_entry
```

**Advantages**:
- Trivial to implement in hardware (counter or LFSR)
- No tracking overhead
- Avoids pathological worst-case patterns

**Disadvantage**: May evict a frequently used entry by chance.

The MIPS `tlbwr` instruction ("TLB write random") implements exactly this—write to a randomly selected slot. Random is the default for software-managed TLBs because it requires no additional hardware support.

## Least Recently Used (LRU)

LRU evicts the entry that has gone longest without being accessed, on the theory that recent usage predicts future usage.

**Advantage**: Exploits temporal locality—keeps "hot" translations.

**Disadvantage**: True LRU is expensive. With N entries, each access must update ordering information. Hardware LRU for a 64-entry TLB requires tracking 64 relative positions—impractical.

## Pseudo-LRU Approximations

Real systems use approximations that capture LRU's benefits without full ordering:

**Not Recently Used (NRU)**: Each entry has a "reference" bit set on access and periodically cleared. Evict entries with reference=0 first. Simple and effective.

**Clock Algorithm**: Arrange entries in a circular list with a "clock hand." On eviction, scan from the hand, clearing reference bits. Evict the first entry found with reference=0. This approximates LRU with O(1) amortized cost.

For page replacement in main memory (larger scale), these approximations are essential. For small TLBs, the hardware may implement true LRU or simply use random.

## Does Replacement Policy Matter?

For typical workloads, TLB hit rates exceed 99%. The replacement policy affects only the miss path:

| Policy | Miss Rate Impact | Hardware Cost |
|--------|-----------------|---------------|
| Random | Baseline | Minimal |
| LRU | ~5-10% fewer misses | High |
| Pseudo-LRU | Similar to LRU | Moderate |

With hit rates already high, reducing misses by 10% improves overall performance by a fraction of 1%. For this reason, many TLBs use random—the simplicity is worth more than the modest improvement from LRU.

## Wired Entries

Some TLB entries must never be evicted—kernel translations needed for interrupt handling, for instance. These are **wired** or **pinned**: the replacement policy skips them. The MIPS architecture has a "wired" register that specifies how many low-numbered TLB slots are protected from random replacement.

## Interaction with Software-Managed TLBs

In [[Hardware-Managed and Software-Managed TLBs Differ in Miss Handling|software-managed TLBs]], the OS can implement any replacement policy. However, the miss handler must be fast—a complex LRU implementation adds cycles to every miss. Most OS implementations use random or simple clock-based schemes for TLB replacement, reserving sophisticated policies for page replacement (where the stakes are higher—disk access vs. memory access).

