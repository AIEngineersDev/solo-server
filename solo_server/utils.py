# solo_server/utils.py

import os
import sys

def get_templates_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(current_dir, 'templates')
    if not os.path.exists(templates_dir):
        try:
            os.makedirs(templates_dir)
            print(f"Created templates directory at {templates_dir}", file=sys.stderr)
        except OSError as e:
            print(f"Error creating templates directory: {e}", file=sys.stderr)
            return None
    return templates_dir

def get_available_templates(templates_dir):
    if templates_dir is None or not os.path.exists(templates_dir):
        return []
    templates = [name for name in os.listdir(templates_dir)
                 if os.path.isdir(os.path.join(templates_dir, name))]
    return templates
