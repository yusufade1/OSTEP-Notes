# Concurrency Agent Guidelines

## Dependencies
- Concurrency notes heavily reference Virtualization concepts. Ensure you are familiar with:
  - [[A Process is a Running Program]]
  - [[The Address Space Abstracts Physical Memory for Each Process]]
  - [[Context Switch Saves and Restores Process State]]

## Code Examples
- Most concurrency examples use `pthread` API.
- Use `volatile` for shared variables in C examples to prevent compiler optimization from hiding race conditions (pedagogical accuracy).
