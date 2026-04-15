#!/usr/bin/env python3
"""
Piyuai - AI Coding Assistant powered by NVIDIA NIM
Like Claude Code, but runs on NVIDIA's NIM inference platform.
"""

import os
import sys
import json
import subprocess
import tempfile
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    from openai import OpenAI
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.table import Table
    from rich.live import Live
    from rich.text import Text
    from rich import box
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.styles import Style
    from prompt_toolkit.key_binding import KeyBindings
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install openai rich prompt_toolkit")
    sys.exit(1)


# ─── Config ───────────────────────────────────────────────────────────────────

CONFIG_FILE = Path.home() / ".piyuai" / "config.json"
HISTORY_FILE = Path.home() / ".piyuai" / "history"
CONVERSATION_FILE = Path.home() / ".piyuai" / "conversation.json"

NVIDIA_NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"

AVAILABLE_MODELS = {
    "1": ("meta/llama-3.1-70b-instruct",      "Llama 3.1 70B   – Fast, great for code"),
    "2": ("meta/llama-3.1-405b-instruct",     "Llama 3.1 405B  – Most powerful"),
    "3": ("mistralai/codestral-22b-instruct-v0.1", "Codestral 22B   – Code specialist"),
    "4": ("microsoft/phi-3-medium-128k-instruct",  "Phi-3 Medium    – Lightweight & fast"),
    "5": ("google/gemma-2-27b-it",            "Gemma 2 27B     – Google's open model"),
}

SYSTEM_PROMPT = """You are Piyuai, an expert AI coding assistant powered by NVIDIA NIM.
You help developers write, debug, explain, and improve code across all languages.

When writing code:
- Always use code blocks with the correct language identifier
- Explain what the code does briefly before or after
- Suggest improvements when you see potential issues
- Be concise but thorough

When debugging:
- Identify the root cause clearly
- Provide a corrected version of the code
- Explain why the bug occurred

You have access to tools the user can invoke via slash commands.
Always be direct, technical, and helpful."""


# ─── Utilities ────────────────────────────────────────────────────────────────

console = Console()

def ensure_config_dir():
    config_dir = Path.home() / ".piyuai"
    config_dir.mkdir(exist_ok=True)

def load_config() -> dict:
    ensure_config_dir()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(cfg: dict):
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

def load_conversation() -> list:
    if CONVERSATION_FILE.exists():
        with open(CONVERSATION_FILE) as f:
            return json.load(f)
    return []

def save_conversation(messages: list):
    ensure_config_dir()
    with open(CONVERSATION_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def clear_conversation():
    if CONVERSATION_FILE.exists():
        CONVERSATION_FILE.unlink()

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def detect_language(code: str) -> str:
    """Basic language detection from code content."""
    if re.search(r'^\s*(def |import |from .* import|class .*:)', code, re.M):
        return "python"
    if re.search(r'(const |let |var |=>|require\(|module\.exports)', code):
        return "javascript"
    if re.search(r'(#include|int main\(|std::)', code):
        return "cpp"
    if re.search(r'(func |package main|:=)', code):
        return "go"
    if re.search(r'(fn |let mut|use std::)', code):
        return "rust"
    return "text"


# ─── Display helpers ──────────────────────────────────────────────────────────

def print_banner():
    console.print()
    banner = Text()
    banner.append("  ██████╗ ██╗██╗   ██╗██╗   ██╗ █████╗ ██╗\n", style="bold green")
    banner.append("  ██╔══██╗██║╚██╗ ██╔╝██║   ██║██╔══██╗██║\n", style="bold green")
    banner.append("  ██████╔╝██║ ╚████╔╝ ██║   ██║███████║██║\n", style="bold green")
    banner.append("  ██╔═══╝ ██║  ╚██╔╝  ██║   ██║██╔══██║██║\n", style="bold green")
    banner.append("  ██║     ██║   ██║   ╚██████╔╝██║  ██║██║\n", style="bold green")
    banner.append("  ╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝\n", style="bold green")
    console.print(banner)
    console.print("  [dim]AI Coding Assistant · Powered by NVIDIA NIM[/dim]")
    console.print()

def print_help():
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold green")
    table.add_column("Command", style="cyan", width=22)
    table.add_column("Description", style="white")

    commands = [
        ("/help",         "Show this help"),
        ("/model",        "Switch NIM model"),
        ("/models",       "List all available models"),
        ("/key",          "Set/update NVIDIA NIM API key"),
        ("/clear",        "Clear conversation history"),
        ("/run <code>",   "Run a Python snippet"),
        ("/file <path>",  "Read a file and add to context"),
        ("/context",      "Show current context size"),
        ("/save <name>",  "Save conversation to file"),
        ("/exit / /quit", "Exit Piyuai"),
    ]
    for cmd, desc in commands:
        table.add_row(cmd, desc)

    console.print(Panel(table, title="[bold green]Piyuai Commands[/bold green]", border_style="green"))

def render_response(text: str):
    """Render assistant response, detecting and syntax-highlighting code blocks."""
    parts = re.split(r'(```(?:\w+)?\n[\s\S]*?```)', text)
    for part in parts:
        if part.startswith("```"):
            lines = part.strip().split("\n")
            lang = lines[0][3:].strip() or "text"
            code = "\n".join(lines[1:-1])
            console.print(Syntax(code, lang, theme="monokai", line_numbers=False,
                                  background_color="default"))
        elif part.strip():
            console.print(Markdown(part))


# ─── Setup wizard ─────────────────────────────────────────────────────────────

def setup_wizard() -> dict:
    console.print(Panel(
        "[bold]Welcome to Piyuai![/bold]\n\nLet's get you set up with NVIDIA NIM.\n"
        "Get a free API key at [link=https://build.nvidia.com]build.nvidia.com[/link]",
        border_style="green"
    ))

    api_key = console.input("\n[green]→[/green] Enter your NVIDIA NIM API key: ").strip()
    if not api_key:
        console.print("[red]No API key provided. Exiting.[/red]")
        sys.exit(1)

    console.print("\n[bold]Available models:[/bold]")
    for num, (model_id, desc) in AVAILABLE_MODELS.items():
        console.print(f"  [cyan]{num}[/cyan]  {desc}")

    choice = console.input("\n[green]→[/green] Choose model [1-5] (default: 1): ").strip() or "1"
    model_id = AVAILABLE_MODELS.get(choice, AVAILABLE_MODELS["1"])[0]

    cfg = {"api_key": api_key, "model": model_id}
    save_config(cfg)
    console.print(f"\n[green]✓[/green] Config saved. Using [bold]{model_id}[/bold]\n")
    return cfg


# ─── NIM client ───────────────────────────────────────────────────────────────

def get_client(api_key: str) -> OpenAI:
    return OpenAI(
        base_url=NVIDIA_NIM_BASE_URL,
        api_key=api_key
    )

def stream_response(client: OpenAI, model: str, messages: list) -> str:
    """Stream a response from NVIDIA NIM and return full text."""
    full_text = ""
    
    console.print(f"\n[dim]● piyuai[/dim] [dim]{get_timestamp()}[/dim]")
    
    with Live(console=console, refresh_per_second=15) as live:
        buffer = ""
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                max_tokens=4096,
                temperature=0.2,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                buffer += delta
                full_text += delta
                live.update(Text(buffer, style="white"))
        except Exception as e:
            live.update(Text(f"[Error] {e}", style="red"))
            return ""

    console.print()  # newline after streaming
    return full_text


# ─── Slash command handlers ───────────────────────────────────────────────────

def cmd_run(code_snippet: str):
    """Run a Python snippet and show output."""
    if not code_snippet.strip():
        console.print("[yellow]Usage: /run <python code>[/yellow]")
        return None

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code_snippet)
        tmpfile = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmpfile],
            capture_output=True, text=True, timeout=15
        )
        output = result.stdout or result.stderr or "(no output)"
        style = "green" if result.returncode == 0 else "red"
        console.print(Panel(output.strip(), title="[bold]Output[/bold]",
                             border_style=style))
        return output
    except subprocess.TimeoutExpired:
        console.print("[red]Execution timed out (15s limit)[/red]")
        return "Execution timed out"
    finally:
        Path(tmpfile).unlink(missing_ok=True)

def cmd_file(path_str: str, messages: list) -> list:
    """Read a file and inject into conversation context."""
    path = Path(path_str.strip()).expanduser()
    if not path.exists():
        console.print(f"[red]File not found: {path}[/red]")
        return messages

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        lang = path.suffix.lstrip(".") or "text"
        msg = f"Here is the file `{path.name}`:\n\n```{lang}\n{content}\n```"
        messages.append({"role": "user", "content": msg})
        console.print(f"[green]✓[/green] Loaded [bold]{path.name}[/bold] "
                       f"([dim]{len(content)} chars[/dim]) into context.")
    except Exception as e:
        console.print(f"[red]Could not read file: {e}[/red]")

    return messages

def cmd_switch_model(cfg: dict) -> dict:
    console.print("\n[bold]Available models:[/bold]")
    for num, (model_id, desc) in AVAILABLE_MODELS.items():
        current = " [green]← current[/green]" if model_id == cfg.get("model") else ""
        console.print(f"  [cyan]{num}[/cyan]  {desc}{current}")

    choice = console.input("\n[green]→[/green] Choose model [1-5]: ").strip()
    if choice in AVAILABLE_MODELS:
        cfg["model"] = AVAILABLE_MODELS[choice][0]
        save_config(cfg)
        console.print(f"[green]✓[/green] Switched to [bold]{cfg['model']}[/bold]")
    else:
        console.print("[yellow]Invalid choice, keeping current model.[/yellow]")
    return cfg

def cmd_save(name: str, messages: list):
    name = name.strip() or f"piyuai_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_path = Path.cwd() / f"{name}.json"
    with open(out_path, "w") as f:
        json.dump(messages, f, indent=2)
    console.print(f"[green]✓[/green] Saved conversation to [bold]{out_path}[/bold]")


# ─── Main REPL ────────────────────────────────────────────────────────────────

def main():
    print_banner()

    cfg = load_config()
    if not cfg.get("api_key"):
        cfg = setup_wizard()

    client = get_client(cfg["api_key"])
    model = cfg.get("model", AVAILABLE_MODELS["1"][0])
    messages = load_conversation()

    # Ensure system prompt is first
    if not messages or messages[0].get("role") != "system":
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    console.print(f"[dim]Model:[/dim] [green]{model}[/green]  "
                  f"[dim]History:[/dim] [green]{len([m for m in messages if m['role']=='user'])} messages[/green]  "
                  f"[dim]Type /help for commands[/dim]\n")

    # Prompt session
    prompt_style = Style.from_dict({"prompt": "bold ansibrightyellow"})
    session = PromptSession(
        history=FileHistory(str(HISTORY_FILE)),
        auto_suggest=AutoSuggestFromHistory(),
        style=prompt_style,
    )

    while True:
        try:
            user_input = session.prompt("\n❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            save_conversation(messages)
            break

        if not user_input:
            continue

        # ── Slash commands ──
        if user_input.startswith("/"):
            parts = user_input.split(None, 1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if cmd in ("/exit", "/quit"):
                console.print("[dim]Goodbye![/dim]")
                save_conversation(messages)
                break

            elif cmd == "/help":
                print_help()

            elif cmd == "/models":
                for num, (mid, desc) in AVAILABLE_MODELS.items():
                    cur = " [green]●[/green]" if mid == model else "  "
                    console.print(f"  {cur}[cyan]{num}[/cyan]  {desc}")

            elif cmd == "/model":
                cfg = cmd_switch_model(cfg)
                model = cfg["model"]
                client = get_client(cfg["api_key"])

            elif cmd == "/key":
                new_key = console.input("[green]→[/green] New NVIDIA NIM API key: ").strip()
                if new_key:
                    cfg["api_key"] = new_key
                    save_config(cfg)
                    client = get_client(new_key)
                    console.print("[green]✓[/green] API key updated.")

            elif cmd == "/clear":
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                clear_conversation()
                console.print("[green]✓[/green] Conversation cleared.")

            elif cmd == "/run":
                output = cmd_run(arg)
                if output:
                    messages.append({"role": "user",
                                     "content": f"I just ran this code and got:\n```\n{output}\n```"})

            elif cmd == "/file":
                messages = cmd_file(arg, messages)

            elif cmd == "/context":
                total = sum(len(m["content"]) for m in messages)
                user_msgs = len([m for m in messages if m["role"] == "user"])
                console.print(f"[dim]Messages:[/dim] [green]{user_msgs}[/green]  "
                               f"[dim]Characters:[/dim] [green]{total:,}[/green]")

            elif cmd == "/save":
                cmd_save(arg, messages)

            else:
                console.print(f"[yellow]Unknown command: {cmd}. Type /help for help.[/yellow]")

            continue

        # ── Regular message → NIM ──
        messages.append({"role": "user", "content": user_input})

        try:
            response_text = stream_response(client, model, messages)
            if response_text:
                messages.append({"role": "assistant", "content": response_text})
                save_conversation(messages)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            messages.pop()  # remove failed user message


if __name__ == "__main__":
    main()
