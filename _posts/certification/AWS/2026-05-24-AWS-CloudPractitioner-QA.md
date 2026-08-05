---
title: "Meow's AWS - Cloud Practitioner Exam Q&A"
date: 2026-05-24 11:11:11 -0400
categories: [certification, AWS]
tags: [AWS, IAM, EC2, S3, VPC, RDS, CloudWatch, CloudFront, Lambda, CloudFormation, ExamPrep, CloudPractitioner]
math: false
toc: true
---

# AWS Cloud Practitioner Exam Q&A

AWS Cloud Practitioner 考试练习题，涵盖云概念、IAM、EC2、S3、VPC、数据库、监控和计费等核心领域。

Practice questions for the AWS Cloud Practitioner exam, covering cloud concepts, IAM, compute, storage, networking, databases, monitoring, and billing.

---

## Cloud Concepts 云概念

---

**Q: What are the 6 advantages of cloud computing?**
云计算的 6 大优势是什么？

> <font color=OrangeRed>**A: (1) Trade capital expenses for variable expenses / (2) Benefit from massive economies of scale / (3) Stop guessing about capacity / (4) Increase speed and agility / (5) Stop spending money running data centers / (6) Go global in minutes**</font>

云计算的六大优势：以可变成本替代资本支出、受益于规模经济、告别容量猜测、提升速度与敏捷性、停止维护数据中心、数分钟内实现全球部署。

---

**Q: What are the 3 types of cloud computing?**
云计算的三种类型是什么？

> <font color=OrangeRed>**A: IaaS (e.g. EC2), PaaS (e.g. Elastic Beanstalk), SaaS (e.g. Gmail)**</font>

- **IaaS** 基础设施即服务：用户管理 OS、运行时、数据、应用 / User manages OS, runtime, data, application
- **PaaS** 平台即服务：用户只管理应用和数据 / User manages only application and data
- **SaaS** 软件即服务：供应商管理一切 / Vendor manages everything

---

**Q: What are the 3 cloud deployment models?**
云的三种部署模型是什么？

> <font color=OrangeRed>**A: Public Cloud (AWS/Azure/GCP), Hybrid (mix of public + private), Private/On-Premises (OpenStack/VMware)**</font>

- **Public cloud** typically incurs OPEX costs — the consumer does not own the infrastructure.
- **Private cloud**: the consumer organization owns and manages the infrastructure.
- **Hybrid**: a mix of public and private.

> **Note:** "On-premises cloud" is a deployment **model**, not a cloud computing **model**.

---

**Q: What is the AWS global infrastructure hierarchy from largest to smallest?**
AWS 全球基础设施从大到小的层级是什么？

> <font color=OrangeRed>**A: AWS Global Infrastructure → AWS Regions → Availability Zones → Data Centers**</font>

---

**Q: What is an Availability Zone?**
可用区（AZ）是什么？

> <font color=OrangeRed>**A: An AZ is one or more discrete data centers housed in separate facilities, each with redundant power, networking, and connectivity.**</font>

可用区由一个或多个独立设施中的数据中心组成，各设施均有冗余电力、网络和连接。

---

**Q: How does elasticity differ from scalability?**
弹性（Elasticity）与可扩展性（Scalability）有何区别？

> <font color=OrangeRed>**A: Elasticity not only scales out but also shrinks back down based on demand; scalability focuses on the ability to scale up.**</font>

弹性不仅能扩容，还能根据需求自动缩容；可扩展性侧重于向上扩展的能力。

---

**Q: What is fault-tolerance?**
容错性是什么？

> <font color=OrangeRed>**A: The ability to maintain operations during and/or after failure.**</font>

---

**Q: How can an application achieve high availability and fault-tolerance?**
应用如何实现高可用性和容错性？

> <font color=OrangeRed>**A: By utilizing multiple Availability Zones.**</font>

---

## IAM / Security

---

**Q: What does IAM stand for, and is it regional or global?**
IAM 代表什么？它是区域级还是全局级？

> <font color=OrangeRed>**A: Identity and Access Management. IAM users, groups, and roles are created globally.**</font>

IAM 是身份和访问管理服务，用户、组和角色均在全局范围内创建，不受区域限制。

---

**Q: What access privileges does a new IAM user have by default?**
新创建的 IAM 用户默认拥有哪些权限？

> <font color=OrangeRed>**A: No access to AWS services (zero permissions by default).**</font>

新 IAM 用户默认无任何 AWS 服务访问权限，必须显式附加策略才能获得权限。

---

**Q: In this scenario: an IAM User has a DenyAll policy, but is also in an IAM Group with access to S3, EC2, VPC, and IAM. Which resources can the user access?**
某 IAM 用户有 DenyAll 策略，同时所在组有 S3/EC2/VPC/IAM 访问权限，该用户能访问哪些资源？

> <font color=OrangeRed>**A: None — an explicit Deny always overrides an explicit Allow.**</font>

显式拒绝（Deny）永远优先于显式允许（Allow）。

---

**Q: What is the most efficient way to give 3 developers access to S3?**
给 3 个开发者授予 S3 访问权限，最高效的方式是什么？

> <font color=OrangeRed>**A: Add the developers to an IAM Group and attach an IAM policy to that group.**</font>

将用户加入组、再为组附加策略，是最低管理开销的方式。

---

**Q: What are IAM roles, and are they regional or universal?**
IAM 角色是什么？它们是区域性还是全局性的？

> <font color=OrangeRed>**A: IAM roles are universal — they can be used in any AWS region. Roles are a better alternative to using Access Key IDs and Secret Access Keys.**</font>

IAM 角色是全局的，可在任何区域使用。角色比硬编码访问密钥更安全——删除角色即可立即撤销访问权限。

---

**Q: What is the AWS Shared Responsibility Model?**
AWS 共同责任模型是什么？

> <font color=OrangeRed>**A: AWS is responsible for security OF the cloud (hardware, facilities, global infrastructure, hypervisor). Customers are responsible for security IN the cloud (OS, data, IAM, application security).**</font>

- **AWS 负责**：物理硬件、设施、全球基础设施、虚拟化层 / hardware, facilities, infrastructure, hypervisor
- **客户负责**：操作系统、数据、IAM、应用安全 / OS, data, IAM, application security

> **Example:** If an AWS datacenter is breached by unauthorized personnel, AWS is responsible.

---

**Q: What is the difference between AWS WAF, AWS Shield, AWS GuardDuty, and Amazon Inspector?**
AWS WAF、Shield、GuardDuty、Inspector 的区别是什么？

> <font color=OrangeRed>**A: WAF = web app firewall (protects apps behind ELB/CloudFront). Shield = DDoS protection. GuardDuty = threat detection for accounts/workloads. Inspector = automated vulnerability assessment for EC2 instances only.**</font>

| 服务 Service | 作用 Purpose |
|---|---|
| AWS WAF | Web 应用防火墙，保护 ELB/CloudFront 后面的应用 / Web app firewall, protects apps behind ELB or CloudFront |
| AWS Shield | DDoS 防护 / DDoS mitigation |
| AWS GuardDuty | 账户和工作负载威胁检测服务 / Threat detection for AWS accounts and workloads |
| Amazon Inspector | 仅适用于 EC2 实例的自动漏洞评估 / Automated vulnerability assessment for EC2 instances ONLY |

---

**Q: What is AWS KMS, and what service does it integrate with for key event logging?**
AWS KMS 是什么？它与哪个服务集成用于记录密钥事件？

> <font color=OrangeRed>**A: KMS (Key Management Service) manages encryption keys. Keys may be generated in KMS, a CloudHSM cluster, or imported from other services. KMS integrates with CloudTrail for logging key events.**</font>

KMS 管理加密密钥，可与 CloudTrail 集成记录密钥使用日志，也可通过 SNS 发送 KMS 活动通知。

---

**Q: What penetration testing activities are prohibited on AWS without prior approval?**
哪些渗透测试活动在 AWS 上未经预先授权是被禁止的？

> <font color=OrangeRed>**A: Prohibited (even with approval): DDoS attacks, port flooding, DNS Zone walking via Route 53. Allowed without prior approval: EC2 instances, RDS, Lightsail, CloudFront, Elastic Beanstalk.**</font>

- **禁止（即使申请也不行）Prohibited:** DDoS 攻击、端口洪泛、Route 53 DNS Zone walking
- **无需预先批准可测试 Allowed without approval:** EC2、RDS、Lightsail、CloudFront、Elastic Beanstalk

> **Note:** S3 is NOT in the allowed list for penetration testing without prior approval.

---

## Compute 计算

---

**Q: What are the 4 EC2 pricing models?**
EC2 的四种定价模型是什么？

> <font color=OrangeRed>**A: On-Demand, Reserved, Spot, Dedicated Hosts**</font>

| 定价模型 Pricing Model | 适用场景 Use Case |
|---|---|
| **On-Demand** 按需 | 无前期承诺，最高灵活性；适合短期无法中断的负载（如节假日流量激增）/ No upfront, max flexibility; good for short-term must-be-available workloads |
| **Reserved** 预留 | 承诺 1–3 年，大幅折扣；适合稳定可预测的负载 / 1–3 year commit, significant discount; best for steady-state predictable workloads |
| **Scheduled RI** 计划预留 | 按可预测的重复日期和时间匹配容量预订 / Matches capacity reservation to predictable recurring dates and times |
| **Spot** 竞价 | 价格最低但可被中断；适合可容忍中断的弹性工作负载 / Lowest price but can be interrupted; for fault-tolerant flexible workloads |
| **Dedicated Host** 专用主机 | 物理主机专用，可带入自有许可证（BYOL）/ Physical server dedicated to you; supports bring-your-own-license |

---

**Q: For a workload that must run for up to 4 months and must always be available, which instance type is best?**
一个需要运行最多 4 个月且必须始终可用的工作负载，应选择哪种实例类型？

> <font color=OrangeRed>**A: On-Demand — no minimum commitment, pay only for what you use, always available.**</font>

Reserved 至少需要 1 年承诺；Spot 可能被中断。对于短期且必须可用的负载，On-Demand 是唯一合适的选项。

---

**Q: What are the benefits of Reserved Instances?**
预留实例（Reserved Instances）有哪些好处？

> <font color=OrangeRed>**A: Reduced cost (significant discount from on-demand) + ability to reserve capacity in a specific Availability Zone.**</font>

---

**Q: Where can resources be launched when configuring EC2 Auto Scaling?**
配置 EC2 Auto Scaling 时，资源可以在哪里启动？

> <font color=OrangeRed>**A: Multiple AZs within a single region — Auto Scaling cannot launch resources into another AWS Region.**</font>

EC2 Auto Scaling 在 EC2 控制台内配置，可在一个区域内跨多个可用区启动实例，不能跨区域。

---

**Q: What is EC2 Dedicated Host?**
EC2 专用主机（Dedicated Host）是什么？

> <font color=OrangeRed>**A: A physical EC2 server dedicated for your use, allowing you to bring your own server-bound software licenses (BYOL).**</font>

> **Dedicated Host vs. Dedicated Instance:** Dedicated Instances run on hardware dedicated to a single customer but share hardware with other instances from the same account. Dedicated Hosts provide a full physical server with more control.

---

**Q: What is AWS Lambda?**
AWS Lambda 是什么？

> <font color=OrangeRed>**A: A serverless compute service that runs code without requiring server management. Charges only when code is executed. Integrates with most AWS services.**</font>

Lambda 特点：
- 无需管理服务器 / No server management
- 按实际执行时间计费 / Charges only when code runs
- 高度可扩展 / Highly scalable
- 与大多数 AWS 服务集成 / Integrates with most AWS services

**Lambda 不适合的用例:** 数据仓库（应使用 Redshift）/ Data warehousing (use Redshift instead)

**Lambda 支持的运行时:** Node.js、Ruby、Java、Python、Go、.NET 等 / Node.js, Ruby, Java, Python, Go, .NET

---

**Q: Are Elastic Beanstalk and CloudFormation free?**
Elastic Beanstalk 和 CloudFormation 本身收费吗？

> <font color=OrangeRed>**A: No charge for the service itself — but the AWS resources they provision (EC2, RDS, etc.) do incur costs.**</font>

服务本身免费，但它们所创建的 EC2 实例、RDS 等资源按正常定价收费。

---

**Q: Can CloudFormation provision any AWS service? Is Elastic Beanstalk programmable?**
CloudFormation 能置备任意 AWS 服务吗？Elastic Beanstalk 可编程吗？

> <font color=OrangeRed>**A: CloudFormation can provision almost any AWS service and is programmable. Elastic Beanstalk is limited in what it can provision and is NOT programmable.**</font>

| 服务 | 置备范围 | 可编程 |
|---|---|---|
| CloudFormation | 几乎所有 AWS 服务 / Almost any service | 是 Yes |
| Elastic Beanstalk | 有限 / Limited | 否 No |

---

**Q: Which service should a user with limited AWS knowledge use to quickly deploy a scalable Node.js application in a VPC?**
AWS 知识有限的用户，如何在 VPC 中快速部署可扩展的 Node.js 应用？

> <font color=OrangeRed>**A: AWS Elastic Beanstalk — handles capacity provisioning, load balancing, auto-scaling, and health monitoring automatically.**</font>

---

**Q: What are the 3 types of load balancers?**
三种负载均衡器类型是什么？

> <font color=OrangeRed>**A: Application Load Balancer (Layer 7, application-aware), Network Load Balancer (Layer 4, high performance), Classic Load Balancer (legacy, dev/test use)**</font>

---

## Storage 存储

---

**Q: What are the 6 S3 storage classes?**
S3 的 6 种存储类型是什么？

> <font color=OrangeRed>**A: S3 Standard, S3-IA (Infrequent Access), S3 One Zone-IA, S3 Intelligent-Tiering, S3 Glacier, S3 Glacier Deep Archive**</font>

- **S3 Standard** is the most expensive. 最贵。
- **S3 Glacier Deep Archive** is the cheapest — best for long-term archival with no retrieval time requirements. 最便宜，适合无时效要求的长期归档。

---

**Q: What are the key fundamentals of S3?**
S3 的核心基本概念是什么？

> <font color=OrangeRed>**A: Object-based storage (files only, not OS/DB), unlimited storage, files stored in buckets, universal namespace (bucket names must be unique globally), HTTP 200 = successful upload.**</font>

- S3 是对象存储，不能安装操作系统或数据库 / Object storage; cannot install OS or DB
- 存储容量无限制 / Unlimited storage
- 文件存放在 Bucket（桶）中 / Files stored in buckets
- Bucket 名全局唯一 / Bucket names globally unique across AWS
- 上传成功返回 HTTP 200

---

**Q: What is the S3 consistency model?**
S3 的一致性模型是什么？

> <font color=OrangeRed>**A: Read-after-write consistency for new object PUTs. Eventual consistency for overwrite PUTs and DELETEs (can take time to propagate).**</font>

- **新对象 PUT** → 写后即读一致性（read-after-write consistency）
- **覆盖 PUT 和 DELETE** → 最终一致性（eventual consistency）

---

**Q: Do you view S3 buckets globally or regionally? Can you store buckets in individual regions?**
S3 桶是全局查看还是区域查看？可以将桶存储在特定区域吗？

> <font color=OrangeRed>**A: Buckets are viewed globally in the console, but data is actually stored in a specific region. You can (and should) choose the region for data residency and compliance.**</font>

---

**Q: How can you make an entire S3 bucket public?**
如何将整个 S3 桶设为公开？

> <font color=OrangeRed>**A: Use bucket policies.**</font>

---

**Q: What does S3 Cross-Region Replication do?**
S3 跨区域复制有什么作用？

> <font color=OrangeRed>**A: Automatically replicates the contents of one bucket to another bucket in a different region.**</font>

Data stored within an AWS Region is NOT replicated outside that region automatically — customers must configure this explicitly.

---

**Q: What is an EBS volume?**
EBS 卷是什么？

> <font color=OrangeRed>**A: A highly available and reliable storage volume that can be attached to any EC2 instance in the same Availability Zone.**</font>

- EBS 是块存储，只能在同一可用区内附加 / Block storage; attachable only within same AZ
- 默认情况下，根 EBS 卷在实例终止时被删除 / Root EBS volume deleted on termination by default

---

**Q: What are the types of AWS Storage Gateway?**
AWS Storage Gateway 有哪些类型？

> <font color=OrangeRed>**A: File Gateway (uploads to S3), Volume Gateway (Stored Volumes: data on-premises; Cached Volumes: data in AWS cloud), Virtual Tape Library (VTL) Gateway (long-term archival)**</font>

Storage Gateway 是混合存储服务（Hybrid Storage Service），必须保留在本地环境中运行。

---

## Database 数据库

---

**Q: What are the 6 RDS database engines?**
RDS 支持哪 6 种数据库引擎？

> <font color=OrangeRed>**A: SQL Server, MySQL, PostgreSQL, Oracle, Amazon Aurora, MariaDB**</font>

---

**Q: What are the key features of Relational Databases in AWS?**
AWS 关系数据库的核心特性是什么？

> <font color=OrangeRed>**A: (1) Multi-AZ for disaster recovery / (2) Read Replicas — reads from copy, writes to primary**</font>

- **Multi-AZ**：跨可用区自动故障转移，用于灾难恢复。读写均在主库。
  Multi-AZ automatic failover for DR. Reads and writes go to the primary.
- **Read Replicas**：读请求发往副本，写请求仍发往主库，减少主库读压力。
  Reads served from the replica; writes go to the primary. Reduces read load.

> **RDS benefits:** Cost-efficient, scalable, fully managed, resizable database.

---

**Q: Which AWS service should be used for data warehousing and SQL/BI analytics?**
哪个 AWS 服务用于数据仓库和 SQL/BI 分析？

> <font color=OrangeRed>**A: Amazon Redshift — a data warehouse database service optimized for complex analytical queries.**</font>

Redshift 是亚马逊的数据仓库服务，专为复杂查询构建，支持标准 SQL 和 BI 工具集成。

---

**Q: What is ElastiCache, and what engines does it support?**
ElastiCache 是什么？支持哪些引擎？

> <font color=OrangeRed>**A: ElastiCache is a data caching database service. It supports Redis and Memcached.**</font>

ElastiCache 将数据缓存在内存中，大幅提升读取性能，减少主数据库的查询压力。

---

**Q: What are the differences between RDS and DynamoDB?**
RDS 和 DynamoDB 的区别是什么？

> <font color=OrangeRed>**A: RDS is a SQL (relational) database; DynamoDB is NoSQL. DynamoDB supports JSON document store models; RDS does not. RDS offers multiple database software options; DynamoDB does not.**</font>

DynamoDB 替代的 NoSQL 数据库包括：Oracle NoSQL、Cassandra DB、MongoDB。

---

## Networking 网络

---

**Q: What is a VPC, and how many are created by default per region?**
VPC 是什么？每个区域默认创建几个？

> <font color=OrangeRed>**A: Virtual Private Cloud — a logically isolated section of the AWS Cloud. One default VPC is created per region, with one subnet per Availability Zone.**</font>

VPC 是 AWS 云中的逻辑隔离网络段。每个区域默认有 1 个 VPC，每个 AZ 默认有 1 个子网。

---

**Q: What is the difference between a Security Group and a NACL?**
安全组（Security Group）和 NACL 的区别是什么？

> <font color=OrangeRed>**A: Security Group is a firewall at the instance level (stateful). NACL is a firewall at the subnet level (stateless, rules evaluated in order).**</font>

| 特性 Feature | 安全组 Security Group | NACL |
|---|---|---|
| 作用范围 Scope | 实例级 Instance level | 子网级 Subnet level |
| 有状态 Stateful | 是 Yes | 否 No |
| 规则评估 Rule evaluation | 所有规则 All rules | 按编号顺序 Ordered by rule number |
| 默认行为 Default | 允许所有出站，拒绝所有入站 / Allow all outbound, deny all inbound | 允许所有 Allow all |

---

**Q: In a NACL with rules: (1) Allow SSH, (2) Allow HTTP, (3) Deny All, (4) Allow All — what traffic is allowed?**
NACL 规则：(1) 允许 SSH，(2) 允许 HTTP，(3) 拒绝所有，(4) 允许所有 — 哪些流量被允许？

> <font color=OrangeRed>**A: Only SSH and HTTP are allowed — all other traffic is denied. NACL rules are evaluated in numbered order and stop at the first match.**</font>

NACL 按规则编号顺序逐条匹配，找到第一条匹配规则即停止。Rule 4 (Allow All) is never reached for non-SSH/HTTP traffic.

---

**Q: Which AWS services are associated with Edge Locations?**
哪些 AWS 服务使用边缘节点（Edge Locations）？

> <font color=OrangeRed>**A: Amazon CloudFront and AWS Shield**</font>

边缘节点是缓存内容的位置。CloudFront 使用边缘节点缓存内容以降低延迟；AWS Shield 在边缘节点实施 DDoS 防护。

---

**Q: How does CloudFront caching work?**
CloudFront 缓存如何工作？

> <font color=OrangeRed>**A: First request fetches from the origin (e.g. S3 bucket) and caches at the edge location. Subsequent requests are served from the edge. Objects are cached for the TTL (Time to Live). Clearing cached objects incurs a charge.**</font>

- 首次请求 → 从源站（如 S3）下载并缓存到边缘节点 / First request fetches from origin
- 后续请求 → 直接从边缘节点提供 / Subsequent requests served from edge
- 缓存时长 = TTL（生存时间）/ Cached for the duration of the TTL
- Edge locations support **both reads and writes** (you can PUT objects to them)
- **A Distribution** is the CDN name for the collection of edge locations

---

**Q: What are Route 53's 3 main functions?**
Route 53 的三大主要功能是什么？

> <font color=OrangeRed>**A: Domain Registration, DNS (Domain Name System) service, Health Checks**</font>

Route 53 是全局性服务（global service），是 AWS 的托管 DNS 服务。DNS = 计算机的电话簿，将域名解析为 IP 地址。

---

**Q: What two services in combination aid in DDoS mitigation?**
哪两个服务组合使用有助于 DDoS 缓解？

> <font color=OrangeRed>**A: CloudFront and Route 53**</font>

---

## Monitoring & Operations 监控与运营

---

**Q: What can Amazon CloudWatch monitor?**
Amazon CloudWatch 可以监控哪些内容？

> <font color=OrangeRed>**A: Compute (EC2, Auto Scaling Groups, ELB, Route 53 health checks), Storage & Content Delivery (EBS, Storage Gateways, CloudFront)**</font>

CloudWatch 默认每 5 分钟监控一次 EC2 指标。开启**详细监控（Detailed Monitoring）**可以实现 1 分钟间隔采集自定义指标。

---

**Q: What are the types of CloudWatch alarms and events?**
CloudWatch 告警和事件有哪些类型？

> <font color=OrangeRed>**A: CloudWatch Alarms (e.g. billing alarms), CloudWatch Events (proactive environment response), Lambda Scheduled Events, AWS WAF (security automations)**</font>

---

**Q: What is the AWS Personal Health Dashboard?**
AWS 个人健康仪表板是什么？

> <font color=OrangeRed>**A: Publishes alerts and remediation guidance when AWS service issues arise, and provides notifications for scheduled events affecting customers.**</font>

> **Contrast with Trusted Advisor:** Trusted Advisor provides architecture guidance (cost, security, performance, fault tolerance, service limits) but does NOT include AWS service health information.

---

**Q: What does CloudTrail do, and where are its logs stored?**
CloudTrail 有什么作用？日志存储在哪里？

> <font color=OrangeRed>**A: CloudTrail enables governance, operational auditing, compliance, and risk auditing by logging all API calls. Logs are stored in S3.**</font>

**Consolidating CloudTrail logs across multiple accounts:**
1. 在付费账户中开启 CloudTrail / Turn on CloudTrail in the paying account
2. 创建允许跨账户访问的 bucket policy / Create a bucket policy that allows cross-account access
3. 在其他账户中开启 CloudTrail 并使用付费账户的 bucket / Turn on CloudTrail in other accounts pointing to the paying account's bucket

---

**Q: What is AWS Systems Manager?**
AWS Systems Manager 是什么？

> <font color=OrangeRed>**A: Manages fleets of EC2 instances and virtual machines by installing a software agent on each. Used to view operational data from multiple AWS services through a unified UI and automate operational tasks.**</font>

> **Contrast with CloudWatch:** CloudWatch is for performance monitoring, not automating operational tasks.

---

**Q: What is AWS Organizations, and how can it help with costs?**
AWS Organizations 是什么？如何帮助控制成本？

> <font color=OrangeRed>**A: A free service for managing multiple AWS accounts. Enables consolidated billing, which pools usage across accounts to achieve volume pricing tier discounts.**</font>

AWS Organizations 可通过 API 自动化账户创建。整合账单通过跨账户汇总用量，使整个组织享受批量折扣。

---

## Billing & Pricing 计费与定价

---

**Q: What are the AWS Support Plans and their key details?**
AWS 支持计划有哪些？各有什么特点？

> <font color=OrangeRed>**A: Basic (free), Developer ($29/mo), Business ($100/mo), Enterprise ($15,000/mo)**</font>

| 支持计划 | 费用 Cost | 技术支持 Tech Support | 可开 Case 数 |
|---|---|---|---|
| Basic | 免费 Free | 无 None | 无法开 Case |
| Developer | $29/月 (按用量扩展) | 工作时间邮件 Business hrs, email | 1人/无限 Case |
| Business | $100/月 (按用量扩展) | 24×7 邮件/聊天/电话 | 无限人数/无限 Case |
| Enterprise | $15,000/月 (按用量扩展) | 24×7 + TAM (技术客户经理) | 无限人数/无限 Case |

**Business plan response times:**
- 一般指导 General: < 24 hours
- 系统受损 System impaired: < 12 hours
- 生产系统受损 Production impaired: < 4 hours
- 生产系统宕机 Production down: < 1 hour

**Enterprise 额外:** 业务关键系统宕机 Business-critical down: < **15 minutes**

> **Lowest cost plan allowing unlimited cases: Developer plan.**

---

**Q: What is the difference between AWS Cost Explorer and the AWS Simple Monthly Calculator?**
AWS Cost Explorer 和 AWS Simple Monthly Calculator 的区别是什么？

> <font color=OrangeRed>**A: Cost Explorer is a free tool for viewing historical cost charts and forecasting future spend (3-month forecast). The Simple Monthly Calculator estimates running costs per month — it is NOT a comparison tool.**</font>

- **Cost Explorer**：查看历史成本图表、管理当前支出、预测未来 3 个月账单 / View charts, manage current spend, forecast 3 months
- **Simple Monthly Calculator**：估算每月运行成本，不用于对比 / Estimate monthly running costs; not a comparison tool

---

**Q: What are the free AWS services?**
哪些 AWS 服务本身是免费的？

> <font color=OrangeRed>**A: Amazon VPC, Elastic Beanstalk, CloudFormation, IAM, Auto Scaling, Consolidated Billing, AWS Organizations**</font>

注意：服务本身免费，但这些服务所置备的资源（EC2、RDS 等）会产生费用。

---

**Q: Which AWS global services exist?**
哪些 AWS 服务是全局性的？

> <font color=OrangeRed>**A: IAM, Route 53, CloudFront, SNS, SES**</font>

EC2 和 S3 是**区域级（regional）**服务，在特定 AWS 区域中管理。

---

**Q: How can a company separate costs for storage, EC2, S3, and other AWS services by department?**
公司如何按部门区分 EC2、S3 等服务的成本？

> <font color=OrangeRed>**A: Add department-specific tags to each resource.**</font>

标签（Tags）是 AWS 成本分配的核心工具，为每个资源添加部门标签后，可在 Cost Explorer 中按标签过滤和分组成本。

---

**Q: When using Amazon RDS, which items are you charged for?**
使用 Amazon RDS 时，哪些项目会被收费？

> <font color=OrangeRed>**A: Multi-AZ replication, outbound data transfer. NOT charged: backup storage up to the size of the database.**</font>

备份存储在不超过数据库大小的范围内是免费的，超出部分才收费。

---

**Q: What is AWS Trusted Advisor?**
AWS Trusted Advisor 是什么？

> <font color=OrangeRed>**A: Provides guidance for architecting your AWS environment, including cost optimization, security, fault tolerance, performance, and service limits. Also displays current usage and limits.**</font>

Trusted Advisor 检查服务限制（Service Limits）并提示哪些接近或超过默认限制。

---

## Architecture Principles 架构原则

---

**Q: What is loose coupling, and why is it recommended?**
什么是松耦合（loose coupling）？为什么推荐它？

> <font color=OrangeRed>**A: Loose coupling means components interact through interfaces (e.g. SQS queues, APIs) rather than direct tight dependencies. This improves fault tolerance and scalability — failure in one component doesn't cascade.**</font>

松耦合通过消息队列（SQS）、API 等接口解耦组件，一个组件的故障不会级联传播到其他组件。

---

**Q: A mobile shopping app uses EC2 with Auto Scaling. The design requires any instance to process any request. What design characteristic is required?**
一个移动购物应用使用带有 Auto Scaling 的 EC2，设计要求任意实例都能处理任意请求。需要什么设计特性？

> <font color=OrangeRed>**A: Stateless design — don't store session state on specific EC2 instances. Any instance provisioned by Auto Scaling can then process any request.**</font>

无状态设计（Stateless Design）：不在特定 EC2 实例上存储会话状态，状态存储在外部（如 ElastiCache、DynamoDB），使任意实例均可处理任意请求。

> **Contrast:** Session affinity (sticky sessions) directs traffic to a specific instance each time — the opposite of stateless design.

---

**Q: What type of cloud is used by traditional on-premise methods?**
传统本地（On-Premises）方法使用哪种云类型？

> <font color=OrangeRed>**A: Private Cloud**</font>

---

**Q: What is AWS Landing Zone?**
AWS Landing Zone 是什么？

> <font color=OrangeRed>**A: A solution that helps customers quickly set up a secure, multi-account (initially 4) AWS environment based on AWS best practices.**</font>

---

**Q: What is AWS Quick Start?**
AWS Quick Start 是什么？

> <font color=OrangeRed>**A: A way of deploying environments quickly using CloudFormation templates built by AWS Solutions Architects (experts).**</font>

---

## Key Takeaways

- **云计算三大模型 Cloud models**: IaaS / PaaS / SaaS；三大部署模型：Public / Hybrid / Private.
- **全局服务 Global services**: IAM, Route 53, CloudFront, SNS, SES. EC2/S3 are regional.
- **IAM 默认零权限 IAM default**: New users have no permissions. Explicit Deny always overrides Allow.
- **共同责任 Shared Responsibility**: AWS = security OF the cloud. Customer = security IN the cloud.
- **安全服务区分 Security services**: WAF (web app firewall) / Shield (DDoS) / GuardDuty (threat detection) / Inspector (EC2 vulnerability assessment only).
- **EC2 定价模型 EC2 pricing**: On-Demand (flexible, no commit), Reserved (1–3 yr discount), Spot (interruptible, cheapest), Dedicated Host (BYOL).
- **S3 一致性 S3 consistency**: New PUT = read-after-write. Overwrite PUT/DELETE = eventual consistency.
- **RDS vs DynamoDB**: RDS = SQL/relational; DynamoDB = NoSQL. Multi-AZ for DR; Read Replicas for read scaling.
- **VPC**: 1 default VPC per region; 1 subnet per AZ. Security Group = instance-level stateful. NACL = subnet-level stateless, ordered rules.
- **CloudWatch**: 5-min default; 1-min with Detailed Monitoring. Alarms → SNS notifications.
- **CloudTrail**: Logs all API calls → stored in S3. KMS integrates with CloudTrail for key event logging.
- **支持计划 Support plans**: Enterprise has TAM + 15-min response for business-critical. Developer = lowest cost with unlimited cases.
- **松耦合 + 无状态 Loose coupling + stateless**: Core AWS architecture principles for fault-tolerant, scalable systems.
- **免费服务 Free services**: VPC, Elastic Beanstalk, CloudFormation, IAM, Auto Scaling, Consolidated Billing, AWS Organizations.

## References

- Source: Linux Academy / A Cloud Guru AWS Cloud Practitioner practice questions
- `_posts/01Cloud/01AWS/IAM/2020-07-18-IAM.md`
- `_posts/01Cloud/01AWS/Networking/2020-07-18-VPC.md`
- `_posts/01Cloud/01AWS/2020-07-18-EC2.md`
- `_posts/01Cloud/01AWS/Storage/2020-07-18-S3.md`
