# Discord-Hawk – Encrypted Discord C2 Implant Builder

**Discord-Hawk** is a Python-based builder that produces fully-encrypted, stealth-enhanced Discord bot implants for authorized red-team engagements.
Every payload is protected with AES-256-GCM, configured at build time with a random key, and includes automated forensic trace removal and hidden persistence.
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.0+-purple?style=flat-square&logo=discord)](https://discordpy.readthedocs.io/)
[![Cryptography](https://img.shields.io/badge/Encryption-AES--256--GCM-red?style=flat-square)](https://cryptography.io/)
[![PyInstaller](https://img.shields.io/badge/PyInstaller-6.0+-yellow?style=flat-square&logo=python)](https://pyinstaller.org/)
[![Pillow](https://img.shields.io/badge/Pillow-10+-green?style=flat-square&logo=pillow)](https://python-pillow.org/)
[![psutil](https://img.shields.io/badge/psutil-System-blue?style=flat-square)](https://github.com/giampaolo/psutil)
[![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20Only-orange?style=flat-square)](https://microsoft.com/windows)
[![Stealth](https://img.shields.io/badge/Stealth-Advanced-red?style=flat-square)](https://github.com)

> ⚠️ **STRICTLY FOR AUTHORISED USE** – Use only on systems you own or have explicit written permission to test.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Core Libraries**:
  - `discord.py` – Discord API integration
  - `cryptography` – AES-256-GCM encryption
  - `pyinstaller` – One-file executable compilation
  - `pillow` – Screenshot capture
  - `psutil` – System information & process management
- **Persistence**: Windows Scheduled Tasks (`schtasks`)
- **Anti-Forensics**: Registry manipulation, Event Logs, PowerShell history
- **Build System**: PyInstaller (single standalone executable)

---

## ✅ Implemented Features
- 🔐 **Per-build random AES-256 key** – Each implant uses a unique 32-byte key; no two builds share a secret.
- 🛡️ **Encrypted configuration** – Discord token, channel ID, and operator ID are encrypted (AES-256-GCM) inside the executable, never in plaintext.
- 🤫 **Silent DM notification** – When an implant connects, the operator receives a private Discord message with system info — nothing appears in the channel.
- 🧹 **Forensic trace removal** – Automatically wipes:
  - PowerShell console history (`PSReadLine`)
  - Run dialog history (`RunMRU`)
  - Recent files shortcuts
  - PowerShell Prefetch files
  - Windows Event Logs (if running as admin)
- 🔒 **Hidden persistence** – Installed as a Scheduled Task that triggers at user logon. Does **not** show in Task Manager’s Startup tab. Installed/removed via `!persist` / `!removepersist`.
- 💻 **Remote control** – Full command set via Discord messages:
  - `!ping`, `!list`, `!cd`, `!cmd`, `!screenshot`, `!upload`, `!download`
  - `!clearlogs` (manual cleanup), `!persist`, `!removepersist`, `!kill`
- 🧬 **Modular structure** – Clear separation between builder, encryption, and implant logic for easy expansion.

---

## 🧱 How It Works
```
 Builder (builder.py)
    │
    ├─ Asks for Discord credentials
    ├─ Generates random 32-byte AES key
    ├─ Encrypts config with key
    ├─ Injects encrypted blob + key into implant template
    └─ Compiles with PyInstaller → single .exe

 Implant (generated .exe)
    │
    ├─ Decrypts config in memory
    ├─ Connects to Discord (DM to operator)
    ├─ Listens for commands
    ├─ Executes commands, auto-clears traces after each
    └─ Can install/remove persistence
```

---

## 📁 File Structure
```
Discord-Hawk/
├── builder.py              # Builder script (generates implant)
├── crypto_utils.py         # AES-256-GCM encrypt/decrypt
├── implant_template.py     # Implant source with placeholders
├── requirements.txt        # Dependencies
└── README.md
```

---

## 🚀 Quick Start
### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Build an implant
```bash
python3 builder.py
```
Enter your Discord bot token, channel ID, and your user ID.

The builder creates `dist/svchost_update.exe`.

### 3. Deploy (on authorised target)
Run the `.exe` on the target Windows machine. The operator will receive a **private Discord message** with system info and a list of available commands.

---

## 🎮 Available Commands
| Command          | Action                                      |
|------------------|---------------------------------------------|
| `!ping`          | Show latency and admin status               |
| `!list`          | List connected implants                     |
| `!cd <path>`     | Change working directory                    |
| `!cmd <command>` | Run PowerShell command (traces cleared)     |
| `!screenshot`    | Capture and send screen                     |
| `!upload`        | Upload a file (attach to your message)      |
| `!download <path>` | Download a file from the target           |
| `!clearlogs`     | Manually wipe forensic traces               |
| `!persist`       | Install hidden persistence (Scheduled Task) |
| `!removepersist` | Remove the persistence task                 |
| `!kill`          | Terminate the implant                       |

---

## 🔐 Security
- **AES-256-GCM** – Authenticated encryption, 96-bit random nonce per encryption.
- **No static key** – Each build uses `os.urandom(32)`.
- **In-memory only decryption** – Config exists as plaintext only during execution.
- **Silent C2** – All startup info goes via DM, not the public channel.
- **Anti-forensics** – Multiple layers of cleanup after each command.

---

## 🗺️ Roadmap (Upcoming)
- [ ] Process hollowing (inject into `RuntimeBroker.exe`)
- [ ] Steganographic data exfiltration (hide output in images)
- [ ] AMSI / ETW runtime patching
- [ ] USB-based config retrieval (for air-gapped delivery)

---

## ⚠️ Legal & Ethical
This tool is for **educational purposes, authorised penetration testing, and red-team operations only**.  
The author assumes no liability for misuse. You are responsible for complying with all applicable laws.

---

## 📄 License

**MIT License**

Copyright (c) 2026 Discord-Hawk Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
