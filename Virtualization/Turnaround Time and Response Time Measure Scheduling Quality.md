---
type: algorithm
source: "OSTEP Ch. 7: Scheduling: Introduction"
tags:
  - virtualization
  - scheduling
  - metrics
related:
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[FIFO Scheduling is Simple but Suffers from Convoy Effect]]"
  - "[[Shortest Job First Minimizes Average Turnaround Time]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[Timer Interrupts Enable Preemptive Multitasking]]"
---

# Turnaround Time and Response Time Measure Scheduling Quality

> [!SUMMARY]
> Scheduling policies are evaluated using quantitative metrics. **Turnaround time** measures how long a job takes from arrival to completion, reflecting batch workload performance. **Response time** measures how long until a job first runs, reflecting interactive workload performance. These two metrics are fundamentally in tension — optimizing one often degrades the other, which is why different scheduling policies exist.

## Workload Assumptions

OSTEP introduces scheduling by progressively relaxing simplifying assumptions about the workload:

1. Each job runs for the same amount of time
2. All jobs arrive at the same time
3. Once started, each job runs to completion (non-preemptive)
4. All jobs only use the CPU (no I/O)
5. The run-time of each job is known

As assumptions are relaxed, simple policies break down and more sophisticated ones are needed.

## Turnaround Time

Turnaround time is defined as:

```
T_turnaround = T_completion - T_arrival
```

This metric captures the total time a job spends in the system from submission to finish. It includes time spent waiting in the ready queue plus actual execution time. Lower turnaround time means jobs complete faster, which matters for batch workloads. [[Shortest Job First Minimizes Average Turnaround Time|SJF]] directly optimizes this metric.

## Response Time

Response time is defined as:

```
T_response = T_firstrun - T_arrival
```

This metric captures how quickly the system begins running a job after it arrives. For interactive workloads — a user typing at a terminal, a process handling network requests — response time is critical. A policy with excellent turnaround time might still leave short interactive jobs waiting behind long-running ones. [[Round Robin Trades Turnaround Time for Response Time|Round Robin]] directly optimizes this metric.

## The Fundamental Trade-Off

No single metric captures all aspects of scheduling quality. A policy that runs jobs to completion (good for turnaround) might leave newly arrived jobs waiting (bad for response). Conversely, rapidly switching between jobs (good for response) adds context switch overhead and can increase turnaround time.

This trade-off is why OSTEP presents multiple scheduling policies: **FIFO** and **SJF** optimize turnaround time, while **Round Robin** optimizes response time. Real schedulers like [[MLFQ Basic Rules - Priority Queues with Feedback|MLFQ]] attempt to balance both by adapting to workload behavior.

## Fairness vs. Performance

Beyond turnaround and response time, **fairness** measures whether all jobs receive an equitable share of CPU time. Optimizing strictly for performance metrics can starve some jobs indefinitely. Jain's fairness index provides a quantitative measure, though most OSTEP discussion focuses on the turnaround/response trade-off.
