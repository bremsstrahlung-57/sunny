# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
