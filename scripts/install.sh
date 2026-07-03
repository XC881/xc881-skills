#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-all}"
copy(){
  mkdir -p "$1"
  for skill in "$ROOT"/skills/xc881-*; do
    name="$(basename "$skill")"
    rm -rf "$1/$name"
    cp -R "$skill" "$1/"
  done
}
case "$TARGET" in
  agents) copy "$HOME/.agents/skills" ;;
  claude) copy "$HOME/.claude/skills" ;;
  codex) copy "$HOME/.codex/skills" ;;
  cursor) copy "$HOME/.cursor/skills" ;;
  cc-switch) copy "$HOME/.cc-switch/skills" ;;
  all) copy "$HOME/.agents/skills"; copy "$HOME/.claude/skills"; copy "$HOME/.codex/skills"; copy "$HOME/.cursor/skills"; copy "$HOME/.cc-switch/skills" ;;
  *) echo "usage: scripts/install.sh agents|claude|codex|cursor|cc-switch|all"; exit 1 ;;
esac
