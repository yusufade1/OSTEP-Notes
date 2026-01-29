---
type: concept
source: "OSTEP Ch. 13: The Abstraction: Address Spaces"
tags:
  - virtualization
  - memory
  - abstraction
related:
  - "[[A Process is a Running Program]]"
  - "[[File Systems - Chapter Overview]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[Stack and Heap Occupy Opposite Ends of the Address Space]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[A Process is a Running Program]]"
---

# The Address Space Abstracts Physical Memory for Each Process

> [!SUMMARY]
> The address space is the OS's abstraction of physical memory for a running process. Each process believes it owns a large, contiguous block of memory starting at address 0, containing its code, stack, and heap. In reality, the OS maps these virtual addresses to arbitrary physical locations, enabling multiple processes to share memory safely and conveniently.

## From Bare Metal to Abstraction

Early computers ran one program at a time with direct access to physical memory. As multiprogramming emerged—multiple processes resident in memory simultaneously—the OS needed a way to isolate them from each other and from itself. Leaving processes unprotected in a shared physical space invited corruption: one errant write could crash another process or the OS kernel.

The solution was the **address space**: a virtual view of memory private to each process. Rather than exposing raw physical addresses, the OS presents each process with its own logical address range, typically starting at 0 and extending to some maximum (e.g., 16 KB in a simple example, or 2^48 bytes on modern 64-bit systems).

## Structure of the Address Space

A typical address space contains three logical segments:

- **Code (text):** The program's instructions, loaded from the executable. Placed at low addresses. Static and read-only after loading.
- **Heap:** Dynamically allocated memory (via [[malloc and free Manage Heap Memory Dynamically|malloc]]), growing downward from just after the code segment toward higher addresses.
- **Stack:** Holds local variables, function arguments, and return addresses. Placed at the high end of the address space, growing upward toward lower addresses.

This layout is a **convention**, not a hardware requirement. The OS and compiler collaborate to arrange these regions so they can grow independently without colliding—the heap grows up, the stack grows down, and the unused gap between them represents available space.

## The Virtualization Illusion

When a process executes `load 0x1000`, it is referencing a **virtual address**. The hardware and OS collaborate to translate this to the actual physical address where the data resides. The process never knows—and never needs to know—where in physical RAM its data actually lives. This property is called **transparency**: the virtualization is invisible to the running program.

The address space abstraction is what makes it possible for multiple processes to coexist in memory without interfering with each other. Each believes it has the whole machine to itself, while the OS quietly multiplexes physical memory among them all.

## Connection to CPU Virtualization

Just as the OS virtualizes the CPU through [[Context Switch Saves and Restores Process State|context switching]] (giving each process the illusion of its own processor), it virtualizes memory through address spaces (giving each process the illusion of its own memory). Together, these abstractions let the OS run many programs concurrently on limited hardware resources.
