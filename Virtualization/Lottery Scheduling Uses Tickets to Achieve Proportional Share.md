---
type: atomic
source: OSTEP Ch. 9
tags:
  - virtualization
  - scheduling
  - proportional-share
related:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[Stride Scheduling Provides Deterministic Proportional Share]]"
  - "[[MLFQ Basic Rules - Priority Queues with Feedback]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
---

# Lottery Scheduling Uses Tickets to Achieve Proportional Share

> [!SUMMARY]
> Lottery scheduling assigns **tickets** to processes representing their share of CPU time, then holds a random drawing each time slice to select which process runs. A process holding 75 out of 100 total tickets gets approximately 75% of the CPU over time. Randomness makes the mechanism simple and avoids worst-case behaviors, though it only converges to the desired proportions over many scheduling decisions.

## The Proportional Share Concept

Unlike [[Turnaround Time and Response Time Measure Scheduling Quality|turnaround or response time]] optimizers, proportional-share (or fair-share) schedulers guarantee each process receives a specified fraction of CPU time. If process A should get twice as much CPU as B, the scheduler ensures this ratio holds over time regardless of the workload mix.

## Mechanism: Ticket Drawing

Each process holds some number of tickets. The scheduler picks a random number between 0 and the total ticket count, then traverses the process list accumulating tickets until the winning ticket is found:

```c
int counter = 0;
int winner = random() % total_tickets;
node_t *current = head;
while (current) {
    counter += current->tickets;
    if (counter > winner)
        break;  // current is the winner
    current = current->next;
}
// schedule current process
```

## Worked Example: Ticket Allocation

Two jobs: A holds 75 tickets, B holds 25 tickets (100 total).

```
Drawing:  63   14   82   7   45   91   28   55   73   36
Winner:    A    A    B   A    A    B    A    A    A    A
```

Over 10 draws: A wins 8 times (80%), B wins 2 times (20%). The expected ratio is 75:25, but with randomness there is variance. Over thousands of draws, the proportions converge to 75% and 25%.

## Ticket Manipulation Mechanisms

Lottery scheduling supports several ticket operations:

- **Ticket currency**: A user allocates tickets among their own jobs using a local currency, which the system converts to a global value
- **Ticket transfer**: A process temporarily gives tickets to another (useful for client-server interactions where the client wants the server to run quickly)
- **Ticket inflation**: A process raises or lowers its own ticket count (only trusted among cooperating processes)

## Why Randomness Works

Random selection has three advantages. First, it avoids worst-case behaviors — no pathological ordering can persistently starve a process. Second, the implementation is lightweight: just a random number and a list traversal. Third, it requires no global state beyond the ticket counts, making it fast and simple.

## Fairness Over Time

The **unfairness metric** U = (time first job completes) / (time second job completes) measures convergence. For two jobs with equal tickets, U = 1.0 means perfect fairness. Short job lengths produce high variance (U far from 1.0), while longer runs converge. For jobs of length 1000 time units, U ≈ 1.0 across trials.

## Limitations

Lottery scheduling provides no hard guarantees over short time windows. A process with 99% of tickets could still lose several consecutive drawings. For workloads requiring deterministic fairness, [[Stride Scheduling Provides Deterministic Proportional Share|stride scheduling]] eliminates this randomness.
