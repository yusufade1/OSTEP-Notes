---
type: algorithm
source: "OSTEP Ch. 7: Scheduling: Introduction"
tags:
  - virtualization
  - scheduling
  - algorithms
related:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Shortest Job First Minimizes Average Turnaround Time]]"
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
---

# FIFO Scheduling is Simple but Suffers from Convoy Effect

> [!SUMMARY]
> First-In, First-Out (FIFO) scheduling — also called First Come, First Served (FCFS) — runs jobs in arrival order until completion. It is trivial to implement and works well when all jobs are similar length. However, when a long job arrives before short ones, all subsequent jobs must wait, a pathology called the **convoy effect** that dramatically inflates average turnaround time.

## How FIFO Works

FIFO maintains a simple queue. Jobs are added to the tail upon arrival and the scheduler always picks the job at the head. Once a job starts running, it runs to completion (non-preemptive). No job-length knowledge is required — the scheduler only needs arrival order.

## Worked Example: Equal Job Lengths

Consider three jobs A, B, C arriving at time 0, each running for 10 seconds:

```
Time:  0----10----20----30
Job A: |==========|
Job B:            |==========|
Job C:                       |==========|
```

- Turnaround: A=10, B=20, C=30
- Average turnaround: (10+20+30)/3 = **20 seconds**

With equal job lengths, FIFO performs reasonably — the average is determined by the inherent total work.

## Worked Example: Convoy Effect

Now relax the "equal length" assumption. Job A runs for 100 seconds, B and C run for 10 each, all arrive at time 0:

```
Time:  0-----------100--110--120
Job A: |============|
Job B:              |====|
Job C:                   |====|
```

- Turnaround: A=100, B=110, C=120
- Average turnaround: (100+110+120)/3 = **110 seconds**

Jobs B and C wait 100 seconds for A to finish despite needing only 10 seconds each. This is the **convoy effect** — short jobs queue behind a long one, like cars stuck behind a slow truck on a single-lane road.

## Why the Convoy Effect Matters

The convoy effect illustrates a fundamental limitation: without knowledge of job lengths, FIFO cannot prioritize short jobs. If the scheduler had known B and C were short, running them first would yield average turnaround of (10+20+120)/3 = 50 seconds — a dramatic improvement.

This motivates [[Shortest Job First Minimizes Average Turnaround Time|Shortest Job First (SJF)]], which explicitly uses job-length knowledge to order execution.

## Implementation

FIFO requires only a simple FIFO queue — no per-job metadata beyond arrival order. Context switches occur only at job completion, minimizing switching overhead. Its simplicity makes it a useful baseline but its susceptibility to the convoy effect makes it unsuitable as a general-purpose scheduler.

## When FIFO Works Well

FIFO is acceptable when:
- All jobs have similar execution times
- Job ordering naturally correlates with priority
- The overhead of more complex scheduling is not justified

In practice, FIFO appears as a component within more sophisticated schedulers — for example, within a single priority queue of a [[Round Robin Trades Turnaround Time for Response Time|Round Robin]] or MLFQ system.
