---
type: atomic
source: OSTEP Ch. 6
tags:
  - virtualization
  - mechanisms
  - system-calls
  - traps
related:
  - "[[User Mode and Kernel Mode Provide Dual Protection Levels]]"
  - "[[Direct Execution Runs Programs Directly on the CPU]]"
  - "[[Process Data Structures - PCB Registers and Memory Image]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[User Mode and Kernel Mode Provide Dual Protection Levels]]"
---

# System Calls Transfer Control via Trap and Return-from-Trap

> [!SUMMARY]
> System calls use a hardware trap mechanism to safely transition from user mode to kernel mode. The user program executes a trap instruction, which saves state on a kernel stack, switches to kernel mode, and jumps to a handler specified in the OS-configured trap table. After servicing the request, return-from-trap restores user state and resumes execution.

## The Trap Table

At boot time (in kernel mode), the OS initializes the **trap table** — a data structure that tells the hardware what code to run for each type of exceptional event. Each entry maps a trap number (system call number, interrupt vector, or exception type) to a handler address:

```c
// OS boot-time setup (privileged)
void os_boot() {
    // Tell hardware where trap handlers are
    set_trap_handler(SYSCALL_TRAP, &syscall_handler);
    set_trap_handler(TIMER_INTERRUPT, &timer_handler);
    set_trap_handler(ILLEGAL_INSTRUCTION, &exception_handler);
    // ... other entries
}
```

This setup is a privileged operation — user programs cannot modify the trap table. The hardware remembers these handler locations until the next boot, ensuring that traps always land in OS-controlled code.

## The Trap Sequence

When a user program needs a kernel service (e.g., `read()`, `write()`, `fork()`), it places the system call number in a designated register and executes a **trap instruction** (e.g., `int 0x80` on x86, `syscall` on x86-64). The hardware then:

1. Saves the user program's registers (PC, flags, stack pointer) onto the process's **kernel stack**
2. Switches the mode bit to **kernel mode**
3. Jumps to the trap handler address from the trap table

The OS trap handler examines the system call number, validates arguments, performs the requested operation, and stores the return value in a register.

## Return-from-Trap

After the system call completes, the OS executes a **return-from-trap** instruction (e.g., `iret` on x86, `sysret` on x86-64). The hardware then:

1. Restores the saved registers from the kernel stack
2. Switches the mode bit back to **user mode**
3. Jumps back to the instruction after the original trap

The user program resumes as if a normal function returned, finding the system call result in the designated return register.

## The Kernel Stack

Each process has its own **kernel stack**, separate from its user-mode stack. This per-process kernel stack is where the hardware saves registers during a trap and where the kernel itself allocates local variables during system call processing. Having a separate kernel stack per process means the OS can handle traps from any process without corrupting another process's state.

## Security Guarantee

The trap mechanism ensures that user programs can *request* kernel services but cannot *execute* arbitrary kernel code. The indirection through the trap table — set up by the OS at boot — means user code only ever enters the kernel at well-defined, audited entry points.
