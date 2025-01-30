import os
import configparser

CONFIG_FILE = os.path.expanduser("~/.solo/solo.conf")

def load_config():
    """Loads configuration from solo.conf."""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config
    return None

def get_config_value(key, default=None):
    """Retrieves a specific configuration value."""
    config = load_config()
    return config["DEFAULT"].get(key, default) if config else default

def save_config(config):
    """Saves configuration to solo.conf."""
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
