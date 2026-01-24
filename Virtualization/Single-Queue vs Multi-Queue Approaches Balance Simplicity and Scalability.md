---
type: atomic
source: OSTEP Ch. 10
tags:
  - virtualization
  - scheduling
  - multiprocessor
related:
  - "[[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges]]"
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges]]"
---

# Single-Queue vs Multi-Queue Approaches Balance Simplicity and Scalability

> [!SUMMARY]
> Multiprocessor schedulers use either a **Single-Queue (SQMS)** or **Multi-Queue (MQMS)** design. SQMS places all jobs in one shared queue, offering simplicity and automatic load balancing but suffering from lock contention and poor cache affinity. MQMS gives each CPU its own queue, achieving better scalability and natural affinity but requiring explicit **work stealing** (migration) to handle load imbalance. Most production systems use MQMS with periodic migration.

## Single-Queue Multiprocessor Scheduling (SQMS)

The simplest extension of uniprocessor scheduling: maintain one global ready queue, protect it with a single lock, and have each CPU grab the next job when it becomes idle.

```
Global Queue: [A, B, C, D, E]
              ↓       ↓
           CPU 0    CPU 1
```

**Advantages:**
- Simple to implement — reuse existing single-CPU scheduler logic
- Inherently load-balanced — no CPU starves while others have work
- Any existing policy (FIFO, SJF, [[Round Robin Trades Turnaround Time for Response Time|RR]]) works unchanged

**Problems:**
- **Lock contention**: Every CPU must acquire the queue lock before selecting a job. With N CPUs, this serializes scheduling decisions
- **Cache affinity loss**: Jobs bounce between CPUs arbitrarily, paying cache warm-up costs each time
- **Scalability ceiling**: Lock contention grows with CPU count, limiting throughput

Adding affinity to SQMS (preferring the last CPU) partially addresses locality but complicates the implementation and loses some load-balancing benefit.

## Multi-Queue Multiprocessor Scheduling (MQMS)

Each CPU gets its own ready queue with its own scheduling policy. Jobs are assigned to a queue (typically at creation time) and stay on that CPU unless explicitly migrated, preserving [[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges|cache affinity]]:

```
CPU 0 Queue: [A, C]     CPU 1 Queue: [B, D]
     ↓                        ↓
  CPU 0                    CPU 1
```

**Advantages:**
- **No lock contention**: Each CPU accesses only its own queue; no shared lock needed
- **Natural cache affinity**: Jobs stay on the same CPU across time slices
- **Scalability**: Adding CPUs adds queues with no shared bottleneck

**Problem — Load Imbalance:**

If CPU 0's jobs finish while CPU 1 still has work, CPU 0 sits idle:

```
Before: CPU 0: [A]    CPU 1: [B, C, D]
After:  CPU 0: []     CPU 1: [B, C, D]    ← CPU 0 idle!
```

## Work Stealing (Migration)

MQMS solves imbalance through **work stealing**: an idle (or under-loaded) CPU periodically checks other CPUs' queues and migrates a job to its own queue.

The migration policy involves a trade-off:
- **Frequent checks**: Quick rebalancing but overhead from queue inspection and cache affinity loss on migrated jobs
- **Infrequent checks**: Less overhead but longer periods of imbalance

A common approach uses a threshold: migrate only when the imbalance exceeds some ratio (e.g., one queue has ≥2 more jobs than another).

## Linux Scheduling: CFS and Multi-Queue

Linux's Completely Fair Scheduler (CFS) uses per-CPU run queues with periodic load balancing. Each CPU maintains a red-black tree ordered by virtual runtime. A balancing thread periodically migrates tasks from busy to idle CPUs, respecting NUMA topology to minimize affinity loss.

## Choosing Between SQMS and MQMS

| Property | SQMS | MQMS |
|----------|------|------|
| Lock contention | High (shared lock) | None (per-CPU) |
| Cache affinity | Poor (jobs move freely) | Good (jobs stay put) |
| Load balance | Automatic | Requires migration |
| Complexity | Low | Moderate (migration logic) |
| Scalability | Poor beyond ~8 CPUs | Scales to many CPUs |

For systems with few CPUs, SQMS suffices. For modern multicore machines (dozens to hundreds of cores), MQMS with work stealing is the dominant approach.
