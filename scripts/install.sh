#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

copy(){
  local dest_root="$1"
  if [ -z "$dest_root" ] || [ "$dest_root" = "/" ] || [ "$dest_root" = "$HOME" ]; then
    echo "install.sh: refusing dest root: ${dest_root:-<empty>}" >&2
    return 1
  fi
  mkdir -p "$dest_root"
  local skill name dest
  for skill in "$ROOT"/skills/xc881-*; do
    name="$(basename "$skill")"
    case "$name" in
      xc881-*) ;;
      *)
        echo "install.sh: refusing skill name: $name" >&2
        return 1
        ;;
    esac
    dest="$dest_root/$name"
    if [ -e "$dest" ]; then
      if [ -L "$dest" ] || [ ! -d "$dest" ] || [ ! -f "$dest/SKILL.md" ]; then
        echo "install.sh: refusing to replace $dest" >&2
        return 1
      fi
      rm -rf "$dest"
    fi
    cp -R "$skill" "$dest_root/"
  done
}

install_target(){
  case "$1" in
    agents) copy "$HOME/.agents/skills" ;;
    claude) copy "$HOME/.claude/skills" ;;
    codex) copy "$HOME/.codex/skills" ;;
    cursor) copy "$HOME/.cursor/skills" ;;
    cc-switch) copy "$HOME/.cc-switch/skills" ;;
    grok) copy "$HOME/.grok/skills" ;;
    all)
      copy "$HOME/.agents/skills"
      copy "$HOME/.claude/skills"
      copy "$HOME/.codex/skills"
      copy "$HOME/.cursor/skills"
      copy "$HOME/.cc-switch/skills"
      copy "$HOME/.grok/skills"
      ;;
    *)
      echo "usage: scripts/install.sh agents|claude|codex|cursor|cc-switch|grok|all" >&2
      return 1
      ;;
  esac
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  install_target "${1:-all}"
fi
