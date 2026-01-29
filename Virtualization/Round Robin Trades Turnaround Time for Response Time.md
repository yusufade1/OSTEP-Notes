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
  - "[[Timer Interrupts Enable Preemptive Multitasking]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Context Switch Saves and Restores Process State]]"
---

# Round Robin Trades Turnaround Time for Response Time

> [!SUMMARY]
> Round Robin (RR) scheduling runs each job for a fixed **time slice** (or scheduling quantum), then preempts it and moves to the next job in the ready queue. This guarantees that every job gets CPU time within a bounded period, providing excellent response time for interactive workloads. However, Round Robin has poor turnaround time because it stretches all jobs equally rather than completing short ones first. The time slice length represents a trade-off: shorter slices improve response time but increase context switch overhead.

## How Round Robin Works

The scheduler maintains a circular queue. Each job runs for at most one time slice before being preempted and placed at the tail of the queue. The [[Timer Interrupts Enable Preemptive Multitasking|timer interrupt]] enforces the time slice boundary, triggering a [[Context Switch Saves and Restores Process State|context switch]] when the quantum expires.

## Worked Example: RR with Time Slice = 1s

Jobs A (5s), B (5s), C (5s) all arrive at time 0:

```
Time: 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
      A  B  C  A  B  C  A  B  C  A  B  C  A  B  C
```

- First run: A=0, B=1, C=2
- Response time: A=0, B=1, C=2 → average = **1 second**
- Completion: A=13, B=14, C=15
- Turnaround: A=13, B=14, C=15 → average = **14 seconds**

Compare to SJF (which equals FIFO here since all are equal length):
- SJF response: A=0, B=5, C=10 → average = **5 seconds**
- SJF turnaround: A=5, B=10, C=15 → average = **10 seconds**

RR achieves far better response time (1 vs 5) but worse turnaround (14 vs 10).

## The Time Slice Trade-Off

The time slice (quantum) length is a critical parameter:

- **Shorter slice** → Better response time, more context switches (overhead)
- **Longer slice** → Fewer switches, approaches FIFO behavior

If the time slice is too short, the system spends more time switching than executing useful work. If too long, response time degrades. A typical quantum is 1-10 milliseconds — short enough for good interactivity, long enough to amortize the ~10 microsecond context switch cost.

## Why RR Has Poor Turnaround Time

RR stretches every job's completion time to near the total schedule length. In the example above, each 5-second job takes 13-15 seconds to complete. This is because RR is fundamentally **fair** — it distributes CPU time equally rather than prioritizing completion of any single job.

In fact, RR is one of the **worst** policies for turnaround time. Even FIFO may produce better turnaround because it at least completes the first job quickly.

## Incorporating I/O

Real workloads mix CPU bursts with I/O. When a job blocks on I/O, the scheduler picks another job. This overlap means even SJF-like policies partially address response time for I/O-bound interactive workloads.

## RR as Building Block

Despite poor turnaround time, RR is widely used as a component within multi-level schedulers. A [[MLFQ Basic Rules - Priority Queues with Feedback|Multi-Level Feedback Queue]] uses Round Robin within each priority level, combining RR's fairness with priority-based turnaround optimization.
