---
type: atomic
source: OSTEP Ch. 4
tags:
  - virtualization
  - processes
  - data-structures
related:
  - "[[A Process is a Running Program]]"
  - "[[Process States - Ready Running and Blocked]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[A Process is a Running Program]]"
  - "[[Process States - Ready Running and Blocked]]"
---

# Process Data Structures - PCB Registers and Memory Image

> [!SUMMARY]
> The OS maintains a **Process Control Block (PCB)** for each process, storing its register context, memory layout, state, and I/O information. A **process list** tracks all active processes. During context switches, the OS saves and restores register state using this structure, enabling time-sharing of the CPU.

## The Process Control Block

The **Process Control Block** (also called the process descriptor or task struct) is the OS data structure that represents a single process. It contains everything the OS needs to manage that process:

```c
// Simplified xv6 process structure
struct proc {
    char *mem;           // Start of process memory
    uint sz;             // Size of process memory
    char *kstack;        // Kernel stack for this process
    enum proc_state state; // Process state
    int pid;             // Process ID
    struct proc *parent; // Parent process
    void *chan;          // If non-zero, sleeping on chan
    int killed;          // If non-zero, has been killed
    struct file *ofile[NOFILE]; // Open files
    struct inode *cwd;   // Current directory
    struct context context; // Register context (switch here to run)
    struct trapframe *tf;   // Trap frame for current interrupt
};
```

## Key Fields

The PCB stores several categories of information:

**Register context:** When the OS stops running a process (descheduling or blocking), it saves the CPU register contents—program counter, stack pointer, general-purpose registers—into the PCB. When the process is later scheduled again, the OS restores these registers, resuming execution exactly where it left off. This save/restore mechanism is the core of **context switching**.

**Memory image:** The PCB records the boundaries of the process's address space—where code, data, heap, and stack reside. This information lets the OS set up hardware memory protection (base/bounds registers or page tables) before running the process.

**Process state:** A field indicating whether the process is running, ready, blocked, or in an initial/final state. The scheduler uses this to determine which processes are candidates for execution.

**I/O state:** The open file table for the process—an array of file descriptors pointing to open files, pipes, or devices. This persists across context switches so the process can resume I/O operations.

**Accounting and metadata:** Process ID (PID), parent PID, user ID, priority, CPU time consumed, and similar bookkeeping fields used for scheduling and resource management.

## The Process List

The OS maintains a **process list** (or process table): a collection of all PCBs for currently active processes. When the scheduler runs, it scans this list for processes in the ready state, selects one according to its policy, and performs a context switch.

## Context Switch Mechanics

A context switch between process A and process B involves:

1. Save A's register state into A's PCB
2. Update A's state field (running → ready or blocked)
3. Load B's register state from B's PCB
4. Update B's state field (ready → running)
5. Resume execution at B's saved program counter

This operation is performed by low-level OS code (often in assembly) and is triggered by timer interrupts or system calls that cause scheduling decisions.

## Why This Matters

The PCB and process list are the data foundation that makes CPU virtualization possible. Without a way to save and restore the complete machine state of each process, time-sharing would be impossible—every context switch would destroy the interrupted process's computation.
