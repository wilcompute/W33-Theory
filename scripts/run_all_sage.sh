#!/usr/bin/env bash
set -euo pipefail

# Run the set of Sage verification scripts we want in CI or locally (inside a Sage container)
# This wrapper uses claude_workspace/run_sage.sh which prefers a usable 'sage' command.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
R=0
FAILURES=()

SAGE_WRAPPER="${REPO_ROOT}/claude_workspace/run_sage.sh"

SCRIPTS=(
  "claude_workspace/THEORY_PART_CXIII_SAGE_VERIFICATION.sage"
  "claude_workspace/THEORY_PART_CVII_SAGE_E8_TEST.sage"
  "claude_workspace/THEORY_PART_LIV_SAGE_VERIFICATION.py"
  "claude_workspace/THEORY_PART_CXVIII_EXPLICIT_CONSTRUCTION.py"
  "claude_workspace/THEORY_PART_CXIX_27_NONNEIGHBORS.py"
)

echo "Running Sage verification scripts..."
for s in "${SCRIPTS[@]}"; do
  echo "\n--- Running: $s ---"
  if [ ! -f "$s" ]; then
    echo "SKIP: $s not found"
    continue
  fi

  # Use run_sage.sh which will invoke sage -python or error out if Sage missing
  if "$SAGE_WRAPPER" "$s"; then
    echo "OK: $s"
  else
    R=$((R+1))
    FAILURES+=("$s")
    echo "FAILED: $s (recording and continuing)"
  fi
done

# Summarize
if [ ${#FAILURES[@]} -ne 0 ]; then
  echo "\nCompleted with ${#FAILURES[@]} failures:" 
  for f in "${FAILURES[@]}"; do
    echo " - $f"
  done
  exit 2
else
  echo "\nAll Sage verification scripts completed successfully."
fi
