---
type: mechanism
source: "OSTEP Ch. 45: Data Integrity and Protection"
tags:
  - persistence
  - reliability
  - checksum
  - algorithm
related:
  - "[[Data Integrity Challenges - Bit Rot and Misdirected Writes]]"
  - "[[Disk Scrubbing Periodically Verifies Data Integrity]]"
prerequisites:
  - "[[Data Integrity Challenges - Bit Rot and Misdirected Writes]]"
---

# Checksums Enable Detection of Data Corruption

> [!SUMMARY]
> A checksum is a small, fixed-size numerical value derived from a larger block of data. By storing a checksum alongside the data and recomputing it during a read, the operating system can detect if the data has been altered by bit rot, misdirected writes, or other silent failures.

Checksums are the primary line of defense against silent data corruption. They transform the problem of "verifying data" into a mathematical comparison.

## How Checksumming Works
1.  **Write**: When data is written, the OS computes a checksum $C(D)$ and stores it in a safe place (usually near the data).
2.  **Read**: When data is read, the OS computes a new checksum $C'(D)$ from the retrieved data.
3.  **Verify**: If $C(D) == C'(D)$, the data is assumed to be correct. If they differ, the data is corrupt.

## Common Checksum Functions
The choice of function balances speed and the probability of detecting an error (collision resistance):
*   **Checksum (Addition)**: Simple and fast, but weak. It can miss multiple bit flips that cancel each other out.
*   **CRC (Cyclic Redundancy Check)**: Uses polynomial division. Very effective at detecting common hardware-induced errors (burst errors).
*   **Cryptographic Hash (SHA-256)**: Extremely strong and practically impossible to "trick," but computationally expensive. Used in systems like ZFS where security and absolute integrity are paramount.

## Layout Strategies
Where you store the checksum determines which errors you can detect:
*   **Interleaved**: Checksum is stored in the same sector as data. (Detects bit rot, but misses misdirected writes because the "wrong" block's checksum will still match its own data).
*   **Parent-Pointer (ZFS style)**: The checksum of a block is stored in its **parent** (the inode or indirect block). This detects misdirected writes because the parent knows what the checksum *should* be for that specific child pointer.

## Recovery
A checksum only **detects** corruption. To **repair** it, the system needs redundancy, such as a mirror or parity block from a [[RAID Uses Redundancy to Improve Performance and Reliability|RAID]] system.

## Connections
- Direct solution to the problems in [[Data Integrity Challenges - Bit Rot and Misdirected Writes]].
- Used as the basis for the background process of [[Disk Scrubbing Periodically Verifies Data Integrity]].
