---
type: atomic
source: OSTEP Ch. 4
tags:
  - virtualization
  - processes
  - abstraction
related:
  - "[[Process States - Ready Running and Blocked]]"
  - "[[Process Data Structures - PCB Registers and Memory Image]]"
  - "[[Virtualization MOC]]"
prerequisites: []
---
# A Process is a Running Program

> [!SUMMARY]
> A process is the OS abstraction for a running program. While a program is a static set of instructions and data on disk, a process is its dynamic instantiation—encompassing the machine state needed to execute those instructions. The OS virtualizes the CPU by time-sharing it among processes, giving each the illusion of owning its own processor.

## The Abstraction

A **program** is a lifeless collection of bytes sitting on disk—instructions and static data waiting to be brought to life. A **process** is what emerges when the OS loads a program into memory and begins executing it. The distinction is fundamental: the program is the recipe, the process is the act of cooking.

The OS can run many processes simultaneously despite having only a few physical CPUs. It achieves this through **time-sharing**: running one process for a short while, then switching to another, creating the illusion that many virtual CPUs exist. This mechanism is called **CPU virtualization**.

## Machine State

A process's **machine state** is everything a running program can read or affect during execution:

- **Memory (address space):** The memory that the process can address. This includes the program's instructions (code), static data, the heap (dynamically allocated memory), and the stack (local variables, function parameters, return addresses).
- **Registers:** The contents of the CPU registers, including the program counter (PC) which indicates the next instruction, and the stack pointer and frame pointer which manage the function call stack.
- **I/O information:** The list of files the process currently has open, represented as file descriptors.

## Creating a Process

The OS must perform several steps to transform a program into a process:

1. **Load** the program's code and static data from disk into the process's address space in memory.
2. **Allocate** the run-time stack and initialize it with arguments (argc/argv).
3. **Allocate** the heap, which starts small and grows via `malloc()` calls.
4. **Set up** I/O—for Unix systems, each process starts with three open file descriptors: stdin, stdout, and stderr.
5. **Jump** to the program's entry point (`main()`), transferring control to the new process.

Loading can happen eagerly (all at once) or lazily (on demand via paging and swapping mechanisms), but the result is the same: the process is ready to run.

## Why This Matters

The process abstraction is the foundation of CPU virtualization. Every scheduling decision, context switch, and memory protection mechanism builds on this concept. Understanding what a process *is*—the complete machine state of a running program—is prerequisite to understanding how the OS manages multiple processes concurrently.
