---
title: "Meow's General - CyberSec Appendix A"
date: 2018-05-21 11:11:11 -0400
categories: [00AGeneralNote, Security+]
tags: [glossary, security+, terminology, cryptography, network-security, certification]
math: false
toc: true
image:
---

# CyberSec Appendix A

- [CyberSec Appendix A](#cybersec-appendix-a)
  - [Overview](#overview)
  - [Number](#number)
  - [A](#a)
  - [B](#b)
  - [C](#c)
  - [D](#d)
  - [E](#e)
  - [F](#f)
  - [G](#g)
  - [H](#h)
  - [I](#i)
  - [J](#j)
  - [K](#k)
  - [L](#l)
  - [M](#m)
  - [N](#n)
  - [O](#o)
  - [P](#p)
  - [Q](#q)
  - [R](#r)
  - [S](#s)
  - [T](#t)
  - [U](#u)
  - [V](#v)
  - [W](#w)
  - [X](#x)
  - [Z](#z)
  - [Key Takeaways](#key-takeaways)
  - [References](#references)

---

## Overview

A comprehensive A-Z glossary of CompTIA Security+ terminology. Terms in <font color=OrangeRed>red</font> are key defined terms. Terms in <font color=blue>blue</font> are core concepts or related references. Terms in <font color=DarkOrange>orange</font> are comparison targets.

---

## Number

- <font color=OrangeRed>**3DES**</font>—Triple Digital Encryption Standard. A symmetric algorithm used to encrypt data and provide confidentiality. Block cipher, encrypts data in **64-bit blocks**.

---

## A

- <font color=OrangeRed>**AAA**</font>—Authentication, authorization, accounting. A group of technologies used in remote access systems.
  - <font color=DarkOrange>Authentication</font> verifies a user's <font color=blue>identification</font>.
  - <font color=DarkOrange>Authorization</font> determines if a user should have <font color=blue>access</font>.
  - <font color=DarkOrange>Accounting</font> tracks / records a user's access / activity with logs. One method is <font color=blue>audit logs</font> that create an audit trail.
  - Sometimes called AAAs of security.

- <font color=OrangeRed>**ABAC**</font>—Attribute-based access control. An access control model that grants access to resources based on attributes assigned to subjects and objects. <font color=blue>Uses policies.</font>

- <font color=OrangeRed>**Acceptable use policy (AUP)**</font>—A policy defining <font color=blue>proper system usage and the rules</font> of behavior for employees. Describes the <font color=blue>purpose</font> of computer systems and networks, how users can access them, and the <font color=blue>responsibilities</font> of users.

- <font color=OrangeRed>**Access point (AP)**</font>—A device that connects wireless clients to wireless networks. Also called <font color=blue>wireless access point (WAP)</font>.

- <font color=OrangeRed>**accounting**</font>—The process of tracking the activity of users and recording this activity in logs. One method is audit logs that create an audit trail.

- <font color=OrangeRed>**ACLs**</font>—Access control lists. Lists of rules used by routers and stateless firewalls. Control traffic based on networks, subnets, IP addresses, ports, and protocols.

- <font color=OrangeRed>**active reconnaissance**</font> /rɪ'kɒnɪs(ə)ns/—A penetration testing method. Sends data to systems and analyzes responses to gain information on the target. Compare with <font color=blue>passive reconnaissance</font>.

- <font color=OrangeRed>**ad hoc mode**</font> 無線隨意網路—A <font color=blue>connection mode</font> where wireless devices connect to each other without an AP.
  - <font color=blue>infrastructure mode</font>: wireless devices connect through an AP.

- <font color=OrangeRed>**administrative controls**</font>—Security controls implemented via <font color=blue>administrative or management methods</font>.

- <font color=OrangeRed>**AES**</font>—Advanced Encryption Standard. A strong symmetric block cipher that encrypts data in **128-bit blocks**. Key sizes: 128, 192, or 256 bits.

- <font color=OrangeRed>**Affinity**</font> 姻亲关系；类同—A scheduling method used with <font color=blue>load balancers</font>. Uses the client's IP address to ensure the client is redirected to the **same server** during a web session.
  - <font color=DarkOrange>round-robin</font>: allows a load balancer to send requests to servers one after another.

- <font color=OrangeRed>**Aggregation switch**</font>—A switch used to connect multiple switches together into a network. Switches connect to the aggregation switch → connects to a router.

- <font color=OrangeRed>**Agile**</font> /'ædʒaɪl/—A <font color=blue>software development life cycle model</font> that focuses on <font color=blue>interaction</font> between customers, developers, and testers. Compare with <font color=DarkOrange>waterfall</font>.

- <font color=OrangeRed>**AH**</font>—Authentication Header. An option within IPsec to provide **authentication and integrity**.

- <font color=OrangeRed>**Airgap**</font>—A <font color=blue>physical</font> security control, provides physical isolation. Systems separated by an airgap don't have physical connections to other systems.

- <font color=OrangeRed>**ALE**</font>—Annual (annualized) loss expectancy /'ɪk'spekt(ə)nsɪ/. The expected loss for a year. Used to measure risk with ARO and SLE in a <font color=blue>quantitative /'kwɒntɪ,tətɪv/ risk assessment</font>. Calculation: **SLE × ARO = ALE**.

- <font color=OrangeRed>**amplification attack**</font>—An attack that increases <font color=blue>the amount of bandwidth</font> sent to a victim.

- <font color=OrangeRed>**Anomaly**</font> 不规则—A type of monitoring on IDS/IPS systems. Detects attacks by comparing operations against a <font color=blue>baseline</font>. Also known as <font color=blue>heuristic /ˌhjʊ(ə)'rɪstɪk/ detection</font>.

- <font color=OrangeRed>**ANT**</font>—A proprietary /prə'praɪət(ə)rɪ/ wireless protocol used by some mobile devices. Not an acronym.

- <font color=OrangeRed>**antispoofing**</font>—A method on some routers to protect against spoofing attacks. Implements specific rules to block certain traffic.

- <font color=OrangeRed>**antivirus**</font>—Software that protects systems from malware. Protects against viruses, Trojans, worms, and more.

- <font color=OrangeRed>**application blacklist**</font>—A list of applications that a system blocks. Users are unable to install or run any applications on the list.

- <font color=OrangeRed>**application cell / application containers**</font>—A virtualization technology that runs services or applications within isolated containers. Each container shares the kernel of the host.

- <font color=OrangeRed>**application whitelist**</font>—A list of applications that a system allows. Users are only able to install or run applications on the list.

- <font color=OrangeRed>**APT**</font>—Advanced persistent threat. A group that has both the capability and intent to launch sophisticated and targeted attacks.

- <font color=OrangeRed>**ARO**</font>—Annual (annualized) rate of occurrence. The number of times a loss is expected to occur in a year. Used with ALE and SLE in a quantitative risk assessment.

- <font color=OrangeRed>**arp**</font>—A command-line tool used to show and manipulate the Address Resolution Protocol (ARP) cache.

- <font color=OrangeRed>**ARP poisoning**</font>—An attack that misleads systems about the actual MAC address of a system.

- <font color=OrangeRed>**asset value**</font>—An element of a risk assessment. Identifies the value of an asset — monetary or subjective.

- <font color=OrangeRed>**asymmetric encryption**</font>—A type of encryption using two keys to encrypt and decrypt data. Uses a **public key** and a **private key**. Compare with <font color=DarkOrange>symmetric encryption</font>.

- <font color=OrangeRed>**attestation**</font>—A process that checks and validates system files during the boot process. TPMs sometimes use <font color=blue>remote attestation</font>, sending a report to a remote system.

- <font color=OrangeRed>**audit trail**</font> 足迹—A record of events recorded in one or more logs. Security professionals can re-create events that occurred leading up to a security incident.

- <font color=OrangeRed>**authentication**</font>—The process that occurs when a user <font color=blue>proves an identity</font>, such as with a password.

- <font color=OrangeRed>**authorization**</font>—The process of <font color=blue>granting access to resources for users</font> who prove their identity, based on their proven identity.

- <font color=OrangeRed>**availability**</font>—One of the three main goals of the CIA security triad. Ensures systems and data are up and operational when needed. Compare with <font color=DarkOrange>confidentiality</font> and <font color=DarkOrange>integrity</font>.

---

## B

- <font color=OrangeRed>**backdoor**</font>—An alternate method of accessing a system. Malware often adds a backdoor after it infects a system.

- <font color=OrangeRed>**background check**</font>—A check into a person's history, typically to determine eligibility /ˌelidʒə'biləti/ for a job.

- <font color=OrangeRed>**Backscatter analysis of DoS Attack**</font>—Backscatter 本意是用來指涉反向散射的電磁波, 粒子或者訊號. 對於阻斷服務攻擊, 攻擊者經常<font color=blue>修改封包當中的來源位址</font>並送給網路中想要攻擊的對象, 被攻擊的機器無法分辨此來源位址的真偽而根據協定內容將回應封包傳送給此來源位址, <font color=blue>此回應的封包即稱為</font> <font color=blue>backscatter</font>. 藉著分析這些回應封包的來源位址可定序阻斷服務攻擊的特徵值, 此之謂 backscatter analysis.

- <font color=OrangeRed>**banner grabbing**</font>—A method used to gain information about a remote system. Identifies the operating system and other details on the remote system.

- <font color=OrangeRed>**bcrypt**</font>—A key stretching algorithm. Protects passwords by <font color=blue>salting passwords with additional bits before encrypting them with Blowfish</font>. Thwarts /θwɔːt/ <font color=DarkOrange>rainbow table attacks</font>.

- <font color=OrangeRed>**BIOS**</font>—Basic Input/Output System. A computer's firmware used to manipulate settings (date/time, boot drive, access password). <font color=DarkOrange>UEFI</font> is the designated /'dɛzɪg,net/ replacement.

- <font color=OrangeRed>**birthday**</font>—A <font color=blue>password attack</font> named after the <font color=DarkOrange>birthday paradox</font> /'pærədɒks/ 悖论 in probability theory. The paradox states that for any random group of 23 people, there is a 50% chance that 2 share a birthday.

- <font color=OrangeRed>**black box test**</font>—A type of <font color=blue>penetration test</font>. Testers have **zero** knowledge of the environment. Compare with <font color=DarkOrange>gray box test</font> and <font color=DarkOrange>white box test</font>.

- <font color=OrangeRed>**block cipher**</font>—An encryption method that encrypts data in fixed-sized blocks. Compare with <font color=DarkOrange>stream cipher</font>.

- <font color=OrangeRed>**Blowfish**</font>—A strong <font color=blue>symmetric block cipher</font>. Encrypts data in 64-bit blocks, key sizes 32–448 bits. Compare with <font color=DarkOrange>Twofish</font>.

- <font color=OrangeRed>**bluejacking**</font>—Attack against Bluetooth: sending unsolicited /ʌnsə'lɪsɪtɪd/ messages to nearby Bluetooth devices.

- <font color=OrangeRed>**bluesnarfing**</font>—Attack against Bluetooth: unauthorized access to Bluetooth devices, can access all data on the device.

- **Bluesmacking** 猛烈地: simple <font color=blue>denial-of-service attack</font> against the device.

- **Bluesniffing**: to <font color=blue>discover Bluetooth-enabled devices</font>, like war driving in wireless hacking.

- **Bluebugging**: Successfully accessing a Bluetooth-enabled device and <font color=blue>remotely using its features</font>. Gaining full access to the phone, the attacker installs a backdoor. Can listen in on phone conversations, enable call forwarding, send messages.

- **Blueprinting**: footprinting for Bluetooth — involves collecting device info over Bluetooth.

- <font color=OrangeRed>**bollards**</font> /'bɒlɑːd/—Short vertical posts that act as a barricade /ˌbærɪ'keɪd/. Block vehicles but not people.

- <font color=OrangeRed>**bots**</font>—Software robots that function automatically. A botnet is a group of computers joined together. Attackers use malware to join computers to a botnet and use it to launch attacks.

- <font color=OrangeRed>**BPA**</font>—Business partners agreement. A written agreement detailing the relationship between business partners, including their obligations.

- <font color=OrangeRed>**bridge**</font>—A network device used to connect multiple networks together. Can be used instead of a router in some situations.

- <font color=OrangeRed>**brute force**</font>—A <font color=blue>password attack</font> that attempts to guess a password.
  - Online brute force attacks guess passwords of online systems.
  - Offline attacks guess passwords contained in a file or database.

- <font color=OrangeRed>**buffer overflow**</font>—An error that occurs when an application receives more input, or different input, than it expects. Exposes system memory that is normally inaccessible.

- <font color=OrangeRed>**business impact analysis (BIA)**</font> /ə'nælɪsɪs/—A process that helps an organization identify critical systems and components essential to the organization's success.

- <font color=OrangeRed>**BYOD**</font>—Bring your own device. A mobile device deployment model. Employees connect their personally owned device to the network. Compare with <font color=DarkOrange>COPE</font> (corporate-owned, personally enabled) and <font color=DarkOrange>CYOD</font> (choose your own device).

---

## C

- <font color=OrangeRed>**CA**</font>—Certificate Authority. An organization that <font color=DarkOrange>manages, issues, and signs certificates</font>. A CA is a main element of a PKI.

- <font color=OrangeRed>**CAC**</font>—Common Access Card. A specialized smart card used by the U.S. Department of Defense. Includes photo identification and provides confidentiality, integrity, authentication, and non-repudiation.

- <font color=OrangeRed>**Captive portal**</font> 俘虏入口—A technical solution that forces wireless clients <font color=blue>using web browsers to complete a process</font> before accessing a network. Often used to ensure users agree to an AUP or pay for access.

- <font color=OrangeRed>**carrier unlocking**</font>—The process of unlocking a mobile phone from a specific cellular /'seljʊlə/ provider.

- <font color=OrangeRed>**CBC**</font>—Cipher Block Chaining. A mode of operation that effectively <font color=blue>converts a block cipher into a stream cipher</font>. Uses an initialization vector (IV) for the first block; each subsequent block is XOR'd with the previous ciphertext block.

![CBC encryption chain showing IV XOR with plaintext blocks and chained ciphertext output](./assets/img/post/crypto-cbc-encryption-chain.png)

![CBC decryption chain showing chained ciphertext blocks XOR'd with decrypted output](./assets/img/post/crypto-cbc-decryption-chain.png)

- <font color=OrangeRed>**CCMP**</font>—Counter Mode with Cipher Block Chaining Message Authentication Code Protocol. Encryption protocol <font color=blue>based on AES and used with WPA2</font>. More secure than <font color=DarkOrange>TKIP</font>.

- <font color=OrangeRed>**CER**</font>—Canonical Encoding Rules /kə'nɒnɪk(ə)l/ 权威的. A base format for PKI certificates. <font color=blue>Binary encoded files</font>. Compare with <font color=DarkOrange>DER (Distinguished Encoding Rules)</font>.

- <font color=OrangeRed>**certificate**</font>—A digital file used for encryption, authentication, digital signatures, and more. <font color=blue>Public certificates</font> include a public key used for asymmetric encryption.

- <font color=OrangeRed>**certificate chaining**</font>—A process that <font color=blue>combines all certificates within a trust model</font>. Includes all certificates in the <font color=blue>trust chain</font> from the root CA down to the end user.

- <font color=OrangeRed>**chain of custody**</font> /'kʌstədɪ/—A process that provides assurances that evidence has been controlled and handled properly after collection.

- <font color=OrangeRed>**change management**</font>—The process used to prevent unauthorized changes. Unauthorized changes often result in unintended outages.

- <font color=OrangeRed>**CHAP**</font>—Challenge Handshake Authentication Protocol. An <font color=blue>authentication mechanism</font> where a server challenges a client. Compare with <font color=DarkOrange>MS-CHAPv2</font> and <font color=DarkOrange>PAP</font>.

- <font color=OrangeRed>**chroot**</font>—A Linux command used to change the root directory. Often used for <font color=blue>sandboxing</font>.

- <font color=OrangeRed>**ciphertext**</font>—The result of encrypting plaintext. Not in readable format until decrypted.

- <font color=OrangeRed>**clean desk policy**</font>—A <font color=blue>security policy</font> requiring employees to keep areas organized and free of papers. Reduces threats by protecting sensitive data.

- <font color=OrangeRed>**clickjacking**</font>—An attack that tricks users into clicking something other than what they think they're clicking, using multiple transparent or opaque layers.

- <font color=OrangeRed>**Clipping level**</font>—Sets certain thresholds 门槛 for specific errors or mistakes allowed and the amount of these occurrences that can take place before it is considered suspicious.

- <font color=OrangeRed>**Cloud access security broker (CASB)**</font>—A software tool or service that enforces cloud-based security requirements. Placed between the organization's resources and the cloud, monitors all network traffic, and can enforce security policies.

- <font color=OrangeRed>**cloud deployment models**</font>—Cloud model types that identify who has access to cloud resources.
  - <font color=blue>Public clouds</font>: for any organization.
  - <font color=blue>Private clouds</font>: for a single organization.
  - <font color=blue>Community clouds</font>: shared among community organizations.
  - <font color=blue>Hybrid cloud</font>: a combination of two or more clouds.

- <font color=OrangeRed>**code signing**</font>—The process of assigning a certificate to code. The certificate includes a digital signature and validates the code.

- <font color=OrangeRed>**cold site**</font>—An alternate location for operations. Has power and connectivity needed for activation, but little else. Compare with <font color=DarkOrange>hot site</font> and <font color=DarkOrange>warm site</font>.

- <font color=OrangeRed>**collision**</font>—A hash vulnerability. A hash collision occurs when two different passwords create the same hash.

- <font color=OrangeRed>**compensating controls**</font>—<font color=blue>Security controls</font> that are alternative controls used when a primary security control is not feasible.

- <font color=OrangeRed>**compiled code**</font>—Code that has been optimized and converted into an executable file. Compare with <font color=DarkOrange>runtime code</font>.

- <font color=OrangeRed>**confidential data**</font>—Data meant to be kept secret among a certain group of people.

- <font color=OrangeRed>**confidentiality**</font>—One of the three main goals of the <font color=blue>CIA security triad</font>.
  - Ensures unauthorized entities cannot access data.
  - <font color=blue>Encryption</font> and <font color=blue>access controls</font> help protect confidentiality.
  - Compare with <font color=DarkOrange>availability</font> and <font color=DarkOrange>integrity</font>.

- <font color=OrangeRed>**configuration compliance scanner**</font>—A type of <font color=blue>vulnerability scanner</font> that verifies systems are configured correctly.

- <font color=OrangeRed>**confusion**</font>—A cryptography concept indicating ciphertext is significantly different than plaintext.

- <font color=OrangeRed>**containerization**</font>—A method used to <font color=blue>isolate applications in mobile devices</font>. Isolates and protects the application, including data.

- <font color=OrangeRed>**context-aware authentication**</font>—An authentication method <font color=blue>using multiple elements to authenticate a user and a mobile device</font>. Can include identity, geolocation, device type, and more.

- <font color=OrangeRed>**continuity of operations planning**</font>—The <font color=blue>planning process</font> that identifies an alternate location for operations after a critical outage. Can include <font color=DarkOrange>hot site, cold site,</font> or <font color=DarkOrange>warm site</font>.

- <font color=OrangeRed>**control diversity**</font>—The use of different security control types: <font color=blue>technical controls, administrative controls, and physical controls</font>. Compare with <font color=DarkOrange>vendor diversity</font>.

- <font color=OrangeRed>**controller-based AP / thin AP**</font>—An AP that is <font color=blue>managed by a controller</font>. Compare with <font color=DarkOrange>fat AP</font>.

- <font color=OrangeRed>**COPE**</font>—Corporate-owned, personally enabled. A <font color=blue>mobile device deployment model</font>. The organization purchases and issues devices to employees. Compare with <font color=DarkOrange>BYOD</font> and <font color=DarkOrange>CYOD</font>.

- <font color=OrangeRed>**corrective controls**</font>—Security controls that attempt to reverse the impact of a security incident.

- <font color=OrangeRed>**CRL**</font>—Certificate revocation list. A list of certificates that a CA has revoked. Revoked when compromised or issued to an employee who has left.

- <font color=OrangeRed>**crossover error rate**</font>—The point where the <font color=DarkOrange>false acceptance rate (FAR)</font> crosses over with the <font color=DarkOrange>false rejection rate (FRR)</font>. A lower CER indicates a more accurate biometric system.

- <font color=OrangeRed>**cross-site request forgery (XSRF)**</font> /'fɔːdʒ(ə)rɪ/—A <font color=blue>web application attack</font>. Tricks users into performing actions on web sites without their knowledge.

- <font color=OrangeRed>**cross-site scripting (XSS)**</font>—A <font color=blue>web application vulnerability</font>. Attackers embed malicious HTML or JavaScript into a web site's code, which executes when a user visits the site.

- <font color=OrangeRed>**crypto-malware**</font>—A type of <font color=blue>ransomware</font> 勒索软件 that encrypts the user's data.

- <font color=OrangeRed>**crypto module**</font>—A <font color=blue>set of hardware, software, and/or firmware</font> that implements cryptographic functions. Compare with <font color=DarkOrange>crypto service provider</font>.

- <font color=OrangeRed>**crypto service provider**</font>—A <font color=blue>software library</font> of cryptographic standards and algorithms. Typically distributed within crypto modules.

- <font color=OrangeRed>**CSR**</font>—Certificate signing request. A method of <font color=blue>requesting a certificate from a CA</font>. Creates an RSA-based private/public key pair and includes the public key in the CSR.

- <font color=OrangeRed>**CTM / Counter mode**</font>—A mode of encryption that combines an IV with a counter. The combined result is used to encrypt blocks.
  - <font color=blue>Combines an initialization vector (IV) with a counter</font> to effectively convert a block cipher into a stream cipher.
  - Generates a keystream block by encrypting sequential values of a counter.
  - Each block uses the same IV but CTM combines it with the counter value, resulting in a different encryption key per block.
  - Multiprocessor systems can encrypt/decrypt multiple blocks simultaneously — <font color=blue>quicker on multiprocessor or multicore systems</font>.
  - CTM is widely used and respected as a secure mode of operation.

- <font color=OrangeRed>**GCM**</font>—Galois/Counter Mode. Combines the Counter mode with hashing techniques for <font color=blue>data authenticity and confidentiality</font>.

- <font color=OrangeRed>**ECB**</font>—Electronic Codebook. The simplest mode of operation. **Not recommended.**
  - Uses the algorithm without any modification.
  - Encrypts blocks with the same key, making it easier for attackers to crack.
  - Examples: DES, AES, Blowfish, GOST — divide plaintext into blocks (often 64-bit or 128-bit) and encrypt each block independently.

![ECB mode encryption showing three plaintext blocks each encrypted independently with the same key](./assets/img/post/crypto-ecb-mode-encryption.png)

- <font color=OrangeRed>**custom firmware**</font>—<font color=blue>Mobile device firmware</font> other than the firmware provided with the device. Sometimes used to root Android devices.

- <font color=OrangeRed>**CIRT**</font>—Cyber-incident response team. A group of experts who respond to security incidents.

- <font color=OrangeRed>**CYOD**</font>—Choose your own device. A <font color=blue>mobile device deployment model</font>. Employees connect their personally owned device as long as it is on a preapproved list. Compare with <font color=DarkOrange>BYOD</font> and <font color=DarkOrange>COPE</font>.

---

## D

- <font color=OrangeRed>**DAC**</font>—Discretionary access control. An access control model where owners can modify permissions for objects (files and folders). <font color=blue>Microsoft NTFS</font> uses the DAC model.

- <font color=OrangeRed>**data-at-rest**</font>—Any data <font color=blue>stored on media</font>. Common to encrypt sensitive data-at-rest.

- <font color=OrangeRed>**data execution prevention (DEP)**</font>—A <font color=blue>security feature</font> that prevents code from executing in memory regions marked as nonexecutable. Helps block malware.

- <font color=OrangeRed>**data exfiltration**</font>—The unauthorized transfer of data outside an organization.

- <font color=OrangeRed>**data-in-transit**</font>—Any data <font color=blue>sent over a network</font>. Common to encrypt sensitive data-in-transit.

- <font color=OrangeRed>**data-in-use**</font>—Any data currently being used by a computer. Not encrypted while in use (the computer needs to process it).

- <font color=OrangeRed>**data retention policy**</font> /rɪ'tenʃ(ə)n/—A <font color=blue>security policy</font> specifying how long data should be kept (retained).

- <font color=OrangeRed>**data sovereignty**</font> 最高统治权 /'sɒvrɪntɪ/—A term referring to <font color=blue>legal implications</font> of data stored in different countries. Primarily a concern for cloud backups stored in alternate locations.

- <font color=OrangeRed>**DDoS**</font>—Distributed denial-of-service. An attack <font color=blue>launched from multiple sources</font> intended to make a computer's resources or services unavailable. Compare with <font color=DarkOrange>DoS</font>.

- <font color=OrangeRed>**dead code**</font>—Code that is never executed or used. Often caused by logic errors.

- <font color=OrangeRed>**defense in depth**</font>—The use of multiple layers of security to protect resources.
  - <font color=blue>Control diversity</font> and <font color=blue>vendor diversity</font> are two methods to provide defense in depth.

- <font color=OrangeRed>**degaussing**</font> /di'ɡausiŋ/ 消磁—Removing data from magnetic media using a powerful electronic magnet. Used on backup tapes or to destroy hard disks.

- <font color=OrangeRed>**DER**</font>—Distinguished Encoding Rules. A base format for PKI certificates. <font color=blue>BASE64 ASCII encoded files</font>. Compare with <font color=DarkOrange>CER (Canonical Encoding Rules)</font>.

- <font color=OrangeRed>**DES**</font>—Data Encryption Standard. A legacy symmetric encryption standard. Has been compromised — use AES or 3DES instead.

- <font color=OrangeRed>**detective controls**</font>—Security controls that attempt to detect security incidents <font color=blue>after they have occurred</font>.

- <font color=OrangeRed>**deterrent controls**</font>—Security controls that attempt to <font color=blue>discourage</font> individuals from causing a security incident.

- <font color=OrangeRed>**dictionary**</font>—A password attack that uses a file of words and character combinations. Tries every entry in the file.

- <font color=OrangeRed>**differential backup**</font>—A type of backup that backs up all the data that has changed <font color=blue>since the last full backup</font>.

- <font color=OrangeRed>**Diffie-Hellman (DH)**</font>—An asymmetric algorithm used to privately share symmetric keys. DH Ephemeral (DHE) uses ephemeral keys re-created for each session. Elliptic Curve DHE (ECDHE) uses elliptic curve cryptography.

- <font color=OrangeRed>**diffusion**</font>—A cryptography concept that ensures small changes in plaintext result in significant changes in ciphertext.

- <font color=OrangeRed>**dig**</font>—A command-line tool used to test DNS on Linux systems. Compare with <font color=DarkOrange>nslookup</font>.

- <font color=OrangeRed>**digital signature**</font>—An encrypted hash of a message, encrypted with the sender's private key. Provides **authentication, non-repudiation, and integrity**.

- <font color=OrangeRed>**disablement policy**</font>—A policy that identifies when administrators should disable user accounts.

- <font color=OrangeRed>**disassociation attack**</font>—An attack that removes wireless clients from a wireless network.

- <font color=OrangeRed>**dissolvable agent**</font>—A NAC agent that runs on a client but deletes itself later. Checks the client for health. Compare with <font color=DarkOrange>permanent agent</font>.

- <font color=OrangeRed>**DLL injection**</font>—An attack that injects a Dynamic Link Library (DLL) into memory and runs it. Attackers rewrite the DLL, inserting malicious code.

- <font color=OrangeRed>**DLP**</font>—Data loss prevention. Technologies used to prevent data loss: block USB devices, monitor outgoing email, and monitor data stored in the cloud.

- <font color=OrangeRed>**DMZ**</font>—Demilitarized zone. A buffer zone between the Internet and an internal network. Internet clients can access services in the DMZ, but it protects the internal network.

- <font color=OrangeRed>**DNS**</font>—Domain Name System. A service used to resolve host names to IP addresses. DNS zones include A records (IPv4) and AAAA records (IPv6).

- <font color=OrangeRed>**DNSSEC**</font>—Domain Name System Security Extensions. A suite of extensions to protect the integrity of DNS records and prevent DNS attacks.

- <font color=OrangeRed>**DNS poisoning**</font>—An attack that modifies or corrupts DNS results. DNSSEC helps prevent it.

- <font color=OrangeRed>**domain hijacking**</font>—An attack that changes the registration of a domain name without permission from the owner.

- <font color=OrangeRed>**DoS**</font>—Denial-of-service. An attack from a **single source** that attempts to <font color=blue>disrupt the services</font> provided by the attacked system. Compare with <font color=DarkOrange>DDoS</font>.

- <font color=OrangeRed>**downgrade attack**</font>—A type of attack that forces a system to downgrade its security. The attacker then exploits the lesser security control.

- <font color=OrangeRed>**Drive-By Downloads**</font>—The unintended download of computer software from the Internet. Happens when visiting a website, opening an email attachment, clicking a link, or clicking a deceptive pop-up. The "supplier" claims the user "consented" to the download. Malicious content may <font color=blue>exploit vulnerabilities in the browser or plugins to run malicious code</font> without the user's knowledge.
  - **Drive-by install**: refers to installation rather than download (sometimes used interchangeably).

- <font color=OrangeRed>**DSA**</font>—Digital signature algorithm. An encrypted hash of a message for authentication, non-repudiation, and integrity. The sender's private key encrypts the hash.

- <font color=OrangeRed>**dumpster diving**</font>—Searching through trash looking for information from discarded documents. Shredding or burning papers helps prevent it.

---

## E

- <font color=OrangeRed>**EAP**</font>—Extensible Authentication Protocol. An authentication framework that provides general guidance for authentication methods. Variations include PEAP, EAP-TLS, EAP-TTLS, and EAP-FAST.

- <font color=OrangeRed>**EAP-FAST**</font>—EAP-Flexible Authentication via Secure Tunneling. A Cisco-designed replacement for LEAP. Supports certificates, but they are optional.

- <font color=OrangeRed>**EAP-TLS**</font>—Extensible Authentication Protocol-Transport Layer Security. One of the most secure EAP standards. Requires **certificates on both the 802.1x server and on the clients**.

- <font color=OrangeRed>**EAP-TTLS**</font>—Extensible Authentication Protocol-Tunneled Transport Layer Security. Allows systems to use older authentication methods (such as PAP) within a TLS tunnel. Requires a certificate on the **802.1x server only** (not on clients).

- <font color=OrangeRed>**embedded system**</font>—Any device with a dedicated function that uses a computer system. Includes a CPU, an operating system, and one or more applications.

- <font color=OrangeRed>**EMI**</font>—Electromagnetic interference. Interference caused by motors, power lines, and fluorescent lights. EMI shielding prevents outside interference and prevents data from emanating outside the cable.

- <font color=OrangeRed>**EMP**</font>—Electromagnetic pulse. A short burst of energy that can damage electronic equipment. Results from electrostatic discharge (ESD), lightning, and military weapons.

- <font color=OrangeRed>**encryption**</font>—A process that scrambles data to make it unreadable. Normally includes a public algorithm and a private key. Compare with <font color=DarkOrange>asymmetric</font> and <font color=DarkOrange>symmetric encryption</font>.

- <font color=OrangeRed>**Enterprise**</font>—A wireless mode that uses an 802.1x server for security. Forces users to authenticate with a username and password. Compare with <font color=DarkOrange>Open</font> and <font color=DarkOrange>PSK</font> modes.

- <font color=OrangeRed>**ephemeral key**</font>—A type of key used in cryptography. Ephemeral keys have very short lifetimes and are re-created for each session.

- <font color=OrangeRed>**error handling**</font>—A programming process that handles errors gracefully.

- <font color=OrangeRed>**ESP**</font>—Encapsulating Security Payload. An option within IPsec to provide **confidentiality, integrity, and authentication**.

- <font color=OrangeRed>**evil twin**</font>—A type of rogue AP. An evil twin has the **same SSID** as a legitimate AP.

- <font color=OrangeRed>**exit interview**</font>—An interview conducted with departing employees just before they leave an organization.

- <font color=OrangeRed>**exploitation frameworks**</font>—Tools used to store information about security vulnerabilities. Used by penetration testers (and attackers) to detect and exploit software.

- <font color=OrangeRed>**extranet**</font>—The part of an internal network shared with outside entities. Often used to provide access to authorized business partners, customers, or vendors.

---

## F

- <font color=OrangeRed>**facial recognition**</font>—A biometric method that identifies people based on facial features.

- <font color=OrangeRed>**false negative**</font>—A security incident that isn't detected or reported. A NIDS false negative occurs if an attack is active but the NIDS does not raise an alert.

- <font color=OrangeRed>**false positive**</font>—An alert on an event that isn't a security incident. A NIDS false positive occurs if the NIDS raises an alert but network activity is normal.

- <font color=OrangeRed>**FAR**</font>—False acceptance rate (also called the false match rate). The percentage of times a biometric authentication system incorrectly indicates a match.

- <font color=OrangeRed>**Faraday cage**</font>—A room or enclosure that prevents signals from emanating beyond it.

- <font color=OrangeRed>**fat AP / stand-alone AP**</font>—An AP that <font color=blue>includes everything needed</font> to connect wireless clients to a wireless network. Must be configured independently. Compare with <font color=DarkOrange>thin AP</font>.

- <font color=OrangeRed>**fault tolerance**</font>—The capability of a system to suffer a fault but continue to operate.

- <font color=OrangeRed>**FDE**</font>—Full disk encryption. A method to encrypt an entire disk. Compare with <font color=DarkOrange>SED</font>.

- <font color=OrangeRed>**federation**</font>—Two or more members of a federated identity management system. Used for single sign-on.

- <font color=OrangeRed>**fingerprint scanners**</font>—Biometric systems that scan fingerprints for authentication.

- <font color=OrangeRed>**firewall**</font>—A software or network device used to filter traffic. Stateful firewalls filter traffic using rules within an ACL. Stateless firewalls filter traffic based on state within a session.

- <font color=OrangeRed>**firmware OTA updates**</font>—Over-the-air updates for mobile device firmware.

- <font color=OrangeRed>**flood guard**</font>—Thwarts flood attacks. On switches, prevents MAC flood attacks. On routers, prevents SYN flood attacks.

- <font color=OrangeRed>**framework**</font>—A structure used to provide a foundation. Cybersecurity frameworks provide guidance on implementing security.

- <font color=OrangeRed>**FRR**</font>—False rejection rate (also called the false nonmatch rate). The percentage of times a biometric system incorrectly rejects a valid match.

- <font color=OrangeRed>**FTPS**</font>—File Transfer Protocol Secure. An extension of FTP that uses TLS. Some implementations use TCP ports 989 and 990.

- <font color=OrangeRed>**full backup**</font>—A type of backup that backs up all the selected data.

- <font color=OrangeRed>**full tunnel**</font>—An encrypted VPN connection where **all traffic** from the user is encrypted. Compare with <font color=DarkOrange>split tunnel</font>.

---

## G

- <font color=OrangeRed>**GCM**</font>—Galois/Counter Mode. Combines Counter (CTM) mode with hashing techniques for data authenticity and confidentiality.

- <font color=OrangeRed>**geofencing**</font>—A virtual fence or geographic boundary using GPS. Apps respond when a mobile device enters the virtual fence.

- <font color=OrangeRed>**geolocation**</font>—The location of a device identified by GPS. Can help locate a lost or stolen mobile device.

- <font color=OrangeRed>**GPO**</font>—Group Policy Object. A technology within Microsoft Windows to manage users and computers. Implemented on a domain controller.

- <font color=OrangeRed>**GPS**</font>—Global Positioning System. A satellite-based navigation system that identifies the location of a device or vehicle.

- <font color=OrangeRed>**GPS tagging**</font>—Adding geographical data (latitude/longitude) to files such as pictures.
  - **Gratuitous ARP**: not waiting for a request — just sending the reply.

- <font color=OrangeRed>**gray box test**</font>—A type of penetration test. Testers have **some** knowledge of the environment. Compare with <font color=DarkOrange>black box test</font> and <font color=DarkOrange>white box test</font>.

- <font color=OrangeRed>**group-based access control**</font>—A role-based access control method that uses groups as roles.

- <font color=OrangeRed>**Guest account**</font>—A pre-created account in Windows systems. Disabled by default.

---

## H

- <font color=OrangeRed>**hacktivist**</font>—An attacker who launches attacks as part of an activist movement or to further a cause.

- <font color=OrangeRed>**hardware root of trust**</font>—A <font color=blue>known secure starting point</font>.
  - <font color=OrangeRed>TPMs</font> have a private key burned into the hardware that provides a hardware root of trust.

- <font color=OrangeRed>**hash**</font>—A number created by <font color=blue>executing a hashing algorithm against data</font> (such as a file or message). Used for <font color=blue>integrity</font>. Common algorithms: MD5, SHA-1, HMAC.

- <font color=OrangeRed>**heuristic / behavioral**</font> 启发式的—A <font color=blue>type of monitoring</font> on IDS/IPS systems. Detects attacks by <font color=blue>comparing traffic against a baseline</font>. Also known as 异常 <font color=OrangeRed>anomaly detection</font>.

- <font color=OrangeRed>**HIDS**</font>—Host-based intrusion detection system. Software installed on a system to detect attacks.
  - <font color=DarkOrange>HIPS (host-based intrusion prevention system)</font>: extension of HIDS that also blocks attacks.

- <font color=OrangeRed>**high availability**</font>—A term indicating a system or component remains available close to 100 percent of the time.

- <font color=OrangeRed>**HMAC**</font>—Hash-based Message Authentication Code. A <font color=blue>hashing algorithm</font> used to verify <font color=OrangeRed>integrity</font> and <font color=OrangeRed>authenticity</font> of a message with a shared secret. Typically combined with SHA.
  - Hashes the secret key with messages. Usually used between server and client.
  - The <font color=blue>secret key should be time-limited and random</font>. Server sends a form and a random key to the client; client finishes the form and hashes it with the random secret key; server verifies the stored hash against the received hash.

- <font color=OrangeRed>**hoax**</font>—A message (often circulated through email) that tells of impending doom from a virus or security threat that doesn't exist.

- <font color=OrangeRed>**honeypot**</font>—A server designed to attract an attacker. Has weakened security encouraging attackers to investigate it.

- <font color=OrangeRed>**honeynet**</font>—A group of honeypots in a network. Often configured in virtual networks.

- <font color=OrangeRed>**hot and cold aisles**</font>—A data center cooling method. Cool air flows from the front of cabinets to the back.

- <font color=OrangeRed>**HOTP**</font>—HMAC-based One-Time Password. An open standard for creating one-time passwords. Combines a secret key and a counter, then uses HMAC to create a hash.

- <font color=OrangeRed>**hot site**</font>—An alternate location for operations. Typically operational within 60 minutes. Compare with <font color=DarkOrange>cold site</font> and <font color=DarkOrange>warm site</font>.

- <font color=OrangeRed>**HSM**</font>—Hardware security module. A removable or external device that can generate, store, and manage RSA keys used in asymmetric encryption. Compare with <font color=DarkOrange>TPM</font>.

- <font color=OrangeRed>**HTTPS**</font>—Hypertext Transfer Protocol Secure. Encrypts HTTP traffic with TLS using **TCP port 443**.

- <font color=OrangeRed>**HVAC**</font>—Heating, ventilation, and air conditioning. A physical security control that increases availability by regulating airflow within data centers.

---

## I

- <font color=OrangeRed>**IaaS**</font>—Infrastructure as a Service. A cloud computing model that allows an organization to rent access to hardware in a self-managed platform. Compare with <font color=DarkOrange>PaaS</font> and <font color=DarkOrange>SaaS</font>.

- <font color=OrangeRed>**ICS**</font>—Industrial control system. Controls large systems such as power plants or water treatment facilities. A SCADA system controls the ICS.

- <font color=OrangeRed>**identification**</font>—The process that occurs when a user claims an identity, such as with a username.

- <font color=OrangeRed>**IEEE 802.1x**</font>—An authentication protocol used in VPNs and wired/wireless networks. VPNs often implement it as a RADIUS server. Wired networks use it for port-based authentication. Wireless networks use it in Enterprise mode.

- <font color=OrangeRed>**ifconfig**</font>—A command-line tool on Linux systems to show and manipulate NIC settings. Similar to <font color=DarkOrange>ipconfig</font> on Windows.

- <font color=OrangeRed>**IMAP4**</font>—Internet Message Access Protocol version 4. Stores and manages email on servers. Uses **TCP port 143**.

- <font color=OrangeRed>**impact**</font>—The magnitude of harm related to a risk. The negative result of an event (loss of confidentiality, integrity, or availability). Compare with <font color=DarkOrange>likelihood of occurrence</font>.

- <font color=OrangeRed>**implicit deny**</font>—A rule in an ACL that blocks all traffic that hasn't been explicitly allowed. The **last rule** in an ACL.

- <font color=OrangeRed>**Incident response**</font>—The process of responding to a security incident.

- <font color=OrangeRed>**incident response plan (IRP)**</font>—The procedures documented in an incident response policy.

- <font color=OrangeRed>**incident response process**</font>—The phases: **preparation, identification, containment, eradication, recovery, and lessons learned**.

- <font color=OrangeRed>**incremental backup**</font>—A type of backup that backs up all data changed since the last full or incremental backup.

- <font color=OrangeRed>**injection attack**</font>—An attack that injects code or commands. Common types: DLL injection, command injection, SQL injection.

- <font color=OrangeRed>**inline**</font>—A configuration that forces traffic to pass through a device. A NIPS is placed inline. Sometimes called in-band. Compare with <font color=DarkOrange>out-of-band</font>.

- <font color=OrangeRed>**input validation**</font>—A programming process that verifies data is valid before using it.

- <font color=OrangeRed>**insider**</font>—An attacker who launches attacks from within an organization, typically as an employee.

- <font color=OrangeRed>**integer overflow**</font>—An application attack that attempts to use or create a numeric value too big for an application to handle. Input handling and error handling thwart the attack.

- <font color=OrangeRed>**integrity**</font>—One of the three main goals of the CIA security triad. Provides assurance that data or system configurations have not been modified. Audit logs and hashing ensure integrity. Compare with <font color=DarkOrange>availability</font> and <font color=DarkOrange>confidentiality</font>.

- <font color=OrangeRed>**intranet**</font>—An internal network. People use an intranet to communicate and share content.

- <font color=OrangeRed>**IoT**</font>—Internet of things. The network of physical devices connected to the Internet. Refers to smart devices with an IP address, such as wearable technology and home automation.

- <font color=OrangeRed>**ipconfig**</font>—A command-line tool on Windows systems to show NIC configuration settings.

- <font color=OrangeRed>**IPsec**</font>—Internet Protocol security. A suite of protocols to encrypt data-in-transit. Operates in Tunnel mode (for VPN traffic) and Transport mode (in private networks).

- <font color=OrangeRed>**IP spoofing**</font>—An attack that changes the source IP address.

- <font color=OrangeRed>**iris scanners**</font>—Biometric systems that scan the iris of an eye for authentication.

- <font color=OrangeRed>**ISA**</font>—Interconnection security agreement. An <font color=blue>agreement</font> that <font color=blue>specifies technical and security requirements</font> for connections between two or more entities. Compare with <font color=DarkOrange>MOU/MOA</font>.

- <font color=OrangeRed>**IV (initialization vector) attack**</font>—A wireless attack that attempts to discover the IV. Legacy wireless security protocols are susceptible to IV attacks.

---

## J

- <font color=OrangeRed>**jailbreaking**</font>—The process of modifying an Apple mobile device to remove software restrictions. Allows a user to install software from any third-party source. Compare with <font color=DarkOrange>rooting</font>.

- <font color=OrangeRed>**jamming**</font>—A DoS attack against wireless networks. Transmits noise on the same frequency used by a wireless network.

- <font color=OrangeRed>**job rotation**</font>—A process that ensures employees rotate through different jobs to learn the processes and procedures in each job. Can sometimes detect fraudulent activity.

---

## K

- <font color=OrangeRed>**KDC**</font>—Key Distribution Center. Also known as a <font color=blue>TGT server</font>. Part of the Kerberos protocol used for network authentication. Issues timestamped tickets that expire.

- <font color=OrangeRed>**Kerberos**</font>—A network authentication mechanism used with Windows Active Directory domains and some Unix environments (realms). Uses a KDC to issue tickets.

- <font color=OrangeRed>**kernel**</font>—The central part of the operating system. In container virtualization, guests share the kernel.

- <font color=OrangeRed>**key escrow**</font>—The process of placing a copy of a private key in a safe environment.

- <font color=OrangeRed>**keylogger**</font>—Software or hardware used to capture a user's keystrokes. Keystrokes are stored in a file and can be manually retrieved or automatically sent to an attacker.

- <font color=OrangeRed>**key stretching**</font>—A technique used to increase the strength of stored passwords. Adds additional bits (salts) and can help thwart brute force and rainbow table attacks.

- <font color=OrangeRed>**known plaintext**</font>—A cryptographic attack that decrypts encrypted data. The attacker knows the plaintext used to create ciphertext.

---

## L

- <font color=OrangeRed>**labeling**</font>—The process of ensuring data is tagged clearly so users know its classification. Labels can be physical (on backup tapes) or digital (embedded in files).

- <font color=OrangeRed>**LDAP**</font>—Lightweight Directory Access Protocol. A <font color=blue>protocol used to communicate with directories</font> such as Microsoft Active Directory. Identifies objects with query strings using codes such as CN=Users and DC=GetCertifiedGetAhead.

- <font color=OrangeRed>**LDAPS**</font>—Lightweight Directory Access Protocol Secure. A protocol used to <font color=blue>encrypt LDAP traffic with TLS</font>.

- <font color=OrangeRed>**least functionality**</font>—A core <font color=blue>principle</font> of secure systems design. Systems should be deployed with only the applications, services, and protocols needed to meet their purpose.

- <font color=OrangeRed>**least privilege**</font>—A security <font color=blue>principle</font> that specifies individuals and processes are granted only the rights and permissions needed to perform assigned tasks, but no more.

- <font color=OrangeRed>**legal hold**</font>—A court order to maintain data for evidence.

- <font color=OrangeRed>**likelihood of occurrence**</font>—The probability that something will occur. Used with impact in a <font color=blue>qualitative risk assessment</font>. Compare with <font color=DarkOrange>impact</font>.

- <font color=OrangeRed>**load balancer**</font>—Hardware or software that <font color=blue>balances the load</font> between two or more servers.
  - <font color=blue>Scheduling methods</font> include source address IP affinity and round-robin.
  - <font color=DarkOrange>Affinity</font>: uses the client's IP address to redirect to the same server during a web session.
  - <font color=DarkOrange>round-robin</font>: sends requests to servers one after another.

- <font color=OrangeRed>**location-based policies**</font>—Policies that <font color=blue>prevent users from logging on from certain locations</font>, or require that they log on only from specific locations.

- <font color=OrangeRed>**logic bomb**</font>—A type of <font color=blue>malware</font> that <font color=blue>executes in response to an event</font> (a specific date/time, or a user action such as launching a specific program).

- <font color=OrangeRed>**loop prevention**</font>—A method of preventing switching loop or bridge loop problems. Both <font color=DarkOrange>STP</font> and <font color=DarkOrange>RSTP</font> prevent switching loops.

---

## M

- <font color=OrangeRed>**MAC**</font>—Mandatory access control. An <font color=blue>access control model</font> that uses sensitivity labels assigned to objects (files and folders) and subjects (users). MAC restricts access based on need to know. Every resource has a sensitivity label matching a clearance level assigned to a user.

- <font color=OrangeRed>**MAC**</font>—Media access control. A **48-bit address** used to identify <font color=blue>network interface cards</font>. Also called a hardware address or physical address.

- <font color=OrangeRed>**MAC filtering**</font>—A form of <font color=blue>network access control</font> to allow or block access based on the MAC address.
  - Configured on switches for <font color=blue>port security</font> or on APs for <font color=blue>wireless security</font>.

- <font color=OrangeRed>**MAC spoofing**</font>—An attack that changes the source MAC address.

- <font color=OrangeRed>**mail gateway**</font>—A server that examines and processes all incoming and outgoing email. Typically includes a spam filter and DLP capabilities.

- <font color=OrangeRed>**Malware**</font>—Malicious software. Includes viruses, worms, ransomware, rootkits, logic bombs, and more.

- <font color=OrangeRed>**Malvertising**</font>—The use of online advertising to spread malware. Injecting malicious advertisements into legitimate online advertising networks and webpages.

- <font color=OrangeRed>**Mandatory vacation**</font>—A <font color=blue>policy</font> that forces employees to take a vacation. Goals: <font color=blue>deter malicious activity</font> (such as fraud and embezzlement /ɪmˈbezlmənt/) and <font color=blue>detect malicious activity</font> when it occurs.

- <font color=OrangeRed>**Man-in-the-browser**</font>—An <font color=blue>attack</font> that infects vulnerable web browsers. Can <font color=blue>capture browser session data</font>, including keystrokes.

- <font color=OrangeRed>**man-in-the-middle (MITM)**</font>—An <font color=blue>attack</font> using <font color=blue>active interception or eavesdropping</font>. Uses a third computer to capture traffic sent between two other systems.

- <font color=OrangeRed>**mantrap**</font>—A <font color=blue>physical security mechanism</font> designed to control access to a secure area. Prevents tailgating.

- <font color=OrangeRed>**MD5**</font>—Message Digest 5. A <font color=blue>hashing function</font> used to provide integrity. Creates **128-bit hashes** (MD5 checksums). Considered cracked.

- <font color=OrangeRed>**MDM**</font>—Mobile device management. Technologies used to <font color=blue>manage mobile devices</font>. Can monitor devices and ensure compliance with security policies.

- <font color=OrangeRed>**memory leak**</font>—An <font color=blue>application flaw</font> that consumes memory without releasing it.

- <font color=OrangeRed>**MFDs**</font>—Multi-function devices. Devices that perform multiple functions (print, scan, copy, fax).

- <font color=OrangeRed>**MMS**</font>—Multimedia Messaging Service. An <font color=blue>extension of SMS</font> that supports sending multimedia content.

- <font color=OrangeRed>**MOU/MOA**</font>—Memorandum 记录 of understanding / agreement. A type of <font color=blue>agreement</font> that <font color=blue>defines responsibilities</font> of each party. Compare with <font color=DarkOrange>ISA</font> (interconnection security agreement).

- <font color=OrangeRed>**MS-CHAPv2**</font>—Microsoft Challenge Handshake Authentication Protocol version 2. Provides <font color=blue>mutual authentication</font>. Compare with <font color=DarkOrange>CHAP</font> and <font color=DarkOrange>PAP</font>.

- <font color=OrangeRed>**MTBF**</font>—Mean time between failures. A <font color=blue>metric</font> that provides the <font color=blue>average time between failures</font>.

- <font color=OrangeRed>**MTTR**</font>—Mean time to recover. A <font color=blue>metric</font> identifying the <font color=blue>average time it takes to restore a failed system</font>.

- <font color=OrangeRed>**multifactor authentication**</font>—A type of authentication that uses methods from more than one factor of authentication.

---

## N

- <font color=OrangeRed>**NAC**</font>—Network access control. A system that inspects clients to ensure they are healthy.
  - NAC systems use **health**: indicating that a client meets predetermined characteristics.
  - Agents inspect clients and can be <font color=DarkOrange>permanent</font> or <font color=DarkOrange>dissolvable (agentless)</font>.

- <font color=OrangeRed>**NAT**</font>—Network Address Translation. Translates public IP addresses to private IP addresses and vice versa. Compare with <font color=DarkOrange>PAT</font>.

- <font color=OrangeRed>**NDA**</font>—Non-disclosure agreement. An <font color=blue>agreement</font> designed to prohibit personnel from sharing proprietary data.

- <font color=OrangeRed>**Netcat**</font>—A command-line tool used to connect to remote systems.

- <font color=OrangeRed>**netstat**</font>—A command-line tool used to show network statistics on a system.

- <font color=OrangeRed>**network mapping**</font>—A process used to <font color=blue>discover devices on a network</font>, including <font color=blue>how they are connected</font>.

- <font color=OrangeRed>**network scanner**</font>—A tool used to discover devices on a network, including their IP addresses, operating system, and services/protocols running.

- <font color=OrangeRed>**NFC**</font>—Near field communication. A group of standards that allow mobile devices to communicate with nearby mobile devices.

- <font color=OrangeRed>**NFC attack**</font>—An attack against mobile devices that use near field communication (NFC).

- <font color=OrangeRed>**NIDS**</font>—Network-based intrusion detection system. A device that <font color=blue>detects attacks and raises alerts</font>. Installed on network devices (routers or firewalls), monitors network traffic.

- <font color=OrangeRed>**NIPS**</font>—Network-based intrusion prevention system. A device that <font color=blue>detects and stops</font> attacks in progress. Placed inline with traffic.

- <font color=OrangeRed>**NIST**</font>—National Institute of Standards and Technology. Part of the U.S. Department of Commerce. Its <font color=blue>Information Technology Laboratory (ITL)</font> publishes special publications related to security.

- <font color=OrangeRed>**Nmap**</font>—A command-line tool used to scan networks. A type of network scanner.

- <font color=OrangeRed>**nonce**</font>—A number used once. Cryptography elements frequently use a nonce to add randomness.

- <font color=OrangeRed>**non-persistence**</font>—A method used in <font color=blue>virtual desktops</font> where changes made by a user are not saved. When users log off, the desktop <font color=blue>reverts to its original state</font>.

- <font color=OrangeRed>**non-repudiation**</font>—The ability to prevent a party from denying an action.
  - <font color=blue>Digital signatures</font> and <font color=blue>access logs</font> provide non-repudiation.

- <font color=OrangeRed>**normalization**</font>—The <font color=blue>process</font> of organizing tables and columns in a database. Reduces redundant data and improves overall database performance.

- <font color=OrangeRed>**nslookup**</font>—A command-line tool used to test DNS on Microsoft systems. Compare with <font color=DarkOrange>dig</font>.

- <font color=OrangeRed>**NTLM**</font>—New Technology LAN Manager. A suite of <font color=blue>protocols</font> that provide <font color=blue>confidentiality, integrity, and authentication</font> within Windows systems. Versions: NTLM, NTLMv2, NTLM2 Session.

---

## O

- <font color=OrangeRed>**OAuth**</font>—An open source standard used for authorization with Internet-based single sign-on solutions.

- <font color=OrangeRed>**Obfuscation**</font> /ɔbfʌ'skeiʃən/—An attempt to make something unclear or difficult to understand.
  - Steganography methods use obfuscation to hide data within data.

- <font color=OrangeRed>**OCSP**</font>—Online Certificate Status Protocol. An alternative to using a CRL. Allows entities to <font color=blue>query a CA</font> with the serial number of a certificate. The CA answers with <font color=blue>good</font>, <font color=blue>revoked</font>, or <font color=blue>unknown</font>.

- <font color=OrangeRed>**onboarding**</font>—The <font color=blue>process</font> of granting individuals access to an organization's computing resources after being hired.

- <font color=OrangeRed>**Open**</font>—A <font color=blue>wireless mode</font> that doesn't use security. Compare with <font color=DarkOrange>Enterprise</font> and <font color=DarkOrange>PSK</font> modes.

- <font color=OrangeRed>**OpenID Connect**</font>—An <font color=blue>open source standard</font> used for identification on the Internet. Typically used with OAuth. <font color=blue>Allows clients to verify the identity of end users</font> without managing their credentials.

- <font color=OrangeRed>**open-source intelligence**</font>—A method of <font color=blue>gathering data using public sources</font>, such as social media sites and news outlets.

- <font color=OrangeRed>**order of volatility**</font> /ˌvɑlə'tɪləti/—The order in which evidence should be <font color=blue>collected</font>. Data in memory is more volatile than data on disk, so it should be collected first.
  - From most volatile to least volatile:
    - Data in **cache memory** (processor cache, hard drive cache)
    - Data in **RAM** (random access memory), including system and network processes
    - A **paging file** (swap file) on the system disk drive
    - Data stored on **local disk drives**
    - Logs stored on **remote systems**
    - Archive /ˈɑ:kaiv/ media

- <font color=OrangeRed>**OSI model**</font>—Open Systems Interconnection reference model. Defines <font color=blue>how applications communicate across the network</font>. Goal: interoperability 互用性 of diverse communication systems.
  - **Layer 1: Physical** — transmission and reception of unstructured raw data. Converts digital bits into electrical, radio, or optical signals.
  - **Layer 2: Data Link** — node-to-node data transfer between two directly connected nodes. Detects and corrects physical layer errors. (Frames)
  - **Layer 3: Network** — transferring variable-length data sequences (packets) between nodes in different networks.
  - **Layer 4: Transport** — transferring variable-length data sequences <font color=blue>from a source to a destination host</font>, maintaining quality of service. (TCP/UDP)
  - **Layer 5: Session** — controls the dialogues 对话 (connections) between computers. Establishes, manages, and terminates connections between local and remote applications.
  - **Layer 6: Presentation** — responsible for <font color=blue>formatting of data being exchanged</font>, translating between application and network formats.
  - **Layer 7: Application** — <font color=blue>provides basic underlying network infrastructure</font>, allows applications to communicate with each other.

- <font color=OrangeRed>**out-of-band**</font>—A configuration that allows a device to <font color=blue>collect traffic without the traffic passing through it</font>. Sometimes called passive. Compare with <font color=DarkOrange>inline</font>.

---

## P

- <font color=OrangeRed>**P7B**</font>—PKCS#7. A common format for PKI certificates. DER-based (ASCII), commonly used to share public keys.

- <font color=OrangeRed>**P12**</font>—PKCS#12. A common format for PKI certificates. CER-based (binary), often holds certificates with the private key. Commonly encrypted.

- <font color=OrangeRed>**PaaS**</font>—Platform as a Service. A cloud computing model that provides a preconfigured computing platform. Compare with <font color=DarkOrange>IaaS</font> and <font color=DarkOrange>SaaS</font>.

- <font color=OrangeRed>**PAP**</font>—Password Authentication Protocol. An older authentication protocol where passwords or PINs are sent across the network in **cleartext**. Compare with <font color=DarkOrange>CHAP</font> and <font color=DarkOrange>MS-CHAPv2</font>.

- <font color=OrangeRed>**passive reconnaissance**</font>—A penetration testing method that typically uses open-source intelligence. Compare with <font color=DarkOrange>active reconnaissance</font>.

- <font color=OrangeRed>**pass the hash**</font>—A password attack that captures and uses the hash of a password. Attempts to log on as the user with the hash. Commonly associated with Microsoft NTLM.

- <font color=OrangeRed>**password cracker**</font>—A tool used to discover passwords.

- <font color=OrangeRed>**patch management**</font>—The process used to keep systems up to date with current patches. Typically includes evaluating and testing patches before deploying them.

- <font color=OrangeRed>**PBKDF2**</font>—Password-Based Key Derivation Function 2. A key stretching technique that adds additional bits as a salt. Helps prevent brute force and rainbow table attacks.

- <font color=OrangeRed>**PEAP**</font>—Protected Extensible Authentication Protocol. An extension of EAP used with 802.1x. Requires a certificate on the **802.1x server**.

- <font color=OrangeRed>**PEM**</font>—Privacy Enhanced Mail. A common format for PKI certificates. Can use CER (ASCII) or DER (binary) formats.

- <font color=OrangeRed>**penetration testing**</font>—A method of testing targeted systems to determine if vulnerabilities can be exploited. Penetration tests are intrusive. Compare with <font color=DarkOrange>vulnerability scanner</font>.

- <font color=OrangeRed>**perfect forward secrecy**</font>—A characteristic of encryption keys ensuring that keys are random. Does not use deterministic algorithms.

- <font color=OrangeRed>**permanent agent**</font>—A NAC agent that is installed on a client. Checks the client for health. Compare with <font color=DarkOrange>dissolvable agent</font>.

- <font color=OrangeRed>**permission auditing review**</font>—An audit that analyzes user privileges. Identifies privileges granted to users and compares them against what users need.

- <font color=OrangeRed>**PFX**</font>—Personal Information Exchange. A common format for PKI certificates. The predecessor to P12 certificates.

- <font color=OrangeRed>**Pharming**</font>—Obtain personal information by <font color=blue>domain spoofing</font>, 'poisons' a DNS server, infuses false information into the DNS server, resulting in a <font color=blue>user's request being redirected elsewhere</font>.

- <font color=OrangeRed>**PHI**</font>—Personal Health Information. PII that includes health information.

- <font color=OrangeRed>**phishing**</font>—The practice of <font color=blue>sending email to users with the purpose of tricking</font> them into revealing personal information or clicking on a link.

- <font color=OrangeRed>**physical controls**</font>—Security controls that can be physically touched.

- <font color=OrangeRed>**PII**</font>—Personally Identifiable Information. Information about individuals that can be used to trace a person's identity (full name, birth date, biometric data, etc.).

- <font color=OrangeRed>**ping**</font>—A command-line tool used to test connectivity with remote systems.

- <font color=OrangeRed>**pinning**</font>—A <font color=blue>security mechanism</font> used by some web sites to detect impersonation.
  - **Public key pinning**: provides clients with a list of public key hashes in HTTPS responses that clients use to detect web site impersonation attempts.
  - **HTTP Public Key Pinning (HPKP)**: A security mechanism that allows HTTPS websites to resist impersonation by attackers using fraudulent certificates.
  - **OCSP stapling**: reduces OCSP traffic by appending a timestamped, digitally signed OCSP response to a certificate.
  - **Perfect forward secrecy**: ensures that the compromise of a long-term key does not compromise keys used in the past.
  - **Key stretching techniques**: add additional bits (salts) to passwords.

- <font color=OrangeRed>**PIV**</font>—Personal Identity Verification card. A specialized smart card used by U.S. federal agencies. Includes photo identification; provides confidentiality, integrity, authentication, and non-repudiation.

- <font color=OrangeRed>**Pivot**</font> 枢轴—One of the steps in penetration testing. After escalating privileges, the tester uses additional tools to gain information on the exploited computer or network.
  - The process of accessing other systems through a single compromised system.

- <font color=OrangeRed>**plaintext**</font>—Text displayed in a readable format. Encryption converts plaintext to ciphertext.

- <font color=OrangeRed>**pointer dereference**</font>—A programming practice that uses a pointer to reference a memory area.
  - A failed dereference operation can corrupt memory and sometimes cause an application to crash.

- <font color=OrangeRed>**POP3**</font>—Post Office Protocol version 3. Protocol used to transfer email from mail servers to clients.

- <font color=OrangeRed>**port mirror**</font>—A monitoring port on a switch. All traffic going through the switch is also sent to the port mirror.

- <font color=OrangeRed>**preventive controls**</font>—Security controls that attempt to prevent a security incident from occurring.

- <font color=OrangeRed>**privacy impact assessment**</font>—An assessment used to identify and reduce risks related to potential loss of PII. Compare with <font color=DarkOrange>privacy threshold assessment</font>.

- <font color=OrangeRed>**privacy threshold assessment**</font>—An assessment used to help identify <font color=blue>if a system is processing PII</font>.

- <font color=OrangeRed>**private data**</font>—Information about an individual that should remain private.
  - Examples: Personally Identifiable Information (PII) and Personal Health Information (PHI).

- <font color=OrangeRed>**private key**</font>—Part of a matched key pair used in asymmetric encryption. The private key always stays private. Compare with <font color=DarkOrange>public key</font>.

- <font color=OrangeRed>**privilege escalation**</font>—The process of gaining elevated rights and permissions.

- <font color=OrangeRed>**privileged account**</font>—An account with elevated privileges, such as an administrator account.

- <font color=OrangeRed>**proprietary data**</font>—Data related to ownership. Common examples: patents or trade secrets.

- <font color=OrangeRed>**protocol analyzer**</font>—A tool used to capture network traffic. Can be used to view data sent in clear text.

- <font color=OrangeRed>**proximity cards**</font>—Small credit card-sized cards that activate when in close proximity to a card reader.

- <font color=OrangeRed>**proxy/proxies**</font>—A server (or servers) used to forward requests for services such as HTTP or HTTPS.
  - **Forward proxy**: forwards requests from internal clients to external servers.
  - **Reverse proxy**: accepts requests from the Internet and forwards them to an internal web server.
  - **Transparent proxy**: does not modify requests.
  - **Application proxy**: used for a specific application.

- <font color=OrangeRed>**PSK**</font>—Pre-shared key. A wireless mode that uses a pre-shared key (similar to a password or passphrase). Compare with <font color=DarkOrange>Enterprise</font> and <font color=DarkOrange>Open</font> modes.

- <font color=OrangeRed>**public data**</font>—Data that is available to anyone. Found in brochures, press releases, or web sites.

- <font color=OrangeRed>**public key**</font>—Part of a matched key pair used in asymmetric encryption. The public key is publicly available. Compare with <font color=DarkOrange>private key</font>.

- <font color=OrangeRed>**Public Key Infrastructure (PKI)**</font>—A group of technologies used to request, create, manage, store, distribute, and revoke digital certificates.

- <font color=OrangeRed>**pulping**</font>—A process performed after shredding papers. Reduces the shredded paper to a mash or puree.

- <font color=OrangeRed>**pulverizing**</font>—A process used to physically destroy items such as optical discs.

- <font color=OrangeRed>**purging**</font>—A general sanitization term indicating that all sensitive data has been removed from a device.

- <font color=OrangeRed>**push notification services**</font>—The services that send messages to mobile devices.

---

## Q

- <font color=OrangeRed>**qualitative risk assessment**</font>—A risk assessment that uses judgment to categorize risks. Based on impact and likelihood of occurrence.

- <font color=OrangeRed>**quantitative risk assessment**</font>—A risk assessment that uses specific monetary amounts to identify cost and asset value. Uses SLE and ARO to calculate ALE.

---

## R

- <font color=OrangeRed>**race condition**</font>—A programming flaw that occurs when two sets of code attempt to access the same resource. The first one to access the resource wins, which can result in inconsistent results.

- <font color=OrangeRed>**RADIUS**</font>—Remote Authentication Dial-In User Service. An authentication service that provides central authentication for remote access clients. Alternatives: TACACS+ and Diameter.

- <font color=OrangeRed>**RAID**</font>—Redundant array of inexpensive disks. Multiple disks added together to increase performance or provide fault protection. Common types: RAID-1, RAID-5, RAID-6, RAID-10.

- <font color=OrangeRed>**rainbow table**</font>—A file containing precomputed hashes for character combinations. Used to discover passwords. PBKDF2 and bcrypt thwart rainbow table attacks.

- <font color=OrangeRed>**ransomware**</font>—A type of malware used to extort money. Typically encrypts the user's data and demands a ransom before decrypting.

- <font color=OrangeRed>**RAT**</font>—Remote access Trojan. Malware that allows an attacker to take control of a system from a remote location.

- <font color=OrangeRed>**RC4**</font>—A symmetric stream cipher that can use between 40 and 2,048 bits. Considered cracked — recommend using stronger alternatives.

- <font color=OrangeRed>**record time offset**</font>—An offset used by recorders to identify times on recordings. If the recording start time is known, the offset identifies the actual time at any point.

- <font color=OrangeRed>**recovery site**</font>—An alternate location for business functions after a major disaster.

- <font color=OrangeRed>**redundancy**</font>—The process of adding duplication to critical system components and networks to provide fault tolerance.

- <font color=OrangeRed>**refactoring**</font>—A driver manipulation method. Developers rewrite code without changing the driver's behavior.

- <font color=OrangeRed>**remote wipe**</font>—The process of sending a signal to a remote device to erase all data. Useful when a mobile device is lost or stolen.

- <font color=OrangeRed>**replay attack**</font>—An attack where data is captured and replayed. Attackers typically modify data before replaying it.

- <font color=OrangeRed>**resource exhaustion**</font>—The malicious result of many DoS and DDoS attacks. Overloads a computer's resources (processor, memory), resulting in service interruption.

- <font color=OrangeRed>**retina scanners**</font>—Biometric systems that scan the retina of an eye for authentication.

- <font color=OrangeRed>**RFID attacks**</font>—Attacks against radio-frequency identification (RFID) systems. Common attacks: eavesdropping, replay, and DoS.

- <font color=OrangeRed>**RIPEMD**</font>—RACE Integrity Primitives Evaluation Message Digest. A hash function for integrity. Creates fixed-length hashes of 128, 160, 256, or 320 bits.

- <font color=OrangeRed>**risk**</font>—The possibility or likelihood of a threat exploiting a vulnerability resulting in a loss. Compare with <font color=DarkOrange>threat</font> and <font color=DarkOrange>vulnerability</font>.

- <font color=OrangeRed>**risk assessment**</font>—A process used to identify and prioritize risks. Includes quantitative and qualitative risk assessments.

- <font color=OrangeRed>**risk management**</font>—The practice of identifying, monitoring, and limiting risks to a manageable level.

- <font color=OrangeRed>**risk mitigation**</font>—The process of reducing risk by implementing controls. Reduces vulnerabilities or reduces the impact of a threat.

- <font color=OrangeRed>**risk register**</font>—A document listing information about risks. Includes risk scores and recommended security controls.

- <font color=OrangeRed>**risk response techniques**</font>—Methods used to manage risks: **accept, transfer, avoid, and mitigate**.

- <font color=OrangeRed>**rogue AP**</font>—An unauthorized AP. Can be placed by an attacker or an employee without permission.

- <font color=OrangeRed>**role-BAC**</font>—Role-based access control. An access control model that uses roles based on jobs and functions to define access. Often implemented with groups.

- <font color=OrangeRed>**root certificate**</font>—A PKI certificate identifying a root CA.

- <font color=OrangeRed>**rooting**</font>—The process of modifying an Android device, giving the user root-level (administrator) access. Compare with <font color=DarkOrange>jailbreaking</font>.

- <font color=OrangeRed>**rootkit**</font>—A type of malware that has system-level access to a computer. Rootkits can hide themselves from users and antivirus software.

- <font color=OrangeRed>**ROT13**</font>—A substitution cipher that uses a key of 13. Rotate each letter 13 spaces to encrypt or decrypt.

- <font color=OrangeRed>**round-robin**</font>—A scheduling method used with load balancers. Redirects each client request to servers in a predetermined order.

- <font color=OrangeRed>**router**</font>—A network device that connects multiple network segments together. Routes traffic based on destination IP address. Does not pass broadcast traffic. Routers use ACLs.

- <font color=OrangeRed>**RPO**</font>—Recovery point objective. The amount of data the organization can afford to lose. Identifies a point in time where data loss is acceptable. Often identified in a BIA.

- <font color=OrangeRed>**RSA**</font>—Rivest, Shamir, and Adleman. An asymmetric algorithm used to encrypt data and digitally sign transmissions.

- <font color=OrangeRed>**RSTP**</font>—Rapid Spanning Tree Protocol. An improvement of STP to prevent switching loop problems.

- <font color=OrangeRed>**RTO**</font>—Recovery time objective. The maximum amount of time it should take to restore a system after an outage. Derived from the maximum allowable outage time identified in the BIA.

- <font color=OrangeRed>**RTOS**</font>—Real-time operating system. An operating system that reacts to input within a specific time. Many embedded systems include an RTOS.

- <font color=OrangeRed>**rule-BAC**</font>—Rule-based access control. An access control model that uses rules to define access. Based on a set of approved instructions (such as an ACL) or rules that trigger in response to an event.

- <font color=OrangeRed>**runtime code**</font>—Code that is interpreted when it is executed. Compare with <font color=DarkOrange>compiled code</font>.

---

## S

- <font color=OrangeRed>**SaaS**</font>—Software as a Service. A cloud computing model that provides applications over the Internet (e.g., webmail). Compare with <font color=DarkOrange>IaaS</font> and <font color=DarkOrange>PaaS</font>.

- <font color=OrangeRed>**salt**</font>—A random set of data added to a password when creating the hash. PBKDF2 and bcrypt use salts.

- <font color=OrangeRed>**SAML**</font>—Security Assertion Markup Language. An XML-based standard used to exchange authentication and authorization information between different parties. Provides SSO for web-based applications.

- <font color=OrangeRed>**sandboxing**</font>—The use of an isolated area on a system, typically for testing. Virtual machines are often used to test patches in an isolated sandbox.

- <font color=OrangeRed>**sanitize**</font>—The process of destroying or removing all sensitive data from systems and devices. Methods: burning, shredding, pulping, pulverizing, degaussing, purging, and wiping.

- <font color=OrangeRed>**SCADA**</font>—Supervisory control and data acquisition. A system used to control an ICS (power plant, water treatment facility). Ideally within an isolated network.

- <font color=OrangeRed>**screen filter**</font>—A physical security device used to reduce visibility of a computer screen. Helps prevent shoulder surfing.

- <font color=OrangeRed>**script kiddie**</font>—An attacker with little expertise or sophistication. Uses existing scripts to launch attacks.

- <font color=OrangeRed>**Scrubbing center**</font>—Centralized <font color=blue>data cleaning stations</font> where traffic to a website is analyzed and malicious traffic is removed.

- <font color=OrangeRed>**SDN**</font>—Software defined network. A method of using software and virtualization technologies to replace hardware routers. Separates the data and control planes.

- <font color=OrangeRed>**secure boot**</font>—A process that checks and validates system files during the boot process. A TPM typically uses a secure boot process.

- <font color=OrangeRed>**secure DevOps**</font>—A software development process using an agile-aligned methodology. Considers security through the lifetime of the project.

- <font color=OrangeRed>**security incident**</font>—An adverse event or series of events that can negatively affect the confidentiality, integrity, or availability of an organization's IT systems and data.

- <font color=OrangeRed>**SED**</font>—Self-encrypting drive. A drive that includes the hardware and software necessary to encrypt a hard drive. Users typically enter credentials to decrypt and use the drive.

- <font color=OrangeRed>**separation of duties**</font>—A security principle that prevents any single person or entity from controlling all the functions of a critical or sensitive process. Designed to prevent fraud, theft, and errors.

- <font color=OrangeRed>**service account**</font>—An account used by a service or application.

- <font color=OrangeRed>**session hijacking**</font>—An attack that attempts to impersonate a user by capturing and using a session ID. Session IDs are stored in cookies.

- <font color=OrangeRed>**SFTP**</font>—Secure File Transfer Protocol. An extension of Secure Shell (SSH) used to encrypt FTP traffic. Uses **TCP port 22**.

- <font color=OrangeRed>**SHA**</font>—Secure Hash Algorithm. A hashing function used to provide integrity. Versions: SHA-1, SHA-2, SHA-3.

- <font color=OrangeRed>**Shibboleth**</font>—An open source federated identity solution.

- <font color=OrangeRed>**shimming**</font>—A driver manipulation method. Uses additional code to modify the behavior of a driver.

- <font color=OrangeRed>**shoulder surfing**</font>—The practice of looking over someone's shoulder to obtain information. A screen filter helps reduce success.

- <font color=OrangeRed>**shredding**</font>—A method of destroying data or sanitizing media. Cross-cut paper shredders cut papers into fine particles. File shredders remove all remnants by overwriting contents multiple times.

- <font color=OrangeRed>**sideloading**</font>—The process of copying an application package to a mobile device. Useful for developers, but risky if users sideload unauthorized apps.

- <font color=OrangeRed>**SIEM**</font>—Security information and event management. A security system that looks at security events throughout the organization.

- <font color=OrangeRed>**signature-based**</font>—A type of monitoring on IDS/IPS systems. Detects attacks based on known attack patterns (attack signatures).

- <font color=OrangeRed>**single point of failure**</font>—A component within a system that can cause the entire system to fail if it fails.

- <font color=OrangeRed>**SLA**</font>—Service level agreement. An agreement between a company and a vendor that stipulates performance expectations (minimum uptime, maximum downtime).

- <font color=OrangeRed>**SLE**</font>—Single loss expectancy. The monetary value of any single loss. Used with ALE and ARO. Calculation: **SLE × ARO = ALE**.

- <font color=OrangeRed>**smart card**</font>—A credit card-sized card with an embedded microchip and a certificate. Used for authentication in the "something you have" factor.

- <font color=OrangeRed>**S/MIME**</font>—Secure/Multipurpose Internet Mail Extensions. A popular standard used to secure email. Provides confidentiality, integrity, authentication, and non-repudiation.

- <font color=OrangeRed>**SMS**</font>—Short Message Service. A basic text messaging service. Compare with <font color=DarkOrange>MMS</font>.

- <font color=OrangeRed>**snapshot**</font>—A copy of a virtual machine (VM) at a moment in time. Can be used to revert the VM if problems arise later.

- <font color=OrangeRed>**SNMPv3**</font>—Simple Network Management Protocol version 3. A protocol used to monitor and manage network devices such as routers and switches.

- <font color=OrangeRed>**SoC**</font>—System on a chip. An integrated circuit that includes a computing system within the hardware. Many mobile devices include an SoC.

- <font color=OrangeRed>**social engineering**</font>—The practice of using social tactics to gain information. Social engineers attempt to gain information from people or get people to do things they wouldn't normally do.

- <font color=OrangeRed>**something you are**</font>—An authentication factor using biometrics, such as a fingerprint scanner.

- <font color=OrangeRed>**something you do**</font>—An authentication factor indicating action, such as gestures on a touch screen.

- <font color=OrangeRed>**something you have**</font>—An authentication factor using something physical, such as a smart card or token.

- <font color=OrangeRed>**something you know**</font>—An authentication factor indicating knowledge, such as a password or PIN.

- <font color=OrangeRed>**somewhere you are**</font>—An authentication factor indicating location, often using geolocation technologies.

- <font color=OrangeRed>**spam**</font>—Unwanted or unsolicited email.

- <font color=OrangeRed>**spam filter**</font>—A method of blocking unwanted email.

- <font color=OrangeRed>**spear phishing**</font>—A targeted form of phishing. Attempts to target specific groups of users or even a single user.

- <font color=OrangeRed>**split tunnel**</font>—An encrypted VPN connection where only traffic going to **private IP addresses** is encrypted. Compare with <font color=DarkOrange>full tunnel</font>.

- <font color=OrangeRed>**spyware**</font>—Software installed on users' systems without their awareness or consent. Monitors the user's computer and activity.

- <font color=OrangeRed>**SRTP**</font>—Secure Real-time Transport Protocol. A protocol used to encrypt and provide authentication for RTP traffic (audio/video streaming).

- <font color=OrangeRed>**SSH**</font>—Secure Shell. A protocol used to encrypt network traffic. Uses **TCP port 22**.

- <font color=OrangeRed>**SSID**</font>—Service set identifier. The name of a wireless network. Disabling SSID broadcast hides it from casual users.

- <font color=OrangeRed>**SSL**</font>—Secure Sockets Layer. The predecessor to TLS. Used to encrypt data-in-transit with the use of certificates.

- <font color=OrangeRed>**SSL decryptors**</font>—Devices used to create separate SSL/TLS sessions. Allow other security devices to examine encrypted traffic.

- <font color=OrangeRed>**SSL/TLS accelerators**</font>—Devices used to handle TLS traffic. Servers can off-load TLS traffic to improve performance.

- <font color=OrangeRed>**SSO**</font>—Single sign-on. An authentication method where users can access multiple resources using a single account.

- <font color=OrangeRed>**standard operating procedures (SOPs)**</font>—A document that provides step-by-step instructions on how to perform common tasks or routine operations.

- <font color=OrangeRed>**stapling**</font>—The process of appending a digitally signed OCSP response to a certificate. Reduces OCSP traffic sent to a CA.

- <font color=OrangeRed>**STARTTLS**</font>—A command (not an acronym) used to upgrade an unencrypted connection to an encrypted connection on the same port.

- <font color=OrangeRed>**steganography**</font>—The practice of hiding data within data. Example: embedding text files within an image.

- <font color=OrangeRed>**storage segmentation**</font>—A method used to isolate data on mobile devices. Allows personal data and encrypted corporate data to be stored separately.

- <font color=OrangeRed>**stored procedures**</font>—A group of SQL statements that execute as a whole. Developers use stored procedures to prevent SQL injection attacks.

- <font color=OrangeRed>**STP**</font>—Spanning Tree Protocol. A protocol enabled on most switches that protects against switching loops.

- <font color=OrangeRed>**stream cipher**</font>—An encryption method that encrypts data as a stream of bits or bytes. Compare with <font color=DarkOrange>block cipher</font>.

- <font color=OrangeRed>**substitution cipher**</font>—An encryption method that replaces characters with other characters.

- <font color=OrangeRed>**supply chain assessment**</font>—An evaluation of the supply chain needed to produce and sell a product.

- <font color=OrangeRed>**switch**</font>—A network device used to connect devices. Layer 2 switches send traffic based on MAC addresses. Layer 3 switches send traffic based on IP addresses and support VLANs.

- <font color=OrangeRed>**symmetric encryption**</font>—A type of encryption using a **single key** to encrypt and decrypt data. Compare with <font color=DarkOrange>asymmetric encryption</font>.

- <font color=OrangeRed>**system sprawl**</font>—A <font color=blue>vulnerability</font> that occurs when an organization has <font color=blue>more systems than it needs</font>, and systems it owns are <font color=blue>underutilized</font>. Compare with <font color=DarkOrange>VM sprawl</font>.

---

## T

- <font color=OrangeRed>**tabletop exercise**</font>—A <font color=blue>discussion-based exercise</font> where participants talk through an event while sitting at a table or in a conference room. Often used to test business continuity plans.

- <font color=OrangeRed>**TACACS+**</font>—Terminal Access Controller Access-Control System Plus. An authentication service that provides central authentication for remote access clients. Can be used as an alternative to RADIUS.

![TACACS+ network topology showing two TACACS+ servers connected to a PICA8 switch with three client PCs](./assets/img/post/network-tacacs-plus-topology.png)

- <font color=OrangeRed>**tailgating**</font>—A <font color=blue>social engineering attack</font> where one person follows behind another without using credentials. Mantraps help prevent tailgating.

- <font color=OrangeRed>**taps**</font>—Monitoring ports on a network device. IDSs use taps to capture traffic.

- <font color=OrangeRed>**tcpdump**</font>—A command-line protocol analyzer. Used <font color=blue>to capture packets</font>.

- <font color=OrangeRed>**technical controls**</font>—Security controls implemented through technology.

- <font color=OrangeRed>**tethering**</font>—The process of sharing an Internet connection from one mobile device to another.

- <font color=OrangeRed>**thin AP / controller-based AP**</font>—An AP that is <font color=blue>managed by a controller</font>. Compare with <font color=DarkOrange>fat AP</font>.

- <font color=OrangeRed>**third-party app store**</font>—An app store other than the primary source for mobile device apps (App Store or Google Play).

- <font color=OrangeRed>**threat**</font>—Any circumstance or event that has the potential to compromise confidentiality, integrity, or availability. Compare with <font color=DarkOrange>risk</font> and <font color=DarkOrange>vulnerability</font>.

- <font color=OrangeRed>**threat assessment**</font>—An evaluation of potential threats. Common types: environmental, manmade, internal, and external.

- <font color=OrangeRed>**three-way handshake**</font>—A method used by TCP to create a TCP/IP connection between a local host/client and server.
  - Both client and server exchange SYN, SYN-ACK, ACK packets before actual data communication begins.

![TCP three-way handshake diagram showing SYN, SYN-ACK, and ACK packet exchange between client and server](./assets/img/post/network-tcp-three-way-handshake.png)

- <font color=OrangeRed>**time-of-day restrictions**</font>—An account restriction that <font color=blue>prevents users from logging on</font> at certain times.

- <font color=OrangeRed>**TKIP**</font>—Temporal Key Integrity Protocol. A legacy <font color=blue>wireless security protocol</font>.
  - **TKIP**: older encryption protocol used with WPA. Upgrade of WEP.
  - <font color=DarkOrange>CCMP</font>: newer encryption protocol used with WPA2. (recommended replacement)

- <font color=OrangeRed>**TLS**</font>—Transport Layer Security. The replacement for SSL. Used to encrypt data-in-transit. Uses certificates issued by CAs.

- <font color=OrangeRed>**token**</font>—An authentication device or file. A hardware token is a physical device (something you have factor). A software token is a small file indicating a user has logged on.

- <font color=OrangeRed>**TOTP**</font>—Time-based One-Time Password. Similar to HOTP. Uses a timestamp instead of a counter. One-time passwords created with TOTP **expire after 30 seconds**.

- <font color=OrangeRed>**TPM**</font>—Trusted Platform Module. A hardware chip on the motherboard included with many laptops and mobile devices. Provides full disk encryption. Compare with <font color=DarkOrange>HSM</font>.

- <font color=OrangeRed>**Tracert / Traceroute**</font>—Network diagnostic commands for <font color=blue>displaying the route (path)</font> and <font color=blue>measuring transit delays</font> of packets across an IP network. Uses small TTL values. Helps identify where a connection stops or breaks (firewall, ISP, router, etc.).

- <font color=OrangeRed>**transitive trust**</font>—An indirect trust relationship created by two or more direct trust relationships.

- <font color=OrangeRed>**Trojan**</font>—Malware also known as a Trojan horse. Often looks useful, but is malicious.

- <font color=OrangeRed>**trusted operating system**</font>—An operating system configured to meet a set of security requirements. Ensures only authorized personnel can access data based on their permissions.

- <font color=OrangeRed>**Twofish**</font>—A symmetric key block cipher. Encrypts data in **128-bit blocks**, supports 128-, 192-, or 256-bit keys. Compare with <font color=DarkOrange>Blowfish</font>.

- <font color=OrangeRed>**Type I hypervisors**</font>—Bare-metal hypervisors that run directly on the system hardware. Do not need to run within an operating system.

- <font color=OrangeRed>**Type II hypervisors**</font>—Hypervisors that run as software within a host operating system. Example: Microsoft Hyper-V.

- <font color=OrangeRed>**Typo squatting / URL hijacking**</font>—The purchase of a domain name close to a legitimate domain name. Attackers try to trick users who inadvertently use the wrong domain name.

---

## U

- <font color=OrangeRed>**UAVs**</font>—Unmanned aerial vehicles. Flying vehicles piloted by remote control or onboard computers.

- <font color=OrangeRed>**UEFI**</font>—Unified Extensible Firmware Interface. A method used to boot some systems. Intended to replace BIOS firmware.

- <font color=OrangeRed>**URL hijacking**</font>—The purchase of a domain name close to a legitimate domain name. Also called typo squatting.

- <font color=OrangeRed>**USB OTG**</font>—Universal Serial Bus On-The-Go. A cable used to connect mobile devices to other devices.

- <font color=OrangeRed>**use case**</font>—A methodology used in system analysis and software engineering to identify and clarify requirements to achieve a goal.

- <font color=OrangeRed>**UTM**</font>—Unified threat management. A group of security controls combined in a single solution. UTM appliances inspect data streams for malicious content and block it.

---

## V

- <font color=OrangeRed>**VDI/VDE**</font>—Virtual desktop infrastructure / environment. Users access a server hosting virtual desktops and run the desktop operating system from the server.

- <font color=OrangeRed>**vendor diversity**</font>—The practice of implementing security controls from different vendors to increase security. Compare with <font color=DarkOrange>control diversity</font>.

- <font color=OrangeRed>**version control**</font>—A method of <font color=blue>tracking changes to software</font> as it is updated.

- <font color=OrangeRed>**virtualization**</font>—A technology that allows hosting multiple virtual machines on a single physical system. Types: Type I, Type II, and application cell/container virtualization.

- <font color=OrangeRed>**virus**</font>—<font color=blue>Malicious code</font> that attaches itself to a host application. The host application <font color=blue>must be executed</font> to run, and the malicious code executes when the host application runs.

- <font color=OrangeRed>**VLAN**</font>—Virtual local area network. A method of <font color=blue>segmenting traffic</font>. Logically groups different computers together without regard to their physical location.

- <font color=OrangeRed>**VM escape**</font>—An <font color=blue>attack</font> that allows an attacker to access the host system from within a virtual machine. Primary protection: keep hosts and guests up to date with current patches.

- <font color=OrangeRed>**VM sprawl**</font> 蔓延—A <font color=blue>vulnerability</font> that occurs when an organization has many VMs that aren't properly managed. Unmanaged VMs are not kept up to date with current patches. Compare with <font color=DarkOrange>system sprawl</font>.

- <font color=OrangeRed>**Voice recognition**</font>—A biometric method that identifies who is speaking using <font color=blue>speech recognition methods</font>.

- <font color=OrangeRed>**VPN**</font>—Virtual private network. A method that <font color=blue>provides access to a private network over a public network</font> such as the Internet.
  - <font color=DarkOrange>VPN concentrators</font>: dedicated devices used to provide VPN access to large groups of users.

- <font color=OrangeRed>**Vulnerability**</font>—A <font color=blue>weakness</font>. Can be a weakness in hardware, software, configuration, or users.
  - <font color=DarkOrange>threat</font>—Any circumstance or event that has the potential to compromise confidentiality, integrity, or availability.
  - <font color=DarkOrange>risk</font>—The <font color=blue>possibility or likelihood</font> of a threat exploiting a vulnerability resulting in a loss.

- <font color=OrangeRed>**Vulnerability scanner**</font>—A tool used to detect vulnerabilities. Identifies vulnerabilities, misconfigurations, and lack of security controls. Tests security controls **passively**.

---

## W

- <font color=OrangeRed>**warm site**</font>—An <font color=blue>alternate location</font> for operations. A compromise between an expensive hot site and a cold site. Compare with <font color=DarkOrange>cold site</font> and <font color=DarkOrange>hot site</font>.

- <font color=OrangeRed>**waterfall**</font>—A software development life cycle model using a **top-down approach**.
  - Uses multiple stages with each stage starting after the previous stage is complete.
  - Compare with <font color=DarkOrange>agile</font>.

- <font color=OrangeRed>**watering hole attack**</font>—An attack method that infects web sites that a group is likely to trust and visit.

- <font color=OrangeRed>**wearable technology**</font>—Smart devices that a person can wear or have implanted.

- <font color=OrangeRed>**web application firewall (WAF)**</font>—A firewall specifically designed to protect a web application. Inspects the contents of traffic to a web server and can detect and block malicious content.

- <font color=OrangeRed>**WEP**</font>—Wired Equivalent Privacy / Wireless Encryption Protocol. Initialization vectors are relatively small and get reused frequently. Legacy wireless security protocol.

- <font color=OrangeRed>**whaling**</font>—A form of spear phishing that attempts to target **high-level executives**.

- <font color=OrangeRed>**white box test**</font>—A type of penetration test. Testers have **full knowledge** of the environment. Compare with <font color=DarkOrange>black box test</font> and <font color=DarkOrange>gray box test</font>.

- <font color=OrangeRed>**Wi-Fi Direct**</font>—A standard that allows devices to connect without a wireless access point.

- <font color=OrangeRed>**wildcard certificate**</font>—A certificate that can be used for multiple domains with the same root domain. Starts with an asterisk (*).

- <font color=OrangeRed>**wiping**</font>—The process of completely removing all remnants of data on a disk. A bit-level overwrite writes patterns of 1s and 0s multiple times.

- <font color=OrangeRed>**wireless scanners**</font>—A network scanner that scans wireless frequency bands. Can discover rogue APs and crack passwords used by wireless APs.

- <font color=OrangeRed>**worm**</font>—Self-replicating malware that travels through a network. Worms do not need user interaction to execute.

- <font color=OrangeRed>**WPA**</font>—Wi-Fi Protected Access. A legacy wireless security protocol. Superseded by WPA2.

- <font color=OrangeRed>**WPA2**</font>—Wi-Fi Protected Access II. A wireless security protocol.
  - Supports CCMP for encryption, based on AES.
  - Can use Open mode, a pre-shared key, or Enterprise mode.

- <font color=OrangeRed>**WPS**</font>—Wi-Fi Protected Setup. A method that allows users to easily configure a wireless network using only a PIN. WPS brute force attacks can discover the PIN.

- <font color=OrangeRed>**WPS attack**</font>—An attack against an AP. Discovers the eight-digit WPS PIN and uses it to discover the AP passphrase.

---

## X

- <font color=OrangeRed>**XML**</font>—Extensible Markup Language. A language used by many databases for inputting or exporting data. Uses <font color=blue>formatting rules</font> to describe the data.

- <font color=OrangeRed>**XOR**</font>—A <font color=blue>logical operation</font> used in some encryption schemes.
  - XOR operations compare two inputs (^). If the two inputs are the **same**, it outputs **0**. If the two inputs are **different**, it outputs **1**.
  - `1 XOR 0 = 1`, `0 XOR 1 = 1`
  - `1 XOR 1 = 0`, `0 XOR 0 = 0`

- <font color=OrangeRed>**XSS (Cross-Site Scripting)**</font>—A type of injection in which malicious scripts are injected into trusted websites.
  - XSS attacks occur when an attacker uses a web application to send malicious code (generally a browser-side script) to a different end user.

---

## Z

- <font color=OrangeRed>**zero-day vulnerability**</font>—A vulnerability or bug that is unknown to trusted sources but can be exploited by attackers.
  - <font color=blue>Zero-day attacks</font> take advantage of zero-day vulnerabilities.

---

## Key Takeaways

- The CIA triad (Confidentiality, Integrity, Availability) underpins all of security.
- Risk formula: **SLE × ARO = ALE**.
- Authentication factors: something you **know**, **have**, **are**, **do**, or **somewhere you are**.
- Encryption modes: ECB (weakest), CBC (IV + XOR chain), CTM (IV + counter), GCM (CTM + hash).
- Access control models: DAC (owner-controlled), MAC (label-based), RBAC (role-based), ABAC (attribute-based), Rule-BAC (rule-triggered).
- Mobile deployment models: BYOD, COPE, CYOD.
- Backup types: full, differential (since last full), incremental (since last full or incremental).
- Recovery sites: hot (60 min), warm (hours), cold (days).
- Penetration test types: black box (zero knowledge), gray box (some knowledge), white box (full knowledge).
- Wireless security evolution: WEP → WPA (TKIP) → WPA2 (CCMP/AES).

## References

- CompTIA Security+ Study Guide (source: Scrivener backup Appendix A, created 2019-2020)
