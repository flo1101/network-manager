# NetWatch — a home network manager (learning project)

A self-built network manager, developed step by step as a learning project.
Goal: **understand** how networks work, not just run tools. Code is written mostly by hand;
each phase introduces a few new networking concepts.

Runs on a laptop first (Python + Docker). Later it can move to an always-on box
(Raspberry Pi 5 2GB, ~€110–130 with PSU/case/SD, or a used mini PC, ~€80–150).

---

## Stack

| Layer      | Choice                         | Why                                     |
|------------|--------------------------------|-----------------------------------------|
| Core       | Python 3.12                    | Great networking libraries, easy to read |
| API        | FastAPI                        | Async, simple, familiar                 |
| Storage    | SQLite (later maybe Postgres)  | Zero setup, one file                    |
| Frontend   | Plain HTML first, React later  | Learn the data first, polish later      |
| Packaging  | Docker / docker compose        | Same setup on laptop and Pi             |

---

## Roadmap

Status: ⬜ not started · 🟨 in progress · ✅ done

### Phase 1 — Network monitoring 🟨
Is my network up, and how fast does it respond?
- [ ] 1.1 Ping a single host from Python, parse latency (concepts: ICMP, RTT, packet loss)
- [ ] 1.2 Monitor a list of targets in a loop (router, 1.1.1.1, a website) — async
- [ ] 1.3 Add TCP/HTTP checks (concepts: ports, TCP handshake, DNS resolution time)
- [ ] 1.4 Store results in SQLite, compute uptime % and avg/p95 latency
- [ ] 1.5 Small FastAPI endpoint + simple HTML page showing status
- [ ] 1.6 Alerts when a target goes down (Telegram / email)

### Phase 2 — Device discovery ⬜
Who is on my network?
- [ ] 2.1 Understand your own network: IP, subnet mask, CIDR, gateway
- [ ] 2.2 Ping sweep of the subnet
- [ ] 2.3 ARP scan (concepts: Layer 2 vs Layer 3, MAC addresses, ARP table) with scapy
- [ ] 2.4 MAC vendor lookup (OUI database)
- [ ] 2.5 Hostname discovery (reverse DNS, mDNS/Bonjour, NetBIOS)
- [ ] 2.6 Port scan of known devices (concepts: open/closed/filtered, common services)
- [ ] 2.7 Device inventory in DB: first seen / last seen / online status
- [ ] 2.8 Alert on unknown new device joining the network

### Phase 3 — Traffic insight ⬜
- [ ] Packet capture basics (pcap, Wireshark, scapy sniffing)
- [ ] Bandwidth per device (needs mirrored port or gateway position)
- [ ] DNS query log per device (ties into Phase 4)
- [ ] Inspiration: ntopng

### Phase 4 — DNS & ad blocking ⬜
- [ ] Run Pi-hole / AdGuard Home in Docker
- [ ] Read its API into the dashboard ("what does my smart TV phone home to?")
- [ ] Optional: build a tiny DNS sinkhole yourself to understand how it works

### Phase 5 — Dashboards & metrics ⬜
- [ ] Export metrics in Prometheus format from NetWatch
- [ ] Grafana dashboards
- [ ] Compare with Uptime Kuma

### Phase 6 — Security ⬜
- [ ] Honeypot (OpenCanary) — alert on anything touching it
- [ ] IDS: Suricata or Zeek (start with pcap files)
- [ ] Integrate alerts into NetWatch

### Phase 7 — Remote access ⬜
- [ ] WireGuard VPN (PiVPN) — reach home network from anywhere
- [ ] Ad blocking on the go via VPN + Pi-hole

### Phase 8 — Infrastructure ⬜
- [ ] Move to always-on hardware (Pi 5 or used mini PC)
- [ ] Mini Kubernetes cluster: k3d/kind on laptop → k3s on Pis

### Extras / side quests ⬜
- [ ] Wi-Fi presence detection (who is home?) + Home Assistant
- [ ] Travel router (Pi + second Wi-Fi adapter + VPN)
- [ ] ADS-B flight tracking (SDR USB stick ~€25–35, works on a laptop too)
- [ ] Meshtastic LoRa mesh (ESP32/LoRa boards ~€30–40 each, need two)

---

## Learning log

Short notes after each step: what I learned, what confused me.

| Step | Date | Notes |
|------|------|-------|
|      |      |       |
