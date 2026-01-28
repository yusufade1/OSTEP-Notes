---
type: atomic
source: OSTEP Ch. 26
tags: [concurrency, bugs, deadlock]
related:
  - "[[Deadlock Occurs When Threads Wait on Each Other Circularly]]"
  - "[[The Dining Philosophers Problem Illustrates Deadlock]]"
  - "[[Deadlock Avoidance Uses Knowledge to Sidestep Unsafe States]]"
prerequisites:
  - "[[Deadlock Occurs When Threads Wait on Each Other Circularly]]"
---

> [!SUMMARY]
> Deadlock prevention involves structuring code to ensure that at least one of the four necessary conditions for deadlock (Mutual Exclusion, Hold-and-Wait, No Preemption, Circular Wait) can never hold.

**Deadlock prevention** is a strategy where we design the system to statically invalidate one of the four Coffman conditions required for deadlock.

### Breaking Circular Wait
The most common and practical prevention strategy is to **break the circular wait**. This is done by imposing a strict **total ordering** on lock acquisition. If there are locks L1 and L2, and the rule is "always acquire L1 before L2", then a cycle cannot form.
- **Example:** In the Linux kernel, locks are often assigned a hierarchy level, and tools (like `lockdep`) verify that locks are taken in the correct order.
- **Complexity:** This works well for simple systems but becomes difficult in complex codebases where functions call each other deeply.

### Breaking Hold-and-Wait
We can prevent threads from holding resources while waiting for others by requiring them to **acquire all locks atomically** at once.
- **Implementation:** A global "lock-acquisition lock" can be used. A thread grabs this global lock, then grabs L1, L2, etc., then releases the global lock.
- **Downside:** This reduces concurrency (serialization) and requires knowing all required locks in advance, which breaks modularity.

### Breaking No Preemption
We can allow resources to be preempted using the **trylock** primitive (`pthread_mutex_trylock`). If a thread holds L1 and tries to get L2 but fails, it releases L1 and tries again later.
```c
top:
pthread_mutex_lock(L1);
if (pthread_mutex_trylock(L2) != 0) {
    pthread_mutex_unlock(L1);
    goto top; // Try again
}
```
- **Downside:** This can lead to **livelock**, where threads continually lock/unlock in sync without making progress. It acts as a form of preemption at the application level.

### Breaking Mutual Exclusion
Using **wait-free** or **lock-free** data structures (using atomic hardware instructions like Compare-And-Swap) can eliminate the need for locks entirely, removing the mutual exclusion condition. However, writing correct lock-free code is notoriously difficult.
