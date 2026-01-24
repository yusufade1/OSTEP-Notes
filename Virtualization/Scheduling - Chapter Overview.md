---
type: overview
source: OSTEP Ch. 7
tags:
  - virtualization
  - scheduling
related:
  - "[[Virtualization MOC]]"
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[FIFO Scheduling is Simple but Suffers from Convoy Effect]]"
  - "[[Shortest Job First Minimizes Average Turnaround Time]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
---

# Scheduling - Chapter Overview

This chapter introduces CPU scheduling **policies** — the decision of *which* process to run next, given that the [[Context Switch Saves and Restores Process State|context switch mechanism]] already provides the ability to switch. The chapter defines quantitative metrics for evaluating schedulers, then presents progressively more sophisticated policies.

## Key Concepts

- **[[Turnaround Time and Response Time Measure Scheduling Quality]]** — Two fundamental metrics for evaluating scheduling policies: turnaround time (arrival to completion) for batch workloads, and response time (arrival to first run) for interactive workloads.
- **[[FIFO Scheduling is Simple but Suffers from Convoy Effect]]** — The simplest policy runs jobs in arrival order, but a single long job can inflate the wait time for all subsequent short jobs.
- **[[Shortest Job First Minimizes Average Turnaround Time]]** — Running the shortest job first is provably optimal for turnaround time; the preemptive variant (STCF) handles staggered arrivals by preempting when a shorter job appears.
- **[[Round Robin Trades Turnaround Time for Response Time]]** — Time-slicing the CPU among all ready jobs provides bounded response time at the cost of worse turnaround time.

## Chapter Questions

1. How do you measure whether a scheduler is "good"?
2. Why is there no single "best" scheduling policy for all workloads?
3. What is the fundamental tension between turnaround time and response time?
4. How does preemption change the capabilities of a scheduler?
