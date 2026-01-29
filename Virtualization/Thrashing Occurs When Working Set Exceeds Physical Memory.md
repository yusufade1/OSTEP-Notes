---
type: algorithm
source: "OSTEP Ch. 22: Beyond Physical Memory: Policies"
tags:
  - virtualization
  - memory
  - paging
  - performance
related:
  - "[[The Working Set Model Predicts Memory Demands]]"
  - "[[Page Faults Trigger the Swap Mechanism]]"
  - "[[Swap Space Extends Memory Beyond Physical Limits]]"
  - "[[LRU Approximates Optimal by Evicting Least Recently Used Pages]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Page Faults Trigger the Swap Mechanism]]"
  - "[[LRU Approximates Optimal by Evicting Least Recently Used Pages]]"
---

# Thrashing Occurs When Working Set Exceeds Physical Memory

> [!SUMMARY]
> Thrashing is a pathological state where the system spends more time paging than executing useful work. It occurs when the combined working sets of running processes exceed physical memory, causing constant page faults. The system becomes unresponsive as the disk becomes the bottleneck, with CPU utilization dropping despite high demand.

## The Thrashing Death Spiral

When memory is overcommitted:

1. Process A faults, evicts page from Process B
2. Process B runs, faults, evicts page from Process A
3. Process A runs, faults, evicts page from Process B
4. Repeat indefinitely...

Each process immediately needs the pages it just lost. The disk becomes saturated with page I/O while the CPU sits idle waiting.

```
Normal operation:          Thrashing:
CPU: ████████░░            CPU: ░░░░░░░░░░  (idle, waiting)
Disk: ░░░░░░░░░░           Disk: ██████████  (saturated)
```

## Symptoms of Thrashing

- **High page fault rate**: Orders of magnitude above normal
- **Low CPU utilization**: Despite runnable processes
- **High disk I/O**: Near 100% disk busy time on swap
- **System unresponsiveness**: Even simple operations stall
- **Memory pressure indicators**: All pages have high reference bits

## Why It Happens: Overcommitment

The fundamental cause is running more processes than memory can support. Each process has a [[The Working Set Model Predicts Memory Demands|working set]]—the pages it actively needs. If:

```
Σ(working_set_size) > physical_memory
```

Then thrashing is inevitable. No page replacement algorithm can help—there simply isn't enough RAM.

## The Positive Feedback Loop

Thrashing can self-amplify:

1. System seems slow, so user launches more applications
2. More applications = larger total working set
3. More thrashing = system even slower
4. User tries to kill apps, but even task manager is slow to respond

## Detection and Prevention

**Admission control**: Limit the number of concurrent processes. If adding a process would cause thrashing, block it until memory frees up.

**Suspend and swap-out**: Temporarily swap out entire processes (all their pages) to give remaining processes enough memory.

**Working set monitoring**: Track page fault rates. If faults spike while CPU utilization drops, reduce multiprogramming degree.

```
if (page_fault_rate > threshold && cpu_utilization < threshold):
    suspend_lowest_priority_process()
```

**OOM killer**: Linux's out-of-memory killer terminates processes when memory is critically low, preventing complete system lockup.

## Historical Context: Early Paging Systems

Thrashing was first identified in early multiprogrammed systems with limited RAM. Denning's [[The Working Set Model Predicts Memory Demands|working set model]] (1968) provided the theoretical framework for understanding and preventing it.

## Thrashing vs. Normal Paging

Some page faults are normal and acceptable:
- **Cold misses**: First access to each page
- **Capacity misses**: Occasionally exceeding memory briefly

Thrashing is distinguished by:
- **Constant, sustained faults**: No progress between faults
- **Circular eviction**: Pages evicted are immediately needed again

The difference is whether the working set *fits* in memory (occasional misses) or *doesn't fit* (thrashing).

## User-Visible Effects

Users experience thrashing as:
- Applications "freezing" for seconds at a time
- Disk activity LED constantly on
- Simple operations (typing, clicking) have huge latency
- System appears to make no forward progress

The solution is often to close applications or add RAM—no software tuning can fix insufficient physical memory.
