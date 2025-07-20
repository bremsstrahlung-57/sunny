#!/bin/bash
set -e

echo "🌤️ Installing Sunny Weather CLI..."
curl -L -O https://github.com/bremsstrahlung-57/sunny/releases/download/v1.0.2/sunny-1.0.2-py3-none-any.whl
python3 -m pip install sunny-1.0.2-py3-none-any.whl
rm sunny-1.0.2-py3-none-any.whl
echo "✅ Done! Run it with: sunny"