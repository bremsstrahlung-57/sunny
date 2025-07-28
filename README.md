# Sunny 🌞 [![version](https://img.shields.io/badge/version-1.2.6-blue)](https://github.com/bremsstrahlung-57/sunny/releases/tag/v1.2.6)

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

### Latest Release (v1.2.6)

#### Using pip (Recommended)
1. Install the `.whl` file from `Releases`. Latest version is `1.2.6`

2. Install it using `pip`
```bash
pip install sunny-1.2.6-py3-none-any.whl
```
3. You can delete the package (Optional)
```bash
rm sunny-1.2.6-py3-none-any.whl
```

#### Using pipx (Linux/macOS)
1. Install the `.whl` file from `Releases`. Latest version is `1.2.6`

2. Install it using `pipx`
```bash
pipx install sunny-1.2.6-py3-none-any.whl
```
3. You can delete the package (Optional)
```bash
rm sunny-1.2.6-py3-none-any.whl
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

## Future targets
- Add forecast support
- More data (pressure, AQI etc.)
- Toggle between current, hourly, and 7-day forecast.
- More languages support
- Location auto-detect via IP if no city is provided
- Warnings:  Warn user if storm, high UV, or rain expected today
- Adding More Themes
- Support multiple weather APIs