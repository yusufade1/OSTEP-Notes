---
type: moc
tags:
  - ostep
  - os
related:
  - "[[Virtualization MOC]]"
  - "[[Concurrency MOC]]"
  - "[[Persistence MOC]]"
prerequisites: []
source: "OSTEP Book"
---

# Operating Systems: Three Easy Pieces (OSTEP)

> [!SUMMARY]
> A comprehensive guide to modern operating systems, organized into three "easy" pieces: Virtualization, Concurrency, and Persistence. This vault contains atomic notes and interconnected concepts derived from the OSTEP textbook.

## The Three Easy Pieces

### 1. [[Virtualization MOC|Virtualization]]
How the OS takes a physical resource (such as a processor, or memory, or a disk) and transforms it into a more general, powerful, and easy-to-use virtual form of itself.
- **Processes**: The abstraction of a running program.
- **Scheduling**: Policies for deciding which process to run.
- **Memory**: Providing each process with its own private address space.

### 2. [[Concurrency MOC|Concurrency]]
How the OS and applications deal with multiple things happening at the same time, particularly when they share resources like memory.
- **Threads**: Parallel execution within a single address space.
- **Locks**: Ensuring mutual exclusion in critical sections.
- **Condition Variables**: Coordinating thread execution.

### 3. [[Persistence MOC|Persistence]]
How the OS stores data reliably over the long term, despite crashes and power failures.
- **I/O Devices**: Communicating with hardware.
- **File Systems**: Organizing data into files and directories.
- **Distributed Systems**: Sharing data across a network.

---
## Navigation
- [[Virtualization MOC]]
- [[Concurrency MOC]]
- [[Persistence MOC]]
