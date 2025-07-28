import sys
from sunny.cli import WeatherCLI


def main():
    """Application entry point."""
    try:
        app = WeatherCLI()
        app.run()

    except KeyboardInterrupt:

        print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)

    except Exception as e:

        print(f"[bold red]Unexpected error[/bold red]: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
