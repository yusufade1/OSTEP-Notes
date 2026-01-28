---
type: atomic
source: OSTEP Ch. 37
tags: [hard-disk, geometry, hardware, persistence]
related: [[Disk Access Time Depends on Seek Rotation and Transfer]], [[IO Architecture Connects CPU Memory and Devices via Bus Hierarchy]]
prerequisites: [[IO Architecture Connects CPU Memory and Devices via Bus Hierarchy]]
---

> [!SUMMARY]
> Hard disk drives (HDDs) consist of spinning platters coated with magnetic material, read/write heads on a moving arm, and discrete sectors for data storage. While the interface presents a linear array of blocks, the physical geometry involves tracks, cylinders, and sectors, necessitating mechanisms like track skew and zoning to maintain performance and density.

The hard disk drive (HDD) remains a fundamental storage technology, relying on mechanical components to store and retrieve data. Its physical structure dictates its performance characteristics and how the operating system interacts with it.

### Physical Components
A drive consists of one or more **platters** that spin around a **spindle** at a constant rate (measured in RPM). Each platter has two surfaces, and the drive uses a **disk arm** with **disk heads** to read and write data. The platters are bound together and spin in unison, while the arm moves the heads across the radius.

Data is organized into concentric circles called **tracks**. Each track is divided into fixed-size units called **sectors** (typically 512 bytes or 4 KB). The set of tracks at the same radius across all platters forms a **cylinder**.

### Geometry Adjustments
To cope with physical constraints, modern drives employ several geometric adjustments:

1.  **Track Skew:** Switching from one track to another requires time (seek time). If sectors were aligned perfectly radially, the head would miss the first sector of the next track by the time it settled. Track skew offsets the sector numbering on adjacent tracks so that the head lands ready to read the next logical sector without waiting for a full rotation.
2.  **Multi-Zoned Recording (Zoning):** Outer tracks have a larger circumference than inner tracks. To maximize capacity, modern drives place more sectors on outer tracks (zones) than inner ones, maintaining a constant bit density rather than a constant angular density.

### The Interface
Despite this complex geometry, the drive exposes a simple linear interface to the OS. The disk controller maps logical block addresses (LBAs) to physical sectors (cylinder, head, sector). This abstraction hides the details of bad sector remapping and zone boundaries, allowing the OS to treat the disk as a large array of blocks.
