---
type: concept
source: "OSTEP Ch. 45: Data Integrity and Protection"
tags:
  - persistence
  - reliability
  - corruption
related:
  - "[[Checksums Enable Detection of Data Corruption]]"
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
prerequisites:
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
---

# Data Integrity Challenges - Bit Rot and Misdirected Writes

> [!SUMMARY]
> Storage systems are susceptible to "silent" failures where the hardware returns incorrect data without reporting an error. These challenges, including bit rot, misdirected writes, and lost writes, bypass traditional disk error-handling and require the operating system to implement its own integrity checks.

While a disk might report a "hard failure" when a sector is physically unreadable, many failures are subtle and leave no hardware trace.

## Latent Sector Errors (LSEs)
An LSE occurs when a disk sector becomes unreadable due to physical damage or magnetic decay. While the disk knows it failed, the error is "latent" because the OS doesn't discover it until it attempts to read that specific sector. If the sector is part of a RAID rebuild, an LSE can lead to total data loss.

## Bit Rot
Bit rot is the spontaneous flipping of bits on the storage media, caused by cosmic rays, magnetic interference, or semiconductor decay. The disk reads the block, but the data it returns is slightly different from what was originally written. To the OS, the data looks "valid" but is actually corrupt.

## Misdirected Writes
A misdirected write occurs when the disk or controller has a firmware bug that causes it to write a block to the **wrong physical location**.
*   The OS asks to write to Block 10.
*   The disk writes the data to Block 20.
*   Later, the OS reads Block 10 and gets the *old* data.
*   Even worse, the OS reads Block 20 and gets the *wrong* data, overwriting whatever was supposed to be there.

## Lost Writes
A lost write happens when the device acknowledges a write as complete, but never actually commits the data to the persistent media. This often happens due to caching bugs in the disk controller. When the OS later reads the block, it receives the "stale" old data rather than the new update.

## The Need for Software-Level Integrity
Because the disk controller may not detect these errors (especially if the corruption happens *after* the disk's internal ECC check), the file system must store its own redundant information. 

## Connections
- Describes the problems solved by [[Checksums Enable Detection of Data Corruption]].
- Motivates the proactive scanning used in [[Disk Scrubbing Periodically Verifies Data Integrity]].
