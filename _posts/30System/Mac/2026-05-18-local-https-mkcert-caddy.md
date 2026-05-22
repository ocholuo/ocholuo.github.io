---
title: "Meow's MacOS - Local HTTPS with mkcert and Caddy 本地 HTTPS 配置"
date: 2026-05-18 11:11:11 -0400
categories: [30System, MacOS]
tags: [MacOS, https, mkcert, caddy, local-dev, ssl, ios, reverse-proxy]
math: false
toc: true
---

# Local HTTPS with mkcert and Caddy 本地 HTTPS 配置

---

## Overview

iPhone Safari enforces HTTPS-Only mode and rejects plain `http://` addresses, blocking access to local development servers. This note covers how to use <font color=OrangeRed>mkcert</font> to create a locally trusted SSL certificate signed by a custom CA, and <font color=OrangeRed>Caddy</font> as an HTTPS reverse proxy that forwards traffic to a local HTTP dev server. The CA is installed on the Mac and trusted on the iPhone via AirDrop, enabling mobile testing without a real domain or public CA.

---

## 为什么要做这件事

iPhone Safari 默认开启 **HTTPS-Only 模式**，拒绝访问 `http://` 地址。
本地开发服务器（如 `http://192.168.1.100:3100`）是 HTTP，所以手机打不开。

解决方案：在 Mac 上用 **mkcert** 生成本地受信任的 SSL 证书，再用 **Caddy** 反向代理，把 HTTPS 请求转发给本地 HTTP 服务器。

---

## 核心概念

### SSL 证书是什么？

浏览器信任 HTTPS 的前提是：证书由**受信任的机构（CA）签发**。
公网用 Let's Encrypt 等真实 CA，本地开发用 **mkcert** 创建一个"本地 CA"，然后手动让设备信任它。

```text
                  ┌──────────────────────────┐
iPhone Safari     │    Mac 本机               │
  │               │                          │
  │  https://<LAN_IP>:3443                   │
  ├─────────────►│  Caddy (HTTPS, port 3443) │
  │               │       │                  │
  │  证书由 mkcert CA 签发  │       ▼          │
  │  iPhone 已信任此 CA    │  localhost:3100  │
  │               │  (HTTP 开发服务器)         │
  └◄──────────────┤                          │
     返回页面内容   └──────────────────────────┘
```

### mkcert 做了什么？

1. 在本机创建一个本地 CA（根证书）
2. 用这个 CA 签发针对局域网 IP 的 SSL 证书
3. 把 CA 根证书安装到 Mac 系统信任链

### Caddy 做了什么？

Caddy 是配置极简的 Web 服务器。它监听 HTTPS 端口（`3443`），用 mkcert 证书加密，然后把流量转发到本机的 HTTP 服务器（`localhost:3100`）。

---

## 操作步骤

### 第一步：安装工具

```bash
brew install mkcert caddy
```

### 第二步：创建本地 CA 并安装到 Mac

```bash
mkcert -install
# 需要输入 sudo 密码
```

这一步在 Mac 系统钥匙串中安装了 mkcert 的根证书，Mac 上的浏览器从此信任它签发的所有证书。

### 第三步：为局域网 IP 生成证书

先确认 Mac 的局域网 IP：

```bash
ipconfig getifaddr en0
# 示例输出：192.168.1.100
```

在项目目录下生成证书：

```bash
cd /path/to/project
mkcert <LAN_IP>
```

生成两个文件：

- `<LAN_IP>.pem` — 证书（公钥）
- `<LAN_IP>-key.pem` — 私钥

### 第四步：写 Caddyfile

文件位置：`/path/to/project/Caddyfile`

```text
{
  admin off
}

https://<LAN_IP>:3443 {
  tls /path/to/project/<LAN_IP>.pem /path/to/project/<LAN_IP>-key.pem
  reverse_proxy localhost:3100
}
```

| 指令 | 作用 |
|---|---|
| `admin off` | 关闭 Caddy 管理 API（沙盒/受限环境需要） |
| `tls` | 指定证书和私钥路径 |
| `reverse_proxy` | 把请求转发到本地 HTTP 服务器 |

### 第五步：把 CA 根证书发到 iPhone

```bash
open "$(mkcert -CAROOT)"
# 打开 Finder 窗口，找到 rootCA.pem
```

右键 `rootCA.pem` → **Share → AirDrop** → 发给 iPhone

### 第六步：iPhone 安装并信任证书

**安装：**

```
Settings → General → VPN & Device Management → 找到 mkcert profile → Install
```

**信任（关键步骤，不做则 HTTPS 握手失败）：**

```
Settings → General → About → Certificate Trust Settings → mkcert 那条 → 打开开关 → Continue
```

### 第七步：启动 Caddy

```bash
caddy run --config /path/to/project/Caddyfile
```

### 第八步：手机访问

```
https://<LAN_IP>:3443/<path>
```

---

## 每次使用流程（配置完成后）

```bash
# 终端 1：启动开发服务器
PORT=3100 pnpm dev

# 终端 2：启动 Caddy
caddy run --config /path/to/project/Caddyfile
```

手机访问 `https://<LAN_IP>:3443`

---

## 常见问题

### 为什么端口是 3443 而不是 443？

标准 HTTPS 端口是 443，但监听 443 需要 root 权限。
用 3443 可以让普通用户运行 Caddy，不需要 `sudo`。

### 证书有效期

mkcert 生成的证书有效期约 **2 年**。过期后重新运行 `mkcert <LAN_IP>` 生成新证书即可，不需要重新在 iPhone 上安装 CA 根证书（CA 本身不过期）。

---

## 相关文件位置

| 文件 | 路径 |
|---|---|
| mkcert CA 根证书 | `~/Library/Application Support/mkcert/rootCA.pem` |
| 项目证书（公钥） | `<project-dir>/<LAN_IP>.pem` |
| 项目私钥 | `<project-dir>/<LAN_IP>-key.pem` |
| Caddyfile | `<project-dir>/Caddyfile` |

---

## Meow's Security Considerations 安全注意事项

此配置仅用于本地开发，它刻意削弱了标准 TLS 信任模型以满足测试需求。只要该设置处于活跃状态，下列攻击面就客观存在，与使用意图无关。

This setup deliberately weakens the standard TLS trust model. The attack surface below exists as long as the setup is active, regardless of intent.

| Severity 严重程度 | Concern 问题 |
|---|---|
| <font color=OrangeRed>Critical 严重</font> | CA 根证书私钥泄露 |
| <font color=OrangeRed>High 高</font> | 单层 CA 架构 — PKI 最弱结构 |
| <font color=OrangeRed>High 高</font> | iOS CA 信任范围过广 |
| <font color=OrangeRed>High 高</font> | 私钥提交到版本库 |
| <font color=OrangeRed>High 高</font> | 开发服务器局域网暴露 |
| **Medium 中** | ARP 欺骗 + CA 密钥组合攻击 |
| **Medium 中** | CORS 通配符 + CSRF |
| **Medium 中** | 会话固定攻击 |
| **Medium 中** | XSS 利用 HTTPS 安全上下文 |
| **Medium 中** | 缺失 CSP 响应头 |
| **Medium 中** | AirDrop 社会工程学 CA 安装 |
| **Medium 中** | iOS 信任持久化与无吊销机制 |
| Low 低 | 数据包嗅探与端口扫描 |
| Low 低 | Caddy 到开发服务器的明文链路 |
| Low 低 | TLS 版本与密码套件配置 |
| Low 低 | mkcert 供应链完整性 |

---

### 1. CA Root Key Compromise 根证书私钥泄露 — Critical

<font color=OrangeRed>此配置中影响最严重的安全问题。 / Highest impact concern in this setup.</font>

mkcert 在 `~/Library/Application Support/mkcert/rootCA-key.pem` 生成 CA 私钥。该私钥可为**任意域名**签发证书，而不仅限于开发使用的局域网 IP。一旦攻击者获取 `rootCA-key.pem`，可以：

mkcert generates a CA private key at `~/Library/Application Support/mkcert/rootCA-key.pem`. This key can sign a certificate for **any domain** — not just the LAN IP used for dev. If an attacker obtains `rootCA-key.pem`, they can:

1. 为 `apple.com`、`google.com` 或任意银行网站签发伪造证书 / Issue a forged certificate for `apple.com`, `google.com`, or any banking site
2. 对 iPhone 的所有 HTTPS 流量实施全量 TLS 中间人攻击 / Perform full TLS MITM on all HTTPS traffic from the iPhone (banking apps, OAuth flows, email)
3. 解密历史 HTTPS 会话（若 TLS 会话未使用前向保密）/ Decrypt previously captured HTTPS sessions if forward secrecy was not in use

iPhone 无法察觉此攻击 —— 该证书在 Certificate Trust Settings 中被明确信任。
The iPhone has no mechanism to detect this — the cert is explicitly trusted in Certificate Trust Settings.

**攻击向量 Attack Vectors:**

- Mac 上存在读取 `~/Library/Application Support/mkcert/` 权限的恶意软件 / Malware on the Mac with read access to the mkcert directory
- 物理接触未锁屏的机器 / Physical access to an unlocked machine
- 备份文件窃取（Time Machine、未加密的 `~/Library/` 云同步）/ Backup theft (Time Machine, unencrypted `~/Library/` cloud sync)
- mkcert 二进制被污染 / Compromised mkcert binary (see Supply Chain concern)

**MITRE ATT&CK:** T1552.004 (Private Keys), T1557 (MITM)

**缓解措施 Mitigation:**

```bash
# 立即限制私钥文件权限 / Restrict key file permissions immediately
chmod 600 "$(mkcert -CAROOT)/rootCA-key.pem"
ls -la "$(mkcert -CAROOT)/"
```

不进行移动端测试时，从 iPhone 完全移除 CA。
Remove the CA from iPhone entirely when mobile testing is not needed:
`Settings → General → VPN & Device Management → mkcert → Remove`

---

### 2. Single-Tier CA — Weakest PKI Hierarchy 单层 CA 架构缺陷 — High

根据 PKI 理论，CA 层级结构分为单层、双层、三层，安全性依次递增。mkcert 生成的 CA 是**单层架构**：根 CA = 签发 CA，两者合一，是最弱的 PKI 设计。

PKI hierarchy ranges from one-tier (weakest) to three-tier (strongest). mkcert creates a **single-tier CA** where the root CA and the issuing CA are the same entity — the weakest possible design.

- **双层架构（生产环境主流）**将根 CA 设为离线状态，私钥物理隔离，签发 CA 在线运行。mkcert 的根 CA 私钥始终在线，直接暴露于网络威胁。
  **Two-tier architecture (production standard)** keeps the root CA offline with physically isolated private key; the issuing CA runs online. The mkcert root CA private key is always online, directly exposed to network threats.

- **三层架构**支持"分支吊销"——当某个子 CA 被吊销时，其他分支不受影响。mkcert 无此能力：根 CA 密钥泄露后所有已签发证书立即全部失效，无法选择性吊销。
  **Three-tier architecture** supports branch-level revocation — revoking one sub-CA leaves other branches intact. mkcert has no such capability: a root key compromise invalidates every issued certificate simultaneously, with no selective revocation.

- 公共 CA（DigiCert、Comodo 等）须通过 WebTrust 审计、加入证书透明度日志。mkcert CA 完全绕过上述监管，iPhone 无从区分。
  Public CAs (DigiCert, Comodo, etc.) undergo WebTrust audits and participate in Certificate Transparency logs. The mkcert CA bypasses all of these controls — the iPhone cannot distinguish it from a legitimate CA.

**CWE-295** (Improper Certificate Validation) — 信任模型降级 / Trust model degradation

**缓解措施 Mitigation:** 将 CA 视为临时凭证，测试结束立即销毁。若需要长期使用本地 CA，考虑使用 [step-ca](https://smallstep.com/docs/step-ca/) 搭建支持 ACME 和 OCSP 的双层本地 CA。
Treat the CA as a temporary credential and destroy it after testing. For long-term use, consider [step-ca](https://smallstep.com/docs/step-ca/) to run a two-tier local CA with ACME and OCSP support.

---

### 3. Overly Broad iOS CA Trust Scope iOS 证书信任范围过广 — High

在 iPhone 上安装并信任 mkcert CA 后，该 CA 成为**系统级受信任根证书**，对所有 App 和所有域名生效——功能上等同于 DigiCert、Comodo 等公共 CA。iOS 不会将信任范围限制在 `192.168.x.x` 或特定 App。

Installing and trusting the mkcert CA on iPhone makes it a **system-level trusted root** that applies to all apps and all domains — functionally equivalent to a public CA like DigiCert or Comodo. iOS does not scope the trust to `192.168.x.x` or to specific apps.

这意味着：/ This means:

- iPhone 上每一个 HTTPS 连接（Safari、Chrome、原生 App）都会接受该 CA 签发的任意证书 / Every HTTPS connection from the iPhone (Safari, Chrome, native apps) will accept any cert signed by this CA
- 持有 CA 密钥的中间人攻击者可冒充 iPhone 联系的任意 TLS 端点 / An attacker with the CA key can impersonate any TLS endpoint the phone contacts
- Apple 的 App Transport Security (ATS) 对用户手动安装的 CA 不施加额外限制 / Apple's ATS does not add extra restrictions for user-installed CAs

**与标准 PKI 对比 Comparison with Standard PKI:** 公共 CA 具有受约束的证书签发范围、接受 WebTrust 审计、加入证书透明度日志。mkcert CA 上述控制全部缺失。
Public CAs have constrained certificate scopes, WebTrust audits, and CT log participation. The mkcert CA has none of these controls.

**CWE-295** (Improper Certificate Validation), **CWE-296** (Improper Following of Chain of Trust)

**缓解措施 Mitigation:** 将 CA 视为临时凭证，开发/测试 session 结束后立即从 iOS 移除。
Treat the CA as temporary. Remove it from iOS immediately after each dev/test session ends.

---

### 4. Private Key Committed to Version Control 私钥提交到版本库 — High

证书文件生成于项目目录内，常见失误是运行 `git add .` 时意外将私钥一并提交。一旦私钥进入 git 历史记录，即使删除后仍可永久恢复。

Certificate files are generated inside the project directory. A common mistake is running `git add .` and accidentally committing the private key. Once in git history, the key is permanently recoverable even after deletion.

```
<project-dir>/
  <LAN_IP>.pem          # 公钥证书 — 低敏感度 / public cert — low sensitivity
  <LAN_IP>-key.pem      # 私钥 — 高敏感度 / private key — HIGH sensitivity
  Caddyfile             # 配置文件 — 低敏感度 / config — low sensitivity
```

公开仓库泄露意味着任何人都可以：/ A public repo exposure allows anyone to:

- 在未来的会话中冒充服务器 / Impersonate the server in future sessions
- 解密在 Caddy 运行期间捕获的 HTTPS 流量（若未使用前向保密）/ Decrypt any HTTPS traffic captured while Caddy was running (if forward secrecy was not used)

**CWE-312** (Cleartext Storage of Sensitive Information), **CWE-321** (Use of Hard-coded Cryptographic Key)

**缓解措施 Mitigation — 生成证书后立即添加到 `.gitignore` / Add to `.gitignore` immediately after cert generation:**

```bash
# <project-dir>/.gitignore
*.pem
*-key.pem
Caddyfile
```

提交前验证无证书文件被暂存 / Verify no cert files are staged before committing:
```bash
git status --short | grep '\.pem'
```

---

### 5. Dev Server Exposed Over LAN 开发服务器局域网暴露 — High

Caddy 绑定到 `<LAN_IP>:3443`，使开发应用对**同一 Wi-Fi 网络中的所有设备**可访问。开发服务器通常有意放宽安全控制。

Caddy binds to `<LAN_IP>:3443`, making the development application reachable by **every device on the same Wi-Fi network**. Dev servers routinely run with security controls intentionally weakened.

| 开发服务器特征 Dev Server Characteristic | 安全影响 Security Implication |
|---|---|
| 身份认证禁用或 mock / Auth disabled or mocked | 局域网中任意设备均可访问受保护路由 / Any LAN device can access protected routes |
| CORS 设为 `*` / CORS set to `*` | 接受来自任意来源的跨域请求 / Cross-origin requests accepted from any origin |
| 调试端点开放 / Debug endpoints active | Source map、内部状态、热更新 WebSocket 暴露 / Source maps, internal state, hot-reload sockets exposed |
| 详细错误信息 / Verbose error messages | 内部路径、包名、查询逻辑泄露 / Internal paths, package names, query logic revealed |
| Staging 凭证 / Staging credentials in env | 凭证可通过网络响应获取 / Credentials visible in network responses |
| 无速率限制 / No rate limiting | 暴力破解不受约束 / Brute-force attempts go unchecked |

**来自机密性攻击笔记 From Confidentiality Attacks Notes:**
局域网内的攻击者可将网卡置于**混杂模式**，使用 Wireshark 捕获明文流量。Nmap 等工具可轻易发现 `<LAN_IP>:3443` 端口，识别正在运行的 Caddy 服务，为进一步攻击提供情报。
An attacker on the LAN can place a NIC in **promiscuous mode** and capture plaintext traffic with Wireshark. Tools like Nmap can easily discover port 3443, identify the running Caddy service, and gather intelligence for follow-on attacks.

**缓解措施 Mitigation:** 移动端测试时优先使用独立隔离网络（家庭路由器、个人热点）；避免使用生产或 staging 凭证；如条件允许，使用支持客户端隔离的 VLAN。
Prefer an isolated private network (home router, personal hotspot) for mobile testing. Avoid running with production or staging credentials. Use client-isolation VLAN when available.

---

### 6. ARP Spoofing + CA Key Pivot ARP 欺骗与 CA 密钥组合攻击 — Medium

ARP 缓存投毒允许同一局域网内的攻击者将发往 `<LAN_IP>` 的流量重定向至自己的机器。

ARP cache poisoning allows an attacker on the same LAN to redirect traffic destined for `<LAN_IP>` to their own machine.

**ARP 协议的固有漏洞 ARP Protocol Vulnerability:**

- ARP 无身份验证机制，设备会无条件信任任何 ARP 回复包，包括未经请求的 Gratuitous ARP。/ ARP has no authentication — devices unconditionally trust any ARP reply, including unsolicited Gratuitous ARP packets.
- Linux ARP 缓存默认保留 60 秒，Windows 约 30-45 秒；攻击者需持续发送伪造回复以维持投毒状态。/ Linux ARP cache expires in 60s, Windows in 30-45s; the attacker must keep sending spoofed replies to maintain the poisoned state.
- 常用攻击工具（**Ettercap**、**arpspoof**、**Cain and Abel**）免费可得，攻击门槛极低。/ Common attack tools (Ettercap, arpspoof, Cain and Abel) are freely available — the barrier to entry is very low.

**两步组合攻击 Two-Step Combined Attack:**

1. 攻击者获得 CA 根密钥（见问题 #1）或服务器叶证书私钥（见问题 #4）/ Attacker obtains the CA root key (concern #1) or the server leaf key (concern #4)
2. 对 iPhone ARP 缓存投毒，将 `<LAN_IP>` 重定向至攻击者机器 / ARP-poison the iPhone's cache to redirect `<LAN_IP>` to the attacker's machine
3. 用 mkcert CA 签发的伪造证书完成 TLS 握手（iPhone 信任该 CA）/ Complete the TLS handshake with a forged cert signed by the mkcert CA (iPhone trusts it)
4. 充当透明 MITM 代理，iPhone 看到有效 HTTPS，所有流量被截获 / Act as a transparent MITM proxy — iPhone sees valid HTTPS while all traffic is intercepted

**ARP DoS 变种 ARP DoS Variant:**
攻击者向局域网广播伪造的默认网关 MAC 地址，所有设备缓存错误 MAC 后无法到达网关，整个局域网断网。
An attacker broadcasting a bogus default gateway MAC address causes all devices to cache the wrong MAC, cutting off all network egress — a denial-of-service against the entire LAN segment.

**MITRE ATT&CK:** T1557.002 (ARP Cache Poisoning), T1498 (DoS)

**缓解措施 Mitigation:** 在路由器上启用 802.1X 端口安全或客户端隔离；仅在受信任的私有网络中使用此配置；在服务器和工作站上配置静态 ARP 条目可作为额外防御层。
Enable 802.1X port security or client isolation on the router. Use this setup only on a trusted private network. Configuring static ARP entries on servers and workstations adds an extra defensive layer.

---

### 7. CORS Wildcard and CSRF CORS 通配符与跨站请求伪造 — Medium

若开发服务器返回 `Access-Control-Allow-Origin: *`，并且开发者同时浏览了任意网站，该网站的 JavaScript 就可以向 `https://<LAN_IP>:3443` 发起请求并读取响应。

If the dev server returns `Access-Control-Allow-Origin: *`, any website the developer browses while the dev server is running can make requests to `https://<LAN_IP>:3443` and read the responses.

**CSRF 攻击路径 CSRF Attack Path:**
CSRF 需要两个要素：(1) 执行操作的 Web 应用，(2) 已认证的用户。开发服务器往往同时满足这两个条件。
CSRF requires two elements: (1) a web application that performs actions, (2) an authenticated user. A dev server routinely satisfies both conditions simultaneously.

更危险的配置：`Access-Control-Allow-Origin: *` 与 `Access-Control-Allow-Credentials: true` 同时存在，允许恶意站点使用浏览器存储的 Cookie 发送认证请求，触发账号修改、数据删除或 Token 泄露。
A more dangerous misconfiguration: `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true` allows the malicious site to send authenticated requests using the browser's stored cookies, triggering account modification, data deletion, or token exfiltration.

**GET 请求的 CSRF 风险 CSRF via GET Requests:**
CSRF 笔记指出：*"If the web site support any action via an HTML link"* — 通过 GET 请求触发状态变更的端点同样存在 CSRF 风险，而开发服务器经常为调试方便提供此类端点。
As noted in the CSRF study note: *"If the web site supports any action via an HTML link"* — endpoints that trigger state changes via GET requests are equally vulnerable, and dev servers often expose such endpoints for debugging convenience.

**CWE-352** (Cross-Site Request Forgery), **CWE-942** (Overly Permissive Cross-domain Whitelist)

**缓解措施 Mitigation:** 即使在开发环境也要将 CORS 配置为允许指定来源，而非通配符。
Even in development, configure CORS to allow only the specific origin rather than a wildcard.

```javascript
// Express example / Express 示例
app.use(cors({ origin: `https://<LAN_IP>:3443` }));
```

---

### 8. Session Fixation 会话固定攻击 — Medium

来自 CSRF 笔记的补充攻击模式。攻击者先登录开发应用获取一个会话 ID，再通过特制链接诱导受害者使用该固定 Session ID 登录，随后以受害者身份访问应用。

Sourced from the CSRF study note. The attacker logs into the dev app to obtain a session ID, then tricks the victim into authenticating with that fixed session ID via a crafted link, after which the attacker uses the same session ID to access the app as the victim.

**攻击的前提条件 Preconditions:**

- 开发服务器允许通过 URL 参数传递 Session ID / Dev server accepts session IDs via URL parameter
- 服务器在用户登录后未刷新 Session ID（未做 Session Rotation）/ Server does not rotate the session ID after login (no session rotation)
- 浏览器存有持久化认证信息（Cookie 或缓存）/ Browser retains persistent auth state (cookie or cache)

**开发环境的特殊风险 Dev-Specific Risk:**
开发服务器通常不实现 Session Rotation，登录状态经常通过 URL 参数或 LocalStorage 而非 HttpOnly Cookie 维护，进一步扩大攻击面。
Dev servers rarely implement session rotation. Auth state is often stored in URL parameters or LocalStorage rather than HttpOnly cookies, significantly widening the attack surface.

**MITRE ATT&CK:** T1563 (Remote Service Session Hijacking), **CWE-384** (Session Fixation)

**缓解措施 Mitigation:** 用户登录后立即使旧 Session 失效并生成新 Session ID；避免在 URL 参数中传递 Session ID；使用 `HttpOnly` + `SameSite=Strict` 的 Cookie 存储会话令牌。
Invalidate the old session and issue a new session ID immediately after login. Never transmit session IDs in URL parameters. Store session tokens in `HttpOnly` + `SameSite=Strict` cookies.

---

### 9. XSS Exploiting HTTPS Secure Context XSS 利用 HTTPS 安全上下文 — Medium

来自 XSS 笔记的交叉参考。XSS 攻击（存储型、反射型、DOM 型）注入恶意 JavaScript 并在受害者浏览器中执行。开发服务器通过 Caddy 暴露于 HTTPS 后，浏览器将其视为**安全上下文（Secure Context）**，这反而扩大了 XSS 的危害范围。

Cross-referenced from the XSS study note. XSS attacks (stored, reflected, DOM-based) inject malicious JavaScript that executes in the victim's browser. Once the dev server is served over HTTPS via Caddy, the browser treats it as a **Secure Context**, which unlocks more powerful browser APIs for XSS to abuse.

**HTTPS 安全上下文解锁的浏览器 API / Secure Context APIs unlocked for XSS abuse:**

| API | XSS 利用方式 / XSS Exploitation |
|---|---|
| `localStorage` / `sessionStorage` | 读取存储的 Token、用户数据 / Read stored tokens and user data |
| Service Worker 注册 / Service Worker registration | 注册持久化 SW，长期拦截请求 / Register a persistent SW to intercept future requests |
| WebAuthn / Credential Management | 尝试注册恶意凭证 / Attempt to register malicious credentials |
| Geolocation, Camera, Microphone | 在受信任 Origin 上更易请求敏感权限 / Sensitive permissions more likely granted on a trusted origin |
| `navigator.sendBeacon` | 静默将窃取数据发送至外部服务器 / Silently exfiltrate stolen data to an external server |

XSS 笔记还指出：开发服务器暴露 Source Map，攻击者可通过 DOM 型 XSS 更容易地定位代码中的注入点。
The XSS study note also notes that exposed source maps allow attackers to locate injection points in the source code more easily, amplifying DOM-based XSS attacks.

**MITRE ATT&CK:** T1059.007 (JavaScript), **CWE-79** (Cross-Site Scripting)

**缓解措施 Mitigation:** 在开发服务器上启用输入验证；配置 CSP 响应头（见下一条）；在 Caddyfile 中限制 Source Map 公开访问。
Enable input validation on the dev server. Configure a CSP header (see next concern). Restrict source map access in the Caddyfile.

---

### 10. Missing Content-Security-Policy Header 缺失 CSP 响应头 — Medium

来自 XSS 笔记：Content Security Policy (CSP) 是防御 XSS 的核心机制，指示浏览器限制脚本来源、禁止内联执行、限制数据外传目标。开发服务器通常不配置 CSP，而 Caddy 可在反向代理层以零成本注入该头。

From the XSS study note: Content Security Policy (CSP) is the primary browser-enforced defense against XSS — it restricts script sources, blocks inline execution, and limits data exfiltration targets. Dev servers rarely configure CSP, but Caddy can inject it at the proxy layer at zero cost.

缺少 CSP 意味着 / Without CSP:

- XSS 的 JavaScript 可自由加载任意外部脚本、向任意域名发送数据 / XSS JavaScript can load arbitrary external scripts and send data to any domain
- `eval()`、内联 `<script>` 等高危操作不受限制 / High-risk operations like `eval()` and inline `<script>` are unrestricted
- 攻击者可通过 `document.cookie` 窃取 Cookie，通过 `fetch` 将数据外传 / Attackers can steal cookies via `document.cookie` and exfiltrate data via `fetch`

**在 Caddyfile 中添加基础 CSP / Adding CSP in Caddyfile:**

```text
https://<LAN_IP>:3443 {
  tls /path/to/<LAN_IP>.pem /path/to/<LAN_IP>-key.pem
  reverse_proxy localhost:3100
  header {
    Content-Security-Policy "default-src 'self'; script-src 'self'; object-src 'none';"
    X-Frame-Options "DENY"
    X-Content-Type-Options "nosniff"
  }
}
```

注意：过严的 CSP 会导致开发应用功能异常（如热更新 WebSocket 被拦截），需根据框架实际需求调整。
Note: An overly strict CSP may break dev app features (e.g., hot-reload WebSockets). Tune the policy based on the framework's actual requirements.

**CWE-79** (XSS), **CWE-693** (Protection Mechanism Failure)

---

### 11. Social Engineering via AirDrop CA Distribution AirDrop 社会工程学 CA 安装 — Medium

AirDrop 用于将 `rootCA.pem` 传输到 iPhone，此步骤产生了社会工程学攻击面。附近的攻击者可发送一个显示名称几乎相同的恶意 CA 证书，若用户安装并信任，攻击者即获得 iPhone 上的系统级受信任根证书。

AirDrop is used to transfer `rootCA.pem` to the iPhone, creating a social engineering attack surface. A nearby attacker can send a malicious CA cert with a nearly identical display name. If the user installs and trusts it, the attacker gains a system-trusted root on the iPhone.

iOS 在安装配置文件时显示证书的 `Common Name` 字段，但该名称由签发者控制，无法区分合法 CA 与恶意 CA。这与部分 MDM 系统和间谍软件在 iOS 上安装持久化 MITM 能力的方式在技术上完全相同。
iOS shows the certificate's `Common Name` field during profile installation, but that name is attacker-controlled — there is no visual indicator distinguishing a legitimate dev CA from a malicious one. This is functionally identical to how some MDM systems and stalkerware install persistent MITM capability on iOS.

**MITRE ATT&CK:** T1566 (Phishing), T1553.004 (Install Root Certificate)

**缓解措施 Mitigation:** 安装前在 Mac 和 iPhone 上分别验证 SHA-256 指纹是否一致。
Verify the SHA-256 fingerprint matches on both Mac and iPhone before trusting.

```bash
openssl x509 -in "$(mkcert -CAROOT)/rootCA.pem" -fingerprint -sha256 -noout
```

安全要求较高时使用 USB 数据线传输代替 AirDrop。
Use a USB cable transfer instead of AirDrop when higher security is required.

---

### 12. iOS Trust Persistence + No Revocation 信任持久化与无吊销机制 — Medium

iOS 上安装的 CA 证书永久有效，直至手动移除。开发结束后开发者通常忘记清理，留下长期暴露的信任根。
Installed CA certificates on iOS are persistent — they remain trusted until manually removed. Developers commonly forget to clean up after a project, leaving a long-lived trusted root on the device.

**来自 PKI 笔记的吊销机制缺失 / From PKI Notes — revocation infrastructure absent:**

| 标准 PKI 机制 Standard PKI Mechanism | mkcert CA 状态 mkcert CA Status |
|---|---|
| CRL Distribution Point (CDP) 证书吊销列表 | 缺失 — 无法发布吊销列表 / Absent — no revocation list can be published |
| OCSP 在线证书状态协议 | 缺失 — 无法实时查询状态 / Absent — no real-time status query possible |
| Authority Information Access (AIA) | 缺失 — 无中间 CA 下载地址 / Absent — no intermediate CA download location |
| Certificate Transparency Log 证书透明度日志 | 缺失 — 无公开审计记录 / Absent — no public audit trail |

Apple's ATS 不对用户手动安装的 CA 执行吊销检查。mkcert CA 本身无过期时间，CA 密钥一旦泄露，iPhone 将无限期信任该 CA，且无法通过任何标准 PKI 机制吊销。
Apple's ATS does not enforce revocation checks for user-installed CAs. The mkcert CA itself never expires. Once the CA key is compromised, the iPhone trusts it indefinitely with no standard PKI revocation path.

**缓解措施 Mitigation:** 将"移除 iPhone 上的 CA"纳入项目收尾检查清单。
Add "remove mkcert CA from iPhone" to the project shutdown checklist.
`Settings → General → VPN & Device Management → mkcert development CA → Remove`

---

### 13. Packet Sniffing and Port Scanning 数据包嗅探与端口扫描 — Low

**来自机密性攻击笔记 From Confidentiality Attacks Notes:**

局域网内的攻击者可将网卡置于**混杂模式**，使用 Wireshark 等工具捕获流经该网段的所有数据包。
An attacker on the LAN can place a NIC in **promiscuous mode** and use Wireshark to capture all packets traversing that network segment.

- HTTPS 加密了 iPhone 到 Caddy 的链路，混杂模式嗅探无法解密该流量。/ HTTPS encrypts the iPhone-to-Caddy leg — promiscuous sniffing cannot decrypt it.
- 但 Caddy 到 `localhost:3100` 的 HTTP 明文链路可被同机运行的进程（如 `tcpdump -i lo0 port 3100`）捕获。/ However, the Caddy-to-`localhost:3100` HTTP leg is visible to local processes with loopback capture access.

**端口扫描发现开发服务器 Port Scanning:**

```bash
# 攻击者在局域网中可轻易执行 / Trivially executed by an attacker on the LAN
nmap -sV <LAN_IP> -p 3443
# 输出 output: 3443/tcp open ssl/http Caddy httpd
```

端口扫描可识别运行中的服务类型（Caddy）和 TLS 版本，为针对 Caddy 已知 CVE 的漏洞利用提供情报。
Port scanning identifies the running service (Caddy) and TLS version, providing intelligence for exploiting Caddy-specific CVEs in follow-on attacks.

**缓解措施 Mitigation:** 在受信任的私有网络中接受此风险；或使用防火墙规则限制 3443 端口仅对特定 IP 开放。
Accept this risk on a trusted private network, or use firewall rules to restrict port 3443 to specific IPs only.

```bash
# macOS pf 规则示例 / macOS pf firewall example (allow only iPhone IP)
pass in on en0 proto tcp from <IPHONE_IP> to <LAN_IP> port 3443
block in on en0 proto tcp to <LAN_IP> port 3443
```

---

### 14. HTTP Internal Leg Caddy 到开发服务器的明文链路 — Low

Caddy 到 `localhost:3100` 的连接是明文 HTTP。虽然回环流量在 OS 网络栈内部流转，不经过物理网卡，但仍可被：
The connection from Caddy to `localhost:3100` is plain HTTP. Although loopback traffic stays within the OS network stack and never hits the physical NIC, it can still be read by:

- 具有 loopback 捕获权限的本地进程（`sudo tcpdump -i lo0 port 3100`）/ Local processes with loopback capture access
- 共享主机网络的 Docker 容器（`--network host`）/ Docker containers sharing the host network
- 若 Caddyfile 启用了 `log`，则明文记录在 Caddy 的访问日志中 / Caddy access logs, if `log` is enabled in the Caddyfile

在受信任的单用户环境中风险较低，但若机器运行了不可信容器、CI Runner 或多用户账号则风险上升。
Risk is low in a trusted single-user environment, but increases when the machine runs untrusted containers, CI runners, or shared user accounts.

**缓解措施 Mitigation:** 若开发服务器支持 TLS，在 Caddyfile 中配置加密内部链路；否则在受信任的单用户本地环境中接受此风险。
If the dev server supports TLS, configure an encrypted internal leg in the Caddyfile; otherwise accept this risk for pure local development.

```text
reverse_proxy localhost:3100 {
  transport http {
    tls
  }
}
```

---

### 15. TLS Version and Cipher Suite TLS 版本与密码套件配置 — Low

本笔记的 Caddyfile 未显式指定最低 TLS 版本或密码套件约束。Caddy 2.x 默认强制 TLS 1.2+ 并使用现代密码套件，配置尚可。但旧版 Caddy 或自定义 `tls` 块可能启用较弱配置。
This note's Caddyfile does not explicitly set a minimum TLS version or cipher suite constraints. Caddy 2.x defaults to TLS 1.2+ with modern cipher suites, which is acceptable. However, older Caddy versions or custom `tls` blocks may enable weaker settings.

在 Caddyfile 中显式硬化 TLS 设置 / Explicit TLS hardening in Caddyfile:

```text
https://<LAN_IP>:3443 {
  tls /path/to/<LAN_IP>.pem /path/to/<LAN_IP>-key.pem {
    protocols tls1.2 tls1.3
    ciphers TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 TLS_CHACHA20_POLY1305_SHA256
  }
  reverse_proxy localhost:3100
}
```

**CWE-326** (Inadequate Encryption Strength), **CWE-327** (Use of Broken or Risky Cryptographic Algorithm)

---

### 16. mkcert Supply Chain Integrity mkcert 供应链完整性 — Low

mkcert 通过 Homebrew 安装。若 Homebrew formula 或 mkcert 二进制被篡改，可能导致：
mkcert is installed via Homebrew. A compromised Homebrew formula or mkcert binary could:

- 安装后门 CA（将 CA 私钥发送至远程服务器）/ Install a backdoored CA that sends the CA private key to a remote server
- 生成含攻击者控制扩展的证书 / Generate certificates containing attacker-controlled extensions
- 在执行 `mkcert -install`（需要 sudo）时运行任意代码 / Run arbitrary code during `mkcert -install` (which requires sudo)

**MITRE ATT&CK:** T1195.001 (Compromise Software Dependencies and Development Tools)

**缓解措施 Mitigation:** 首次使用前验证 mkcert 二进制 SHA 哈希，并与官方发布页面的哈希值对比。
Verify the mkcert binary SHA hash before first use and compare against the published hash on the official releases page.

```bash
brew info mkcert
shasum -a 256 "$(which mkcert)"
# 与 / Compare against: https://github.com/FiloSottile/mkcert/releases
```

---

### Summary Table 汇总表

| # | 问题 Concern | MITRE / CWE | 本文档状态 Status |
|---|---|---|---|
| 1 | CA 根密钥泄露 CA root key compromise | T1552.004, T1557 | 需手动缓解 Manual action required |
| 2 | 单层 CA 架构 Single-tier CA | CWE-295 | 设计取舍 Design tradeoff |
| 3 | iOS CA 信任范围过广 Overly broad iOS trust | CWE-295, CWE-296 | 需手动移除 Remove when done |
| 4 | 私钥提交版本库 Private key in VCS | CWE-312, CWE-321 | 需添加 .gitignore Add .gitignore |
| 5 | 局域网暴露 LAN exposure | — | 受信任网络可接受 Trusted network |
| 6 | ARP 欺骗 + DoS ARP spoofing + DoS | T1557.002, T1498 | 两步攻击，低概率高影响 |
| 7 | CORS 通配 + CSRF CORS wildcard + CSRF | CWE-352, CWE-942 | 在开发服务器中配置 Fix in dev server |
| 8 | 会话固定 Session fixation | T1563, CWE-384 | 在开发服务器中配置 Fix in dev server |
| 9 | XSS 利用安全上下文 XSS secure context | T1059.007, CWE-79 | 输入验证 + CSP Input validation + CSP |
| 10 | 缺失 CSP Missing CSP | CWE-79, CWE-693 | 在 Caddyfile 中添加 Add to Caddyfile |
| 11 | AirDrop 社会工程 AirDrop social engineering | T1566, T1553.004 | 验证指纹 Verify fingerprint |
| 12 | iOS 信任持久化 + 无吊销 Trust persistence + no CRL | — | 项目结束手动移除 Remove at project end |
| 13 | 嗅探 + 端口扫描 Sniffing + port scan | — | 受信任网络可接受 Trusted network |
| 14 | 内部 HTTP 明文链路 Internal HTTP leg | — | 单用户本地可接受 Accepted local risk |
| 15 | TLS 版本配置 TLS config | CWE-326, CWE-327 | Caddy 2.x 默认可接受 Defaults acceptable |
| 16 | 供应链完整性 Supply chain | T1195.001 | 验证二进制哈希 Verify binary hash |

---

## Key Takeaways

- iPhone Safari's HTTPS-Only mode blocks plain HTTP local dev servers — mkcert + Caddy is the standard fix.
- mkcert creates a local CA and issues a cert for the LAN IP; the CA must be installed AND explicitly trusted on iOS (two separate steps in Settings).
- Caddy listens on port 3443 (not 443) to avoid requiring root; it terminates TLS and reverse-proxies to the HTTP dev server.
- Only the fix commit (not version-bump commits) should be cherry-picked when back-porting to main — same discipline applies to cert files: never commit private key files (`-key.pem`) to version control.
- After initial setup, daily use is just two terminal commands: start the dev server, then `caddy run`.

## References

- [mkcert — locally trusted development certificates](https://github.com/FiloSottile/mkcert)
- [Caddy — fast, multi-platform web server with HTTPS](https://caddyserver.com/docs/)
