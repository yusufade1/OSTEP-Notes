---
type: concept
source: "OSTEP Ch. 44: Flash-based SSDs"
tags:
  - persistence
  - ssd
  - flash
  - hardware
related:
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
  - "[[The Flash Translation Layer Manages SSD Mapping and Wear]]"
prerequisites:
  - "[[Disk Geometry Defines the Physical Structure of Hard Drives]]"
---

# Flash Memory Basics - Pages Blocks and Erasure Asymmetry

> [!SUMMARY]
> Flash memory is a non-volatile storage technology organized into pages (typically 4KB-16KB) and blocks (typically 128-256 pages). Its defining characteristic is an operational asymmetry: while data can be read or written at the page level, it can only be erased at the block level, making updates more complex than on traditional magnetic media.

Unlike Hard Disk Drives (HDDs) which can overwrite any sector at any time, flash memory cells must be in an "erased" state before they can be programmed with new data. This physical reality dictates how SSDs must be managed.

## Hierarchical Organization
Flash chips are organized into a hierarchy:
1.  **Bank/Plane**: The high-level parallel units of the chip.
2.  **Block**: The unit of erasure. A block contains many pages.
3.  **Page**: The unit of reading and writing.

## The Three Basic Operations
*   **Read**: The device can read any page at high speed, regardless of where it is on the chip. This provides the near-instant "random access" SSDs are known for.
*   **Program (Write)**: The device can change a page from an erased state (all 1s) to a programmed state (some 0s). Once a page is programmed, its contents cannot be changed without an erase.
*   **Erase**: To reset a page, the device must erase the entire **block** it belongs to. Erasure is a slow, high-voltage operation that resets all bits in the block to 1.

## The "Erase-Before-Write" Constraint
Because erasure happens only at the block level, you cannot simply "overwrite" Page 5 in Block 10. If you wanted to change one byte in Page 5, you would theoretically have to:
1.  Read all pages in Block 10 into a memory buffer.
2.  Modify the data for Page 5 in the buffer.
3.  Erase the entire Block 10 on the chip.
4.  Write the entire buffer back to Block 10.

This approach is extremely slow and causes unnecessary wear. Instead, modern SSDs use a [[The Flash Translation Layer Manages SSD Mapping and Wear|Flash Translation Layer]] to write the new data to a different, already-erased location, leaving the old version of Page 5 as "dead" data.

## Connections
- Contrasts with the mechanical seek-based constraints of [[Disk Geometry Defines the Physical Structure of Hard Drives]].
- Necessitates the indirection provided by [[The Flash Translation Layer Manages SSD Mapping and Wear]].
