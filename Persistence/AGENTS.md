# Persistence Agents Knowledge Base

## Documentation Patterns
- **Problem -> Solution Chains:** Many persistence concepts follow a clear evolution:
  - Problem: PIO wastes CPU (Polling)
  - Solution 1: Interrupts (allows overlap)
  - New Problem: Copy overhead
  - Solution 2: DMA (offloads copy)
  Structure notes to highlight this evolutionary path.

## Code Standards
- **Mock Interfaces:** When showing device driver code, use simplified mock interfaces (like `device_read_register()`) rather than complex real-world kernel structures unless specifically illustrating a Linux/Unix struct.
