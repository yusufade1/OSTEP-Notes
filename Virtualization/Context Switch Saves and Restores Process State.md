---
type: mechanism
source: "OSTEP Ch. 6: Mechanism: Limited Direct Execution"
tags:
  - virtualization
  - mechanisms
  - context-switch
  - scheduling
related:
  - "[[Timer Interrupts Enable Preemptive Multitasking]]"
  - "[[Context Switches Require TLB Flush or ASID Tagging]]"
  - "[[Process Data Structures - PCB Registers and Memory Image]]"
  - "[[Process States - Ready Running and Blocked]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Timer Interrupts Enable Preemptive Multitasking]]"
  - "[[Process Data Structures - PCB Registers and Memory Image]]"
---

# Context Switch Saves and Restores Process State

> [!SUMMARY]
> A context switch is the OS mechanism for stopping one process and starting another. The OS saves the current process's register state into its process control block (PCB), then restores the next process's saved state. This low-level, performance-critical code is typically written in assembly and executes in the kernel after a timer interrupt or blocking system call.

## Two Levels of Register Saving

A context switch involves **two distinct** register save/restore operations, which is often confusing:

1. **Hardware saves user registers** onto the kernel stack when the timer interrupt fires (trap mechanism)
2. **OS saves kernel registers** from the current process's kernel stack into its PCB, then restores the next process's kernel registers from its PCB

The first is done by hardware automatically (as with any trap). The second is the actual context switch, done explicitly by the OS in software.

## The Context Switch in Assembly

The xv6 operating system implements context switching with a dedicated assembly routine. The key operation saves callee-saved registers of the current process and restores those of the next:

```asm
# void swtch(struct context **old, struct context *new);
# Save current registers in old context,
# then load registers from new context.
swtch:
    # Save old callee-saved registers
    movl %ebx, 0(%eax)
    movl %esi, 4(%eax)
    movl %edi, 8(%eax)
    movl %ebp, 12(%eax)
    movl %esp, 16(%eax)

    # Load new callee-saved registers
    movl 0(%edx), %ebx
    movl 4(%edx), %esi
    movl 8(%edx), %edi
    movl 12(%edx), %ebp
    movl 16(%edx), %esp
    ret
```

By switching the **stack pointer** (`%esp`), the `ret` instruction pops the return address from the *new* process's stack — effectively jumping into that process's execution context.

## Complete Sequence

When process A is running and the OS decides to switch to process B:

1. Timer interrupt fires → hardware saves A's user registers onto A's kernel stack
2. Hardware enters kernel mode, jumps to timer handler
3. OS scheduler decides to switch from A to B
4. OS calls `swtch(&A->context, B->context)`:
   - Saves A's kernel registers into A's PCB
   - Restores B's kernel registers from B's PCB
   - Stack pointer now points to B's kernel stack
5. OS returns from B's trap frame → hardware restores B's user registers
6. Process B resumes in user mode where it left off

## Performance Cost

Context switches are pure overhead — neither process makes useful progress during the switch. The cost includes saving/restoring registers (fast), flushing TLB entries and CPU caches (slower), and pipeline stalls. On commodity hardware, a context switch costs roughly 1-10 microseconds of direct overhead, plus indirect costs from cold caches.

## When Context Switches Occur

The OS performs a context switch when:
- A timer interrupt fires and the scheduler picks a different process
- The running process blocks on I/O (transitions to **blocked** state)
- The running process calls `yield()` voluntarily
- The running process exits
