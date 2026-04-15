#!/bin/bash
set -e

# ── Colors ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

echo ""
echo -e "${GREEN}${BOLD}"
echo "  ██████╗ ██╗██╗   ██╗██╗   ██╗ █████╗ ██╗"
echo "  ██╔══██╗██║╚██╗ ██╔╝██║   ██║██╔══██╗██║"
echo "  ██████╔╝██║ ╚████╔╝ ██║   ██║███████║██║"
echo "  ██╔═══╝ ██║  ╚██╔╝  ██║   ██║██╔══██║██║"
echo "  ██║     ██║   ██║   ╚██████╔╝██║  ██║██║"
echo "  ╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝"
echo -e "${RESET}"
echo -e "  ${CYAN}AI Coding Assistant · Powered by NVIDIA NIM${RESET}"
echo ""

INSTALL_DIR="$HOME/.piyuai"
BIN_DIR="$HOME/.local/bin"
PIYUAI_URL="https://raw.githubusercontent.com/Piyush-manwani/piyuai/main/piyuai.py"

# ── Check / install Python ─────────────────────────────────────────────────
install_python() {
    echo -e "${YELLOW}[~]${RESET} Python not found. Attempting to install..."

    if command -v apt-get &>/dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y python3 python3-pip
    elif command -v brew &>/dev/null; then
        brew install python
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &>/dev/null; then
        sudo pacman -Sy --noconfirm python python-pip
    else
        echo -e "${RED}[✗]${RESET} Cannot auto-install Python on this system."
        echo "    Please install Python 3.8+ from https://python.org and re-run this script."
        exit 1
    fi
}

if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    install_python
else
    PYVER=$(python3 --version 2>/dev/null || python --version 2>/dev/null)
    echo -e "${GREEN}[✓]${RESET} Found $PYVER"
fi

# Pick python command
PYTHON=$(command -v python3 || command -v python)

# ── Create install directory ───────────────────────────────────────────────
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# ── Download piyuai.py ─────────────────────────────────────────────────────
echo -e "${YELLOW}[~]${RESET} Downloading Piyuai..."
curl -fsSL "$PIYUAI_URL" -o "$INSTALL_DIR/piyuai.py"
echo -e "${GREEN}[✓]${RESET} Downloaded piyuai.py"

# ── Install pip if missing ─────────────────────────────────────────────────
if ! $PYTHON -m pip --version &>/dev/null; then
    echo -e "${YELLOW}[~]${RESET} Installing pip..."
    curl -fsSL https://bootstrap.pypa.io/get-pip.py | $PYTHON
fi

# ── Install dependencies ───────────────────────────────────────────────────
echo -e "${YELLOW}[~]${RESET} Installing dependencies..."
$PYTHON -m pip install --quiet --upgrade openai rich prompt_toolkit
echo -e "${GREEN}[✓]${RESET} Dependencies installed."

# ── Create launcher ────────────────────────────────────────────────────────
cat > "$BIN_DIR/piyuai" << EOF
#!/bin/bash
exec $PYTHON "$INSTALL_DIR/piyuai.py" "\$@"
EOF
chmod +x "$BIN_DIR/piyuai"

# ── Add ~/.local/bin to PATH if needed ────────────────────────────────────
add_to_path() {
    local shell_rc="$1"
    if [ -f "$shell_rc" ] && ! grep -q 'local/bin' "$shell_rc"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$shell_rc"
        echo -e "${GREEN}[✓]${RESET} Added ~/.local/bin to PATH in $shell_rc"
    fi
}

add_to_path "$HOME/.bashrc"
add_to_path "$HOME/.zshrc"
add_to_path "$HOME/.profile"

export PATH="$HOME/.local/bin:$PATH"

echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║   Piyuai installed successfully!             ║${RESET}"
echo -e "${GREEN}${BOLD}║                                              ║${RESET}"
echo -e "${GREEN}${BOLD}║   Run:  ${CYAN}piyuai${GREEN}                              ║${RESET}"
echo -e "${GREEN}${BOLD}║                                              ║${RESET}"
echo -e "${GREEN}${BOLD}║   Get your free NVIDIA NIM API key at:       ║${RESET}"
echo -e "${GREEN}${BOLD}║     https://build.nvidia.com                 ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${YELLOW}Tip:${RESET} Open a new terminal or run ${CYAN}source ~/.bashrc${RESET} first."
echo ""
