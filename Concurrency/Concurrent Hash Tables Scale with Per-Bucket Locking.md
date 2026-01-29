---
type: mechanism
source: "OSTEP Ch. 29: Locked Data Structures"
tags:
  - concurrency
  - data-structures
  - hashing
related:
  - "[[Concurrent Linked Lists Enable Parallel Access]]"
  - "[[Concurrent Counters Scale with Approximate Counting]]"
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
prerequisites:
  - "[[Concurrent Linked Lists Enable Parallel Access]]"
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
---

> [!SUMMARY]
> Concurrent hash tables represent the "sweet spot" of lock-based concurrency. By combining the O(1) average access time of hash tables with **lock striping** (one lock per bucket), they achieve excellent scalability. Unlike linked lists where fine-grained locking is too expensive, hash tables naturally partition data, meaning threads accessing different buckets effectively run in parallel with zero contention.

## Scaling with Lock Striping

A hash table is essentially a fixed-size array of lists (buckets). To make it thread-safe, we could use a single global lock. However, this returns us to the same bottleneck as the global counter or single-lock list: only one thread can do anything at a time.

A better approach is to give **each bucket its own lock**. This is often called "lock striping."

```c
#define BUCKETS 29

typedef struct __hash_t {
    list_t lists[BUCKETS]; // Each list has its own lock
} hash_t;

int Hash_Insert(hash_t *H, int key) {
    int bucket = key % BUCKETS;
    // Only lock the specific list we need
    return List_Insert(&H->lists[bucket], key);
}
```

## Why This Works

This design works incredibly well because of the statistical properties of hash functions. If the hash function distributes keys uniformly, then `N` threads will likely map to `N` different buckets.
- Thread A inserts key 10 (Bucket 2) -> Locks Bucket 2.
- Thread B inserts key 50 (Bucket 5) -> Locks Bucket 5.
- Thread C lookups key 99 (Bucket 1) -> Locks Bucket 1.

All three threads proceed in parallel. Contention only occurs if two threads happen to hash to the exact same bucket at the same time. As the table grows (more buckets), the probability of collision drops, and scalability remains linear with the number of CPUs.

## Simplicity and Performance

What makes this pattern powerful is that it reuses the simpler concurrent data structures we already built. The hash table doesn't need complex new logic; it is simply a collection of **concurrent linked lists**.

We saw earlier that fine-grained locking (hand-over-hand) was bad for a *single* list. But here, the "fine-grained" nature is at the *bucket* level, not the *node* level. The lock acquisition overhead is paid once per operation (per bucket), not once per node. This balance—locking at the granularity of the data partition—is often the key to high-performance concurrent design. It avoids the global bottleneck while avoiding the excessive overhead of locking every tiny element.
