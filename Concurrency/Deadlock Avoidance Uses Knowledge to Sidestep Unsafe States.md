---
type: concept
source: "OSTEP Ch. 26: Concurrency: An Introduction"
tags:
  - concurrency
  - bugs
  - deadlock
  - algorithm
related:
  - "[[Deadlock Prevention Breaks One of the Four Necessary Conditions]]"
  - "[[Deadlock Occurs When Threads Wait on Each Other Circularly]]"
  - "[[Semaphores Define wait and post Operations]]"
prerequisites:
  - "[[Deadlock Occurs When Threads Wait on Each Other Circularly]]"
---

> [!SUMMARY]
> Deadlock avoidance differs from prevention by allowing the system to potentially enter unsafe configurations but checking at runtime if a resource allocation request would lead to a deadlock. If it might, the request is denied or delayed.

**Deadlock avoidance** uses runtime knowledge about resource demands to steer the system clear of deadlock. Unlike prevention, which imposes strict structural rules (like lock ordering), avoidance allows more flexibility but requires global knowledge.

### The Banker's Algorithm
The classic example of deadlock avoidance is Dijkstra's **Banker's Algorithm**.
1.  **Declaration:** Each process declares its maximum possible resource needs upfront.
2.  **Request:** When a process requests a resource, the OS simulates granting it.
3.  **Check:** The OS checks if the resulting state is "safe".
    *   A **safe state** is one where there exists at least one sequence of execution where all processes can finish (i.e., the OS can satisfy the maximum demands of one process, wait for it to finish and return resources, then satisfy the next, etc.).
4.  **Decision:** If the state is safe, the request is granted. If unsafe (deadlock is possible), the thread is put to sleep until resources allow a safe transition.

### Limitations
While theoretically elegant, deadlock avoidance is rarely used in modern general-purpose operating systems for several reasons:
*   **Global Knowledge:** Processes rarely know their maximum resource needs in advance.
*   **Performance:** Running a safety check on every allocation is expensive.
*   **Concurrency:** The algorithm itself must be synchronized, becoming a bottleneck.

Avoidance is mostly found in specialized environments (like embedded real-time systems) where workloads are static and well-defined.
