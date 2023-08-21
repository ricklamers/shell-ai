import os
import json

def load_config():
    # Determine the platform
    platform = os.name  # posix, nt, java, etc.
    config_app_name = "shell-ai"
    try:
        # Determine the path to the configuration file based on the platform
        if platform == 'posix':
            config_path = os.path.expanduser(f'~/.config/{config_app_name}/config.json')
        elif platform == 'nt':
            config_path = os.path.join(os.environ['APPDATA'], config_app_name, 'config.json')
        else:
            raise Exception('Unsupported platform')

        # Read the configuration file
        with open(config_path, 'r') as f:
            config = json.load(f)

        return config
    except Exception:
        return {}
