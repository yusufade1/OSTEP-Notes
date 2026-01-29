---
type: overview
source: "OSTEP Ch. 45: Data Integrity and Protection"
tags:
  - persistence
  - reliability
  - checksum
  - chapter-overview
related:
  - "[[Persistence MOC]]"
  - "[[RAID Uses Redundancy to Improve Performance and Reliability]]"
  - "[[Crash Consistency - Chapter Overview]]"
prerequisites:
  - "[[IO and Storage - Chapter Overview]]"
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
---

# Data Integrity and Protection - Chapter Overview

> [!SUMMARY]
> Storage devices are not perfectly reliable; they can lose data through latent sector errors, bit rot, or firmware bugs. This chapter explores how operating systems and file systems protect against these "silent" failures using redundant information (checksums) and proactive maintenance (scrubbing).

## The Threat Model: Silent Data Corruption
Traditional errors (like a disk reporting a failed read) are easy to handle. The real danger comes from corruption that goes undetected by the hardware.
*   **[[Data Integrity Challenges - Bit Rot and Misdirected Writes]]:** Understanding the various ways data can be lost without the disk controller noticing, including spontaneous bit flips and "lost" writes.

## Detecting Corruption
The primary tool for ensuring data integrity is the checksum.
*   **[[Checksums Enable Detection of Data Corruption]]:** How storing a mathematical summary of data allows the OS to verify that the data read is exactly what was written.

## Proactive Maintenance
Detection only works when data is actually read. To prevent "data rot" in rarely used files, the system must be proactive.
*   **[[Disk Scrubbing Periodically Verifies Data Integrity]]:** The mechanism of background scanning that checks the entire disk for corruption before it leads to permanent data loss.

## Connections
- Complements the redundancy strategies found in [[RAID Uses Redundancy to Improve Performance and Reliability]].
- Addresses a different class of failure than the power-loss scenarios in [[Crash Consistency - Chapter Overview]].
