#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-all}"
copy(){ mkdir -p "$1"; cp -R "$ROOT"/skills/xc881-* "$1/"; }
case "$TARGET" in
  agents) copy "$HOME/.agents/skills" ;;
  claude) copy "$HOME/.claude/skills" ;;
  codex) copy "$HOME/.codex/skills" ;;
  cursor) copy "$HOME/.cursor/skills" ;;
  all) copy "$HOME/.agents/skills"; copy "$HOME/.claude/skills"; copy "$HOME/.codex/skills"; copy "$HOME/.cursor/skills" ;;
  *) echo "usage: scripts/install.sh agents|claude|codex|cursor|all"; exit 1 ;;
esac
