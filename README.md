# 🛡️ Security Toolkit API

A modular, security-focused REST API built with **FastAPI** that combines classic network reconnaissance tools with an **AI-powered analysis layer**. Run a port scan or a network discovery sweep, let a language model interpret the results like a security analyst would, and manage everything behind proper JWT authentication — all through a clean, well-documented API.

This project was built from the ground up as a learning project bridging **Cybersecurity** and **AI/Backend Engineering**, following a "Computer Science → Backend → Security → AI" roadmap rather than treating these as separate disciplines.

---

## ✨ What This Project Does

| Feature | Description |
|---|---|
| 🔍 **Port Scanner** | Multithreaded TCP port scanner with banner grabbing (identifies the service and version running on open ports) |
| 📡 **Network Discovery** | ARP-based LAN scanner that finds live devices on your network (IP, MAC address, hostname) |
| ⚙️ **Background Task Processing** | Scans run asynchronously — you get an instant task ID and poll for results, instead of the API hanging while a scan runs |
| 💾 **Persistent Storage** | Every scan result is saved to a SQLite database via SQLAlchemy, so nothing is lost when the server restarts |
| 🤖 **AI-Powered Analysis** | Feed any completed scan result to an LLM (via the Groq API) and get a human-readable security assessment — risks, CVEs, and remediation advice, not just raw data |
| 🔐 **JWT Authentication** | Full register/login/logout flow with hashed passwords (bcrypt) and a token blacklist for real logout support |
| 📚 **Auto-Generated Docs** | Every endpoint is instantly testable through FastAPI's built-in Swagger UI at `/docs` |

---

## 🏗️ Architecture

The project follows a clean, layered structure — each layer has exactly one job:

```
security-toolkit-api/
├── app/
│   ├── core/          # Database connection, config, security (hashing, JWT)
│   ├── models/        # Pydantic request models & SQLAlchemy database models
│   ├── routers/        # API endpoints — the "front door" of each feature
│   ├── services/       # The actual business logic (scanning, AI calls)
│   └── main.py         # Wires all routers into a single FastAPI app
├── requirements.txt
└── .env                # Secrets (never committed to git)
```

**Design principle:** routers handle HTTP concerns (requests, responses, auth checks); services handle the actual work (scanning a port, calling an AI model) and know nothing about HTTP. This separation makes each piece independently testable and easy to reason about.

---

## 🧰 Tech Stack

- **Framework:** FastAPI + Uvicorn
- **Database:** SQLite + SQLAlchemy ORM
- **Auth:** JWT (via `python-jose`) + `passlib`/`bcrypt` for password hashing
- **AI:** [Groq API](https://groq.com/) (LLM inference)
- **Networking:** `socket`, `scapy` (ARP scanning), `concurrent.futures.ThreadPoolExecutor` for concurrent scanning
- **Validation:** Pydantic v2

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed
- **Git** installed
- On Windows, network discovery (ARP scanning) requires **[Npcap](https://npcap.com/)** to be installed, and the terminal must be run **as Administrator**. On Linux/macOS, you'll need to run the server with `sudo` for the same reason.
- A free API key from [Groq Console](https://console.groq.com/) (for the AI analysis feature)

### 1. Clone the repository

```bash
git clone https://github.com/emirkrgl/security-toolkit-api.git
cd security-toolkit-api
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll know it worked if you see `(venv)` at the start of your terminal prompt.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Create a file named `.env` in the project root (same level as the `app/` folder) with the following content:

```env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_random_secret_key_here
```

- Get your `GROQ_API_KEY` for free at [console.groq.com](https://console.groq.com/) → API Keys → Create API Key.
- Generate a strong `SECRET_KEY` by running:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
  and pasting the output.

> ⚠️ **Never commit your `.env` file.** It's already listed in `.gitignore` — keep it that way.

### 5. Run the API

**On Windows, run your terminal as Administrator** (required for the network discovery feature), then:

```bash
uvicorn app.main:app --reload
```

If `uvicorn` isn't recognized directly, use:
```bash
python -m uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### 6. Explore the API

Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

This opens the interactive Swagger UI, where you can test every endpoint directly — including authenticating via the **Authorize** button once you've registered a user.

---

## 🔑 Typical Usage Flow

1. **Register** an account → `POST /auth/register`
2. **Log in** → `POST /auth/login` → copy the returned `access_token`
3. Click **Authorize** in `/docs` and paste your credentials (or the token) to unlock protected endpoints
4. **Start a scan** → `POST /scan/port` or `POST /scan/netdiscover` → you'll instantly get back a `task_id`
5. **Check the result** → `GET /scan/status/{task_id}` → poll until `status` becomes `"done"`
6. **Get an AI-written analysis** of that result → `POST /scan/analyze` with the same `task_id`
7. **Log out** whenever you're done → `POST /auth/logout` (the token is blacklisted and can no longer be used)

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/auth/register` | Create a new user account | ❌ |
| `POST` | `/auth/login` | Log in and receive a JWT access token | ❌ |
| `POST` | `/auth/logout` | Invalidate the current token | ✅ |
| `GET` | `/auth/me` | Get the currently logged-in user's info | ✅ |
| `DELETE` | `/auth/delete` | Permanently delete your account | ✅ |
| `POST` | `/scan/port` | Start a background TCP port scan | ✅ |
| `GET` | `/scan/status/{task_id}` | Check the status/result of a port scan | ❌ |
| `POST` | `/scan/netdiscover` | Start a background ARP network scan | ✅ |
| `GET` | `/scan/netdiscover/status/{task_id}` | Check the status/result of a network scan | ❌ |
| `POST` | `/scan/analyze` | Get an AI-generated security analysis of a completed scan | ✅ |

*(Full request/response schemas are available live at `/docs`.)*

---

## ⚠️ Responsible Use

This tool performs active network reconnaissance (port scanning, ARP discovery). **Only run it against systems and networks you own or have explicit permission to test.** Unauthorized scanning of third-party systems may be illegal depending on your jurisdiction. The `scanme.nmap.org` host is provided by the Nmap project specifically for safe, legal scan testing.

---

## 🗺️ Roadmap / What's Next

This project is a work in progress, built as part of a structured Cybersecurity + AI learning path. Planned additions include:

- [ ] Directory brute-forcer
- [ ] Packet sniffer integration
- [ ] Password auditor
- [ ] Mini intrusion detection system (IDS)
- [ ] Dockerized deployment
- [ ] Per-user scan history (linking scans to the authenticated user)

---

## 📄 License

This project is open source and available for learning purposes. Feel free to fork it, break it, and build on it.
