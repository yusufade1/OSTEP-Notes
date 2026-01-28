---
type: atomic
source: OSTEP Ch. 26
tags: [concurrency, bugs, condition-variables]
related:
  - "[[Condition Variables Allow Threads to Sleep and Wake]]"
  - "[[Always Use While Loops with Condition Variables]]"
  - "[[Semaphores Can Order Threads Like Condition Variables]]"
prerequisites:
  - "[[Condition Variables Allow Threads to Sleep and Wake]]"
---

> [!SUMMARY]
> Order violation bugs occur when the assumed order of memory accesses between threads is not enforced, leading to operations occurring in an incorrect sequence. These are typically fixed using condition variables or semaphores to enforce ordering.

An **order violation** happens when the correctness of a program depends on the relative ordering of events in different threads, but the code does not explicitly guarantee that order.

### The Problem
Consider this example from a Mozilla bug where a strict initialization order was expected.

**Thread 1 (Initialization):**
```c
void init() {
    mThread = PR_CreateThread(mMain, ...);
}
```

**Thread 2 (Main Logic):**
```c
void mMain(...) {
    mState = mThread->State;
}
```

The programmer assumes that Thread 1 will complete the initialization (setting `mThread`) before Thread 2 attempts to use it. However, if Thread 2 runs immediately—perhaps because it was created earlier or scheduled aggressively—it may access `mThread` before it has been assigned, resulting in a NULL pointer dereference or reading garbage data.

### The Solution
To fix an order violation, we must enforce the specific order of execution. This is the primary use case for **condition variables** (or semaphores). We create a synchronization point where Thread 2 waits until Thread 1 signals that initialization is complete.

**Fixed Code:**
```c
pthread_mutex_lock(&mtLock);
while (mtInit == 0)
    pthread_cond_wait(&mtCond, &mtLock);
pthread_mutex_unlock(&mtLock);

mState = mThread->State;
```

In the initialization thread:
```c
pthread_mutex_lock(&mtLock);
mThread = PR_CreateThread(...);
mtInit = 1;
pthread_cond_signal(&mtCond);
pthread_mutex_unlock(&mtLock);
```

By adding a state variable (`mtInit`) and a condition variable, we ensure that `mMain` never proceeds until `init` has finished its work. This transforms the implicit assumption of ordering into an explicit constraint enforced by the OS.
