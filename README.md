# PiyuAI
**AI Coding Assistant powered by NVIDIA NIM** — like Claude Code, but runs on NVIDIA's inference platform.

---

## One-line Install (no Python needed)

### Linux / macOS
```bash
curl -fsSL https://raw.githubusercontent.com/Piyush-manwani/piyuai/main/install.sh | bash
```

### Windows (CMD)
```cmd

curl -L https://raw.githubusercontent.com/Piyush-manwani/piyuai/main/install.bat -o install.bat && install.bat
```

> The installer auto-downloads Python if missing, installs all deps, and adds `piyuai` to your PATH.

---

## Manual Install (if you have Python)

```bash
git clone https://github.com/Piyush-manwani/piyuAI.git
cd piyuai
pip install -r requirements.txt
python piyuai.py
```

---

## First Launch
Get a free NVIDIA NIM API key at https://build.nvidia.com — Piyuai will ask on first run.

---

## Commands

| Command | Description |
|---|---|
| `/help` | Show all commands |
| `/model` | Switch NIM model |
| `/key` | Update API key |
| `/clear` | Clear history |
| `/run <code>` | Run a Python snippet |
| `/file <path>` | Load file into context |
| `/save [name]` | Save conversation |
| `/exit` | Quit |

---

## Uninstall

Linux/macOS: `rm -rf ~/.piyuAI && rm ~/.local/bin/piyuAI`  
Windows: `rmdir /s /q %USERPROFILE%\piyuAI`
