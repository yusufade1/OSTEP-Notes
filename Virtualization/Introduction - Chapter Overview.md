---
type: overview
source: "OSTEP Ch. 1-2: Introduction to Operating Systems"
tags:
  - virtualization
  - introduction
  - overview
related:
  - "[[Virtualization MOC]]"
  - "[[Concurrency MOC]]"
  - "[[Persistence MOC]]"
prerequisites: []
---

# Operating Systems: Three Easy Pieces (Preface & Introduction)

> [!SUMMARY]
> An introduction to the Operating System as a resource manager that virtualizes hardware (CPU/Memory), handles concurrency, and ensures data persistence, evolved from simple libraries to complex systems like UNIX.

## Context

The Operating System (OS) exists to make computer systems easy to use and efficient. It manages limited physical resources (CPU, Memory, Disk) and provides a "Standard Library" of system calls for applications. Without an OS, developers would have to manage hardware protection, scheduling, and concurrency manually.

**Prerequisites:** Understanding of the **Von Neumann model** (fetch, decode, execute) and basic C programming.

---

## Core Concept: The Three Easy Pieces

The book decomposes Operating Systems into three primary thematic elements:

1.  **Virtualization**
    *   **Concept:** The OS takes a physical resource (like the CPU or Memory) and transforms it into a more general, powerful, and easy-to-use virtual form.
    *   **Goal:** To provide each running program with the illusion that it has the system to itself.

2.  **Concurrency**
    *   **Concept:** Managing multiple things happening at the same time.
    *   **Problem:** Arises when threads (or processes) access shared resources, leading to potential bugs like race conditions.
    *   **Goal:** To enable correct and efficient multi-threaded execution.

3.  **Persistence**
    *   **Concept:** Storing data reliably so it survives system crashes or power outages.
    *   **Mechanism:** File Systems, managing data on disk/SSDs.
    *   **Goal:** To ensure data integrity and accessibility over time.

> [!VISUAL]+ Inferred: Structural Model
> The OS acting as an abstraction layer between User Applications and Physical Hardware.
>
> *Reconstruction:*
> ```mermaid
> graph TD
>     User[User / Applications]
>     OS[Operating System / Virtual Machine]
>     HW[Physical Hardware]
>
>     User -->|System Calls API| OS
>     OS -->|Virtualization| User
>     OS -->|Management| HW
>     HW -->|CPU, RAM, Disk| OS
> ```

---

## Implementation: The System Call

To provide **protection**, the OS runs in a privileged mode (**Kernel Mode**), while applications run in restricted **User Mode**.

1.  **Transition:** Applications perform a **System Call** (via a `trap` instruction).
2.  **Privilege Elevation:** Hardware raises privilege level to Kernel Mode.
3.  **Execution:** OS handles the request (e.g., accessing disk).
4.  **Return:** OS executes `return-from-trap` to lower privilege back to User Mode.

---

## Key Takeaways

*   **OS = Resource Manager:** It arbitrates who gets CPU, memory, and disk access (Policy) and how (Mechanism).
*   **Abstraction:** OS design relies heavily on abstractions (hiding implementation details) to manage complexity.
*   **History Matters:** Understanding *why* systems were built (e.g., Multics, UNIX) helps explain *how* they work today.
*   **Practicality:** Real understanding comes from writing code. The book emphasizes projects in C and the **xv6** educational kernel.

---

## Connections

*   **Relates to:** [[UNIX]] — The historical root of modern OS design concepts discussed.
*   **Enables:** [[Systems Programming]] — The skills developed (C, kernel hacking) are foundational for low-level software development.
*   **Depends on:** [[Computer Architecture]] — Hardware features (interrupts, memory management units) enable OS virtualization.

---

## Critical Inquiries

> [!QUESTION] **The Cost of Abstraction:** At what point do OS abstractions (like processes) become "leaky" or too costly, requiring developers to punch through to the underlying hardware (e.g., for CPU affinity or cache locality)?

> [!QUESTION] **Concurrency vs. Parallelism:** How does the OS's role change when moving from concurrency (interleaving) to true parallelism (multi-core)? Does the OS hide this distinction effectively?

> [!QUESTION] **Persistence & NVM:** How does Non-Volatile Memory (NVM) challenge the traditional distinction between "Virtualization" (RAM) and "Persistence" (Disk)?

---

## Source Reference

*   **Original:** `ch12.md` (Preface & Introduction)
*   **Processed:** 2026-01-24
*   **Note:** This note synthesizes the Preface and Introduction (Chapters 1 & 2) of OSTEP.
