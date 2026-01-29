---
type: mechanism
source: "OSTEP Ch. 30: Condition Variables"
tags:
  - concurrency
  - synchronization
  - condition-variables
related:
  - "[[Condition Variables Allow Threads to Sleep and Wake]]"
  - "[[Producer-Consumer Problem Solved with Condition Variables]]"
  - "[[Slab Allocators Pre-Allocate Fixed-Size Object Caches]]"
prerequisites:
  - "[[Condition Variables Allow Threads to Sleep and Wake]]"
---

> [!SUMMARY]
> A covering condition occurs when a thread cannot determine exactly which waiting thread to wake, potentially waking the wrong one. The solution is to use `pthread_cond_broadcast()` to wake all waiting threads, allowing them to re-check their conditions, albeit at a performance cost.

## The Problem: Which Thread to Wake?

Standard `pthread_cond_signal()` wakes up at least one waiting thread. In many cases (like the simple producer-consumer), any waiting thread will do. However, in some scenarios, the signaling thread doesn't know *which* thread needs to be woken.

Consider a memory allocator where threads wait for free memory:
```c
// Thread A wants 100 bytes
while (bytes_free < 100)
    wait(&c, &m);

// Thread B wants 10 bytes
while (bytes_free < 10)
    wait(&c, &m);
```

Suppose `bytes_free` is 0. Both A and B are waiting.
Then Thread C frees 50 bytes and calls `signal(&c)`.

If the system wakes Thread A:
1. A wakes up.
2. Checks `bytes_free < 100` (50 < 100 is true).
3. A goes back to sleep.
4. Thread B remains asleep, even though it *could* have run (50 > 10).
5. The memory sits unused.

This scenario is called a **covering condition** because the condition (memory is free) "covers" many specific needs (10 bytes, 100 bytes, etc.), and the simple signal isn't smart enough to distinguish them.

## The Solution: Broadcast

The solution is to use `pthread_cond_broadcast()` (or `notifyAll` in Java).

```c
void free(int size) {
    Lock(&m);
    bytes_free += size;
    Cond_broadcast(&c); // Wake EVERYONE
    Unlock(&m);
}
```

With broadcast:
1. Thread C frees 50 bytes and broadcasts.
2. Both A and B (and any others) are moved to the ready queue.
3. Thread A runs, checks condition (50 < 100), goes back to sleep.
4. Thread B runs, checks condition (50 > 10), grabs the memory, and proceeds.

## Trade-off: Correctness vs. Performance

Broadcast is a heavy hammer. If 100 threads are waiting and only one can proceed, waking all 99 others is wasteful (the "thundering herd" problem). They all wake up, contend for the lock, check their condition, and 99 go back to sleep.

However, for covering conditions, broadcast is often the *only* way to ensure correctness without complex logic to manage specific queues for every possible condition size. It trades CPU cycles for semantic correctness.
