---
type: mechanism
source: "OSTEP Ch. 41: Locality and The Fast File System"
tags:
  - file-system
  - implementation
  - locality
  - ffs
  - persistence
related:
  - "[[FFS Cylinder Groups Improve Locality]]"
  - "[[FFS Allocation Policies Optimize Seek Times]]"
prerequisites:
  - "[[FFS Allocation Policies Optimize Seek Times]]"
---

> [!SUMMARY]
> While FFS prioritizes keeping a file's data in the same cylinder group as its inode, doing so for extremely large files would fill the group and force unrelated files to be placed far away. FFS solves this with a **large file exception**, which breaks large files into "chunks" and spreads them across multiple cylinder groups, ensuring no single file monopolizes a local region.

The core philosophy of FFS is locality: keep related things together. However, a blind application of this rule to large files creates a significant problem. If a multi-gigabyte file were forced into a single cylinder group, it would quickly consume all the data blocks in that group. Any subsequent files created in that directory—which should also be placed in that group for locality—would be forced to a distant part of the disk, breaking the locality principle for the rest of the system.

### Spreading the Load
To prevent this "group saturation," FFS implements a specific exception for large files. After a file reaches a certain size threshold (typically after the first few direct blocks or after a specific number of blocks are allocated in a single group), FFS redirects the allocation of the next portion of the file to a **different** cylinder group.

### The Chunking Mechanism
The file is essentially broken into chunks (e.g., 4 MB segments). 
*   The first 4 MB are placed in Group A (with the inode).
*   The next 4 MB are placed in Group B.
*   The following 4 MB are placed in Group C.

### Performance Trade-off
This strategy introduces a seek when the file is read sequentially (as the disk arm moves from Group A to Group B). However, because the chunks are large, the time spent reading the 4 MB of data vastly outweighs the time spent seeking. By making the chunks large enough, FFS achieves "amortized sequentiality"—the seek cost becomes negligible compared to the massive transfer, while the disk remains balanced and available for other files to maintain their own local groupings.
