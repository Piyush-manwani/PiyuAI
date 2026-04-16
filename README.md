# PiyuAI 🟢
**AI Coding Assistant powered by NVIDIA NIM** — like Claude Code, but runs on NVIDIA's inference platform.

---

## ⚡ Install

### Windows
```cmd
curl -L --max-redirs 10 https://github.com/Piyush-manwani/PiyuAI/releases/download/1.0.0/PiyuAI_setup.exe -o PiyuAI_setup.exe
```
Then double-click `PiyuAI_setup.exe` to install.

Or download directly: [PiyuAI_setup.exe](https://github.com/Piyush-manwani/PiyuAI/releases/download/1.0.0/PiyuAI_setup.exe)

### macOS
```bash
curl -L --max-redirs 10 https://github.com/Piyush-manwani/PiyuAI/releases/download/1.0.0/PiyuAI.dmg -o PiyuAI.dmg
```
Then open `PiyuAI.dmg` and drag PiyuAI to your Applications folder.

Or download directly: [PiyuAI.dmg](https://github.com/Piyush-manwani/PiyuAI/releases/download/1.0.0/PiyuAI.dmg)

---

## First Launch
On first run, PiyuAI will ask for your **NVIDIA NIM API key**.
Get one free at 👉 [build.nvidia.com](https://build.nvidia.com)

---

## Commands

| Command | Description |
|---|---|
| `/help` | Show all commands |
| `/model` | Switch NIM model |
| `/key` | Update API key |
| `/clear` | Clear conversation history |
| `/run <code>` | Execute a Python snippet |
| `/file <path>` | Load a file into context |
| `/save [name]` | Save conversation to JSON |
| `/exit` | Quit PiyuAI |

---

## Available Models

| # | Model | Best For |
|---|---|---|
| 1 | meta/llama-3.1-70b-instruct | Fast, general coding (default) |
| 2 | meta/llama-3.1-405b-instruct | Most powerful |
| 3 | mistralai/codestral-22b-instruct-v0.1 | Code specialist |
| 4 | microsoft/phi-3-medium-128k-instruct | Lightweight & fast |
| 5 | google/gemma-2-27b-it | Google's open model |

---

## Uninstall

**Windows:** Go to Settings → Apps → search PiyuAI → Uninstall

**macOS:** Drag PiyuAI from Applications to Trash
