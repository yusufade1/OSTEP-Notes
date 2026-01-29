---
type: mechanism
source: "OSTEP Ch. 36: I/O Devices"
tags:
  - persistence
  - io
  - dma
  - performance
related:
  - "[[Polling and Interrupts Trade CPU Cycles for Responsiveness]]"
  - "[[Device Interface Exposes Registers for Status Command and Data]]"
  - "[[Direct Execution Runs Programs Directly on the CPU]]"
prerequisites:
  - "[[Polling and Interrupts Trade CPU Cycles for Responsiveness]]"
---

> [!SUMMARY]
> Direct Memory Access (DMA) is a hardware optimization that allows specific I/O devices to transfer data directly to and from main memory without continuous CPU intervention. By offloading the burden of data copying from the main processor, DMA significantly enhances system concurrency and overall performance.

# The Problem with Programmed I/O (PIO)

In a basic I/O system using **Programmed I/O (PIO)**, the CPU is responsible for every single byte of data transferred. To write a 4KB block to a disk, the CPU must run a loop that reads a word from memory and writes it to the device's data register, repeating this thousands of times.

Even if the system uses interrupts to avoid polling the status register, the CPU is still fully occupied during the actual data movement phase. This "copy overhead" prevents the CPU from performing other useful work during heavy I/O operations, limiting the parallelism achievable by the OS.

# The DMA Engine Solution

**Direct Memory Access (DMA)** solves this by introducing a specialized piece of hardware: the DMA engine (or controller). The DMA engine is essentially a very simple, single-purpose processor designed solely to copy memory.

With DMA, the interaction changes:
1.  The OS programs the DMA engine, telling it **where** the data is in memory, **how much** data to copy, and **which device** to send it to.
2.  The OS issues the command to the device and then yields the CPU to other processes.
3.  The DMA engine handles the tedious task of moving bytes between memory and the device controller.
4.  When the transfer is complete, the DMA engine raises an interrupt to notify the OS.

# Increasing Concurrency

The primary benefit of DMA is the **overlap of execution and data transfer**. While the DMA engine is busy copying a large file to the network card or reading from the disk, the main CPU is free to execute other runnable processes. The CPU is only interrupted once—when the entire transaction is finished—rather than being tied up for the duration of the transfer.

This mechanism is crucial for high-throughput systems. Without DMA, a high-speed network link or SSD could easily saturate the CPU just by moving data, leaving no cycles left to actually process that data (e.g., parsing a web request or querying a database). DMA ensures the CPU is reserved for computation, while specialized hardware handles the plumbing of moving bits.
