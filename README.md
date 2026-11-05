# 🛡️ File Integrity & Security Monitoring System (FIM)

A lightweight, host-based intrusion detection and integrity monitoring suite built in Python for Linux environments. This tool combines cryptographic file hashing, directory baseline snapshots, real-time tamper detection, and automated authentication log parsing to identify unauthorized file modifications and brute-force attacks.

---

## 📌 Project Overview

This project bridges endpoint integrity verification with proactive log auditing to defend Linux systems:

* **Cryptographic File Verification**: Uses chunked SHA-256 hashing to process files of arbitrary sizes without exhausting system RAM.
* **Baseline Snapshotting**: Recursively traverses directory structures, indexes file paths, and serializes metadata into a structured JSON baseline (`baseline.json`).
* **Tamper & Anomaly Detection**: Performs two-way set comparisons between live filesystem states and stored baselines to immediately flag modified, added, or deleted files.
* **Authentication Log Auditing**: Implements regular-expression-based parsing of Linux `/var/log/auth.log` records to detect repeated login failures, aggregate targeted usernames, and flag suspicious IP addresses exceeding configured attack thresholds.
* **Unified CLI Orchestrator**: Uses Python’s `argparse` module to expose modular subcommands (`hash`, `baseline`, `verify`, `logs`) from a single entry point.

---

## 🛠️ Technical Details & Environment

* **Operating System**: Kali Linux / Debian-based Linux
* **Language**: Python 3.x
* **Core Libraries**: `hashlib`, `argparse`, `json`, `re`, `os`, `sys`, `collections` (Zero third-party dependencies required)
* **Version Control**: Git & GitHub (`main` branch workflow)

---

## 📂 Repository Structure

```text
File_Integrity_Monitor/
│
├── src/
│   ├── __init__.py          # Package initialization
│   ├── hasher.py            # Memory-safe SHA-256 hashing engine
│   ├── baseline.py          # Directory traversal & JSON baseline generator
│   ├── detector.py          # State comparison & tamper detection engine
│   └── log_monitor.py       # Auth log parser & brute-force detector
│
├── test_dir/                # Local test bed for simulated file attacks
├── sample_auth.log          # Mock Linux authentication log for intrusion tests
├── main.py                  # Unified CLI orchestrator
└── README.md                # Technical project documentation

```

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone [https://github.com/ameyrane07/File_Integrity_Monitor.git](https://github.com/ameyrane07/File_Integrity_Monitor.git)
cd File_Integrity_Monitor

```

### 2. Run CLI Commands

#### Compute a File's Cryptographic Hash

```bash
python3 main.py hash sample_auth.log

```

#### Generate a Directory Baseline Snapshot

```bash
python3 main.py baseline test_dir/ -o baseline.json

```

#### Check Directory Integrity (Detect Tampering)

```bash
python3 main.py verify -b baseline.json

```

#### Audit Authentication Logs for Brute-Force Attacks

```bash
python3 main.py logs sample_auth.log -t 3

```

---

## 📊 Sample Execution & Output

### 1. Unified CLI Help Menu (`python3 main.py --help`)

```text
usage: main.py [-h] {hash,baseline,verify,logs} ...

Comprehensive File Integrity & Security Monitoring System

positional arguments:
  {hash,baseline,verify,logs}
                        Available modules
    hash                Compute SHA-256 hash of a file
    baseline            Generate snapshot baseline
    verify              Check directory integrity
    logs                Analyze authentication logs

options:
  -h, --help            show this help message and exit

```

### 2. Tamper Detection Output (`python3 main.py verify`)

```text
--- Integrity Verification Report ---
Target Directory: /home/amey/Desktop/File_Integrity_Monitor/test_dir
Status: ANOMALIES DETECTED

[!] MODIFIED FILES:
    - /home/amey/Desktop/File_Integrity_Monitor/test_dir/config.conf

[!] NEW / UNINDEXED FILES:
    + /home/amey/Desktop/File_Integrity_Monitor/test_dir/backdoor.sh

[!] DELETED FILES:
    x /home/amey/Desktop/File_Integrity_Monitor/test_dir/auth.key

```

### 3. Brute-Force Log Analysis (`python3 main.py logs sample_auth.log -t 3`)

```text
--- Authentication Log Analysis Report (sample_auth.log) ---
IP: 192.168.1.100    Failures: 4    Users: ['root', 'amey', 'admin'] [ALERT: BRUTE-FORCE DETECTED]
IP: 10.0.0.15        Failures: 1    Users: ['amey'] [NORMAL]

```

---

## 🧠 Key Takeaways

1. **Host-Based Intrusion Detection (HIDS)**: Real-time integrity verification prevents undetected persistence; even if an attacker alters one line of a script or drops a backdoor, the cryptographic checksum immediately triggers an anomaly alert.
2. **Memory Efficiency in Security Tooling**: Reading files in 64 KB binary chunks ensures that multi-gigabyte server files or database dumps can be verified without CPU starvation or Out-of-Memory (OOM) crashes.
3. **Log Aggregation & Threat Detection**: Automated log parsing bridges file monitoring with access monitoring, converting raw SSH failure logs into structured security alerts ready for automated IP blocking.

---

```

```
