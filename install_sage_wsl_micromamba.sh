#!/usr/bin/env bash
# Install Sage in WSL via micromamba/conda-forge (no sudo needed)
set -euo pipefail

echo "=== Installing Sage via micromamba (no sudo required) ==="
MAMBA_ROOT_PREFIX="${MAMBA_ROOT_PREFIX:-$HOME/micromamba}"
export MAMBA_ROOT_PREFIX
export PATH="$HOME/bin:$PATH"

# Check if micromamba exists
if ! command -v micromamba >/dev/null 2>&1; then
  echo "Installing micromamba..."
  cd ~
  curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest -o /tmp/micromamba.tar.bz2
  tar -xvjf /tmp/micromamba.tar.bz2 -C "$HOME" bin/micromamba
  micromamba shell init -s bash -r "$MAMBA_ROOT_PREFIX"
  source ~/.bashrc || true
fi

# Create sage environment
echo "Creating sage environment..."
micromamba create -n sage -c conda-forge sage -y

echo ""
echo "=== Installation complete! ==="
echo ""
echo "To use Sage, run:"
echo "  micromamba activate sage"
echo "  sage -v"
echo ""
echo "To make it permanent, add to your ~/.bashrc:"
echo "  eval \"\$(micromamba shell hook --shell bash)\""
echo "  micromamba activate sage"
