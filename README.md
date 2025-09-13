<div align="center">

# Sunny 🌞

[![version](https://img.shields.io/badge/version-1.4.0-blue)](https://github.com/bremsstrahlung-57/sunny/releases/tag/v1.4.0)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)

</div>

A minimal, themeable CLI weather tool for your terminal. Get beautifully displayed weather information right where you need it.

## Features

- **Minimal & Clean** - Clean interface that shows you just what you need
- **Customizable** - Personalize your weather display with themes and color schemes
- **ASCII Art** - Fun and informative ASCII art representing current weather conditions
- **Essential Info** - Temperature (°C/°F), wind speed, and humidity
- **Terminal-Friendly** - Designed for a great experience in any terminal
- **5-Day Forecast** - Extended weather forecast support

![preview1_default](https://github.com/user-attachments/assets/ee910cef-501a-46c2-86cf-9628eaca5f44)
![preview2_new_york_city_and_default_forecast](https://github.com/user-attachments/assets/8e72cd5d-1054-4a4a-a903-d634d4df24b3)


## Installation

### Quick Install (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/bremsstrahlung-57/sunny/master/install.sh | bash
```

This script will automatically:
- Download the latest release
- Install using pipx (if available) for isolated installation
- Fall back to pip if pipx is unavailable
- Clean up downloaded files

### Manual Installation

1. Download the `.whl` file from the [latest release](https://github.com/bremsstrahlung-57/sunny/releases/latest)

2. Install using your preferred method:

    **Using pipx (Recommended)**
    ```bash
    pipx install sunny-1.4.0-py3-none-any.whl
    ```

    **Using pip**
    ```bash
    pip install sunny-1.4.0-py3-none-any.whl
    ```

## Configuration

1. **Get an API Key** from [OpenWeatherMap](https://openweathermap.org/appid) (free account required)

2. **Initialize Sunny**
    ```bash
    sunny --init
    ```
    Follow the prompts to enter your API key and set a default location.

## Usage

```bash
# Get weather for your default location
sunny

# Get weather for a specific city (use underscores for spaces)
sunny -c New_York

# Display help
sunny -h

# Check version
sunny -v
```

## Development

```bash
git clone https://github.com/bremsstrahlung-57/sunny.git
cd sunny
pip install -e .
```

## Roadmap

- [ ] More weather metrics (pressure, AQI)
- [ ] Location auto-detection via IP
- [ ] Weather alerts and warnings
- [ ] Additional themes and languages
- [ ] Multiple weather API support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
