---
type: mechanism
source: "OSTEP Ch. 29: Locked Data Structures"
tags:
  - concurrency
  - data-structures
  - synchronization
related:
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
  - "[[Critical Sections Require Mutual Exclusion]]"
  - "[[Race Conditions lead to Non-Deterministic Behavior]]"
prerequisites:
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
---

> [!SUMMARY]
> Concurrent linked lists present a more complex synchronization challenge than counters because the critical section involves pointer manipulation. While a single global lock is simple and correct, finer-grained approaches like **hand-over-hand locking** attempt to increase parallelism by locking individual nodes. However, the overhead of acquiring and releasing many locks often outweighs the benefits, serving as a cautionary tale against premature optimization.

## Single Lock vs. Fine-Grained Locking

The most straightforward way to make a linked list thread-safe is to add a single lock to the list structure. Every operation (insert, lookup, delete) acquires this lock before starting and releases it upon completion.

```c
// Simplified insert with single lock
void List_Insert(list_t *L, int key) {
    pthread_mutex_lock(&L->lock);
    node_t *new = malloc(sizeof(node_t));
    new->key = key;
    new->next = L->head;
    L->head = new;
    pthread_mutex_unlock(&L->lock);
}
```

This approach is correct but limits concurrency; only one thread can access the list at a time. If one thread is reading the tail of a long list, another thread cannot even insert at the head.

## Hand-Over-Hand Locking (Lock Coupling)

To allow more concurrency, developers might try **hand-over-hand locking** (or lock coupling). Instead of one lock for the whole list, each node has its own lock. When traversing the list, a thread:
1.  Locks the current node.
2.  Locks the next node.
3.  Unlocks the current node.

This conceptual "crabbing" movement ensures that at any point, the thread holds a lock preventing the portion of the list it is traversing from being modified. It allows multiple threads to traverse different parts of the list simultaneously.

## The Performance Trap

Despite the theoretical concurrency gain, hand-over-hand locking is rarely used in practice for linked lists. The cost of acquiring and releasing a lock is significant. In a list traversal, paying that cost for *every single node* is prohibitively expensive.

For example, if lock operations take 100 cycles and traversing a node takes 10 cycles, the fine-grained approach makes the traversal 10x slower, even if it allows some parallelism. A single lock is often faster simply because it has low overhead.

This highlights a key lesson in concurrent data structure design: **granularity matters**. Moving from coarse-grained (one lock) to fine-grained (many locks) only helps if the work done inside the lock is substantial enough to amortize the locking overhead. For simple structures like linked lists, the "simple" solution is often also the most performant one unless the list is extremely long and contention is incredibly high.
