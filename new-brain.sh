#!/usr/bin/env bash
# new-brain.sh — stamp out a new self-compiling knowledge brain from _skeleton/.
#
# Usage:
#   ./new-brain.sh "LLM Memory & Agent Systems"            # -> brains/llm-memory-agent-systems
#   ./new-brain.sh "Robotics SOTA" ~/vaults/robotics       # custom target path
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SKELETON="$ROOT/_skeleton"

NAME="${1:-}"
if [ -z "$NAME" ]; then
  echo "Usage: ./new-brain.sh \"Brain Name\" [target_dir]" >&2
  exit 1
fi

# slug: lowercase, spaces/punct -> hyphens
SLUG="$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"
TARGET="${2:-$ROOT/brains/$SLUG}"
TODAY="$(date +%Y-%m-%d)"

if [ -e "$TARGET" ]; then
  echo "Target already exists: $TARGET" >&2
  exit 1
fi

# escape a string for safe use in the REPLACEMENT half of sed s///  (handles \ & /)
esc() { printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/&/\\&/g' -e 's/\//\\\//g'; }
NAME_E="$(esc "$NAME")"; SLUG_E="$(esc "$SLUG")"; TODAY_E="$(esc "$TODAY")"

cp -R "$SKELETON" "$TARGET"
rm -rf "$(find "$TARGET" -name '__pycache__' -type d 2>/dev/null)" 2>/dev/null || true

# fill placeholders in text files
find "$TARGET" -type f \( -name '*.md' -o -name '*.txt' \) -print0 | while IFS= read -r -d '' f; do
  sed -i.bak \
    -e "s/{{BRAIN_NAME}}/$NAME_E/g" \
    -e "s/{{BRAIN_SLUG}}/$SLUG_E/g" \
    -e "s/{{DATE}}/$TODAY_E/g" \
    "$f"
  rm -f "$f.bak"
done

# each brain is its own portable git repo (identity is self-contained so it works anywhere)
if command -v git >/dev/null 2>&1; then
  ( cd "$TARGET" \
    && git init -q \
    && git add -A \
    && git -c user.name="brain-template" -c user.email="brain@local" \
         commit -qm "init brain: $NAME" ) || true
fi

echo "Created brain: $NAME"
echo "  -> $TARGET"
echo ""
echo "Next:"
echo "  1. Edit $TARGET/BRAIN.md  (fill in scope, page types, seed concepts)"
echo "  2. Open $TARGET in Obsidian"
echo "  3. Drop sources into $TARGET/raw/  then run your agent: 'compile new sources'"
