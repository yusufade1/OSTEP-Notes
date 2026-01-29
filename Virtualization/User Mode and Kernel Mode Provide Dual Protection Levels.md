---
type: mechanism
source: "OSTEP Ch. 6: Mechanism: Limited Direct Execution"
tags:
  - virtualization
  - mechanisms
  - protection
  - hardware-support
related:
  - "[[Direct Execution Runs Programs Directly on the CPU]]"
  - "[[System Calls Transfer Control via Trap and Return-from-Trap]]"
  - "[[Process States - Ready Running and Blocked]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[A Process is a Running Program]]"
  - "[[Direct Execution Runs Programs Directly on the CPU]]"
---

# User Mode and Kernel Mode Provide Dual Protection Levels

> [!SUMMARY]
> The CPU provides two privilege levels: user mode (restricted) and kernel mode (unrestricted). User programs execute in user mode and cannot perform privileged operations like I/O or modifying trap tables. The OS kernel runs in kernel mode with full hardware access. This hardware-enforced boundary is the foundation of safe CPU virtualization.

## The Protection Problem

If programs run directly on the CPU with full privileges, nothing prevents them from reading other processes' memory, writing directly to disk, or disabling interrupts. The OS needs hardware support to restrict what user programs can do while still allowing them to run at native speed.

## Processor Modes

The hardware provides (at minimum) two execution modes indicated by a **mode bit** in a processor status register:

**User mode** — Code running in user mode is restricted. If a user-mode process attempts a privileged operation (such as issuing an I/O request, modifying page table base registers, or disabling interrupts), the processor raises an exception and the OS kills the offending process. Application code always runs in user mode.

**Kernel mode** — Code running in kernel mode can execute any instruction the hardware supports. This includes privileged operations like configuring memory mappings, setting up trap handlers, and accessing device registers. Only the operating system runs in kernel mode.

## Crossing the Boundary

A user program that needs to perform a privileged operation (reading a file, allocating memory, sending a network packet) must request the OS to do it on its behalf. The mechanism for this is the **system call**: the program executes a special **trap** instruction that simultaneously switches the mode bit to kernel mode and jumps to a pre-defined OS entry point.

The key security insight is that the user program cannot jump to *arbitrary* kernel code. The hardware consults a **trap table** (set up at boot time by the OS) that maps trap numbers to specific handler addresses. The user program can only request services the OS has explicitly exposed — it cannot execute arbitrary privileged instructions.

## Why Two Modes Suffice

This dual-mode approach creates a clean separation:

- User code runs at full speed for unprivileged computation
- Privileged operations require a controlled, audited transition to the kernel
- The OS retains authority over all hardware resources

Some architectures provide more than two modes (x86 has rings 0-3), but the fundamental user/kernel split remains the essential boundary for OS protection. Without hardware mode support, safe multiprogramming would require interpreting every user instruction — sacrificing the performance that direct execution provides.
