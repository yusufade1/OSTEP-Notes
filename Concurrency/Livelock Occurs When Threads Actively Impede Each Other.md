---
type: atomic
source: OSTEP Ch. 26
tags: [concurrency, bugs]
related:
  - "[[Deadlock Occurs When Threads Wait on Each Other Circularly]]"
  - "[[Deadlock Prevention Breaks One of the Four Necessary Conditions]]"
  - "[[Spin Locks rely on Busy Waiting]]"
prerequisites:
  - "[[Deadlock Occurs When Threads Wait on Each Other Circularly]]"
---

> [!SUMMARY]
> Livelock is a concurrency bug where threads are not blocked (they are running and consuming CPU), but they make no progress because they constantly react to each other's state changes.

**Livelock** differs from deadlock in that threads are not sleeping or waiting on a lock; they are actively executing code, but the system as a whole is stuck in a loop of fruitless activity.

### The Scenario
Livelock often arises from algorithms designed to prevent deadlock. Consider the **trylock** strategy for deadlock prevention:

**Thread 1:**
```c
lock(L1);
if (trylock(L2) fail) { unlock(L1); retry; }
```

**Thread 2:**
```c
lock(L2);
if (trylock(L1) fail) { unlock(L2); retry; }
```

If these threads run in perfect synchrony, they might repeatedly:
1.  Thread 1 grabs L1, Thread 2 grabs L2.
2.  Thread 1 fails to get L2, Thread 2 fails to get L1.
3.  Both release their locks.
4.  Both retry immediately and repeat step 1.

They are running (consuming CPU cycles) but never progressing past the lock acquisition phase. This is effectively a deadlock that burns power.

### The Solution: Randomness
The standard solution to livelock, particularly in retry loops, is to introduce **randomness**.
*   **Exponential Backoff:** Instead of retrying immediately, a thread waits for a random interval. If it fails again, it increases the potential wait time.
*   This technique is famously used in Ethernet (CSMA/CD) to handle packet collisions. In the context of threads, the random delay ensures that two threads will eventually fall out of sync, allowing one to proceed while the other waits.

Livelock illustrates that simple solutions to one concurrency problem (using trylock to avoid deadlock) can introduce new, subtle failure modes.
