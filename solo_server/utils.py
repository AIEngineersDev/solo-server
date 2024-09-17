# solo_server/utils.py

import os

def get_templates_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(current_dir, 'templates')
    return templates_dir

def get_available_templates(templates_dir):
    templates = [name for name in os.listdir(templates_dir)
                 if os.path.isdir(os.path.join(templates_dir, name))]
    return templates
