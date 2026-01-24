---
type: overview
source: OSTEP Ch. 4
tags:
  - virtualization
  - processes
related:
  - "[[Virtualization MOC]]"
  - "[[A Process is a Running Program]]"
  - "[[Process States - Ready Running and Blocked]]"
  - "[[Process Data Structures - PCB Registers and Memory Image]]"
---

# Processes - Chapter Overview

This chapter introduces the **process** as the fundamental abstraction the OS provides for a running program. The OS virtualizes the CPU by time-sharing it among processes, giving each the illusion of having its own processor.

## Key Concepts

- **[[A Process is a Running Program]]** — The process abstraction encompasses all the state needed to run a program: memory, registers, and I/O information.
- **[[Process States - Ready Running and Blocked]]** — A process transitions between ready, running, and blocked states as it executes and waits for resources.
- **[[Process Data Structures - PCB Registers and Memory Image]]** — The OS tracks each process using a Process Control Block containing register context, memory mappings, and scheduling metadata.

## Chapter Questions

1. What makes a process different from a program on disk?
2. How does the OS create the illusion of many CPUs from few?
3. What information must the OS track for each running process?
