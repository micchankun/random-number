#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ -z "${AQUESTALK_LIB:-}" ]]; then
  echo "AQUESTALK_LIB を設定してください。例:"
  echo "  export AQUESTALK_LIB=/path/to/libAquesTalk.so"
  exit 1
fi
exec python3 "$SCRIPT_DIR/server.py"
