---
type: atomic
source: OSTEP Ch. 25
tags: [concurrency, synchronization, semaphores, deadlock, patterns]
related: [[Semaphores Define wait and post Operations]], [[Binary Semaphores Act as Mutual Exclusion Locks]]
prerequisites: [[Semaphores Define wait and post Operations]]
---

> [!SUMMARY]
> The **Dining Philosophers Problem** is a classic concurrency puzzle proposed by Dijkstra. It illustrates how competition for shared resources (forks) can lead to **deadlock** if not managed carefully. The solution involves breaking the circular dependency in resource acquisition.

## The Setup

*   **5 Philosophers** sit around a table.
*   **5 Forks** are placed between them.
*   A philosopher needs **two forks** (left and right) to eat.
*   Between eating, they think.

We represent each fork as a semaphore:
```c
sem_t forks[5]; // Init all to 1
```

## The Deadlock Scenario

If every philosopher follows this algorithm:
1.  Grab left fork (`sem_wait(forks[left])`)
2.  Grab right fork (`sem_wait(forks[right])`)
3.  Eat
4.  Put down forks

If all philosophers act simultaneously, each grabs their left fork. Now, every fork is taken (value 0). When they try to grab their right fork, they all wait forever. This is **deadlock**.

## The Solution: Breaking Circularity

To prevent deadlock, we must break the cycle of dependency. A simple solution is to change the order for at least one philosopher.

Let the last philosopher (P4) grab the **right** fork first, then the **left**. Everyone else grabs left then right.

```c
void philosopher(int p) {
    int left = p;
    int right = (p + 1) % 5;

    if (p == 4) { // Break dependency
        sem_wait(&forks[right]);
        sem_wait(&forks[left]);
    } else {
        sem_wait(&forks[left]);
        sem_wait(&forks[right]);
    }
    
    eat();
    
    sem_post(&forks[left]);
    sem_post(&forks[right]);
}
```

This ensures that at least one philosopher can always proceed, preventing the circular wait condition required for deadlock.
