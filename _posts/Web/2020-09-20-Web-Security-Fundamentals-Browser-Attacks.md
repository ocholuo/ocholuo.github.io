---
title: "Meow's Web Security - Web Security Fundamentals: Browser Attacks"
date: 2020-09-20 11:11:11 -0400
categories: [Web, WebSecurity]
tags: [web-security, phishing, URL-obfuscation, mobile-code, cookies, SQL-injection, click-jacking, XSS, browser-attacks]
math: false
toc: true
image: ""
---

# Web Security Fundamentals: Browser Attacks 浏览器攻击基础

---

## Overview

Web browsers are the primary interface between users and web applications, and they expose a wide attack surface: HTML rendering, client-side scripting, cookie storage, form submission, and URL parsing. This note covers the foundational browser-level attack categories — phishing, URL obfuscation, mobile code exploitation, cookie theft, and SQL injection — providing the conceptual model needed to understand how attackers abuse web primitives.

---

## HTML as an Attack Surface HTML 攻击面

<font color="blue">HTML (Hypertext Markup Language)</font> describes the content and formatting of web pages, rendered within the browser window.

**Core features exploited by attackers:**

- <font color=OrangeRed>Static document description</font>: supports linking to external pages and embedding images by reference — both linkable and embeddable resources can be weaponized
- <font color=OrangeRed>User input via forms</font>: form data sent to server-side code creates injection surfaces
- <font color=OrangeRed>Plugin / extension support</font>: additional media content (PDF, video) delivered through plugins expands the attack surface beyond the browser engine itself
- <font color=OrangeRed>Embedded programs</font>: JavaScript, Java, and other supported languages provide <font color="blue">dynamic content</font> that interacts with the user, modifies the browser UI, and can access the client environment

---

## Phishing 网络钓鱼

<font color=OrangeRed>Phishing</font> uses forged web pages to fraudulently acquire sensitive information. Users are typically directed to the phished page via a spam email.

**Most-targeted sites:**

- Financial services (e.g., Citibank)
- Payment services (e.g., PayPal)
- Auction platforms (e.g., eBay)

**Methods attackers use to avoid detection:**

- Misspelled URLs (typosquatting)
- URL obfuscation (see next section)
- Removed or forged address bar

> See the dedicated phishing note at `_posts/10CyberAttack/SocialEngineering/2018-10-5-Phishing.md` for phishing variants (spear phishing, whaling, vishing).

---

## URL Obfuscation URL 混淆

URL obfuscation techniques disguise a malicious destination as a trusted one. Three main vectors:

### URL Escape Character Attack

Old versions of Internet Explorer did not display anything past the `Esc` or `null` character, allowing attackers to inject a hidden redirect:

```
http://trusted.com%01%00@malicious.com
```

- <font color="blue">Displayed URL</font>: `http://trusted.com` (truncated at `%01%00`)
- <font color=OrangeRed>Actual destination</font>: `malicious.com`

### Unicode Homograph Attack

Domain names with Unicode characters can be registered using characters that have identical or visually similar rendering to ASCII characters:

- Example: Cyrillic `а` (U+0430) is visually indistinguishable from Latin `a`
- A PayPal phishing domain registered with Cyrillic characters renders identically to `paypal.com` in the address bar

**Defense:** Modern browsers display the <font color="blue">Punycode</font> representation (ASCII-encoded Unicode) instead of rendering the Unicode directly:

```
www.xn--pypal-4ve.com
```

### IE Image Crash (DoS via HTML)

<font color=OrangeRed>Browser implementation bugs</font> can lead to denial-of-service attacks. The classic IE image crash uses an absurdly large image dimension to crash the browser or freeze Windows:

```html
<HTML>
  <BODY>
    <IMG SRC="./imagecrash.jpg" width="9999999" height="9999999">
  </BODY>
</HTML>
```

Variations of this attack remained exploitable in later IE versions. The root cause is missing input validation on image dimension parameters in the rendering engine.

---

## Mobile Code 移动代码

<font color=OrangeRed>Mobile code</font> is an executable program sent via a computer network and executed at the destination (the browser).

**Examples:**

- <font color="blue">JavaScript</font> — interpreted by the browser; not the same as Java
- <font color="blue">ActiveX</font> — Windows-only browser plugins with broad system access
- <font color="blue">Java Plugins</font> — runs inside a sandboxed JVM embedded in the browser
- <font color="blue">Integrated Java Virtual Machines</font> — JVM built into the browser

### JavaScript click-jacking

JavaScript is a scripting language interpreted by the browser. Code is enclosed within `<script>…</script>` tags. Event handlers can be embedded directly in HTML to hijack user interactions:

```html
<!-- Event handler fires on mouse-up, opening attacker site -->
<a onMouseUp="window.open('http://www.evilsite.com')"
   href="http://www.trustedsite.com/">Trust me!</a>
```

The user sees the trusted site link but the `onMouseUp` event fires before the `href` navigation, redirecting the browser to the attacker's domain.

**Other JS attack primitives:**

- Defining hidden functions that execute on page events:

```javascript
<script type="text/javascript">
  function hello() { alert("Hello world!"); }
</script>
<img src="picture.gif" onMouseOver="javascript:hello()">
```

- Programmatic window control: `window.open("http://attacker.com")` silently opens attacker windows

---

## Cookies 会话 Cookie

<font color="blue">Cookies</font> are small pieces of information stored on the client side, associated with a specific server. Every time a browser revisits a server, it re-sends the stored cookie — effectively holding state information across sessions.

**Cookie types:**

| Type | Behavior |
|---|---|
| <font color=OrangeRed>Session cookie</font> | Deleted when the browser closes — lives only for the current session |
| <font color=OrangeRed>Non-persistent cookie</font> | Expires according to the expiry set by the server |
| <font color=OrangeRed>Persistent cookie</font> | Survives browser restarts; stored on disk until expiry |

**Security concerns:**

- Cookies can hold sensitive information: passwords, credit card numbers, session tokens, SSNs
- Storage on client disk makes cookies a theft target — malware, XSS, and cross-site request forgery (CSRF) all exploit cookie access
- Expiration is set by the server — cookies may persist far longer than the user expects
- Many sites require cookies to function, making full blocking impractical

**Mitigations:**

- Set `HttpOnly` flag — prevents JavaScript from reading the cookie
- Set `Secure` flag — cookie transmitted only over HTTPS
- Set `SameSite=Strict` — prevents cross-site request forgery by blocking cookie submission on cross-origin requests
- Clear cookies on a regular basis
- Use browser controls to exclude specific sites from setting persistent cookies

---

## SQL Injection Attack SQL 注入攻击

Many web applications take user input from a form and use it <font color=OrangeRed>directly</font> in the construction of a SQL query submitted to a database. An SQL injection attack places SQL statements inside the user input field.

### SQL Basics

<font color="blue">SQL (Standard Query Language)</font> lets applications access and manage databases — large collections of data organized in tables with fields and columns.

**Core syntax:**

```sql
SELECT column_name(s) or *
FROM table_name
WHERE column_name operator value
ORDER BY column_name ASC|DESC
LIMIT starting_row, number_of_rows
```

### Classic Login Bypass

Standard authentication query:

```sql
select * from users where user='$username' AND pwd='$password'
```

Server-side code assigns `$username` and `$password` from user form input, then passes them directly to the query. An attacker enters specially crafted strings:

```sql
-- Attacker input in both fields: M' OR '1=1
select * from users where user='M' OR '1=1' AND pwd='M' OR '1=1'
```

Because `'1=1'` is always true, the `WHERE` clause evaluates to `true` for every row — the attacker obtains access without a valid password.

**Additional injection techniques:**

- `'; DROP TABLE users; --` — destructive injection (Bobby Tables)
- `' UNION SELECT username, password FROM admin --` — data exfiltration via UNION
- `' OR 1=1 LIMIT 1 --` — returns the first row (often an admin account)

**Mitigations:**

- Use parameterized queries / prepared statements — treat user input as data, never as SQL syntax
- Apply input validation and allowlisting on all form fields
- Run the database with the minimum required privileges
- Never expose raw SQL error messages to the browser

> See the full SQL injection note at `_posts/10CyberAttack/0ApplicationServerAttacks/Injection/2020-09-17-CyberAttack-SQL_Injection.md` for advanced techniques, blind injection, and tooling.

---

## Key Takeaways

- <font color=OrangeRed>HTML's extensibility</font> (plugins, embedded scripts, forms) is the root cause of most browser-side attack surface.
- <font color=OrangeRed>Phishing</font> exploits user trust in visual URL rendering — URL obfuscation (escape chars, Unicode homographs) defeats naive visual inspection.
- <font color=OrangeRed>Punycode display</font> in modern browsers is the primary defense against Unicode homograph attacks.
- <font color=OrangeRed>Mobile code (JS, ActiveX, Java)</font> enables click-jacking, silent window opens, and event-handler hijacking — the browser sandbox is the primary containment boundary.
- <font color=OrangeRed>Cookies</font> hold session state on the client; `HttpOnly`, `Secure`, and `SameSite` flags are the three controls that reduce cookie theft surface.
- <font color=OrangeRed>SQL injection</font> works because user input is concatenated directly into queries — parameterized queries are the complete fix.

## References

- Course slides: Web Security Fundamentals (HTML, Phishing, Mobile Code, SQL Injection)
- OWASP Top 10 — A03: Injection, A05: Security Misconfiguration
- CWE-89: Improper Neutralization of Special Elements in SQL Command
- CWE-116: Improper Encoding or Escaping of Output (URL obfuscation)
- RFC 3492 — Punycode: A Bootstring encoding of Unicode for Internationalized Domain Names in Applications (IDNA)
