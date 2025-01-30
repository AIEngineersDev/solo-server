import os
import configparser
from solo.setup import interactive_setup

CONFIG_FILE = os.path.expanduser("~/.solo/solo.conf")

def test_setup():
    os.remove(CONFIG_FILE) if os.path.exists(CONFIG_FILE) else None
    interactive_setup()
    assert os.path.exists(CONFIG_FILE)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    assert "DEFAULT" in config

if __name__ == "__main__":
    test_setup()
