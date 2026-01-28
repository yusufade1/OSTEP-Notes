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

## Condition Variable Patterns
- **Always use `while` loops**, never `if` statements, when waiting on a condition variable. This handles Mesa semantics and spurious wakeups.
- **Producer-Consumer problems** require **two** condition variables (e.g., `empty` and `fill`) to prevent the "Wakeup One" bug where a producer wakes a producer (or consumer wakes consumer) leading to deadlock.

## Semaphore Patterns
- **POSIX vs Conceptual:** Note that POSIX definitions often allow negative semaphore values (counting waiters), while implementations built on CVs (like Zemaphores) often keep the value $\ge 0$ and rely on the CV queue for waiters. Both are valid semantics but implementation details differ.
- **Initialization:** The initial value determines behavior (1 for lock, 0 for ordering/CV).

## Bug & Anti-Pattern Notes
- **Problem -> Solution Structure:** When documenting concurrency bugs (e.g., Atomicity Violations, Deadlocks), use a clear structure:
  1.  **The Problem:** Define the bug and show a code example of how it manifests.
  2.  **The Solution:** Explain the fix (e.g., add a lock, enforce ordering) and show the corrected code.
- **Real-World Examples:** Use concrete cases from OSTEP (MySQL, Mozilla, etc.) to ground theoretical bugs in reality.

## Event-Based Concurrency Patterns
- **The Golden Rule:** Explicitly state "No Blocking Calls" in every context involving event loops. This is the defining constraint of the model.
- **Stack Ripping:** Use the "Before (Procedural) vs After (Event-driven)" code comparison pattern to illustrate how state management shifts from the stack (automatic) to the heap (manual).
