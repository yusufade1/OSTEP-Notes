---
type: mechanism
source: "OSTEP Ch. 42: Crash Consistency: FSCK and Journaling"
tags:
  - file-system
  - crash-consistency
  - journaling
related:
  - "[[Journaling Provides Crash Consistency via Write-Ahead Logging]]"
  - "[[Journal Structure Organizes Transactions with Transaction Blocks]]"
prerequisites:
  - "[[Journaling Provides Crash Consistency via Write-Ahead Logging]]"
---

> [!SUMMARY]
> Checkpointing is the process of writing committed journal transactions to their final on-disk locations, allowing the journal space to be reused for new updates.

Because the journal is a fixed-size circular buffer on the disk, it would eventually fill up if we only ever added new transactions to it. **Checkpointing** is the mechanism used to manage this space and ensure the journal remains available for future writes. 

Once a transaction has been successfully committed to the journal (meaning its TxEnd block is safely on disk), the file system is guaranteed to be recoverable. At this point, the OS can eventually write the changes to their permanent locations in the main file system structures (e.g., updating the actual inode table and data bitmaps). This is the checkpointing phase.

The lifecycle of a journaled update is thus:
1.  **Journaling:** Write the update to the log.
2.  **Commit:** Mark the log entry as complete.
3.  **Checkpointing:** Write the contents of the log entry to the main file system.
4.  **Freeing:** Mark the transaction as no longer needed in the journal.

Crucially, the transaction cannot be removed from the journal until the checkpointing is complete. If the system crashes during checkpointing, the recovery process will see that the transaction is still in the journal and replay it, ensuring the permanent structures are correctly updated. Only after the permanent structures are updated does the OS update the **journal superblock** to indicate that the space previously occupied by that transaction can now be reused. By separating the "safe" write to the log from the "slow" update to the main file system, journaling allows the OS to respond to the user quickly while ensuring long-term consistency.
