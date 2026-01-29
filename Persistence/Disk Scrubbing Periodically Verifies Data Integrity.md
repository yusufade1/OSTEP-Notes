---
type: mechanism
source: "OSTEP Ch. 45: Data Integrity and Protection"
tags:
  - persistence
  - reliability
  - maintenance
related:
  - "[[Checksums Enable Detection of Data Corruption]]"
  - "[[RAID Uses Redundancy to Improve Performance and Reliability]]"
prerequisites:
  - "[[Checksums Enable Detection of Data Corruption]]"
---

# Disk Scrubbing Periodically Verifies Data Integrity

> [!SUMMARY]
> Disk scrubbing is a proactive background process that systematically reads all data on a storage device to verify its integrity using stored checksums. By checking data that is rarely accessed by users, scrubbing detects latent corruption early, allowing the system to repair it before a second failure makes recovery impossible.

Integrity checks that only happen when a user reads a file are insufficient for long-term storage. If a file is not accessed for a year, it could slowly "rot" on the disk without the OS noticing.

## The Problem of Latent Corruption
Consider a mirrored system (RAID-1). If Block 10 on Disk A becomes corrupt but is never read, the system won't know it's broken. If Disk B then suffers a total failure, the system must rely on Disk A to rebuild. It is only *then* that the corruption on Disk A is discovered—and by then, it is too late to recover.

## How Scrubbing Works
The disk scrubber is usually a low-priority background task that:
1.  Iterates through every block on the disk.
2.  Reads the data and its associated [[Checksums Enable Detection of Data Corruption|checksum]].
3.  Verifies the integrity.
4.  If a mismatch is found, the scrubber uses a redundant copy (from a RAID mirror or parity block) to overwrite the corrupt data with a correct version.

## Scheduling the Scrubber
Scrubbing consumes I/O bandwidth and can impact application performance. Most systems run scrubbing during idle periods (e.g., once a week or once a month). The goal is to scrub the entire drive frequently enough that the probability of two independent failures (corruption on one disk and hardware failure on another) remains extremely low.

## The Value of Proactivity
By finding and fixing "silent" errors while a redundant copy still exists, scrubbing significantly increases the **Mean Time to Data Loss (MTTDL)** for the system. It ensures that the redundancy built into [[RAID Uses Redundancy to Improve Performance and Reliability|RAID]] is actually available when needed.

## Connections
- Proactively utilizes the detection mechanism of [[Checksums Enable Detection of Data Corruption]].
- Critical for the practical reliability of [[RAID Uses Redundancy to Improve Performance and Reliability]].
