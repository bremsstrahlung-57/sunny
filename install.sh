#!/bin/bash
echo "🌤️ Installing Sunny Weather CLI..."
curl -L -O https://github.com/bremsstrahlung-57/sunny/releases/download/v1.2.5/sunny-1.2.5-py3-none-any.whl
python3 -m pip install sunny-1.2.5-py3-none-any.whl
rm sunny-1.2.5-py3-none-any.whl
echo "✅ Done! Setup it with: sunny --init"