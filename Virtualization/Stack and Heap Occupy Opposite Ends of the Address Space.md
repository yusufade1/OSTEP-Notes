---
type: atomic
source: OSTEP Ch. 13
tags:
  - virtualization
  - memory
  - address-space
related:
  - "[[The Address Space Abstracts Physical Memory for Each Process]]"
  - "[[malloc and free Manage Heap Memory Dynamically]]"
  - "[[Process Data Structures - PCB Registers and Memory Image]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The Address Space Abstracts Physical Memory for Each Process]]"
---

# Stack and Heap Occupy Opposite Ends of the Address Space

> [!SUMMARY]
> The canonical address space layout places the code segment at the bottom, the heap growing upward above it, and the stack growing downward from the top. This opposing-growth convention maximizes the available space for both dynamically-sized regions without requiring the OS to predict their final sizes at process creation.

## The Canonical Layout

A typical address space is arranged as follows (addresses increase upward):

```
  ┌─────────────────┐  ← Max (e.g., 16 KB)
  │      Stack      │  grows downward ↓
  │        ↓        │
  │                 │
  │   (free space)  │
  │                 │
  │        ↑        │
  │       Heap      │  grows upward ↑
  ├─────────────────┤
  │   Code (Text)   │  static, read-only
  └─────────────────┘  ← Address 0
```

- **Code segment** occupies the lowest addresses. It is loaded from the executable and remains fixed in size throughout the process's lifetime.
- **Heap** begins just above the code and grows toward higher addresses as the program calls `malloc()`.
- **Stack** starts at the top of the address space and grows toward lower addresses as functions are called and local variables are allocated.

## Why Opposing Growth

The key insight is that both heap and stack sizes are unpredictable at compile time. A program might allocate megabytes of heap data with few function calls, or recurse deeply while barely touching the heap. By placing them at opposite ends growing toward each other, the OS avoids committing to a fixed division—each region can independently claim free space from the shared gap between them.

If both grew in the same direction, one would need a hard size limit that might waste memory or cause premature out-of-memory errors.

## Stack: Implicit and Automatic

The stack is managed automatically by the compiler and hardware—part of the [[Process Data Structures - PCB Registers and Memory Image|machine state]] tracked by the OS. Each function call pushes a **stack frame** containing:

- Return address (where to resume after the function returns)
- Saved registers
- Local variables
- Function arguments

The stack pointer register tracks the current top. Allocation is a single pointer decrement; deallocation is a pointer increment on function return. This makes stack allocation extremely fast—no bookkeeping needed.

## Heap: Explicit and Manual

Unlike the stack, the heap requires explicit management. The programmer calls [[malloc and free Manage Heap Memory Dynamically|malloc]] to request memory and `free()` to release it. The heap can grow arbitrarily (up to available virtual address space), but fragmentation and bugs make it harder to manage. The OS expands the heap via system calls like `brk()` or `sbrk()` when the allocator needs more space.

## When the Gap Disappears

If the stack and heap grow toward each other until they meet, the process has exhausted its address space. In practice, modern 64-bit address spaces are so large (2^48 bytes) that this collision is unlikely. On smaller 32-bit systems, a 4 GB address space could be exhausted by memory-hungry applications, resulting in stack overflow or failed `malloc()` calls.
