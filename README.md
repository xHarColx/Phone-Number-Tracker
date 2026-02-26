# 📱 PhoneTrackerPro v5.0.0

> **Advanced Phone Intelligence & OSINT Framework**
> **2650+ lines** of pure Python intelligence gathering
> Author: **Vishal** | For Educational & Authorized Security Research Only

---

## 🚀 Features at a Glance

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Phone Parsing & Validation** | E.164 / international / national format, valid + possible checks, auto country-code detection |
| 2 | **CDR-Style Subscriber Info** | Carrier, country, timezone, region, line type, HLR status, network reachability |
| 3 | **India Telecom Circle DB** | 700+ prefix → circle mapping (Jio, Airtel, Vi, BSNL) with SIM registration city |
| 4 | **Live Location (Multi-API Consensus)** | Cross-references up to 7 sources with weighted voting → most likely current city |
| 5 | **Roaming Detection** | Compares SIM registration circle vs live network city → flags roaming |
| 6 | **IP Grabber Link** | Flask-powered tracking link captures visitor IP, User-Agent, GPS (if allowed), with Rich live dashboard |
| 7 | **Advanced Geolocation** | OpenCage + Nominatim forward/reverse geocoding → lat/lng + formatted address |
| 8 | **OSINT Platform Probes** | WhatsApp, Telegram, Truecaller (multi-method), Eyecon, SyncMe, Facebook, Instagram, Google |
| 9 | **UPI ID Generation** | Auto-generates 10 possible UPI IDs (@paytm, @ybl, @okaxis, @upi, etc.) for Indian numbers |
| 10 | **Email Intelligence** | Email guessing from phone number, Gravatar profile lookup, AbstractAPI email validation |
| 11 | **Truecaller Multi-Method** | 3 API endpoints + web scrape + JSON extraction — attempts to fetch owner name & email |
| 12 | **Deep OSINT** | Spam DB checks (SpamCalls.net, ShouldIAnswer), breach-style exposure check, web mention scraping |
| 13 | **Owner Name Detection** | Auto-extracts real name from Truecaller/SyncMe/Eyecon and shows in summary |
| 14 | **Case Management** | Case ID (auto-UUID or custom), operator name, unit, classification levels |
| 15 | **Audit Trail & Evidence Hashing** | SHA-256 chain-of-custody, per-phase evidence logging, persistent audit log files |
| 16 | **HTML Report (Professional)** | Dark-themed report with classification banners, case metadata, legal notice, audit trail, SHA-256 hash |
| 17 | **JSON Export** | Forensic envelope with case metadata, evidence integrity hash, full data dump |
| 18 | **Interactive Map** | Folium map with SIM location + live location markers, heatmap layer |
| 19 | **Persistent API Keys** | `.env` file auto-loaded every run via `python-dotenv` |
| 20 | **Flexible CLI** | Grouped argument categories, API status panel, version flag, epilog with examples |

---

## 📦 Installation

### 1. Clone / Download

```bash
git clone https://github.com/Vishal-HaCkEr1910/Python_Cybersec_Projects.git
cd Python_Cybersec_Projects
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
```
phonenumbers
opencage
folium
requests
colorama
rich
beautifulsoup4
lxml
python-dotenv
flask
tqdm
fake-useragent
httpx
```

Or install manually:
```bash
pip install phonenumbers opencage folium requests colorama rich beautifulsoup4 lxml python-dotenv flask tqdm fake-useragent httpx
```

---

## 🔑 API Key Setup

PhoneTrackerPro uses 4 API keys for maximum intelligence. **All are free tier.**

### Getting Your API Keys

| API | Sign Up Link | Free Tier | Used For |
|-----|-------------|-----------|----------|
| **Numverify** | [numverify.com/signup](https://numverify.com/signup) | 100 req/month | Carrier lookup, location vote |
| **AbstractAPI** | [app.abstractapi.com](https://app.abstractapi.com/users/signup) | 1000 req/month | Phone validation, location vote |
| **ipinfo** | [ipinfo.io/signup](https://ipinfo.io/signup) | 50,000 req/month | Your IP location (reference point) |
| **OpenCage** | [opencagedata.com](https://opencagedata.com/users/sign_up) | 2,500 req/day | Forward/reverse geocoding |

### Setting Up `.env` File

Create a `.env` file in the project root:

```env
NUMVERIFY_API_KEY=your_numverify_key_here
ABSTRACT_API_KEY=your_abstract_api_key_here
IPINFO_TOKEN=your_ipinfo_token_here
OPENCAGE_API_KEY=your_opencage_key_here
```

> **Note:** The tool shows which API keys are configured at startup with ✓/✗ indicators. Missing keys are NOT fatal — the tool gracefully skips those APIs and uses the remaining sources.

---

## 🛠 Usage — All Commands

### Basic Syntax

```bash
python phone_tracker.py <phone_number> [options]
```

### Input Formats (All Work)

```bash
python phone_tracker.py +919876543210       # Full international
python phone_tracker.py 9876543210          # Auto-adds +91 (India default)
python phone_tracker.py 09876543210         # Leading 0 stripped
python phone_tracker.py +1-202-555-0100     # US number with dashes
python phone_tracker.py "(+91) 98765-43210" # Parentheses and dashes
```

---

### 🔍 Scan Modes

#### Full Scan (Default — All 8 Phases)
```bash
python phone_tracker.py +919876543210
```
Runs: Parse → Basic Info → Telecom Circle → Live Location → Geolocation → OSINT → Deep OSINT → Reports

#### Quick Scan (Basic Info + Telecom Only)
```bash
python phone_tracker.py +919876543210 --quick
```
Fast check — skips all advanced phases. Great for quick carrier/circle lookup.

#### Skip Specific Phases
```bash
# Skip live location detection (saves ~5 seconds)
python phone_tracker.py +919876543210 --skip-live

# Skip OSINT platform probes (WhatsApp, Telegram, etc.)
python phone_tracker.py +919876543210 --skip-osint

# Skip deep OSINT (spam DB, breach check, web mentions)
python phone_tracker.py +919876543210 --skip-deep

# Skip both OSINT phases (just location intelligence)
python phone_tracker.py +919876543210 --skip-osint --skip-deep

# Location-only scan (fastest meaningful scan)
python phone_tracker.py +919876543210 --skip-osint --skip-deep
```

---

### 🎯 IP Grabber Mode

Generate a tracking link that captures the target's IP address, browser info, and GPS coordinates (if they allow location access). **The IP grabber runs AFTER a full scan**, so you get all intel plus the IP grab.

```bash
# Full scan + IP grabber on default port (8888)
python phone_tracker.py +919876543210 --grab

# Full scan + IP grabber on custom port
python phone_tracker.py +919876543210 --grab --grab-port 9999
```

**What it does:**
1. Runs the complete scan (all phases)
2. Saves JSON + HTML + Map reports
3. Then starts a Flask web server on your machine
4. Generates a tracking URL (e.g., `http://192.168.1.5:8888/track/e921e8732992`)
5. Shows a **Rich live dashboard** with captured visitor data
6. Saves all captures to `output/grab_<id>.json`

**What it captures when someone opens the link:**

| Data | How |
|------|-----|
| IP Address | Server-side (always captured) |
| City / Region / Country | IP geolocation lookup |
| ISP / ASN | IP info API |
| User-Agent | Browser header |
| Platform / OS | Parsed from UA |
| GPS Coordinates | Browser Geolocation API (requires user permission) |
| Accuracy | GPS accuracy in meters |
| Timestamp | Server-side UTC timestamp |

#### 🌐 Exposing with ngrok (For Remote Targets)

By default, the tracking link only works on your local network. To make it accessible over the internet, use **ngrok**:

**Step 1: Install ngrok**
```bash
# macOS
brew install ngrok

# Linux
sudo snap install ngrok

# Or download from https://ngrok.com/download
```

**Step 2: Sign up & get auth token**
- Go to [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
- Copy your auth token from the dashboard

**Step 3: Authenticate ngrok**
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

**Step 4: Start PhoneTrackerPro IP Grabber**
```bash
python phone_tracker.py +919876543210 --grab --grab-port 8888
```

**Step 5: In a NEW terminal, expose the port**
```bash
ngrok http 8888
```

**Step 6: Copy the ngrok URL**
ngrok will show something like:
```
Forwarding  https://a1b2c3d4.ngrok-free.app -> http://localhost:8888
```

**Step 7: Send the tracking link**
Replace the local IP part of the tracking URL with the ngrok URL:
```
Original:  http://192.168.1.5:8888/track/e921e8732992
Send this: https://a1b2c3d4.ngrok-free.app/track/e921e8732992
```

When the target opens the link, their IP + location + GPS data appears in your terminal dashboard in real-time!

---

### 🏷️ Case Management

Tag your scans with case metadata for organized record-keeping:

```bash
# Custom case ID + operator name
python phone_tracker.py +919876543210 --case-id "CASE-2026-0042" --officer "Vishal Rao"

# Add unit/team
python phone_tracker.py +919876543210 --case-id "INV-001" --officer "Agent V" --unit "Cyber Recon"

# Set classification level
python phone_tracker.py +919876543210 --classification CONFIDENTIAL

# Full metadata
python phone_tracker.py +919876543210 \
  --case-id "CASE-2026-0042" \
  --officer "Vishal Rao" \
  --unit "OSINT Division" \
  --classification CONFIDENTIAL
```

**Classification Levels:**

| Level | Color | Use Case |
|-------|-------|----------|
| `UNCLASSIFIED` | 🟢 Green | Public / open research |
| `RESTRICTED` | 🟡 Yellow | Default — internal use |
| `CONFIDENTIAL` | 🔴 Red | Sensitive investigations |
| `SECRET` | 🔴 Bold Red | Highest sensitivity |

If not specified:
- **Case ID:** Auto-generated UUID (e.g., `CASE-20260227-A3F9B2`)
- **Officer:** `OPERATOR` (default)
- **Unit:** `UNSPECIFIED`
- **Classification:** `RESTRICTED`

---

### 📄 Report Options

```bash
# Skip map generation
python phone_tracker.py +919876543210 --no-map

# Skip HTML report
python phone_tracker.py +919876543210 --no-report

# Only generate JSON (no HTML or map)
python phone_tracker.py +919876543210 --json-only

# Custom output directory
python phone_tracker.py +919876543210 --output-dir results/

# Combine options
python phone_tracker.py +919876543210 --skip-deep --no-map --output-dir my_reports/
```

---

### 📌 Other Options

```bash
# Show version
python phone_tracker.py --version

# Show help with all options + examples
python phone_tracker.py -h
```

---

## 📁 Output Files

All outputs are saved in the `output/` directory (or your `--output-dir`):

| File Pattern | Description |
|---|---|
| `phone_intel_<number>_<timestamp>.json` | Full JSON with forensic metadata envelope, all intelligence data, evidence hash |
| `phone_report_<number>_<timestamp>.html` | Professional HTML report with dark theme, classification banners, legal notice |
| `phone_map_<number>_<timestamp>.html` | Folium interactive map with SIM + live location markers |
| `grab_<id>.json` | IP Grabber captures (IP, User-Agent, GPS coords, timestamps) |
| `output/audit_logs/audit_YYYYMMDD.log` | Persistent audit trail log (one per day, appended to) |

### JSON Report Structure

The JSON export wraps everything in a metadata envelope:

```json
{
  "case_metadata": {
    "case_id": "CASE-20260227-A3F9B2",
    "scan_id": "D7E4BF952D5B",
    "officer": "Vishal Rao",
    "classification": "RESTRICTED",
    "timestamp_utc": "2026-02-27T00:57:30Z",
    "tool_version": "5.0.0"
  },
  "phone_number": "+919876543210",
  "basic_info": { "..." },
  "telecom_circle": { "..." },
  "live_location": { "..." },
  "all_votes": [ "..." ],
  "consensus_city": "Delhi",
  "geo_results": { "..." },
  "osint_results": { "..." },
  "deep_osint": { "..." },
  "evidence_integrity": {
    "algorithm": "SHA-256",
    "hash": "dece06207c8f54c5..."
  },
  "evidence_chain": [ "..." ],
  "audit_trail": [ "..." ]
}
```

### HTML Report Sections

The HTML report includes:
- 🔒 **Classification banner** (sticky, color-coded by level)
- 📋 **Case metadata grid** (Case ID, Officer, Unit, Classification, Timestamp)
- 👤 **Subject / SIM registration details** (MSISDN, carrier, IMSI range, MCC-MNC, HLR status)
- 📧 **Email intelligence** (Truecaller email, guessed emails, Gravatar profiles)
- 📡 **Location intelligence** (consensus city, roaming indicator, lat/lng, address)
- 🗳️ **Source vote breakdown** (which API voted for which city, confidence %)
- 🎯 **IP/Device intelligence** (if IP grabber was used)
- 🔍 **OSINT platform findings** (per-platform found/not-found)
- ⚠️ **Threat/risk intelligence** (spam reports, breach exposure, web mentions)
- 📜 **Evidence audit trail** (timestamped log of all collection phases)
- 🔐 **SHA-256 evidence integrity hash**
- ⚖️ **Legal disclaimer**
- 🖨️ **Print-friendly CSS** (works with Ctrl+P / Cmd+P)

---

## ⚙ How It Works — Phase-by-Phase

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: PARSE & VALIDATE                                     │
│  phonenumbers library → E.164, valid/possible, country detect   │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 2: SUBSCRIBER INFO (CDR-STYLE)                          │
│  Carrier, country, timezone, line type, HLR/network status      │
│  Format: Case ID, Scan ID, Operator, MSISDN, all formats       │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 3: TELECOM CIRCLE (India)                               │
│  700+ prefix DB → Jio/Airtel/Vi/BSNL → circle + city            │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 4: LIVE LOCATION (Multi-API Consensus Voting)           │
│  Up to 7 APIs queried → weighted votes → consensus city          │
│  Compares with SIM circle → roaming detection                    │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 5: GEOLOCATION                                          │
│  OpenCage + Nominatim → lat/lng + formatted address              │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 6: OSINT PLATFORM PROBES                                │
│  WhatsApp • Telegram • Truecaller (multi-method)                 │
│  Eyecon • SyncMe • Facebook • Instagram • Google                 │
│  UPI ID generation • Email guessing • Gravatar                   │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 7: DEEP OSINT                                           │
│  Spam DBs (SpamCalls.net, ShouldIAnswer)                        │
│  Breach-style exposure check                                     │
│  Web mentions scraping (Google dorking)                          │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 8: REPORTS                                              │
│  JSON (metadata envelope) + HTML (professional) + Folium Map     │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 9: IP GRABBER (optional --grab)                         │
│  Flask server → tracking link → captures IP/GPS in real-time     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 📡 Live Location — Consensus Voting System

The tool queries up to 7 different sources and uses **weighted consensus voting** to determine the most likely current city:

| Source | Weight | Requires API Key |
|--------|--------|-----------------|
| Numverify | 3 | ✅ `NUMVERIFY_API_KEY` |
| AbstractAPI | 3 | ✅ `ABSTRACT_API_KEY` |
| ipinfo | 2 | ✅ `IPINFO_TOKEN` |
| Free Network Probe | 1 | ❌ |
| VLR/MSC Detection | 1 | ❌ |
| PhoneInfo Probe | 1 | ❌ |
| MobileTracker Probe | 1 | ❌ |

**How voting works:**
1. Each API returns a city/region
2. Cities are normalized (case-insensitive, "New Delhi" → "Delhi")
3. Votes are weighted by source reliability
4. The city with the highest weighted vote count wins
5. Confidence is calculated as `(winning votes / total votes)`
6. If consensus city ≠ SIM registration city → **ROAMING** is flagged

---

### 🔍 OSINT Probes — What Each One Does

| Probe | Method | What It Finds |
|-------|--------|---------------|
| **WhatsApp** | Registration check via web endpoint | Whether number is registered on WhatsApp |
| **Telegram** | API probe for user existence | Whether profile exists on Telegram |
| **Truecaller** | 3 API endpoints + web scrape + JSON extraction | Owner name, email (requires auth for full data) |
| **Eyecon** | Caller ID API probe | Name if publicly listed |
| **SyncMe** | Caller ID lookup | Name from SyncMe database |
| **Facebook** | Password reset flow indicator | Whether FB account is linked to number |
| **Instagram** | Account recovery signal detection | Whether IG account is linked |
| **Google** | Web scraping for phone number mentions | Public mentions of the number online |
| **UPI IDs** | Pattern generation | 10 possible UPI addresses (@paytm, @ybl, @okaxis, etc.) |
| **Email Guess** | Pattern generation from phone number | 5 possible emails (number@gmail.com, @yahoo, @outlook, etc.) |
| **Gravatar** | Hash lookup against Gravatar API | Profile picture + display name if email exists |
| **AbstractAPI Email** | Email validation API | Validates guessed emails for deliverability |

---

### 🔐 Evidence Integrity & Audit Trail

Every scan produces a complete audit trail:

**Chain-of-Custody Log:**
- Each phase logs: timestamp (UTC), action, detail, scan ID, operator
- Each entry includes a SHA-256 hash chained to the previous entry (tamper-evident)
- Stored in `self.evidence_chain` and exported in JSON

**Evidence Integrity Hash:**
- After all data is collected, a SHA-256 hash is computed over the entire JSON payload
- This hash appears in the terminal summary, HTML report, and JSON export
- Any modification to the data will produce a different hash

**Persistent Audit Log File:**
- Written to `output/audit_logs/audit_YYYYMMDD.log`
- One file per day, appended to on each scan
- Format: `YYYY-MM-DD HH:MM:SS | INFO | [ACTION] ScanID=XXX | detail`

Example audit log:
```
2026-02-27 00:56:38 | INFO | [SCAN_INITIATED] ScanID=D7E4BF952D5B | Target=9469593244, Officer=Vishal, Case=CASE-2026-0042
2026-02-27 00:56:38 | INFO | [NUMBER_PARSED] ScanID=D7E4BF952D5B | E164=+919469593244, Valid=True, CC=+91
2026-02-27 00:56:38 | INFO | [BASIC_INFO_COLLECTED] ScanID=D7E4BF952D5B | Carrier=BSNL MOBILE, Country=India, Type=Mobile
2026-02-27 00:56:45 | INFO | [live_location_complete] ScanID=D7E4BF952D5B | Consensus: Jammu Kashmir, Votes: 1
2026-02-27 00:56:46 | INFO | [geolocation_complete] ScanID=D7E4BF952D5B | Resolved: India
2026-02-27 00:57:16 | INFO | [osint_complete] ScanID=D7E4BF952D5B | Platforms found: 3, Owner: Unknown
2026-02-27 00:57:30 | INFO | [deep_osint_complete] ScanID=D7E4BF952D5B | Breach sources: 0
2026-02-27 00:57:30 | INFO | [report_generated] ScanID=D7E4BF952D5B | HTML report saved: output/phone_report_...html
```

---

### 🗺️ Folium Map

The interactive map includes:
- 📍 **SIM Registration marker** (where the SIM was activated)
- 📡 **Live/Consensus location marker** (where the phone currently is)
- 🔥 **Heatmap layer** (if GPS data from IP grabber is available)
- 🏷️ Popup cards with carrier, circle, coordinates
- 🌍 OpenStreetMap + satellite tile layers

---

## 🧰 Advanced Usage Examples

### Combine Everything
```bash
# Full scan with case management, then IP grabber
python phone_tracker.py +919876543210 \
  --case-id "RECON-001" \
  --officer "Agent V" \
  --unit "CyberOps" \
  --classification CONFIDENTIAL \
  --grab \
  --grab-port 9999
```

### Quick Lookup (Carrier + Circle Only)
```bash
python phone_tracker.py 9876543210 --quick
```

### Location Intelligence Only (Skip OSINT)
```bash
python phone_tracker.py +919876543210 --skip-osint --skip-deep
```

### Minimal Output (JSON Only, No Map)
```bash
python phone_tracker.py +919876543210 --json-only --no-map
```

### Batch Processing (Shell Loop)
```bash
for num in 9876543210 9123456789 9555555555; do
  python phone_tracker.py $num --json-only --skip-deep --output-dir batch_results/
  sleep 2  # Rate limit courtesy
done
```

---

## 📊 Terminal Output Preview

When you run a full scan, you see:

1. **ASCII Banner** — PhoneTrackerPro v5.0.0
2. **Scan Configuration Panel** — Mode, API key status, classification, case ID, output dir
3. **CDR-Style Subscriber Table** — Case ID, Scan ID, Operator, MSISDN, carrier, HLR status, formats
4. **Telecom Circle** — Circle name + SIM registration city
5. **Live Location Voting Table** — Each API's vote with confidence %
6. **Live Location Summary** — Consensus city, roaming status, detection method
7. **Geolocation Table** — City, state, country, lat/lng, address, timezone
8. **OSINT Intelligence Table** — Per-platform found/not-found with details
9. **Deep OSINT Results** — Spam score, breach exposure, web mentions
10. **Report Generation** — File paths for JSON, HTML, Map
11. **Classification Banner** — Color-coded classification level
12. **Case Information Table** — Case ID, Officer, Unit, Classification, Time
13. **Subject Intelligence Table** — Full summary of all findings
14. **Chain of Custody Panel** — SHA-256 evidence integrity hash
15. **Completion Message** — Case ID + Classification confirmation

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside your venv |
| `Invalid phone number` | Include country code: `+91`, `+1`, etc. |
| API keys not working | Check `.env` file is in the same directory as `phone_tracker.py` |
| No live location data | Free APIs have rate limits — wait and retry, or add more API keys |
| IP Grabber not reachable | Use ngrok (see above) for external access |
| Map not generating | Ensure `opencage` package is installed and API key is set |
| Permission denied on port | Use a port > 1024: `--grab-port 8888` |
| Truecaller says "No public data" | Truecaller requires a logged-in bearer token for full results — use the Truecaller app for manual lookup |
| SyncMe returns tagline as name | "Always knowwho's calling" is SyncMe's tagline, not a real name — known limitation |
| Evidence hash shows "N/A" | Ensure the scan completes all phases before the hash is computed |
| `Address already in use` | Kill the process on that port: `lsof -ti:8888 \| xargs kill` |

---

## 📋 Full Command Reference

```
usage: phone_tracker.py [-h] [--quick] [--skip-live] [--skip-osint]
                        [--skip-deep] [--case-id ID] [--officer NAME]
                        [--unit UNIT] [--classification LEVEL]
                        [--grab] [--grab-port PORT]
                        [--no-map] [--no-report] [--json-only]
                        [--output-dir DIR] [--version]
                        phone

PhoneTrackerPro v5.0.0 — Advanced Phone Intelligence & OSINT Framework

positional arguments:
  phone                  Phone number (e.g., +919876543210 or 9876543210)

Scan Options:
  --quick                Quick mode: basic info + telecom only
  --skip-live            Skip live location (multi-API) detection
  --skip-osint           Skip OSINT platform probes
  --skip-deep            Skip deep OSINT (spam/breach/web)

Case Management:
  --case-id ID           Case/investigation ID (default: auto-UUID)
  --officer NAME         Operator / researcher name
  --unit UNIT            Team / department name
  --classification LEVEL UNCLASSIFIED, RESTRICTED, CONFIDENTIAL, SECRET
                         (default: RESTRICTED)

IP Grabber:
  --grab                 Launch IP Grabber link server
  --grab-port PORT       Port for IP Grabber server (default: 8888)

Report Options:
  --no-map               Skip Folium map generation
  --no-report            Skip HTML report generation
  --json-only            Only generate JSON report
  --output-dir DIR       Output directory (default: output/)

Other:
  --version              Show version and exit
  -h, --help             Show help message and exit
```

---

## 🏗️ Architecture

```
phone_tracker.py (2650+ lines)
├── Imports & Config
│   ├── AuditLogger class (SHA-256 chain-of-custody)
│   ├── _audit() / _sha256() helpers
│   ├── BANNER, VERSION, CLASSIFICATION levels
│   └── API key loading from .env
├── class PhoneTrackerPro
│   ├── __init__() — 90+ instance vars, case management, forensic fields
│   ├── _log_evidence() — chain-of-custody logger
│   ├── parse_number() — E.164 parsing, validation
│   ├── get_basic_info() — carrier, country, timezone, HLR status
│   ├── display_basic_info() — CDR-style Rich table
│   ├── INDIA_CIRCLE_DB — 700+ prefix mapping
│   ├── detect_telecom_circle() — circle + city detection
│   ├── detect_live_location() — orchestrates 7 API sources
│   │   ├── _api_numverify()
│   │   ├── _api_abstractapi()
│   │   ├── _api_ipinfo()
│   │   ├── _api_vlr_msc()
│   │   ├── _api_phoneinfo()
│   │   ├── _api_mobiletracker()
│   │   └── _api_free_network()
│   ├── _consensus_vote() — weighted voting algorithm
│   ├── _display_live_location() — voting table + summary
│   ├── generate_ip_grabber() — Flask server + tracking page
│   ├── advanced_geolocate() — OpenCage + Nominatim
│   ├── run_osint() — orchestrates all platform probes
│   │   ├── _probe_whatsapp()
│   │   ├── _probe_telegram()
│   │   ├── _probe_truecaller_web() — 3 APIs + web + JSON
│   │   ├── _probe_eyecon()
│   │   ├── _probe_syncme()
│   │   ├── _probe_facebook()
│   │   ├── _probe_instagram()
│   │   ├── _probe_google()
│   │   ├── _check_india_upi()
│   │   ├── _probe_email_from_name()
│   │   ├── _probe_gravatar()
│   │   └── _probe_abstractapi_email()
│   ├── run_deep_osint()
│   │   ├── Spam DB checks
│   │   ├── _check_haveibeenpwned_style()
│   │   └── Web mentions scraping
│   ├── generate_map() — Folium with markers + heatmap
│   ├── to_dict() — metadata envelope with SHA-256 hash
│   ├── generate_html_report() — professional dark-themed report
│   ├── generate_json_report() — full JSON export
│   └── generate_reports() — orchestrates all report types
├── _print_summary() — Rich tables with case info + intel + hash
└── main() — argparse CLI with grouped options
```

---

## 📝 Changelog

| Version | Changes |
|---------|---------|
| **v5.0.0** | Case management (--case-id, --officer, --unit, --classification), AuditLogger with SHA-256 chain-of-custody, metadata envelope in JSON, professional HTML reports with classification banners + legal notice + audit trail, evidence integrity hashing, persistent audit log files, CDR-style subscriber info display, forensic fields (HLR, IMSI range, MCC-MNC, network status) |
| **v4.1.0** | Argparse overhaul with grouped options, API status panel, Truecaller multi-method probe (3 APIs + web), email guessing + Gravatar lookup, --grab runs full scan THEN IP grabber, clean --help with epilog examples |
| **v4.0.0** | Full rewrite — 8-phase scan, 7-API consensus voting, IP grabber with Flask + Rich dashboard, OSINT probes (WhatsApp/Telegram/Truecaller/SyncMe/Eyecon/Facebook/Instagram/Google), deep OSINT (spam/breach/web), Folium maps, HTML + JSON reports, .env support |
| **v3.0** | Multi-API live location, telecom circle DB, roaming detection |
| **v2.0** | Basic OSINT, geolocation, map generation |
| **v1.0** | Initial phone number lookup with phonenumbers library |

---

## ⚠️ Disclaimer

> **This tool is intended for educational purposes and authorized security research ONLY.**
> Unauthorized tracking, surveillance, or data collection of individuals without their consent is **illegal** in most jurisdictions.
> The author assumes **no liability** for misuse.
> Always obtain proper authorization before using this tool on any phone number.
> All operations are **audit-logged** with timestamps and operator identification.

---

**Made with ❤️ by Vishal | PhoneTrackerPro v5.0.0**
