# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-10-16

### Added
- Daily forecast low/high temperatures and location-local forecast times.
- Support for `[display].show_forecast` and `[display].days` to customize the default forecast view.

### Changed
- Responsive weather cards and compact theme previews with automatic heights to prevent clipped content.
- Reuse one current-weather response across selected outputs and fetch current weather and forecasts concurrently when both are requested.
- Use HTTPS with connection/read timeouts and clearer API errors that do not expose the API key.

### Fixed
- Single-metric and ASCII-only commands no longer display an unintended forecast or full weather view.
- `--version` exits without loading configuration or fetching weather.
- Forecasts group three-hour samples by local date and select the sample nearest local noon instead of sampling at incorrect intervals.
- City names with spaces or underscores are correctly encoded in API requests.
- Configuration is loaded lazily without creating files during imports or read operations.
- Re-running `--init` restores missing built-in themes without overwriting existing configuration or theme files.
- Missing themes and partial custom themes fall back to built-in defaults; invalid box styles use a safe fallback.
- Placeholder API keys, invalid units, malformed configuration, and incomplete weather responses produce clearer errors.
- Temperature colors use the correct thresholds for Fahrenheit values.
- Theme and ASCII previews work without configuration, and ASCII preview syntax supports Python 3.9.
- Errors are written to stderr, and interrupted commands return exit code 130.

## [1.4.0] - 2025-09-13

### Added
- Forecast of 5-days

### Fixed
- A TypeError (`string indices must be integers`) that occurred when the weather API response was not in the expected format. Added validation to handle this gracefully.
- A rendering error (`closing tag '[/None]'`) by ensuring no None values are passed into the rich console output.
- Additionally, overall error handling has been improved to provide better user feedback on failures

### Fixed
- Correct data handling and rendering errors.

## [1.2.6] - 2025-07-28

### Changed
- Update installation script and README.

### Fixed
- The panel was not showing the whole weather data.
- Removed openweather api token.

## [1.2.5] - 2025-07-28

### Changed
- Update README, install script, and pyproject for version 1.2.5.
- Removed config files.

### Refactored
- Refactored the main code.

### Fixed
- Config files now work. Can edit and add new themes.

## [1.0.3] - 2025-07-20

### Added
- Themes support.
- ASCII art according to weather condition. Use `--showall` to show all ascii arts and `--ascii` to only show the ascii of current weather condition.
- ASCII art according to weather-conditions. More fluent and boxed output.
- Color-coded output for temperature, humidity, and weather condition.
- Support for `--temperature`, `--humidity`, `--version`, `--description`, `--units`, and `--about`.

### Changed
- Replace JSON configuration with TOML.

### Fixed
- Location with space in their name was having error in API calls.

## [1.0.0] - 2025-07-20

### Added
- Initial project setup.
- API calls and cli arguments.
- Package made `sunny` and added config files for user to add API Key and Default Location.
- New folder system for package building.

### Refactored
- Refactored `configure.py`.
- Refactored the main code.
