# PRD: OSTEP Book → Atomic Obsidian PKM Conversion

## Introduction

Convert all ~50 chapters of *Operating Systems: Three Easy Pieces* (OSTEP) by Remzi and Andrea Arpaci-Dusseau into an interconnected Obsidian vault of atomic notes following the `content-to-knowledge` format. Each chapter produces 3-8 atomic notes (200-500 words each) organized into three theme folders, connected via wikilinks, and enriched with simplified C code examples from the book.

The result is a navigable knowledge graph where any OS concept can be accessed independently, traced to related concepts across themes, and followed along prerequisite learning paths.

## Goals

- Convert all ~50 OSTEP chapters into 150-300 atomic Obsidian notes
- Organize notes into exactly 3 theme folders: `Virtualization/`, `Concurrency/`, `Persistence/`
- Provide Map of Content (MOC) notes per theme and chapter overview notes for hierarchical navigation
- Interlink notes with wikilinks (minimum 2 per note) for graph-based exploration
- Include simplified C code examples from OSTEP inline within relevant notes
- Track explicit prerequisites in frontmatter to enable learning-path generation
- Pass all 6 quality gates on every note: atomic, complete, practical, future-proof, connected, scannable

## Chapter Inventory

### Virtualization (~18 chapters → ~70-100 notes)

| # | Chapter Topic | Estimated Notes |
|---|---------------|-----------------|
| 1 | Dialogue on Virtualization | 1 (overview) |
| 2 | Processes | 4-5 |
| 3 | Process API (fork, exec, wait) | 4-5 |
| 4 | Direct Execution (limited) | 3-4 |
| 5 | CPU Scheduling: Introduction | 3-4 |
| 6 | MLFQ Scheduling | 4-5 |
| 7 | Proportional Share (Lottery/Stride) | 3-4 |
| 8 | Multi-CPU Scheduling | 3-4 |
| 9 | Address Spaces | 3-4 |
| 10 | Memory API (malloc, free) | 3-4 |
| 11 | Address Translation | 4-5 |
| 12 | Segmentation | 3-4 |
| 13 | Free-Space Management | 3-4 |
| 14 | Paging: Introduction | 4-5 |
| 15 | TLBs | 4-5 |
| 16 | Paging: Smaller Tables | 3-4 |
| 17 | Swapping: Mechanisms | 3-4 |
| 18 | Swapping: Policies | 3-4 |

### Concurrency (~12 chapters → ~50-70 notes)

| # | Chapter Topic | Estimated Notes |
|---|---------------|-----------------|
| 19 | Dialogue on Concurrency | 1 (overview) |
| 20 | Threads Introduction | 4-5 |
| 21 | Thread API (pthreads) | 3-4 |
| 22 | Locks: Basic Concepts | 4-5 |
| 23 | Lock-Based Data Structures | 3-4 |
| 24 | Condition Variables | 4-5 |
| 25 | Semaphores | 4-5 |
| 26 | Concurrency Bugs | 5-6 |
| 27 | Event-Based Concurrency | 3-4 |
| 28 | Dialogue on Concurrency (summary) | 1 |

### Persistence (~16 chapters → ~60-90 notes)

| # | Chapter Topic | Estimated Notes |
|---|---------------|-----------------|
| 29 | Dialogue on Persistence | 1 (overview) |
| 30 | I/O Devices | 4-5 |
| 31 | Hard Disk Drives | 4-5 |
| 32 | RAID | 5-6 |
| 33 | Files and Directories API | 3-4 |
| 34 | File System Implementation (VSFS) | 5-6 |
| 35 | Locality and FFS | 4-5 |
| 36 | Crash Consistency (FSCK/Journaling) | 5-6 |
| 37 | Log-Structured File Systems | 4-5 |
| 38 | Flash-Based SSDs | 3-4 |
| 39 | Data Integrity and Protection | 3-4 |
| 40 | Dialogue on Persistence (summary) | 1 |
| 41 | Distributed Systems Intro | 3-4 |
| 42 | NFS (Sun's Network File System) | 4-5 |
| 43 | AFS (Andrew File System) | 4-5 |

---

## User Stories

### US-001: Virtualization Theme MOC
**Description:** As a student, I want a Virtualization Map of Content so I can see all process, scheduling, and memory concepts at a glance.

**Acceptance Criteria:**
- [ ] `Virtualization/Virtualization MOC.md` exists with wikilinks to all chapter overview notes
- [ ] Grouped by sub-themes: Processes, Scheduling, Memory
- [ ] Frontmatter includes `type: moc`, `tags: [virtualization]`

### US-002: Process Concepts (Chapters 2-4)
**Description:** As a learner, I want atomic notes on process abstraction, API, and direct execution so I can understand how the OS virtualizes the CPU.

**Acceptance Criteria:**
- [ ] Chapter overview note: `Virtualization/Processes - Chapter Overview.md`
- [ ] Atomic notes for: process abstraction, process states, process API (fork/exec/wait), PCB/context switch, limited direct execution, system calls, timer interrupts
- [ ] Each note includes simplified C code where OSTEP provides examples (e.g., `fork()` return values)
- [ ] `prerequisites` field correctly chains: abstraction → states → API → direct execution
- [ ] All notes pass 6 quality gates

### US-003: CPU Scheduling (Chapters 5-8)
**Description:** As a student, I want atomic notes on scheduling algorithms so I can compare FIFO, SJF, RR, MLFQ, and proportional-share approaches.

**Acceptance Criteria:**
- [ ] Chapter overview note for scheduling
- [ ] Atomic notes for: scheduling metrics (turnaround/response time), FIFO, SJF/STCF, Round Robin, MLFQ rules, MLFQ gaming prevention, lottery scheduling, stride scheduling, multi-CPU scheduling
- [ ] Each algorithm note includes a worked example or trace
- [ ] Cross-links between scheduling notes and process notes
- [ ] All notes pass 6 quality gates

### US-004: Address Spaces & Memory API (Chapters 9-10)
**Description:** As a learner, I want atomic notes on memory virtualization concepts so I understand the goals before diving into mechanisms.

**Acceptance Criteria:**
- [ ] Atomic notes for: address space abstraction, memory virtualisation goals (transparency/efficiency/protection), stack vs heap, malloc/free API, common memory bugs
- [ ] Code examples for memory allocation patterns
- [ ] Prerequisites chain from process concepts
- [ ] All notes pass 6 quality gates

### US-005: Address Translation & Segmentation (Chapters 11-12)
**Description:** As a student, I want notes on base-and-bounds and segmentation so I understand early translation mechanisms before paging.

**Acceptance Criteria:**
- [ ] Atomic notes for: address translation concept, base-and-bounds, dynamic relocation, segmentation (coarse/fine-grained), segment table, external fragmentation
- [ ] Prerequisites reference address space notes
- [ ] All notes pass 6 quality gates

### US-006: Free-Space Management (Chapter 13)
**Description:** As a learner, I want notes on memory allocation strategies so I understand how the OS manages variable-sized memory regions.

**Acceptance Criteria:**
- [ ] Atomic notes for: splitting/coalescing, free list, allocation strategies (best-fit, worst-fit, first-fit, next-fit), buddy system, slab allocator
- [ ] Each strategy note includes trade-off analysis
- [ ] All notes pass 6 quality gates

### US-007: Paging (Chapters 14-16)
**Description:** As a student, I want atomic notes on paging mechanisms so I understand page tables, TLBs, and multi-level structures.

**Acceptance Criteria:**
- [ ] Atomic notes for: paging concept, page table entries (PTE), page table structure, TLB (concept, miss handling, context switches), TLB replacement policies, multi-level page tables, inverted page tables
- [ ] TLB note includes MIPS-style assembly example from OSTEP
- [ ] Prerequisites chain: segmentation → paging → TLB → multi-level
- [ ] Cross-link to scheduling (context switch TLB flush)
- [ ] All notes pass 6 quality gates

### US-008: Swapping (Chapters 17-18)
**Description:** As a learner, I want notes on swapping mechanisms and page replacement policies.

**Acceptance Criteria:**
- [ ] Atomic notes for: swap space, page fault handling, page replacement policies (optimal, FIFO, LRU, clock/approximating LRU), thrashing, working set
- [ ] Each policy note includes comparison to alternatives
- [ ] Prerequisites reference paging notes
- [ ] All notes pass 6 quality gates

### US-009: Concurrency Theme MOC
**Description:** As a student, I want a Concurrency Map of Content so I can navigate threads, synchronization primitives, and bug patterns.

**Acceptance Criteria:**
- [ ] `Concurrency/Concurrency MOC.md` exists with wikilinks to all chapter overview notes
- [ ] Grouped by sub-themes: Threads, Synchronization, Bugs & Patterns
- [ ] Frontmatter includes `type: moc`, `tags: [concurrency]`

### US-010: Threads (Chapters 20-21)
**Description:** As a learner, I want atomic notes on thread concepts and POSIX API so I understand shared-memory concurrency.

**Acceptance Criteria:**
- [ ] Chapter overview note for threads
- [ ] Atomic notes for: thread vs process, shared address space, thread creation, race conditions, critical sections, pthread API (create, join, mutex, cond)
- [ ] Code examples for `pthread_create`, `pthread_mutex_lock`
- [ ] Cross-link to process notes (threads as lightweight processes)
- [ ] All notes pass 6 quality gates

### US-011: Locks (Chapters 22-23)
**Description:** As a student, I want notes on lock implementations so I understand hardware and OS support for mutual exclusion.

**Acceptance Criteria:**
- [ ] Atomic notes for: lock concept/goals, spin locks, test-and-set, compare-and-swap, fetch-and-add, ticket locks, yield-based locks, queue-based locks (park/unpark), two-phase locks
- [ ] Lock-based data structures: concurrent counters, linked lists, queues, hash tables
- [ ] Each implementation includes C pseudocode
- [ ] All notes pass 6 quality gates

### US-012: Condition Variables & Semaphores (Chapters 24-25)
**Description:** As a learner, I want notes on higher-level synchronization primitives.

**Acceptance Criteria:**
- [ ] Atomic notes for: condition variable concept, wait/signal semantics, producer-consumer problem (with CVs), covering conditions, semaphore definition, binary semaphore as lock, semaphore as CV, reader-writer locks, dining philosophers
- [ ] Each pattern includes C code from OSTEP
- [ ] Prerequisites reference lock notes
- [ ] All notes pass 6 quality gates

### US-013: Concurrency Bugs (Chapter 26)
**Description:** As a student, I want notes on common bug patterns so I can recognize and avoid them.

**Acceptance Criteria:**
- [ ] Atomic notes for: atomicity violations, order violations, deadlock (conditions, prevention, avoidance, detection/recovery), livelock
- [ ] Each bug type includes a real-world example from OSTEP (MySQL, Mozilla, etc.)
- [ ] Cross-links to lock and CV notes
- [ ] All notes pass 6 quality gates

### US-014: Event-Based Concurrency (Chapter 27)
**Description:** As a learner, I want notes on event-driven programming as an alternative to threads.

**Acceptance Criteria:**
- [ ] Atomic notes for: event loop concept, select/poll API, problem of blocking, async I/O, state management in event systems
- [ ] Cross-links to thread notes (comparing models)
- [ ] All notes pass 6 quality gates

### US-015: Persistence Theme MOC
**Description:** As a student, I want a Persistence Map of Content so I can navigate I/O, storage, and file system concepts.

**Acceptance Criteria:**
- [ ] `Persistence/Persistence MOC.md` exists with wikilinks to all chapter overview notes
- [ ] Grouped by sub-themes: I/O & Storage, File Systems, Distributed FS
- [ ] Frontmatter includes `type: moc`, `tags: [persistence]`

### US-016: I/O Devices (Chapter 30)
**Description:** As a learner, I want notes on I/O architecture so I understand how the OS communicates with hardware.

**Acceptance Criteria:**
- [ ] Atomic notes for: I/O architecture (bus hierarchy), device interface (status/command/data), polling vs interrupts, DMA, device drivers
- [ ] Cross-links to process notes (interrupt handling)
- [ ] All notes pass 6 quality gates

### US-017: Hard Disk Drives (Chapter 31)
**Description:** As a student, I want notes on HDD geometry and scheduling algorithms.

**Acceptance Criteria:**
- [ ] Atomic notes for: disk geometry (platter/track/sector), rotational delay, seek time, disk scheduling (SSTF, SCAN/C-SCAN, SPTF), I/O merging, disk cache
- [ ] Each scheduling algorithm includes seek-sequence example
- [ ] All notes pass 6 quality gates

### US-018: RAID (Chapter 32)
**Description:** As a learner, I want notes on RAID levels so I understand redundancy-performance trade-offs.

**Acceptance Criteria:**
- [ ] Atomic notes for: RAID concept, RAID-0 (striping), RAID-1 (mirroring), RAID-4 (parity), RAID-5 (rotating parity), RAID analysis (capacity/reliability/performance)
- [ ] Each level includes capacity/reliability/performance formula
- [ ] All notes pass 6 quality gates

### US-019: File Systems (Chapters 33-34)
**Description:** As a student, I want notes on FS abstractions and VSFS implementation.

**Acceptance Criteria:**
- [ ] Atomic notes for: file abstraction, directory abstraction, file API (open/read/write/close/fsync), inode, data bitmap, inode bitmap, superblock, directory entries, file read/write paths, free-space tracking
- [ ] Code examples for file API system calls
- [ ] All notes pass 6 quality gates

### US-020: FFS & Crash Consistency (Chapters 35-36)
**Description:** As a learner, I want notes on FFS optimizations and journaling for crash safety.

**Acceptance Criteria:**
- [ ] Atomic notes for: FFS motivation, cylinder groups, block allocation policy, small file problem, crash consistency problem, fsck approach, journaling (write-ahead log), journal structure, checkpointing, metadata journaling
- [ ] Prerequisites chain: VSFS → FFS → crash consistency → journaling
- [ ] All notes pass 6 quality gates

### US-021: LFS & Data Integrity (Chapters 37-39)
**Description:** As a student, I want notes on log-structured file systems, SSDs, and data protection.

**Acceptance Criteria:**
- [ ] Atomic notes for: LFS motivation, write buffering, inode map, checkpoint region, garbage collection, flash memory (pages/blocks/erase), FTL (flash translation layer), wear leveling, checksums, disk scrubbing
- [ ] Cross-links to journaling notes (LFS as alternative)
- [ ] All notes pass 6 quality gates

### US-022: Distributed File Systems (Chapters 42-43)
**Description:** As a learner, I want notes on NFS and AFS so I understand distributed storage approaches.

**Acceptance Criteria:**
- [ ] Atomic notes for: NFS architecture, stateless protocol, idempotent operations, client-side caching, cache consistency (NFS), AFS architecture, whole-file caching, callbacks, AFS vs NFS comparison
- [ ] Cross-links between NFS and AFS notes
- [ ] All notes pass 6 quality gates

---

## Functional Requirements

### Note Structure

- FR-1: Every note MUST have YAML frontmatter with fields: `type`, `source`, `tags`, `related`, `prerequisites`
- FR-2: The `type` field MUST be one of: `concept`, `mechanism`, `algorithm`, `pattern`, `moc`, `overview`
- FR-3: The `source` field MUST reference the OSTEP chapter: `"OSTEP Ch. X: [Title]"`
- FR-4: The `tags` field MUST include the theme tag plus 1-3 topic tags from the taxonomy
- FR-5: The `related` field MUST contain at least 2 wikilinks to other notes in the vault
- FR-6: The `prerequisites` field MUST list notes that should be understood before this one (empty list `[]` for foundational concepts)
- FR-7: Note titles MUST be declarative statements (e.g., "TLB is a hardware cache for virtual-to-physical address translation")
- FR-8: Every note MUST begin with a `> [!SUMMARY]` callout containing a 2-3 sentence overview
- FR-9: Notes MUST be 200-500 words (excluding frontmatter and code blocks)
- FR-10: Notes MUST be atomic — one concept, mechanism, or algorithm per note

### Code Examples

- FR-11: Notes MUST include simplified C code snippets where OSTEP provides relevant examples
- FR-12: Code blocks MUST use ` ```c ` fencing with brief inline comments
- FR-13: Code examples MUST be simplified for clarity (remove error checking boilerplate unless it's the point)
- FR-14: Each code example MUST have a 1-line description above it explaining what it demonstrates

### Navigation Structure

- FR-15: Each theme folder MUST contain exactly one MOC note (e.g., `Virtualization MOC.md`)
- FR-16: MOC notes MUST group chapter overviews by sub-theme with wikilinks
- FR-17: Each OSTEP chapter (or logical chapter group) MUST have one overview note linking to its atomic notes
- FR-18: Overview notes MUST include a brief chapter summary and a bulleted list of wikilinks to atomic notes

### Linking Strategy

- FR-19: **Intra-theme links**: Every note MUST link to at least 1 note within its theme folder
- FR-20: **Cross-theme links**: Where applicable, notes MUST link across themes (e.g., process → threads, address spaces → file system)
- FR-21: **Prerequisite links**: The `prerequisites` field MUST form a valid DAG (no cycles)
- FR-22: **Bidirectional awareness**: If note A lists note B in `related`, note B SHOULD list note A (Obsidian backlinks supplement this)

### Tagging Taxonomy

- FR-23: Theme tags: `#virtualization`, `#concurrency`, `#persistence`
- FR-24: Topic tags (non-exhaustive): `#process`, `#scheduling`, `#memory`, `#paging`, `#tlb`, `#segmentation`, `#swapping`, `#threads`, `#locks`, `#synchronization`, `#deadlock`, `#io`, `#disk`, `#raid`, `#filesystem`, `#journaling`, `#distributed`
- FR-25: Type-derived tags: `#concept`, `#mechanism`, `#algorithm`, `#pattern`

---

## Non-Goals

- No conversion of OSTEP homework/simulation exercises (content only)
- No creation of a `Resources/` folder — all notes go in theme folders
- No Anki flashcard generation (separate concern)
- No per-section granularity below atomic concept level (don't split a single concept across notes)
- No multimedia embedding (diagrams described in text, not images)
- No versioning of notes against OSTEP editions
- No automated tooling development — this PRD is for manual/agent-assisted conversion

---

## Design Considerations

### Note Template

```markdown
---
type: mechanism
source: "OSTEP Ch. 15: TLBs"
tags: [virtualization, memory, tlb, mechanism]
related:
  - "[[Paging divides address space into fixed-size pages]]"
  - "[[Context switch requires TLB flush or ASID tagging]]"
  - "[[Multi-level page tables reduce memory overhead]]"
prerequisites:
  - "[[Paging divides address space into fixed-size pages]]"
  - "[[Page table entry maps virtual page to physical frame]]"
---

# TLB is a hardware cache for virtual-to-physical address translation

> [!SUMMARY]
> The Translation Lookaside Buffer (TLB) is a small, fast hardware cache that stores recent virtual-to-physical page mappings. Without it, every memory access would require an expensive page table lookup. TLBs exploit temporal and spatial locality to achieve near-100% hit rates for most workloads.

## How the TLB Works

On every memory reference, the hardware extracts the virtual page number (VPN) and checks the TLB...

## TLB Miss Handling

```c
// Hardware-managed TLB miss (x86)
PTE = PageTable[VPN];
if (PTE.Valid == 0)
    RaiseException(PAGE_FAULT);
else
    TLB_Insert(VPN, PTE.PFN, PTE.ProtectBits);
```

## Key Trade-offs

- **Size vs speed**: Larger TLBs = more coverage but slower lookup
- **Replacement policy**: LRU approximations common...

## Connections

- On a [[Context switch requires TLB flush or ASID tagging|context switch]], the TLB must be invalidated or tagged
- Works with [[Multi-level page tables reduce memory overhead|multi-level page tables]] to keep page table memory low
```

### Folder Structure

```
OSTEP-PKM/
├── Virtualization/
│   ├── Virtualization MOC.md
│   ├── Processes - Chapter Overview.md
│   ├── A process is a running program.md
│   ├── Process states describe lifecycle transitions.md
│   ├── fork creates a new process by copying the parent.md
│   ├── ...
│   ├── Scheduling - Chapter Overview.md
│   ├── MLFQ uses multiple queues with priority feedback.md
│   ├── ...
│   ├── Memory - Chapter Overview.md
│   ├── TLB is a hardware cache for address translation.md
│   └── ...
├── Concurrency/
│   ├── Concurrency MOC.md
│   ├── Threads - Chapter Overview.md
│   ├── A thread shares address space with other threads.md
│   ├── ...
│   ├── Locks - Chapter Overview.md
│   ├── Test-and-set provides atomic lock acquisition.md
│   └── ...
└── Persistence/
    ├── Persistence MOC.md
    ├── IO Devices - Chapter Overview.md
    ├── DMA offloads data transfer from the CPU.md
    ├── ...
    ├── File Systems - Chapter Overview.md
    ├── An inode stores file metadata and block pointers.md
    └── ...
```

---

## Technical Considerations

- **Obsidian compatibility**: All wikilinks must use `[[Note Title]]` syntax (not `[[folder/note]]` — Obsidian resolves by title)
- **File naming**: Note filenames = note titles (declarative statements), no special characters except periods and hyphens
- **Frontmatter parsing**: YAML must be valid — quote strings containing colons, use proper list syntax
- **Graph density**: Target 3-5 links per note (2 minimum) to create a connected but not over-linked graph
- **DAG validation**: The `prerequisites` graph must be acyclic — foundational concepts have `prerequisites: []`

---

## Quality Gates

Every note MUST pass all 6 gates before being considered complete:

| Gate | Definition | Check |
|------|-----------|-------|
| **Atomic** | One concept per note | Title is a single declarative statement |
| **Complete** | Self-contained understanding | Reader doesn't need to open another note to grasp the concept |
| **Practical** | Includes example or analogy | Has code snippet, worked example, or real-world analogy |
| **Future-proof** | No temporal references | No "recently", "new", "modern" — state facts timelessly |
| **Connected** | Minimum 2 wikilinks | `related` field has ≥2 entries; body uses inline wikilinks |
| **Scannable** | Uses formatting for quick reading | Has headers, bullets/lists, callout, and/or code blocks |

---

## Success Metrics

- All ~50 OSTEP chapters converted to atomic notes (150-300 total notes)
- Every note passes all 6 quality gates
- The Obsidian graph view shows a connected graph (no orphan notes)
- `prerequisites` fields form a valid learning DAG from foundational → advanced concepts
- A student can trace any concept to its prerequisites and related ideas via wikilinks
- Cross-theme links exist for at least: process↔thread, address space↔file system memory, interrupt↔I/O, scheduling↔concurrency

---

## Open Questions

- Should dialogue/intro chapters (Chapters 1, 19, 29) produce only overview notes, or also atomic concept notes?
- Should the vault include a top-level `OSTEP MOC.md` that links to all three theme MOCs?
- For the distributed systems chapters (41-43): should these live in `Persistence/` or warrant a sub-grouping?
- How to handle OSTEP "asides" and "tips" — inline in relevant notes, or separate pattern-type notes?
