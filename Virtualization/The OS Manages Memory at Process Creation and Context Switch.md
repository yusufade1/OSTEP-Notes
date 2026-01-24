---
type: atomic
source: OSTEP Ch. 15
tags:
  - virtualization
  - memory
  - os-role
  - free-list
related:
  - "[[Base-and-Bounds Provides Dynamic Relocation]]"
  - "[[Hardware Registers Enable Efficient Address Translation]]"
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[Process Data Structures - PCB Registers and Memory Image]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Hardware Registers Enable Efficient Address Translation]]"
---

# The OS Manages Memory at Process Creation and Context Switch

> [!SUMMARY]
> While the hardware performs address translation on every memory access, the OS is responsible for managing the translation parameters. The OS must find free physical memory for new processes, save and restore base/bounds registers during context switches, handle exception faults when processes violate their bounds, and reclaim memory when processes terminate. A free list data structure tracks which physical regions are available.

## OS Responsibilities

The hardware provides the base-and-bounds translation mechanism, but the OS must manage it at four critical points in a process's lifecycle:

### 1. Process Creation: Finding Free Memory

When a new process is created, the OS must find a contiguous region of physical memory large enough to hold its address space. The OS maintains a **free list**—a data structure tracking which ranges of physical memory are unoccupied.

```c
// Simplified free list allocation
struct free_region {
    uint32_t start;   // physical start address
    uint32_t size;    // size in bytes
    struct free_region *next;
};

// OS searches for a region >= process address space size
region = find_free_region(address_space_size);
new_process->base = region->start;
new_process->bounds = address_space_size;
```

The OS allocates a region from the free list, records the base and bounds in the [[Process Data Structures - PCB Registers and Memory Image|process control block (PCB)]], and loads the process's code and data into that physical region.

### 2. Context Switch: Save and Restore

When the OS [[Context Switch Saves and Restores Process State|switches]] from process A to process B, it must:

1. **Save** process A's current base/bounds register values into A's PCB.
2. **Load** process B's base/bounds values from B's PCB into the hardware registers.

This save/restore happens alongside the general-purpose register save/restore that already occurs during a context switch. The per-process base/bounds values stored in the PCB define where each process's address space physically resides.

### 3. Exception Handling: Bounds Violations

When the hardware detects that a virtual address exceeds the bounds register, it raises a protection fault and transfers control to the OS's exception handler. The OS response is typically to terminate the offending process—the famous "segmentation fault" originates from this class of bounds violation.

The OS installs exception handlers at boot time (via the [[System Calls Transfer Control via Trap and Return-from-Trap|trap table]]) so the hardware knows where to jump on a fault.

### 4. Process Termination: Reclaiming Memory

When a process exits or is killed, the OS must return its physical memory region to the free list. This involves adding the region (identified by the process's base and bounds from its PCB) back to the free list data structure, making it available for future process creation.

## The Free List

The free list is a simple but critical data structure. In a base-and-bounds system, it tracks variable-sized contiguous regions of physical memory. As processes are created and destroyed, the free list becomes fragmented—free regions may not be adjacent. The OS may need to compact memory (relocating processes by updating their base registers) to create larger contiguous regions, though compaction is expensive and rarely done in practice.

## The OS/Hardware Division

| Responsibility | Who |
|---------------|-----|
| Translation on every memory access | Hardware (MMU) |
| Bounds checking on every access | Hardware |
| Setting up base/bounds at creation | OS |
| Saving/restoring at context switch | OS |
| Handling protection faults | OS |
| Maintaining the free list | OS |
| Reclaiming memory at termination | OS |

This division—hardware handles the fast path (every access), OS handles the slow path (lifecycle events)—is the recurring pattern in all memory virtualization mechanisms.
