---
type: atomic
source: OSTEP Ch. 26
tags: [concurrency, threads, execution]
related: [[Threads - Chapter Overview]], [[Thread vs Process - Shared Address Space]], [[Context Switch Saves and Restores Process State]]
prerequisites: [[Thread vs Process - Shared Address Space]]
---

# Thread Creation and Execution Model

When a program runs as a single-threaded process, its execution path is straightforward: it starts at `main()` and executes instructions sequentially until it exits. Introducing threads changes this model into one where multiple instruction streams execute seemingly at once.

## The Thread Lifecycle

Creating a thread is distinct from a simple function call. When you call a function, the caller pauses, the callee runs to completion, and then returns control. When you create a thread, the "caller" (the creating thread) continues running, and the "callee" (the new thread) *also* starts running independently.

From the operating system's perspective, creating a thread involves allocating a new **stack** for it and initializing a new **Thread Control Block (TCB)** to store its state (PC, registers, stack pointer). The OS then adds this new thread to the scheduler's "ready" queue.

## Non-Deterministic Scheduling

Once a thread is created, the order in which it executes relative to the creator is undefined. Consider a main thread that creates Thread A and Thread B. The OS scheduler decides which thread runs at any given moment. 
*   The main thread might continue running for a while before A starts.
*   The OS might context switch to A immediately.
*   The OS might run B before A.

This **indeterminacy** is a core property of concurrent programming. You cannot assume anything about the relative speed or ordering of independent threads unless you use explicit synchronization primitives (like locks or condition variables) to enforce it.

## Stack Allocation

Because each thread needs its own stack, the address space becomes fragmented with multiple stack regions. The OS (or the threading library) must find a chunk of free space in the process's virtual memory to place the new stack. If the address space is crowded or if threads are created recursively without bound, the process can run out of address space solely due to stack allocation overhead.

When a thread finishes its task, it exits. However, its resources (like its stack and TCB) must be cleaned up. This often requires a "join" operation (similar to `wait()` for processes) where another thread waits for the termination and reaps the resources.

> [!SUMMARY]
> Thread creation spawns an independent execution stream with its own stack and register state. Unlike a function call, the created thread runs concurrently with the creator. The OS scheduler manages these threads independently, leading to **non-deterministic execution order**—the programmer cannot predict which thread will run when. Managing this lifecycle requires allocating memory for thread stacks and properly joining threads to ensure resource cleanup upon termination.
