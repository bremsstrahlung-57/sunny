# Sunny 🌞 [![version](https://img.shields.io/badge/version-1.2.6-blue)](https://github.com/bremsstrahlung-57/sunny/releases/tag/v1.2.6) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A minimal, themeable CLI weather tool for your terminal. Get beautifully displayed weather information right where you need it.

## Features ✨

- **Minimal & Clean:** A clean interface that shows you just what you need.
- **Customizable:** Personalize your weather display with themes and color schemes.
- **ASCII Art:** Fun and informative ASCII art representing current weather conditions.
- **Essential Info:** Get temperature (°C/°F), wind speed, and humidity.
- **Terminal-Friendly:** Designed for a great experience in any terminal.

## Installation 📦

The only way to install `sunny` for now is from the `.whl` file from the latest release.

1.  **Download the `.whl` file** from the [latest release](https://github.com/bremsstrahlung-57/sunny/releases/latest).

2.  **Install the package**. You have two options:

    -   **Using `pipx` (Recommended for CLI tools)**: This installs `sunny` globally in an isolated environment, so it won't conflict with other packages.

        ```bash
        pipx install sunny-1.2.6-py3-none-any.whl
        ```

    -   **Using `pip`**: This installs `sunny` in your current Python environment.

        ```bash
        pip install sunny-1.2.6-py3-none-any.whl
        ```

3.  **Clean up (Optional)**. You can now delete the downloaded file.
    -   On **Linux/macOS**:
        ```bash
        rm sunny-1.2.6-py3-none-any.whl
        ```
    -   On **Windows**:
        ```powershell
        del sunny-1.2.6-py3-none-any.whl
        ```

## Configuration ⚙️

Before you can fetch weather data, you need to configure `sunny` with your OpenWeatherMap API key.

1.  **Get an API Key:**
    Sign up for a free account on [OpenWeatherMap](https://openweathermap.org/appid) to get your API key.

2.  **Initialize Sunny:**
    Run the following command to initialize `sunny`. It will prompt you to enter your API key and set a default location.

    ```bash
    sunny --init
    ```

## Quick Start 🚀

Once configured, you can get the weather instantly.

```bash
# Get the weather for your default location
sunny

# Get weather for a specific city
# (use underscores for cities with spaces)
sunny -c New_York

# Display help for all commands
sunny -h

# Check the installed version
sunny -v
```

## Development Setup 🛠️

If you want to contribute or customize themes:

```bash
git clone https://github.com/bremsstrahlung-57/sunny.git
cd sunny
pip install -e .
```

## Future Targets 🎯

- **Forecast Support:** Add daily and hourly forecasts.
- **More Data:** Include pressure, AQI, and other useful metrics.
- **Location Auto-Detect:** Automatically find the user's location via IP address.
- **Weather Alerts:** Warn users about storms, high UV, or rain.
- **More Themes & Languages:** Expand customization and accessibility.
- **Support for More Weather APIs:** Add more data sources.