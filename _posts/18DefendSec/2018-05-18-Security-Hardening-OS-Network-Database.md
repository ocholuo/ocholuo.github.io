---
title: "Meow's DefendSec - Security Hardening: OS, Network, Database & Enterprise"
date: 2018-05-18 11:11:11 -0400
categories: [18DefendSec, Hardening]
tags: [Hardening, OS, NetworkSec, Database, EnterpriseSecuirty, RBAC, RADIUS, Kerberos, TACACS, SQLInjection, PatchManagement]
math: false
toc: true
image:
---

# Security Hardening: OS, Network, Database & Enterprise

- [Security Hardening: OS, Network, Database \& Enterprise](#security-hardening-os-network-database--enterprise)
  - [Overview 概述](#overview-概述)
  - [OS Hardening 操作系统加固](#os-hardening-操作系统加固)
    - [1. Preparation and Installation 准备与安装](#1-preparation-and-installation-准备与安装)
    - [2. Security Settings 安全配置](#2-security-settings-安全配置)
    - [3. Patches and Patch Management 补丁与补丁管理](#3-patches-and-patch-management-补丁与补丁管理)
    - [4. Process Security 进程安全](#4-process-security-进程安全)
    - [5. User Account Policies and Access Control 用户账户策略与访问控制](#5-user-account-policies-and-access-control-用户账户策略与访问控制)
    - [6. Audit Policy and Change Management 审计策略与变更管理](#6-audit-policy-and-change-management-审计策略与变更管理)
    - [7. Additional Controls 其他控制](#7-additional-controls-其他控制)
    - [8. Physical Security 物理安全](#8-physical-security-物理安全)
    - [9. Attacks Mitigated by OS Hardening](#9-attacks-mitigated-by-os-hardening)
  - [Enterprise Security 企业安全](#enterprise-security-企业安全)
    - [1. Risk Assessment 风险评估](#1-risk-assessment-风险评估)
    - [2. Risk Management 风险管理](#2-risk-management-风险管理)
    - [3. Policies, Standards, and Guidelines 策略、标准与指南](#3-policies-standards-and-guidelines-策略标准与指南)
    - [4. Disaster Recovery and Incident Response 灾难恢复与事件响应](#4-disaster-recovery-and-incident-response-灾难恢复与事件响应)
  - [Network Controls 网络控制](#network-controls-网络控制)
    - [OSI Model Mapping OSI模型控制映射](#osi-model-mapping-osi模型控制映射)
    - [Confidentiality Controls 机密性控制](#confidentiality-controls-机密性控制)
      - [Cryptography and Encryption 加密](#cryptography-and-encryption-加密)
      - [Authentication Protocols 认证协议](#authentication-protocols-认证协议)
        - [Kerberos](#kerberos)
        - [RADIUS](#radius)
        - [TACACS+](#tacacs)
    - [Integrity Controls 完整性控制](#integrity-controls-完整性控制)
    - [Availability Controls 可用性控制](#availability-controls-可用性控制)
  - [Database Hardening 数据库加固](#database-hardening-数据库加固)
    - [1. Physical Database Server Security 物理安全](#1-physical-database-server-security-物理安全)
    - [2. Firewalls for Database Servers 防火墙](#2-firewalls-for-database-servers-防火墙)
    - [3. Database Software 数据库软件](#3-database-software-数据库软件)
    - [4. Application / Web Servers / Application Code](#4-application--web-servers--application-code)
    - [5. Accounts, Permissions, and Passwords 账户与权限](#5-accounts-permissions-and-passwords-账户与权限)
    - [6. Protected Data 数据保护](#6-protected-data-数据保护)
    - [7. Change Management 变更管理](#7-change-management-变更管理)
    - [8. Database Auditing 数据库审计](#8-database-auditing-数据库审计)
    - [9. Database Backup and Recovery 备份与恢复](#9-database-backup-and-recovery-备份与恢复)
    - [10. Database Encryption and Key Management 加密与密钥管理](#10-database-encryption-and-key-management-加密与密钥管理)
    - [11. Attack: SQL Injection SQL注入攻击](#11-attack-sql-injection-sql注入攻击)
  - [Meow's Security Considerations 安全注意事项](#meows-security-considerations-安全注意事项)
    - [1. Kerberos KDC Compromise — Golden Ticket 黄金票据攻击 — Critical](#1-kerberos-kdc-compromise--golden-ticket-黄金票据攻击--critical)
    - [2. Incomplete Patch Management 补丁管理不完整 — High](#2-incomplete-patch-management-补丁管理不完整--high)
    - [3. SQL Injection via Missing Parameterized Queries SQL注入 — High](#3-sql-injection-via-missing-parameterized-queries-sql注入--high)
    - [4. RBAC Misconfiguration — Privilege Escalation 权限配置错误 — High](#4-rbac-misconfiguration--privilege-escalation-权限配置错误--high)
    - [5. BIOS/Firmware Password Bypass 固件密码绕过 — Medium](#5-biosfirmware-password-bypass-固件密码绕过--medium)
    - [6. Audit Log Tampering 审计日志篡改 — Medium](#6-audit-log-tampering-审计日志篡改--medium)
    - [7. RADIUS Password-Only Encryption RADIUS仅加密密码 — Medium](#7-radius-password-only-encryption-radius仅加密密码--medium)
    - [Summary Table 汇总表](#summary-table-汇总表)
  - [Key Takeaways](#key-takeaways)
  - [References](#references)

---

## Overview 概述

Security hardening reduces the attack surface of systems by removing unnecessary services, enforcing access controls, applying patches, and implementing monitoring. This note covers four hardening domains: operating systems, enterprise security governance, network controls, and database servers. Together they form a layered defense aligned with the CIA triad and OSI model.

安全加固通过删除不必要的服务、强制访问控制、应用补丁和实施监控来减少系统的攻击面。本文涵盖四个加固领域：操作系统、企业安全治理、网络控制和数据库服务器，共同构建与CIA三要素和OSI模型对齐的纵深防御体系。

---

## OS Hardening 操作系统加固

### <font color="#fb02ff">1. Preparation and Installation 准备与安装</font>

- Use <font color=OrangeRed>master images</font> to deploy a consistent, pre-hardened baseline across all systems.
- Complete a **programs clean-up** — remove all unnecessary programs. Attackers look for backdoors and security holes; minimizing installed software reduces their entry points.
- <font color=OrangeRed>Disable or uninstall unused services and unused user accounts.</font>
  - Example: disable ICMP if not required — prevents <font color="#ecb8ff">Ping of Death</font> attacks.

### <font color="#fb02ff">2. Security Settings 安全配置</font>

- Establish <font color=OrangeRed>configuration baselines</font> and measure compliance on a schedule. Use the <font color="blue">CIS Benchmark</font> as the baseline standard.
- Make a system image of each OS using tools like **GHOST** or **Clonezilla** to simplify further installation and re-hardening after incidents.

### <font color="#fb02ff">3. Patches and Patch Management 补丁与补丁管理</font>

- Planning, testing, implementing, and auditing patch management should be part of a regular security regimen.
- Keep the OS and all installed programs patched regularly.
- Use <font color="blue">sandbox and container environments</font> to test patches before production deployment.
- <font color="#ecb8ff">0-day exploits</font> represent attacks for which no patch exists — layered defenses (network segmentation, monitoring) are the primary mitigation.

### <font color="#fb02ff">4. Process Security 进程安全</font>

- Set a <font color=OrangeRed>BIOS/firmware password</font> to prevent unauthorized changes to system startup settings.
- Configure <font color=OrangeRed>Secure Boot</font> settings and set the device boot order to prevent unauthorized booting from alternate media.
- Enable <font color=OrangeRed>TPM (Trusted Platform Module)</font> to provide hardware-based integrity measurements and key storage.

### <font color="#fb02ff">5. User Account Policies and Access Control 用户账户策略与访问控制</font>

- Enforce <font color=OrangeRed>strong passwords</font> and account lockout policies via Group Policy.
- Apply <font color=OrangeRed>Advanced File Permissions</font> and Access Control to classify user rights precisely.

**Access Control Models 访问控制模型:**

| Model | Description |
|---|---|
| <font color=OrangeRed>RBAC (Role-Based)</font> | Access based on role membership; uses Group → User → Matrix assignment |
| <font color=OrangeRed>Rule-Based Access Control</font> | Access governed by ACL rules applied to resources |
| <font color=OrangeRed>ABAC (Attribute-Based)</font> | Access rules expressed in natural language using subject/object attributes |
| <font color=OrangeRed>DAC (Discretionary)</font> | Resource owner determines access — least restrictive |
| <font color=OrangeRed>MAC (Mandatory)</font> | Sensitivity labels matched to user clearance levels — most restrictive |

- Configure <font color="blue">Least Privilege</font> — every account receives only the permissions required for its function.
- <font color="#ecb8ff">Backdoors and privilege escalation</font> are the primary threats mitigated by strict account control.

### <font color="#fb02ff">6. Audit Policy and Change Management 审计策略与变更管理</font>

- Configure <font color=OrangeRed>audit policy settings</font> and event log retention to capture all security-relevant events.
- Implement a <font color="blue">change management process</font> to track all configuration changes with approval and rollback capability.

### <font color="#fb02ff">7. Additional Controls 其他控制</font>

- Disallow <font color=OrangeRed>remote registry access</font> if not required.
- Install and enable <font color=OrangeRed>anti-virus software</font> — provides detection against <font color="#ecb8ff">Trojans, worms, adware, spyware, and rootkits</font>.
- Use <font color="blue">virtualization and containers</font> to isolate workloads and limit the blast radius of a compromise.

### <font color="#fb02ff">8. Physical Security 物理安全</font>

- Control physical access to servers and networking equipment. Physical access bypasses most software-enforced controls.
- Use locked racks, access logs, and camera monitoring for all server rooms.

### <font color="#fb02ff">9. Attacks Mitigated by OS Hardening</font>

Many attack classes are directly mitigated by OS hardening:

| Attack | Mitigation |
|---|---|
| <font color="#ecb8ff">Logic bomb</font> | Application whitelisting, change management |
| <font color="#ecb8ff">Rootkit</font> | Secure Boot, TPM integrity checks, anti-virus |
| <font color="#ecb8ff">Ping of Death</font> | Disable ICMP, firewall rules |
| <font color="#ecb8ff">Privilege escalation</font> | Least privilege, RBAC, auditing |

---

## Enterprise Security 企业安全

### <font color="#fb02ff">1. Risk Assessment 风险评估</font>

| Type | Description |
|---|---|
| <font color=OrangeRed>Qualitative 定性</font> | Opinion-based and subjective; uses judgment and experience to prioritize risk |
| <font color=OrangeRed>Quantitative 定量</font> | Cost-based and objective; uses metrics and models |

**Quantitative formula 定量公式:**

> <font color="blue">SLE × ARO = ALE</font>
>
> - **SLE** (Single Loss Expectancy): cost of a single incident
> - **ARO** (Annual Rate of Occurrence): estimated frequency per year
> - **ALE** (Annual Loss Expectancy): expected annual financial impact

### <font color="#fb02ff">2. Risk Management 风险管理</font>

Five standard risk responses:

| Response | Description |
|---|---|
| <font color=OrangeRed>Risk Avoidance</font> | Stop the activity that creates the risk |
| <font color=OrangeRed>Risk Transference</font> | Transfer financial impact to a third party (e.g., insurance) |
| <font color=OrangeRed>Risk Acceptance</font> | Accept the risk when cost of mitigation exceeds impact |
| <font color=OrangeRed>Risk Mitigation</font> | Reduce likelihood or impact through controls |
| <font color=OrangeRed>Risk Deterrence</font> | Implement controls that discourage attackers (e.g., legal warnings) |

### <font color="#fb02ff">3. Policies, Standards, and Guidelines 策略、标准与指南</font>

| Document | Purpose |
|---|---|
| <font color="blue">Policy</font> | Provides people in an organization with guidance about expected behavior — privacy policy, acceptable use policy, mandatory vacations, job rotation, separation of duties, least privilege |
| <font color="blue">Standard</font> | Provides enough detail that an audit can determine whether it is being met |
| <font color="blue">Guideline</font> | Helps implement and maintain standards by describing how to accomplish policies |

- <font color="#ecb8ff">Social engineering and malicious insider threats</font> are the primary policy violations to guard against.

### <font color="#fb02ff">4. Disaster Recovery and Incident Response 灾难恢复与事件响应</font>

<font color=OrangeRed>Key components: different backup types, backup plans, and recovery site tiers.</font>

| Site Type | RTO | Cost |
|---|---|---|
| Hot site | Minutes | High — fully operational duplicate |
| Warm site | Hours | Medium — partially ready infrastructure |
| Cold site | Days | Low — space and power, no pre-loaded systems |

- Plan, test, and document backup and recovery procedures. An untested backup is not a backup.

---

## Network Controls 网络控制

### <font color="#fb02ff">OSI Model Mapping OSI模型控制映射</font>

Harden the network following the <font color=OrangeRed>CIA (Confidentiality, Integrity, Availability)</font> concept, applied at each OSI layer.

![OSI Model — 7 layers from Physical (Bits) to Application (Data), with Data/Layer columns showing PDU names at each layer](./assets/img/post/hardening-network-osi-model-layers.png)

| OSI Layer | Controls |
|---|---|
| <font color="blue">Layer 1 — Physical</font> | Physical access controls, cable security, hardware locks |
| <font color="blue">Layer 2 — Data Link</font> | Switch port security, MAC filtering, 802.1X, VLAN segmentation |
| <font color="blue">Layer 3 — Network</font> | Firewall, VPN, IDS/IPS, Honeypots, NAT/PAT, SSL/TLS, port blocking, routing control |
| <font color="blue">Layer 4 — Transport</font> | TCP/UDP session control, flow control, congestion control |
| <font color="blue">Layer 5 — Session</font> | SSH, RPC, NFS authentication |
| <font color="blue">Layer 6 — Presentation</font> | Encryption/decryption, data format validation |
| <font color="blue">Layer 7 — Application</font> | Application-layer firewalls, WAF, content filtering |

<font color=OrangeRed>Perform port blocking at the network level.</font> Analyze which ports must be open and restrict all others.

<font color=OrangeRed>Remove file and print sharing from network settings</font> unless explicitly required — file/print sharing can allow connection to a server without credentials.

---

### <font color="#fb02ff">Confidentiality Controls 机密性控制</font>

#### Cryptography and Encryption 加密

<font color="blue">Network-security mechanisms include firewalls, access control lists (ACL), and encryption protocols such as SSL/TLS</font> — which provide encryption for many protocols (HTTPS, FTPS, LDAPS).

#### Authentication Protocols 认证协议

##### Kerberos

<font color=OrangeRed>Kerberos</font> is a network authentication protocol using symmetric key cryptography and a trusted third party — the <font color="blue">Key Distribution Center (KDC)</font>.

**Ticket exchange flow:**

1. Client authenticates to the **Authentication Service (AS)** and receives a Ticket Granting Ticket (TGT).
2. Client presents the TGT to the **Ticket Granting Service (TGS)** to obtain a Service Ticket.
3. Client presents the Service Ticket to the target service to establish a session.

![Kerberos Ticket Exchange diagram — KDC with Authentication Service (AS) and Ticket Granting Service (TGS); user logs in, obtains TGT, exchanges for Service Ticket, then authenticates to network services](./assets/img/post/hardening-network-kerberos-ticket-exchange.png)

- Port: <font color="blue">TCP/UDP 88</font>
- Provides mutual authentication — both client and server verify identity.

##### RADIUS

<font color="blue">RADIUS (Remote Authentication Dial-In User Service)</font> centralizes authentication for remote connections.

| Property | Value |
|---|---|
| Transport | UDP |
| Primary use | Network access authentication |
| AAA model | Combines authentication and authorization |
| Encryption | Encrypts only the password field |

![RADIUS topology — Atlanta VPN, Virginia Beach VPN, and Chicago VPN all connecting to a central RADIUS Server, which queries an LDAP Server for user directory information](./assets/img/post/hardening-network-radius-ldap-topology.jpg)

##### TACACS+

<font color=OrangeRed>TACACS+ (Terminal Access Controller Access-Control System Plus)</font> is a Cisco-developed replacement for RADIUS with stronger separation of AAA functions.

| Property | RADIUS | TACACS+ |
|---|---|---|
| Transport | UDP | TCP (port 49) |
| Encryption | Password only | Full packet encryption |
| AAA model | Combined auth + authz | Separate authentication, authorization, accounting |
| Use case | Network access | Device administration |

<font color="blue">TACACS+ encrypts all authentication information</font>, making it more secure than RADIUS for device management.

![AAA with RADIUS and TACACS+ — Host with Cisco Trust Agent sends EAPoUDP/EAP802.1x credentials through Network Access Devices to AAA Server (ACS), which enforces posture validation and returns access rights or notification](./assets/img/post/hardening-network-aaa-radius-tacacs-flow.jpg)

---

### <font color="#fb02ff">Integrity Controls 完整性控制</font>

- <font color="blue">Backups</font>: maintain regular, tested backups to restore data integrity after incidents.
- <font color="blue">Checksums</font>: verify file and transfer integrity using cryptographic hashes (SHA-256).
- <font color="blue">Data correcting codes</font>: small changes can be detected and automatically corrected in storage systems.

### <font color="#fb02ff">Availability Controls 可用性控制</font>

- <font color="blue">Physical protections</font>: infrastructure (UPS, redundant power, climate control) to keep systems available during physical challenges.
- <font color="blue">Computational redundancies</font>: redundant hardware and tested backup systems for critical services.
- Use firewalls and routers to detect and prevent <font color=OrangeRed>DoS/DDoS attacks</font>.

---

## Database Hardening 数据库加固

### <font color="#fb02ff">1. Physical Database Server Security 物理安全</font>

- House the database server in a secured, locked, and monitored environment to prevent unauthorized entry, access, or theft.
- <font color=OrangeRed>Application/web servers must not be hosted on the same machine as the database server.</font>

### <font color="#fb02ff">2. Firewalls for Database Servers 防火墙</font>

- The database server sits behind a firewall with <font color=OrangeRed>default-deny rules</font>.
- Firewall rules allow access only from specific application or web servers. <font color=OrangeRed>Direct client access to the database port is never permitted.</font>

### <font color="#fb02ff">3. Database Software 数据库软件</font>

- Keep database software patched to the latest supported version.
- Disable all unused database features, stored procedures, and remote access options.
- Review and restrict the permissions of the database service account (principle of least privilege).

### <font color="#fb02ff">4. Application / Web Servers / Application Code</font>

- No spyware or unauthorized software is permitted on application, web, or database servers.
- Application code must enforce <font color=OrangeRed>server-side input validation</font> before any data reaches the database.

### <font color="#fb02ff">5. Accounts, Permissions, and Passwords 账户与权限</font>

- Rename or disable default administrator accounts.
- Create dedicated, least-privilege database accounts for each application.
- Enforce strong password policies for all database accounts.
- Regularly audit account permissions and remove unused accounts.

### <font color="#fb02ff">6. Protected Data 数据保护</font>

- Keep only the data required for the business function within the database — data minimization.
- Apply <font color=OrangeRed>hashing functions</font> to protected data elements (passwords, PINs) before storage when the data is only required for matching.
- <font color="#ecb8ff">Dictionary attacks</font> against password hashes are the primary threat — use salted, slow hashing algorithms (bcrypt, Argon2).

### <font color="#fb02ff">7. Change Management 变更管理</font>

- Document all changes to the database schema, stored procedures, and configuration.
- Change management procedures must meet the data proprietor's requirements and include rollback capability.

### <font color="#fb02ff">8. Database Auditing 数据库审计</font>

- Log all logins to OS and database servers — both successful and unsuccessful.
- <font color=OrangeRed>Retain logs for at least one year.</font>
- Store audit logs on a separate, protected system — not on the database server itself.

### <font color="#fb02ff">9. Database Backup and Recovery 备份与恢复</font>

- Implement regular automated backups with tested restore procedures.
- Store backup copies off-site or in a separate security zone.
- Verify backup integrity after each backup cycle.

### <font color="#fb02ff">10. Database Encryption and Key Management 加密与密钥管理</font>

- Encrypt data at rest for all tables containing sensitive or regulated data.
- Encrypt data in transit between the application server and the database (TLS).
- Store encryption keys in a dedicated key management system — not alongside the encrypted data.

### <font color="#fb02ff">11. Attack: SQL Injection SQL注入攻击</font>

<font color="#ecb8ff">SQL injection</font> is the primary application-layer threat to database servers. An attacker injects malicious SQL syntax through unvalidated input fields to manipulate the database.

**Mitigations:**

| Control | Description |
|---|---|
| <font color=OrangeRed>Parameterized queries / stored procedures</font> | Separate SQL logic from user-supplied data — the most effective defense |
| <font color=OrangeRed>Server-side input validation</font> | Filter and validate all input on the server, never trust client-side validation alone |
| <font color=OrangeRed>Proper error handling</font> | Return generic error pages — never expose SQL error details, table names, or stack traces to the user |
| <font color=OrangeRed>Least-privilege DB accounts</font> | Application account cannot DROP, ALTER, or access tables outside its scope |

---

## Meow's Security Considerations 安全注意事项

实施安全加固会创建新的配置状态和依赖关系，这些本身也可能成为攻击目标。以下涵盖加固过程中密钥管理、权限配置、认证协议和审计日志的核心安全风险。

Applying hardening creates new configuration state and trust dependencies that can themselves be targeted. The concerns below cover credential management, access control misconfiguration, authentication protocol weaknesses, and audit log integrity arising from the hardening procedures described in this note.

| Severity 严重程度 | Concern 问题 |
|---|---|
| Critical 严重 | Kerberos KDC compromise — Golden Ticket grants unlimited access to all services |
| High 高 | Incomplete or untested patch management leaves 0-day exposure |
| High 高 | SQL injection via missing parameterized queries bypasses all DB access controls |
| High 高 | RBAC misconfiguration grants excessive privileges — enables lateral movement |
| Medium 中 | BIOS/firmware password bypass via physical access (cold boot, flash reset) |
| Medium 中 | Audit log tampering — locally stored logs can be cleared by a compromised admin |
| Medium 中 | RADIUS password-only encryption exposes session tokens on the wire |
| Low 低 | Default LDAP/AD service accounts with weak passwords expose directory services |

---

### 1. Kerberos KDC Compromise — Golden Ticket 黄金票据攻击 — Critical

攻击者一旦控制Kerberos密钥分发中心（KDC），即可伪造任意用户的票据授予票据（TGT），即"黄金票据"。由于所有Kerberos票据均由KDC签发，黄金票据可绕过所有基于票据的认证，在整个域内横向移动，且难以被检测。

If an attacker compromises the Kerberos KDC — typically the Domain Controller — they can forge arbitrary Ticket Granting Tickets (TGTs) for any user. These "Golden Tickets" bypass all Kerberos-based authentication across the entire domain and are valid until the krbtgt account password is rotated.

**攻击向量 Attack Vectors:**

- KDC服务器遭受远程代码执行攻击，攻击者提取krbtgt账户的NTLM哈希 / Remote code execution on the KDC server; attacker extracts the krbtgt account NTLM hash
- 利用黄金票据在整个Active Directory域内横向移动，无需知道真实用户密码 / Golden Ticket used to move laterally across the entire AD domain without knowing real user passwords

**缓解措施 Mitigation:** 将KDC与其他服务器隔离，限制域控制器的管理访问，定期（至少每180天）轮换krbtgt账户密码，并监控异常票据请求（如非工作时间、非正常主机）。
Isolate the KDC from other workloads, restrict administrative access to Domain Controllers, rotate the krbtgt account password regularly (at minimum every 180 days), and monitor for anomalous ticket requests (unusual hours, unknown hosts). MITRE ATT&CK T1558.001.

---

### 2. Incomplete Patch Management 补丁管理不完整 — High

未及时应用的补丁使系统暴露于已知的CVE漏洞中。攻击者优先针对已发布补丁但尚未部署的漏洞——这类漏洞同时拥有公开的漏洞利用代码和大量未打补丁的目标。

Unpatched systems remain exposed to known CVE vulnerabilities. Attackers prioritize vulnerabilities for which a public patch exists but deployment is lagging — these have both published exploit code and a large pool of unpatched targets.

**攻击向量 Attack Vectors:**

- 利用公开的CVE漏洞对未打补丁的OS或应用发起远程代码执行攻击 / Exploiting public CVEs against unpatched OS or application components for remote code execution
- 0-day漏洞在补丁发布前无法通过补丁管理修复，需依赖网络分段和行为监控 / 0-day exploits cannot be addressed by patch management before a patch exists — rely on network segmentation and behavioral monitoring

**缓解措施 Mitigation:** 建立自动化补丁管理流程，在受控的沙盒环境中测试补丁后快速部署。对关键漏洞（CVSS ≥ 9.0）设置72小时内修补的SLA。
Establish automated patch management with sandbox testing before production deployment. Set an SLA of 72 hours for critical vulnerabilities (CVSS ≥ 9.0). CWE-1329.

---

### 3. SQL Injection via Missing Parameterized Queries SQL注入 — High

若应用程序代码未使用参数化查询或存储过程，用户输入会被直接拼接进SQL语句，攻击者可操控查询逻辑，绕过认证、提取数据，甚至执行OS命令。

If application code concatenates user-supplied input directly into SQL statements instead of using parameterized queries or stored procedures, attackers can manipulate query logic to bypass authentication, extract data, or execute OS-level commands via the database engine.

**攻击向量 Attack Vectors:**

- 在登录表单或搜索字段注入`' OR '1'='1`绕过认证 / Injecting `' OR '1'='1` into login forms or search fields to bypass authentication
- 使用`UNION SELECT`从其他表提取数据，或使用`xp_cmdshell`执行系统命令 / Using `UNION SELECT` to extract data from other tables, or `xp_cmdshell` to run OS commands

**缓解措施 Mitigation:** 所有数据库查询必须使用参数化查询或存储过程；服务器端验证所有输入；错误消息不得暴露数据库结构；定期进行代码审查和渗透测试。
All database queries must use parameterized queries or stored procedures; validate all input server-side; error messages must never expose database structure; conduct regular code review and penetration testing. CWE-89 / MITRE T1190.

---

### 4. RBAC Misconfiguration — Privilege Escalation 权限配置错误 — High

角色配置错误（权限过宽、遗留权限未清理、DAC所有者误操作）会使攻击者或恶意内部人员获得超出其职能所需的访问权限，进而进行横向移动或数据泄露。

Misconfigured roles — overly broad permissions, stale accounts with residual access, or DAC owners granting rights without oversight — allow attackers or malicious insiders to access resources beyond their function, enabling lateral movement or data exfiltration.

**攻击向量 Attack Vectors:**

- 利用残留的遗留账户（如已离职员工）进行未授权访问 / Exploiting residual legacy accounts (e.g., departed employees) for unauthorized access
- 向非特权账户授予过宽的共享角色权限 / Overly broad shared roles granting non-privileged accounts elevated access

**缓解措施 Mitigation:** 定期审计所有账户权限，实施职责分离，定期执行访问权限复查（每季度一次），并对特权账户操作启用审计日志。
Audit all account permissions regularly, enforce separation of duties, run quarterly access reviews, and enable audit logging for all privileged account actions. CWE-269 / MITRE T1078.

---

### 5. BIOS/Firmware Password Bypass 固件密码绕过 — Medium

设置BIOS密码后，拥有物理访问权限的攻击者仍可通过拆除CMOS电池重置密码，或通过外部启动介质绕过操作系统安全控制。固件级后门（如UEFI植入）比OS层检测更难发现。

A BIOS password prevents casual unauthorized changes, but an attacker with physical access can reset it by removing the CMOS battery or using manufacturer reset jumpers. External boot media bypasses OS-level access controls entirely. Firmware-level backdoors (UEFI implants) are harder to detect than OS-layer threats.

**缓解措施 Mitigation:** 将服务器置于上锁的机架和受监控的机房中；启用Secure Boot并验证固件签名；使用TPM进行启动完整性测量；记录并审计对物理基础设施的访问。
Place servers in locked racks and monitored rooms; enable Secure Boot and verify firmware signatures; use TPM for boot integrity measurements; log and audit all physical infrastructure access. MITRE T1542.

---

### 6. Audit Log Tampering 审计日志篡改 — Medium

若审计日志存储在被攻击的主机本地，具有管理员权限的攻击者可清除、修改或停用日志，抹去入侵痕迹。这直接破坏了事件响应和取证调查能力。

If audit logs are stored locally on the compromised host, an attacker with administrator access can clear, modify, or disable logging — erasing evidence of the intrusion. This directly undermines incident response and forensic investigation.

**缓解措施 Mitigation:** 将日志实时转发到集中式、只写的SIEM或日志服务器；对日志存储应用只追加权限；对日志完整性使用加密哈希链（如 syslog over TLS）。
Forward logs in real time to a centralized, append-only SIEM or log server; apply write-only permissions to log storage; use cryptographic hash chaining for log integrity (e.g., syslog over TLS). MITRE T1070.001.

---

### 7. RADIUS Password-Only Encryption RADIUS仅加密密码 — Medium

RADIUS仅加密认证数据包中的密码字段，其他属性（用户名、授权数据）以明文传输。在可以监听UDP流量的网络环境中，攻击者可通过流量分析获取用户名及会话元数据。

RADIUS encrypts only the password field in authentication packets; all other attributes — username, authorization data — are transmitted in cleartext over UDP. On networks where UDP traffic can be intercepted, an attacker can perform traffic analysis to harvest usernames and session metadata.

**缓解措施 Mitigation:** 在RADIUS和网络设备之间使用RadSec（RADIUS over TLS/DTLS）或将RADIUS迁移到TACACS+（对设备管理场景）；对所有认证流量强制执行网络分段和加密隧道。
Use RadSec (RADIUS over TLS/DTLS) between RADIUS and network devices, or migrate to TACACS+ for device administration; enforce network segmentation and encrypted tunnels for all authentication traffic. CWE-311.

---

### Summary Table 汇总表

| # | 问题 Concern | MITRE / CWE | 状态 Status |
|---|---|---|---|
| 1 | Kerberos KDC Compromise — Golden Ticket | MITRE T1558.001 | Mitigate: isolate KDC, rotate krbtgt |
| 2 | Incomplete Patch Management | CWE-1329 | Mitigate: automated patching, SLA |
| 3 | SQL Injection — Missing Parameterized Queries | CWE-89 / T1190 | Mitigate: parameterized queries |
| 4 | RBAC Misconfiguration — Privilege Escalation | CWE-269 / T1078 | Mitigate: access reviews, auditing |
| 5 | BIOS/Firmware Password Bypass | MITRE T1542 | Mitigate: physical controls, Secure Boot |
| 6 | Audit Log Tampering | MITRE T1070.001 | Mitigate: centralized SIEM, append-only |
| 7 | RADIUS Password-Only Encryption | CWE-311 | Mitigate: RadSec or TACACS+ |

---

## Key Takeaways

- <font color=OrangeRed>OS hardening starts at installation</font>: master images, service minimization, BIOS/Secure Boot/TPM, and least-privilege accounts — established before the system is connected to a network
- <font color=OrangeRed>CIS Benchmarks</font> provide measurable, auditable baselines for OS and application hardening
- <font color=OrangeRed>Access control models</font> range from most restrictive (MAC) to least restrictive (DAC) — choose based on the classification level of data handled
- <font color="blue">Quantitative risk: SLE × ARO = ALE</font> — use ALE to justify the cost of security controls
- <font color=OrangeRed>TACACS+ vs RADIUS</font>: TACACS+ encrypts the full packet and separates AAA — preferred for network device administration; RADIUS is lighter-weight and common for network access
- <font color=OrangeRed>Kerberos Golden Ticket</font> is the primary threat to Kerberos-based environments — KDC isolation and krbtgt rotation are the key mitigations
- <font color=OrangeRed>Database hardening</font>: database server must sit behind a firewall with default-deny rules, no direct client access, parameterized queries, and encrypted data at rest and in transit
- <font color="blue">Audit logs stored locally are untrustworthy</font> — forward to a centralized SIEM immediately

## References

- CompTIA Security+ objectives — OS hardening, risk management, access control models
- CISSP Chapter 13 — security controls and hardening
- CIS Benchmarks — configuration baselines for OS and application hardening
- MITRE ATT&CK — T1558 (Kerberos), T1078 (Valid Accounts), T1190 (Exploit Public-Facing App), T1542 (Pre-OS Boot), T1070 (Indicator Removal)
- CWE-89 (SQL Injection), CWE-269 (Privilege Management), CWE-311 (Missing Encryption), CWE-1329 (Reliance on Component Without Maintenance)
- CCNP 300-115 — AAA with RADIUS and TACACS+
