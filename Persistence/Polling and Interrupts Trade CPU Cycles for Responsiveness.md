---
type: mechanism
source: "OSTEP Ch. 36: I/O Devices"
tags:
  - persistence
  - io
  - interrupts
  - polling
  - efficiency
related:
  - "[[Device Interface Exposes Registers for Status Command and Data]]"
  - "[[Context Switch Saves and Restores Process State]]"
  - "[[Timer Interrupts Enable Preemptive Multitasking]]"
  - "[[DMA Offloads Data Transfer Tasks from the Main CPU]]"
prerequisites:
  - "[[Device Interface Exposes Registers for Status Command and Data]]"
---

> [!SUMMARY]
> The choice between polling and interrupts represents a fundamental trade-off in I/O management: polling is simple but wastes CPU cycles waiting for slow devices, while interrupts allow for overlap of computation and I/O but introduce context switching overhead. Modern systems often employ hybrid approaches to balance responsiveness and efficiency.

# The Cost of Polling

**Polling** is the simplest method for an operating system to check if a device has completed a task. The OS repeatedly reads the device's status register—looping until the device indicates it is "ready." While easy to implement, polling is notoriously inefficient for slow devices.

Consider a disk drive that takes 10 milliseconds to complete a read. For a modern CPU running at 3 GHz, 10 milliseconds represents 30 million clock cycles. If the CPU spends that time just spinning in a `while` loop checking a status bit, it effectively wastes an enormous amount of computing power that could have been used to run other processes.

# The Interrupt Solution

**Interrupts** solve this problem by allowing the CPU to perform other work while the device is busy. Instead of polling, the OS issues a command to the device and then puts the calling process to sleep (blocking it). The OS then performs a **context switch** to run a different process.

When the device finally finishes its task, it raises a hardware interrupt signal. This signal pauses the CPU's current execution and forces it to jump to a pre-defined **interrupt service routine (ISR)** or interrupt handler. The ISR processes the device completion (e.g., checks for errors), wakes up the original process, and potentially schedules it to run again.

This "overlap" of computation (running process B) and I/O (device working for process A) significantly improves **system utilization**.

# The Trade-offs and Livelock

However, interrupts are not always superior. Handling an interrupt involves significant overhead: saving the current context, switching to kernel mode, executing the handler, and restoring context. If a device is extremely fast (e.g., a high-speed network card receiving thousands of small packets per second), the CPU might spend 100% of its time processing interrupts and never make progress on user-level code. This condition is known as **livelock**.

To mitigate this, high-performance systems often use a **hybrid approach**. The OS might poll for a short period to catch quick completions; if the device takes too long, it switches to interrupts. Alternatively, under high load, an OS might temporarily disable interrupts and switch to polling (coalescing) to process events in batches, avoiding the per-event context switch cost.
