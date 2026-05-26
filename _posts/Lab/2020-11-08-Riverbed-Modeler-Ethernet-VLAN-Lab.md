---
title: "Meow's Lab - Riverbed Modeler: Ethernet CSMA/CD & VLAN Lab"
date: 2020-11-08 11:11:11 -0400
categories: [Lab, Riverbed]
tags: [Lab, Riverbed, Ethernet, CSMA-CD, VLAN, switching, network-simulation, LAN]
math: false
toc: true
image: ""
---

# Riverbed Modeler: Ethernet CSMA/CD & VLAN Lab

---

## Overview

Two Riverbed Modeler Academic Edition labs covering core LAN performance concepts. Lab 1 studies CSMA/CD Ethernet behavior under varying traffic loads on a 30-node coaxial bus. Lab 2 measures how VLAN segmentation reduces switch broadcast overhead in a multi-building switched Ethernet network for the fictional consulting firm Simple-n-Real.

Both labs use Discrete Event Simulation (DES) to compress hours of real network traffic into minutes of simulation time.

---

## Lab 1: Ethernet CSMA/CD — Direct Link Network with Media Access Control

**Objective:**
- Demonstrate the operation of an Ethernet network.
- Examine Ethernet performance under different traffic load scenarios.

### Background

<font color="blue">The Ethernet is a working example of CSMA/CD (Carrier Sense, Multiple Access with Collision Detect) LAN technology.</font>

- <font color=OrangeRed>Multiple access</font>: all nodes share a common transmission medium.
- <font color=OrangeRed>Carrier sense</font>: all nodes can distinguish between an idle and a busy link.
- <font color=OrangeRed>Collision detect</font>: a node listens while transmitting; if interference is detected, it stops and retries after a random back-off delay.
- <font color=OrangeRed>1-persistent</font>: an adaptor with a frame to send transmits with probability 1 whenever a busy line goes idle.

The lab sets up an Ethernet with 30 nodes connected via a coaxial link in a bus topology at 10 Mbps.

---

### <font color="#fb02ff">Step 1 — Create a New Project</font>

<font color="blue">**Local area networks (LANs):** designed to span distances of up to a few thousand meters.</font>

1. Start **Riverbed Modeler Academic Edition** → File → New.
2. Select **Project** → OK → Name the project: `<initials>_Ethernet`, scenario: `Coax_2` → check **Use Startup Wizard** → OK.
3. In the **Startup Wizard: Initial Topology** dialog:
   - Select **Create Empty Scenario** → Next
   - Network Scale: **Office** → Next
   - X Span: **200**, Y Span: **100** → Next → Finish.
4. Close the **Object Tree** dialog box.

---

### <font color="#fb02ff">Step 2 — Create the Network</font>

<font color=OrangeRed>To create the coaxial Ethernet network:</font>

1. Select **Topology** → **Rapid Configuration** → **Bus** → Next.
2. Click **Select Models** → Model List: <font color="blue">**ethcoax**</font> → OK.
   - <font color="blue">`eth_tap`</font>: Ethernet bus tap that connects a node to the bus.
   - <font color="blue">`eth_coax`</font>: Ethernet bus connecting nodes via taps.
3. In the **Rapid Configuration** dialog, set 30 nodes and click OK.

![Rapid Configuration: Bus dialog showing Node model=ethcoax_station, Link model=eth_coax, Tap model=eth_tap, Number=30, with horizontal placement options](./assets/img/post/riverbed-ethernet-rapid-config-bus-dialog.png)

4. Right-click the horizontal link → **Edit Attributes (Advanced)**:
   - Click **model** → Edit → select <font color="blue">`eth_coax_adv`</font> model.
   - Set **delay**: `0.05` (propagation delay in sec/m).
   - <font color=OrangeRed>A higher delay is used as an alternative to generating higher traffic, which would require much longer simulation time.</font>
   - Set **thickness**: `5` (display width of the bus link).
   - → OK.

![bus_0 Attributes dialog — model=eth_coax_adv, delay=0.05, data rate=10,000,000, thickness=5](./assets/img/post/riverbed-ethernet-coax-link-attributes.png)

5. The network should now look like the illustration below. Save the project.

![30-node Ethernet coaxial bus topology in Riverbed Modeler — all nodes connected via a shared horizontal bus link](./assets/img/post/riverbed-ethernet-bus-30nodes-topology.png)

---

### <font color="#fb02ff">Step 3 — Configure the Network Nodes</font>

1. Right-click any node → **Select Similar Nodes** (selects all 30).
2. Right-click any node → **Edit Attributes**.
3. Check **Apply Changes to Selected Objects**.
4. Expand <font color="blue">**Traffic Generation Parameters**</font>:
   - **ON State Time**: `exponential(100)`
   - **OFF State Time**: `exponential(0.00001)`
   - *(Packets are generated only in the ON state.)*
5. Expand <font color="blue">**Packet Generation Arguments**</font>:
   - **Packet Size**: `constant(1024)`
   - **Interarrival Time**: `exponential(2)` *(mean 2 sec between packets in ON state)*
6. Click OK. Save the project.

<font color="blue">The argument of the exponential distribution is the mean of the interval between successive events. Packet inter-arrival time determines the traffic intensity injected into the network.</font>

![node_0 Attributes dialog — Traffic Generation Parameters showing ON State=exponential(100), OFF State=exponential(0.00001), Interarrival Time=exponential(2), Packet Size=constant(1024), Apply Changes to Selected Objects checked](./assets/img/post/riverbed-ethernet-node-traffic-params.png)

---

### <font color="#fb02ff">Step 4 — Choose Statistics</font>

<font color="blue">A probe represents a request by the user to collect a particular piece of data about a simulation.</font>

1. Right-click workspace (not on a node) → **Choose Individual DES Statistics** → Expand **Global Statistics**:
   - <font color="blue">Traffic Sink</font> → check **Traffic Received (packets/sec)**
   - <font color="blue">Traffic Source</font> → check **Traffic Sent (packets/sec)**
   - Click OK.
2. Select **DES** → **Choose Statistics (Advanced)**:
   - Right-click **Traffic Received** probe → **Edit Attributes**:
     - **scalar data**: enabled
     - **scalar type**: time average
     - → OK
   - Repeat for the **Traffic Sent** probe.
3. **Probe Model** → File → save → close.

![pb0 Attributes dialog — Traffic Sink probe with scalar data=enabled, scalar type=time average, vector data=enabled](./assets/img/post/riverbed-ethernet-probe-scalar-config.png)

---

### <font color="#fb02ff">Step 5 — Run Simulation — Multiple Load Scenarios</font>

1. Click **Configure/Run Simulation** ![Configure/Run Simulation toolbar button — red running figure](./assets/img/post/riverbed-ethernet-run-sim-button-icon.png) → Duration: **30 seconds** → Run.

![Configure/Run DES dialog showing Duration=30 seconds, Values per statistic=100, with Run button](./assets/img/post/riverbed-ethernet-run-simulation-dialog.png)

2. After completion, click Close → save project.
3. **Scenarios** → **Duplicate Scenario**, name `Coax_1`.
4. Repeat duplication, changing **Interarrival Time** for each scenario:

| Scenario | Interarrival Time | Relative Load |
|---|---|---|
| `Coax_2` | `exponential(2)` | Lightest |
| `Coax_1` | `exponential(1)` | |
| `Coax_05` | `exponential(0.5)` | |
| `Coax_025` | `exponential(0.25)` | |
| `Coax_01` | `exponential(0.1)` | |
| `Coax_005` | `exponential(0.05)` | |
| `Coax_0035` | `exponential(0.035)` | |
| `Coax_003` | `exponential(0.03)` | |
| `Coax_0025` | `exponential(0.025)` | |
| `Coax_002` | `exponential(0.02)` | Heaviest |

<font color=OrangeRed>Each successive run takes longer to complete because traffic intensity is increasing — more collisions and retransmissions consume bandwidth.</font>

---

### <font color="#fb02ff">Step 6 — View Results</font>

1. Click **View Results** ![View Results toolbar button — small chart icon](./assets/img/post/riverbed-ethernet-view-results-button-icon.png) → open **Results Browser**.
2. Select the **DES Parametric Studies** tab.
3. From **Results for: Current Project**, check all results (uncheck `Coax_0025`).
4. Uncheck **Include vectors**.
5. Expand **Scalar Statistics** → **Traffic Sink** and **Traffic Source**.
6. Right-click **Traffic Received** → **Set as Y-Series**.
7. Right-click **Traffic Sent** → **Set as X-Series** → click **Show**.

![Riverbed Results Browser showing Ethernet throughput (received packets/sec) vs. load (sent packets/sec) — the curve rises, peaks near saturation, then drops as collisions dominate at high load](./assets/img/post/riverbed-ethernet-throughput-vs-load-csmacd.png)

**Key observations:**
- <font color="blue">At very low load</font>: throughput is near zero — the network is underutilized.
- <font color=OrangeRed>At medium load</font>: throughput peaks as traffic saturates the channel efficiently.
- <font color="blue">At high load</font>: collisions multiply, retransmissions waste bandwidth, and throughput collapses.

---

### Lab 1 Discussion Questions

1. **Why does throughput drop at both very low and very high load?**
   At very low load, the channel is mostly idle — few packets arrive so throughput is naturally low. At very high load, every transmission attempt triggers a collision, retransmissions pile up, and useful throughput collapses.

2. **Effect of collision count:** Duplicate `Coax_01`, `Coax_005`, `Coax_0025`. Add **Node Statistics → Ethcoax → Collision Count** for node 0. Compare collision counts and received traffic across the three scenarios using **DES → Results → Compare Results**.

3. **Effect of station count:** Duplicate `Coax_0025` as `Coax_Q3`. Remove the 15 odd-numbered nodes (node 1, 3, … 29). Compare node 0 collision counts between `Coax_0025` and `Coax_Q3` — fewer nodes reduce collision probability at the same load.

4. **Effect of packet size:** Duplicate `Coax_0025` as `Coax_Q4`. Change packet size to `constant(512)`. Compare throughput in **packets/sec** and **bits/sec** between `Coax_0025` and `Coax_Q4`.

---

## Lab 2: Improving LAN Performance Using VLANs

**Objective:**
- Configure VLANs to improve switch performance.
- Use simulation to make data-driven infrastructure decisions.

**Scenario:** Simple-n-Real consulting firm — three buildings (A, B, C), each with a switch. User groups: Engineering, Marketing, Sales. Servers provide FTP, Database, HTTP, and email services.

---

### <font color="#fb02ff">Part 1 — Understand the Baseline Model</font>

1. Start **Riverbed Modeler Academic Edition** → File → Open → **LAN_Lab_2**.
2. Open scenario **`Switched_Ethernet_No_VLAN`**.

![Riverbed Modeler — Switched_Ethernet_No_VLAN scenario showing three building switches (A, B, C) connected in a hub-and-spoke topology, with Engineering, Marketing, and Sales workstations in each building](./assets/img/post/riverbed-vlan-3buildings-switched-topology.png)

![README for the No-VLAN scenario — explains that all workstations share one broadcast domain, causing unnecessary cross-department broadcast flooding and higher switch load](./assets/img/post/riverbed-vlan-readme-no-vlan-scenario.png)

3. Read the **README** file (double-click the ![README book icon](./assets/img/post/riverbed-vlan-readme-book-icon.png) book icon), then click ![Return to topology view icon](./assets/img/post/riverbed-vlan-return-topology-icon.png) to return to the topology view.
4. Explore **Application Config** and **Profile Config** to understand traffic: Email, FTP, HTTP, Database. <font color="blue">These values are pre-tuned — changes may alter results significantly.</font>
5. Right-click any switch (Building_A, B, or C) → **Edit Attributes** → expand **Switch Port Configuration** → expand any port row → expand <font color="blue">**VLAN Parameters**</font>:
   - Verify **Scheme** = <font color=OrangeRed>**Default**</font> — no VLANs configured.
   - Click Cancel.
6. Right-click the link between Building_A ↔ B or Building_A ↔ C → **Edit Attributes** → note the link data rate (in bits/sec).

---

### <font color="#fb02ff">Part 2 — Run the Baseline Simulation</font>

1. Click **Configure/Run Simulation** ![Configure/Run Simulation toolbar button — red running figure](./assets/img/post/riverbed-vlan-run-sim-button-icon.png) toolbar button.
2. Set **Simulation Duration**: <font color=OrangeRed>**8 hours**</font>.
3. Click **Run** — monitor the progress bar.
4. When complete, click **Close**.

---

### <font color="#fb02ff">Part 3 — View Baseline Results</font>

<font color=OrangeRed>**View Application Response Times:**</font>

1. **DES** → **Results** → **View Results**.
2. Expand **Global Statistics** → **Email** and **FTP**.
3. Select **Download Response Time (sec)** and **Upload Response Time (sec)** for both Email and FTP.
4. Settings: **Stacked Statistics**, This Scenario, **As Is** → click **Show**.
5. Switch **As Is** dropdown to **average** → click **Add** → overlay raw + average curves.

> **Note:** Use the ![Hide/Show Graphs icon — small stacked-chart button](./assets/img/post/riverbed-vlan-hide-show-graphs-icon.png) button in the Results Browser toolbar to toggle individual graph panels on or off.

<font color="#fb02ff">**View Switch Throughput Statistics:**</font>

1. Back in **View Results**, unselect Email/FTP.
2. Expand **Object Statistics** → **subnet_0** → **Building_A** → **Switch**.
3. Select <font color="blue">**Traffic Received (bits/sec)**</font> and <font color="blue">**Traffic Forwarded (bits/sec)**</font>.
4. Settings: **Stacked Statistics**, This Scenario, **As Is** → **Show** → switch to **average**.
5. Repeat for Building_B and Building_C.

![Four result panels for the No-VLAN scenario — top-left: Email/FTP application response times; top-right and bottom: switch Traffic Received and Forwarded for Buildings A, B, C, showing high broadcast-driven throughput](./assets/img/post/riverbed-vlan-4graphs-response-time-switch-traffic.png)

**Record baseline values:**

| Metric | Min | Max | Avg |
|---|---|---|---|
| Email Download Response Time (sec) | | | |
| Email Upload Response Time (sec) | | | |
| FTP Download Response Time (sec) | | | |
| FTP Upload Response Time (sec) | | | |
| Building_A Traffic Received (bits/sec) | | | |
| Building_A Traffic Forwarded (bits/sec) | | | |
| Building_B Traffic Received (bits/sec) | | | |
| Building_B Traffic Forwarded (bits/sec) | | | |
| Building_C Traffic Received (bits/sec) | | | |
| Building_C Traffic Forwarded (bits/sec) | | | |

---

### <font color="#fb02ff">Part 4 — Switch to VLAN Scenario and Compare</font>

1. **Scenarios** → **Switch Scenarios** → choose <font color="blue">**3_VLANs**</font>.
2. Right-click any switch → **Edit Attributes** → expand **VLAN Parameters**:
   - Verify **Scheme** = <font color=OrangeRed>**Port-Based VLAN**</font> (vs. Default in the previous scenario).
3. Click **( ... )** next to **Supported VLANs** → **Edit**:
   - Note the 3 VIDs defined: <font color="blue">**10, 20, 30**</font> (one per department: Engineering, Marketing, Sales).
   - Click Cancel twice.
4. <font color="blue">The topology, application, and profiles are identical to the No-VLAN scenario.</font>
5. Run the simulation (same 8-hour duration).
6. View results following the same steps as Part 3.

![3_VLANs scenario — Email Download/Upload and FTP Download/Upload response times over 8 hours; all four metrics stay below 0.40 sec, showing stable application performance with VLAN segmentation](./assets/img/post/riverbed-vlan-results-app-response-times.png)

![3_VLANs scenario — Building_A Switch Traffic Forwarded and Traffic Received (bits/sec) with raw and time-average curves; both averages settle around 700 bits/sec](./assets/img/post/riverbed-vlan-results-buildinga-switch-traffic.png)

![3_VLANs scenario — Building_B Switch Traffic Forwarded and Traffic Received (bits/sec) with raw and time-average curves; both averages settle around 400 bits/sec](./assets/img/post/riverbed-vlan-results-buildingb-switch-traffic.png)

![3_VLANs scenario — Building_C Switch Traffic Forwarded and Traffic Received (bits/sec) with raw and time-average curves; averages track upward and settle around 500 bits/sec](./assets/img/post/riverbed-vlan-results-buildingc-switch-traffic.png)

![3_VLANs scenario — Building_C Switch Traffic Forwarded and Received with raw (blue) and rolling average (red) overlaid; both metrics converge around 400–500 bits/sec over 8 hours](./assets/img/post/riverbed-vlan-results-buildingc-raw-average-overlay.png)

**Compare scenarios** using **DES** → **Results** → **Compare Results**:
- Select both projects in the top-right pane.
- Plot **Object Statistics** → **subnet_0** → **Building_A** → **Switch** → **Traffic Forwarded (bits/sec)**.
- Settings: **Overlaid Statistics**, **average** → **Show**.

![Compare Results — Building_A Switch Traffic Forwarded: red line (No_VLAN) consistently ~2x higher than blue line (3_VLANs), confirming VLAN broadcast containment halves forwarded traffic on the core switch](./assets/img/post/riverbed-vlan-compare-switch-forwarded-traffic.png)

---

### <font color="#fb02ff">Part 5 — Analyze Queuing Delay</font>

Compare queuing delay on the Building_C → Building_A link across both scenarios:

1. **DES** → **Results** → **Compare Results** (both projects selected).
2. Expand **Object Statistics** → **subnet_0** → **Building_A ↔ Building_C** → **point-to-point**.
3. Select **queuing delay (sec)** ←.
4. Settings: **Overlaid Statistics**, **average** → **Show**.

![Queuing delay comparison — red line (No_VLAN) vs. blue line (3_VLANs) on the Building_C to Building_A link over 8 hours of simulation. VLAN reduces the average queuing delay by more than half.](./assets/img/post/riverbed-vlan-queuing-delay-comparison.png)

**Interpretation:**

- <font color=OrangeRed>Switch throughput drops significantly with VLANs</font>: broadcast frames are confined within each VLAN — switches no longer flood broadcasts across all three buildings.
- <font color="blue">Application response times do not change significantly</font>: queuing delays are small to begin with, so the reduction is real but too small to materially impact end-to-end response time.
- <font color=OrangeRed>The amount of application data sent is identical across both scenarios</font> — only switch forwarding behavior changes.

> **Key insight:** VLAN reduces switch broadcast overhead and improves bandwidth utilization. The benefit to application response time becomes large only when queuing congestion is already significant. VLANs also provide security isolation and administrative flexibility regardless of load.

**Network Delay Components:**

| Component | Description |
|---|---|
| <font color=OrangeRed>Bandwidth delay</font> | Time to serialize the packet onto the wire |
| <font color=OrangeRed>Propagation delay</font> | Speed-of-light travel time across the medium |
| <font color=OrangeRed>Protocol delay</font> | Processing time in the protocol stack |
| <font color=OrangeRed>Congestion (queuing) delay</font> | Wait time in switch/router queues — the target metric for VLAN optimization |

---

## Key Takeaways

- <font color=OrangeRed>CSMA/CD throughput peaks at medium load and collapses at high load</font> — collisions and retransmissions consume all available bandwidth.
- <font color=OrangeRed>1-persistent Ethernet</font> transmits immediately when the link goes idle — maximizes utilization at low load, maximizes collisions at high load.
- <font color=OrangeRed>VLAN reduces switch forwarded traffic</font> by confining broadcast domains — switches no longer flood traffic across the entire network.
- <font color="blue">VLAN impact on application response time is small at moderate load</font> — queuing delays must already be significant for VLAN to materially improve response time.
- <font color=OrangeRed>VLAN benefits</font>: bandwidth utilization, security isolation, and administrative flexibility via virtual organization.
- <font color="blue">Reducing station count</font> or <font color="blue">packet size</font> reduces collision probability on a shared CSMA/CD medium.

## References

- Riverbed Modeler Academic Edition Lab 1: Ethernet CSMA/CD
- Riverbed Modeler Academic Edition Lab 2: Improving LAN Performance Using VLANs
- IEEE 802.1Q — Virtual Bridged Local Area Networks
