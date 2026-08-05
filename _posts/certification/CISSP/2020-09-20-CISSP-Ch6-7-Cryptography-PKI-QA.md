---
title: "Meow's Certification - CISSP Ch6-7: Cryptography, PKI & Applications Q&A"
date: 2020-09-20 11:11:11 -0400
categories: [Certification, CISSP]
tags: [Certification, CISSP, Cryptography, PKI, DES, AES, RSA, ECC, SHA, IPsec, DigitalSignatures, TLS]
math: false
toc: true
image:
---

# CISSP Ch6–7: Cryptography, PKI & Applications Q&A

---

## Overview

CISSP exam essentials and practice questions covering Chapters 6 and 7: symmetric and asymmetric cryptographic algorithms, hash functions, PKI, digital signatures, secure protocols (TLS, IPsec, S/MIME, PGP), and cryptographic attacks. Each practice question includes the correct answer with an explanation.

---

## Chapter 6 — Cryptography and Symmetric Key Algorithms

### Exam Essentials 考试要点

#### <font color="#fb02ff">CIA Goals in Cryptosystems 密码系统中的CIA目标</font>

| Goal | Description |
|---|---|
| <font color=OrangeRed>Confidentiality 机密性</font> | Protects the secrecy of data at rest and in transit |
| <font color=OrangeRed>Integrity 完整性</font> | Assures the recipient that data was not altered between creation and access |
| <font color=OrangeRed>Nonrepudiation 不可否认性</font> | Provides undeniable proof that the sender authored a message; prevents the sender from subsequently denying it |

#### <font color="#fb02ff">Authentication via Cryptosystems 认证</font>

<font color="blue">Authentication provides assurances as to the identity of a user.</font> The <font color=OrangeRed>challenge-response protocol</font> asks the remote user to encrypt a message using a key known only to the communicating parties. Authentication can be achieved with both symmetric and asymmetric cryptosystems.

#### <font color="#fb02ff">Basic Terminology 基本术语</font>

- <font color="blue">Plaintext</font>: unencrypted message
- <font color="blue">Ciphertext</font>: encrypted message produced by applying an algorithm and key to plaintext
- <font color="blue">Encryption</font>: sender applies algorithm + key to plaintext → ciphertext
- <font color="blue">Decryption</font>: recipient applies algorithm + key to ciphertext → plaintext

#### <font color="#fb02ff">Codes vs. Ciphers 编码与密码</font>

| Type | Description |
|---|---|
| <font color=OrangeRed>Codes</font> | Operate on words or phrases; sometimes secret but don't always provide confidentiality |
| <font color=OrangeRed>Ciphers</font> | Always meant to hide the true meaning of a message |

**Cipher types 密码类型:**

| Cipher | How it works |
|---|---|
| <font color="blue">Transposition cipher</font> | Rearranges the location of characters within a message |
| <font color="blue">Substitution cipher</font> | Replaces characters with other characters (e.g., Caesar cipher) |
| <font color="blue">One-time pad</font> | Substitution cipher using a random key as long as the message — unbreakable when used correctly |
| <font color="blue">Stream cipher</font> | Operates on individual characters or bits |
| <font color="blue">Block cipher</font> | Operates on large fixed-size blocks of data |
| <font color="blue">Running key cipher</font> | Uses a passage from a well-known book as the encryption key |

#### <font color="#fb02ff">One-Time Pad Requirements 一次性密码本要求</font>

For a one-time pad to be unbreakable, **all four** conditions must hold:

1. The key must be generated **randomly** without any known pattern.
2. The key must be **at least as long** as the message to be encrypted.
3. The pad must be **protected against physical disclosure**.
4. Each pad must be used **only once** and then discarded.

> **VENONA failure:** Soviet cryptanalysts in the 1940s reused one-time pad keys — violating rule 4 — allowing US cryptanalysts to break the cipher.

#### <font color="#fb02ff">Advanced Concepts 高级概念</font>

| Concept | Description |
|---|---|
| <font color=OrangeRed>Zero-knowledge proof</font> | A specific type of information is exchanged but no real data is transferred — as with digital signatures and digital certificates |
| <font color=OrangeRed>Split knowledge</font> | Information required to perform an operation is divided among multiple users so that no single person can compromise security alone |
| <font color=OrangeRed>M of N Control</font> | A minimum of M agents out of N total agents must cooperate to perform high-security tasks — an example of split knowledge |
| <font color=OrangeRed>Work function / Work factor</font> | Measures the strength of a cryptosystem by the effort (cost and time) required to perform a complete brute-force attack; security is directly proportional to work function value |

#### <font color="#fb02ff">Key Length and Security 密钥长度与安全性</font>

- Modern cryptosystems use keys of **at least 128 bits** for adequate security.
- <font color=OrangeRed>DES 56-bit key is no longer considered secure</font> — insufficient against modern brute-force attacks.
- Key space for an n-bit key = **2^n** possible keys.

#### <font color="#fb02ff">Symmetric vs. Asymmetric Cryptosystems 对称与非对称密码系统</font>

| Property | Symmetric (Secret Key) | Asymmetric (Public Key) |
|---|---|---|
| Keys | Single shared secret key | Public-private key pair |
| Speed | <font color="blue">Much faster</font> | Much slower |
| Key distribution | Difficult | Easy — public key freely shared |
| Scalability | Poor — n(n-1)/2 keys for n users | Good — 2n keys for n users |
| Nonrepudiation | Not supported | Supported |

**Key count formula 密钥数量公式:**

- Symmetric: `n(n-1)/2` keys for n participants (e.g., 10 users → 45 keys)
- Asymmetric: `2n` keys for n participants (e.g., 10 users → 20 keys)

#### <font color="#fb02ff">Data Encryption Standard (DES) DES加密标准</font>

- Key length: <font color=OrangeRed>56 bits</font> (no longer secure)
- Block size: 64 bits

**DES operating modes DES工作模式:**

| Mode | Notes |
|---|---|
| <font color="blue">ECB (Electronic Codebook)</font> | Least secure; identical plaintext blocks produce identical ciphertext blocks; suitable only for short messages |
| <font color="blue">CBC (Cipher Block Chaining)</font> | Each block XORed with the previous ciphertext block; an early error propagates through all subsequent blocks |
| <font color="blue">CFB (Cipher Feedback)</font> | Stream cipher mode; an error propagates to subsequent blocks |
| <font color="blue">OFB (Output Feedback)</font> | Stream cipher mode; errors do **not** propagate — safe for large messages where error isolation is needed |

#### <font color="#fb02ff">Triple DES (3DES)</font>

- Uses **three iterations** of DES with two or three different keys.
- Effective key strength: <font color=OrangeRed>112 bits (2-key) or 168 bits (3-key)</font>.

#### <font color="#fb02ff">Advanced Encryption Standard (AES) AES高级加密标准</font>

- Algorithm: <font color=OrangeRed>Rijndael</font>
- US government standard for sensitive but unclassified data.
- Key lengths: **128, 192, or 256 bits**
- Block size: **128 bits** (fixed, despite Rijndael supporting variable block sizes)

**AES finalists AES候选算法:**

| Algorithm | Notable feature |
|---|---|
| <font color="blue">Rijndael</font> | Selected as AES |
| <font color="blue">Twofish</font> | Uses prewhitening and postwhitening techniques |
| <font color="blue">Blowfish</font> | Earlier Schneier algorithm; variable key length |
| <font color="blue">Skipjack</font> | NSA-designed; 80-bit key; used in Clipper chip |

#### <font color="#fb02ff">Frequency Analysis Attack 频率分析攻击</font>

<font color=OrangeRed>Frequency analysis</font> exploits the fact that letters occur with predictable frequency in natural language. It makes simple substitution ciphers (such as the Caesar cipher) virtually unusable.

---

### Chapter 6 Practice Questions 练习题

**Q1.** How many possible keys exist in a 4-bit key space?
> **C. 16** — 2^4 = 16 possible key values.

**Q2.** What cryptographic goal convinces John that Bill was actually the sender of a message?
> **A. Nonrepudiation** — provides undeniable proof of message authorship.

**Q3.** What is the key length of DES?
> **A. 56 bits**

**Q4.** What type of cipher changes the location of characters to achieve confidentiality?
> **B. Transposition cipher**

**Q5.** Which is NOT a valid AES key length?
> **A. 56 bits** — Rijndael supports 128, 192, and 256 bits only.

**Q6.** Which cannot be achieved by a secret key (symmetric) cryptosystem?
> **A. Nonrepudiation** — nonrepudiation requires a public key cryptosystem; symmetric keys are shared and cannot prove sole authorship.

**Q7.** When correctly implemented, what is the only unbreakable cryptosystem?
> **D. One-time pad** — mathematically unbreakable when all four requirements are met.

**Q8.** What is the output of 16 mod 3?
> **B. 1** — 16 = 5×3 + 1, so 16 mod 3 = 1.

**Q9.** What rule did the Soviets break that caused VENONA to succeed?
> **C. Key values must be used only once** — the Soviets reused one-time pad keys, breaking the fundamental requirement.

**Q10.** Which cipher type operates on large pieces of a message rather than individual characters or bits?
> **C. Block cipher**

**Q11.** What is the minimum number of keys required for secure two-way communication in symmetric cryptography?
> **A. One** — both parties share a single symmetric key.

**Q12.** Dave's escrow system requires multiple people but not all participants. What technique is he using?
> **B. M of N Control** — requires a minimum of M agents (out of N total) to cooperate; not all participants must be present.

**Q13.** Which DES mode can be used for large messages with assurance that an early error won't spoil the entire communication?
> **D. Output Feedback (OFB)** — errors do not propagate in OFB mode; CBC and CFB both propagate errors.

**Q14.** Many algorithms rely on the difficulty of factoring large prime products. What characteristic are they relying on?
> **C. It is a one-way function** — a mathematical operation that is easy to compute in one direction but computationally infeasible to reverse.

**Q15.** How many keys are required for a symmetric algorithm with 10 participants?
> **C. 45** — n(n-1)/2 = 10×9/2 = 45.

**Q16.** What block size does AES use?
> **C. 128 bits** — AES uses a fixed 128-bit block size, even though Rijndael supports variable block sizes.

**Q17.** What attack makes the Caesar cipher virtually unusable?
> **C. Frequency analysis attack** — exploits predictable letter frequencies in natural language.

**Q18.** What type of cryptosystem uses a passage from a well-known book as the key?
> **B. Running key cipher**

**Q19.** Which AES finalist uses prewhitening and postwhitening?
> **B. Twofish**

**Q20.** How many encryption keys are required for an asymmetric algorithm with 10 participants?
> **B. 20** — asymmetric requires 2n keys (one public + one private per participant).

---

## Chapter 7 — PKI and Cryptographic Applications

### Exam Essentials 考试要点

#### <font color="#fb02ff">Asymmetric Key Usage Rules 非对称密钥使用规则</font>

| Operation | Key to use |
|---|---|
| <font color=OrangeRed>Encrypt a message to recipient</font> | Recipient's **public** key |
| <font color=OrangeRed>Decrypt a received message</font> | Own **private** key |
| <font color=OrangeRed>Sign a message (digital signature)</font> | Own **private** key |
| <font color=OrangeRed>Verify a signature</font> | Sender's **public** key |

#### <font color="#fb02ff">Major Public Key Cryptosystems 主要公钥密码系统</font>

| Algorithm | Basis | Notes |
|---|---|---|
| <font color=OrangeRed>RSA</font> | Difficulty of factoring the product of large prime numbers | Most famous; invented by Rivest, Shamir, Adleman in 1977 |
| <font color=OrangeRed>El Gamal</font> | Modular arithmetic (extension of Diffie-Hellman) | Ciphertext is twice the length of plaintext |
| <font color=OrangeRed>ECC (Elliptic Curve)</font> | Elliptic curve discrete logarithm problem | Provides more security per bit than RSA; 160-bit ECC ≈ 1,024-bit RSA |

#### <font color="#fb02ff">Hash Function Requirements 哈希函数要求</font>

A good hash function must:

1. Accept input of **any length**
2. Produce **fixed-length** output
3. Be **easy to compute** for any input
4. Provide **one-way** functionality (computationally infeasible to reverse)
5. Be **collision-free** (infeasible to find two inputs with the same hash)

#### <font color="#fb02ff">Major Hashing Algorithms 主要哈希算法</font>

| Algorithm | Output size | Notes |
|---|---|---|
| <font color="blue">SHA-1</font> | 160 bits | Government standard; now considered weak |
| <font color="blue">SHA-2</font> | 224–512 bits (variable) | Current standard; includes SHA-256, SHA-512 |
| <font color="blue">SHA-3</font> | Variable | Next generation; different internal design from SHA-2 |
| <font color="blue">MD5</font> | 128 bits | Considered broken; collision-vulnerable |

#### <font color="#fb02ff">Cryptographic Salts 加密盐值</font>

<font color=OrangeRed>Rainbow table attacks</font> use precomputed hash values to identify commonly used passwords. <font color="blue">Adding a salt</font> (a random value appended to the password before hashing) makes each hash unique and defeats rainbow table lookups.

#### <font color="#fb02ff">Digital Signatures 数字签名</font>

**To sign 签名过程:**

1. Apply a hash function to the message → produce a **message digest**.
2. Encrypt the digest with the sender's **private key** → the digital signature.

**To verify 验证过程:**

1. Decrypt the signature with the sender's **public key** → obtain the message digest.
2. Independently compute the hash of the received message.
3. If the two digests match → the message is authentic and unmodified.

#### <font color="#fb02ff">Digital Signature Standard (DSS)</font>

DSS uses <font color="blue">SHA-1 or SHA-2</font> message digest functions combined with one of three signature algorithms:

| Algorithm | Notes |
|---|---|
| <font color="blue">DSA (Digital Signature Algorithm)</font> | Original DSS algorithm |
| <font color="blue">RSA</font> | Widely used alternative |
| <font color="blue">ECDSA (Elliptic Curve DSA)</font> | ECC-based; efficient for constrained devices |

> **Note:** El Gamal DSA is **not** part of the DSS standard.

#### <font color="#fb02ff">Public Key Infrastructure (PKI)</font>

- <font color=OrangeRed>Certificate Authorities (CAs)</font> generate digital certificates containing users' public keys.
- Users distribute certificates to communicating parties.
- Recipients verify a certificate using the **CA's public key**.
- Standard: <font color=OrangeRed>ITU X.509</font> governs the format and endorsement of digital certificates.
- <font color="blue">Key escrow</font> stores a copy of private keys; used for recovery if the original private key is lost.
- <font color=OrangeRed>Certificate Revocation Lists (CRLs)</font> have a key disadvantage: **latency** — time between revocation and distribution of the updated CRL leaves a window of exposure.

#### <font color="#fb02ff">Secure Email 安全电子邮件</font>

| Protocol | Notes |
|---|---|
| <font color=OrangeRed>S/MIME</font> | Emerging standard; built into most modern email clients; uses RSA and X.509 certificates |
| <font color=OrangeRed>PGP (Pretty Good Privacy)</font> | Phil Zimmerman's tool; commercial version uses <font color="blue">IDEA</font> for encryption |

#### <font color="#fb02ff">Secure Web Activity 安全网络通信</font>

- <font color=OrangeRed>TLS (Transport Layer Security)</font> is the de facto standard for HTTPS (port **443**).
- <font color=OrangeRed>SSL</font> is the older predecessor — many sites are dropping SSL support due to security concerns.
- <font color=OrangeRed>WEP</font> is considered flawed and should no longer be used.
- <font color="blue">WPA</font> uses <font color=OrangeRed>TKIP</font> for encryption; <font color="blue">WPA2</font> uses <font color=OrangeRed>AES</font>.
- WPA protects the **client to wireless access point** link only.

#### <font color="#fb02ff">IPsec 网络安全协议</font>

<font color=OrangeRed>IPsec</font> is a security architecture framework for secure communication over IP. It defines a **framework** for setting up secure communication channels.

| Mode | Encryption scope | Use case |
|---|---|---|
| <font color="blue">Transport mode</font> | Packet payload only | Peer-to-peer communication |
| <font color="blue">Tunnel mode</font> | Entire packet (header + payload) | Gateway-to-gateway VPN |

**IPsec protocols:**

| Protocol | Function |
|---|---|
| <font color="blue">AH (Authentication Header)</font> | Provides authentication and integrity; no encryption |
| <font color="blue">ESP (Encapsulating Security Payload)</font> | Provides authentication, integrity, and encryption |

#### <font color="#fb02ff">Cryptographic Attacks 密码攻击</font>

| Attack | Description |
|---|---|
| <font color=OrangeRed>Brute-force</font> | Exhaustively tries all possible keys |
| <font color=OrangeRed>Known plaintext</font> | Attacker has both plaintext and corresponding ciphertext samples |
| <font color=OrangeRed>Chosen ciphertext</font> | Attacker can choose ciphertexts and obtain their decryptions |
| <font color=OrangeRed>Chosen plaintext</font> | Attacker can choose plaintexts and obtain their encryptions |
| <font color=OrangeRed>Meet-in-the-middle</font> | Exploits protocols using two rounds of encryption; why Double DES (2DES) is no more effective than single DES |
| <font color=OrangeRed>Man-in-the-middle</font> | Fools both parties into communicating through the attacker |
| <font color=OrangeRed>Birthday attack</font> | Attempts to find collisions in hash functions |
| <font color=OrangeRed>Replay attack</font> | Reuses previously captured authentication requests |

#### <font color="#fb02ff">Digital Rights Management (DRM)</font>

<font color="blue">DRM solutions</font> allow content owners to enforce usage restrictions on their content (music, movies, e-books, enterprise documents). They control how content can be copied, redistributed, or accessed.

---

### Chapter 7 Practice Questions 练习题

**Q1.** In the RSA public key cryptosystem, which number is always largest?
> **B. n** — n is the product of two large prime numbers p and q; n is always larger than either p or q individually.

**Q2.** Which cryptographic algorithm forms the basis of El Gamal?
> **B. Diffie-Hellman** — El Gamal is an extension of the Diffie-Hellman key exchange algorithm.

**Q3.** Richard wants to send an encrypted message to Sue. Which key does he use to encrypt?
> **C. Sue's public key** — to encrypt a message for a recipient, use the recipient's public key. If Richard used his own private key, any user could decrypt it with Richard's freely available public key.

**Q4.** A 2,048-bit plaintext message encrypted with El Gamal — how long is the resulting ciphertext?
> **C. 4,096 bits** — El Gamal ciphertext is twice the length of the plaintext.

**Q5.** A company using 1,024-bit RSA wants to convert to ECC with equivalent strength. What ECC key length?
> **A. 160 bits** — a 1,024-bit RSA key is cryptographically equivalent to a 160-bit ECC key; ECC provides more security per bit.

**Q6.** John hashes a 2,048-byte message using SHA-1. What size is the message digest?
> **A. 160 bits** — SHA-1 always produces a 160-bit digest regardless of input size.

**Q7.** Which technology is considered flawed and should no longer be used?
> **C. WEP** — Wired Equivalent Privacy has known cryptographic weaknesses and is deprecated.

**Q8.** What encryption does WPA use?
> **A. TKIP** — WPA uses TKIP; WPA2 uses AES.

**Q9.** Richard received an encrypted message from Sue. Which key decrypts it?
> **B. Richard's private key** — messages encrypted with the recipient's public key are decrypted with the recipient's private key.

**Q10.** Richard wants to digitally sign a message to Sue. Which key encrypts the digest?
> **B. Richard's private key** — signing uses the sender's own private key; Sue verifies using Richard's public key.

**Q11.** Which algorithm is NOT supported by the Digital Signature Standard?
> **C. El Gamal DSA** — DSS supports DSA, RSA, and ECDSA only.

**Q12.** Which ITU standard governs digital certificates for secure electronic communication?
> **B. X.509**

**Q13.** Which cryptosystem provides encryption for the commercial version of PGP?
> **B. IDEA** — the commercial version of PGP uses the IDEA cipher.

**Q14.** What TCP/IP port is used by TLS traffic?
> **C. 443** — HTTPS/TLS uses port 443.

**Q15.** What attack rendered Double DES (2DES) no more effective than single DES?
> **C. Meet-in-the-middle attack** — the attacker can attack the two encryption layers from both ends simultaneously, reducing the effective security.

**Q16.** Which tool improves the effectiveness of a brute-force password cracking attack?
> **A. Rainbow tables** — precomputed hash-to-plaintext lookups accelerate cracking of unsalted password hashes.

**Q17.** WPA encryption protects which link?
> **C. Client to wireless access point** — WPA encrypts the wireless segment between the client device and the access point.

**Q18.** What is the major disadvantage of certificate revocation lists (CRLs)?
> **B. Latency** — time between certificate revocation and distribution of the updated CRL creates a window where revoked certificates may still be trusted.

**Q19.** Which encryption algorithm is now considered insecure?
> **D. Merkle-Hellman Knapsack** — broken in 1982; no longer considered secure.

**Q20.** What does IPsec define?
> **B. A framework for setting up a secure communication channel** — IPsec specifies the architecture and protocols for establishing secure IP communications.

---

## Key Takeaways

- <font color=OrangeRed>CIA in cryptography</font>: Confidentiality (secrecy), Integrity (unmodified), Nonrepudiation (proven authorship) — nonrepudiation requires asymmetric crypto
- <font color=OrangeRed>One-time pad</font>: the only mathematically unbreakable cipher — requires random key, key ≥ message length, single use, physical protection
- <font color=OrangeRed>Key counts</font>: symmetric needs n(n-1)/2 keys; asymmetric needs 2n keys — asymmetric scales far better
- <font color=OrangeRed>DES (56-bit) is broken</font>; AES (Rijndael) with 128/192/256-bit keys and 128-bit block size is the current standard
- <font color=OrangeRed>OFB mode</font> does not propagate errors; CBC and CFB do — choose OFB for large messages requiring error isolation
- <font color="blue">Asymmetric key rules</font>: encrypt → recipient's public key; decrypt → own private key; sign → own private key; verify → sender's public key
- <font color=OrangeRed>ECC efficiency</font>: 160-bit ECC ≈ 1,024-bit RSA in security strength
- <font color=OrangeRed>El Gamal</font> doubles ciphertext length; extends Diffie-Hellman; forms basis of PGP commercial encryption (IDEA)
- <font color=OrangeRed>DSS</font> supports DSA, RSA, and ECDSA — El Gamal is NOT part of DSS
- <font color=OrangeRed>X.509</font> is the ITU standard for digital certificates; CRL latency is the key weakness
- <font color=OrangeRed>IPsec</font>: transport mode encrypts payload; tunnel mode encrypts entire packet — uses AH (auth only) and ESP (auth + encryption)
- <font color=OrangeRed>Meet-in-the-middle attack</font> breaks Double DES — made 2DES no stronger than single DES
- <font color=OrangeRed>WEP is broken</font>; WPA uses TKIP; WPA2 uses AES
- <font color="blue">Rainbow tables</font> accelerate brute-force on unsalted hashes — salting defeats them
- <font color=OrangeRed>Work function</font> measures cryptographic strength — security is proportional to the cost/time of brute-force attack

## References

- CISSP Study Guide — Chapter 6: Cryptography and Symmetric Key Algorithms
- CISSP Study Guide — Chapter 7: PKI and Cryptographic Applications
- NIST FIPS 197 — Advanced Encryption Standard (AES)
- NIST FIPS 186 — Digital Signature Standard (DSS)
- ITU-T X.509 — Digital Certificate Standard
- RFC 4301 — Security Architecture for IPsec
