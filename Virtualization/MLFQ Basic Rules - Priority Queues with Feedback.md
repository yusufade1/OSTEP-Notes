---
type: algorithm
source: "OSTEP Ch. 8: Scheduling: The Multi-Level Feedback Queue"
tags:
  - virtualization
  - scheduling
  - algorithms
related:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[MLFQ Prevents Gaming with Priority Boost and Accounting]]"
  - "[[MLFQ Tuning Balances Queue Count and Time Slice Length]]"
  - "[[Scheduling - Chapter Overview]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
---

# MLFQ Basic Rules - Priority Queues with Feedback

> [!SUMMARY]
> The Multi-Level Feedback Queue (MLFQ) uses multiple priority queues to optimize **both** turnaround time and response time without requiring advance knowledge of job lengths. It learns job behavior through feedback: jobs that use their entire time slice are demoted (assumed CPU-intensive), while jobs that release the CPU quickly remain at high priority (assumed interactive). This achieves SJF-like turnaround for short jobs while providing RR-like responsiveness for interactive workloads.

## The Five Basic Rules

MLFQ operates on a set of distinct queues, each assigned a priority level:

1. **Rule 1:** If Priority(A) > Priority(B), A runs (B does not)
2. **Rule 2:** If Priority(A) = Priority(B), A and B run in [[Round Robin Trades Turnaround Time for Response Time|Round Robin]]
3. **Rule 3:** When a job enters the system, it is placed at the highest priority (topmost queue)
4. **Rule 4a:** If a job uses up an entire time slice, its priority is reduced (moved down one queue)
5. **Rule 4b:** If a job gives up the CPU before the time slice expires (e.g., for I/O), it stays at the same priority level

## How Feedback Learns Job Behavior

The key insight is that MLFQ uses the **history** of a job's execution to predict its future behavior. A job that repeatedly uses its full time slice is likely a long-running CPU-bound process — it gets demoted, approximating [[Shortest Job First Minimizes Average Turnaround Time|SJF]] by letting shorter jobs run first. A job that frequently yields for I/O is likely interactive — it stays at high priority, receiving quick [[Turnaround Time and Response Time Measure Scheduling Quality|response time]].

## Worked Example: Interactive vs CPU-Bound

Consider 3 queues (Q2=highest, Q0=lowest) with time slice = 10ms. Job A is interactive (uses 1ms then does I/O). Job B is CPU-bound (runs for 50ms total).

```
Time:  0    10   20   30   40   50
Q2:    A,B  A    A    A    A    A
Q1:         B
Q0:              B    B    B    B
```

- t=0: Both start in Q2. A runs 1ms, yields for I/O → stays Q2. B runs 10ms → demoted to Q1
- t=10: A runs 1ms, yields → stays Q2. B runs 10ms in Q1 → demoted to Q0
- t=20+: A continues getting fast response in Q2. B runs only when Q2 is empty

Job A gets sub-millisecond response time while Job B still completes — achieving both goals simultaneously.

## Problems with Basic Rules

These basic rules have two significant problems:

- **Starvation:** If many interactive jobs arrive, CPU-bound jobs in lower queues may never run
- **Gaming:** A malicious job could issue a fake I/O operation just before its time slice expires to stay at high priority

Both problems are addressed by [[MLFQ Prevents Gaming with Priority Boost and Accounting|priority boost and accounting]] refinements.
