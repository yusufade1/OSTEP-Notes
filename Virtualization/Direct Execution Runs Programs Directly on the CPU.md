---
type: atomic
source: OSTEP Ch. 6
tags:
  - virtualization
  - mechanisms
  - direct-execution
related:
  - "[[A Process is a Running Program]]"
  - "[[User Mode and Kernel Mode Provide Dual Protection Levels]]"
  - "[[Timer Interrupts Enable Preemptive Multitasking]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[A Process is a Running Program]]"
---

# Direct Execution Runs Programs Directly on the CPU

> [!SUMMARY]
> Direct execution means the OS runs user programs directly on the hardware CPU rather than emulating them. This is fast but creates two problems: how does the OS restrict what a program can do, and how does the OS regain control of the CPU? Limited Direct Execution solves both through hardware privilege modes and timer interrupts.

## The Basic Idea

When the OS wants to run a program, the simplest approach is to execute it directly on the CPU. The OS creates a process entry in the process list, allocates memory, loads the program code, sets up the stack with `argc`/`argv`, clears registers, and jumps to the program's entry point (`main()`). The program then runs native machine instructions at full hardware speed.

This **direct execution** protocol is straightforward:

| OS Actions | Program Actions |
|---|---|
| Create entry in process list | |
| Allocate memory; load program | |
| Set up stack with argv | |
| Clear registers | |
| Call main() | |
| | Run main() |
| | Execute return from main |
| Free memory; remove from list | |

## The Two Problems

Direct execution is fast, but it gives the OS no control:

**Problem 1: Restricted Operations.** If the program runs directly, how can the OS prevent it from accessing disk arbitrarily, consuming all memory, or interfering with other processes? Without restrictions, the OS cannot virtualize resources safely.

**Problem 2: Regaining Control.** Once the OS has jumped to user code, the OS is *not running*. If the OS is not running, how can it switch to another process? A cooperative approach (waiting for system calls) fails when programs loop or crash without yielding.

## Limited Direct Execution

The solution is to add *limits* to direct execution. The CPU provides **user mode** with restricted privileges and **kernel mode** with full hardware access. Programs execute in user mode; privileged operations require a controlled transfer to the kernel via **traps**. The OS regains control involuntarily through **timer interrupts**, which fire periodically regardless of what user code is doing.

This combination — direct execution with hardware-enforced limits — gives the OS both performance (native speed for user code) and control (restricted access, guaranteed preemption). It forms the foundation upon which scheduling, memory protection, and all higher-level OS abstractions are built.
