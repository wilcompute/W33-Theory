#!/usr/bin/env bash
# Install Sage in WSL via micromamba/conda-forge (no sudo needed)
set -euo pipefail

echo "=== Installing Sage via micromamba (no sudo required) ==="

# Check if micromamba exists
if ! command -v micromamba >/dev/null 2>&1; then
  echo "Installing micromamba..."
  cd ~
  curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
  export PATH="$HOME/bin:$PATH"
  micromamba shell init -s bash -p ~/micromamba
  source ~/.bashrc || true
fi

# Create sage environment
echo "Creating sage environment..."
micromamba create -n sage -c conda-forge sagemath -y

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
