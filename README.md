# PiyuAI 🟢
**AI Coding Assistant powered by NVIDIA NIM** — like Claude Code, but runs on NVIDIA's inference platform.

---

## Install

### Windows
```
Then double-click `PiyuAI_setup.exe
```
###Macos
open `PiyuAI.dmg` but this one will need python

---

## First Launch
On first run, PiyuAI asks for your **NVIDIA NIM API key**.
Get one free at 👉 [build.nvidia.com](https://build.nvidia.com)

---

## Commands

### General
| Command | Description |
|---|---|
| `/help` | Show all commands |
| `/model` | Switch NIM model |
| `/models` | List available models |
| `/key` | Update API key |
| `/clear` | Clear conversation history |
| `/file <path>` | Load any file into context |
| `/context` | Show context size |
| `/save [name]` | Save conversation to JSON |
| `/exit` | Quit PiyuAI |

### Python
| Command | Description |
|---|---|
| `/run <code>` | Execute a Python snippet inline |

### Rust
| Command | Description |
|---|---|
| `/rust <code>` | Compile and run a Rust snippet |
| `/cargo <cmd>` | Run cargo in current project directory |
| `/rustfmt <code>` | Format Rust code with rustfmt |
| `/rustup` | Show Rust install instructions |

---

## Rust Integration

PiyuAI has first-class Rust support:

- **Run snippets instantly** — `/rust println!("hello");` compiles and runs with `rustc`, no project needed
- **Cargo integration** — `/cargo build`, `/cargo test`, `/cargo run` work in any Rust project directory
- **Auto wraps snippets** — you don't need to write `fn main()`, PiyuAI adds it for you
- **Formatter** — `/rustfmt` pretty-prints your Rust code via `rustfmt`
- **AI knows Rust** — asks about ownership, lifetimes, error handling, crates.io packages
- **Rust-aware file loading** — `/file src/main.rs` loads with proper Rust syntax highlighting in context

To use Rust features, install Rust from [rustup.rs](https://rustup.rs) — PiyuAI will detect it automatically on launch.

### Example Rust session
```
> write a rust function that reads a file and counts lines

> /rust
fn count_lines(path: &str) -> usize {
    std::fs::read_to_string(path).unwrap().lines().count()
}

> /cargo test

> /file src/main.rs
```

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

**Windows:** Settings → Apps → PiyuAI → Uninstall

**macOS:** Drag PiyuAI from Applications to Trash
