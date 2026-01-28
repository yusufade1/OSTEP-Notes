# Persistence Agents Knowledge Base

## Documentation Patterns
- **Problem -> Solution Chains:** Many persistence concepts follow a clear evolution:
  - Problem: PIO wastes CPU (Polling)
  - Solution 1: Interrupts (allows overlap)
  - New Problem: Copy overhead
  - Solution 2: DMA (offloads copy)
  Structure notes to highlight this evolutionary path.
- **Locality-Aware Design:** FFS notes should emphasize the "Disk Awareness" principle—how physical geometry (cylinders, tracks) dictates software allocation policies (cylinder groups).
- **Policy vs. Exception:** FFS uses strong general policies (locality) but must implement specific "exceptions" (large files) to prevent system-wide performance degradation (group saturation).
- **The Journaling Lifecycle:** Journaling notes should emphasize the four-step lifecycle: Journaling -> Commit -> Checkpointing -> Freeing. Highlighting that a transaction is only "safe" after Commit but only "permanent" after Checkpointing is key for student understanding.
- **Write Ordering for Integrity:** In metadata-only journaling, emphasize that data *must* be written before metadata commit to prevent information leakage (the "garbage data" problem).

## Code Standards
- **Mock Interfaces:** When showing device driver code, use simplified mock interfaces (like `device_read_register()`) rather than complex real-world kernel structures unless specifically illustrating a Linux/Unix struct.
