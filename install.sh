echo "🌤️ Installing Sunny Weather CLI..."
curl -L https://github.com/bremsstrahlung-57/sunny/releases/download/v1.0.0/sunny-1.0.0-py3-none-any.whl -o sunny.whl
pip install sunny.whl
rm sunny.whl
echo "✅ Installation complete! Try: sunny"