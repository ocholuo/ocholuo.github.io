---
title: Contents
icon: fas fa-compass
order: 5
---

- [Contents](#contents)
  - [How to read this site 如何阅读本站](#how-to-read-this-site-如何阅读本站)
  - [Folder map](#folder-map)

---

# Contents

This page maps every folder under `_posts/`: what each folder covers and how many notes it holds. Counts are approximate (as of 2026-11-15).

---

## How to read this site 如何阅读本站

Folders are grouped by topic and layer, not by source book. The numeric prefix sets the sort order:

- `0x` for foundations and code;
- `1x` for attack, concepts, cryptography and network security;
- `3x`-`5x` for systems, data and AI;

Most notes carry a `categories` field that follows their folder, so the folder names below are mostly also the category names on the [Categories](/categories/) page. Older notes are not fully consistent.

Start here:

- Learning a topic from scratch: read `00LearningPath/` first. It holds the pinned one-page guides.
- Preparing for an exam: go to `certification/`.
- Looking up an attack, a concept or a tool: go to `10CyberAttack/` or `10SecConcepts/`.
- Practising hands-on: go to `Lab/`.

---

## Folder map

Color key: <font color=MediumSeaGreen>**group**</font>, <font color=OrangeRed>**top-level folder**</font>, <font color=DodgerBlue>**second-level folder**</font>.

- <font color=MediumSeaGreen>**Foundations and code**</font>
  - <font color=OrangeRed>**00AGeneralNote**</font> — General notes (about 4)
    - Mixed everyday reference that fits no technical domain, such as hardware basics (screws, bearings), a glossary appendix and work commands.
  - <font color=OrangeRed>**00Basic**</font> — Engineering basics (about 30)
    - <font color=DodgerBlue>**90DevPortal**</font>: Developer portals and small app deployments (Backstage, Flask).
    - <font color=DodgerBlue>**API**</font>: API frameworks (FastAPI).
    - <font color=DodgerBlue>**AppEng**</font>: Application engineering: Spring Boot, data-intensive design, App Mesh, Terraform.
    - <font color=DodgerBlue>**Auth**</font>: Authentication, identity management, third-party vendors.
    - <font color=DodgerBlue>**Database**</font>: Databases (Redis so far).
    - <font color=DodgerBlue>**ELK**</font>: Elastic stack and Kafka.
    - <font color=DodgerBlue>**Network**</font>: DNS, DNS security, API gateways.
    - <font color=DodgerBlue>**VMandContainer**</font>: Virtualization, containers, Docker security.
  - <font color=OrangeRed>**00CodeNote**</font> — Code notes (about 207)
    - <font color=DodgerBlue>**0.DS**</font>: Data structures and algorithms (recursion, sorting, trees).
    - <font color=DodgerBlue>**0.Leetcode**</font>: Coding-problem practice.
    - <font color=DodgerBlue>**AIML**</font>: Machine-learning labs.
    - <font color=DodgerBlue>**CodeUsecase**</font>: Small scripts for real tasks, such as web scraping.
    - <font color=DodgerBlue>**Cybrary**</font>: Course notes.
    - <font color=DodgerBlue>**Interview**</font>: Coding interview questions.
    - <font color=DodgerBlue>**language**</font>: Per-language notes (Go, Python and its libraries, testing). The largest folder.
    - <font color=DodgerBlue>**Linux**</font>: Linux Foundation certification (LFCE) topics.
    - <font color=DodgerBlue>**project**</font>: Notes on personal projects.
    - <font color=DodgerBlue>**SourceMangr**</font>: Git and GitHub, including stacked PRs and squash merge.
    - <font color=DodgerBlue>**SystemDesign**</font>: System design and distributed systems.
    - <font color=DodgerBlue>**terraform**</font>: Infrastructure as code with Terraform.
  - <font color=OrangeRed>**00LearningPath**</font> — Learning paths (about 13)
    - Pinned one-page guides (InfoSec, Web, Code, Course) sit at the folder root.
    - <font color=DodgerBlue>**conference**</font>: Conference notes.
    - <font color=DodgerBlue>**courses**</font>: Course notes (operating-systems chapters, network performance).

- <font color=MediumSeaGreen>**Cloud**</font>
  - <font color=OrangeRed>**01Cloud**</font> — Cloud platforms (about 184)
    - Cloud models and service types sit at the folder root.
    - <font color=DodgerBlue>**01AWS**</font>: AWS services, CLI, security and patch management. The second-largest folder.
    - <font color=DodgerBlue>**01GCP**</font>: Google Cloud services, build and registry tooling.
    - <font color=DodgerBlue>**01Ali**</font>: Alibaba Cloud: CLI, security center, load balancing.

- <font color=MediumSeaGreen>**Security**</font>
  - <font color=OrangeRed>**02Security**</font> — Security tooling and monitoring (about 9)
    - Security tools (Falco, cloud security tools) sit at the folder root.
    - <font color=DodgerBlue>**conference**</font>: Conference notes.
    - <font color=DodgerBlue>**Prometheus**</font>: Prometheus monitoring.
  - <font color=OrangeRed>**10CyberAttack**</font> — Attacks and attack tools (about 81)
    - <font color=DodgerBlue>**0ApplicationServerAttacks**</font>: Attack types: replay, SYN flood, ICMP, sinkholing and more.
    - <font color=DodgerBlue>**AttackTools**</font>: Tools: Burp Suite, Hydra, John the Ripper and more.
    - <font color=DodgerBlue>**securityEvent**</font>: Case studies of real incidents.
    - <font color=DodgerBlue>**SocialEngineering**</font>: Phishing, vishing, pharming.
    - <font color=DodgerBlue>**Spoofing**</font>: ARP and IP spoofing.
    - <font color=DodgerBlue>**vulnerability**</font>: Specific vulnerabilities and malware scripts.
  - <font color=OrangeRed>**10SecConcepts**</font> — Security concepts and frameworks (about 28)
    - Threat models, CMMI and tenancy sit at the folder root.
    - <font color=DodgerBlue>**Attack**</font>: Cyber kill chain, MITRE ATT&CK, OWASP Top 10 with CWE.
    - <font color=DodgerBlue>**Compliance**</font>: SOX, NIST, CIS controls, child privacy.
    - <font color=DodgerBlue>**OWASP**</font>: Reserved for OWASP material. Empty for now.
    - <font color=DodgerBlue>**PenTest**</font>: Secure coding.
    - <font color=DodgerBlue>**SoftwareSupplyChain**</font>: SonarQube, Semgrep, CycloneDX.
    - <font color=DodgerBlue>**Vulnerability**</font>: Vulnerability management, CVE and NVD.
  - <font color=OrangeRed>**13Crypt**</font> — Cryptography (about 14)
    - Asymmetric encryption, hashing and SSL/TLS sit at the folder root.
    - <font color=DodgerBlue>**cipher-code**</font>: Ciphers and codes.
    - <font color=DodgerBlue>**PKI**</font>: Digital signatures and PKI.
    - <font color=DodgerBlue>**TrustedDevicesAndPlatforms**</font>: TPM and hardware trust.
  - <font color=OrangeRed>**15NetworkSec**</font> — Network fundamentals (about 13)
    - <font color=DodgerBlue>**NetworkBasic**</font>: VLAN, Ethernet and basic labs.
    - <font color=DodgerBlue>**NetworkProtocol**</font>: Protocols: TLS handshake, HTTP status codes.
    - <font color=DodgerBlue>**OSIModel**</font>: OSI layers, IP, routing, autonomous systems.
  - <font color=OrangeRed>**16NetworkSecII**</font> — Network security (about 11)
    - <font color=DodgerBlue>**AdvancedSecurityDevices**</font>: IDS, IPS, IDS evasion, Calico.
    - <font color=DodgerBlue>**NetworkAttacks**</font>: Confidentiality and availability attacks, physical disturbances.
    - <font color=DodgerBlue>**Scraping**</font>: Web scraping.
  - <font color=OrangeRed>**18DefendSec**</font> — Defense (about 2)
    - Security hardening sits at the folder root.
    - <font color=DodgerBlue>**ControlType**</font>: Control types.
  - <font color=OrangeRed>**SOC**</font> — Security operations (about 27)
    - Splunk, Nessus and interview prep sit at the folder root.
    - <font color=DodgerBlue>**PaloAltoNetwork**</font>: Prisma, AutoFocus. The largest sub-folder.
    - <font color=DodgerBlue>**FireEye**</font>: FireEye notes.
    - <font color=DodgerBlue>**IBM-Cybersecurity-Analyst-Professional-Certificate**</font>: IBM course notes and quizzes.
    - <font color=DodgerBlue>**PenTest**</font>: Web application penetration testing.
  - <font color=OrangeRed>**Web**</font> — Web technology and security (about 24)
    - CORS, robots and web application penetration testing sit at the folder root.
    - <font color=DodgerBlue>**html**</font>: HTML, lists, tables, styling, PHP.
    - <font color=DodgerBlue>**HTTP**</font>: HTTP, headers, status codes, retry.
    - <font color=DodgerBlue>**JavaScript**</font>: JavaScript, forms, getting started with the web.

- <font color=MediumSeaGreen>**Systems, data and AI**</font>
  - <font color=OrangeRed>**30System**</font> — Operating systems (about 62)
    - <font color=DodgerBlue>**Linux**</font>: Commands, files, cron, sockets, vim. The bulk of the folder.
    - <font color=DodgerBlue>**docker**</font>: Docker install, images, basics.
    - <font color=DodgerBlue>**Mac**</font>: Terminal notes, local HTTPS.
    - <font color=DodgerBlue>**Win**</font>: Windows (LOLBins).
    - <font color=DodgerBlue>**VirtualBox**</font>: VirtualBox install and setup.
    - <font color=DodgerBlue>**servicenow**</font>, <font color=DodgerBlue>**other**</font>: ServiceNow and miscellaneous.
  - <font color=OrangeRed>**50BigData**</font> — Big data (about 7)
    - Trino, MongoDB and MongoDB X.509 authentication sit at the folder root.
    - <font color=DodgerBlue>**public_dataset**</font>: Empty for now.
  - <font color=OrangeRed>**51AI**</font> — AI and machine learning (about 45)
    - <font color=DodgerBlue>**AIML**</font>: General AI and ML, NER, LLM vulnerability detection.
    - <font color=DodgerBlue>**LLM**</font>: LLM security, pretraining, evaluation.
    - <font color=DodgerBlue>**LLMApps**</font>: Vibe coding, security scanners, knowledge bases.
    - <font color=DodgerBlue>**AIAttack**</font>: AI attack surfaces (MCP security).
    - <font color=DodgerBlue>**CLAUDE**</font>: Claude skills and agents.
    - <font color=DodgerBlue>**CNN**</font>: Convolutional networks.
    - <font color=DodgerBlue>**Paper**</font>: Paper reading notes.
    - <font color=DodgerBlue>**Prompts**</font>, <font color=DodgerBlue>**Tool**</font>: Prompt collections and AI tools.

- <font color=MediumSeaGreen>**Practice and exams**</font>
  - <font color=OrangeRed>**Lab**</font> — Labs and CTF (about 35)
    - <font color=DodgerBlue>**htb**</font>: Hack The Box. The largest sub-folder.
    - <font color=DodgerBlue>**Burp**</font>, <font color=DodgerBlue>**CloudCTF**</font>, <font color=DodgerBlue>**CTF**</font>, <font color=DodgerBlue>**ITgame**</font>, <font color=DodgerBlue>**NDG**</font>, <font color=DodgerBlue>**SEEDLab**</font>, <font color=DodgerBlue>**theForage**</font>, <font color=DodgerBlue>**Tryhackme**</font>: Tool-, platform- and course-specific labs.
    - <font color=DodgerBlue>**otw**</font>: OverTheWire.
    - <font color=DodgerBlue>**01hacklab**</font>: Empty for now.
  - <font color=OrangeRed>**certification**</font> — Exam prep (about 9)
    - <font color=DodgerBlue>**AWS**</font>: Solutions Architect, Cloud Practitioner, Developer Associate Q&A.
    - <font color=DodgerBlue>**CISSP**</font>: CISSP chapters and Q&A.
    - <font color=DodgerBlue>**CompTIA_Security+**</font>: Security+ book summary, index, chapters.
