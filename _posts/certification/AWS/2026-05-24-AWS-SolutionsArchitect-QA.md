---
title: "Meow's AWS - Solutions Architect Associate Exam Q&A"
date: 2026-05-24 11:11:11 -0400
categories: [certification, AWS]
tags: [AWS, IAM, EC2, S3, EFS, FSx, RDS, Aurora, DynamoDB, VPC, Route53, WAF, KMS, SQS, CloudFront, ExamPrep, SolutionsArchitect]
math: false
toc: true
---

# AWS Solutions Architect Associate Exam Q&A

AWS Solutions Architect Associate 考试练习题，涵盖计算、存储、数据库、网络、安全、应用服务、迁移与成本优化等核心领域。

Practice questions for the AWS Solutions Architect Associate exam, covering compute, storage, database, networking, security, application services, migration, and cost optimization.

---

## Compute & Auto Scaling 计算与弹性伸缩

---

**Q: A nightly batch job starts at 1 AM and takes 1 hour to scale up before reaching desired capacity. Peak capacity is consistent every night. What is the most cost-effective solution?**
夜间批处理作业每晚 1 AM 开始，自动扩展需 1 小时才能达到目标容量，峰值容量每晚固定。最具成本效益的解决方案是什么？

> <font color=OrangeRed>**A: Configure scheduled scaling to scale up to the desired compute level before 1 AM.**</font>

定时扩展（Scheduled Scaling）可以在已知峰值时间之前预先扩容，避免响应式扩展的等待延迟，同时在批处理完成后自动缩容。

Scheduled Scaling pre-provisions the required capacity before the known peak time, eliminating the 1-hour scale-up lag. The Auto Scaling group scales down automatically after the batch completes.

---

**Q: An application requires low network latency and high network throughput between EC2 instances. Which component should be included?**
应用需要 EC2 实例之间低网络延迟和高吞吐量，应该使用什么组件？

> <font color=OrangeRed>**A: A placement group using a cluster placement strategy.**</font>

集群置放组（Cluster Placement Group）将实例放在同一可用区的高带宽底层网络上，可实现实例间的低延迟和高吞吐量，适合 HPC 和大数据等场景。

Cluster Placement Groups pack instances onto the same high-bandwidth underlying network within a single AZ, delivering low inter-instance latency and high throughput. Best for HPC, big data, and tightly coupled applications.

---

**Q: A clustered application must be placed across multiple AZs with high-speed, low-latency communication and minimized risk of underlying hardware failure. Which placement strategy should be used?**
一个集群应用需要跨多个 AZ 部署，要求低延迟通信，同时最小化底层硬件故障风险，应使用哪种置放策略？

> <font color=OrangeRed>**A: Spread Placement Group.**</font>

分散置放组（Spread Placement Group）将实例分布在不同的底层硬件上，降低同时故障风险，支持跨 AZ 部署，适合少量关键实例需要彼此隔离的场景。

Spread Placement Groups distribute instances across distinct underlying hardware to reduce the risk of simultaneous failures. They support cross-AZ deployment and are suited for a small number of critical instances that must be kept separate.

---

**Q: A monolithic application cannot use Auto Scaling. What provides automatic recovery of the EC2 instance if underlying hardware fails?**
单体应用无法使用 Auto Scaling，底层硬件故障时如何实现 EC2 实例的自动恢复？

> <font color=OrangeRed>**A: Configure a CloudWatch alarm that triggers the recovery of the EC2 instance if it becomes impaired.**</font>

CloudWatch 的 `StatusCheckFailed_System` 指标可以触发 EC2 实例恢复操作（`recover`），将实例迁移到新硬件，同时保留实例 ID、IP 地址和 EBS 卷。

The CloudWatch `StatusCheckFailed_System` metric can trigger the `recover` action, migrating the instance to new hardware while preserving instance ID, IP addresses, and EBS volumes.

---

**Q: Many Auto Scaling Groups use similar launch configurations with subtle differences. An ideal approach would have a default version with additional feature versions. What meets this requirement?**
多个 Auto Scaling Group 使用相似的启动配置，希望有一个默认版本加额外版本。什么满足这个需求？

> <font color=OrangeRed>**A: Use launch templates instead of launch configurations.**</font>

启动模板（Launch Templates）支持版本控制，可以创建默认版本并派生多个版本，而启动配置（Launch Configurations）是不可变的，每次变更必须创建全新配置。

Launch Templates support versioning — create a default version and derive additional versions. Launch Configurations are immutable; any change requires creating an entirely new configuration.

---

**Q: Global users access an application in different AWS Regions exposing public static IP addresses and experiencing poor performance. How to reduce internet latency?**
全球用户访问部署在不同 AWS Region 的应用，应用暴露公共静态 IP，用户体验延迟高。如何降低延迟？

> <font color=OrangeRed>**A: Set up AWS Global Accelerator and add the regional endpoints.**</font>

Global Accelerator 利用 AWS 全球骨干网络路由流量，为应用提供两个静态 anycast IP，将用户就近路由到最优 Region，减少公网跳数。适合需要静态 IP 的非 HTTP/HTTPS 场景。与 CloudFront 的区别：CloudFront 适合 HTTP 内容缓存；Global Accelerator 适合 TCP/UDP 应用的静态 IP 路由。

Global Accelerator routes traffic over the AWS global backbone, providing two static anycast IPs and routing users to the nearest healthy endpoint. Unlike CloudFront, which caches HTTP content, Global Accelerator is suited for TCP/UDP applications that require static IPs.

---

**Q: A company has an EC2 instance that is extremely sensitive to network jitter and latency variations. What removes the risk of network performance degradation?**
EC2 实例对网络抖动和延迟波动极度敏感，如何消除网络性能下降的风险？

> <font color=OrangeRed>**A: Ensure the instance has enhanced networking.**</font>

增强型网络（Enhanced Networking）通过 SR-IOV 绕过 CPU 对网络接口虚拟化的参与，提高每秒包数（PPS）并降低网络延迟波动，适合对网络一致性要求高的应用。

Enhanced Networking uses SR-IOV to bypass CPU involvement in virtualizing the network interface, increasing packets per second and reducing variability in network performance — eliminating jitter for latency-sensitive applications.

---

## Storage 存储

---

**Q: Multiple EC2 Linux instances need to rapidly and concurrently read and write to shared storage with a hierarchical directory structure. How to achieve this?**
多个 EC2 Linux 实例需要对具有层级目录结构的共享存储进行并发读写。如何实现？

> <font color=OrangeRed>**A: Create an EFS file system and mount it from each EC2 instance.**</font>

Amazon EFS 是完全托管的 NFS 文件系统，支持多个 EC2 Linux 实例同时挂载，提供 POSIX 权限模型和标准的层级目录结构，弹性自动扩展。EBS 卷无法被多个实例共享；S3 不可挂载；instance store 是临时存储。

Amazon EFS is a fully managed NFS file system that supports simultaneous mounting by multiple EC2 Linux instances with POSIX permissions and standard hierarchical directory structure. EBS cannot be shared across instances; S3 is not mountable; instance store is ephemeral.

---

**Q: An application needs shared storage accessible from multiple Linux EC2 instances, supports POSIX permissions, and can be used by multiple instances simultaneously. Which product should be suggested?**
应用需要可被多个 Linux EC2 实例同时挂载、支持 POSIX 权限的共享存储，应使用哪个产品？

> <font color=OrangeRed>**A: EFS**</font>

> **注意：** S3 可存储无限数量的对象，但无法挂载为文件系统，不支持 POSIX 权限。
> **Note:** S3 stores virtually unlimited objects but cannot be mounted and does not support POSIX permissions.

---

**Q: A persistent database migration requires 64,000 IOPS on a single EBS volume. Which solution meets this?**
一个数据库迁移需要单个 EBS 卷提供 64,000 IOPS，应使用什么方案？

> <font color=OrangeRed>**A: Create a Nitro-based EC2 instance with an EBS Provisioned IOPS SSD (io1) volume configured for 64,000 IOPS.**</font>

io1/io2 卷在基于 Nitro 的 EC2 实例上可支持最高 64,000 IOPS，满足要求。非 Nitro 实例上 io1 最大 32,000 IOPS。I3 实例的本地存储是临时的（ephemeral），不适合持久化数据库。

io1/io2 volumes on Nitro-based EC2 instances support up to 64,000 IOPS per volume. Non-Nitro instances cap at 32,000. I3 instance store is ephemeral — not suitable for a persistent database.

---

**Q: A media company needs 10 TB with maximum I/O for video processing, 300 TB durable storage for media, and 900 TB for archival. Which set of services should be recommended?**
媒体公司需要 10 TB 高 IOPS 视频处理存储、300 TB 耐久媒体存储、900 TB 归档存储，应推荐哪组服务？

> <font color=OrangeRed>**A: EBS for maximum performance, S3 for durable data storage, and S3 Glacier for archival storage.**</font>

- **EBS Provisioned IOPS (io1/io2)**：10 TB 高 IOPS，适合视频处理
- **S3 Standard**：300 TB 耐久对象存储，11 个 9 的持久性
- **S3 Glacier**：900 TB 低成本长期归档

EC2 instance store 性能最高但是临时存储，不适合作为需要持久化的视频处理存储。

---

**Q: A company delivers files in S3 to users without AWS credentials for a limited time. What is the recommended approach?**
向无 AWS 凭证的用户提供 S3 文件的有限时间访问，应如何实现？

> <font color=OrangeRed>**A: Generate a presigned URL to share with the users.**</font>

预签名 URL（Presigned URL）由拥有 S3 对象权限的 IAM 主体生成，携带时间戳和签名，在有效期内任何人（无需 AWS 凭证）可访问该对象，到期自动失效。

A presigned URL is generated by an IAM principal with S3 permissions. It embeds a timestamp and signature, granting time-limited access to anyone holding the URL — no AWS credentials required. Access expires automatically.

---

**Q: Premium content in S3 must be accessible for 14 days after payment, then access is denied. What is the least complicated implementation?**
S3 中的付费内容需在付款后 14 天内可下载，之后拒绝访问。最简单的实现方案是什么？

> <font color=OrangeRed>**A: Use a CloudFront distribution with an OAI. Configure the distribution with an S3 origin. Design the application to set an expiration of 14 days for the signed URL.**</font>

CloudFront 签名 URL 内置过期时间字段，将过期设为 14 天后即可实现自动失效，无需额外 Lambda 清理任务。OAI（Origin Access Identity）确保 S3 内容只能通过 CloudFront 访问，不对公网暴露。

CloudFront signed URLs have a built-in expiration field. Setting it to 14 days provides automatic access expiry — no Lambda cleanup function required. The OAI ensures S3 content is only reachable through CloudFront.

---

**Q: S3 hosted website serves petabytes of outbound traffic monthly. How to reduce costs?**
S3 托管网站每月产生 PB 级出站流量，如何降低成本？

> <font color=OrangeRed>**A: Configure CloudFront with the existing S3 website as the origin.**</font>

将 CloudFront 置于 S3 前面可大幅降低 S3 出站数据传输费用（因为 CloudFront → S3 回源流量免费），同时提高全球用户访问速度。

Placing CloudFront in front of S3 dramatically reduces S3 data transfer-out charges — CloudFront-to-S3 origin requests are free — while also improving latency for global users via edge caching.

---

**Q: A company uses a two-tier ecommerce website in the US but now serves European and Australian users who experience slow browsing. What is the most cost-effective solution?**
美国的两层电商网站开始服务欧洲和澳大利亚用户，国际用户访问缓慢，最具成本效益的方案是什么？

> <font color=OrangeRed>**A: Use CloudFront and S3 to host static images.**</font>

使用 CloudFront 缓存静态内容（图片、CSS、JS）并配合 S3 存储，可以通过边缘节点向国际用户就近提供内容，而无需在多个 Region 重新部署整个架构。

Caching static content (images, CSS, JS) at CloudFront edge locations near international users provides significant latency improvement at low incremental cost, without the expense of redeploying the full stack across multiple Regions.

---

**Q: Two applications access the same files concurrently with low latency requirements. Which architecture should be recommended?**
两个应用同时访问相同文件，要求低延迟。应推荐什么架构？

> <font color=OrangeRed>**A: Configure two EC2 instances to run both applications. Configure Amazon EFS with General Purpose performance mode and Bursting Throughput mode to store the data.**</font>

EFS 通用性能模式（General Purpose）适合延迟敏感的场景（Web 服务、CMS、文件共享）；突增吞吐量模式（Bursting Throughput）根据存储量积累积分，支持突发高吞吐。两个 EC2 实例可同时挂载 EFS，实现并发低延迟访问。

EFS General Purpose mode is ideal for latency-sensitive use cases. Bursting Throughput scales with storage size. Two EC2 instances can mount EFS simultaneously for concurrent low-latency file access.

---

**Q: Data is analyzed daily for one week, then must remain immediately accessible for occasional analysis. What is the most cost-effective lifecycle policy?**
数据每日分析一周后，需要保持随时可访问（偶尔分析）。最具成本效益的生命周期策略是什么？

> <font color=OrangeRed>**A: Configure a lifecycle policy to transition objects to S3 One Zone-Infrequent Access (S3 One Zone-IA) after 30 days.**</font>

题目中未提及高可用要求，One Zone-IA 比 Standard-IA 成本更低，且仍提供即时访问。Glacier 不满足"随时可访问"的要求。

The question does not mention high-availability requirements, so One Zone-IA is cheaper than Standard-IA while still providing immediate retrieval. Glacier fails the "must remain immediately accessible" requirement.

---

**Q: An on-premises data center running out of storage needs to migrate to AWS while minimizing bandwidth costs. Solution must allow immediate retrieval at no additional cost. How to meet these requirements?**
本地数据中心存储不足，需迁移到 AWS，同时最小化带宽成本，且必须支持立即检索（无额外费用）。如何满足这些需求？

> <font color=OrangeRed>**A: Deploy AWS Storage Gateway using cached volumes. Use Storage Gateway to store data in S3 while retaining copies of frequently accessed data subsets locally.**</font>

缓存卷模式（Cached Volumes）将主数据存储在 S3，仅在本地缓存最近访问的数据子集，最小化本地存储需求和带宽消耗，同时提供低延迟的即时访问。Glacier Vault 有额外的快速检索费用，不满足"无额外成本"要求。

Cached Volumes store primary data in S3 while caching recently accessed subsets locally, minimizing bandwidth and on-premises storage while providing immediate local-cache retrieval. Glacier expedited retrieval incurs extra cost — disqualifying it.

---

**Q: A company wants to host on-premises NAS files using the NFS protocol on AWS while also making the data accessible for analytics in the AWS Cloud. Which solution meets these requirements?**
公司需要使用 NFS 协议在 AWS 托管本地 NAS 文件，同时使数据可用于云端分析，应使用什么方案？

> <font color=OrangeRed>**A: Use an AWS Storage Gateway file gateway to provide file storage to AWS, then perform analytics on this data in the AWS Cloud.**</font>

文件网关（File Gateway）使用 NFS 或 SMB 协议将本地应用与 S3 集成，文件在 S3 中以原生对象存储，可供 AWS 分析服务（如 Athena、EMR）直接访问。

The File Gateway presents an NFS/SMB interface to on-premises applications while storing files natively in S3, making them immediately accessible to AWS analytics services such as Athena, EMR, and Glue.

---

**Q: A company needs to replace physical backup tapes while preserving the existing backup application investment and workflows. What should be recommended?**
公司需要取消物理备份磁带，但必须保留现有备份应用和工作流，应推荐什么方案？

> <font color=OrangeRed>**A: Set up AWS Storage Gateway to connect with the backup applications using the iSCSI-virtual tape library (VTL) interface.**</font>

磁带网关（Tape Gateway/VTL）通过 iSCSI 向现有备份软件呈现虚拟磁带库接口，与现有备份应用无缝集成，无需更改工作流，将备份数据存储到 S3 和 Glacier。

Tape Gateway presents a VTL interface over iSCSI to existing backup applications, requiring no workflow changes. Backup data is stored in S3 and can be lifecycle-managed to Glacier for long-term retention.

---

**Q: S3 storage: An on-premises Windows document management app stores many files on a network file share. To reduce the on-premises footprint and minimize storage costs. What should be done?**
本地 Windows 文档管理应用使用网络文件共享存储大量文件，需减少本地占用并最小化存储成本，应如何处理？

> <font color=OrangeRed>**A: Set up an AWS Storage Gateway file gateway.**</font>

文件网关支持 SMB 和 NFS，将本地文件存储卸载到 S3，仅在本地缓存常用文件，减少本地存储需求，同时保持低延迟访问体验。

File Gateway supports SMB and NFS, offloading file storage to S3 while caching frequently accessed files locally. This reduces on-premises storage footprint while maintaining low-latency access.

---

**Q: A company wants to retain old backup solution in AWS during migration. Which solution allows retaining existing backups and archives?**
公司在迁移期间希望在 AWS 保留旧备份方案，不丢失现有备份和归档，应使用什么方案？

> <font color=OrangeRed>**A: AWS Storage Gateway VTL solution.**</font>

Storage Gateway VTL 可在本地环境安装并与现有企业备份产品集成，在迁移过渡期间不丢失对现有备份和归档的访问。旧磁带可恢复到 Storage Gateway 卷或迁移为 Tape Gateway 中的虚拟磁带。

The Storage Gateway VTL can be deployed on-premises alongside the existing enterprise backup product. During migration, old tapes can be restored to the Storage Gateway volume or migrated to virtual tapes inside AWS using Tape Gateway — without losing access to existing backups.

---

**Q: An app moving static content from EC2 to S3 + CloudFront must restrict access to a limited set of IP ranges. Which two steps should be taken?**
应用将静态内容从 EC2 迁移到 S3 + CloudFront，需要限制访问特定 IP 范围，应采取哪两个步骤？

> <font color=OrangeRed>**A: (1) Create an Origin Access Identity (OAI) and associate it with the distribution; change the bucket policy so only the OAI can read objects. (2) Create an AWS WAF web ACL with the same IP restrictions as the EC2 security group; associate the web ACL with the CloudFront distribution.**</font>

OAI 确保 S3 内容只能通过 CloudFront 访问。WAF IP 匹配条件在 CloudFront 层过滤 IP，二者组合实现内容保护和 IP 限制。安全组无法附加到 CloudFront 分发。

OAI locks S3 access to CloudFront only. A WAF IP match rule on the CloudFront distribution enforces the IP allowlist. Security groups cannot be attached to CloudFront distributions.

---

**Q: EBS capabilities — which operations are supported?**
EBS 支持哪些操作？

> <font color=OrangeRed>**A: (1) Create an encrypted snapshot from an unencrypted snapshot by creating an encrypted copy. (2) Create an encrypted volume from a snapshot of another encrypted volume.**</font>

EBS 限制：
- **不能**从加密快照创建未加密卷
- **不能**加密现有未加密卷（需创建快照 → 加密副本 → 从加密快照创建新卷）

EBS limitations: cannot create an unencrypted volume from an encrypted snapshot; cannot encrypt an existing volume in place. Workaround: snapshot → encrypted copy → new volume from the encrypted snapshot.

---

**Q: Use multipart upload for S3 — what are the benefits?**
何时使用 S3 多段上传（Multipart Upload）？有哪些好处？

> <font color=OrangeRed>**A: (1) Quick recovery from network issues. (2) Improved throughput. (3) Begin an upload before knowing the final object size. (4) Pause and resume object uploads.**</font>

多段上传将大文件分片并行上传，单个分片失败只需重传该分片，整体提升上传可靠性和速度，并支持流式上传。

Multipart upload splits large objects into parts for parallel upload. A failed part only needs to be retransmitted. Benefits include better throughput, resilience to network failures, streaming uploads before the final size is known, and the ability to pause and resume.

---

**Q: A company's S3 gateway endpoint must allow traffic to trusted buckets only. Which method should be implemented?**
S3 网关端点必须只允许流量访问可信 S3 桶，应使用什么方法？

> <font color=OrangeRed>**A: Create an S3 endpoint policy for each S3 gateway endpoint that provides access to the Amazon Resource Name (ARN) of the trusted S3 buckets.**</font>

端点策略（Endpoint Policy）附加在 VPC 端点上，通过指定受信任 S3 桶的 ARN 限制只有这些桶可通过该端点访问，而不影响其他 VPC 中的访问路径。桶策略限制来源 VPC，但无法通过单一策略控制所有端点流量。

An endpoint policy attached to the VPC endpoint restricts which S3 buckets are accessible through it. Specifying trusted bucket ARNs in the endpoint policy is the correct control — bucket policies restrict source VPCs but cannot centrally control all endpoint traffic.

---

**Q: An application on EC2 instances in a private subnet needs access to an S3 bucket. Traffic cannot traverse the internet. How to configure access?**
私有子网中的 EC2 实例需要访问 S3，流量不能经过公网，如何配置访问？

> <font color=OrangeRed>**A: Configure a VPC gateway endpoint for S3 in the VPC.**</font>

S3 和 DynamoDB 支持 VPC 网关端点（Gateway Endpoint），流量通过 AWS 内部网络路由，不经过公网。网关端点免费，且无需 NAT 网关。PrivateLink（接口端点）适用于其他 AWS 服务和第三方服务。

S3 and DynamoDB support VPC Gateway Endpoints, routing traffic over the AWS internal network without traversing the internet. Gateway endpoints are free and require no NAT gateway. PrivateLink (interface endpoints) covers other AWS services and third-party services.

---

**Q: An application in a VPC requires access to a sensitive S3 bucket protected from internet access. Services within the VPC need access. Which two actions should be taken?**
VPC 内应用需要访问受保护的 S3 桶，桶不能对互联网开放，应采取哪两个步骤？

> <font color=OrangeRed>**A: (1) Create a VPC endpoint for S3. (2) Apply a bucket policy to restrict access to the S3 endpoint.**</font>

VPC 端点为流量提供私有路径；桶策略通过 `aws:sourceVpce` 或 `aws:sourceVpc` 条件将访问限定在 VPC 端点，防止来自互联网的访问。

A VPC endpoint provides the private traffic path; the bucket policy with `aws:sourceVpce` or `aws:sourceVpc` conditions restricts access to that endpoint, preventing any internet-originated requests.

---

**Q: A Windows application requires a shared Windows file system attached to multiple Windows EC2 instances. What should be done?**
Windows 应用需要连接到多个 Windows EC2 实例的共享 Windows 文件系统，应如何实现？

> <font color=OrangeRed>**A: Configure Amazon FSx for Windows File Server. Mount the FSx volume to each Windows instance.**</font>

FSx for Windows 是完全托管的 Windows 原生文件系统，支持 SMB 协议、Windows 权限（NTFS ACL）和 Active Directory 集成，可挂载到多个 Windows EC2 实例。EFS 不支持 Windows SMB 协议，EBS 无法多实例共享。

FSx for Windows is a fully managed Windows-native file system with SMB, NTFS ACLs, and Active Directory integration, mountable across multiple Windows EC2 instances. EFS does not support Windows SMB; EBS cannot be shared across instances.

---

**Q: A company needs to deploy a shared file system for .NET and SQL Server on Windows Server 2016, integrated into corporate Active Directory with high durability. What meets these requirements?**
公司需要为 .NET 和 SQL Server（Windows Server 2016）部署共享文件系统，需与企业 AD 集成、高持久性，应使用什么？

> <font color=OrangeRed>**A: Use Amazon FSx for Windows File Server.**</font>

FSx for Windows 可集成本地 Active Directory，支持 .NET 应用的 SMB 访问，提供多 AZ 高持久性配置，AWS 托管减少运维负担。

FSx for Windows integrates with on-premises Active Directory, provides SMB access for .NET applications, offers Multi-AZ high durability, and is fully managed by AWS.

---

**Q: A Windows IIS web application must migrate from on-premises NAS file share. What is the most resilient and durable replacement?**
Windows IIS Web 应用需从本地 NAS 文件共享迁移，最具弹性和持久性的替代方案是什么？

> <font color=OrangeRed>**A: Migrate the file share to Amazon FSx for Windows File Server.**</font>

---

**Q: A company needs to migrate a Windows file server to AWS for use by WorkSpaces. What is the most cost-effective and resilient way using SMB protocol?**
公司需要将 Windows 文件服务器迁移到 AWS 供 WorkSpaces 使用，使用 SMB 协议最具成本效益且最具弹性的方案是什么？

> <font color=OrangeRed>**A: Amazon FSx for Windows File Server.**</font>

FSx for Windows 原生支持 SMB 协议，与 WorkSpaces（虚拟桌面）无缝集成，提供高可用性和托管服务，减少运维开销。

**SMB 协议总结 SMB Protocol Summary:**
- For SMB protocol: always use <font color=OrangeRed>Amazon FSx for Windows File Server</font>
- For NFS protocol (Linux): use <font color=OrangeRed>Amazon EFS</font>
- EFS does not support Windows SMB; EBS is single-instance only

---

**Q: A company wants to run a hybrid workload for data processing. On-premises apps access data via the SMB protocol. Which two services meet the business requirements?**
公司需要混合工作负载，本地应用通过 SMB 协议访问数据，哪两个服务满足需求？

> <font color=OrangeRed>**A: (1) Amazon FSx for Windows. (2) AWS Storage Gateway file gateway (supports both NFS and SMB).**</font>

---

**Q: CloudTrail logs must be accessed by an internal auditor from a central account while developer accounts cannot access them. What is the most secure and optimized solution?**
内部审计员需从中央账户访问 CloudTrail 日志，而开发账户用户不能访问，最安全和优化的方案是什么？

> <font color=OrangeRed>**A: Configure CloudTrail from each developer account to deliver logs to an S3 bucket in the central account. Create an IAM role in the central account for the auditor. Attach an IAM policy providing read-only permissions to the bucket.**</font>

CloudTrail 支持将日志直接传递到其他账户的 S3 桶。在中央账户创建 IAM 角色（而非 IAM 用户）符合最小权限原则，只读权限防止审计员修改日志，IAM 角色支持跨账户访问而无需共享凭证。

CloudTrail can deliver logs directly to an S3 bucket in another account. An IAM role (not IAM user) in the central account follows least privilege, and read-only permissions prevent log tampering. IAM roles allow cross-account access without sharing credentials.

---

**Q: A 7-year backup solution needs to replace physical tapes. Daily volume is 50 TB, backups are rarely accessed, a week's notice before restoration. What is the most cost-effective solution?**
7 年备份替换物理磁带，每日 50 TB，备份几乎不被访问，恢复前通常有一周通知，最具成本效益的方案是什么？

> <font color=OrangeRed>**A: Use Amazon Storage Gateway to back up to S3 and create a lifecycle policy to move the backup to S3 Glacier.**</font>

Storage Gateway VTL 与现有备份应用无缝集成，数据先写入 S3，再通过生命周期策略转移到 Glacier。一周的恢复通知时间与 Glacier 标准检索（3-5 小时）或批量检索（5-12 小时）完全兼容，Deep Archive 的 12-48 小时检索也在一周内完成，但 Glacier 更为标准。

Storage Gateway VTL integrates with existing backup applications. Data lands in S3, then lifecycle policy moves it to Glacier. A week's restoration notice is fully compatible with Glacier standard retrieval (3–5 hours).

---

## Database 数据库

---

**Q: Aurora instances are handling both read and write traffic. The database is hitting performance bottlenecks from read traffic. What should be recommended?**
Aurora 实例同时处理读写流量，数据库因读流量遇到性能瓶颈，应推荐什么？

> <font color=OrangeRed>**A: Create Aurora read replicas to separate read and write traffic.**</font>

Aurora 最多支持 15 个只读副本，读副本与主实例共享相同的底层存储集群，可承载只读查询，释放主实例资源处理写入，延迟通常不超过 100 毫秒。

> **重要区别：** Multi-AZ 备用实例（Standby）是 HA 用途，<font color=OrangeRed>不接受读流量</font>；只读副本（Read Replica）接受读流量但不提供自动故障转移。
>
> **Critical distinction:** Multi-AZ standby instances are for HA only — <font color=OrangeRed>they do not accept read traffic</font>. Read Replicas serve reads but require manual promotion.

---

**Q: A reporting tool queries the production RDS database and is causing performance issues. The reporting tool needs its own database that stays current with the production database. What should be created?**
报告工具查询生产 RDS 数据库导致性能问题，报告工具需要始终与生产数据库保持同步的独立数据库，应创建什么？

> <font color=OrangeRed>**A: A Multi-AZ RDS Read Replica for the reporting tool.**</font>

读副本与主实例保持持续复制，报告工具可查询读副本而不影响生产工作负载。Multi-AZ 读副本在主实例故障时还可晋升为主实例。

A Read Replica maintains continuous replication from the primary. The reporting tool queries the replica without impacting production. A Multi-AZ Read Replica can also serve as a DR target.

---

**Q: A mobile app experiences slowdown when reading data. EC2 instances do not cross CPU thresholds. How can this issue be addressed?**
移动应用在读取数据时出现卡顿，EC2 实例 CPU 未超阈值，如何解决这个问题？

> <font color=OrangeRed>**A: Add read replicas for the RDS instances and direct read traffic to the replica.**</font>

EC2 CPU 未饱和说明瓶颈在数据库层，RDS 实例正在处理大量读请求。增加读副本并将读流量路由到副本可卸载 RDS 主实例压力。

EC2 CPU staying within thresholds indicates the bottleneck is at the database layer. Adding read replicas and directing read traffic there offloads the primary RDS instance.

---

**Q: A web application's RDS-based performance is degrading due to increased read-only SQL queries from business analysts. How to solve this with minimal changes to the existing web application?**
RDS 应用因业务分析师的大量只读 SQL 查询导致性能下降，如何以最少的代码改动解决？

> <font color=OrangeRed>**A: Create a read replica of the primary database and have the business analysts run their queries on it.**</font>

---

**Q: An application requires collecting, processing, and storing users' service usage data with analytics using standard SQL queries. The solution must be highly available and ensure ACID compliance. What should be recommended?**
应用需要收集、处理和存储用户服务使用数据，分析工具使用标准 SQL，需要高可用性和 ACID 合规。应推荐什么？

> <font color=OrangeRed>**A: Use a fully managed RDS for MySQL database in a Multi-AZ design.**</font>

ACID 合规 + 标准 SQL + 高可用 → RDS Multi-AZ。DynamoDB 支持 ACID 事务但不是关系型数据库，不支持标准 SQL。Neptune 是图数据库。Redshift 是数据仓库，非 OLTP。

ACID compliance + standard SQL + HA → RDS Multi-AZ. DynamoDB supports ACID transactions but is not relational and doesn't support standard SQL. Neptune is a graph DB. Redshift is a data warehouse, not OLTP.

---

**Q: A mission-critical web application needs a highly available and fault-tolerant relational database. Which two implementations meet these requirements?**
关键业务 Web 应用需要高可用且容错的关系型数据库，哪两种实现满足要求？

> <font color=OrangeRed>**A: (1) MySQL-compatible Amazon Aurora Multi-AZ. (2) Amazon RDS for SQL Server Standard Edition Multi-AZ.**</font>

关系型数据库 + 高可用 + 容错 → Multi-AZ 部署。Aurora Multi-AZ 是原生高可用设计；RDS Multi-AZ 提供自动故障转移。DynamoDB 不是关系型数据库；Redshift 是数据仓库。

Relational + HA + fault-tolerant → Multi-AZ. Aurora Multi-AZ is natively HA; RDS Multi-AZ provides automatic failover. DynamoDB is not relational; Redshift is a data warehouse.

---

**Q: A company needs a relational database with a multi-Region RPO of 1 second and an RTO of 1 minute. Which AWS solution can achieve this?**
公司需要关系型数据库，多 Region RPO 1 秒、RTO 1 分钟，哪个 AWS 方案可以实现？

> <font color=OrangeRed>**A: Amazon Aurora Global Database.**</font>

Aurora Global Database 通过专用基础设施进行跨 Region 复制，RPO 通常小于 1 秒，故障转移（RTO）通常小于 1 分钟。RDS Multi-AZ 仅限单 Region；RDS 跨区域快照恢复 RTO 远超 1 分钟。

Aurora Global Database uses dedicated replication infrastructure across Regions, achieving RPO typically under 1 second and RTO typically under 1 minute. RDS Multi-AZ is single-Region; cross-Region snapshot restore takes far longer than 1 minute.

---

**Q: An Oracle RDS Multi-AZ database in us-east-1 needs disaster recovery in us-west-2 within 2 hours with no more than 3 hours of data loss. How can these requirements be met?**
Oracle RDS Multi-AZ（us-east-1）需要在 us-west-2 建立 DR，要求 2 小时内上线，数据丢失不超过 3 小时，如何实现？

> <font color=OrangeRed>**A: Edit the DB instance and create a read replica in us-west-2. Promote the read replica to master in us-west-2 if disaster recovery needs to be activated.**</font>

跨区域 RDS 读副本持续同步，通常数据延迟在分钟级（远小于 3 小时 RPO）。激活 DR 时将读副本晋升为主实例，配合 CloudFormation 自动化可在 2 小时 RTO 内完成。

A cross-region RDS read replica maintains continuous replication (typically minutes of lag, well within the 3-hour RPO). Promoting the read replica to master, combined with CloudFormation automation, meets the 2-hour RTO.

---

**Q: A DynamoDB table has pre-configured read and write capacity. Users report slowdowns; analysis reveals the table is throttling during peak traffic. Which step improves performance?**
DynamoDB 表有预配置的读写容量，用户反映延迟，分析发现高峰期间出现限流，应如何改善性能？

> <font color=OrangeRed>**A: Make sure DynamoDB Auto Scaling is turned on.**</font>

DynamoDB Auto Scaling 根据流量自动调整预配置的读写容量，防止限流（ThrottlingException），无需手动干预。ElastiCache 适用于 RDS，不是 DynamoDB 的首选缓存（DAX 才是）。

DynamoDB Auto Scaling automatically adjusts provisioned capacity in response to traffic, preventing ThrottlingExceptions without manual intervention. ElastiCache is for RDS; DAX is the correct in-memory cache for DynamoDB.

---

**Q: A mobile chat application uses DynamoDB. Users want new messages read with minimal latency. Which method requires minimal application changes?**
移动聊天应用使用 DynamoDB，用户希望新消息以最低延迟读取，哪种方法需要最少的代码改动？

> <font color=OrangeRed>**A: Configure Amazon DynamoDB Accelerator (DAX) for the new messages table. Update the code to use the DAX endpoint.**</font>

DAX（DynamoDB Accelerator）是 DynamoDB 专用的内存缓存，将读延迟从毫秒级降至微秒级，API 兼容 DynamoDB，代码变更最小。

> **缓存对应关系 Caching mapping:**
> - <font color=OrangeRed>DAX → DynamoDB</font>
> - <font color=OrangeRed>ElastiCache → RDS/relational databases</font>

DAX is a DynamoDB-specific in-memory cache that reduces read latency from milliseconds to microseconds. Its API is DynamoDB-compatible, minimizing code changes.

---

**Q: A company has a read-heavy travel website with latency issues at certain times of the year. What alleviates the latency issues?**
旅游网站读取流量非常大，在特定时间会出现延迟问题，如何缓解延迟？

> <font color=OrangeRed>**A: Add read replicas.**</font>

Read replicas are perfectly suited for read-heavy workloads. CloudFront can accelerate static content delivery but does not directly address database read latency.

---

**Q: A DynamoDB table allocated 5,000 WCU is achieving only half the expected write throughput with three candidates as partition key values. What is the reason?**
DynamoDB 表分配了 5,000 WCU，但只达到预期写吞吐量的一半，分区键只有三个候选值，原因是什么？

> <font color=OrangeRed>**A: The partition key structure is the issue — the small range of possible PK values causes hot partitions.**</font>

- 每个 PK 值存储在单个分区中
- 每个分区最多支持 1,000 WCU
- 只有三个候选值 → 最多 3 个分区 → 最多 3,000 WCU 实际可用（远小于分配的 5,000）
- 应使用高基数（High Cardinality）分区键以充分利用分配的容量

Each distinct PK value is stored on one partition; each partition supports a maximum of 1,000 WCU. Three candidate values → at most 3 partitions → at most 3,000 WCU effective throughput, far below the allocated 5,000. Use a high-cardinality partition key to distribute load across partitions.

---

**Q: Which service reduces DynamoDB response times by an order of magnitude (milliseconds to microseconds)?**
哪个服务将 DynamoDB 响应时间从毫秒级降至微秒级？

> <font color=OrangeRed>**A: DAX (DynamoDB Accelerator).**</font>

> ElastiCache 可以执行内存缓存，但不适用于 DynamoDB。ElastiCache 对应 RDS，DAX 对应 DynamoDB。
> ElastiCache performs in-memory caching but is not for DynamoDB. ElastiCache is to RDS as DAX is to DynamoDB.

---

**Q: Which description best describes Amazon Redshift?**
哪个描述最准确地描述了 Amazon Redshift？

> <font color=OrangeRed>**A: Amazon Redshift is a fully managed, petabyte-scale data warehouse service optimized for OLAP (Online Analytical Processing) workloads.**</font>

Redshift 基于 PostgreSQL，列式存储，适合复杂分析查询和大数据集聚合，不是用于事务性工作负载（OLTP）。

> **注意 Note:** Redshift does <font color=OrangeRed>NOT</font> withstand AZ outages within a single database cluster — it is not Multi-AZ HA by design.

---

## Networking & VPC 网络与 VPC

---

**Q: An EC2 instance in a private subnet needs access to a public website to download patches. The company does not want external websites to see the EC2 IP address or initiate connections. How to achieve this?**
私有子网中的 EC2 实例需要访问公共网站下载补丁，但不希望外部网站看到实例 IP 或主动发起连接，如何实现？

> <font color=OrangeRed>**A: Create a NAT gateway in a public subnet. Route outbound traffic from the private subnet through the NAT gateway.**</font>

NAT 网关提供出站互联网访问的同时，使用 NAT 网关的公共 IP 屏蔽后端实例的私有 IP，外部无法主动发起到私有实例的连接。

The NAT gateway provides outbound internet access while masking the private instance IP with the NAT gateway's public EIP. Inbound connections from the internet to private instances are blocked by default.

---

**Q: EC2 instances run in private subnets in 3 AZs and must connect to the internet to download files. The company wants a highly available design across the Region. Which solution ensures no disruptions to internet connectivity?**
EC2 实例在 3 个 AZ 的私有子网中运行，需要连接互联网下载文件，需要跨 Region 高可用的设计，应如何部署？

> <font color=OrangeRed>**A: Deploy a NAT gateway in a public subnet of each Availability Zone.**</font>

每个 AZ 部署一个 NAT 网关（位于该 AZ 的公共子网中），私有子网路由表指向本 AZ 的 NAT 网关。单个 NAT 网关故障不影响其他 AZ 的出站访问，实现跨 AZ 高可用。

One NAT gateway per AZ (in that AZ's public subnet). Each private subnet's route table targets its AZ-local NAT gateway. A NAT gateway failure in one AZ does not affect others — achieving regional HA.

---

**Q: Two-tier application in two AZs, databases in private subnets, web servers in public subnets. Database servers are unable to access internet patches. How to maintain security with least operational overhead?**
两层应用部署在两个 AZ，数据库在私有子网，Web 服务器在公共子网，数据库服务器无法访问互联网补丁，应如何在最低运维开销下维护安全？

> <font color=OrangeRed>**A: Deploy a NAT gateway inside the public subnet for each Availability Zone and associate it with an Elastic IP address. Update the routing table of the private subnet to use it as the default route.**</font>

NAT 网关是 AWS 托管服务，运维开销最低，部署在公共子网，私有子网路由出站流量通过 NAT 网关访问互联网，私有实例不暴露 IP。

NAT gateway is a managed service with minimal operational overhead. Deployed in the public subnet, it enables private-subnet instances to reach the internet for patches without exposing their private IPs.

---

**Q: An application in VPC-A needs to access files in an EC2 instance in VPC-B across separate AWS accounts. The connectivity should not have a single point of failure or bandwidth concerns. Which solution meets these requirements?**
VPC-A 中的应用需要访问不同 AWS 账户 VPC-B 中的 EC2 实例文件，连接不应有单点故障或带宽限制，应使用哪种方案？

> <font color=OrangeRed>**A: Set up a VPC peering connection between VPC-A and VPC-B.**</font>

VPC 对等（VPC Peering）是高可用的设计，利用 AWS 网络骨干，没有单点故障，支持跨账户连接，无带宽瓶颈。

VPC Peering is HA by design, uses the AWS network backbone, has no single point of failure, and supports cross-account connections with no bandwidth bottleneck.

---

**Q: A company has a hybrid environment and needs a hybrid connectivity solution that meets the requirement to reuse existing internet connections at the lowest cost. Which technology best meets these requirements?**
公司需要混合环境连接，要求复用现有互联网连接并降低成本，哪种技术最符合需求？

> <font color=OrangeRed>**A: AWS VPN.**</font>

VPN 使用现有互联网连接建立加密隧道，成本低，无需专线。Direct Connect 需要独立专用线路，成本较高。

VPN uses existing internet connections for an encrypted tunnel — low cost and no dedicated circuit required. Direct Connect requires a dedicated physical connection with higher cost.

---

**Q: A hybrid application requires highly resilient connectivity between on-premises and AWS using Direct Connect. Which DX configuration should be implemented?**
混合应用需要本地与 AWS 之间高度弹性的 Direct Connect 连接，应使用哪种 DX 配置？

> <font color=OrangeRed>**A: Configure DX connections at multiple DX locations.**</font>

在多个 DX 接入点配置连接，消除单一 DX 位置的故障风险，实现高可用的专线连接。单一 DX 连接上的多个虚拟接口不能解决物理层故障；添加 VPN 提供备用路径但 DX 仍存在单点。

Connecting at multiple DX locations eliminates the risk of a single physical location failure, achieving true high-availability dedicated connectivity. Multiple virtual interfaces on one DX connection do not address physical-layer failures.

---

**Q: An application requires migrating to AWS with internet-facing load balancers and application servers that need patches from an internet-hosted repository. Which services should be hosted in the public subnet?**
应用迁移到 AWS，需要面向互联网的负载均衡器和需要从互联网仓库获取补丁的应用服务器，哪些服务应放在公共子网？

> <font color=OrangeRed>**A: (1) NAT gateway. (2) Application Load Balancers.**</font>

公共子网放置面向互联网的资源：ALB（接收入站互联网流量）和 NAT 网关（为私有子网提供出站互联网访问）。EC2 应用服务器和 RDS 实例应在私有子网。

Public subnets hold internet-facing resources: ALB (accepts inbound internet traffic) and NAT gateway (provides outbound internet for private subnets). EC2 application servers and RDS instances should be in private subnets.

---

**Q: A company wants to make its website accessible to global geographic locations and needs the ability to shift traffic from resources in one region to another. What should be recommended?**
公司希望向全球地理位置提供应用访问，并需要在不同 Region 之间切换流量，应推荐什么？

> <font color=OrangeRed>**A: Configure a Route 53 geoproximity routing policy.**</font>

- **Geoproximity（地理邻近）**：可以通过调整偏差值（Bias）在 Region 之间主动迁移/切换流量，适合流量切换需求
- **Geolocation（地理位置）**：基于用户实际地理位置路由，用于内容分发权限控制，不支持手动流量调整

**Route 53 Routing Policies 路由策略对比:**

| 策略 Policy | 用途 Use Case |
|---|---|
| Simple 简单 | 单一资源，无路由逻辑 |
| Weighted 权重 | A/B 测试，分流 |
| Latency 延迟 | 路由到延迟最低的 Region |
| Failover 故障转移 | 主备切换（主健康检查）|
| Geolocation 地理位置 | 按用户所在地理位置路由（内容权限控制）|
| <font color=OrangeRed>Geoproximity 地理邻近</font> | 按地理近距离路由 + **可调整偏差值切换流量** |
| Multivalue 多值 | 多记录随机返回，基本健康检查 |

---

**Q: Route 53 content distribution: a company wants to serve content based on user location for content distribution rights. Which routing policy should be used?**
公司需要根据用户地理位置分发不同内容（内容分发权限控制），应使用哪种路由策略？

> <font color=OrangeRed>**A: Configure a Route 53 geolocation routing policy.**</font>

地理位置策略将请求路由到与用户地理位置匹配的资源，适合基于国家/大洲的内容许可控制。与地理邻近策略的区别：地理位置是精确的位置→资源映射；地理邻近可以通过 Bias 扩大或缩小某个端点的服务范围。

Geolocation policy routes requests to resources matching the user's geographic location — ideal for content licensing by country or continent. Unlike Geoproximity, it does not use adjustable bias; it maps exact locations to resources.

---

**Q: A company recently expanded globally and wants to shift traffic between resources in different Regions. Which Route 53 policy should be used?**
公司最近全球扩张，需要在不同 Region 之间切换流量，应使用哪种 Route 53 策略？

> <font color=OrangeRed>**A: Route 53 geoproximity routing policy.**</font>

地理邻近策略允许通过调整偏差值（Bias）主动扩大或缩小某个 Region 的服务范围，实现流量的定向切换。

---

**Q: A company's main website is down and a backup website with contact information is needed. How should it be deployed?**
主网站宕机时需要展示包含联系方式的备用网站，应如何部署？

> <font color=OrangeRed>**A: Use S3 website hosting for the backup website and Route 53 failover routing policy.**</font>

Route 53 故障转移路由策略结合主记录的健康检查，主站不健康时自动切换到 S3 静态备用网站，成本低且简单。

Route 53 failover routing with a health check on the primary record automatically switches to the S3-hosted backup when the primary is unhealthy. Simple and low-cost.

---

**Q: A company needs automated failover between regions using an existing warm standby in another region fronted by an ALB, currently requiring manual DNS alias record updates. How to automate failover?**
公司在另一 Region 有 warm standby 备份（ALB 前端），当前故障切换需手动更新 DNS 别名记录，如何自动化？

> <font color=OrangeRed>**A: Enable a Route 53 health check.**</font>

Route 53 健康检查 + 主动-被动故障转移记录可以自动检测主 ALB 不健康并切换 DNS 到备用 Region 的 ALB，实现无人工干预的自动故障转移。

Route 53 health check with active-passive failover record automatically detects when the primary ALB is unhealthy and switches DNS to the standby Region's ALB — no manual intervention required.

---

**Q: When would a virtual private gateway be used?**
虚拟私有网关（Virtual Private Gateway）何时使用？

> <font color=OrangeRed>**A: (1) When a VPC connects to a Private VIF with Direct Connect. (2) When using a VPN connection between a customer gateway and a VPC.**</font>

虚拟私有网关是 VPC 侧的 VPN/DX 终端，是建立 VPN 连接或 Direct Connect 私有虚拟接口的前提条件，本身具有高可用设计。

The Virtual Private Gateway is the VPC-side endpoint for both VPN connections and Direct Connect Private VIFs. It is HA by design.

---

**Q: Which routing table entry has the highest priority in a VPC?**
VPC 路由表中哪条路由条目具有最高优先级？

> <font color=OrangeRed>**A: Local routes (VPC CIDR block).**</font>

本地路由（Local Route）指向 VPC 的 CIDR 范围，不可删除，始终具有最高优先级，确保 VPC 内部流量始终通过内部网络路由。

Local routes point to the VPC's CIDR range, cannot be deleted, and always have the highest priority — ensuring intra-VPC traffic always routes internally.

---

**Q: A web application in a VPC with two EC2 instances in different AZs requires internet-accessible DNS. Which DNS configurations could be considered?**
VPC 中两个不同 AZ 的 EC2 实例运行 Web 服务器，需要可从互联网访问，应考虑哪些 DNS 配置？

> <font color=OrangeRed>**A: (1) Assign Elastic IP Addresses; configure a Route 53 "A" multi-value record with both EIPs and health checks. (2) Set up an ALB; configure a Route 53 Alias record pointing to the ALB.**</font>

指向 AWS 资源（如 ALB）时应使用 Alias 记录（而非 CNAME），因为 Alias 不收取额外查询费用且支持区顶域（Zone Apex）。

Use Alias records (not CNAME) when pointing to AWS resources like ALBs — Alias records are free of charge for AWS resource queries and support zone apex domains.

---

**Q: The deployment operates from two AZs, one application tier, and the option to launch public and private EC2 instances. Which design meets the requirement with the least infrastructure?**
部署需要使用两个 AZ，一个应用层，以及公共和私有 EC2 实例的选项，哪种设计以最少基础设施满足需求？

> <font color=OrangeRed>**A: One VPC and two subnets.**</font>

两个子网（每个 AZ 一个）即可支持公共和私有实例（通过路由表和 internet gateway 配置控制），最简化设计。

Two subnets (one per AZ) support both public and private instances via route table and internet gateway configuration — the minimal design.

---

**Q: A web application needs 9 subnets for three-AZ HA with separate tiers. How many subnets are required?**
需要三个 AZ 的高可用 Web 应用，有独立的负载均衡、Web 和数据库层，需要多少个子网？

> <font color=OrangeRed>**A: 9 subnets.**</font>

3 层（公共/Web/数据库）× 3 AZ = 9 个子网，确保每层在每个 AZ 有独立子网实现隔离和高可用。

3 tiers (public/web/database) × 3 AZs = 9 subnets, ensuring each tier has an isolated subnet in each AZ.

---

**Q: Valid sources or destinations for a VPC Security Group?**
VPC 安全组的有效来源或目标是什么？

> <font color=OrangeRed>**A: (1) The prefix list ID for an AWS service. (2) A range of IPv4 addresses. (3) A different security group.**</font>

> 安全组的来源/目标**不能**是 IAM Role 或 S3 Bucket（DynamoDB 是公共服务，安全组是 VPC 层控制，不能附加到 DynamoDB）。
>
> Security groups **cannot** use IAM Roles or S3 Buckets as sources/destinations. DynamoDB is a public service; security groups are VPC-based controls and cannot be attached to DynamoDB.

---

**Q: NACL inbound rule allows port 3389 but users still cannot connect via RDP. What is the reason?**
NACL 入站规则允许 3389 端口，但用户仍无法通过 RDP 连接，原因是什么？

> <font color=OrangeRed>**A: Network Access Control Lists are stateless — an outbound rule allowing RDP response traffic is also required.**</font>

NACL 是无状态的（stateless），需要分别配置入站和出站规则。允许 RDP 入站的同时，还需要允许出站临时端口（1024–65535）以传输响应流量。安全组是有状态的（stateful），不需要显式配置响应规则。

NACLs are stateless — inbound and outbound rules must be configured separately. Allowing RDP inbound requires a corresponding outbound rule for ephemeral ports (1024–65535) to carry response traffic. Security groups are stateful and automatically allow response traffic.

---

**Q: A company has a website and needs to set up a backup static website with a phone number and email. The DNS is managed by Route 53. How should the company deploy this solution?**
公司有一个网站，需要设置包含电话和邮件的备用静态网站，DNS 使用 Route 53，如何部署？

> <font color=OrangeRed>**A: Use S3 website hosting for the backup website and Route 53 failover routing policy.**</font>

---

## Security & IAM 安全与身份管理

---

**Q: A company has enabled AWS CloudTrail logs for each developer account and needs a central account for audit reviews. The internal auditor needs access but developer account users must be restricted. What is the most secure and optimized solution?**

*(See answer in the Database section — CloudTrail centralized logging question above.)*

---

**Q: An IAM policy for a Lambda function needs to allow put, update, and delete items in the Books DynamoDB table only, preventing any other actions on Books or any other table. Which IAM policy provides LEAST privileged access?**
Lambda 函数的 IAM 策略需要只允许对 Books DynamoDB 表的 PutItem、UpdateItem、DeleteItem 操作，不允许其他任何操作，哪个策略提供最小权限访问？

> <font color=OrangeRed>**A: Option A — Allow `dynamodb:PutItem`, `dynamodb:UpdateItem`, `dynamodb:DeleteItem` on Resource `arn:aws:dynamodb:region:account:table/Books` (specific ARN).**</font>

**Option A (correct — least privilege):**

![IAM policy: Allow specific DynamoDB actions on specific Books table ARN](./assets/img/post/iam-policy-dynamodb-books-specific-actions.png)

具体的操作列表 + 具体的资源 ARN = 最小权限原则。

Specific action list + specific resource ARN = least privilege.

**Option B (too broad — wildcard resource):**

![IAM policy: Allow specific DynamoDB actions on wildcard table/*](./assets/img/post/iam-policy-dynamodb-books-wildcard-resource.png)

Resource `table/*` 允许访问账户中所有表，违反最小权限。

`table/*` grants access to all tables in the account — violates least privilege.

**Option C (too broad — all DynamoDB actions):**

![IAM policy: Allow all dynamodb:* actions on Books table](./assets/img/post/iam-policy-dynamodb-books-all-actions.png)

`dynamodb:*` 允许所有 DynamoDB 操作（包括 Scan、Query、DeleteTable 等），超出需要。

`dynamodb:*` allows all DynamoDB operations including Scan, Query, and DeleteTable — far exceeds requirements.

**Option D (deny wins — no access):**

![IAM policy: Allow dynamodb:* with Deny dynamodb:* on same resource — Deny wins](./assets/img/post/iam-policy-dynamodb-books-allow-deny-conflict.png)

Allow + Deny 在同一资源上 → Deny 始终优先，Lambda 函数将无法执行任何操作。

Allow + Deny on the same resource → Deny always wins. The Lambda function would have no access at all.

---

**Q: An EC2 IAM policy uses `StringNotEquals` on `ec2:Region`. What does this policy allow?**
EC2 IAM 策略使用 `StringNotEquals` 条件判断 `ec2:Region`，这个策略允许什么操作？

> <font color=OrangeRed>**A: The policy allows EC2 instance termination only from a specific IP range, but denies ALL EC2 actions in regions other than us-east-1.**</font>

![IAM policy: Allow ec2:TerminateInstances with IP condition; Deny ec2:* with StringNotEquals ec2:Region = us-east-1](./assets/img/post/iam-policy-ec2-region-condition-stringnotequals.png)

策略逻辑解析：

1. **Statement 1 (Allow)**：Allow `ec2:TerminateInstances` on `*` with condition `aws:SourceIp = 10.100.100.0/24`
   → 只允许从特定 IP 段（10.100.100.0/24）终止实例
2. **Statement 2 (Deny)**：Deny `ec2:*` on `*` with condition `StringNotEquals ec2:Region = "us-east-1"`
   → 拒绝所有非 us-east-1 区域的所有 EC2 操作

**综合效果：** 只能从 10.100.100.0/24 在 us-east-1 中终止实例；其他区域的所有 EC2 操作被拒绝。

Policy analysis:

1. **Statement 1**: Allow `ec2:TerminateInstances` from source IP `10.100.100.0/24` only
2. **Statement 2**: Deny all `ec2:*` when region is NOT `us-east-1`

**Net effect:** Can terminate instances from the specified IP range, but only in us-east-1. All EC2 actions in other regions are denied.

> **`StringNotEquals` 的含义 Meaning of `StringNotEquals`:**
> `StringNotEquals: {"ec2:Region": "us-east-1"}` 表示"当 Region 不等于 us-east-1 时匹配"，即应用于 us-east-1 以外的所有区域。
>
> `StringNotEquals: {"ec2:Region": "us-east-1"}` matches when the region is anything other than us-east-1 — i.e., it applies to all regions except us-east-1.

---

**Q: An application must restrict DynamoDB access to specific people from specific IP addresses. What design should be suggested?**
应用需要将 DynamoDB 访问限制为特定 IP 的特定人员，应建议什么设计？

> <font color=OrangeRed>**A: Configure an IAM group for each level of access and add the people who need access. Give those groups access to the required DynamoDB operations with a condition matching specific IP addresses.**</font>

安全组无法附加到 DynamoDB（DynamoDB 是公共服务，安全组是 VPC 层控制）。IAM 策略条件（`aws:SourceIp`）是正确的控制机制。

Security groups cannot be attached to DynamoDB — it is a public service and security groups are VPC-based controls. IAM policy conditions (`aws:SourceIp`) are the correct mechanism.

---

**Q: A new AWS account is concerned about root user security. How to secure the root user?**
新建 AWS 账户担心 root 用户安全，如何保护 root 用户？

> <font color=OrangeRed>**A: Create IAM users for daily administrative tasks. Enable multi-factor authentication on the root user.**</font>

Root 用户无法被禁用（AWS 不允许），但可以通过启用 MFA 保护，并通过创建 IAM 用户处理日常管理任务来最小化 root 用户的使用。

Root user cannot be disabled — AWS doesn't allow it. Protect it with MFA, and create IAM users for day-to-day administration to minimize root usage.

> **Root 用户特殊性 Root user facts:**
> - Root 用户**不能**被 IAM 策略拒绝访问资源
> - Root 用户**不能**被禁用，只能最小化使用
> - 设置 MFA 时应保留 MFA URL 或 QR 码副本

---

**Q: A company has a requirement that all data must be encrypted at rest with complete control of encryption key lifecycle management. They must be able to immediately remove key material and audit key usage independently of CloudTrail. Which service satisfies these requirements?**
公司要求数据在静态加密时对密钥生命周期有完全控制，可以立即删除密钥材料，且审计独立于 CloudTrail，哪个服务满足这些要求？

> <font color=OrangeRed>**A: AWS CloudHSM with the CloudHSM client.**</font>

CloudHSM 是专用的硬件安全模块，客户完全控制密钥材料（AWS 无法访问），可立即删除密钥，有独立于 CloudTrail 的审计日志。KMS 密钥管理是 AWS 共享责任，KMS 的审计通过 CloudTrail 完成。

CloudHSM provides dedicated HSMs where the customer has full control over key material — AWS has no access. Keys can be immediately removed, and CloudHSM has its own independent audit logs separate from CloudTrail. KMS keys are managed under AWS shared responsibility, and KMS auditing flows through CloudTrail.

---

**Q: Company stores symmetric encryption keys in an on-premises HSM and wants to migrate to AWS. The solution must allow key rotation and support customer-provided keys. Where should key material be stored?**
公司在本地 HSM 存储对称加密密钥，需迁移到 AWS，方案必须支持密钥轮换和客户自带密钥，应使用什么？

> <font color=OrangeRed>**A: AWS Key Management Service (AWS KMS).**</font>

KMS 支持密钥轮换（Automatic Key Rotation）以及客户自带密钥材料（BYOK/External Key Material），与其他 AWS 存储服务集成。

KMS supports automatic key rotation and customer-provided key material (BYOK/external key origin), and integrates natively with other AWS storage services.

---

**Q: A company wants to prevent cross-site scripting and SQL injection attacks on its application. What steps should be taken?**
公司遭受跨站脚本攻击和 SQL 注入攻击，应采取什么步骤快速缓解？

> <font color=OrangeRed>**A: Using WAF, set up rules which block SQL injection and cross-site scripting attacks. Associate the rules to the ALB.**</font>

AWS WAF 提供内置的 SQLi 和 XSS 检测规则，通过关联到 ALB（或 CloudFront、API Gateway）可以在到达应用之前过滤恶意请求。

AWS WAF provides built-in SQLi and XSS detection rules. Associating the WAF web ACL with an ALB (or CloudFront, API Gateway) filters malicious requests before they reach the application.

---

**Q: A web application needs WAF protection for XSS attacks. An NLB is currently in use. What should be changed?**
Web 应用需要 WAF 保护 XSS 攻击，当前使用 NLB，应如何调整？

> <font color=OrangeRed>**A: Replace the NLB with an ALB and associate a WAF web ACL with it.**</font>

WAF 只能附加到 ALB（7 层）、CloudFront 和 API Gateway，无法附加到 NLB（4 层）或 Classic Load Balancer。

WAF can only be attached to ALB (Layer 7), CloudFront, and API Gateway — not NLB (Layer 4) or Classic Load Balancer.

---

**Q: A company wants to block malicious IP addresses reaching its CloudFront-served web application. Which configuration is correct?**
公司想要阻止恶意 IP 访问 CloudFront 提供的 Web 应用，应如何配置？

> <font color=OrangeRed>**A: Configure a WAF IP match condition to block the malicious IP, and associate the WAF web ACL with the CloudFront distribution.**</font>

NACL 无法直接应用于 CloudFront（CloudFront 位于 AWS 边缘，不在 VPC 内）。WAF 可以关联到 CloudFront 分发，在边缘层过滤流量。

NACLs cannot be applied directly to CloudFront — CloudFront operates at AWS edge locations outside the VPC. WAF can be associated with CloudFront distributions to filter at the edge.

---

**Q: A company needs to quickly protect web application against known CVE vulnerabilities. Which WAF feature should be used?**
公司需要快速保护 Web 应用免受已知 CVE 漏洞影响，应使用 WAF 的哪个功能？

> <font color=OrangeRed>**A: WAF managed rules for CVE protection.**</font>

AWS WAF 托管规则由 AWS 和合作伙伴维护，包含针对已知 CVE 的规则组（如 Amazon IP Reputation List、Core Rule Set），可快速部署无需自定义规则编写。

AWS WAF managed rules (from AWS and partners) include rule groups targeting known CVEs (e.g., Core Rule Set, IP Reputation List). They can be deployed immediately without writing custom rules.

---

**Q: A company is being informed of attacks as they happen and wants AWS assistance to mitigate attacks. WAF is deployed and Enterprise Support is in place. What additional step is recommended?**
公司希望在攻击发生时获得通知，并希望 AWS 协助缓解攻击，已有 WAF 和企业支持，应采取什么额外步骤？

> <font color=OrangeRed>**A: Purchase AWS Shield Advanced. During an attack, lodge a support request asking for assistance from AWS.**</font>

Shield Advanced 提供 DDoS 防护、自动 WAF 规则缓解，以及在攻击期间通过 Shield Response Team (SRT) 获得 AWS 主动协助，适合需要 AWS 直接支持的高价值资产。

Shield Advanced provides DDoS protection, automatic WAF rule mitigation, and access to the Shield Response Team (SRT) for proactive AWS assistance during attacks — essential for high-value assets requiring direct AWS support.

---

**Q: You manage hundreds of AWS accounts and need to restrict what can occur within a development account. There are 6 IAM users and an account root user that need to be restricted. What solution would be best?**
管理数百个 AWS 账户，需要限制开发账户中的操作，包括 6 个 IAM 用户和 root 用户，什么方案最好？

> <font color=OrangeRed>**A: Service Control Policy (SCP).**</font>

SCP 通过 AWS Organizations 应用于整个账户（包括 root 用户），可以限制账户内所有主体（IAM 用户、角色、root）可执行的最大权限，是跨账户权限边界的标准工具。IAM 策略无法限制 root 用户。

SCPs applied through AWS Organizations restrict the maximum permissions for all principals in an account — including the root user. IAM policies alone cannot restrict the root user.

---

**Q: Create a configuration allowing access to S3 buckets to IAM users from an external account. Objects uploaded must be owned by your account. What is the best design?**
允许外部账户的 IAM 用户访问本账户的 S3 桶，上传的对象必须归本账户所有，最佳设计是什么？

> <font color=OrangeRed>**A: Create an IAM role in your AWS account and allow external IAM users to assume it.**</font>

通过 IAM 角色（跨账户信任策略）授权外部用户访问，角色的权限策略在本账户内执行，外部用户上传的对象所有权属于本账户（因为操作通过本账户角色执行）。

An IAM role with a cross-account trust policy grants external users access. Operations performed through this role execute within the target account's context, so uploaded objects are owned by the target account.

---

**Q: You intend on managing the encryption keys and using Amazon S3 to manage the encryption itself. Which encryption option should be used?**
希望自己管理加密密钥，由 Amazon S3 执行加密操作，应使用哪种加密选项？

> <font color=OrangeRed>**A: Server-Side Encryption with Customer-Provided Keys (SSE-C).**</font>

SSE-C 允许客户提供密钥，S3 使用该密钥执行加密和解密，密钥不由 AWS 存储。SSE-S3 使用 AWS 托管密钥；SSE-KMS 使用 KMS 管理的密钥；CSE（客户端加密）是由客户端执行加密。

SSE-C lets the customer provide the key while S3 performs the encryption/decryption — AWS does not store the key. SSE-S3 uses AWS-managed keys; SSE-KMS uses KMS-managed keys; CSE has the client perform encryption.

---

**Q: Which item is NOT a feature of AWS CloudTrail?**
哪个不是 AWS CloudTrail 的功能？

> <font color=OrangeRed>**A: Monitor Auto Scaling Groups and optimize resource utilization — this is a CloudWatch feature, not CloudTrail.**</font>

CloudTrail 的功能：回答用户活动问题（who did what, when）、演示合规性、跟踪资源变更。
CloudWatch 的功能：监控指标、自动扩展组监控、资源利用率优化。

CloudTrail features: answer questions about user activity, demonstrate compliance, track resource changes.
CloudWatch features: metric monitoring, Auto Scaling group monitoring, resource utilization optimization.

---

**Q: Certain EBS volume metrics need to be monitored and the database team notified by email when thresholds are exceeded. Which AWS services should be configured?**
需要监控 EBS 卷指标，超过阈值时通过邮件通知数据库团队，应配置哪些 AWS 服务？

> <font color=OrangeRed>**A: CloudWatch (monitoring) + SNS (email notification).**</font>

CloudWatch 监控 EBS 指标（如 VolumeQueueLength、BurstBalance），配置告警阈值后触发 SNS 主题，SNS 订阅者收到邮件通知。

CloudWatch monitors EBS metrics and triggers an alarm at the threshold. The alarm action publishes to an SNS topic; SNS sends the email notification to subscribers.

---

**Q: An on-premises Active Directory is connected to AWS via site-to-site VPN. WorkSpaces must be set up. What needs to be done before deploying WorkSpaces?**
本地 AD 通过 Site-to-Site VPN 连接到 AWS，需要部署 WorkSpaces，在此之前需要做什么？

> <font color=OrangeRed>**A: Configure AD Connector.**</font>

AD Connector 是目录网关，将目录请求重定向到本地 Microsoft Active Directory，无需在云中缓存信息，是 WorkSpaces 使用本地 AD 身份验证的必要前提。

AD Connector is a directory gateway that redirects directory requests to the on-premises Microsoft Active Directory without caching any information in the cloud — required for WorkSpaces to authenticate against on-premises AD.

---

**Q: EBS/S3/EFS: which AWS services allow native encryption of data at rest?**
哪些 AWS 服务允许原生加密静态数据？

> <font color=OrangeRed>**A: EBS, S3, and EFS.**</font>

> **注意 Exception:** ElastiCache for <font color=OrangeRed>Memcached</font> does NOT offer native encryption at rest. ElastiCache for <font color=OrangeRed>Redis</font> does support encryption at rest.

---

## Application Services 应用服务

---

**Q: A video processing platform uses SQS to manage transcoding jobs. What options reduce costs without negatively impacting performance over time?**
视频转码平台使用 SQS 管理任务，如何在不负面影响性能的前提下降低成本？

> <font color=OrangeRed>**A: Use Spot Instances.**</font>

Spot 实例可大幅降低 EC2 成本。Spot 实例被终止时，Auto Scaling Group 会补充新实例，SQS 的可见性超时会使失败任务重新入队，整体成本显著低于 On-Demand。增强型网络降低延迟但不影响整体吞吐成本。

Spot Instances significantly reduce EC2 costs. When terminated, the ASG compensates with new instances; SQS visibility timeouts re-queue failed jobs. Overall cost is much lower than On-Demand. Enhanced networking reduces latency but doesn't materially impact overall cost.

---

**Q: SQS is used to manage messages in a ticketing system. Messages are not arriving in the order they were generated. Which are correct explanations?**
SQS 管理票务系统中的消息，消息没有按生成顺序到达，哪些解释是正确的？

> <font color=OrangeRed>**A: (1) If an agent abandons a message, it is offered in the queue again — preventing message loss but causing out-of-order delivery. (2) SQS uses multiple hosts; each host holds only a portion of all messages — consumers do not see all hosts simultaneously.**</font>

SQS Standard 队列设计特点：
- **至少一次传递（At-least-once delivery）**：消息可能重复
- **尽力排序（Best-effort ordering）**：不保证顺序
- 多主机架构：消费者在某次 poll 中可能只看到部分消息

SQS Standard Queue design characteristics:
- At-least-once delivery: messages may be duplicated
- Best-effort ordering: order not guaranteed
- Multi-host architecture: a consumer poll may only see a subset of messages from a subset of hosts

---

**Q: SQS FIFO queue is needed for ordered, exactly-once processing. What should be noted about the maximum VisibilityTimeout?**
需要 SQS FIFO 队列实现有序和精确一次处理，SQS 消息最大 VisibilityTimeout 是多少？

> <font color=OrangeRed>**A: 12 hours.**</font>

SQS 消息 VisibilityTimeout 最大值为 12 小时，在此期间消息对其他消费者不可见，允许消费者在长时间处理后才删除消息。

The maximum VisibilityTimeout for SQS messages (both Standard and FIFO) is 12 hours, allowing consumers sufficient time to process long-running tasks before the message becomes visible again.

---

**Q: An SQS design review discovers that `WaitTimeSeconds` is being changed to reduce costs. What is the effect of this parameter?**
SQS 设计审查发现修改 `WaitTimeSeconds` 来降低成本，这个参数的效果是什么？

> <font color=OrangeRed>**A: When the consumer instance polls for new work, SQS allows it to wait a certain time for one or more messages to be available before closing the connection — this is long polling.**</font>

长轮询（Long Polling，WaitTimeSeconds > 0）让消费者等待消息到达，减少空 API 调用次数，降低 SQS 请求费用。短轮询（WaitTimeSeconds = 0）立即返回，即使没有消息，产生更多 API 调用。

Long polling (WaitTimeSeconds > 0) allows the consumer to wait for messages before closing the connection, reducing empty API calls and SQS request costs. Short polling (WaitTimeSeconds = 0) returns immediately even if no messages are available, generating more API calls.

---

**Q: A cloud-based email notification is needed when users push code to a CodeCommit repository. How to configure this?**
需要在用户向 CodeCommit 推送代码时接收邮件通知，如何配置？

> <font color=OrangeRed>**A: Configure Notifications in the CodeCommit console — this creates a CloudWatch Events rule that sends a notification to an SNS topic, which triggers an email.**</font>

正确配置路径：CodeCommit Notifications → CloudWatch Events 规则（自动创建）→ SNS 主题 → 邮件订阅者。

> **注意：** SNS <font color=OrangeRed>不能</font>主动轮询 CodeCommit 事件；CodeCommit 触发器可以直接发送到 SNS，但 Notifications 是推荐路径。
>
> **Note:** SNS <font color=OrangeRed>cannot</font> poll CodeCommit for events. CodeCommit triggers can send directly to SNS, but the Notifications feature is the recommended path.

---

**Q: An application needs to capture IoT data in real-time, process it in order per sensor, and store to S3. What should be recommended?**
应用需要实时捕获 IoT 数据，按传感器有序处理，存储到 S3，应推荐什么？

> <font color=OrangeRed>**A: Kinesis Data Streams (for ordered per-partition capture) + Kinesis Data Firehose (to deliver to S3).**</font>

Kinesis Data Streams 通过分区键（partition key）保证同一分区内的数据有序；Kinesis Firehose 提供从 Kinesis Streams 到 S3 的无服务器传输。

Kinesis Data Streams guarantees ordering within a partition (using partition key = sensor ID); Kinesis Data Firehose provides serverless delivery from Kinesis Streams to S3.

---

**Q: A web app with burst/inactivity traffic pattern needs to be cost-effective and scalable. What combination should be recommended?**
具有突发/静止流量模式的 Web 应用需要成本效益和可扩展性，应推荐什么组合？

> <font color=OrangeRed>**A: API Gateway + Lambda.**</font>

Lambda 按请求计费，无流量时零费用；API Gateway 自动扩展处理突发流量；两者结合实现完全无服务器架构，最适合突发/静止流量模式。

Lambda charges per request with zero cost during inactivity; API Gateway scales automatically to handle bursts. Together they provide a fully serverless architecture — optimal for burst/inactivity traffic patterns.

---

**Q: A manufacturing company's application executes workflows with multiple AWS services, human interaction, and steps taking weeks to complete. What is a cost-effective alternative?**
制造公司的应用运行包含多个 AWS 服务、人工交互，步骤可能需要数周完成的工作流，什么是具有成本效益的替代方案？

> <font color=OrangeRed>**A: Migrate the flows to one or more state machines (AWS Step Functions).**</font>

Step Functions 是无服务器的状态机编排服务，可以协调长时间运行的工作流（包含人工交互等待）、调用其他 AWS 服务，按状态转换次数计费，适合复杂、长时间工作流。

Step Functions is a serverless workflow orchestrator that can coordinate long-running workflows involving human interaction waits and calls to multiple AWS services. Pricing is per state transition — cost-effective for complex, long-duration workflows.

---

**Q: A decoupled, scalable architecture is needed for an app with traffic-spiking scenarios. S3 fronts the app, with dynamic processing behind it. What should the architecture look like?**
需要一个解耦、可扩展的架构应对流量突增场景，S3 作为前端，后端进行动态处理。架构应如何设计？

> <font color=OrangeRed>**A: S3 frontend + API Gateway + SQS + Auto Scaling group to process the queue.**</font>

S3 提供静态前端；API Gateway 接收动态请求并写入 SQS；Auto Scaling 组根据 SQS 队列长度自动扩展处理能力，实现前后端解耦和流量削峰。

S3 serves the static frontend; API Gateway accepts dynamic requests and enqueues to SQS; the Auto Scaling group scales based on SQS queue depth. This decouples the frontend from processing and handles traffic spikes gracefully.

---

**Q: An ECS application needs to access an S3 bucket. How to ensure the application has permission?**
ECS 应用需要访问 S3 桶，如何确保应用有权限？

> <font color=OrangeRed>**A: Create an IAM role with S3 permissions, and then specify that role as the `taskRoleArn` in the task definition.**</font>

ECS 任务角色（Task Role）通过 `taskRoleArn` 为容器提供 AWS 权限，是 ECS 访问 AWS 服务的正确方式。不应使用 IAM 用户凭证嵌入容器，违反安全最佳实践。

The ECS Task Role assigned via `taskRoleArn` provides AWS service permissions to the container — the correct and secure pattern for ECS. Embedding IAM user credentials in containers violates security best practices.

---

## Migration & Hybrid 迁移与混合

---

**Q: A company has 150 TB of archived image data on-premises to move to AWS within 1 month. Network allows 100 Mbps uploads nights only. What is the most cost-effective mechanism?**
公司有 150 TB 归档图像数据需要在 1 个月内迁移到 AWS，网络仅允许夜间 100 Mbps 上传。最具成本效益的方案是什么？

> <font color=OrangeRed>**A: Order multiple AWS Snowball devices to ship the data to AWS.**</font>

100 Mbps × 夜间 8 小时 = ~360 GB/天 → 150 TB 需要约 416 天，远超 1 个月的截止时间。Snowball 设备每台 80 TB，订购多台物理运输可在数周内完成。Snowmobile 用于 EB 级数据（过于大型）；Transfer Acceleration 仍受网络限制。

100 Mbps × 8 hours/night ≈ 360 GB/day → 150 TB would take ~416 days via network — far beyond the 1-month deadline. Multiple Snowball devices (each 80 TB) ship physically and can complete in weeks. Snowmobile is for exabyte-scale; Transfer Acceleration is still network-constrained.

---

**Q: A company must migrate 20 TB from a data center to the AWS Cloud within 30 days. Network bandwidth is limited to 15 Mbps at 70% utilization. What should be done?**
公司需要在 30 天内将 20 TB 数据迁移到 AWS，网络带宽限制为 15 Mbps（最多 70% 利用率），应如何处理？

> <font color=OrangeRed>**A: Use AWS Snowball.**</font>

15 Mbps × 70% ≈ 10.5 Mbps → 20 TB 需要约 174 天，无法在 30 天内完成。Snowball 物理传输是唯一满足时间要求的方案。

15 Mbps × 70% ≈ 10.5 Mbps → 20 TB would take ~174 days over network. Physical Snowball transfer is the only option that meets the 30-day deadline.

---

**Q: 750 TB of data needs to be transferred. The company wants to avoid saturating the bandwidth. What should a solutions architect recommend?**
需要传输 750 TB 数据，公司希望避免带宽饱和，应推荐什么方案？

> <font color=OrangeRed>**A: Use AWS Snowball to transfer the data, then configure an S3 lifecycle policy to transition it to S3 Glacier.**</font>

Snowball 用于大规模物理数据传输，避免占用生产网络带宽；S3 生命周期策略将数据转移到 Glacier 降低长期存储成本。

Snowball handles large-scale physical data transfer without consuming production network bandwidth. S3 lifecycle policy then moves the data to Glacier for cost-effective long-term retention.

---

**Q: A company needs to automate the replication of on-premises data to AWS over Direct Connect. Which service should be recommended?**
公司需要通过 Direct Connect 自动将本地数据复制到 AWS，应推荐哪个服务？

> <font color=OrangeRed>**A: AWS DataSync.**</font>

DataSync 是自动化的数据迁移和同步服务，支持通过 Direct Connect 将本地 NFS/SMB/S3 兼容存储传输到 AWS，提供调度、带宽限制和数据完整性验证。

DataSync is an automated data migration and synchronization service that supports scheduled, bandwidth-throttled transfers from on-premises NFS/SMB storage to AWS over Direct Connect, with built-in data integrity verification.

---

**Q: A company has VMDK files from a private cloud platform and needs to create EC2 instances from them. Which AWS service helps achieve this?**
公司有私有云的 VMDK 文件，需要使用这些文件创建 EC2 实例，哪个 AWS 服务有助于实现这一目标？

> <font color=OrangeRed>**A: VM Import/Export.**</font>

VM Import/Export 支持将 VMware、Microsoft Hyper-V、Citrix 等格式的虚拟机（包括 VMDK、VHD、OVA）导入为 AMI，然后从中启动 EC2 实例。

VM Import/Export supports importing virtual machines from VMware, Hyper-V, and Citrix (including VMDK, VHD, OVA formats) as AMIs, which can then be used to launch EC2 instances.

---

**Q: A freight carrier and shipping company both run on AWS and need to automate ordering. The shipping company needs the best security and operational efficiency for transactions. What architecture should be recommended?**
货运公司和航运公司都在 AWS 上运行，需要自动化订单，要求最佳安全性和运营效率，应推荐什么架构？

> <font color=OrangeRed>**A: Have the freight carrier create an Endpoint Service (PrivateLink). The shipping company connects via an Interface VPC Endpoint.**</font>

AWS PrivateLink 在 AWS 网络内部提供跨账户、跨 VPC 的私有连接，无需将流量暴露给公网，安全性高，运营开销低于 VPN 连接或 VPC 对等。

AWS PrivateLink provides private cross-account, cross-VPC connectivity over the AWS network without exposing traffic to the internet. It has lower operational overhead than VPN or VPC Peering for service-to-service connectivity.

---

## Cost Optimization 成本优化

---

**Q: A company requires DEV and PROD environments for several years. DEV instances run 10 hours each day during business hours. PROD instances run 24 hours. What is the most cost-effective instance purchase strategy?**
公司需要多年运行 DEV 和 PROD 环境。DEV 每天工作时间运行 10 小时；PROD 每天运行 24 小时。最具成本效益的购买策略是什么？

> <font color=OrangeRed>**A: DEV with Scheduled Reserved Instances and PROD with Reserved Instances.**</font>

- **DEV**：定时预留实例（Scheduled Reserved Instances）按预定时间窗口保留容量，仅在使用时计费，适合每天 10 小时的固定工作时间
- **PROD**：标准预留实例（Reserved Instances，1 年或 3 年期）对比 On-Demand 提供最高折扣，适合 24/7 持续运行

- **DEV**: Scheduled Reserved Instances reserve capacity for a fixed time window (business hours), paying only for scheduled usage — ideal for predictable 10-hour daily workloads.
- **PROD**: Standard Reserved Instances (1-year or 3-year) provide the highest discount vs. On-Demand for 24/7 continuous operation.

---

**Q: An analytics workload using EC2 runs variable jobs nightly that must finish by start of business. What is the most cost-effective solution?**
EC2 夜间大数据分析工作负载，每晚运行不固定，必须在次日上班前完成，最具成本效益的方案是什么？

> <font color=OrangeRed>**A: Reserved Instances.**</font>

工作负载关键且必须在特定时间完成 → Spot 和 Spot Fleet 不能保证实例可用性，存在被中断的风险。Reserved Instances 提供容量保证和成本折扣，On-Demand 成本最高。

Critical workload with a firm deadline → Spot/Spot Fleet cannot guarantee availability. Reserved Instances provide capacity guarantee with cost savings. On-Demand is the most expensive option.

---

**Q: A stateless web tier with high availability needs to be deployed in the most cost-effective way. Which approach is recommended?**
需要以最具成本效益的方式部署具有高可用性的无状态 Web 层，应推荐什么方案？

> <font color=OrangeRed>**A: Use an ELB + multi-AZ Auto Scaling Group of EC2 Spot instances (primary) with On-Demand instances (secondary) + DynamoDB.**</font>

Spot 实例（主）+ On-Demand 实例（备）：On-Demand 仅在 Spot 实例不可用时启动，成本最低。DynamoDB（区域服务）比 RDS Multi-AZ 更适合无状态 Web/应用层，无需多 AZ 部署配置。

Spot (primary) + On-Demand (secondary): On-Demand instances only spin up when Spot instances are unavailable — minimizing cost while maintaining availability. DynamoDB is a regional service natively suited for stateless web tiers; no Multi-AZ deployment configuration needed.

---

**Q: To scale as quickly as possible in a cost-effective way for increasing and decreasing demand, what approach should be used?**
为了以最具成本效益的方式快速应对增减需求，应使用什么方法？

> <font color=OrangeRed>**A: Horizontal scaling with small instances.**</font>

水平扩展（增加实例数量）比垂直扩展（增大实例规格）更灵活，更快响应需求变化。小型实例每次扩展的步进粒度更细，容量利用更高效，无实例大小限制问题。

Horizontal scaling (adding instances) is more responsive than vertical scaling (resizing). Smaller instances provide finer-grained capacity steps — fewer wasted resources per scaling event and no instance-size availability restrictions.

---

## Key Takeaways 核心要点

- **EFS vs EBS vs FSx**: EFS = Linux 多实例 NFS；FSx for Windows = Windows SMB + AD；EBS = 单实例块存储。EFS for Linux multi-instance NFS; FSx for Windows SMB+AD; EBS is single-instance block.
- **RDS 读副本 vs Multi-AZ**: 读副本 = <font color=OrangeRed>可读</font>，用于分流读流量；Multi-AZ 备用实例 = <font color=OrangeRed>不可读</font>，仅用于 HA 故障转移。Read Replica = readable for offloading reads; Multi-AZ standby = not readable, HA only.
- **Aurora Global Database**: 多 Region <font color=OrangeRed>RPO ~1s, RTO ~1min</font>。Multi-Region RPO ~1s, RTO ~1min.
- **DAX vs ElastiCache**: DAX → DynamoDB；ElastiCache → RDS/关系型。DAX for DynamoDB; ElastiCache for RDS.
- **DynamoDB 热分区**: PK 基数低（如 3 个候选值）→ 每分区上限 1,000 WCU → 总吞吐受限。Low PK cardinality creates hot partitions (max 1,000 WCU each).
- **WAF 附加目标**: 只能附加到 <font color=OrangeRed>ALB、CloudFront、API Gateway</font>，不能附加 NLB 或 Classic LB。WAF attaches to ALB/CloudFront/API Gateway only — not NLB or Classic LB.
- **NAT 网关 HA**: 每个 AZ 的公共子网部署一个 NAT 网关，私有子网路由到本 AZ 的 NAT 网关。One NAT gateway per AZ public subnet for HA.
- **Snowball 适用场景**: 网络带宽不足以在截止时间前完成传输时选择 Snowball 物理传输。Use Snowball when network bandwidth cannot meet the migration deadline.
- **SQS Standard**: at-least-once delivery + best-effort ordering（不保证顺序）。SQS Standard: at-least-once, best-effort ordering — not guaranteed order.
- **SQS VisibilityTimeout 最大值**: <font color=OrangeRed>12 小时 12 hours</font>。
- **NAT Instance**: 必须禁用 Source/Destination Checks。Must disable Source/Destination Checks.
- **Route 53 Geoproximity vs Geolocation**: Geoproximity = 可调偏差切换流量；Geolocation = 精确位置→资源映射（内容权限控制）。Geoproximity = bias-adjustable traffic shifting; Geolocation = exact location-to-resource mapping.
- **IAM 最小权限**: 具体操作 + 具体资源 ARN；Deny 始终优先于 Allow。Specific actions + specific ARN; Deny always overrides Allow.
- **SCP**: 限制整个 AWS 账户（包括 root 用户）的最大权限，IAM 策略无法限制 root。SCP restricts the entire account including root; IAM policies cannot restrict root.
- **PrivateLink**: 跨账户/跨 VPC 私有服务连接，不经公网；Direct Connect 用于本地到 AWS，不用于两个 AWS 账户之间。PrivateLink for cross-account/VPC private connectivity; Direct Connect is not for two AWS customers.
- **CloudHSM**: 客户完全控制密钥，独立审计（非 CloudTrail），可立即删除密钥材料。Customer full key control, independent audit, immediate key removal.
- **S3 加密**: SSE-S3 (AWS 管理) / SSE-KMS (KMS 管理) / SSE-C (客户提供密钥，S3 执行加密) / CSE (客户端加密)。SSE-C: customer provides key, S3 performs encryption.
- **Global Accelerator**: 静态 IP + AWS 骨干网路由，适合 TCP/UDP；CloudFront 适合 HTTP 内容缓存。Global Accelerator for static-IP TCP/UDP; CloudFront for HTTP content caching.

## References

- Source: AWS Solutions Architect Associate practice questions
- `_posts/01Cloud/01AWS/IAM/` — IAM, STS, KMS references
- `_posts/01Cloud/01AWS/Networking/` — VPC, Route 53, Direct Connect references
- `_posts/01Cloud/01AWS/Storage/` — S3, EFS, FSx, Storage Gateway references
- `_posts/01Cloud/01AWS/Database/` — RDS, Aurora, DynamoDB references
