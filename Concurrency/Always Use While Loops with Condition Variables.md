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
  - "[[Race Conditions lead to Non-Deterministic Behavior]]"
prerequisites:
  - "[[Condition Variables Allow Threads to Sleep and Wake]]"
---

> [!SUMMARY]
> When waiting on a condition variable, threads must always use a while loop rather than an if statement to check the condition. This pattern handles spurious wakeups and ensures the condition is still true after re-acquiring the lock, adhering to Mesa semantics.

## The Rule: Always Use While

A fundamental rule when using condition variables is to enclose the wait call in a `while` loop, not an `if` statement.

**Correct:**
```c
pthread_mutex_lock(&m);
while (condition == false)
    pthread_cond_wait(&c, &m);
pthread_mutex_unlock(&m);
```

**Incorrect:**
```c
pthread_mutex_lock(&m);
if (condition == false)
    pthread_cond_wait(&c, &m);
pthread_mutex_unlock(&m);
```

## Mesa vs. Hoare Semantics

The reason for this rule lies in the semantics of the condition variable implementation.

In **Hoare semantics**, when a thread signals, the ownership of the lock is immediately transferred to the waiting thread. The waiter is guaranteed to run immediately, so the condition it was waiting for must still be true.

However, most systems (including Linux pthreads, Java, and C#) use **Mesa semantics**. In Mesa semantics, a signal simply moves a waiter from the sleep queue to the ready queue. The signaling thread continues to hold the lock until it unlocks. By the time the awakened thread actually runs and re-acquires the lock, the state of the world may have changed.

## Why `if` Breaks

Consider two consumer threads ($C_1$, $C_2$) and one producer ($P$).
1. $C_1$ checks the buffer, finds it empty, and waits.
2. $P$ produces an item, signals, and releases the lock.
3. $C_1$ is woken up but hasn't run yet.
4. Before $C_1$ runs, another consumer $C_2$ swoops in, acquires the lock, consumes the item, and releases the lock.
5. Now $C_1$ runs. It re-acquires the lock.
6. If $C_1$ used an `if` statement, it assumes the buffer is full (because it was signaled) and tries to consume. But $C_2$ already ate the item! This leads to an error (e.g., assertion failure or processing garbage).

## Spurious Wakeups

Additionally, some implementations allow **spurious wakeups**, where a thread returns from `wait` even though no signal was sent. This can happen due to implementation details or race conditions within the thread library.

Using a `while` loop solves both problems. When the thread wakes up (whether due to a signal or spuriously), it loops back and re-checks the condition. If the condition is false (e.g., the buffer is empty again), it goes back to sleep. This ensures the code is robust regardless of scheduling order.
