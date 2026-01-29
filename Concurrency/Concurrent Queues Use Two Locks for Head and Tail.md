---
type: mechanism
source: "OSTEP Ch. 29: Locked Data Structures"
tags:
  - concurrency
  - data-structures
  - queues
related:
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
  - "[[Concurrent Linked Lists Enable Parallel Access]]"
  - "[[Race Conditions lead to Non-Deterministic Behavior]]"
prerequisites:
  - "[[pthread_mutex_lock() and unlock() Protect Critical Sections]]"
---

> [!SUMMARY]
> Concurrent queues are a fundamental building block for producer-consumer patterns. Unlike linked lists where fine-grained locking often fails, queues benefit significantly from a **two-lock approach**: one lock for the head (enqueuing) and one for the tail (dequeuing). This separation allows enqueue and dequeue operations to proceed in parallel, effectively doubling throughput in many scenarios without the complexity of lock-free algorithms.

## The Two-Lock Strategy

A standard unbounded queue implementation usually tracks a `head` pointer (where items are removed) and a `tail` pointer (where items are added). In a naive thread-safe approach, we would use a single lock to protect the entire struct. This means a producer adding an item blocks a consumer trying to remove an item, even though they are modifying different ends of the data structure.

The Michael and Scott queue (a famous algorithm, though we discuss a lock-based variant here) solves this by using **two locks**:
1.  `headLock`: Protects the `head` pointer during dequeue operations.
2.  `tailLock`: Protects the `tail` pointer during enqueue operations.

```c
typedef struct __queue_t {
    node_t *head;
    node_t *tail;
    pthread_mutex_t headLock;
    pthread_mutex_t tailLock;
} queue_t;

void enqueue(queue_t *q, int value) {
    node_t *tmp = malloc(sizeof(node_t));
    tmp->value = value;
    tmp->next = NULL;

    pthread_mutex_lock(&q->tailLock);
    q->tail->next = tmp;
    q->tail = tmp;
    pthread_mutex_unlock(&q->tailLock);
}
```

## The Dummy Node Trick

A subtle issue arises when the queue is empty or nearly empty: the head and tail pointers might refer to the same node, leading to a race condition where enqueue and dequeue threads fight over the same memory despite holding different locks.

To solve this cleanly, the queue is initialized with a **dummy node** (often called a sentinel). This node does not contain valid data but ensures that `head` and `tail` are never NULL.
- **Enqueue** always attaches new nodes to `tail->next`.
- **Dequeue** always removes the node *after* head (making the old head the "new" dummy node to be freed, or reading the data from the node after head).

This structural trick ensures that the enqueue and dequeue operations remain independent for the vast majority of cases. The only contention occurs when memory allocators themselves lock, but the logical queue operations are separated.

This design demonstrates **concurrency by separation**: by identifying which parts of the state are truly shared (the structure itself) vs. which are effectively independent (the two ends), we can split locks and increase parallelism safely.
