---
type: atomic
source: OSTEP Ch. 28
tags: [concurrency, locks, fairness, ticket-lock]
related: [[Lock Design Goals - Mutual Exclusion Fairness and Performance]], [[Test-and-Set Instruction Enables Atomic Locking]]
prerequisites: [[Critical Sections Require Mutual Exclusion]]
---

> [!SUMMARY]
> Ticket locks use the Fetch-and-Add atomic instruction to solve the fairness problem inherent in simple spin locks. By assigning a unique "ticket" number to each arriving thread and serving them in order, ticket locks ensure First-In-First-Out (FIFO) access and prevent starvation.

# Ticket Locks Ensure Fairness with Fetch-and-Add

Simple spin locks (using Test-and-Set or CAS) rely on luck: when the lock is released, the "winner" is whichever thread happens to execute the atomic instruction next. This can lead to starvation. Ticket locks solve this by adding order.

## The Fetch-and-Add Instruction
This instruction atomically increments a value and returns the *old* value.

```c
int FetchAndAdd(int *ptr) {
    int old = *ptr;
    *ptr = old + 1;
    return old;
}
```

## Ticket Lock Implementation
A ticket lock uses two counters: `ticket` (total requests) and `turn` (currently serving).

```c
typedef struct {
    int ticket;
    int turn;
} lock_t;

void lock_init(lock_t *lock) {
    lock->ticket = 0;
    lock->turn = 0;
}

void lock(lock_t *lock) {
    int myturn = FetchAndAdd(&lock->ticket);
    while (lock->turn != myturn)
        ; // spin
}

void unlock(lock_t *lock) {
    lock->turn = lock->turn + 1;
}
```

## How It Works
1.  **Arrival:** A thread grabs a ticket (`myturn`) by incrementing the global `ticket` counter. This operation is atomic.
2.  **Waiting:** The thread spins until the global `turn` counter matches its ticket.
3.  **Release:** When the holder finishes, it increments `turn`, allowing the next thread in line (ticket `n+1`) to stop spinning.

## Benefits
*   **Fairness:** Threads are guaranteed to acquire the lock in the exact order they requested it.
*   **Determinism:** No thread can be starved by a stream of incoming high-priority threads.
