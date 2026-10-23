# Network Basics — Cheat Sheet

Quick reference for the NetWatch project.

---

## 1. Network layers

The real internet uses the **TCP/IP model** (OSI's 7 layers simplified to 4):

| TCP/IP layer    | OSI | Job                                    | Address    | Examples               |
|-----------------|-----|----------------------------------------|------------|------------------------|
| **Application** | 5–7 | What the program wants to say          | names/URLs | HTTP, DNS, SSH, DHCP   |
| **Transport**   | 4   | Which program on the host; reliable?   | **port**   | TCP, UDP               |
| **Internet**    | 3   | Network A → network B (routing)        | **IP**     | IP, ICMP               |
| **Link**        | 1–2 | Next device on the same local network  | **MAC**    | Ethernet, Wi-Fi, ARP   |

**Encapsulation:** each layer wraps the data from above in its own header.

```
[ Ethernet hdr | IP hdr | TCP hdr | HTTP data ]
   MAC addrs    IP addrs   ports     "GET /index.html"
```

Routers replace the outer (Ethernet) envelope at every hop; the inside stays the same end to end.

Common shorthand (OSI numbering): **L2** = MAC/switches · **L3** = IP/routers · **L4** = TCP/UDP ports · **L7** = applications.

---

## 2. IP addresses (Layer 3) — *where* on the internet

- **Logical** address; it depends on the network you're in.
- **IPv4:** 32 bits, e.g. `192.168.178.42`.
- **CIDR / subnet:** `192.168.178.42/24` → first 24 bits = network, last 8 = host.
  - `/24` = mask `255.255.255.0` → range `.0`–`.255`, 254 usable hosts (`.0` = network, `.255` = broadcast).
  - Device discovery = trying every host in the subnet.
- **Private ranges:** `10.x.x.x`, `172.16–31.x.x`, `192.168.x.x` (valid only inside your LAN).
- **Public IP:** one per home, from the ISP. **NAT** lets all devices share it.
- **Localhost:** `127.0.0.1` = this machine.
- **Gateway:** the router (e.g. `192.168.178.1`); traffic leaving your subnet goes there.
- **DHCP:** hands out IP, gateway and DNS server automatically.
- **IPv6:** 128 bits (`2a02:810d:...`), no NAT needed. Usually runs alongside IPv4.

---

## 3. MAC addresses (Layer 2) — *who* on the local network

- **Physical** hardware address of a network interface, e.g. `a4:83:e7:1c:2f:09` (48 bits).
- **First 3 bytes = OUI** → manufacturer (used for vendor lookup).
- Only meaningful **inside the local network**; never passes the router.
- Phones often use **randomized MACs** per Wi-Fi network for privacy.

**ARP** connects L2 and L3:
- "Who has `192.168.178.20`?" (broadcast) → "That's me, here's my MAC."
- Answers are cached in the **ARP table**.
- An ARP scan = asking this for every IP in the subnet.

---

## 4. DNS — the phonebook

- Translates names (`google.com`) into IPs.
- Device → **resolver** (router / ISP / `1.1.1.1`) → if unknown: **root → `.com` → google's nameservers** → cached.
- **TTL** = how long an answer may be cached (not the same as the IP packet TTL).
- Mostly **UDP port 53**.

| Record  | Meaning                     |
|---------|-----------------------------|
| `A`     | name → IPv4                 |
| `AAAA`  | name → IPv6                 |
| `CNAME` | alias → another name        |
| `MX`    | mail server                 |
| `PTR`   | IP → name (reverse lookup)  |

**Pi-hole** works purely via DNS: blocked domains get a "doesn't exist" answer.

---

## 5. Relevant protocols

| Protocol       | Layer | Port   | Purpose                                         | NetWatch phase          |
|----------------|-------|--------|-------------------------------------------------|-------------------------|
| **IP**         | 3     | –      | Addressing & routing                            | everywhere              |
| **ICMP**       | 3     | none   | Diagnostics: ping, traceroute                   | 1 (ping)                |
| **ARP**        | 2/3   | none   | IP → MAC on the LAN                             | 2 (discovery)           |
| **TCP**        | 4     | –      | Reliable connection (SYN → SYN-ACK → ACK)       | 1.3 checks, 2.6 portscan|
| **UDP**        | 4     | –      | Fast, connectionless, no guarantees             | DNS, DHCP, WireGuard    |
| **DNS**        | 7     | 53     | Name → IP                                       | 1.3, 4 (Pi-hole)        |
| **DHCP**       | 7     | 67/68  | Automatic IP assignment                         | new-device detection    |
| **HTTP/HTTPS** | 7     | 80/443 | Web; HTTPS = HTTP + TLS                         | 1.3 checks              |
| **mDNS**       | 7     | 5353   | Local name announcements (`printer.local`)      | 2.5 hostnames           |
| **SSH**        | 7     | 22     | Encrypted remote shell                          | managing the Pi         |

- **TCP vs UDP:** a phone call (connect, confirm, hang up) vs. throwing postcards (fast, some may get lost).
- **Ports:** IP reaches the *machine*, the port reaches the *program*.

---

## 6. Putting it all together — typing `https://google.com`

1. **DHCP** (earlier): laptop got `192.168.178.42/24`, gateway `.1`, DNS `.1`.
2. **DNS:** A record for `google.com` over UDP:53 → e.g. `142.250.185.78`.
3. **Routing:** not in my `/24` → send to the gateway.
4. **ARP:** "Who has `192.168.178.1`?" → router's MAC.
5. **TCP handshake** to `142.250.185.78:443` (SYN → SYN-ACK → ACK).
6. **TLS** encryption, then the **HTTP** request.
7. Router applies **NAT** (private → public IP); every router on the path decrements the IP **TTL** and forwards.
8. The response returns the same way.

→ **Phase 1** measures steps 2, 5, 6 (+ ICMP ping). **Phase 2** is about steps 1 and 4.
