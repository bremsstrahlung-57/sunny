# Sunny 🌞

A minimal, themeable CLI weather tool for your terminal - beautifully display weather information right where you need it.

## Features ✨

- Minimal and clean interface
- Customizable Themes and Color Schemes
- Create and Share Custom Themes
- ASCII Art of Weather Condition
- Multiple Temperature Units (°C/°F)
- Wind Speed
- Humidity
- Terminal-friendly Output
- Minimal Resource Usage

## Installation 📦

### Latest Release (v1.2.5)

#### Using pip (Recommended)
1. Install the `.whl` file from `Releases`. Latest version is `1.2.5`

2. Install it using `pip`
```bash
pip install sunny-1.2.5-py3-none-any.whl
```
3. You can delete the package (Optional)
```bash
rm sunny-1.2.5-py3-none-any.whl
```

#### Using pipx (Linux/macOS)
1. Install the `.whl` file from `Releases`. Latest version is `1.2.5``

2. 
```bash
pipx install sunny-1.2.5-py3-none-any.whl
```
3. Optional
```bash
rm sunny-1.2.5-py3-none-any.whl
```

## Quick Start 🚀

```bash
# Initialize sunny with your preferences
sunny --init

# Get current weather
sunny

# Display help
sunny -h

# Check version
sunny -v
```

## Development Setup 🛠️

To contribute or customize themes:

```bash
git clone https://github.com/bremsstrahlung-57/sunny.git
cd sunny
python3 -m pip install -e .
```