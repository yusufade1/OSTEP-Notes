---
type: mechanism
source: "OSTEP Ch. 36: I/O Devices"
tags:
  - persistence
  - io
  - interface
  - registers
related:
  - "[[IO Architecture Connects CPU Memory and Devices via Bus Hierarchy]]"
  - "[[Polling and Interrupts Trade CPU Cycles for Responsiveness]]"
  - "[[Direct Execution Runs Programs Directly on the CPU]]"
prerequisites:
  - "[[IO Architecture Connects CPU Memory and Devices via Bus Hierarchy]]"
---

> [!SUMMARY]
> The device interface is the standard mechanism by which the operating system controls hardware, utilizing a set of registers for status, commands, and data. This interface abstracts the internal complexity of the device, allowing the OS to perform operations through a defined protocol of reading and writing these registers.

# The Canonical Device Interface

To interact with the diverse array of hardware connected to the system, the operating system relies on a **canonical device interface**. Regardless of whether the device is a simple mouse or a complex solid-state drive, it exposes a set of hardware registers that the OS can read and write. These registers typically fall into three categories:

1.  **Status Register:** Indicates the current state of the device (e.g., busy, ready, error).
2.  **Command Register:** Accepts instructions from the OS (e.g., read, write, seek).
3.  **Data Register:** Used to pass data to the device or retrieve data from it.

This register-based interface serves as a contract between the software and the hardware. The OS does not need to know how the device physically spins a disk or fires a laser; it only needs to know which values to write to these registers to trigger those actions.

# The Interaction Protocol

The interaction between the OS and the device usually follows a specific protocol, often referred to as **Programmed I/O (PIO)** when the CPU is directly involved in moving data. A typical protocol for a write operation might look like this:

1.  **Polling:** The OS reads the status register repeatedly, waiting for the `BUSY` bit to clear. This ensures the device is ready to accept a new command.
2.  **Sending Data:** Once the device is ready, the OS writes data to the data register. If the transfer is large, this might happen in chunks.
3.  **Sending Command:** The OS writes a "write" command to the command register. This signals the device to begin the actual operation.
4.  **Execution:** The device sets its `BUSY` status and processes the request. The OS may then return to step 1 to wait for completion.

# Memory-Mapped I/O vs. Explicit Instructions

How the OS accesses these registers depends on the architecture. Some systems use explicit **I/O instructions** (like `in` and `out` on x86), which specify a dedicated I/O port address. Others use **memory-mapped I/O**, where the device registers are mapped into the physical address space of the system. In memory-mapped systems, the OS simply uses standard load and store instructions (like `mov` in Assembly or pointer dereferencing in C) to talk to the device. The hardware memory controller intercepts these specific addresses and routes the traffic to the device bus instead of main memory.
