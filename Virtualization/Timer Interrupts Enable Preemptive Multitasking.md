---
type: atomic
source: OSTEP Ch. 6
tags:
  - virtualization
  - mechanisms
  - interrupts
  - preemption
related:
  - "[[Direct Execution Runs Programs Directly on the CPU]]"
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[Process States - Ready Running and Blocked]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[System Calls Transfer Control via Trap and Return-from-Trap]]"
  - "[[User Mode and Kernel Mode Provide Dual Protection Levels]]"
---

# Timer Interrupts Enable Preemptive Multitasking

> [!SUMMARY]
> A timer interrupt is a hardware mechanism that fires periodically to transfer control from user programs back to the OS. Without it, a non-cooperative process (infinite loop, buggy code) could monopolize the CPU forever. The timer interrupt makes scheduling preemptive — the OS can forcibly stop any process and switch to another regardless of what the process is doing.

## The Non-Cooperative Problem

In a **cooperative** approach, the OS trusts processes to periodically give up the CPU through system calls or explicit `yield()` calls. This fails when a program enters an infinite loop or simply never makes a system call — the OS never runs and cannot switch to another process. The only recovery is a reboot.

## Timer Interrupt Solution

The hardware includes a **timer device** that can be programmed to raise an interrupt at a fixed interval (e.g., every few milliseconds). At boot time, the OS:

1. Configures the timer interval
2. Installs a **timer interrupt handler** in the trap table
3. Starts the timer

Once started, the timer fires regardless of what user code is executing. When the interrupt fires, the hardware performs the same sequence as a trap: save current registers to the kernel stack, switch to kernel mode, and jump to the timer interrupt handler. The currently running process is **forcibly suspended** mid-instruction.

## Cooperative vs. Preemptive Scheduling

| Approach | OS regains control via | Failure mode |
|---|---|---|
| Cooperative | System calls, yield | Infinite loop hangs system |
| Preemptive | Timer interrupts | None — OS always regains control |

All general-purpose operating systems use preemptive scheduling via timer interrupts. The cooperative approach appears only in specialized embedded systems where all code is trusted.

## What Happens on Timer Interrupt

When the timer fires during user code execution:

1. Hardware saves user registers onto the process's kernel stack
2. Hardware switches to kernel mode
3. Hardware jumps to the timer interrupt handler
4. The OS **scheduler** decides: resume the current process, or switch to a different one?
5. If switching, the OS performs a [[Context Switch Saves and Restores Process State|context switch]]
6. The selected process resumes via return-from-trap

The decision in step 4 is the **scheduling policy** — a separate concern from the timer mechanism itself. The timer merely *guarantees* the OS gets to make that decision regularly.

## Concurrency Concerns

What if an interrupt arrives while the OS is handling a system call or another interrupt? Operating systems handle this by **disabling interrupts** during critical sections of interrupt processing. While interrupts are disabled, no further timer interrupts can preempt the handler. This must be done carefully — disabling interrupts for too long causes missed events and poor responsiveness.
