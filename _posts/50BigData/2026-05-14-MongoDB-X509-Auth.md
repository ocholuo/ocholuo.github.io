---
title: "Meow's BigData - MongoDB X.509 Authentication"
date: 2026-05-14 11:11:11 -0400
categories: [00Basic, 50BigData]
tags: [mongodb, x509, authentication, tls, certificates, nosql, security]
math: false
toc: true
---

# MongoDB X.509 Authentication

---

## Overview

MongoDB supports <font color=OrangeRed>X.509 client certificate authentication</font> as an alternative to username/password. Instead of a stored password, the client presents a TLS certificate whose subject string acts as the username. MongoDB verifies the cert against a trusted CA and looks up the subject string in the `$external` database to determine the user's roles.

This pattern is common in service-to-service scenarios (e.g., a backend pod connecting to a MongoDB replica set) where you want to avoid storing secrets in plaintext and instead rely on PKI infrastructure.

---

## How X.509 Auth Works 认证原理

```
Client (app)                     MongoDB
   │                                │
   │── TLS handshake ──────────────►│
   │   presents client certificate  │
   │                                │  1. Verify cert is signed by trusted CA
   │                                │  2. Extract subject string from cert
   │                                │  3. Look up subject string in $external DB
   │                                │  4. Assign roles from matching user document
   │◄── connection established ─────│
```

Key insight: **the certificate subject string IS the username**. There is no separate username field. If the subject string from the presented cert does not exactly match a user document in `$external`, authentication fails — even if the cert is valid and CA-signed.

认证关键点：证书的 Subject 字符串就是用户名。即使证书本身合法，只要 Subject 与 `$external` 中的用户记录不完全匹配，认证就会失败。

---

## The `$external` Database

X.509 users are stored in a special virtual database called `$external`. This database holds all externally-authenticated accounts — X.509, LDAP, and Kerberos. No passwords are stored in MongoDB for these users.

X.509 用户存储在 `$external` 虚拟数据库中，不保存任何密码。

To inspect a user:

```javascript
// Connect to the replica set as an admin, then:
db.getSiblingDB("$external").getUser("<subject-string>")

// Or shorthand on the $external db:
use $external
db.getUser("C=US,ST=YourState,O=Your Org,OU=management:group.12345,CN=svc-myapp.corp.example.com")
```

---

## Reading `db.getUser()` Output / 解读用户记录

Example output:

```javascript
{
  _id: '$external.C=US,ST=YourState,O=Your Org,OU=management:group.12345,CN=svc-myapp-replicaset-dbname.corp.example.com',
  userId: UUID('b0890c1b-9c89-4e88-bd36-4dd059f27d53'),
  user: 'C=US,ST=YourState,O=Your Org,OU=management:group.12345,CN=svc-myapp-replicaset-dbname.corp.example.com',
  db: '$external',
  roles: [ { role: 'APP_OWNER_ROLE', db: 'mydb' } ],
  mechanisms: [ 'external' ]
}
```

**Field-by-field breakdown / 字段说明:**

| Field | Meaning |
| --- | --- |
| `_id` | MongoDB's internal document ID — always `$external.<subject-string>` for X.509 users. Auto-constructed, never set manually. |
| `userId` | System-generated UUID for audit logs and change tracking. Appears in `mongod` logs when this user authenticates. |
| `user` | The actual MongoDB username — the full certificate subject string, exactly as produced by `openssl x509 -subject -nameopt RFC2253`. This is what MongoDB compares against the connecting client's cert. |
| `db` | Always `$external` for X.509 users. Indicates the credential is externally managed (no password in MongoDB). |
| `roles` | Array of `{ role, db }` objects. Each entry grants a named role scoped to one specific database. |
| `mechanisms` | `["external"]` means TLS certificate auth only — no SCRAM, no password challenge. |

**The `roles` field in detail / roles 字段说明:**

```javascript
roles: [ { role: 'APP_OWNER_ROLE', db: 'mydb' } ]
```

- `role` — the named role granted (can be a built-in role like `readWrite`, or a custom role defined by the DBA team)
- `db` — the database this role applies to; the user cannot access other databases unless additional role entries exist

---

## Certificate and Subject String 证书与 Subject 字符串

### Subject String Format

A MongoDB X.509 subject string follows RFC2253 format:

```
C=US,ST=<State>,O=<Organization>,OU=<OrgUnit>,CN=<CommonName>
```

The CN (Common Name) is the most meaningful part — it typically encodes the service identity and environment.

### Common Naming Convention / 常用命名约定

```
<user>-<replicaset>-<dbname>.corp.example.com
```

- `<user>` — service role or identifier (e.g., `svc-myapp`, `svc-myapp-owner`, `svc-myapp-ro`)
- `<replicaset>` — optional; the MongoDB replica set name
- `<dbname>` — optional; the target database name

**CN length constraint:** keep everything after `/CN=` at or below 64 characters — this is the OpenSSL safe limit for standards-compliant CSRs.

**CN 长度限制：** `/CN=` 之后的内容不超过 64 个字符，超过可能导致 CSR 不合规。

---

## Creating a New X.509 User 创建 X.509 用户

### Step 1 — Generate Private Key and CSR

```bash
openssl req -new -newkey rsa:2048 -sha256 \
  -keyout svc-myapp-replicaset-mydb.corp.example.com.key.pem \
  -subj "/CN=svc-myapp-replicaset-mydb.corp.example.com" \
  -out svc-myapp-replicaset-mydb.corp.example.com.csr
```

This produces two files:

- `.key.pem` — your private key (keep this secret, never commit to git)
- `.csr` — the certificate signing request (safe to share)
- **File naming rule:** both files must share the same prefix and differ only by extension.

### Step 2 — Request Certificate from Internal CA

Submit the `.csr` to your organization's internal certificate authority (e.g., an internal certificate manager portal). Select the appropriate certificate type and management group for your team.

将 `.csr` 提交至内部证书管理系统，选择正确的证书类型和管理组。

Download the signed `.cert.pem` file when the request is approved.

### Step 3 — Merge Private Key + Certificate

```bash
cat svc-myapp-replicaset-mydb.corp.example.com.key.pem > svc-myapp.pem
cat svc-myapp-replicaset-mydb.corp.example.com.cert.pem >> svc-myapp.pem
```

The merged file (`svc-myapp.pem`) is the `certkey.pem` used by the application. It starts with `-----BEGIN PRIVATE KEY-----` (or `BEGIN ENCRYPTED PRIVATE KEY` if you added a passphrase) and ends with `-----END CERTIFICATE-----`.

### Step 4 — Download CA Certificate Chain

Also download the issuer and chain PEM files from the certificate manager. Concatenate them to form the `CA.pem` used to verify the server:

```bash
cat chain.pem > CA.pem
cat issuer.pem >> CA.pem
```

### Step 5 — Extract Subject String

```bash
openssl x509 -in svc-myapp.pem -inform PEM -subject -nameopt RFC2253 
# Output example: 
subject= C=US,ST=YourState,O=Your Org,OU=management:group.12345,CN=svc-myapp-replicaset-mydb.corp.example.com
```

This exact string (starting from `C=US,...`) is what you send to the DBA team.

### Step 6 — DBA Creates the MongoDB User

Share with the DBA team:

```bash
Replica set / cluster: <host1:port1,host2:port2,...>
Database: <dbname>
Requested role: <readWrite / owner / read-only>
Subject string: C=US,ST=YourState,O=Your Org,OU=management:group.12345,CN=svc-myapp-replicaset-mydb.corp.example.com
```

The DBA runs something like:

```javascript
db.getSiblingDB("$external").createUser({
  user: "C=US,ST=YourState,O=Your Org,OU=management:group.12345,CN=svc-myapp-replicaset-mydb.corp.example.com",
  roles: [{ role: "readWrite", db: "mydb" }]
})
```

The user is not active until the cert has been issued and the app presents it.

---

## Connecting with PyMongo / Python 连接示例

```python
import urllib.request
import urllib.parse
from pymongo import MongoClient

# URL-encode the subject string (everything from "C=US,..." onwards)
raw_subject = "C=US,ST=YourState,O=Your Org,OU=management:group.12345,CN=svc-myapp-replicaset-mydb.corp.example.com"
username = urllib.parse.quote_plus(raw_subject)

uri = "mongodb://{0}@host1:port1,host2:port2/?authMechanism=MONGODB-X509&replicaSet=myReplicaSet".format(username)

client = MongoClient(
    uri,
    tls=True,
    tlsCertificateKeyFile="/path/to/svc-myapp.pem",        # merged key+cert
    tlsCAFile="/path/to/CA.pem",                            # CA chain
    tlsCertificateKeyFilePassword="<passphrase-if-encrypted>",
)

db = client["mydb"]
```

**Notes on the path arguments:**

- `tlsCertificateKeyFile` — the merged file from Step 3 (private key + certificate in one PEM)
- `tlsCAFile` — the CA chain from Step 4; tells PyMongo which CA to trust for the server cert
- `tlsCertificateKeyFilePassword` — only needed if the key was generated with a passphrase

---

## Certificate Renewal 证书续期

When the certificate expires, repeat the CSR → cert manager → merge → verify steps. Two constraints that **must not change**:

| Item | Why it must stay the same |
| --- | --- |
| CN in the new CSR | MongoDB user lookup is a string match on the subject. A different CN = different subject = authentication fails |
| Management group / OU | The OU (e.g., `management:group.12345`) is part of the subject string. Different group = different subject = auth fails |

If both CN and OU match the original, the new cert produces an identical subject string, and the existing MongoDB user entry continues to work with no DBA action required.

只要 CN 和 OU 与原始证书相同，新证书的 Subject 字符串就完全一致，无需 DBA 重新创建用户。

---

## Verifying a Certificate Before Use / 使用前验证证书

```bash
# Check the certificate subject, issuer, and validity dates
openssl x509 -in svc-myapp.pem -noout -subject -issuer -dates

# Verify the private key matches the certificate (output should say "OK")
openssl x509 -noout -modulus -in svc-myapp.pem | openssl md5
openssl rsa  -noout -modulus -in svc-myapp.pem | openssl md5
# Both lines must produce the same hash

# Check the full subject in RFC2253 format (for the DBA)
openssl x509 -in svc-myapp.pem -inform PEM -subject -nameopt RFC2253
```

---

## Key Takeaways

- X.509 auth replaces passwords with TLS certificates; the certificate subject string **is** the MongoDB username
- All X.509 users live in the `$external` virtual database — no passwords stored in MongoDB
- `db.getUser()` returns: `_id` (internal doc ID), `userId` (UUID for audit logs), `user` (the subject string / username), `db` (`$external`), `roles` (array of role+db pairs), `mechanisms` (`["external"]`)
- The subject string must be an **exact character-for-character match** — one difference means auth fails
- `certkey.pem` = private key block + certificate block concatenated in one file
- `CA.pem` = chain.pem + issuer.pem concatenated — used by the client to verify the server's cert
- Certificate renewal: keep the same CN and OU/management-group — the subject string must be identical to avoid breaking the existing MongoDB user mapping
- Never commit `.key.pem` or the merged `certkey.pem` to version control

## References

- MongoDB X.509 auth docs: `docs.mongodb.com/manual/tutorial/configure-x509-client-authentication`
- PyMongo TLS docs: `pymongo.readthedocs.io/en/stable/examples/tls.html`
- RFC 2253 — Distinguished Names encoding standard
- Related notes: [[50BigData/MongoDB]], [[13Crypt/PKI]]
