---
type: overview
source: "OSTEP Ch. 44: Flash-based SSDs"
tags:
  - persistence
  - ssd
  - flash
  - chapter-overview
related:
  - "[[Persistence MOC]]"
  - "[[IO and Storage - Chapter Overview]]"
  - "[[Log-Structured File Systems - Chapter Overview]]"
prerequisites:
  - "[[IO and Storage - Chapter Overview]]"
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
---

# Flash-Based SSDs - Chapter Overview

> [!SUMMARY]
> Flash-based Solid State Drives (SSDs) provide high-performance, semiconductor-based storage as an alternative to mechanical hard disks. While they offer massive improvements in random I/O latency, SSDs introduce unique hardware constraints, including a limited number of write cycles and the requirement that memory must be erased in large blocks before it can be rewritten.

## The Nature of Flash Memory
Flash memory differs fundamentally from magnetic disks in its physical operations.
*   **[[Flash Memory Basics - Pages Blocks and Erasure Asymmetry]]:** The core constraints of flash—reading and writing in pages, but erasing in blocks—and why "update-in-place" is impossible.

## The Flash Translation Layer (FTL)
To make SSDs compatible with existing operating systems, they include a complex firmware layer.
*   **[[The Flash Translation Layer Manages SSD Mapping and Wear]]:** How the FTL uses a log-structured approach to map logical blocks to physical flash pages while hiding the underlying erasure requirements.

## Performance and Longevity
The management of flash cells directly impacts the drive's speed and its lifespan.
*   **[[SSD Performance Characteristics and Wear Leveling]]:** Why SSDs excel at reads but face write amplification, and how the drive ensures longevity by distributing writes evenly across all physical cells.

## Connections
- The log-structured design of the FTL is a hardware-level implementation of the concepts in [[Log-Structured File Systems - Chapter Overview]].
- SSDs represent a significant evolution from the mechanical constraints described in [[Disk Geometry Defines the Physical Structure of Hard Drives]].
