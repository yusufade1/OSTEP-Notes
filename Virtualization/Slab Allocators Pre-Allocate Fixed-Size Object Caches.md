---
type: atomic
source: OSTEP Ch. 17
tags:
  - virtualization
  - memory
  - free-space-management
  - allocation-strategy
related:
  - "[[The Buddy System Enables Fast Coalescing Through Power-of-Two Sizes]]"
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[malloc and free Manage Heap Memory Dynamically]]"
  - "[[Splitting and Coalescing Keep the Free List Efficient]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[Splitting and Coalescing Keep the Free List Efficient]]"
---

# Slab Allocators Pre-Allocate Fixed-Size Object Caches

> [!SUMMARY]
> Slab allocation creates dedicated caches for frequently allocated object types (like inodes, PCBs, or network buffers), pre-dividing memory into fixed-size slots that exactly match the object size. Allocation and deallocation become O(1) free-list operations with no splitting, coalescing, or fragmentation. The slab allocator was invented by Jeff Bonwick for SunOS and is used in Linux, FreeBSD, and other kernels.

## The Problem with General Allocators

Kernels frequently allocate and free objects of the same type: process control blocks, file descriptors, buffer headers. A general-purpose allocator like [[First-Fit and Next-Fit Trade Search Time for Simplicity|first-fit]] treats each as a variable-size request, repeatedly splitting and coalescing. This overhead is wasteful when the same sizes recur constantly.

## Slab Structure

A **slab** is a contiguous memory region divided into slots of identical size:

```
Slab for 128-byte objects:
+------+------+------+------+------+------+------+------+
| obj0 | obj1 | obj2 | obj3 | obj4 | obj5 | obj6 | obj7 |
+------+------+------+------+------+------+------+------+
  free   used   used   free   free   used   free   free

Free list: obj0 → obj3 → obj4 → obj6 → obj7
```

Each object type (inode, task_struct, etc.) has its own **cache** consisting of one or more slabs. Objects are never split—they are exactly the required size.

## Allocation and Deallocation

**Allocation**: Pop an object from the cache's free list. If the free list is empty, allocate a new slab from the [[The Buddy System Enables Fast Coalescing Through Power-of-Two Sizes|buddy allocator]] and partition it into slots.

```c
void *slab_alloc(cache_t *cache) {
    if (cache->free_list == NULL) {
        slab_grow(cache);  // Get new slab from buddy allocator
    }
    void *obj = cache->free_list;
    cache->free_list = obj->next;
    return obj;
}
```

**Deallocation**: Push the object back onto the cache's free list.

```c
void slab_free(cache_t *cache, void *obj) {
    obj->next = cache->free_list;
    cache->free_list = obj;
}
```

Both operations are O(1). No search, no splitting, no coalescing.

## Additional Optimizations

**Object constructors**: Many objects require initialization (zeroing, setting magic numbers). The slab allocator can pre-initialize objects when the slab is created, so allocation returns a ready-to-use object.

**Cache coloring**: Different slabs offset their starting position to reduce cache line conflicts when multiple objects from the same cache are accessed together.

**Magazine layer**: Modern implementations (like Solaris's vmem) add per-CPU caches to avoid lock contention on the global free list.

## Trade-off Analysis

| Factor | Slab Allocator Behavior |
|--------|------------------------|
| **Allocation time** | O(1) |
| **Fragmentation** | Zero (exact-fit objects) |
| **Memory overhead** | Per-cache metadata, possible unused slots |
| **Flexibility** | Only efficient for known, fixed-size objects |

**The trade-off**: Slab allocators are spectacularly efficient for their target workload (repeated same-size allocations) but require knowing object sizes in advance. They complement, rather than replace, general-purpose allocators. The Linux kernel uses slabs for kernel objects atop a buddy allocator for page-level management.

## Design Insight

Slab allocation exemplifies a key systems principle: **specialize the common case**. By recognizing that most kernel allocations are repetitive, the slab allocator eliminates the overhead of generality where it is not needed.
