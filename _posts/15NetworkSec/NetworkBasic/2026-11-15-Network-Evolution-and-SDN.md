---
title: "Meow's NetworkSec - Network Evolution and SDN 网络演进与SDN入门"
date: 2018-05-18 11:11:11 -0400
categories: [15NetworkSec, NetworkBasic]
tags: [Network, sdn, hub, switch, router, Firewall, wifi, network-architecture]
math: false
toc: true
---

# Network Evolution and SDN

只要网络硬件可以集中式<font color="#0433ff">软件管理</font>，可编程化，控制转发层面分开，则可以认为这个网络是一个SDN网络。

## Evolution of network devices

1. 网络诞生之前：pc 单机运行，没有网卡，网线，协议栈，数据通过软盘，光盘…

2. 网络通信三要素：`【IP地址+端口号+传输协议】`三要素，是网络中通信必不可少的角色。
    - `IP地址`: 即确定和哪台主机通信
    - `端口`: 分为物理端口和逻辑端口
      - 物理端口主要是网卡口（路由器、交换机等）
      - 逻辑端口是指确定进程（应用程序）
    - `传输协议`: TCP/UDP

3. 网络组成三要素：<font color="#ff2600">网线+网卡+协议栈</font> 最小单元网络
    - 网线：物理介质，承载比特流/电信号（类似电话线承载语音流/模拟信号）
    - 网卡：数据处理，例如将电脑磁盘的数据/字节转换为网线上的电流/比特，将比特流转换为数据
    - 协议栈：沟通语言，实现通信过程中的数据解析、地址寻址、流控制等
    - ![Two PCs, PC1 and PC2, are joined by one yellow cable, with labels for the network card, cable and protocol.](./assets/img/post/15networksec/net-evolution-sdn-p106-0-two-pcs-linked-by-cable.png)
    - <font color="#ff2600">缺点：网线不够长：</font>但是当距离超过网线物理传输距离上限，数据则开始丢失。
    - ![Two PCs are joined by a long cable of over 100 metres, and data frames fade and are lost before PC2.](./assets/img/post/15networksec/net-evolution-sdn-p106-1-signal-lost-over-long-cable.png)

4. <font color="#ff2600">中继器 repeater 出现</font>
    - 物理层产品，对信息进行中继和放大，实现设备远距离传输。
    - ![A repeater placed in the middle of a long cable lets data frames reach PC2 intact.](./assets/img/post/15networksec/net-evolution-sdn-p107-0-repeater-extends-cable-distance.png)
    - <font color="#ff2600">缺点：中继口不够.</font> 一般中继器只有两个接口，如果超过三个主机，则无法实现多主机直接的数据通信。
    - ![A repeater with Left and Right sides joins PC1 and PC2, and PC3 hangs below it with a cross mark.](./assets/img/post/15networksec/net-evolution-sdn-p107-1-repeater-with-third-pc.png)

5. <font color="#ff2600">集线器 hub 来了</font>
    - hub是一种“多口中继器”，物理层产品，对信息进行中继和放大，从任一个接收到的数据，可以往其他所有接口泛洪。
    - ![A hub receives frames from PC1 and sends copies out to both PC2 and PC3.](./assets/img/post/15networksec/net-evolution-sdn-p108-0-hub-floods-frames-to-all-ports.png)
    - <font color="#ff2600">缺点：</font>集线器不能识别数据包的寻址信息和上层内容，无法对终端主机隔离，多个主机出于冲突域中，导致带宽利用率低

6. 怕骚扰，<font color="#ff2600">网桥 bridge</font> 来了
    - 链路层产品，记录终端主机MAC地址，生成MAC表，根据MAC表转发主机之间的数据流。
    - 网桥能冲突域隔离，提高网络带宽利用率，不同接口间的数据不会互相冲突。
    - ![A bridge joins two hub segments with PC1 to PC4, and keeps a table mapping its ports to MAC addresses.](./assets/img/post/15networksec/net-evolution-sdn-p108-1-bridge-mac-table-two-segments.png)
    - <font color="#ff2600">缺点: </font>接口有限，默认是两个接口，对网络的隔离冲突有限，无专用硬件处理数据而是采用CPU导致处理速度稍慢

7. 不够快，交换机 <font color="#ff2600">switch</font> 来了
    - 链路层产品，记录`终端主机MAC地址`并生成`MAC表（CAM表）`，根据MAC表转发主机之间的数据流。
    - 交换机在网桥基础上升级和延伸，相比网桥，有以下优点：
      - 接口数量更密集，独立冲突域，带宽利用率大大增长
      - 采用专用ASIC硬件芯片进行高速转发
      - 能够进行VLAN隔离（不仅仅可以隔离冲突域，而且可以通过VLAN隔离广播域）
    - ![A switch with four ports connects PC1 to PC4 directly, with a table mapping each port to one MAC address.](./assets/img/post/15networksec/net-evolution-sdn-p109-0-switch-port-to-mac-table.png)
    - <font color="#ff2600">缺点: </font>是局域网产品，适用于本地网络，无法实现远程广域网通信。

8. 不够远，<font color="#ff2600">路由器</font> 来了：
    - 网络层产品，基于IP寻址，采用路由表实现数据转发
    - 路由器主要用于连接不同局域网（可以是不同介质，即令牌网和以太网互通），实现广播域隔离，也可以用于远程通信（广域网连接）
    - 是物联网大爆发的主要原因，使跨介质夸地理的网络大融合成为现实
    - IP逻辑协议寻址机制是实现不同类型局域网连通的关键，不同局域网主机只要有配置IP地址，有合理网段规划，则可以通信，路由器在实现局域网之间通信时，会实现”介质翻转“和”路由转发“。
    - 第一台路由器，斯坦福大学，用于大学校园网络 `SUNet`
    - ![A router links an Ethernet network on 192.168.1.0/24 to a Token Ring network on 192.168.2.0/24.](./assets/img/post/15networksec/net-evolution-sdn-p109-1-router-joins-ethernet-token-ring.png)
    - ![Three routers R1, R2 and R3 link three LANs over WAN connections, each LAN with its own subnet.](./assets/img/post/15networksec/net-evolution-sdn-p110-0-three-routers-connect-three-lans.png)

9. 布线麻烦，<font color="#ff2600">无线AC/AP（Access point）</font>来了：
    - 可以看成带`有无线功能的交换机/路由器`，能将有线信号转换成无线的设备都可以叫无线AP。指802.11协议的无线AP，即大家耳熟能详的`WIFI`。
    - 根据部署方式不同，分为胖AP和瘦AP。
      - `AC（Wireless Access Point Controller）`统一管理的就是瘦AP，
      - 瘦AP中，无线AP仅具备无线信号发射的功能，所有命令调试全部集中在后台的AC/无线控制器中。
      - 其余都是胖AP。
      - 胖AP方案中，无线AP有独立的操作系统，独立调试无线热点所有配置。
      - 小型无线网络（家用、小型企业）采用胖AP，大型无线网络(无线城市、无线校园网)采用瘦AP方案（AP+AC）
    - ![A WLAN controller and two L3 switches connect four access points, AP1 to AP4, that give wifi to users.](./assets/img/post/15networksec/net-evolution-sdn-p110-1-wlan-controller-with-four-aps.png)
    - ![A campus network diagram with carriers, exit routers, core area, access areas and wireless APs, plus a text list on wireless design.](./assets/img/post/15networksec/net-evolution-sdn-p111-0-campus-network-wireless-design-diagram.jpeg)
    - 无线设计思路
      - 有线无线一体化：共用汇聚交换机（最常见）
      - 无线独立组网：有线无线两张网（医疗）
    - 无线四件套：
      - AC：漫游、认证、安全控制
      - AP：将有线转换成无线
      - POE：供电交换机或POE模块
      - 网管：网络管理，射频管理

10. 不够安全，<font color="#ff2600">防火墙（Firewall</font> 来了：
    - 网络安全产品，对于网络进行安全访问限制，一般用于互联网边缘防黑客攻击
    - 根据防火墙的技术特征，分为：包过滤、应用代理、状态检测防火墙。
    - 根据产品形态：软件和硬件防火墙。
    - 防火墙类似有安全功能的路由器，早期firewalls就是在路由器+访问控制功能，多亿防火墙的很多功能可以在router上看到，比如路由协议，访问控制列表，地址翻转技术等。
      - But we need both router and firewalls:
        - 网络边界的router可以替代成firewalls，但是在网络里可以同时存在
        - 路由器侧重`地址翻转和路由策略`
        - 防火墙侧重`安全隔离`
      - 在firewall基础上：后面又延伸出了web防火墙，安全网关，入侵检测防御等产品
    - 一般中小型单位 互联网出口使用防火墙或者只使用路由器，功能多且便宜
    - 特定行业内网出口 必须用路由器，政策要求和业务需要，如公安/法院/金融等
    - 大型网络防火墙和路由器分开，如果都用防火墙，性能可能扛不住
    - 路由器和防火墙两者都存在的情况下，一般都是路由器在最外层，防火墙一般会旁挂服务器，即DMZ区域，采用第一种架构，服务器在私网IP域，相对安全。黑客攻击首先需要穿透路由器的NAT，还需绕过防火墙的检测。
    - ![Chalkboard diagram of two PCs connected through a switch to a firewall and then the Internet, with a 192.168.1.0/24 label.](./assets/img/post/15networksec/net-evolution-sdn-p112-0-home-network-firewall-internet-diagram.png)

11. 网络拥挤，<font color="#ff2600">流量控制</font> 来了：
    - <b>产品主要分为上网行为管理, 负载均衡器/应用交付, 链路优化等</b>，
    - <b>行为管理</b>：主要针对流量进行精细化区分控制
    - ![Chalkboard diagram of two PCs behind a switch and router to the Internet, with three traffic flows labelled with bandwidth in kb/s.](./assets/img/post/15networksec/net-evolution-sdn-p112-1-router-traffic-bandwidth-by-type-diagram.png)
    - <b>负载均衡器/应用交付：侧重流量的负载均衡（根据流量的特征、应用、地址等进行区分，然后分发到不同的链路和server上）</b>
    - ![Chalkboard diagram of four PCs connected through a switch and router to two separate Internet service provider clouds.](./assets/img/post/15networksec/net-evolution-sdn-p112-2-router-two-isp-uplinks-diagram.png)
    - <b>链路优化：主要应用在广域网里低速路边界，最大利用链路。</b>
    - ![Chalkboard diagram of Internet users PC1 to PC3 reaching Server1, Server2 and Server3 through a router and switch.](./assets/img/post/15networksec/net-evolution-sdn-p113-0-internet-users-reach-server-cluster-diagram.png)
    - 流控产品是一种七层产品，更多关注流量和应用特征。

## 一个网络到底需要多少设备？

1. 家庭<b>SOHO</b>网络
    - ![Chalkboard diagram of a PC on a wired link and a laptop and pad on wireless links, joined at an access point to the Internet.](./assets/img/post/15networksec/net-evolution-sdn-p113-1-wired-and-wireless-access-point-diagram.png)
    - 说明：典型家庭网络，路由器连接外网，无线路由器提供wifi
    - 设备：无线路由器
    - 技术：WI-FI、NAT(网络地址转换)、PPPOE（以太网上的点对点协议，即无线路由器拨号协议）、DHCP（动态主机设置协议，用于内部网或网络服务供应商自动分配IP地址）
2. 小型创业公司
    - ![Chalkboard diagram of department PC groups on L2 switches joined to a core switch, an egress router, a server cluster and the Internet.](./assets/img/post/15networksec/net-evolution-sdn-p114-0-departmental-campus-network-with-core-switch.png)
    - 说明：小型企业架构，两层架构，单核心拓扑
    - 设备：路由器、交换机、服务器
    - 技术：VLAN、TRUNK、DHCP、WLAN、静态路由/OSPF、PPPOE、NAT、ACL等
    - ![Colored network diagram of a headquarters with firewall, core switches and server cluster linked by IPSEC VPN to a branch office.](./assets/img/post/15networksec/net-evolution-sdn-p114-1-headquarters-and-branch-office-topology.jpeg)
      <details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

      出差员工 / 电信 / 网通 / Internet / L2TP Over IPSEC / IPSEC VPN / 出口防火墙 / AC控制器 / 服务器集群 / 192.168.88.0/24 / 核心层交换机 / 总部 / 分部 / 出口路由器 / 三层交换机 / 二层交换机 / \[?\] / \[?\] / 192.168.19.0/24 / 192.168.20.0/24 / 192.168.21.0/24 / 192.168.22.0/24 / 192.168.23.0/24

      </details>
    - 说明：总部属于中型企业架构，分部属于小型企业架构
    - 设备：
        - 总部：路由器、交换机、防火墙、瘦AP(无线AC+AP)、服务器
        - 分布：路由器、交换机
    - 技术：
        - 总部：VLAN、MSTP、VRRP、WIFI、NAT、VPN、TRUNK、DHCP、ACL等
        - 分部：VLAN、VPN、WIFI
    - 解决思路：
        - 使用<font color="#ff2600">子网划分</font>：对每个部门进行规划 （各部门单独一个24位的子网断，保证连续性，即使后续有新增加的员工，24位有254个地址，可以保证能正常使用，并且连续性可以方便做汇总、与一些策略的控制）。
        - 冗余性的实现，可以利用<font color="#ff2600">MSTP+VRRP技术</font>实现链路的冗余性与网关的热备功能，并且核心之间链路起链路聚合，提高带宽。
        - 安全性的实施，可以利用<font color="#ff2600">ACL与端口隔离技术</font> 来进行部署，当然也可以高级点，dot1x、DHCP snooping+DAI+IPSGD等技术。（一般ACL与端口隔离技术即可，除非有特殊需求在使用后续的）。
        - 使用<font color="#ff2600">AC+AP</font>的三层旁挂架构组件无线网络，实现内部网络使用5G接入网络，而访问则使用2.4G频率，并且实现，访客只能访问公司提供的WEB页面与Internet访问，并且要求无线访客区之间实现隔离。
        - 利用<font color="#ff2600">浮动路由+NQA</font>或者ip-link技术实现自动切换
        - 使用<font color="#ff2600">IPSEC技术</font>实现总部与分部之间的互访，通过<font color="#ff2600">加密验证</font>等机制来保证数据的安全性
        - 部署<font color="#ff2600">L2TP Over IPSEC</font>实现出差员工能够拨入到内网，访问特定的资源。
        - 开启<font color="#ff2600">Telnet或者SSH功能</font>，实现访问，并且用<font color="#ff2600">ACL限制</font>只能特点的主机访问。

<b>1. 园区网络：</b>

- 说明：
- ![Chalkboard diagram of a three-tier network with routers, firewalls, core, aggregation and access layers and several server zones.](./assets/img/post/15networksec/net-evolution-sdn-p116-0-enterprise-three-tier-network-zones-diagram.png)
  - 大中型企业网/校园网的最常见的园区网络架构，采用<font color="#ff2600">三层架构（接入层，汇聚层，核心层）</font>，双核心网络。
  - 根据网络需求，分为用户区，对内服务区，对外服务区，管理区，互联网区等
  - 通过核心交换机和防火墙进行连接和隔离。
  - 互联网采用多出口连接，通过路由器进行博号和NAT，通过流控产品进行负载均衡/上网行为管理，通过防火墙进行安全隔离。
- 设备：路由器、交换机、无线AC/AP，防火墙、负载均衡/上网行为管理、服务器
- 技术：VLAN、TRUNK、MSTP\\HSRP/VRRP、Etherchannel、WLAN、OSPF、NAT、ACL、PPPOE、security SNMP等

## 网络架构案例 Network architecture examples

### 政务网

![Chalkboard diagram of a government network with core, aggregation and access layers, server zones, plus a printed explanation below.](./assets/img/post/15networksec/net-evolution-sdn-p117-0-government-mpls-wan-network-diagram.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

「图解」

①说明：政府网包括政府、电力、公安等，都采用类似的城域网架构，全网通过MPLS技术来设计，将不同的地市接入CE通过汇聚PE进行连接，并划分到不同的VRF中，核心设备作为P/PE进行高速转发。不同地市之间通过VRF隔离访问，当需要访问互联网、政务外网、服务器等，通过RD/RT的设计来实现适度互通。

②设备：路由器、交换机、负载均衡器、防火墙、入侵防御、防DDOS、服务\[?\]

③技术：VLAN、TRUNK、OSPF、BGP、MPLS、QoS、ACL、NAT、SNMP、Security等

**板书 Board labels:** Telecom / Mobile / Router / AC/AD / FW/IPS

</details>

### 数据中心网

![Chalkboard diagram of a data center network with three ISP links, router, IPS/DDOS, AC/AD and firewall layers, tenant and security zones.](./assets/img/post/15networksec/net-evolution-sdn-p118-0-data-center-tenant-and-security-zones.png)

![Printed Chinese explanation of a typical large layer-2 data center or IDC network design, with its devices and technologies.](./assets/img/post/15networksec/net-evolution-sdn-p118-1-data-center-design-explanation-text.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

「图解」

①说明：典型的大二层数据中心网络/IDC设计，主要分为租户区（服务集群）、互联网区、安全管理区。其中租户区采用设备虚拟化和链路虚拟化技术，将设备处理能力和链路承载能力提高，并且在服务器区域放置负载均衡器，将流量合理有效分配到固定的服务器上。互联网出口区采用路由器执行BGP和地址翻译，采用IPS/防DDOS设备放置大流量泛洪攻击，采用流控执行出口负载、采用防火墙进行安全隔离。安全管理区通过防火墙进行安全接入，通过审计、日志、入侵检测、网管等产品进行全网安全管理。

②设备：路由器、交换机、负载均衡器、防火墙、入侵检测/入侵防御、网络审计、防DDOS、服务器

③技术：VLAN、TRUNK、vPC、IRF、LISP、Vxlan、TRILL、FabriPath、\[?\]、BGP、MPLS、Security、SNMP\[?\]

注：互联网公司（百度、阿里、腾讯）、IDC/云计算服务器商等常见网络架构。

</details>

### 电信网/互联网是这样的

![Four ovals for Chinese carrier autonomous systems linked in a square, with BGP/MPLS written in the middle.](./assets/img/post/15networksec/net-evolution-sdn-p119-0-four-china-carrier-as-diagram.png)

![A mesh of Chinese province nodes connected to a dense core of major cities on a black background.](./assets/img/post/15networksec/net-evolution-sdn-p120-0-china-provincial-backbone-mesh-topology.png)

![Seven router symbols joined by lines in a mesh, labeled ISIS/BGP/MPLS in yellow.](./assets/img/post/15networksec/net-evolution-sdn-p121-0-isis-bgp-mpls-router-mesh.png)

![A text-only slide explaining the carrier and internet network, its devices and its technologies.](./assets/img/post/15networksec/net-evolution-sdn-p121-1-carrier-network-description-text.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

「图解」

①说明：电信网/互联网主要采用城域网技术架构来实现，主要用于承载全国/全球的客户流量，是互联网中最核心承载网络。不同运营商之间采用多个AS自治系统隔离和相连，通过BGP协议交互路由，采用MPLS实现标签交换。

②设备：路由器、交换机

③技术：OSPF/ISIS、BGP、MPLS、Multicast、TE/QoS、Security、SNMP等

</details>

## 为什么需要 SDN Why SDN

### 有哪些厂商在生产网络设备？

![Chalkboard listing network vendor names in four rows, with a printed explanation of three vendor categories below.](./assets/img/post/15networksec/net-evolution-sdn-p122-0-network-vendor-names-blackboard.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

「图解」

①简单来说，网络行业的厂商可以分为三大类，一类是综合厂商/全栈厂商，一类是安全厂商，一类是流控厂商。

②综合厂商是指的是能够提供从交换机、路由器、防火墙、无线等全系列产品并提供整体解决方案，例如思科、华为、Juniper、H3C等。安全厂商专门对外提供防火墙、入侵检测/入侵防御、安全网关、漏洞扫描、防病毒等产品，例如Checkpoint、启明星辰、绿盟科技、天融信、山石网科等。流控厂商主要有\[?\]Radware、Array Network、深信服、网康等。

**板书 Board labels:** F5 / Checkpoint / Radware / Array Network / Brocade / 思科 / 华为 / Juniper / 飞塔 / Aruba / H3C / 中兴 / 锐捷 / 深信服 / 启明星辰 / 绿盟科技 / 天融信 / 山石网科

</details>

### 如何对网络设备进行操作？

![Three routers from Cisco, Huawei and Juniper linked in a triangle, each with its own command-line syntax shown beside it.](./assets/img/post/15networksec/net-evolution-sdn-p122-1-multivendor-cli-commands-diagram.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

「图解」

①不同厂商生产的网络设备，需要通过不同的方式进行调试和配置，一般通过命令行和Web界面管理。由于各个公司有自己独立的网络操作系统，所以命令行和Web界面都是不同的。

②虽然命令行调试界面不同，但是底层遵循的网络协议是相同的，所以设备之间互操作是没有问题的。正是因为这一点，所以客户进行网络设备采购时，可以根据自身情况，根据产品价格、产品性能、\[?\]需求等来选择合适的技术方案。

③常见的网络中，很有可能有非常多的厂商设备混合，对于网络部署和管理是一个非常大的挑战。

**板书 Board labels:** cisco \> enable / cisco#conf t / (cisco-conf)# / 思科 / 华为 / \<Huawei\>system-view / \[Huawei\]sysname AR1 / \[AR1\]int g0/0/0 / \[AR1-g0/0/0\]undo sh / Juniper / system { / host-name JR / domain-name pinginglab.net / }

</details>

### 如何管理这么多网络设备？

![Multivendor router triangle with a network management server linked to each router by dashed SNMP lines.](./assets/img/post/15networksec/net-evolution-sdn-p123-0-snmp-network-management-system-diagram.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

「图解」

①网管服务器是目前主流的网络管理方案，网络设备（路由器、交换机、防火墙）和网管系统（例如H3C iMC、Huawei eSight）部署SNMP协议，通过网管系统可以对全网进行可视化拓扑发现、配置管理、链路质量检测等。

②网管系统是企业网络运维必不可少的组件，一般部署在服务区或者安全管理区域。

③SNMP协议即简单网络管理协议，更多侧重于对网络设备进行监控，而不是\[?\]和部署，也就是说，如果网络出现故障，通过网管系统告警了解情况，然后通过远程登录或者到IDC机房对设备进行命令调试和故障排除。

**板书 Board labels:** cisco \> enable / cisco#conf t / (cisco-conf)# / 思科 / 华为 / SNMP / 网管 / Juniper / system { / host-name JR / domain-name pinginglab.net / }

</details>

### 问题一：传统网络管理和部署非常麻烦

![Black slide stating many vendors, device types, device counts and inconsistent commands lead to hard deployment and management.](./assets/img/post/15networksec/net-evolution-sdn-p123-1-multivendor-deployment-management-difficulty-summary.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

网络厂商杂　设备类型多　设备数量多　命令不一致

部署难　管理烦

</details>

### 网络设备之间如何协同工作？

![Eight routers in a triangular mesh with yellow arrows showing neighbors passing information to each other in both directions.](./assets/img/post/15networksec/net-evolution-sdn-p124-0-distributed-protocol-relay-exchange-mesh.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

「图解」

①网络设备之间的沟通主要通过网络协议（交换、路由、标签、安全等协议）来实现，例如OSPF/BGP/MPLS/MSTP等等，大体的工作流程都是依据：「邻居建立-信息共享-路径选择」三个步骤来实现，这是很多协议设计的逻辑基础。

②大部分的网络采用典型的分布式架构，设备和设备之间以“接力棒”方式交互本地的信息，然后建立数据库信息，再根据选路算法进行最优路径选择，最具代表性的算法便是SPF算法。

③每个设备会进行独立的计算，有独立的“大脑”和独立的转发硬件。

④协议是互联网的基础，相当于人类沟通的语言。

</details>

![Router mesh where a failure notice for A passes hop by hop between neighbors, numbered in yellow by step.](./assets/img/post/15networksec/net-evolution-sdn-p124-1-network-change-failure-propagation-relay.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 如果网络发生变动？如何进行交互？

「图解」

①当网络发生动荡时，网络设备会将故障信息以“接力棒”的方式不断告知下\[?\]邻居设备，然后将故障路径信息删除。

②网络收敛过程中，有可能出现冗余的路径通告信息。

</details>

![Router mesh with failure notices spreading toward a red swamp-like contour map and a sad face on the right.](./assets/img/post/15networksec/net-evolution-sdn-p125-0-traffic-surge-topology-swamp-convergence.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 当流量暴涨拓扑膨胀时

「图解」

①随着云计算、大数据、移动互联等技术发展，流量不断翻番，使得底层网络的体积膨胀，压力增大；网络体积越大，需要收敛的时间越长。等

②在所有的网络类型中，数据中心网（互联网公司）、电信网（运营商）的网络压力最大，需要变革的意愿最强。

**板书 Board labels:** 沼泽地

</details>

### 问题二：分布式网络架构瓶颈凸显

![Black slide listing independent computing, relay interaction and distributed architecture, with an arrow to bottleneck becomes prominent.](./assets/img/post/15networksec/net-evolution-sdn-p125-1-distributed-architecture-bottleneck-summary.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

独立计算　接力棒交互　分布式架构

瓶颈凸显

</details>

![Two chalkboard diagrams: unbalanced link load between routers, and a data center fabric with colored flows of different bandwidth to the Internet.](./assets/img/post/15networksec/net-evolution-sdn-p126-0-network-bandwidth-allocation-problem-diagrams.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 网络带宽分配如何解决？

**板书 Board labels:** Internet / 1G\<95%\> / 1G\<20%\> / 50M / 30M / 12M / 5M / 2M / 1M

</details>

![A text-only slide explaining traffic control with QoS and TE, where it runs, and its static bandwidth limits.](./assets/img/post/15networksec/net-evolution-sdn-p126-1-qos-te-traffic-control-text.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

「图解」

①流量控制一般采用QoS/TE等技术来实现，大体的思路就是：通过为流量分类和标记，定义不同的优先级别，根据业务需求，分配不同的带宽。流控的好坏直接影响带宽利用率，影响客户的投资效益。

②流控技术可以在支持QoS/TE的交换机、路由器等产品上执行，也可以在专业的流控产品（负载均衡器）上实现。

③不管是软件还是硬件实现流控，传统的流控产品大体是一种静态带宽处理，\[?\]据业务需求，制定特定规则，走特定的链路等等，策略一般是前期固定好的，无法根据网络情况，智能的实现带宽分配。

</details>

![Chalkboard diagram of a two-tier switch network connected to the Internet with links colored red, yellow and green by congestion percentage.](./assets/img/post/15networksec/net-evolution-sdn-p127-0-traffic-visualization-link-congestion-topology.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 流量可视化难！

「图解」

①常规流控产品只能实现部分链路带宽分配可视化，常规网管系统只能实现链路状态故障检测等，无法实现全网全局链路带宽可视化。

②全网流量可视化是带宽智能调配的基础。

**板书 Board labels:** 拥塞 / 一般 / 畅通 / Internet

</details>

### 问题三：流量控制是棘手难题

![Chalkboard diagram of packets crossing switches A to D where a device cannot apply a custom forwarding policy for source and destination IPs.](./assets/img/post/15networksec/net-evolution-sdn-p128-0-custom-forwarding-policy-device-blackbox.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 能否自定义设备的转发策略？

「图解」

①传统的网络设备，工作方式一般都是固定好的，例如交换机根据MAC地址表转发（基于源MAC学习，基于目的MAC转发），路由器根据路由表转发（修改源目MAC，源目IP不修改，基于目的IP查表）。

②按照业务需求进行网络设备的策略自定义，实际上便是一个可编程的需求，\[?\]统网络设备是一个黑盒子，内部源码、产品功能对用户封闭，话语权在网络厂商这边。

</details>

![Chalkboard diagram of an arrow labeled Software pointing at three network devices, each marked no, with a sad red face.](./assets/img/post/15networksec/net-evolution-sdn-p128-1-software-cannot-run-on-device.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 能否将这个软件运行在设备上?

「图解」

①不可编程，无法按需，是网络设备几十年来的老规矩！

**板书 Board labels:** Software / no! / no! / no!

</details>

![Chalkboard slide with the phrases cannot be on demand and not programmable pointing down to a box reading eat hard not soft.](./assets/img/post/15networksec/net-evolution-sdn-p129-0-problem-four-not-programmable-on-demand.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 问题四：无法按需，不可编程

**板书 Board labels:** 无法按需 / 不可编程 / 吃硬不吃软

</details>

## SDN是什么？

### SDN是什么？学术界，怎么又是斯坦福？跨世纪的继承

![Chalkboard diagram of the Ethane design with a central controller running NOX sending OpenFlow instructions to four switches.](./assets/img/post/15networksec/net-evolution-sdn-p130-0-sdn-origins-academia-stanford-ethane.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** SDN是什么？学术界，怎么又是斯坦福？跨世纪的继承！

「图解」

①2007年，斯坦福大学博士生Martin Casado 领导了一个关于网络安全与管理的项目Ethane，该项目试图通过一个集中式的控制器，让网络管理员可以方便地定义基于网络流的安全控制策略，并将这些安全策略应用到各种网络设备中，从而实现对整个网络通讯的安全控制。

②2008年，基于Ethane 及其前续项目Sane的启发， Nick McKeown教授等人提出了OpenFlow 的概念，并于当年在ACM SIGCOMM 发表了题为《OpenFlow: Enabling Innovation in Campus Networks》的论文，首次详细地介绍了OpenFlow 的概念。

③上图中，交换机没有独立的“大脑”，仅具备转发功能，所有的路径计算、安全策略等等全部在控制器（Controller）上执行，然后通过Openflow协议下发给交换机，交换机根据流表（Flow table）进行转发。

④Ethane这种网络架构跟传统的网络架构相比，最大的特点便是：控制和转发完全分离！控制层实现集中式控制、软件可编程、可视化、自动化等等，转发层通过硬件实现高速转发。

注：

全球第一台路由器由斯坦福大学的莱昂纳德·波萨克和桑蒂·勒纳这对教师夫妇创造的，用于斯坦福大学校园网络（SUNet），而全球网络行业的领头羊思科便是这对夫妇创立的（1984年）。

巧合的是，20多年后（2006年），同样来自斯坦福的学生Martin Casado和\[?\]ick McKeown开创并奠定了Openflow/SDN基础，实现跨世纪的接力棒，为互联网技术注入未来！

**板书 Board labels:** Martin Casado / Nick McKeown / Ethane / Controller / NOX / openflow / switch

</details>

### SDN是什么？商业界，一马当先的Google，标杆案例B4网络

![Chalkboard diagram of Google B4 with a Gateway and TE Server above three controllers, each managing a data center site linked by BGP.](./assets/img/post/15networksec/net-evolution-sdn-p131-0-google-b4-network-sdn-case.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** SDN是什么？商业界，一马当先的Google，标杆案例B4网络！

「图解」

①Google B4网络是谷歌的数据中心网络，用于存储和备用用户数据。B4网络由不同的数据中心站点组成，采用非常多的WAN链路互联。由于WAN光纤成本昂高，数据中心的链路利用率不高（30%-40%），谷歌需要通过引入软件实现流量可视化和路径可操作等需求，提高WAN链路利用率。

②Google B4网络是目前最知名影响最广泛的SDN商用案例，可以说是目前SDN浪潮中的标杆案例。此网络架构充分利用了SDN的核心思想，引入Openflow交换机，采用分布式的Controller架构，而且应用在流量密集环境复杂的数据中心，最终将链路利用率提高到接近100%！

③Quagga是开源的路由协议栈，用于运行ISIS/BGP路由协议。RAP（Routing Application Proxy）是路由应用代理程序，作为交换机到Quagga的代理，例如Openflow交换机将链路状态信息发给Controller之后，Controller会调用RAP将信息转发给Quagga协议栈处理。Paxos是一个选举器，用于选择Controller集群中，哪个主哪个备。TE Agent用于收集数据中心的链路/带宽信息等，然后将其交给顶层的Gateway，Gateway进行汇总再交给TE Server计算路径等。TE Server计算好路径和带宽分配信息之后，也会返回给Gateway，由Gateway下发给C\[?\]ller，再由Controller下发给Op\[?\]flow交换机，即TE Server--\>Gateway--\>Controller--\>Switch。

**板书 Board labels:** Gateway / TE Server / Quagga / RAP / TE Agent / Paxos / Controller / Onix / BGP / site A / site B / site C

</details>

### SDN是什么？运营商NFV/ETSI

![Chalkboard diagram showing separate router, switch and firewall devices on the left merged into one big box of virtual functions on the right.](./assets/img/post/15networksec/net-evolution-sdn-p132-0-nfv-etsi-operator-virtualization.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** SDN是什么？运营商NFV/ETSI

「图解」

①NFV（network function virtualization）即网络功能虚拟化，核心思想是将网络硬件设备通过虚拟化技术，集成到通用的服务器或其他硬件平台上，然后在通用标准的硬件平台上，执行路由器、交换机、负载均衡、防火墙、入侵防御等功能。说白了，就是将分散的网络硬件产品集成到一个“大盒子”里面，然后每种产品相当于一个插件来使用。

②NFV与SDN虽然是由不同的组织来引导发展，但是基本诉求是一致的：将\[?\]网络架构软件化/虚拟化，统一部署管理，可以为客户节省大量成本。

**板书 Board labels:** 虚拟化 / 省成本 / 易迁移 / 易扩展 / 易部署

</details>

### SDN到底是什么?

![Two chalkboards: the words Software Defined Network, and a comparison list of SDN network versus traditional network traits.](./assets/img/post/15networksec/net-evolution-sdn-p133-0-sdn-definition-versus-traditional-network.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** SDN到底是什么?

**板书 Board labels:** Software Defined Network / SDN网络 VS 传统网络 / 控制转发分离 / 控制转发耦合 / 集中式控制 / 分布式控制 / 可编程 / 不可编程 / 开放接口 / 不开放

</details>

![Chalkboard diagram of SDN layers: application on top, two controllers with REST API northbound and OpenFlow southbound, and forwarding devices below.](./assets/img/post/15networksec/net-evolution-sdn-p134-0-sdn-three-layer-architecture-openflow.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

「图解」

①SDN（Software Defined Network）即软件定义网络，是一种网络设计理念，或者一种推倒重来的设计思想。只要网络硬件可以集中式软件管理，可编程化，控制转发层面分开，则可以认为这个网络是一个SDN网络。所以说，SDN并不是一个具体的技术，不是一个具体的协议，而是一个思想、一个框架。

②狭义的SDN是指的“软件定义网络”，广义的SDN的概念还延伸出了：软件定义安全、软件定义存储等等。可以说，SDN是一个浪潮，席卷整个IT产业。

③SDN框架主要由应用层、控制层、转发层（基础设施层）组成，其中应用层提供应用和服务（网管、安全、流控等）、控制层提供统一管理和控制（协议计算、策略下发、链路信息收集）、\[?\]硬件设备（交换机、路由器、防火墙等）进行数据转发。

**板书 Board labels:** 应用层 / 控制层 / 转发层 / Application / Controller / API / REST API \<北向接口\> / openFlow \<南向接口\>

</details>

### 哪些组织在推动SDN发展?

![Chalkboard ring diagram of SDN organizations: ODL, ONF and ONOS in the center, surrounded by ETSI/NFV, OPNFV, OCP and ONRC.](./assets/img/post/15networksec/net-evolution-sdn-p135-0-sdn-standards-organizations-onf-odl-onos.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 哪些组织在推动SDN发展?

「图解」

①ONF（Open Networking Foundation）即开放网络联盟，于2011年成立，是最早的SDN组织，创始成员主要是Google、Facebook、微软、雅虎等互联网成员（后期加入了腾讯、华为、中兴、中国移动等），旨在推动SDN的标准化（ONF Plugfest），制定并发布Openflow技术标准。

②ODL（OpenDayLight）成立于2013年4月，由思科携手IBM、Juniper、BigSwitch、Broadcade、Redhat、VMware、NEC、Arista、惠普、英特尔、Citrix、Ericsson等发起，成员主要是网络厂商。ODL主要是为了打造一个开源的SDN平台框架，包括网络应用和服务、北向接口、控制器、南向接口等等，更简单一点，就是提供开源的网络操作系统，目前最核心的是做了行业默认标准的OpenDayLight控制器（SDN系统）。

③ONOS（Open Network Operating System）即开发网络操作系统，于2014年11月成立，创始成员主要包括ON.LAB、AT&T、NTT、华为、爱立信、富士通、NEC、Ciena、Intel，成员主要来自运营商，旨在为运营商用户提供一个开源网络控制器。目前核心工作是做出了面向运营商的ONOS控制器（SDN系统），与ODL控制器直面竞争。

④NFV（Network Function Virtualization）即网络功能虚拟化，成立于2012年10月，由AT&T、英国电信、德国电信、中国移动等成员提出，成员主要来自运营商，该组织所属欧洲电信标准协\[?\]SI，致力于\[?\]设备虚拟化，提\[?\]运营能力减低运维成本等。

**板书 Board labels:** ETSI/NFV / ODL / ONF / ONOS / ONRC / OPNFV / OCP

</details>

### SDN网络交互方式变革

![Chalkboard comparison: devices managed by CLI, SNMP and HTML on the left, versus controllers with APIs used by C, Java and Python on the right.](./assets/img/post/15networksec/net-evolution-sdn-p136-0-sdn-interaction-cli-to-api-change.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** SDN网络交互方式变革

「图解」

①传统的手工作坊式的网管方式会慢慢被软件的方式代替，更好的满足自动化运维需求。

②手工的命令配置不会被完全消除，很多初始化和自动化没法解决的问题，还\[?\]要人为干预。只不过遵循一个规则：能软则软，能自动化则自动化！

**板书 Board labels:** CLI / SNMP / HTML / C / Java / python / API / Controllers

</details>

### 产业链分析（玩家图谱）

![Chalkboard triangle diagram of three SDN players: equipment users, network vendors and software vendors, with example company names beside each.](./assets/img/post/15networksec/net-evolution-sdn-p137-0-sdn-industry-chain-player-map.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 产业链分析（玩家图谱）

「图解」

①设备用户：主要倡导并推动SDN发展的创始玩家，是用户而不是网络厂商。因为互联网公司（谷歌、Facebook）、运营商（AT&T、NTT）等网络的压力最大（数据中心网、互联网），最渴求变革。

互联网公司/运营商

②网络厂商：分为老牌网络厂商（思科、Juniper、华为、H3C、F5、Radware）和新网络厂商（Big Switch、Nicira）。老牌网络厂商一直对网络行业有着不可撼动的技术和市场能力，对SDN发展原来持观望和被动状态，但是目前已经成为各个SDN组织最活跃的机构，他们通过将自有的产品加入SDN支持，提供混合和全部的SDN产品，依靠原有的渠道，牢牢掌握原有的市场份额。新网络厂商希望SDN大力发展起来，给自己多一些机会，通过自身革命性的解决方案，提供物美价廉的技术方案来争夺老牌网络厂商的蛋糕。

③软件厂商：加入SDN主战场的软件厂商主要有Vmware、Citrix、Redhat等，本来SDN跟他们没什么关系，但是网络虚拟化的快速发展，跟原有他们的服务器虚拟化等技术撞上了，所以他们希望SDN和NFV大力发展，最好将网络硬件通通软件化，然后将网络集成进入自己的服务器，再通过原有的虚拟化技术进\[?\]理。2012年，Vmware 12亿\[?\]元收购Nicira（创始人是Openflow之父Martin Casado）正式与思科在SDN网络战场竞争。

**板书 Board labels:** 设备用户 / Google / Facebook / ebay / AT&T / NTT / 网络厂商 / 思科 / 华为 / Juniper / H3C / 软件商 / Vmware / Citrix / Redhat

</details>

### 学习SDN的最佳姿势

![Text-only slide listing four steps for learning SDN: traditional networking knowledge, a programming language, OpenFlow white papers, and a hands-on lab.](./assets/img/post/15networksec/net-evolution-sdn-p138-0-best-way-to-learn-sdn-steps.png)

<details markdown="1"><summary>转录 Transcription (read from the image by Claude, may contain errors)</summary>

**标题 Title:** 学习SDN的最佳姿势

Step1：既然SDN是网络技术的前言，那学习SDN必须要懂传统的网络知识.

• 协议栈：ARP、IP、ICMP、UDP、TCP、DHCP、DNS等

• 路由技术：OSPF、ISIS、BGP、IPv6、Multicast等

• 交换技术：VLAN、Trunk、Ethechannel、VRRP等

• 标签技术：MPLS、MPLS L2VPN、MPLS L3 VPN、MPLS TE等

• 流控技术：QoS（分类标记、队列机制、拥塞避免、监管整形）

• 安全技术：IPsec VPN、SSL VPN、Firewall、IDS/IPS

建议学习以上内容的时候，参考思科、华为等网络厂商的认证课程（CCNA/HCNA等），按照基础到进阶到高级一点点知识累积起来。

Step2：需要懂一门编程语言，经典的C或者C++，还是Java或Python.

目前大部分的控制器都是Java和Python写的；对于网络工程师出身的，如果是编程新手，直接从Python入手，如果是码农，对于各种编程语言都比较熟悉，那直接忽略本步骤，回到 Step1。

Step3：开始啃各种OpenFlow白皮书，阅读OpenFlow行业大会的PPT和资料（靠谱的技术方案，靠谱的商用案例）.

OpenFlow的白皮书可以直接到官网下载，根据版本迭代从1.0到目前的1.5版本，最好通读一遍英文版，然后再搜集国内的一些中文翻译版。OpenFlow的行业大会无非就是ONF/ONS、OpenDayLight、ONOS等，技术大会是整个行业的方向标，有利于判断现阶段SDN走到什么阶段，有什么比较好的商用案例借鉴，是否有新的产品更新等等。

Step4：搭建SDN学习环境，开始上手折腾起来.

常用的SDN虚拟系统/控制器，例如Mininet、OpenDayLight、ONOS等。通过这些工具搭建出SDN网络，然后通过Wireshark工具来进行OpenFlow协议分析，通过编程语言如Python编写基础\[?\]用，并进行测试。（前期可以研读一些开源的SDN代码，再慢慢根据自己的业务需求来进行定制）

</details>

---

## Suspected typos

The wording above is kept as in the source. These look like typing errors: `主要死网卡口` (是), `多亿防火墙`, `博号` (拨号), `分布：路由器、交换机` (分部).
