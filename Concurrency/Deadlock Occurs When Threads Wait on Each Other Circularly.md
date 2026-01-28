---
type: atomic
source: OSTEP Ch. 26
tags: [concurrency, bugs, deadlock]
related:
  - "[[The Dining Philosophers Problem Illustrates Deadlock]]"
  - "[[Lock Design Goals - Mutual Exclusion Fairness and Performance]]"
  - "[[Deadlock Prevention Breaks One of the Four Necessary Conditions]]"
prerequisites:
  - "[[Semaphores Define wait and post Operations]]"
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
---

> [!SUMMARY]
> Deadlock is a state where a set of threads are blocked forever, each waiting for a resource held by another in the group. It arises when four specific conditions are met simultaneously: Mutual Exclusion, Hold-and-Wait, No Preemption, and Circular Wait.

**Deadlock** is a severe concurrency bug where the program halts progress entirely because threads are stuck in a cycle of dependency. Unlike race conditions which produce incorrect results, deadlocks stop the program from producing any result at all.

### The Example
A classic deadlock scenario involves two threads and two locks (L1 and L2):

**Thread 1:**
```c
pthread_mutex_lock(L1);
pthread_mutex_lock(L2);
```

**Thread 2:**
```c
pthread_mutex_lock(L2);
pthread_mutex_lock(L1);
```

If Thread 1 grabs L1 and is then interrupted by Thread 2 which grabs L2, neither can proceed. Thread 1 waits for L2 (held by Thread 2), and Thread 2 waits for L1 (held by Thread 1). This is a cycle of waiting.

### The Four Coffman Conditions
For a deadlock to occur, four conditions must hold simultaneously:

1.  **Mutual Exclusion:** Threads claim exclusive control of resources that they require (e.g., a thread grabs a lock).
2.  **Hold-and-Wait:** Threads hold resources allocated to them (e.g., L1) while waiting for additional resources (e.g., L2).
3.  **No Preemption:** Resources cannot be forcibly removed from the threads holding them.
4.  **Circular Wait:** There exists a circular chain of threads such that each thread holds one or more resources that are being requested by the next thread in the chain.

If any one of these conditions is broken, deadlock cannot occur. This framework provides the basis for all deadlock prevention and avoidance strategies. Understanding these conditions helps developers design systems that are immune to this class of failure.
