import sys
from sunny.cli import WeatherCLI


def main():
    """Application entry point."""
    try:
        app = WeatherCLI()
        app.run()

    except KeyboardInterrupt:

        print("\nOperation cancelled by user")
        sys.exit(0)

    except Exception as e:

        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
