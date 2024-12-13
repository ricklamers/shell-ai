import os
import json

def debug_print(*args, **kwargs):
    if os.environ.get("DEBUG", "").lower() == "true":
        print(*args, **kwargs)

def load_config():
    # Determine the platform
    platform = os.name  # posix, nt, java, etc.
    config_app_name = "shell-ai"
    
    # Default configuration values
    default_config = {
        "OPENAI_MODEL": "gpt-3.5-turbo",
        "SHAI_SUGGESTION_COUNT": "3",
        "SHAI_API_PROVIDER": "groq",
        "GROQ_MODEL": "llama-3.3-70b-versatile",
        "SHAI_TEMPERATURE": "0.05"
    }
    
    try:
        # Determine the path to the configuration file based on the platform
        if platform == 'posix':
            config_path = os.path.expanduser(f'~/.config/{config_app_name}/config.json')
        elif platform == 'nt':
            config_path = os.path.join(os.environ['APPDATA'], config_app_name, 'config.json')
        else:
            raise Exception('Unsupported platform')

        debug_print(f"Looking for config file at: {config_path}")
        
        # Read the configuration file
        with open(config_path, 'r') as f:
            config = json.load(f)
            debug_print("Found and loaded config file successfully")
            
        # Merge with defaults, keeping user settings where they exist
        return {**default_config, **config}
    except FileNotFoundError:
        debug_print("No config file found, using default configuration")
        return default_config
    except json.JSONDecodeError:
        debug_print("Config file exists but contains invalid JSON, using default configuration")
        return default_config
    except Exception as e:
        debug_print(f"Unexpected error loading config: {str(e)}, using default configuration")
        return default_config
