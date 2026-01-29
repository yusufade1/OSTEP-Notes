---
type: overview
source: "OSTEP Ch. 7-10: CPU Scheduling"
tags:
  - virtualization
  - scheduling
related:
  - "[[Virtualization MOC]]"
  - "[[Concurrency Bugs - Chapter Overview]]"
  - "[[MLFQ Basic Rules - Priority Queues with Feedback]]"
  - "[[Lottery Scheduling Uses Tickets to Achieve Proportional Share]]"
  - "[[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges]]"
prerequisites: []
---

# Scheduling - Chapter Overview

> [!SUMMARY]
> These chapters explore CPU scheduling **policies** — the decision of *which* process to run next. Starting from basic metrics and algorithms (FIFO, SJF, RR), we progress to sophisticated modern schedulers like MLFQ, proportional share approaches (Lottery/Stride), and the unique challenges of multiprocessor environments.


## Key Concepts

- **[[Turnaround Time and Response Time Measure Scheduling Quality]]** — Fundamental metrics for evaluating performance: turnaround (completion time) and response (time to first run).
- **[[MLFQ Basic Rules - Priority Queues with Feedback]]** — The Multi-Level Feedback Queue scheduler balances turnaround and response time without prior knowledge of job lengths.
- **[[Lottery Scheduling Uses Tickets to Achieve Proportional Share]]** — Randomized scheduling that allocates CPU shares proportional to the number of tickets held by each process.
- **[[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges]]** — The complexity of scaling scheduling to multiple cores while maintaining cache locality and avoiding synchronization bottlenecks.

## Scheduling Algorithms

- **[[FIFO Scheduling is Simple but Suffers from Convoy Effect]]**
- **[[Shortest Job First Minimizes Average Turnaround Time]]**
- **[[Round Robin Trades Turnaround Time for Response Time]]**
- **[[Stride Scheduling Provides Deterministic Proportional Share]]**
- **[[Single-Queue vs Multi-Queue Approaches Balance Simplicity and Scalability]]**

## Chapter Questions

1. How does MLFQ learn the behavior of a job over time?
2. What are the advantages of randomized (lottery) vs. deterministic (stride) scheduling?
3. Why is cache affinity important in multiprocessor scheduling?
4. How do you prevent users from "gaming" an MLFQ scheduler?