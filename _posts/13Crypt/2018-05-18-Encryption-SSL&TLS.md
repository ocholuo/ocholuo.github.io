---
title: Cryptography - SSL/TLS Encryption
date: 2018-05-18 11:11:11 -0400
categories: [13Cryptography]
tags: [cryptography]
toc: true
image:
---

- [Cryptography - SSL/TLS Encryption](#cryptography---ssltls-encryption)
  - [overall](#overall)
  - [SSL/TLS vs SSH](#ssltls-vs-ssh)

---

# Cryptography - SSL/TLS Encryption

---

## overall

SSL/TLS uses both asymmetric and symmetric encryption to protect the confidentiality and integrity of data-in-transit. Asymmetric encryption is used to establish a secure session between a client and a server, and symmetric encryption is used to exchange data within the secured session.




--


## SSL/TLS vs SSH

similar:
- SSL and SSH both provide the cryptographic elements to build a tunnel for confidential data transport with checked integrity. For that part, they use similar techniques, and may suffer from the same kind of attacks, so they should provide similar security (i.e. good security) assuming they are both properly implemented.
- That both exist is a kind of NIH syndrome: the SSH developers should have reused SSL for the tunnel part (the SSL protocol is flexible enough to accommodate many variations, including not using certificates).

differ:
- They differ on the things which are around the tunnel.
- 1
  - **SSL** traditionally uses `X.509 certificates` for announcing server and client public keys;
  - SSH has its own format.
- 2
  - SSH comes with a set of protocols for what goes inside the tunnel (multiplexing several transfers, performing password-based authentication within the tunnel, terminal management...)
  - while there is no such thing in SSL,
    - or, more accurately, when such things are used in SSL, they are not considered to be part of SSL
    - for instance, when doing password-based HTTP authentication in a SSL tunnel, we say that it is part of "HTTPS", but it really works in a way similar to what happens with SSH

Conceptually,
- you could take SSH and replace the tunnel part with the one from SSL.
- You could also take HTTPS and replace the SSL thing with SSH-with-data-transport and a hook to extract the server public key from its certificate.
- There is no scientific impossibility and, if done properly, security would remain the same. However, there is no widespread set of conventions or existing tools for that.

- So we do not use SSL and SSH for the same things, but that's because of what tools historically came with the implementations of those protocols, not due to a security related difference. And whoever implements SSL or SSH would be well advised to look at what kind of attacks were tried on both protocols.









---
