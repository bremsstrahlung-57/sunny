#!/bin/bash

VERSION="1.4.0"
FILE="sunny-${VERSION}-py3-none-any.whl"
URL="https://github.com/bremsstrahlung-57/sunny/releases/download/v${VERSION}/${FILE}"

echo "🌤️  Installing Sunny Weather CLI v${VERSION}..."

# Download the file
curl -L -O "${URL}"

# Check if pipx is installed and use it, otherwise fall back to pip
if command -v pipx &> /dev/null; then
    echo "🚀 pipx found. Installing with pipx for a clean, isolated installation..."
    pipx install "${FILE}"
else
    echo "⚠️  pipx not found. Falling back to pip. For a better experience, consider installing pipx."
    python3 -m pip install "${FILE}"
fi

# Clean up the downloaded file
rm "${FILE}"

echo "✅ Done! Setup Sunny with: sunny --init"