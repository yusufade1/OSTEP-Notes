# Concurrency Agent Guidelines

## Dependencies
- Concurrency notes heavily reference Virtualization concepts. Ensure you are familiar with:
  - [[A Process is a Running Program]]
  - [[The Address Space Abstracts Physical Memory for Each Process]]
  - [[Context Switch Saves and Restores Process State]]

## Code Examples
- Most concurrency examples use `pthread` API.
- Use `volatile` for shared variables in C examples to prevent compiler optimization from hiding race conditions (pedagogical accuracy).
- **Always check return codes** for pthread functions (e.g., using `assert()` or wrapper functions) to ensure robustness in examples.

## Lock Implementation Patterns
- When explaining locks, distinguish between:
  - **Hardware Primitives:** Test-and-Set, CAS, Fetch-and-Add (universally available in some form).
  - **OS Primitives:** park/unpark (Solaris), futex (Linux). The specific API matters less than the concept (sleep/wake).
- Pseudocode for locks should clearly separate the "fast path" (atomic check) from the "slow path" (yielding/sleeping).
