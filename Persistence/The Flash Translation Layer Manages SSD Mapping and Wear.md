---
type: mechanism
source: "OSTEP Ch. 44: Flash-based SSDs"
tags:
  - persistence
  - ssd
  - flash
  - ftl
  - mapping
related:
  - "[[Flash Memory Basics - Pages Blocks and Erasure Asymmetry]]"
  - "[[Log-Structured File Systems - Chapter Overview]]"
  - "[[SSD Performance Characteristics and Wear Leveling]]"
prerequisites:
  - "[[Flash Memory Basics - Pages Blocks and Erasure Asymmetry]]"
---

# The Flash Translation Layer Manages SSD Mapping and Wear

> [!SUMMARY]
> The Flash Translation Layer (FTL) is the firmware inside an SSD that translates logical block addresses (LBAs) from the operating system into physical flash locations. By using a log-structured approach, the FTL allows the SSD to appear like a standard block device while internally managing the complex "erase-before-write" constraints of flash memory.

Because flash memory cannot be overwritten in place, an SSD cannot store data at a fixed physical location. The FTL provides the indirection necessary to make the drive functional and efficient.

## Log-Structured Mapping
The FTL works very much like a [[Log-Structured File Systems - Chapter Overview|Log-structured File System]]. When the OS sends a write command for "Logical Block 100," the FTL does not overwrite the physical location where Block 100 was previously stored. Instead:
1.  It picks a fresh, erased physical page.
2.  It writes the new data there.
3.  It updates an internal **mapping table** to record that Logical Block 100 now resides at the new physical address.
4.  It marks the old physical page as "invalid" or "garbage."

## Managing the Mapping Table
The mapping table is critical for performance. 
*   **Page-level mapping**: Provides the most flexibility but requires a huge table (GBs of RAM for a large SSD).
*   **Block-level mapping**: Reduces table size but makes small writes extremely inefficient (requiring a full block copy).
*   **Hybrid Mapping**: Modern FTLs often use a hybrid approach where a small number of blocks are treated as "logs" with page-level mapping, while the majority of the drive is managed with coarser block-level mapping.

## Garbage Collection
As more writes occur, the SSD eventually runs out of free pages. The FTL must perform **garbage collection** (similar to LFS cleaning):
1.  Find a physical block that contains mostly invalid (dead) pages.
2.  Read the remaining "live" pages from that block into memory.
3.  Write the live pages to a new location.
4.  Erase the old block, making it available for new writes.

## Connections
- Implements the same conceptual logic as [[Log-Structured File Systems - Chapter Overview]] but at the hardware firmware level.
- Hides the physical reality of [[Flash Memory Basics - Pages Blocks and Erasure Asymmetry]] from the operating system.
- Enables the implementation of [[SSD Performance Characteristics and Wear Leveling]].
