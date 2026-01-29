---
type: concept
source: "OSTEP Ch. 4: The Abstraction: The Process"
tags:
  - virtualization
  - processes
  - scheduling
related:
  - "[[A Process is a Running Program]]"
  - "[[Process Data Structures - PCB Registers and Memory Image]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[A Process is a Running Program]]"
---
# Process States - Ready Running and Blocked

> [!SUMMARY]
> A process exists in one of three primary states: **running** (executing on the CPU), **ready** (able to run but waiting for CPU time), or **blocked** (waiting for an event such as I/O completion). The OS scheduler moves processes between these states, and understanding these transitions is essential to understanding CPU virtualization and scheduling.

## The Three States

At any point in time, a process is in exactly one of these states:

- **Running:** The process is currently executing instructions on a CPU. Only one process can be running per CPU core at any given instant.
- **Ready:** The process is prepared to run—it has everything it needs—but the OS has chosen not to run it at this moment. It is waiting in a queue for its turn on the CPU.
- **Blocked:** The process has performed an operation that makes it unable to continue until some external event occurs. The most common cause is initiating an I/O request (e.g., reading from disk). The process cannot use the CPU productively until the I/O completes.

## State Transitions

Processes move between states through these transitions:

```
         Scheduled
  Ready ──────────► Running
    ▲                  │  │
    │   Descheduled    │  │
    │◄─────────────────┘  │
    │                     │
    │      I/O done       │  I/O initiate
    │◄──────────────      │
    │              │      ▼
    └──────────  Blocked
```

1. **Running → Ready (Descheduled):** The OS decides to stop running this process, typically because a timer interrupt fired and the scheduler picked a different process.
2. **Ready → Running (Scheduled):** The OS scheduler selects this process from the ready queue to execute next.
3. **Running → Blocked (I/O initiate):** The process issues a blocking request (e.g., disk read). The OS moves it off the CPU since it cannot make progress until the request completes.
4. **Blocked → Ready (I/O done):** The I/O operation finishes. The OS moves the process back to the ready queue; it can now be scheduled again.

## Scheduling Decisions

These transitions represent two types of OS decisions:

- When a process becomes **blocked**, the OS *must* run something else (or idle). This is straightforward.
- When a process is **descheduled** (running → ready), the OS is making a **policy** choice: which process deserves the CPU next? This decision is the domain of scheduling algorithms (FIFO, SJF, Round Robin, MLFQ, etc.).

## Additional States

Some systems define additional states beyond the core three:

- **Initial (embryo):** The process is being created but is not yet ready to run.
- **Final (zombie):** The process has finished execution but its entry persists in the process table so the parent can collect its exit status (via `wait()`). Once the parent reaps it, the process is fully destroyed.

These bookend states handle the lifecycle edges, but the core dynamics of CPU virtualization happen in the ready–running–blocked triangle.
