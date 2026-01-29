---
type: overview
source: "OSTEP Ch. 4-6: Processes"
tags:
  - virtualization
  - processes
related:
  - "[[Virtualization MOC]]"
  - "[[Threads - Chapter Overview]]"
  - "[[fork() Creates a Child by Copying Parent]]"
  - "[[Direct Execution Runs Programs Directly on the CPU]]"
  - "[[System Calls Transfer Control via Trap and Return-from-Trap]]"
prerequisites: []
---

# Processes - Chapter Overview

> [!SUMMARY]
> These chapters introduce the **process** as the fundamental abstraction for a running program. We cover the process lifecycle, the UNIX process API (`fork`, `exec`, `wait`), and the mechanism of **Limited Direct Execution**, which allows the OS to maintain control while running programs at hardware speed.


## Key Concepts

- **[[A Process is a Running Program]]** — The abstraction of an executing program's state.
- **[[Process States - Ready Running and Blocked]]** — The transitions between execution phases.
- **[[Process API Design Philosophy]]** — Why UNIX separates process creation (`fork`) from program execution (`exec`).
- **[[Direct Execution Runs Programs Directly on the CPU]]** — Achieving high performance by letting user code run on the processor.
- **[[User Mode and Kernel Mode Provide Dual Protection Levels]]** — Hardware support for restricting sensitive operations to the OS.
- **[[System Calls Transfer Control via Trap and Return-from-Trap]]** — The controlled mechanism for applications to request OS services.
- **[[Timer Interrupts Enable Preemptive Multitasking]]** — How the OS regains control from a running process to switch tasks.

## Chapter Questions

1. How does the `fork()` return value differ in parent and child?
2. Why is a system call more expensive than a regular function call?
3. How does the trap table prevent users from executing arbitrary kernel code?
4. What state must be saved during a context switch?