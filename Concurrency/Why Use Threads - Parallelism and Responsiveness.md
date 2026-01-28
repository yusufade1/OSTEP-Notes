---
type: atomic
source: OSTEP Ch. 26
tags: [concurrency, threads, performance, parallelism]
related: [[Threads - Chapter Overview]], [[Thread vs Process - Shared Address Space]], [[Multi-CPU Scheduling Faces Cache Affinity and Synchronization Challenges]]
prerequisites: [[Thread vs Process - Shared Address Space]]
---

# Why Use Threads - Parallelism and Responsiveness

There are two primary reasons why developers choose to complicate their programs by using threads: **parallelism** and **responsiveness**. While single-threaded programming is simpler and easier to debug, it cannot fully exploit modern hardware or provide the user experience required by interactive applications.

## Parallelism

The first motivation is simply speed. For decades, CPU clock speeds doubled regularly (Moore's Law), allowing single-threaded programs to run faster without modification. However, this trend has stalled, and modern processors gain performance by adding more **cores** rather than increasing frequency. A standard laptop today might have 8 or more cores, and servers can have dozens.

A single-threaded program can only run on one core at a time. If you have a compute-intensive task—such as matrix multiplication, image processing, or searching a large dataset—running it on a single thread leaves the other cores idle. By splitting the task into smaller sub-tasks and assigning each to a separate thread, you can run them in parallel on different cores. Ideally, using $N$ threads on $N$ cores would speed up the program by a factor of $N$ (linear scaling), though synchronization overhead often reduces this gain.

## Responsiveness via Overlapping I/O

The second motivation is to avoid blocking the entire program due to slow I/O operations. In a single-threaded process, if the program issues a disk request or waits for a network packet, the CPU scheduler puts the process in a **blocked** state. The CPU sits idle (with respect to that program) until the I/O completes.

Imagine a web browser or a GUI text editor. If the main thread (which handles the UI) performs a network request to load a file, the entire interface would "freeze" until the download finishes. The user couldn't scroll, click buttons, or type. 

Threads solve this by allowing **overlap**. One thread can initiate a blocking I/O operation and go to sleep, while another thread (e.g., the UI thread) continues to run and handle user input. The OS scheduler sees that one thread is blocked but others are ready to run, so it switches to the ready threads. This makes the application feel responsive and utilizes the CPU cycles that would otherwise be wasted waiting for the disk.

> [!SUMMARY]
> Threads are used to achieve **parallelism** and **responsiveness**. Parallelism leverages multi-core architectures by distributing compute-heavy tasks across multiple processors to speed up execution. Responsiveness is achieved by overlapping blocking I/O operations (like disk or network access) with useful work; when one thread blocks waiting for data, others can continue execution, ensuring the application remains interactive and the CPU stays busy.
