---
type: algorithm
source: "OSTEP Ch. 8: Scheduling: The Multi-Level Feedback Queue"
tags:
  - virtualization
  - scheduling
  - algorithms
related:
  - "[[MLFQ Basic Rules - Priority Queues with Feedback]]"
  - "[[MLFQ Tuning Balances Queue Count and Time Slice Length]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[MLFQ Basic Rules - Priority Queues with Feedback]]"
---

# MLFQ Prevents Gaming with Priority Boost and Accounting

> [!SUMMARY]
> The basic MLFQ rules suffer from **starvation** (CPU-bound jobs never run when interactive jobs dominate) and **gaming** (jobs trick the scheduler by issuing I/O just before their time slice expires). Two refinements fix these problems: **priority boost** periodically moves all jobs to the top queue, preventing starvation and accommodating phase changes; **CPU accounting** tracks total allotted time per queue rather than per slice, preventing gaming by demoting jobs based on cumulative CPU usage.

## The Starvation Problem

Under the basic rules, if enough interactive jobs continuously enter the system, CPU-bound jobs in lower queues may **never** receive CPU time. This violates fairness guarantees and can leave long-running computations indefinitely delayed.

Additionally, a job may **change behavior** over time — a CPU-bound process might become interactive. Under basic rules, it remains stuck at low priority with no mechanism to recover.

## Solution: Priority Boost (Rule 5)

**Rule 5:** After some time period S, move all jobs to the topmost queue.

This single rule solves both problems simultaneously:

- **Prevents starvation:** CPU-bound jobs are guaranteed to run at high priority at least once every S seconds
- **Handles phase changes:** A formerly CPU-bound job that becomes interactive gets a fresh start at high priority

### Worked Example: Priority Boost

Three queues (Q2=top, Q0=bottom). Long-running job B is stuck in Q0. Boost period S = 50ms:

```
Time:   0    10   20   30   40   50   60   70
Q2:     A    A    A    A    A    A,B  A    A
Q0:     B    B    B    B    B              B
                                     ↑ boost
```

At t=50, B is boosted to Q2. It gets one time slice before being demoted again — but it makes progress every S period.

## The Gaming Problem

A clever program can exploit Rule 4b: issue an I/O operation at 99% of the time slice to avoid demotion. It stays at the highest priority while consuming nearly its full allotment — monopolizing the CPU unfairly.

## Solution: CPU Accounting (Revised Rule 4)

**Revised Rule 4:** Once a job uses up its total time allotment at a given level (regardless of how many times it gives up the CPU), its priority is reduced.

Instead of resetting the timer on each I/O, the scheduler tracks **cumulative** CPU time used at each priority level. A gaming job that uses 1ms across 10 slices still accumulates 10ms total — once that exceeds the allotment, it is demoted.

### Worked Example: Accounting Defeats Gaming

Job G issues I/O at 9ms of a 10ms time slice. Without accounting, G stays in Q2 forever. With accounting:

```
Slice 1: G runs 9ms, I/O → cumulative: 9ms (allotment: 10ms)
Slice 2: G runs 1ms → cumulative: 10ms → DEMOTED to Q1
```

The gaming job is caught after just slightly more than one allotment period.

## Combined Effect

With both refinements, MLFQ achieves its design goals: [[Turnaround Time and Response Time Measure Scheduling Quality|response time]] for interactive jobs, reasonable [[Turnaround Time and Response Time Measure Scheduling Quality|turnaround time]] for CPU-bound jobs, starvation freedom, and resistance to gaming. The remaining challenge is [[MLFQ Tuning Balances Queue Count and Time Slice Length|tuning the parameters]] — how many queues, what time allotments, and how often to boost.
