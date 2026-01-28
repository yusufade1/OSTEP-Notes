---
type: atomic
source: OSTEP Ch. 42
tags: [file-system, crash-consistency, journaling]
related:
  - [[Journaling Provides Crash Consistency via Write-Ahead Logging]]
  - [[Journal Checkpointing Reclaims Log Space After Successful Writes]]
prerequisites:
  - [[Journaling Provides Crash Consistency via Write-Ahead Logging]]
---

> [!SUMMARY]
> The journal is organized into transactions, bounded by TxBegin and TxEnd blocks, to ensure that groups of related updates are applied atomically.

To implement write-ahead logging effectively, the journal must have a clear internal structure. A typical journal entry represents a **transaction**, which groups multiple related writes—such as the inode, bitmap, and data block updates for a single file append—into a single atomic unit.

A transaction in the journal usually consists of the following components:
*   **TxBegin Block:** A descriptor block that marks the start of a transaction and contains a unique transaction ID (TID).
*   **Metadata/Data Blocks:** The actual content of the blocks that will be updated in the file system. In "full" journaling, this includes both metadata and user data; in "metadata-only" journaling, only the metadata blocks are logged.
*   **TxEnd Block (or Commit Block):** The final block of the transaction, which also contains the TID. The presence of this block on disk signifies that the entire transaction was successfully written to the log.

A critical implementation detail is the **atomicity of the commit**. If the OS issues all blocks (Begin, Metadata, End) to the disk at once, the disk might reorder them, writing the TxEnd block before a metadata block. If a crash occurs then, the journal would appear to have a valid transaction but contain corrupted data. To prevent this, the OS must first issue the TxBegin and metadata blocks, wait for them to complete (using a write barrier or a synchronous write), and only *then* issue the TxEnd block. Alternatively, modern systems use a **checksum** in the TxEnd block that covers the entire transaction; during recovery, if the checksum doesn't match, the transaction is discarded, allowing all blocks to be written in a single asynchronous burst.
