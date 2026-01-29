---
type: algorithm
source: "OSTEP Ch. 7: Scheduling: Introduction"
tags:
  - virtualization
  - scheduling
  - algorithms
related:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[FIFO Scheduling is Simple but Suffers from Convoy Effect]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[FIFO Scheduling is Simple but Suffers from Convoy Effect]]"
---

# Shortest Job First Minimizes Average Turnaround Time

> [!SUMMARY]
> Shortest Job First (SJF) schedules the job with the smallest remaining run time. When all jobs arrive simultaneously, SJF is provably optimal for average turnaround time. However, non-preemptive SJF still suffers the convoy effect when short jobs arrive after a long one is already running. The preemptive variant — Shortest Time-to-Completion First (STCF) — solves this by preempting the current job when a shorter one arrives, achieving optimality even with staggered arrivals.

## SJF: Non-Preemptive

SJF examines all jobs in the ready queue and runs the one with the shortest total execution time. Once a job begins, it runs to completion.

### Worked Example: Simultaneous Arrivals

Jobs A (100s), B (10s), C (10s) all arrive at time 0:

```
Time:  0--10--20-----------120
Job B: |====|
Job C:      |====|
Job A:           |===========|
```

- Turnaround: B=10, C=20, A=120
- Average turnaround: (10+20+120)/3 = **50 seconds**

Compare to FIFO's 110 seconds — SJF achieves a 55% reduction by running short jobs first.

### Worked Example: Staggered Arrivals (SJF Breaks Down)

Job A arrives at time 0 (100s), B and C arrive at time 10 (10s each):

```
Time:  0-----------100--110--120
Job A: |============|
Job B:              |====|     (arrived t=10, waited 90s)
Job C:                   |====|
```

- Turnaround: A=100, B=100, C=110
- Average turnaround: (100+100+110)/3 = **103.3 seconds**

Since A was already running when B and C arrived, non-preemptive SJF cannot interrupt it. The [[FIFO Scheduling is Simple but Suffers from Convoy Effect|convoy effect]] reappears.

## STCF: Preemptive SJF

Shortest Time-to-Completion First (STCF), also called Preemptive Shortest Job First (PSJF), solves staggered arrivals by allowing preemption. When a new job arrives with less remaining time than the current job, the scheduler preempts the running job.

### Worked Example: STCF with Staggered Arrivals

Same scenario — A arrives at 0 (100s), B and C arrive at 10 (10s each):

```
Time:  0--10--20--30-----------120
Job A: |===|              |======|
Job B:      |====|
Job C:           |====|
Job A (cont):         |=========|
```

At time 10, B arrives with 10s remaining vs A's 90s — STCF preempts A.

- Turnaround: B=20-10=10, C=30-10=20, A=120-0=120
- Average turnaround: (10+20+120)/3 = **50 seconds**

STCF achieves optimal average turnaround time even with staggered arrivals.

## Optimality Proof Intuition

SJF/STCF is optimal for average turnaround because running a short job before a long one reduces the short job's wait by a small amount (the short job's length) while only increasing the long job's wait by the same small amount. Since we are averaging, moving short jobs earlier always improves or maintains the average.

## The Response Time Problem

Despite optimal turnaround, SJF/STCF can have terrible response time. If many short jobs keep arriving, a long job may wait indefinitely (starvation). More fundamentally, running jobs to completion means interactive jobs get no CPU time until their turn. This motivates [[Round Robin Trades Turnaround Time for Response Time|Round Robin]], which sacrifices turnaround optimality for bounded response time.

## Practical Limitation

SJF/STCF requires knowing job lengths in advance — rarely possible in practice. Real systems estimate run times using historical data or user hints. This impracticality motivates schedulers like MLFQ that *learn* job behavior through feedback rather than requiring advance knowledge.
