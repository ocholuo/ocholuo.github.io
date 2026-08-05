---
title: "Meow's Cryptography - TPM LPC Bus Hijacking and Physical Interface Attacks"
date: 2026-05-25 11:11:11 -0400
categories: [13Cryptography, TPM]
tags: [TPM, LPC-bus, hardware-attack, trusted-computing, chain-of-trust, physical-attack, D-RTM, PCR, I2C, attestation]
math: false
toc: true
image:
---

# TPM LPC Bus Hijacking and Physical Interface Attacks

> Source: "A Hijacker's Guide to Communication Interfaces of the Trusted Platform Module"
> J. Winter, K. Dietrich — Computers and Mathematics with Applications 65 (2013) 748–761

---

## Overview

<font color=OrangeRed>While Trusted Platform Modules (TPMs) are designed to be tamper-resistant integrated circuits, the communication channel between the TPM and the rest of the trusted platform is comparatively insecure.</font>

<font color=blue>Passive attacks can be mounted against TPMs and their bus communication with fairly inexpensive equipment. This paper extends that work to show how the LPC bus protocol can be **actively manipulated** with basic hardware to circumvent security mechanisms — including the chain of trust — provided by modern trusted platforms. The same attack principles apply to TPMs on embedded systems using I2C bus interfaces.</font>

Key claim: a motivated adversary with limited resources can break the integrity of the transitive chain of trust constructed by either static or dynamic roots of trust for measurement (RTMs).

---

## 1. Background — Trusted Computing Concepts

### 1.1 TPM Basics

<font color=blue>The core of every trusted platform is the Trusted Platform Module (TPM).</font> The TPM records and reports events that occurred on a platform — such as loading a new software module or reading configuration data from hardware. "Measure" in this context means <font color=OrangeRed>the SHA-1 hash value of a specific event</font>.

A typical <font color=OrangeRed>application of this mechanism is the creation of the chain of trust</font>. During boot, <font color=blue>all individual software components — BIOS, bootloader, OS — are measured and the corresponding hash value is recorded in the TPM, creating the chain of trust.</font>

### 1.2 Platform Configuration Registers (PCRs)

The TPM uses a fixed set of <font color=OrangeRed>Platform Configuration Registers (PCRs)</font> to store integrity metrics. PCRs are:

- Neither resettable nor directly assignable during normal operation
- Extended via the **extend** primitive: chains the old PCR value to a new measurement by concatenating and hashing

```
PCR_new = SHA-1(PCR_old || new_measurement)
```

### 1.3 Remote Attestation and Sealing

**Remote attestation**: the TPM applies a cryptographic signature on PCR values using a key that can only be used inside that specific TPM. This signed receipt of PCR values proves the current platform software configuration state to a remote verifier.

**Sealing (local attestation)**: binds sensitive data blobs to a particular TPM in a particular software configuration state. The data can only be decrypted on the correct platform in the correct state.

### 1.4 Roots of Trust for Measurement (RTMs)

| Type | Description |
|---|---|
| **S-RTM** (Static RTM) | Single static root originating in the platform BIOS; builds a chain of measurements from platform boot |
| **D-RTM** (Dynamic RTM) | Based on special "late-launch" processor extensions (Intel TXT / AMD SVM); enables transitions from arbitrary untrusted states into trusted states with short measurement chains |

<font color=blue>D-RTMs are intended to allow platforms to switch from previously untrusted states into trusted states, comparable to a special kind of system reset that jumps directly to trusted software instead of the BIOS entry point.</font>

---

## 2. Anatomy of a Trusted Platform

### 2.1 TPM Localities

The TPM natively provides five **localities** (0–4) reflecting the level of trust of the communicating entity:

| Locality | Intended User |
|---|---|
| 0 | Normal OS and applications |
| 1–3 | Trusted applications, OS kernel |
| 4 | D-RTM hardware/microcode only (Intel TXT SINIT / AMD SVM SKINIT) |

<font color=OrangeRed>Locality 4 has special importance for D-RTMs.</font> PCRs 17–22 can only be extended at locality 4. Normal software (including the OS) cannot generate locality 4 bus cycles — the Southbridge (I/O controller hub) filters any attempt. On Intel TXT, only the Intel-signed SINIT ACM (authenticated code module) can access locality 4.

### 2.2 The Low Pin Count (LPC) Bus

The LPC bus was introduced to replace legacy bus standards on PCI-based PC platforms. Key characteristics:

- Minimal wiring: 4 bidirectional address/data lines, 1 frame signal, 1 reset signal, 1 clock signal
- Bidirectional architecture with multiplexed address/data lines
- Used for: firmware flash chips, Super-I/O controllers, and the **TPM**

<font color=blue>TPMs are connected to the hosting platform via the LPC bus.</font> While the TPM chip itself is protected, the bus provides no protection mechanisms and is easy to access with simple equipment.

#### 2.2.1 LPC Target Cycle Structure

All LPC target cycles follow this structure:

```
[START] → [CYCLE TYPE] → [ADDRESS] → [DATA (write)] → [TAR] → [SYNC] → [DATA (read)] → [TAR]
```

- **START**: host asserts frame signal; indicates major bus cycle type
- **SYNC**: device acknowledges; can insert wait-states
- **TAR (turn-around)**: transfers bus ownership between host and device

The only format difference between I/O and memory cycles is address phase length:
- I/O cycles: 4 clock cycles for 16-bit address
- Memory cycles: 8 clock cycles for 32-bit address

#### 2.2.2 TPM TIS Interface (TPM 1.2)

Prior to TPM 1.2, each vendor had incompatible interfaces. The TCG released the **TPM Interface Specification (TIS)** standard with TPM 1.2, defining:

- A common software-visible hardware register interface
- A standard generic TPM TIS driver (eliminating vendor-specific drivers)
- Special **LPC TPM cycles** (START value = `0x5`) distinct from standard I/O cycles (START = `0x0`)

TPM locality is encoded in the most significant bits of the 16-bit target address.

---

## 3. Active LPC Frame Hijacking

### 3.1 Hijacking LPC Bus Cycles

<font color=OrangeRed>The core observation enabling the attack: the address phase of a memory cycle perfectly overlaps a time-shifted I/O (TPM) cycle.</font>

When a memory write cycle and a TPM write cycle start at the same time:
- Memory cycle address phase: 8 clock cycles (32-bit address)
- I/O/TPM cycle address phase: 4 clock cycles

By delaying the frame signal assertion by 4 clock cycles, the trailing data phase of both cycle types becomes perfectly aligned.

**Frame hijacker device behavior:**

1. Monitors the LPC frame and data signals
2. Detects the start of an appropriate memory cycle
3. Intercepts the LPC frame signal to the TPM
4. Delays de-assertion of the frame signal by 4 clock cycles
5. From the TPM's perspective: a new TPM bus cycle begins at the delayed frame de-assertion

The LPC bus specification explicitly allows the frame signal to remain active for more than one consecutive clock cycle — the device must use the last value observed on the address/data lines while the frame was active as the START value. <font color=blue>This is exactly the behavior needed for the frame hijacker attack.</font>

**Result**: an adversary with physical hardware access can promote an ordinary memory cycle into a TPM cycle at **any desired locality, including locality 4**, bypassing all Southbridge software filtering.

The hardware required is a simple logic device (describable in a few lines of VHDL) with no expensive components like FPGAs.

---

## 4. Trusted Embedded Platforms

### 4.1 I2C Bus Interface TPMs

Several major vendors produce TPM 1.2 chips with I2C compatible hardware interfaces. The I2C TIS TPM interface operates on the same principles as the LPC TIS:

- Command blocks are submitted to internal register addresses of the TPM
- Locality is indicated by parts of the internal register address

**I2C bus characteristics:**

- 2 wires: bidirectional clock (SCL) + bidirectional data (SDA)
- Open-drain outputs; bus values determined by logical AND of all connected devices
- Speed: 100 kbit/s (standard), 400 kbit/s (fast), up to 5 Mbit/s (high-speed)
- Multi-master capable

#### 4.1.1 TPM Localities on I2C

<font color=OrangeRed>The I2C bus has no native indication of TPM localities</font>, unlike the LPC bus. Access filtering must be mediated by the I2C bus controller or operating system drivers. Advanced scenarios use ARM TrustZone with physically distinct I2C buses for security-critical and non-critical devices.

#### 4.1.2 Attack 1 — Injecting Commands via External Microcontroller

The I2C multi-master design allows additional bus masters to be added by simply connecting SDA and SCL pins to existing bus wires. <font color=OrangeRed>An adversary only needs to tap into two bus signals without cutting any circuit board traces.</font>

Required hardware: a cheap general-purpose microcontroller board (e.g., Arduino) and basic soldering skills. This allows arbitrary TPM commands to be injected into the I2C bus.

Detection risk: the platform can detect unauthorized I2C transfers by monitoring bus transactions to the TPM's I2C device address and correlating them against CPU-initiated transfers.

#### 4.1.3 Attack 2 — I2C Frame Hijacking

The LPC frame hijacking concept maps to I2C by cutting the I2C clock line near the TPM. The hijacker device:

1. Monitors incoming data on the CPU-side I2C bus for a trigger sequence
2. Detaches the TPM-side I2C clock signal from the CPU-side bus (forces to logic zero — appears as clock stretching)
3. On trigger sequence detection, re-attaches the TPM-side clock
4. The TPM sees the adversary's payload as the start of a new bus transfer

This approach hides the attack more effectively than direct command injection since the bus activity pattern looks normal to the CPU.

---

## 5. Platform Reset Attack — Reviving the TPM Reset Attack

### 5.1 Classic TPM Reset Attack

The original TPM reset attack (Kauer; Sparks et al.) relies on the fact that the LPC reset signal is active-low: asserting a reset can be accomplished by simply grounding the LPC reset line. This resets only the TPM without affecting the main processor.

Classic attack sequence:
```
1. Capture measurement logs for the target platform state
2. Reset the TPM (ground LPC reset signal)
3. Send TPM_Startup command to simulate BIOS startup
4. Replay measurement log via PCR extend commands
→ TPM holds attacker-chosen fake PCR values
```

<font color=OrangeRed>D-RTMs partially defeat this attack</font> because PCRs 17–22 can only be extended at locality 4, which requires hardware-level privilege that the software-running attacker cannot simulate after a TPM-only reset.

### 5.2 Reversed Attack — Resetting the Platform Instead of the TPM

<font color=blue>The innovation: reverse the roles. Instead of resetting the TPM independently of the platform, reset the platform independently of the TPM.</font>

| | Classic TPM Reset | Platform Reset Attack |
|---|---|---|
| What is reset | TPM (PCRs zeroed) | Platform (CPU/BIOS) |
| What remains | Platform continues running | TPM keeps its PCR values |
| Result | Attacker replays fake measurements | Attacker boots evil OS with legitimate TPM PCR state |

**Platform reset attack sequence:**
```
1. Boot platform into trusted state (legitimate software image)
2. Shield TPM from platform reset signal
3. Trigger hardware platform reset (reset button, power-good glitch)
4. BIOS re-initializes platform without touching TPM PCRs
5. Boot attacker's evil OS image of choice
6. TPM still holds PCR values from the trusted boot (step 1)
→ Remote attestation shows "trusted" state while evil OS is running
```

The key advantage: the attacker does not need to know the complete measurement chain. Any legitimate boot into a trusted state automatically produces the correct PCR values.

### 5.3 Shielding the TPM from the Platform Reset

The LPC reset signal is active-low. Shielding the TPM requires preventing it from seeing the reset pulse.

**Pull-down reset lines**: can be shielded by short-circuiting the reset signal to positive supply voltage (normal deasserted condition, no damage).

**Pull-up reset lines** (more common, more difficult):
- Cannot directly force to positive voltage (would destroy Southbridge output drivers during reset)
- Solution: cut the LPC reset signal near the TPM, insert a large resistor, add a switch between the TPM-side reset and supply voltage

The switch + resistor circuit:
```
Southbridge ──── [existing pull-up] ──┬──── [attacker resistor] ──── [switch] ──── VCC
                                       │
                                     [TPM]
```

- Switch **open** (normal operation): no effect; platform operates normally
- Switch **closed** (attack mode): TPM reset line held at VCC (inactive); platform reset proceeds normally

### 5.4 Hiding the TPM from the BIOS

When the platform resets while the TPM is shielded, the BIOS performs its TPM detection and startup sequence. The BIOS checks for TPM presence via the vendor ID register; if the TPM is hidden (frame signal forced low), no LPC transactions complete and the BIOS sees no TPM — provided the BIOS handles missing TPM gracefully.

<font color=OrangeRed>The "disable-and-hide" switch</font> extends the reset shielding with a logic AND gate on the LPC frame signal:

```
Frame (Southbridge) ──── AND gate ──── Frame (TPM)
                              │
                           switch ──── logic-0 (attack mode) / logic-1 (normal mode)
```

- **Normal mode**: AND gate passes through frame signal unchanged
- **Attack mode**: AND gate forces frame output permanently low → TPM appears absent → BIOS continues boot without TPM

Once the attacker's OS has loaded, the switch is returned to normal position. The TPM is now accessible with its pre-reset PCR values intact.

---

## 6. Conclusion and Attack Summary

### 6.1 What These Attacks Can and Cannot Do

<font color=blue>These attacks do **not** allow direct retrieval of TPM-protected data (e.g., private keys in non-migratable key slots). Extracting that data still requires invasive high-effort chip-level methods.</font>

<font color=OrangeRed>What these attacks do achieve:</font>

| Attack | Effect | Hardware Cost |
|---|---|---|
| LPC frame hijacking | Injects arbitrary PCR measurements at any locality including 4 | Simple FPGA/VHDL device |
| I2C command injection | Injects arbitrary TPM commands on embedded platforms | Arduino + soldering |
| I2C frame hijacking | Stealthy version of command injection; harder to detect | Arduino/FPGA + cutting clock line |
| Platform reset attack | Boots attacker OS while TPM holds legitimate trusted-boot PCR values | Wire, resistor, switch |

The platform reset attack has material costs an order of magnitude lower than the active frame hijacking attack — reproducible by anyone with a soldering iron.

### 6.2 Combined Attack Scenario

Combining LPC frame hijacking with the classic TPM reset attack: an adversary can construct arbitrary fake measurement chains spanning **all** TPM PCRs, including the D-RTM-protected registers (PCRs 17–22).

### 6.3 Broader Implications

From the conclusion:

> Results from passive sniffing [Schellekens], classic TPM reset [Kauer, Sparks], LPC frame hijacking [this paper], and platform reset [Section 5] should be carefully taken into account when attackers can gain physical access to the target platforms or when attackers are the legitimate owners of those platforms.

<font color=OrangeRed>Trustworthiness of current trusted platforms highly depends on the trust relation to the physical platform owner and ultimately requires a minimum level of physical platform security.</font>

---

## Key Takeaways

- The TPM chip itself is tamper-resistant, but the LPC bus connecting it to the platform is not — it has no protection mechanisms and is trivially accessible with simple hardware
- TPM locality enforcement is implemented in Southbridge software filtering, which is bypassed entirely by physical bus manipulation
- The LPC frame hijacking attack exploits a timing coincidence between memory and TPM cycle formats to promote arbitrary memory cycles into TPM locality-4 cycles
- D-RTMs (Intel TXT, AMD SVM) provide software barriers against locality spoofing but offer no protection against physical bus access
- The platform reset attack reverses the classic TPM reset: reboot the platform while holding the TPM's PCR state, then boot untrusted software that passes attestation
- The same attack principles apply one-to-one to embedded I2C-based TPMs, sometimes with lower hardware cost
- Physical security of the platform is a prerequisite for any meaningful trust guarantee from a TPM

---

## References

1. L. Chen, M. Ryan — Attack, solution and verification for shared authorisation data in TCG TPM. LNCS vol. 5983, Springer, 2010
2. J.M. McCune et al. — Flicker: an execution infrastructure for TCB minimization. EuroSys'08, ACM, 2008
3. F. Krautheim et al. — Introducing the trusted virtual environment module. LNCS vol. 6101, Springer, 2010
4. B. Kauer — OSLO: improving the security of trusted computing. USENIX Security 2007
5. M. Pirker et al. — Dynamic enforcement of platform integrity. LNCS vol. 6101, Springer, 2010
6. J. Cihula et al. — Trusted boot. 2007. tboot.sourceforge.net
7. Trusted Computing Group — TPM Main Part 3 Commands, Spec v1.2 L2 Rev 103, July 2007
8. **J. Winter, K. Dietrich — A Hijacker's Guide to the LPC Bus. EuroPKI 2011. LNCS vol. 7163, Springer, 2012** (companion paper)
9. E.R. Sparks et al. — TPM Reset Attack. cs.dartmouth.edu
10. Trusted Computing Group — TCG Platform Reset Attack Mitigation Specification, Rev 1.0, 2008
11. D. Schellekens, B. Preneel, K. Kursawe — Analyzing trusted platform communication. COSIC, KU Leuven
12. N. Lawson — TPM hardware attacks (Part 2). Blog, 2007. rdist.root.org
13. J.A. Halderman et al. — Lest we remember: cold-boot attacks on encryption keys. Commun. ACM 52(5), 2009
14. C. Tarnovsky — Hacking the smartcard chip. Black Hat DC 2010
15. Trusted Computing Group — TCG PC Client Specific TPM Interface Specification (TIS), v1.2 Final, 2005
16. Intel — Intel Low Pin Count (LPC) Interface Specification, Rev 1.1, August 2002
17. J. Winter — Eavesdropping trusted platform module communication. ETISS 2009
18. NXP Semiconductors — I2C-bus Specification and User Manual, Rev 4, 2012
19–21. P. Huewe; C.H. Ricard; D. Morav — Linux kernel I2C TIS TPM driver contributions, 2010–2011
22. SBS Implementers Forum — System Management Bus (SMBus) Specification, v2.0, 2000
23. T. Alves, D. Felton — TrustZone: integrated hardware and software security. ARM, 2004
24. Philips Semiconductors — AN10160: Level shifting I2C and SMBus bus buffers. NXP, 2003
25. D. Grawrock — Dynamics of a Trusted Platform: A Building Block Approach. Intel Press, 2009
