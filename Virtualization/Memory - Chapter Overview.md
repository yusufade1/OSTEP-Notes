---
type: overview
source: OSTEP Ch. 13-14
tags:
  - virtualization
  - memory
related:
  - "[[Virtualization MOC]]"
  - "[[The Address Space Abstracts Physical Memory for Each Process]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[Stack and Heap Occupy Opposite Ends of the Address Space]]"
  - "[[malloc and free Manage Heap Memory Dynamically]]"
  - "[[Common Memory Bugs - Dangling Pointers Double Free and Leaks]]"
---

# Memory - Chapter Overview

These chapters introduce **memory virtualization**: the OS gives each process the illusion of its own large, private address space, while actually sharing limited physical memory among all running processes. The abstraction (address space), its goals, and the programmer-facing API (malloc/free) form the conceptual foundation before diving into hardware mechanisms.

## Key Concepts

- **[[The Address Space Abstracts Physical Memory for Each Process]]** — Each process sees a contiguous address space from 0 to max, containing code, stack, and heap, even though physical memory is shared.
- **[[Memory Virtualization Goals - Transparency Efficiency and Protection]]** — The OS must virtualize memory transparently, efficiently (via hardware TLBs/page tables), and with isolation between processes.
- **[[Stack and Heap Occupy Opposite Ends of the Address Space]]** — The stack grows downward from the top and the heap grows upward from after the code segment, maximizing usable space.
- **[[malloc and free Manage Heap Memory Dynamically]]** — The C library provides malloc/free for explicit heap management, built on top of OS system calls like brk and mmap.
- **[[Common Memory Bugs - Dangling Pointers Double Free and Leaks]]** — Manual memory management introduces bug classes that are difficult to detect: use-after-free, double-free, leaks, and buffer overflows.

## Chapter Questions

1. Why does the OS not simply let processes use physical memory directly?
2. What three goals must memory virtualization achieve simultaneously?
3. Why does the address space place stack and heap at opposite ends?
4. What system calls does malloc ultimately rely on to get memory from the OS?
5. Which memory bugs can crash a program immediately vs. silently corrupt data?
