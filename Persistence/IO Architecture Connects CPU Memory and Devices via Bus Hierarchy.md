---
type: atomic
source: OSTEP Ch. 36
tags: [persistence, io, architecture, hardware]
related: 
  - [[Device Interface Exposes Registers for Status Command and Data]]
  - [[Direct Execution Runs Programs Directly on the CPU]]
prerequisites:
  - [[System Calls Transfer Control via Trap and Return-from-Trap]]
---

> [!SUMMARY]
> I/O architecture is structured hierarchically to balance performance and cost, connecting the CPU and main memory to various input/output devices through a system of buses. High-performance devices reside on faster buses closer to the CPU, while slower peripherals are connected via lower-performance expansion buses.

# The Hierarchical Bus Structure

Modern computing systems are not designed as a flat network where all components communicate at equal speeds. Instead, they employ a **hierarchical bus structure** that reflects the fundamental physics of data transmission: faster signals require shorter distances and more expensive engineering. This hierarchy organizes the flow of data between the central processing unit (CPU), main memory, and the vast array of I/O devices.

At the top of this hierarchy is the **memory bus**, a specialized, high-speed pathway connecting the CPU directly to the system's DRAM. This bus is designed for maximum bandwidth and low latency, as the CPU fetches instructions and data from memory constantly.

Below the memory bus, systems typically feature a general-purpose **I/O bus**, such as PCI (Peripheral Component Interconnect) or its modern successor, PCIe (PCI Express). This bus connects high-performance devices—like graphics cards and high-speed network interfaces—that require significant throughput but do not need the ultra-low latency of the main memory bus.

Finally, at the bottom of the hierarchy is the **peripheral bus**, such as SCSI, SATA, or USB. These buses connect slower devices like hard disks, mice, and keyboards. They are often longer cables that allow devices to be plugged in externally or positioned further from the motherboard's core logic.

# The Physics of Cost and Performance

The primary reason for this tiered architecture is the trade-off between performance and cost. A bus that can run at extremely high frequencies (like the memory bus) must be physically short and constructed with high-precision materials to maintain signal integrity. As the bus gets longer to accommodate more devices, signal degradation and capacitance prevent high-speed operation.

Therefore, system architects create a compromise: a short, fast bus for the most critical components (CPU and RAM) and longer, slower buses for peripherals. This design allows a system to support a wide variety of devices—from fast GPUs to slow keyboards—without forcing every component to adhere to the rigorous (and expensive) constraints of the memory bus.

The CPU interacts with these devices through **I/O instructions** (like x86 `in` and `out`) or **memory-mapped I/O**, where device registers are mapped to specific physical memory addresses. In either case, the hierarchical structure determines the path and potential bottleneck for every byte of data entering or leaving the system.
