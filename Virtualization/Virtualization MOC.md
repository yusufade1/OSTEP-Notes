---
type: moc
tags:
  - virtualization
related:
  - "[[Concurrency MOC]]"
  - "[[Persistence MOC]]"
prerequisites: []
source: "OSTEP Book"
---

# Virtualization

> [!SUMMARY]
> The OS virtualizes physical resources (CPU, memory) to provide each process the illusion of having its own dedicated machine.

## Introduction
Foundation and overview of operating system goals.
- [[Introduction - Chapter Overview]] — The OS as a resource manager and the Three Easy Pieces.

## Processes
The fundamental abstraction of a running program and its lifecycle.
- [[Processes - Chapter Overview]] — Introduction to the process abstraction and its management.
- [[A Process is a Running Program]] — The core definition of what an OS manages during execution.
- [[Process States - Ready Running and Blocked]] — How processes transition between execution states.
- [[Process Data Structures - PCB Registers and Memory Image]] — The metadata the OS tracks for every process.
- [[Direct Execution Runs Programs Directly on the CPU]] — How the OS maintains control while allowing high-speed execution.

## Scheduling
Policies and algorithms for deciding which process to run next.
- [[Scheduling - Chapter Overview]] — Overview of CPU scheduling goals and basic algorithms.
- [[Turnaround Time and Response Time Measure Scheduling Quality]] — The primary metrics used to evaluate scheduler performance.
- [[MLFQ Basic Rules - Priority Queues with Feedback]] — The sophisticated scheduler used in many modern operating systems.
- [[Lottery Scheduling Uses Tickets to Achieve Proportional Share]] — A randomized approach to fair-share scheduling.
- [[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges]] — The complexities of scaling scheduling to multiple processors.

## Memory
Mechanisms for providing each process with a private, protected address space.
- [[Memory - Chapter Overview]] — Introduction to address spaces and memory virtualization goals.
- [[Address Translation and Paging - Chapter Overview]] — Hardware/software mechanisms for efficient translation.
- [[Swapping - Chapter Overview]] — Mechanisms and policies for using disk as memory.
- [[The Address Space Abstracts Physical Memory for Each Process]] — The logical view of memory presented to applications.
- [[The Page Table Stores Virtual-to-Physical Mappings]] — The core data structure for fixed-size memory virtualization.
- [[The TLB Caches Address Translations for Fast Access]] — Hardware support for making paging efficient.
- [[Multi-Level Page Tables Save Space Through Demand Allocation]] — A technique for managing large, sparse address spaces.