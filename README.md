<div align="center">

# Sunny 🌞

[![version](https://img.shields.io/badge/version-1.5.0-blue)](https://github.com/bremsstrahlung-57/sunny/releases/tag/v1.4.0)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)

<img width="670" height="359" alt="Screenshot 2026-10-16 183220" src="https://github.com/user-attachments/assets/22a8fb47-17c6-47d4-ae26-1251a153b7fb" />
</div>

A minimal, themeable CLI weather tool for your terminal. Get beautifully displayed weather information right where you need it.

## Features

- **Minimal & Clean** - Clean interface that shows you just what you need
- **Customizable** - Personalize your weather display with themes and color schemes
- **ASCII Art** - Fun and informative ASCII art representing current weather conditions
- **Essential Info** - Temperature (°C/°F), wind speed, and humidity
- **Terminal-Friendly** - Designed for a great experience in any terminal
- **5-Day Forecast** - Daily cards with local times and forecast low/high temperatures
- **Efficient Requests** - Shared current-weather requests and concurrent fetching when current weather and forecasts are both requested


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
    Edit the generated `config.toml` at the printed path to set `[api].key` and `[defaults].location`.
    Running `--init` again restores missing built-in themes without overwriting your configuration or existing themes.

## Usage

```bash
# Get weather for your default location
sunny

# Get weather for a specific city (underscores also work)
sunny -c "New York"

# Show only selected metrics (one weather request, no automatic forecast)
sunny -t -y -d

# Show daily forecast cards in Fahrenheit
sunny --forecast -u imperial

# Combine selected current conditions and forecasts (fetched concurrently)
sunny -t --forecast

# Preview themes without configuring an API key
sunny --themes

# Display help
sunny -h

# Check version
sunny -v
```

Set `[display].show_forecast = true` in `config.toml` to include forecasts alongside the default current-weather view. `[display].days` limits the forecast to 1–5 days. Daily cards use the sample closest to local noon; low/high values cover the available three-hour forecast samples, not full-day observations.

## Development

With [uv](https://docs.astral.sh/uv/) installed:

```bash
git clone https://github.com/bremsstrahlung-57/sunny.git
cd sunny
uv sync
uv run sunny --help
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
