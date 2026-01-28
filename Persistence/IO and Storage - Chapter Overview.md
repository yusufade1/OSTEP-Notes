---
type: overview
source: OSTEP Ch. 36
tags: [persistence, io, chapter-overview]
related: 
  - [[IO Architecture Connects CPU Memory and Devices via Bus Hierarchy]]
  - [[Device Interface Exposes Registers for Status Command and Data]]
  - [[Polling and Interrupts Trade CPU Cycles for Responsiveness]]
  - [[DMA Offloads Data Transfer Tasks from the Main CPU]]
  - [[Device Drivers Abstract Hardware Details from the OS]]
prerequisites:
  - [[System Calls Transfer Control via Trap and Return-from-Trap]]
---

> [!SUMMARY]
> This chapter introduces the fundamental mechanisms of Input/Output (I/O) systems, exploring how the operating system communicates with and manages the diverse array of hardware peripherals that make computers useful.

# Core Concepts

The I/O subsystem is the bridge between the purely digital world of the CPU/memory and the physical world of interfaces and storage.

*   **[[IO Architecture Connects CPU Memory and Devices via Bus Hierarchy]]**: Understanding how devices are physically connected to the system via memory, I/O, and peripheral buses.
*   **[[Device Interface Exposes Registers for Status Command and Data]]**: The canonical protocol (Status, Command, Data) used to control hardware registers.
*   **[[Device Drivers Abstract Hardware Details from the OS]]**: How software encapsulates hardware complexity to keep the OS kernel generic.

# Mechanisms for Efficiency

A major theme in I/O is performance—specifically, how to interact with slow devices without stalling the fast CPU.

*   **[[Polling and Interrupts Trade CPU Cycles for Responsiveness]]**: The choice between checking device status continuously (polling) or letting the device notify the CPU when done (interrupts).
*   **[[DMA Offloads Data Transfer Tasks from the Main CPU]]**: A hardware optimization that allows data to move between devices and memory without constant CPU supervision, enabling true concurrency between processing and I/O.
