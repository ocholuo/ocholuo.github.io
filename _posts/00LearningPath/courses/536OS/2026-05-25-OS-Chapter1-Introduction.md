---
title: "Meow's 536OS - 1. Introduction to Operating Systems"
date: 2026-05-25 11:11:11 -0400
categories: [00LearningPath, 536OS]
tags: [536OS, operating-systems, computer-architecture, interrupts, storage-hierarchy, multiprocessor, NUMA, virtualization, multiprogramming, DMA, bootstrap]
math: false
toc: true
image: ""
---

# 1. Introduction to Operating Systems

---

> Source: CS 536 Operating Systems — Chapter 1: Introduction

---

## Overview

An <font color=OrangeRed>operating system</font> is software that manages a computer's hardware, provides a basis for application programs, and acts as an intermediary between the computer user and the computer hardware.

**OS goals:**

- Execute user programs and make solving user problems easier
- Make the computer system convenient to use
- Use computer hardware in an efficient manner

---

## 1.1 What Operating Systems Do 操作系统的作用

A computer system can be divided into four components:

| Component | Role |
|---|---|
| <font color=OrangeRed>Hardware</font> | Provides basic computing resources: CPU, memory, I/O devices |
| <font color=OrangeRed>Operating System</font> | Controls hardware, coordinates its use among applications and users |
| <font color=OrangeRed>Application Programs</font> | Define how resources solve user problems (compilers, browsers, word processors) |
| <font color=OrangeRed>User</font> | People, machines, or other computers |

The operating system consists of hardware, software, and data. It provides proper use of these resources and simply provides an environment within which programs can do useful work.

![Layered architecture showing multiple users interacting with system/application programs, which sit above the operating system, which sits above computer hardware](./assets/img/post/os-layers-computer-system-components.png)

![Figure 1.1 — Abstract view of the components of a computer system: user at top, then application programs (compilers, web browsers), then operating system, then computer hardware (CPU, memory, I/O devices) at the bottom](./assets/img/post/os-abstract-view-computer-system.png)

### 1.1.1 User View 用户视角

The user's view of the computer varies according to the interface being used.

- **Personal workstation**: designed for ease of use — performance and security take priority over resource utilization
- **Shared computer** (mainframe/minicomputer): must keep all users satisfied, resource sharing is important
- **Handheld computers**: resource-poor, optimized for usability and battery life
- **Embedded computers**: designed primarily to run without user intervention (home devices, automobiles)

Increasingly, users interact through touch screens, physical keyboards, voice recognition interfaces (like Siri), and cellular/wireless networks.

### 1.1.2 System View 系统视角

From the computer's point of view, the operating system is the program most intimately involved with the hardware.

- <font color=OrangeRed>Resource allocator</font>: manages all resources (CPU time, memory space, storage space, I/O devices), faces conflicting requests and decides how to allocate them efficiently and fairly
- <font color=OrangeRed>Control program</font>: manages the execution of user programs to prevent errors and improper use; especially concerned with I/O device operation and control

### 1.1.3 Defining Operating Systems 定义

Operating systems have no completely adequate universal definition.

- Computing started with fixed-purpose military/governmental systems; general-purpose mainframes gave birth to operating systems
- In the 1960s, Moore's Law predicted transistor count doubling every 18 months — computers shrank and gained functionality, leading to a vast variety of operating systems
- The fundamental goal: execute programs and make solving user problems easier
- The common functions of controlling and allocating resources are brought together into one piece of software: the OS
- The one program running at all times on the computer is the <font color=OrangeRed>kernel</font>; everything else is either a system program or an application program

---

## 1.2 Computer-System Organization 计算机系统组织

### 1.2.0 Hardware Organization 硬件组织

A modern computer system consists of one or more CPUs and a number of <font color=OrangeRed>device controllers</font> connected through a <font color=OrangeRed>common bus</font> (provides access between components and shared memory).

- Each device controller maintains a <font color="blue">local buffer storage</font> and a set of special-purpose registers
- Device controllers are responsible for moving data between the peripheral devices they control and their local buffer storage
- The CPU moves data between main memory and local buffers
- The CPU and device controllers can execute in parallel, competing for memory cycles — a <font color="blue">memory controller</font> synchronizes access to shared memory

The OS has a <font color="blue">device driver</font> for each device controller. The device driver understands the controller and provides a uniform interface to the rest of the OS.

![Hardware bus diagram showing CPU, disk controller, USB controller, and graphics adapter all connected to a shared memory bus, with peripheral devices (disks, mouse, keyboard, printer, monitor) attached to their respective controllers](./assets/img/post/os-hardware-bus-system-organization.png)

**Bootstrap program:**

- Stored in ROM or EPROM, known as <font color=OrangeRed>firmware</font>
- Runs at power-up or reboot
- Initializes all aspects of the system (CPU registers, device controllers, memory contents)
- Knows how to load the OS kernel and start executing it
- Locates the OS kernel and loads it into memory

---

### 1.2.1 Interrupts 中断

#### Overview 概述

When the CPU and a peripheral device interact during I/O, two approaches exist for detecting completion:

| Approach | Mechanism | Drawback |
|---|---|---|
| <font color=OrangeRed>Polling 轮询</font> | CPU repeatedly queries device for completion | Unnecessary CPU consumption |
| <font color=OrangeRed>Vectored interrupt system 中断</font> | Device signals CPU asynchronously on completion | More efficient — CPU executes other processes while waiting |

In an interrupt-driven system:
1. Device driver loads appropriate registers in the device controller
2. Device controller examines the registers and starts data transfer
3. On completion, device controller causes an <font color=OrangeRed>interrupt</font> (sends a signal via the system bus)
4. CPU stops current task, saves state, and transfers control to the <font color=OrangeRed>interrupt handler</font>
5. Interrupt handler processes the event and returns control to the interrupted task

![Figure 1.4 — Interrupt-driven I/O cycle: 7-step flowchart showing device driver initiating I/O, device controller performing operation, signaling completion via interrupt, CPU transferring control to interrupt handler, and resuming the interrupted task](./assets/img/post/os-interrupt-driven-io-cycle.png)

![Linux interrupt handling flow: hardware generates interrupt → interrupt controller signals processor → do_IRQ() checks for handler → handle_IRQ_event() or ret_from_intr()](./assets/img/post/os-interrupt-linux-irq-handler-flow.jpg)

![Interrupt I/O cycle timing waveform showing CPU (user program and interrupt processing) and I/O device (idle vs. transferring) signal states over time, with I/O request, transfer done, interrupt signaled, and interrupt handled events](./assets/img/post/os-interrupt-io-cycle-timing-waveform.jpg)

#### Implementation 实现机制

The basic interrupt mechanism:

1. The CPU hardware has an <font color=OrangeRed>interrupt-request line</font> that the CPU senses after executing every instruction
2. When a device controller asserts a signal on the interrupt-request line, the CPU reads the <font color="blue">interrupt number</font> and jumps to the corresponding <font color=OrangeRed>interrupt handler</font> via the <font color=OrangeRed>interrupt vector</font>
3. The interrupt handler:
   - Saves any state it will change during operation
   - Determines the cause of the interrupt
   - Performs necessary processing
   - Restores state
   - Executes a return-from-interrupt instruction

**Interrupt types:**

- <font color=OrangeRed>Maskable interrupts</font>: can be disabled by the CPU when executing a critical, non-interruptible sequence
- <font color=OrangeRed>Nonmaskable interrupts</font>: reserved for events like unrecoverable memory errors
- <font color="blue">Interrupt chaining</font>: used when more interrupt handlers exist than elements in the interrupt vector — each element points to the head of a list of handlers

#### Two I/O Methods 两种I/O方式

| Method | Behavior |
|---|---|
| <font color=OrangeRed>Synchronous I/O</font> | Control returns to user program only upon I/O completion; CPU idles waiting |
| <font color=OrangeRed>Asynchronous I/O</font> | Control returns to user program without waiting; system call allows user to wait for completion; OS maintains a device-status table |

![Synchronous vs asynchronous I/O timing diagram: in synchronous I/O the requesting process blocks waiting for the kernel to handle data transfer; in asynchronous I/O the requesting process continues executing concurrently](./assets/img/post/os-sync-async-io-comparison.png)

---

### 1.2.2 Storage Structure 存储结构

#### Storage Definitions and Notation 存储定义

| Unit | Definition |
|---|---|
| <font color=OrangeRed>Bit</font> | Basic unit of computer storage — holds 0 or 1 |
| <font color=OrangeRed>Byte</font> | 8 bits; smallest convenient chunk of storage for most computers |
| <font color="blue">Word</font> | A computer architecture's native unit of data — one or more bytes (e.g., 64-bit architecture → 8-byte word) |
| KB | 1,024 bytes = 2¹⁰ bytes |
| MB | 1,024² bytes ≈ 1 million bytes |
| GB | 1,024³ bytes ≈ 1 billion bytes |
| TB | 1,024⁴ bytes |
| PB | 1,024⁵ bytes |

Note: Networking measurements are given in bits (networks move data a bit at a time), while computer storage is generally measured in bytes.

#### Storage Hierarchy 存储层次

Main memory is the only large storage medium the CPU can access directly.

| Tier | Type | Properties |
|---|---|---|
| <font color=OrangeRed>Primary</font> | Registers, cache, main memory (DRAM) | Fast, volatile (loses content on power-off) |
| <font color=OrangeRed>Secondary</font> | Hard disks (HDD), solid-state disks (SSD) | Large, nonvolatile |
| <font color=OrangeRed>Tertiary</font> | Optical disks, magnetic tapes | Largest capacity, slowest |

![Figure 1.6 — Storage-device hierarchy pyramid: from top (fastest/smallest: registers, cache, main memory) down through nonvolatile memory and hard-disk drives to optical disks and magnetic tapes (largest/slowest), with primary, secondary, and tertiary storage tiers labeled](./assets/img/post/os-storage-device-hierarchy.png)

**Key properties:**

- <font color=OrangeRed>Main memory</font>: random access, volatile, implemented in DRAM — the only storage a CPU can load instructions from directly
- <font color="blue">Bootstrap program</font>: cannot be stored in RAM (volatile) — stored in ROM/firmware
- <font color=OrangeRed>Secondary storage</font>: extends main memory, provides large nonvolatile storage
  - Hard disks: rigid platters covered in magnetic recording material; surface divided into tracks subdivided into sectors; disk controller manages logical interaction
  - Solid-state disks (SSD): faster than HDD, nonvolatile, increasingly popular

---

### 1.2.3 I/O Structure 输入输出结构

<font color=OrangeRed>Direct Memory Access (DMA)</font> solves the high-overhead problem of interrupt-driven I/O for bulk data movement:

- Used for high-speed I/O devices able to transmit at near memory speeds
- After the OS sets up buffers, pointers, and counters for the I/O device, the <font color="blue">device controller</font> transfers an entire block of data directly between the device buffer and main memory — with no CPU intervention
- Only one interrupt per block (vs. one interrupt per byte for low-speed devices)
- While the device controller performs the transfer, the CPU is available for other tasks

The form of interrupt-driven I/O is fine for small amounts of data, but produces high overhead for bulk data such as NVS I/O. DMA removes that overhead.

![Figure 1.7 — How a modern computer system works: relationships between CPU (with cache and thread of execution), memory (instructions and data), and devices — showing instruction execution cycle, data movement, I/O request/data/interrupt signals, and DMA direct memory access path](./assets/img/post/os-modern-computer-system-works.png)

---

## 1.3 Computer-System Architecture 计算机系统架构

### Definitions 定义

| Term | Definition |
|---|---|
| <font color=OrangeRed>Processor</font> | Physical chip containing one or more CPUs |
| <font color=OrangeRed>CPU</font> | Hardware that executes instructions |
| <font color=OrangeRed>Core</font> | Basic computation unit of the CPU |
| <font color=OrangeRed>Multicore</font> | Multiple computing cores on the same CPU |
| <font color=OrangeRed>Multiprocessor</font> | Multiple processors in the system |

### 1.3.1 Single-Processor Systems 单处理器系统

- One main CPU with a single processing core — capable of executing a general-purpose instruction set including process instructions
- The core executes instructions and has registers for local data storage
- May include special-purpose processors (disk/keyboard/graphics controllers) that run a limited instruction set and do not run processes
- Special-purpose processors relieve the main CPU of overhead (e.g., disk controller manages its own disk queue and scheduling algorithm; keyboard microprocessor converts keystrokes into codes)

### 1.3.2 Multiprocessor Systems 多处理器系统

Multiprocessor systems (two or more processors, each with a single-core CPU) now dominate the computing landscape. Processors share the bus, and sometimes clock, memory, and peripheral devices.

Also known as: <font color="blue">parallel systems</font>, <font color="blue">tightly-coupled systems</font>

**Advantages:**
- <font color=OrangeRed>Increased throughput</font>: N processors allow many processes to run simultaneously; speed-up ratio is less than N due to overhead and resource contention
- <font color=OrangeRed>Economy of scale</font>: multiprocessors cost less than equivalent single-processor systems
- <font color=OrangeRed>Increased reliability</font>: graceful degradation / fault tolerance — if one processor fails, others continue; no significant performance deterioration

**Two types of multiprocessing:**

| Type | Behavior |
|---|---|
| <font color=OrangeRed>Asymmetric Multiprocessing</font> | Each processor is assigned a specific task; boss processor controls others |
| <font color=OrangeRed>Symmetric Multiprocessing (SMP)</font> | Each processor performs all tasks; all processors are peers sharing main memory |

![Figure 1.8 — Symmetric multiprocessing architecture: two processors (processor0 and processor1), each containing a CPU with registers and cache, both sharing a single main memory bus](./assets/img/post/os-arch-smp-two-processor-architecture.png)

![Symmetric multiprocessing diagram showing three CPUs (CPU0, CPU1, CPU2), each with their own registers and cache, all connected to a single shared main memory](./assets/img/post/os-arch-smp-three-cpu-shared-memory.png)

#### NUMA 非均匀内存访问

Adding more CPUs to a multiprocessor system increases computing power, but the shared system bus becomes a bottleneck — performance begins to degrade.

<font color=OrangeRed>NUMA (Non-Uniform Memory Access)</font>: provide each CPU (or group of CPUs) with its own local memory accessed via a small, fast local bus. CPUs are connected by a shared system interconnect — all share one physical address space.

| Aspect | Detail |
|---|---|
| **Advantage** | Faster, no contention when CPU accesses local memory; scales more effectively as processors are added |
| **Drawback** | Increased latency when a CPU must access remote memory across the system interconnect (performance penalty) |
| **OS mitigation** | Careful CPU scheduling and memory management minimize the NUMA penalty |

NUMA systems can scale to accommodate large numbers of processors — increasingly popular on servers and HPC systems.

![Figure 1.10 — NUMA multiprocessing architecture: four CPUs (CPU0–CPU3) each with their own local memory, connected to each other via interconnect lines in a fully-connected mesh topology](./assets/img/post/os-arch-numa-four-cpu-mesh.png)

![Dual-core processor architecture: single processor chip (processor0) containing two CPU cores (core0 and core1), each with own registers and L1 cache, sharing a common L2 cache, connecting to main memory](./assets/img/post/os-arch-dual-core-processor.jpg)

**SMP vs NUMA memory topology:**

- <font color="blue">SMP (Symmetric Multi-Processor)</font>: processes allocate memory from a single memory space; consistent performance across all memory — but limited scalability due to bus contention
- <font color="blue">NUMA</font>: sections of physical memory are controlled by one or more processors (NUMA nodes); the OS sees all CPUs and memory in each NUMA node; servers now support multi-terabyte configurations because of NUMA

#### Blade Servers 刀片服务器

<font color=OrangeRed>Blade servers</font>: multiple processor boards, I/O boards, and networking boards placed in the same chassis. Each blade-processor board boots independently and runs its own operating system. Some blade boards are themselves multiprocessor — these servers consist of multiple independent multiprocessor systems.

### 1.3.3 Clustered Systems 集群系统

A <font color=OrangeRed>clustered system</font> gathers together multiple CPUs, differing from multiprocessor systems in that it is composed of two or more individual systems or nodes. Each node is typically a multicore system — considered <font color="blue">loosely coupled</font>.

- Clustered computers share storage and are closely linked via LAN or a faster interconnect (e.g., InfiniBand)
- Many cluster products support thousands of systems in a cluster, including nodes separated by miles
- <font color=OrangeRed>Storage-Area Networks (SANs)</font>: allow many systems to attach to a pool of storage; if the application and its data are stored on a SAN, the cluster software can assign the application to run on any attached host

**Clustering types:**

| Type | Behavior |
|---|---|
| <font color=OrangeRed>Asymmetric clustering</font> | One host runs the application; another is in hot-standby mode monitoring the active host |
| <font color=OrangeRed>Symmetric clustering</font> | Two or more hosts run applications and monitor each other; more efficient — uses all available hardware |

![Figure 1.11 — General structure of a clustered system: three computers interconnected via interconnect links, all sharing a common storage-area network (SAN)](./assets/img/post/os-arch-clustered-system-san.png)

---

## 1.4 Operating-System Operations 操作系统的运行

### Bootstrap and Kernel Loading 引导与内核加载

1. Computer powered up or rebooted → runs the <font color=OrangeRed>bootstrap program</font> (simple, stored in firmware)
2. Bootstrap program initializes the system (CPU registers, device controllers, memory contents)
3. Bootstrap program locates the OS kernel and loads it into memory
4. Once the kernel is loaded and executing, it starts providing services to the system and users
5. Some services are provided by <font color=OrangeRed>system daemons 守护进程</font>: loaded into memory at boot time, running the entire time the kernel is running
   - On Linux, the first system program is `systemd`, which starts many other daemons

A computer operating system typically consists of:

- Process management
- Main memory management
- File management
- I/O system management
- Secondary storage management
- Protection system

### 1.4.1 Multiprogramming and Multitasking 多道程序设计与多任务

<font color=OrangeRed>Multiprogramming</font>: increases CPU utilization by organizing programs so the CPU always has one to execute.

- The OS keeps several <font color="blue">processes</font> in memory simultaneously
- The OS picks and executes one process; when that process must wait (e.g., for I/O), the OS switches to another process
- As long as at least one process needs to execute, the CPU is never idle

<font color=OrangeRed>Multitasking (time-sharing)</font>: an extension of multiprogramming where the CPU switches among jobs so frequently that users can interact with each program while it runs.

- Requires an interactive computer system with direct communication between user and system
- Response time should be less than one second
- Requires: <font color="blue">CPU scheduling</font> (if multiple processes are ready), <font color="blue">swapping</font> (if processes don't fit in memory), <font color="blue">virtual memory</font> (executing processes larger than physical memory)

---

## 1.5 Storage Management 文件系统管理

The operating system provides a uniform, logical view of information storage — abstracting from the physical properties of storage devices to define a logical storage unit: the <font color=OrangeRed>file</font>.

- The OS maps files onto physical media and accesses them via storage devices
- A file is a collection of related information defined by its creator — commonly programs (source and object forms) and data
- Files may be free-form (text files) or formatted rigidly (fixed-format records)

**OS file-management responsibilities:**
- Creating and deleting files and directories
- Supporting primitives for manipulating files and directories
- Mapping files onto secondary storage
- Backing up files on stable storage

---

## 1.6 Data Structures 数据结构基础

### 1.6.1 Lists, Stacks, and Queues

An <font color="blue">array</font> is a simple data structure where each element can be accessed directly (e.g., main memory is constructed as an array).

A <font color=OrangeRed>linked list</font> is a collection of data values as a sequence, where items are linked to one another:

| Type | Structure |
|---|---|
| <font color="blue">Singly linked list</font> | Each item points to its successor |
| <font color="blue">Doubly linked list</font> | Each item can refer to either its predecessor or successor |
| <font color="blue">Circularly linked list</font> | Last element points back to the first element |

Linked lists accommodate items of varying sizes and can accommodate insertion or deletion while preserving order — better suited than arrays when size varies or order must be preserved during insertions/deletions.

---

## 1.7 Virtualization 虚拟化

<font color=OrangeRed>Virtualization</font>: a technology that abstracts the hardware of a single computer (CPU, memory, disk drives, network interface cards) into several different execution environments, creating the illusion that each separate environment is running on its own private computer.

- Each virtual environment can run a different operating system (e.g., Windows and UNIX simultaneously)
- A user of a virtual machine can switch among operating systems in the same way a user can switch among processes in a single OS
- Virtualization allows operating systems to run as applications within other operating systems

**Virtualization vs Emulation:**

| Concept | Description |
|---|---|
| <font color=OrangeRed>Virtualization</font> | Guest OS compiled natively for the CPU; runs on a virtual machine manager (VMM/hypervisor) |
| <font color="blue">Emulation</font> | Simulates computer hardware in software; typically used when the source CPU type is different from the target CPU type |

---

## 1.8 Distributed Systems 分布式系统

A <font color=OrangeRed>distributed system</font> is a collection of physically separate, possibly heterogeneous computer systems that are networked to provide users with access to various shared resources.

- Access to shared resources increases computation speed, functionality, data availability, and reliability
- Some operating systems generalize network access as a form of file access (network interface's device driver handles networking details)
- TCP/IP is the most common network protocol — provides the fundamental architecture of the Internet; most operating systems (including all general-purpose ones) support it

**Example protocols and systems:**

- <font color="blue">FTP</font>: file transfer with explicit network function invocation
- <font color="blue">NFS</font>: network file system treated like local file access
- Systems typically contain a mix of both modes

---

## Key Takeaways

- <font color=OrangeRed>OS roles</font>: resource allocator (manages CPU, memory, I/O), control program (prevents errors and improper use), and kernel (the one program always running).
- <font color=OrangeRed>Computer system components</font>: hardware → OS → application programs → user; OS is the intermediary coordinating hardware use.
- <font color=OrangeRed>Interrupt-driven I/O</font>: device signals CPU via interrupt-request line on completion; CPU jumps to interrupt handler via interrupt vector; saves state, processes, restores, returns. More efficient than polling.
- <font color=OrangeRed>Two I/O methods</font>: synchronous (CPU waits) vs asynchronous (CPU continues; device-status table tracks completion).
- <font color=OrangeRed>DMA</font>: device controller transfers entire data blocks directly to/from main memory without CPU intervention — one interrupt per block instead of one per byte.
- <font color=OrangeRed>Storage hierarchy</font>: registers → cache → DRAM (volatile, CPU-accessible) → secondary (HDD/SSD, nonvolatile) → tertiary (tape/optical). Bootstrap stored in ROM/firmware, not volatile RAM.
- <font color=OrangeRed>SMP vs NUMA</font>: SMP shares one memory bus (limited scalability); NUMA gives each CPU local memory for faster access and better scaling, at the cost of remote-memory latency.
- <font color=OrangeRed>Multiprocessor advantages</font>: increased throughput, economy of scale, fault tolerance via graceful degradation.
- <font color=OrangeRed>Clustered systems</font>: loosely-coupled nodes sharing SAN storage; asymmetric (hot-standby) or symmetric (both active, monitoring each other).
- <font color=OrangeRed>Multiprogramming</font>: keep CPU busy by switching to another process when current one waits. Multitasking: frequent switching for interactive response (< 1 second).
- <font color=OrangeRed>Virtualization</font>: abstracts hardware into multiple execution environments; each VM appears to run on its own private computer. Emulation simulates a different CPU type.

## References

- Operating System Concepts — Silberschatz, Galvin & Gagne, Chapter 1 (Introduction)
- CS 536 Operating Systems — Lecture notes: Chapter 1
