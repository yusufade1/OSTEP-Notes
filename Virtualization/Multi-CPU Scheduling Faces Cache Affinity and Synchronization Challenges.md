---
type: atomic
source: OSTEP Ch. 10
tags:
  - virtualization
  - scheduling
  - multiprocessor
related:
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Single-Queue vs Multi-Queue Approaches Balance Simplicity and Scalability]]"
  - "[[Round Robin Trades Turnaround Time for Response Time]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Turnaround Time and Response Time Measure Scheduling Quality]]"
  - "[[Context Switch Saves and Restores Process State]]"
---

# Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges

> [!SUMMARY]
> Scheduling on multiprocessor systems introduces challenges absent from single-CPU designs. **Cache affinity** means a process benefits from running on the same CPU where its data is already cached — migrating it incurs cold-start cache penalties. **Cache coherence** requires hardware protocols (like bus snooping) to keep per-CPU caches consistent when multiple processors access shared data. **Synchronization overhead** from locking shared scheduler data structures can become a bottleneck as CPU count grows.

## Why Multiprocessor Scheduling Differs

On a single CPU, scheduling is straightforward: pick the next job from one ready queue. With multiple CPUs, the scheduler must decide both *which* job runs next and *on which CPU*. This introduces new concerns about data locality, shared state protection, and load imbalance that single-CPU policies like [[Round Robin Trades Turnaround Time for Response Time|Round Robin]] or [[MLFQ Basic Rules - Priority Queues with Feedback|MLFQ]] never face.

## Cache Affinity

When a process runs on a CPU, its working set gets loaded into that CPU's cache hierarchy. If the scheduler later moves the process to a different CPU, all cached state is cold — the process suffers cache misses until it rebuilds locality on the new processor. **Cache affinity** is the preference for keeping a process on the CPU where it last ran. However, strict affinity can cause load imbalance if some CPUs accumulate more runnable processes.

## Cache Coherence

With per-CPU caches, a single memory location may exist in multiple caches simultaneously. When one CPU writes to a shared variable, other CPUs' cached copies become stale. Hardware **cache coherence protocols** (bus snooping or directory-based) detect writes and invalidate stale copies, ensuring all CPUs see consistent memory. This happens transparently but adds latency to shared-memory access, making lock-based synchronization more expensive on multiprocessors.

## Synchronization and Locking

A shared scheduler queue accessed by all CPUs requires a lock. As CPU count grows, **lock contention** becomes severe — CPUs spin waiting for access to the run queue instead of doing useful work. This contention is why single shared queues (SQMS) scale poorly and why per-CPU queue designs ([[Single-Queue vs Multi-Queue Approaches Balance Simplicity and Scalability|MQMS]]) are preferred.

The overhead includes cache-line bouncing: the lock variable moves between CPU caches on each acquire/release cycle, generating coherence traffic.

## The Load Balancing Problem

Even with per-CPU queues, workload imbalance arises when processes finish or block unevenly. A migration policy must periodically move processes from overloaded CPUs to idle ones. This conflicts with cache affinity — every migration pays a cache warm-up cost. The scheduler must balance these tensions: too little migration causes idle CPUs while others are overloaded; too much migration wastes cache locality.

## Context Switch Cost on Multiprocessors

A [[Context Switch Saves and Restores Process State|context switch]] on a multiprocessor has the same register save/restore cost as on a single CPU, plus potential TLB and cache effects. If the new process has never run on this CPU, the entire cache is cold. This amplifies the importance of scheduling decisions on multiprocessor systems.
