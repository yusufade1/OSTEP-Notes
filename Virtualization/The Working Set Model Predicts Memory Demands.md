---
type: atomic
source: OSTEP Ch. 22
tags:
  - virtualization
  - memory
  - paging
  - theory
related:
  - "[[Thrashing Occurs When Working Set Exceeds Physical Memory]]"
  - "[[Page Faults Trigger the Swap Mechanism]]"
  - "[[LRU Approximates Optimal by Evicting Least Recently Used Pages]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[LRU Approximates Optimal by Evicting Least Recently Used Pages]]"
  - "[[Thrashing Occurs When Working Set Exceeds Physical Memory]]"
---

# The Working Set Model Predicts Memory Demands

> [!SUMMARY]
> The working set of a process is the set of pages it has referenced within a recent time window. Peter Denning's working set model (1968) observes that if a process's working set fits in memory, it runs efficiently with few faults. If it doesn't fit, thrashing ensues. This model enables memory allocation policies that prevent thrashing by ensuring each process gets at least its working set.

## Definition: Working Set

The working set W(t, Δ) at time t with window Δ is the set of pages referenced in the interval [t-Δ, t]:

```
W(t, Δ) = { pages referenced in time interval [t-Δ, t] }
|W(t, Δ)| = working set size (WSS)
```

The window Δ captures "recent" behavior. Too small a window misses pages that are used but not in the immediate past. Too large includes pages no longer relevant.

## Why Working Sets Matter

Programs exhibit **phase behavior**: they work on different data at different times. During each phase, only certain pages are active:

```
Phase 1: Working on module A → WSS = pages of A
Phase 2: Working on module B → WSS = pages of B
Phase 3: Computationally intensive → WSS = small set
```

If physical memory ≥ WSS for current phase, the process runs smoothly. If physical memory < WSS, every access to an out-of-memory page causes a fault.

## Working Set vs. Resident Set

- **Working set**: Pages the process *needs* (theoretical demand)
- **Resident set**: Pages the process *has* in memory (actual allocation)

Good memory management keeps resident set ≥ working set. When insufficient, fault rate spikes.

## Estimating Working Set Size

The OS can approximate WSS by tracking page access patterns using the [[Page Table Entries Contain PFN and Control Bits|reference bit]]:

1. **Reference bit sampling**: Periodically scan reference bits, count how many are set, clear them
2. **Page fault frequency (PFF)**: High fault rate suggests insufficient memory
3. **Timer-based aging**: Track recency of page accesses over time

None of these give exact WSS, but they indicate whether a process has enough memory.

## Working Set Policy for Thrashing Prevention

Denning proposed a **working set policy**:

1. Monitor each process's working set size
2. Only run processes whose combined WSS fits in RAM:
   ```
   Σ WSS_i ≤ physical_memory
   ```
3. Suspend processes if total exceeds memory

This prevents [[Thrashing Occurs When Working Set Exceeds Physical Memory|thrashing]] by admission control rather than reactive measures.

## The Locality Principle

The working set model is grounded in the **principle of locality**:

- **Temporal locality**: Recently accessed pages likely to be accessed again
- **Spatial locality**: Pages near recently accessed pages likely to be accessed

These properties arise from program structure: loops reuse code, functions access local variables, data structures are traversed sequentially.

## Phase Transitions

Working sets change during program execution. Phase transitions cause temporary spikes in fault rate as new pages are loaded:

```
|WSS|
  ^
  |    ____         _____
  |   /    \       /     \
  |  /      \_____/       \____
  +---------------------------------> time
      Phase 1    Phase 2    Phase 3
```

A well-tuned system tolerates these transitions but maintains enough memory to avoid sustained thrashing.

## Practical Impact

The working set model influenced:
- **Page replacement design**: Approximate LRU preserves working sets
- **Memory allocation**: Give processes enough RAM for their WSS
- **Load balancing**: Don't overcommit memory across processes
- **Prefetching**: Predict and preload working set pages

Understanding working sets remains essential for diagnosing memory performance issues.
