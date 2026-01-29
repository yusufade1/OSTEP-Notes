---
type: overview
source: "OSTEP Ch. 38: Redundant Disk Arrays (RAID)"
tags:
  - persistence
  - raid
  - reliability
  - performance
  - overview
related:
  - "[[Persistence MOC]]"
  - "[[IO and Storage - Chapter Overview]]"
prerequisites:
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
---

# RAID - Chapter Overview

> [!SUMMARY]
> **RAID (Redundant Array of Independent Disks)** is a technology used to combine multiple physical disk drives into a single logical unit. The primary goals of RAID are to improve **performance** (by spreading I/O across multiple disks) and **reliability** (by using redundancy to protect against disk failure).


## Key Concepts

*   **[[RAID Uses Redundancy to Improve Performance and Reliability]]**: The fundamental trade-offs between capacity, reliability, and performance.
*   **[[RAID-0 Striping Maximizes Performance but Lowers Reliability]]**: Spreading data across disks for speed, but with no protection against failure.
*   **[[RAID-1 Mirroring Guarantees Reliability at High Cost]]**: Keeping an exact copy of data on two disks for maximum safety.
*   **[[RAID-4 Uses a Dedicated Parity Disk]]:** Using a single parity disk to provide redundancy for a set of data disks.
*   **[[RAID-5 Rotates Parity to Eliminate Bottlenecks]]:** Distributing parity across all disks to avoid the write-bottleneck of RAID-4.

## Summary
Different RAID levels offer different balances of capacity, reliability, and performance. RAID-0 is for high performance, RAID-1 is for safety, and RAID-5 is a popular middle ground. Understanding the mathematical analysis of these levels is key to selecting the right storage strategy for a given workload.