---
type: algorithm
source: "OSTEP Ch. 9: Scheduling: Proportional Share"
tags:
  - virtualization
  - scheduling
  - proportional-share
related:
  - "[[Lottery Scheduling Uses Tickets to Achieve Proportional Share]]"
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[MLFQ Basic Rules - Priority Queues with Feedback]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Lottery Scheduling Uses Tickets to Achieve Proportional Share]]"
---

# Stride Scheduling Provides Deterministic Proportional Share

> [!SUMMARY]
> Stride scheduling is a deterministic alternative to [[Lottery Scheduling Uses Tickets to Achieve Proportional Share|lottery scheduling]] that guarantees exact proportional CPU allocation at every scheduling point. Each process has a **stride** inversely proportional to its ticket count and a **pass counter** that accumulates strides. The scheduler always picks the process with the lowest pass value, ensuring mathematically precise fairness without the variance of random selection.

## From Random to Deterministic

Lottery scheduling achieves proportional share probabilistically — the actual allocation only converges to the desired ratio over many draws. Stride scheduling eliminates this variance by computing the exact interleaving deterministically. Unlike [[Turnaround Time and Response Time Measure Scheduling Quality|turnaround or response time]] optimizers that rank jobs, stride scheduling explicitly enforces proportional CPU shares. The trade-off is slightly more state (a pass counter per process) and the need to handle new process arrivals.

## Mechanism: Stride and Pass

Each process gets:
- **Tickets**: the share weight (same as lottery)
- **Stride**: a large constant divided by tickets (stride = K / tickets)
- **Pass**: a running counter, initially 0

The scheduler always picks the process with the lowest pass value, runs it for one time slice, then increments its pass by its stride:

```c
// K = large constant, e.g., 10000
// stride[i] = K / tickets[i]
current = process with min(pass)
schedule(current)
current->pass += current->stride
```

## Worked Example

Three processes: A (100 tickets), B (50 tickets), C (250 tickets). Using K = 10000:
- Stride(A) = 10000/100 = 100
- Stride(B) = 10000/50 = 200
- Stride(C) = 10000/250 = 40

```
Step | Pass(A) | Pass(B) | Pass(C) | Run
  1  |    0    |    0    |    0    |  A  (tie: pick any)
  2  |  100    |    0    |    0    |  B  (tie: pick B)
  3  |  100    |  200    |    0    |  C
  4  |  100    |  200    |   40    |  C
  5  |  100    |  200    |   80    |  C
  6  |  100    |  200    |  120    |  A
  7  |  200    |  200    |  120    |  C
  8  |  200    |  200    |  160    |  C
```

Process C (highest ticket count) runs most frequently, exactly matching its 250/400 = 62.5% share. Unlike lottery scheduling, this ratio holds at every step — there is no period of convergence.

## The New Process Problem

When a new process arrives, what should its initial pass value be? Setting it to 0 gives the newcomer an unfair burst of CPU time (it will run repeatedly until its pass catches up). Setting it to the current global minimum pass is more fair but still imperfect. This state initialization problem is lottery scheduling's primary advantage: a new process with tickets naturally gets its fair share immediately without any pass counter management.

## Comparison with Lottery Scheduling

| Property | Lottery | Stride |
|----------|---------|--------|
| Fairness per quantum | Probabilistic | Deterministic |
| Convergence | Over time | Immediate |
| New process handling | Simple (add tickets) | Requires pass init |
| Implementation | Random + traverse | Min pass + increment |
| Global state | Just ticket total | Pass counter per process |

## Why Lottery Still Matters

Despite stride's superior short-term fairness, lottery scheduling remains attractive for its simplicity and statelessness. Adding a process to lottery requires only updating the total ticket count. Stride requires careful initialization of the pass counter. In practice, the difference matters most for short-lived processes where lottery's variance has not yet converged.
