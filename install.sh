#!/bin/bash
echo "🌤️ Installing Sunny Weather CLI..."
curl -L -o sunny.whl "https://github.com/bremsstrahlung-57/sunny/releases/download/v1.0.0/sunny-1.0.0-py3-none-any.whl"
python3 -m pip install sunny.whl
rm sunny.whl
echo "✅ Installation complete! Try running: sunny"
