---
type: mechanism
source: "OSTEP Ch. 15: Mechanism: Address Translation"
tags:
  - virtualization
  - memory
  - hardware
  - MMU
related:
  - "[[Address Translation Maps Virtual Addresses to Physical Addresses]]"
  - "[[Base-and-Bounds Provides Dynamic Relocation]]"
  - "[[The OS Manages Memory at Process Creation and Context Switch]]"
  - "[[User Mode and Kernel Mode Provide Dual Protection Levels]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Base-and-Bounds Provides Dynamic Relocation]]"
---

# Hardware Registers Enable Efficient Address Translation

> [!SUMMARY]
> The CPU's Memory Management Unit (MMU) contains privileged registers—base and bounds—that perform address translation on every memory reference without slowing down program execution. These registers are accessible only in kernel mode, ensuring that user processes cannot tamper with their own translations. The hardware also raises exceptions when bounds are violated, transferring control to the OS for handling.

## The Memory Management Unit

The portion of the CPU responsible for address translation is called the **Memory Management Unit (MMU)**. In the simplest dynamic relocation scheme, the MMU contains just two registers:

| Register | Purpose |
|----------|---------|
| **Base** | Added to every virtual address to produce the physical address |
| **Bounds** | Maximum legal virtual address (or equivalently, address space size) |

These are **per-CPU registers**, meaning each processor core has its own pair. When the OS [[Context Switch Saves and Restores Process State|context switches]] between processes, it loads the new process's base and bounds values into these registers.

## Privileged Access

The base and bounds registers are **privileged**: only code running in [[User Mode and Kernel Mode Provide Dual Protection Levels|kernel mode]] can read or write them. If a user-mode process could modify its own base register, it could point it at any physical address—accessing other processes' memory or the kernel itself. The privilege restriction is enforced by the hardware: any attempt to execute a privileged register instruction in user mode raises an exception.

This mirrors the pattern seen throughout OS design—the hardware provides the enforcement mechanism, while the OS provides the policy (which base/bounds values each process gets).

## Hardware Requirements for Dynamic Relocation

The hardware must provide several capabilities to support base-and-bounds translation:

1. **Privileged mode:** A kernel/user mode bit that determines whether privileged instructions can execute.
2. **Base/bounds registers:** Storage for the translation parameters, accessible only in kernel mode.
3. **Translation and checking:** On every memory reference, the hardware adds the base and compares against bounds—both operations happen in the same cycle, adding no latency to the memory access.
4. **Privileged register instructions:** Special instructions (e.g., `mfbase`, `mtbase` on some architectures) to read/write base and bounds.
5. **Exception mechanism:** When a bounds violation occurs, the hardware raises a fault. The CPU saves the offending PC and transfers control to a kernel exception handler at a predetermined address (registered at boot via a [[System Calls Transfer Control via Trap and Return-from-Trap|trap table]]).
6. **Exception on user privilege violation:** If user code attempts to modify base/bounds, the hardware traps to the OS.

## Translation Timing

The translation occurs in the CPU pipeline's **memory stage**—after the effective address is computed but before the actual memory access. This means:

- The ALU computes the virtual address (e.g., register + offset).
- The MMU adds the base and checks bounds in parallel.
- If valid, the physical address is sent to the cache/memory hierarchy.
- If invalid, a fault is raised before the access completes.

This pipelining ensures that address translation adds **zero additional cycles** in the common (valid) case, satisfying the [[Memory Virtualization Goals - Transparency Efficiency and Protection|efficiency goal]] of memory virtualization.
