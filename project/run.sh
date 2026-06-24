#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "${1:-$(dirname "${BASH_SOURCE[0]}")/src}" && pwd)"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAIN_FILE="$SRC_DIR/main.py"

echo "$MAIN_FILE"
pid="$(pgrep -af "python.*${MAIN_FILE}" | awk '{print $1}' || true)"
if [ -z "$pid" ]; then
    echo "No running Python processes found."
else
    echo "$pid"
    kill $pid
fi

cd "$SRC_DIR"
nohup uv run --project "$PROJECT_ROOT" python "$MAIN_FILE" > run.log &
