import os
import toml
import tomllib
from rich import print
from pathlib import Path
import importlib.resources as pkg_resources

def add_config():
    """Create and populate user config directory with default configuration files."""
    user_config_folder_path = Path.home() / ".config" / "sunny"
    theme_folder_path = user_config_folder_path / "themes"

    try:
        os.makedirs(user_config_folder_path, exist_ok=True)
        print(f"✓ Config directory ready at '{user_config_folder_path}'")
        os.makedirs(theme_folder_path, exist_ok=True)
        print(f"✓ Theme directory ready at '{theme_folder_path}'")

        config_files = {
            "config.template.toml": (user_config_folder_path, "config.template.toml"),
            "sunny_dynamic.toml": (theme_folder_path, "themes/sunny_dynamic.toml"),
            "minimal.toml": (theme_folder_path, "themes/minimal.toml"),
            "cyberpunk.toml": (theme_folder_path, "themes/cyberpunk.toml"),
        }
        for filename, (dest_dir, src_path) in config_files.items():
            dest_file = dest_dir / filename
            
            try:
                with pkg_resources.open_text('sunny', f'.config/{src_path}') as f:
                    data = tomllib.loads(f.read())

                with open(dest_file, 'w') as f:
                    toml.dump(data, f)
                print(f"✓ Created {dest_file}")

            except Exception as e:
                print(f"⚠️ Error with {filename}: {e}")

        print("\n✨ Configuration setup complete!")

    except Exception as e:
        print(f"⚠️ Error setting up config directory: {e}")