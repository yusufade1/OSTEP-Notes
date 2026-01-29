---
type: concept
source: "OSTEP Ch. 26: Concurrency: An Introduction"
tags:
  - concurrency
  - race-condition
  - bug
  - non-determinism
related:
  - "[[Threads - Chapter Overview]]"
  - "[[Critical Sections Require Mutual Exclusion]]"
  - "[[Concurrency Bugs - Chapter Overview]]"
prerequisites:
  - "[[Thread Creation and Execution Model]]"
---

# Race Conditions lead to Non-Deterministic Behavior

A **race condition** occurs when the results of a program depend on the relative timing of events, such as the scheduling order of threads. In concurrent programming, this typically happens when multiple threads access shared data and at least one modifies it, without proper synchronization.

## The Shared Counter Example

Consider a simple program where two threads try to increment a shared global counter `cnt` by 1.

```c
#include <pthread.h>

static volatile int cnt = 0;

void *mythread(void *arg) {
    for (int i = 0; i < 10000000; i++) {
        cnt = cnt + 1; // The Critical Section
    }
    return NULL;
}
```

If we run this with two threads, we expect the final result to be 20,000,000. However, the actual result often ends up being less, like 19,482,311. Even worse, the result changes every time we run the program. This is **non-deterministic behavior**.

## The Problem: Uncontrolled Scheduling

The reason this fails is that the C statement `cnt = cnt + 1` is not **atomic**. The compiler compiles it into three machine instructions:
1.  **Load**: Move the value of `cnt` from memory into a register.
2.  **Add**: Increment the value in the register.
3.  **Store**: Write the value from the register back to memory.

A race condition occurs if a **context switch** happens in the middle of this sequence.

1.  **Thread A** loads `cnt` (value 50) into its register.
2.  **Thread A** increments register to 51.
3.  **Timer Interrupt!** OS saves Thread A's state (register=51) and switches to Thread B.
4.  **Thread B** loads `cnt` (still 50!) into its register.
5.  **Thread B** increments register to 51.
6.  **Thread B** stores 51 into memory.
7.  **Context Switch** back to Thread A.
8.  **Thread A** resumes and stores 51 into memory.

Both threads claimed to increment the counter, but the value only went from 50 to 51. One increment was "lost." This sequence of code that accesses a shared variable is called a **critical section**, and executing it without protection causes a race.

> [!SUMMARY]
> A **race condition** arises when multiple threads access shared data concurrently and the outcome depends on the unlucky timing of thread scheduling. This leads to **non-deterministic** bugs that are hard to reproduce. It happens because high-level operations (like incrementing a variable) are often composed of multiple low-level machine instructions (load-update-store) that can be interrupted by context switches.
