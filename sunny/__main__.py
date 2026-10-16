import sys

from sunny.cli import WeatherCLI
from sunny.utility import WeatherError


def main():
    """Application entry point."""
    try:
        app = WeatherCLI()
        app.run()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except BrokenPipeError:
        sys.exit(0)
    except (WeatherError, OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
