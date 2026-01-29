---
type: mechanism
source: "OSTEP Ch. 27: Interlude: Thread API"
tags:
  - concurrency
  - events
  - coding-style
related:
  - "[[Event-Based Concurrency Relies on an Event Loop]]"
  - "[[Blocking Calls Freeze Event-Based Systems]]"
  - "[[Thread Creation and Execution Model]]"
prerequisites:
  - "[[Event-Based Concurrency Relies on an Event Loop]]"
  - "[[Stack and Heap Occupy Opposite Ends of the Address Space]]"
---

> [!SUMMARY]
> "Stack Ripping" is the primary programming difficulty in event-based systems. Because a function cannot block, any logic that requires waiting for I/O must be split into two parts: the call that initiates the operation and the callback that runs upon completion. This forces the programmer to manually save and restore state that the compiler normally manages automatically on the stack.

# The Problem of Stack Ripping

In a traditional threaded program, state is preserved on the stack. If a function `do_work()` calls `read()`, the local variables of `do_work` sit safely on the stack frame while the thread sleeps. When `read()` returns, execution resumes exactly where it left off, with all context intact.

In an event-based system, you cannot sleep. You must initiate the read and then **return** to the event loop so it can process other events. This requirement forces you to rip the function in half.

## Before: Procedural Code

```c
void do_work() {
    int id = get_id();           // Local variable
    char *buf = malloc(1024);    // Local variable
    read(fd, buf, 1024);         // BLOCKING CALL
    process(id, buf);            // Use variables after read
}
```

## After: Event-Driven Code

To make this non-blocking, we split it into a start function and a callback handler:

```c
// Part 1: Start the operation
void do_work_start() {
    int id = get_id();
    char *buf = malloc(1024);
    
    // We must manually package this state!
    struct request *req = malloc(sizeof(struct request));
    req->id = id;
    req->buf = buf;
    
    aio_read(fd, buf, 1024, do_work_finish, req); // Register callback
    // Function RETURNS here - stack is destroyed!
}

// Part 2: The Callback
void do_work_finish(struct request *req) {
    // Manually unpack state
    int id = req->id;
    char *buf = req->buf;
    
    process(id, buf);
    free(req);
}
```

## The Burden of Manual Management

This transformation is called **stack ripping**. The programmer must explicitly define a data structure (`struct request`) to hold what would have been local variables. Every blocking point in the logical flow becomes a rupture point in the code, requiring:
1.  Defining a state struct.
2.  Packaging state before the call.
3.  Unpacking state in the callback.

This manual stack management makes event-based code significantly harder to write, read, and debug than threaded code. It obscures the control flow and scatters related logic across multiple functions. Modern languages use features like **Closures**, **Promises**, and **async/await** to sweeten this syntax, but the underlying requirement to heap-allocate the context remains.
