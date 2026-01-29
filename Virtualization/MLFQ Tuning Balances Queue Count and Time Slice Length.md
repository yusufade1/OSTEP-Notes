---
type: algorithm
source: "OSTEP Ch. 8: Scheduling: The Multi-Level Feedback Queue"
tags:
  - virtualization
  - scheduling
  - algorithms
related:
  - "[[MLFQ Basic Rules - Priority Queues with Feedback]]"
  - "[[MLFQ Prevents Gaming with Priority Boost and Accounting]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[MLFQ Prevents Gaming with Priority Boost and Accounting]]"
---

# MLFQ Tuning Balances Queue Count and Time Slice Length

> [!SUMMARY]
> A practical MLFQ requires careful tuning of its parameters: the **number of queues**, the **time slice per queue** (typically increasing at lower priorities), and the **priority boost period** S. These are sometimes called "voo-doo constants" because no single configuration works optimally for all workloads. Real systems like Solaris provide administrator-configurable tables, while others like FreeBSD use mathematical decay formulas to dynamically compute priority.

## Key Parameters

An MLFQ implementation must decide:

1. **How many queues?** — More queues provide finer-grained priority distinctions but add complexity
2. **What time slice per queue?** — Higher-priority queues typically have shorter slices for responsiveness; lower-priority queues have longer slices to amortize [[Context Switch Saves and Restores Process State|context switch]] overhead
3. **How often to boost (period S)?** — Too frequent wastes CPU on re-classification; too infrequent leads to starvation

## Variable Time Slices Across Queues

A critical refinement is using **different time slices at different priority levels**:

- High priority (interactive): short slices (e.g., 10ms) → fast [[Turnaround Time and Response Time Measure Scheduling Quality|response time]]
- Low priority (CPU-bound): long slices (e.g., 100ms) → less context switch overhead, better throughput

This matches each priority level to its expected workload character.

### Worked Example: 3-Queue Variable Slice

Queues with slices: Q2=10ms, Q1=20ms, Q0=40ms. Job X uses 50ms total CPU:

```
Queue   Allotment   X's behavior
Q2      10ms        Runs 10ms → uses full allotment → demoted
Q1      20ms        Runs 20ms → uses full allotment → demoted
Q0      40ms        Runs remaining 20ms → completes in Q0
```

Job X descends through queues, receiving progressively larger time slices. If it were interactive (using <10ms per burst), it would remain in Q2 permanently.

## Solaris Time-Sharing Scheduler

Solaris provides a configurable **dispatch table** with 60 priority levels. Administrators can set per-level parameters:

| Priority | Time Slice | Time Quantum Expired → | Return From Sleep → |
|----------|-----------|----------------------|-------------------|
| 59 (top) | 20ms      | priority 49          | priority 59       |
| 30 (mid) | 40ms      | priority 20          | priority 58       |
| 0 (low)  | 200ms     | priority 0           | priority 54       |

The table specifies both demotion targets and sleep-return targets, giving fine control over interactive responsiveness.

## FreeBSD Decay-Usage Formula

Rather than fixed tables, FreeBSD 4.3 uses a **mathematical formula** to compute priority dynamically:

```
priority = base_priority + (recent_cpu_usage / weight)
```

CPU usage decays over time, so jobs that have not recently used the CPU drift back toward higher priority. This approach avoids explicit boost periods — the decay naturally handles starvation prevention and phase changes.

## The "Voo-Doo Constants" Problem

OSTEP calls these parameters "voo-doo constants" because their optimal values depend on the workload mix, which varies across systems and over time. There is no universally correct configuration — tuning MLFQ requires understanding the expected balance of interactive, I/O-bound, and CPU-bound processes on a given system.
