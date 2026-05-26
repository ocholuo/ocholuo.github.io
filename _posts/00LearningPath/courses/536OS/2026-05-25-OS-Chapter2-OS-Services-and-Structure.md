---
title: "Meow's 536OS - 2. Operating System Services, Interfaces, and Structure"
date: 2026-05-25 11:11:11 -0400
categories: [00LearningPath, 536OS]
tags: [536OS, operating-systems, system-calls, OS-structure, user-interface, shell, microkernel, monolithic, GRUB, boot-process, linker-loader, BCC, eBPF]
math: false
toc: true
image: ""
---

# 2. Operating System Services, Interfaces, and Structure

---

> Source: CS 536 Operating Systems — Chapter 2: Operating-System Structures

---

## Overview

Chapter 2 covers the services an OS provides, how users and programs interact with it through interfaces and system calls, how programs are compiled and loaded, and how the OS kernel itself is structured — from monolithic to microkernel to hybrid designs.

---

## 2.1 Operating-System Services 操作系统服务

An operating system provides an environment for the execution of programs. It makes certain services available to programs and to the users of those programs. Figure 2.1 shows the common classes of OS services and how they interrelate.

![Figure 2.1 — A view of operating system services: user interfaces (GUI, touch screen, command line) sit above system calls, which expose core OS services (program execution, I/O operations, file systems, communication, resource allocation, accounting, error detection, protection and security) running on top of the hardware](./assets/img/post/os-services-overview-ch2.1-figure2.1.png)

### Services Helpful to the User 面向用户的服务

| Service | Description |
|---|---|
| <font color=OrangeRed>User Interface (UI)</font> | Almost all OSes provide a UI — GUI, touch-screen, or CLI |
| <font color=OrangeRed>Program execution</font> | Load a program into memory and run it; end normally or abnormally |
| <font color=OrangeRed>I/O operations</font> | Mediate all I/O on behalf of user programs; users cannot control devices directly |
| <font color=OrangeRed>File-system manipulation</font> | Read, write, create, delete, search, list files/directories; permissions management |
| <font color=OrangeRed>Communication</font> | Exchange information between processes on the same machine or across a network, via <font color="blue">shared memory</font> or <font color="blue">message passing</font> |
| <font color=OrangeRed>Error detection</font> | Detect and correct errors in CPU, memory, I/O devices, and user programs; take appropriate action (halt, terminate process, return error code) |

### Services for Efficient System Operation 面向系统效率的服务

| Service | Description |
|---|---|
| <font color=OrangeRed>Resource allocation</font> | Allocate CPU cycles, memory, storage, and I/O devices across multiple concurrent processes |
| <font color=OrangeRed>Logging / Accounting</font> | Track which programs use how much of which resources; used for billing or performance analysis |
| <font color=OrangeRed>Protection and security</font> | Ensure all access to system resources is controlled; require user authentication; defend against invalid external access |

**Protection vs Security:**
- <font color=OrangeRed>Protection</font>: ensures all access to system resources is controlled
- <font color=OrangeRed>Security</font>: defends against external threats — authentication, I/O device defense, break-in detection
- "A chain is only as strong as its weakest link" — both must be applied throughout the system

---

## 2.2 User and Operating-System Interface 用户与操作系统接口

Three fundamental interfaces exist between the user and the OS:

| Interface | Description |
|---|---|
| <font color=OrangeRed>Command-Line Interface (CLI)</font> | Text commands; preferred by system administrators and power users |
| <font color=OrangeRed>Graphical User Interface (GUI)</font> | Mouse-and-window system; desktop metaphor |
| <font color=OrangeRed>Touch-Screen Interface</font> | Gesture-based; used by smartphones and tablets |

### 2.2.1 Command Interpreters 命令解释器

Most OSes treat the command interpreter as a special program that runs when a process is initiated or when a user logs on. On systems with multiple interpreters, they are called <font color="blue">shells</font>.

- UNIX/Linux shells: C shell, Bourne-Again shell (bash), Korn shell, and others
- The main function of the command interpreter: **get and execute the next user-specified command**

**Two implementation approaches:**

1. **Interpreter contains the code** — the command interpreter itself executes each command; each command requires its own implementing code, making the interpreter large
2. **Commands are system programs** (used by UNIX) — the interpreter uses the command name to identify a file to load into memory and execute; adding new commands only requires creating new files; the interpreter stays small

```bash
# UNIX approach: the command interpreter finds and runs the "rm" program
rm file.txt
# equivalent to: load /bin/rm into memory, execute with argument file.txt
```

### 2.2.2 Graphical User Interface 图形用户界面

A GUI uses a <font color="blue">desktop metaphor</font>: icons represent programs, files, directories, and functions; mouse clicks invoke programs or pull down menus.

- First GUI appeared on the Xerox Alto (1973); popularized by Apple Macintosh (1980s)
- macOS uses the Aqua interface; Windows added GUI to MS-DOS in version 1.0
- UNIX traditionally CLI-dominant; KDE and GNOME are open-source GUIs for Linux/UNIX

### 2.2.3 Touch-Screen Interface 触摸屏界面

Smartphones and tablets use <font color=OrangeRed>touch-screen interfaces</font>.

- Users interact via gestures (press, swipe)
- Physical keyboard or simulated keyboard on screen
- iPad and iPhone use the <font color="blue">Springboard</font> touch-screen interface

### 2.2.4 Choice of Interface 接口选择

| Interface | Best for |
|---|---|
| **CLI** | System administrators, power users — faster, scriptable, repeatable tasks |
| **GUI** | General users — intuitive, visual, easier to learn |
| **Touch** | Mobile users — no physical keyboard required |

**Shell scripts**: CLI commands recorded in a file and run as a program (not compiled); very common on UNIX/Linux.

macOS now provides both the Aqua GUI and a CLI. Windows recent versions provide both standard GUI (desktop/laptop) and touch-screen (tablets). Mobile iOS/Android users almost exclusively use touch.

---

## 2.3 System Calls 系统调用

<font color=OrangeRed>System calls</font> provide an interface to the services made available by an operating system. Written in C/C++; low-level tasks may require assembly.

### 2.3.1 Example — File Copy Sequence

A simple `cp in.txt out.txt` operation requires many system calls:

1. Acquire input/output file names (write prompt, read input)
2. Open input file (error if not found)
3. Create/open output file (handle conflicts)
4. Loop: read from input, write to output (handle errors)
5. Close both files
6. Write completion message
7. Terminate normally

```
Acquire input file name    → write prompt to screen, accept input
Acquire output file name   → write prompt to screen, accept input
Open the input file        → if file doesn't exist, abort
Create output file         → if file exists, abort
Loop: read from input file, write to output file (until read fails)
Close output file
Write completion message
Terminate normally
```

### 2.3.2 Application Programming Interface (API) 应用程序编程接口

Most programmers design programs according to an <font color=OrangeRed>API</font> rather than invoking system calls directly. The API specifies functions, parameters, and return values.

Common APIs:
- **Windows API** — for Windows systems
- **POSIX API** — for POSIX-based systems (UNIX, Linux, macOS)
- **Java API** — for programs running on the Java virtual machine

The <font color=OrangeRed>run-time environment (RTE)</font> provides a <font color="blue">system-call interface</font> that intercepts API function calls and invokes the appropriate system calls. A number is associated with each system call; the system-call interface maintains a table indexed by those numbers.

**Why use an API instead of direct system calls?**
- **Portability**: code compiles and runs on any system supporting the same API
- **Simplicity**: actual system calls are more complex and detailed

**Example — `read()` system call (POSIX):**

```c
#include <unistd.h>
ssize_t read(int fd, void *buf, size_t count);
// fd: file descriptor to read
// buf: buffer to read into
// count: max bytes to read
// returns: bytes read; 0 = EOF; -1 = error
```

**Parameter-passing methods:**

| Method | Description |
|---|---|
| **Registers** | Simplest; limited by number of registers (Linux: <= 5 params) |
| **Block/table in memory** | Address of block passed in a register (Linux: > 5 params) |
| **Stack** | Parameters pushed; OS pops them; no limit on count or size |

### 2.3.3 Types of System Calls 系统调用类型

| Category | Examples |
|---|---|
| <font color=OrangeRed>Process control</font> | `fork()`, `exit()`, `wait()`, `exec()`, `create_process()`, `terminate_process()`, `get/set_process_attributes()`, `acquire/release_lock()` |
| <font color=OrangeRed>File management</font> | `create()`, `delete()`, `open()`, `close()`, `read()`, `write()`, `reposition()`, `get/set_file_attributes()` |
| <font color=OrangeRed>Device management</font> | `request()`, `release()`, `read()`, `write()`, `reposition()`, `get/set_device_attributes()` |
| <font color=OrangeRed>Information maintenance</font> | `time()`, `date()`, `dump()`, `get/set_process_attributes()`, `strace` (Linux) |
| <font color=OrangeRed>Communications</font> | `open/close_connection()`, `send/receive_messages()`, `shared_memory_create/attach()` |
| <font color=OrangeRed>Protection</font> | `set/get_permission()`, `allow/deny_user()` |

**Windows vs UNIX equivalents:**

| Category | Windows | UNIX |
|---|---|---|
| Process | `CreateProcess()`, `ExitProcess()`, `WaitForSingleObject()` | `fork()`, `exit()`, `wait()` |
| File | `CreateFile()`, `ReadFile()`, `WriteFile()`, `CloseHandle()` | `open()`, `read()`, `write()`, `close()` |
| IPC | `CreatePipe()`, `CreateFileMapping()`, `MapViewOfFile()` | `pipe()`, `shm_open()`, `mmap()` |
| Protection | `SetFileSecurity()`, `InitializeSecurityDescriptor()` | `chmod()`, `umask()`, `chown()` |

**Two IPC models:**

| Model | Mechanism | Best for |
|---|---|---|
| <font color=OrangeRed>Message passing</font> | Processes exchange packets via OS; connection required | Smaller data; easier for cross-computer IPC |
| <font color=OrangeRed>Shared memory</font> | Two or more processes read/write a shared memory region | Maximum speed; memory-transfer rates; requires synchronization |

**FreeBSD multitasking example:**

```bash
# fork() creates a new process
# exec() loads the program into memory
# exit() terminates and returns status code
./program &   # run in background; shell continues
```

---

## 2.4 System Services 系统服务

<font color=OrangeRed>System services</font> (also called system utilities) provide a convenient environment for program development and execution. Categories:

| Category | Description |
|---|---|
| File management | Create, delete, copy, rename, print, list files and directories |
| Status information | Date/time, memory/disk space, number of users; some systems support a <font color="blue">registry</font> |
| File modification | Text editors; commands to search or transform file contents |
| Programming-language support | Compilers, assemblers, debuggers, interpreters (C, C++, Java, Python) |
| Program loading and execution | Absolute/relocatable loaders, linkage editors, overlay loaders, debuggers |
| Communications | Virtual connections among processes, users, computers (web browser, email, remote login, file transfer) |
| Background services (daemons) | Launched at boot; run until system halted (network daemons, process schedulers, print servers, error monitors) |

The view of the OS seen by most users is defined by application and system programs, not the underlying system calls.

---

## 2.5 Linkers and Loaders 链接器与加载器

A program resides on disk as a binary executable. To run, it must be loaded into memory within a process context.

**Compilation pipeline:**

```
main.c
  ↓  gcc -c main.c          (compiler)
main.o                       (relocatable object file)
  ↓  gcc -o main main.o -lm  (linker)
main                         (executable)
  ↓  ./main                  (loader)
program in memory
```

| Step | Tool | Description |
|---|---|---|
| Compile | Compiler | Source → <font color="blue">relocatable object file</font> (can be loaded at any physical address) |
| Link | <font color=OrangeRed>Linker</font> | Combine relocatable object files into a single binary executable; include libraries |
| Load | <font color=OrangeRed>Loader</font> | Load binary into memory within the address space of a new process; perform <font color="blue">relocation</font> (assign final addresses) |

On UNIX: `fork()` creates the process, `exec()` invokes the loader.

**Dynamic linking:** Most systems allow libraries to be linked at load/run time (<font color="blue">DLLs</font> on Windows). Advantages: avoids loading unused libraries; multiple processes can share the same dynamically linked library.

**Executable formats:**
- UNIX/Linux: <font color=OrangeRed>ELF</font> (Executable and Linkable Format) — separate formats for relocatable and executable files
- Windows: <font color="blue">PE</font> (Portable Executable)
- macOS: <font color="blue">Mach-O</font>

```bash
file main.o   # ELF relocatable file
file main     # ELF executable
readelf main  # inspect ELF sections
```

---

## 2.6 Why Applications Are Operating-System Specific 应用程序的操作系统特异性

Applications compiled on one OS are generally not executable on other OSes, due to:

1. **Binary format** — each OS defines the layout of headers, instructions, and variables in executable files
2. **CPU instruction sets** — only applications with the appropriate instructions can execute correctly
3. **System calls** — OSes differ in system-call names, numbering, operands, ordering, and return values

**Three ways to achieve portability:**

| Approach | Mechanism | Tradeoff |
|---|---|---|
| Interpreted language | Interpreter (Python, Ruby) runs on multiple OSes | Slower; subset of OS features |
| Virtual machine | Java RTE/JVM runs bytecode on any platform where RTE is available | Slower; complex deployment |
| Standard API + porting | POSIX API; compile natively for each OS | Best performance; requires porting effort per OS |

**ABI vs API:**
- <font color=OrangeRed>API</font>: application-level interface (functions, parameters, return values)
- <font color=OrangeRed>ABI (Application Binary Interface)</font>: architecture-level interface — address width, parameter passing, stack organization, binary format, data type sizes; specific to a CPU architecture + OS pair (e.g., ARMv8 ABI)

---

## 2.7 Operating-System Design and Implementation 操作系统的设计与实现

### 2.7.1 Design Goals 设计目标

Requirements split into two groups:

| Group | Concerns |
|---|---|
| <font color=OrangeRed>User goals</font> | Convenient to use, easy to learn, reliable, safe, fast |
| <font color=OrangeRed>System goals</font> | Easy to design/implement/maintain; flexible, reliable, error-free, efficient |

There is no unique solution — different requirements lead to vastly different systems (e.g., VxWorks RTOS vs Windows Server).

### 2.7.2 Mechanisms and Policies 机制与策略

The most important principle: separate <font color=OrangeRed>policy</font> from <font color=OrangeRed>mechanism</font>.

| Concept | Definition | Example |
|---|---|---|
| <font color=OrangeRed>Mechanism</font> | Determines **how** to do something | Timer construct ensures CPU protection |
| <font color=OrangeRed>Policy</font> | Determines **what** will be done | How long the timer is set for a particular user |

**Why separate them?** Policies change over time and across environments. A general mechanism flexible enough to work across a range of policies avoids the need to change the mechanism every time the policy changes.

- **Microkernel OSes**: almost policy-free mechanisms; policies added via user-created modules
- **Windows/macOS**: mechanism and policy tightly encoded in the system; enforces global look and feel
- **Linux**: open-source; anyone can modify the scheduler or other policy components

### 2.7.3 Implementation 实现

Early OSes: assembly language. Modern OSes: mainly C/C++; small amounts of assembly for low-level hardware interaction.

**Android layered implementation:**
- Kernel: mostly C + some assembly
- System libraries: C or C++
- Application frameworks: mostly Java

**Advantages of high-level language:**
- Faster to write, more compact, easier to debug
- Compiler improvements benefit the whole OS
- Easier to port to new hardware

**Performance note:** Major performance improvements come from better data structures and algorithms, not assembly optimization. Critical routines (interrupt handlers, I/O manager, memory manager, CPU scheduler) can be optimized after the system works correctly.

---

## 2.8 Operating-System Structure 操作系统结构

### 2.8.1 Monolithic Structure 单体结构

All OS functionality in a single, static binary running in a single address space. Example: original UNIX, Linux.

```
Users
  ↓
shells / compilers / system libraries
  ↓ (system-call interface)
kernel: file system, CPU scheduling, memory management, I/O, device drivers
  ↓ (kernel interface to hardware)
hardware: terminals, disks, memory
```

**Linux kernel structure (Figure 2.13):**

```
applications
  ↓ (glibc standard C library)
system-call interface
  ↓
kernel: file systems, CPU scheduler, networks (TCP/IP), memory manager, block/character devices, device drivers
  ↓
hardware
```

- **Advantages**: minimal system-call overhead; fast intra-kernel communication; high performance
- **Disadvantages**: difficult to implement and extend; changes in one area can affect others (tightly coupled)

Linux is monolithic but modular — the kernel can be modified at run time via loadable kernel modules.

### 2.8.2 Layered Approach 分层方法

OS divided into layers, each implemented using only operations provided by lower layers.

```
Layer N: user interface
Layer N-1: ...
Layer 1: hardware abstraction
Layer 0: hardware
```

- **Advantage**: simplicity of construction and debugging — each layer verified independently
- **Disadvantage**: poor performance (user programs traverse multiple layers); difficult to define layer boundaries cleanly
- Used in networking (TCP/IP) and web applications; rarely used as the sole OS structure

### 2.8.3 Microkernels 微内核

Developed by Carnegie Mellon in the mid-1980s (Mach). Removes all nonessential components from the kernel; implements them as user-level programs in separate address spaces.

**Minimal kernel provides:**
- Basic process and memory management
- Communication (message passing / IPC)

**Client programs communicate with services via message passing through the microkernel — never directly.**

| Aspect | Detail |
|---|---|
| <font color=OrangeRed>Advantage</font> | Easier to extend (add services in user space); easier to port; more security/reliability (service failures don't crash the kernel) |
| <font color=OrangeRed>Disadvantage</font> | Performance overhead — messages must be copied between separate address spaces; process switches to exchange messages |

Examples: **Darwin** (macOS/iOS kernel component — combines Mach microkernel + BSD), **QNX** (real-time embedded OS).

### 2.8.4 Modules 可加载内核模块

The best current methodology: <font color=OrangeRed>Loadable Kernel Modules (LKMs)</font>. The kernel has core components; additional services are linked in dynamically at boot time or run time.

- Core services (CPU scheduling, memory management) built directly into the kernel
- Support for different file systems, device drivers added via loadable modules
- Similar to layered system (protected interfaces) but more flexible (any module can call any other)
- More efficient than microkernel (no message passing needed between modules)

```bash
# Linux LKM operations
insmod  mymodule.ko   # insert module
rmmod   mymodule.ko   # remove module
lsmod                 # list loaded modules
# USB device plugged in → kernel dynamically loads the driver
```

### 2.8.5 Hybrid Systems 混合结构

Most real OSes combine multiple approaches.

| OS | Structure | Notes |
|---|---|---|
| **Linux** | Monolithic + modular | Single address space (performance) + LKMs (extensibility) |
| **Windows** | Mostly monolithic + microkernel elements | Operating-system personalities run as user-mode processes; supports dynamically loadable modules |
| **macOS/iOS** | Hybrid (Darwin = Mach + BSD) | Mach microkernel + BSD kernel in same address space (avoids message-passing overhead) |
| **Android** | Linux-based + ART VM + HAL | Modified Linux kernel + Bionic C library + ART ahead-of-time compiler |

**macOS/iOS architecture layers:**

```
User experience (Aqua / Springboard)
Application frameworks (Cocoa / Cocoa Touch)
Core frameworks (QuickTime, OpenGL)
Kernel environment — Darwin (Mach microkernel + BSD)
```

Darwin provides two system-call interfaces: **Mach traps** and **BSD POSIX system calls**. All services run in the same address space — message passing within Mach requires no copying.

**Android architecture:**

```
Applications (Java, compiled to .dex)
Android frameworks
Android RunTime (ART) — AOT compilation (.dex → native machine code)
Native libraries (webkit, SQLite, SSL, OpenGL) via JNI
Bionic (Android's custom C library, smaller than glibc)
Linux kernel (modified for power management, Binder IPC)
HAL (Hardware Abstraction Layer)
Hardware
```

- ART uses <font color="blue">ahead-of-time (AOT)</font> compilation: `.dex` files compiled to native code at install time (more efficient, less power)
- <font color="blue">JNI</font> (Java Native Interface): allows Java programs to access hardware directly; not portable across devices
- <font color=OrangeRed>HAL</font>: abstracts all hardware (camera, GPS, sensors) so apps are portable across different hardware platforms
- <font color="blue">Bionic</font>: smaller than glibc; optimized for slower mobile CPUs; avoids GPL licensing

**Windows Subsystem for Linux (WSL):**

Windows 10 adds WSL, allowing native Linux ELF binaries to run on Windows. `bash.exe` starts a Linux instance with `init` and `/bin/bash` running in a Windows <font color="blue">Pico process</font>. `LXSS/LXCore` translates Linux system calls to Windows equivalents; `fork()` is handled by combining LXSS work with `CreateProcess()`.

---

## 2.9 Building and Booting an Operating System 系统的构建与启动

### System Boot Process 系统启动过程

<font color=OrangeRed>Booting</font>: the process of starting a computer by loading the kernel.

**Standard boot sequence:**

1. Computer powered on → run <font color=OrangeRed>bootstrap program / boot loader</font> (small code in nonvolatile firmware)
2. Bootstrap program <font color="blue">locates the kernel</font>
3. Kernel is <font color="blue">loaded into memory</font> and started
4. Kernel <font color="blue">initializes hardware</font>
5. Root <font color="blue">file system is mounted</font>
6. Kernel starts the <font color=OrangeRed>init daemon</font> (Linux: `systemd`) which starts other services

**Multistage boot process:**

| Stage | Component | Role |
|---|---|---|
| 1 | BIOS / UEFI (firmware) | Run on power-on; initial boot loader |
| 2 | Boot block (MBR/GPT) | Located at fixed disk location; loaded by BIOS/UEFI |
| 3 | GRUB (Linux) | Grand Unified Boot Loader; loads the kernel; supports multiple kernels and boot targets |
| 4 | Kernel | Loaded into memory; initializes hardware; mounts root FS; starts init |
| 5 | init / systemd | PID 1; starts all system services |

**BIOS vs UEFI:**

| | BIOS | UEFI |
|---|---|---|
| Architecture | 16-bit, legacy | 64-bit, modern |
| Boot stages | Multistage (slower) | Single complete boot manager (faster) |
| Disk support | MBR (< 2 TB) | GPT (large disks) |

UEFI's greatest advantage: it is a single, complete boot manager — faster than the multistage BIOS process.

**GRUB configuration example:**

```bash
# /proc/cmdline — kernel parameters set by GRUB at boot time
BOOT_IMAGE=/boot/vmlinuz-4.4.0-59-generic
root=UUID=5f2e2232-4e47-4fe8-ae94-45ea749a5c92
```

**Linux kernel image boot sequence:**

1. Boot loader creates <font color="blue">initramfs</font> — a temporary RAM file system containing drivers and kernel modules needed to support the real root file system
2. Kernel decompresses itself from the compressed image
3. Loads necessary drivers from initramfs
4. Switches root file system from the temporary RAM location to the real root file system
5. Creates `systemd` (PID 1), which starts all other services
6. Presents the user with a login prompt

**Android boot differences:**
- Does not use GRUB; vendors provide their own boot loader (most common: LK — Little Kernel)
- Android **maintains** `initramfs` as the root file system (unlike Linux, which discards it)
- After mounting root FS, starts `init` process, then displays the home screen

**Recovery mode:** Most boot loaders support booting into recovery/single-user mode for diagnosing hardware, fixing corrupt file systems, or reinstalling the OS.

---

## 2.10 Operating-System Debugging 操作系统调试

<font color=OrangeRed>Debugging</font>: finding and fixing errors — both hardware and software, including performance problems (<font color="blue">performance tuning</font>).

### 2.10.1 Failure Analysis 故障分析

- Process failure: OS writes error info to a <font color="blue">log file</font>; may take a <font color="blue">core dump</font> (memory snapshot) for later debugger analysis
- Kernel failure: called a <font color=OrangeRed>crash</font>; error info saved to a log file; memory state saved to a <font color=OrangeRed>crash dump</font>
- Crash dump strategy: kernel saves memory to a reserved disk section (no file system) before reboot; a post-reboot process moves it into a file system

### 2.10.2 Performance Monitoring and Tuning 性能监控与调优

Tools use either **counters** or **tracing**.

**Counter-based tools (Linux):**

| Scope | Tool | Purpose |
|---|---|---|
| Per-process | `ps` | Reports info for selected processes |
| Per-process | `top` | Real-time statistics for current processes |
| System-wide | `vmstat` | Memory usage statistics |
| System-wide | `netstat` | Network interface statistics |
| System-wide | `iostat` | Disk I/O usage |

Most Linux counter-based tools read from the <font color="blue">/proc pseudo file system</font> (exists only in kernel memory; organized as a directory hierarchy; `/proc/<pid>` for per-process stats).

**Tracing tools (Linux):**

| Scope | Tool | Purpose |
|---|---|---|
| Per-process | `strace` | Traces system calls invoked by a process |
| Per-process | `gdb` | Source-level debugger |
| System-wide | `perf` | Collection of Linux performance tools |
| System-wide | `tcpdump` | Collects network packets |

### 2.10.3 BCC — BPF Compiler Collection

<font color=OrangeRed>BCC</font> (BPF Compiler Collection): a rich toolkit providing dynamic, low-impact kernel tracing for Linux.

- Front-end interface to <font color="blue">eBPF</font> (extended Berkeley Packet Filter)
- eBPF programs written in C, compiled into eBPF instructions dynamically inserted into the running kernel
- A <font color="blue">verifier</font> checks that eBPF instructions do not affect system performance or security before insertion
- BCC provides a Python front-end to make eBPF tools easier to write
- Tools can be used on **live production systems without causing harm**

```bash
# disksnoop.py — trace disk I/O activity
./disksnoop.py
# TIME(s)          T  BYTES  LAT(ms)
# 1946.29186700   R      8    0.27
# 1946.33965000   R      8    0.26
# 1948.34585000   W   8192    0.96

# opensnoop — trace open() calls by a specific process
./opensnoop -p 1225
```

> "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it." — Kernighan's Law

---

## Key Takeaways

- <font color=OrangeRed>OS services split</font>: user-facing (UI, program execution, I/O, file system, communication, error detection) and system-efficiency (resource allocation, logging, protection/security).
- <font color=OrangeRed>Three UI types</font>: CLI (text commands, scriptable, power users), GUI (desktop metaphor), touch-screen (gesture-based, mobile). UNIX CLI uses shells; commands are separate programs found by name, not built into the interpreter.
- <font color=OrangeRed>System calls</font>: the interface between user programs and OS services; accessed through an API (POSIX, Windows, Java). Parameters passed via registers, memory block, or stack. Six categories: process control, file management, device management, information maintenance, communications, protection.
- <font color=OrangeRed>IPC models</font>: message passing (OS-mediated, easier across computers) vs shared memory (memory-speed, requires synchronization). Both commonly provided.
- <font color=OrangeRed>Linker/Loader pipeline</font>: source → compiler → relocatable object → linker → executable → loader → program in memory. Dynamic linking avoids loading unused libraries; ELF is the UNIX/Linux binary format.
- <font color=OrangeRed>Mechanism vs policy separation</font>: mechanism = how; policy = what. Separating them enables flexible reconfiguration without changing underlying implementation.
- <font color=OrangeRed>OS structures</font>: monolithic (single address space, fast, hard to maintain); layered (debuggable, poor performance); microkernel (extensible, secure, slow IPC); loadable modules (best of layered + microkernel, flexible, efficient); hybrid (most real systems).
- <font color=OrangeRed>Darwin</font>: macOS/iOS kernel = Mach microkernel + BSD in same address space (avoids IPC copying overhead).
- <font color=OrangeRed>Android</font>: Linux kernel + ART (AOT compilation) + HAL + Bionic; maintains initramfs as root FS; Binder IPC.
- <font color=OrangeRed>Boot process</font>: firmware (BIOS/UEFI) → boot loader (GRUB) → kernel → initramfs → systemd → login. UEFI faster than BIOS (single complete manager). Linux discards initramfs after loading drivers; Android keeps it.
- <font color=OrangeRed>Debugging tools</font>: counters (ps, top, vmstat, netstat, iostat via /proc) vs tracing (strace, gdb, perf, tcpdump). BCC/eBPF enables live production tracing with no system risk.

## References

- Operating System Concepts — Silberschatz, Galvin & Gagne, Chapter 2 (Operating-System Structures)
- CS 536 Operating Systems — Lecture notes: Chapter 2
