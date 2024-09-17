# solo_server/commands/init.py

import os
import shutil
from solo_server import utils

def handle_command(args):
    print("Welcome to Solo Server Project Initialization!")
    project_name = input("Enter your project name (default: my_project): ") or "my_project"

    # Check if the directory exists
    if os.path.exists(project_name):
        overwrite = input(f"Directory '{project_name}' already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Project initialization canceled.")
            return
        else:
            shutil.rmtree(project_name)

    # Choose template
    templates_dir = utils.get_templates_dir()
    templates = utils.get_available_templates(templates_dir)
    print("Available templates:")
    for idx, template in enumerate(templates):
        print(f"{idx + 1}. {template}")
    template_choice = input("Select a template by number (default: 1): ") or "1"
    template_idx = int(template_choice) - 1
    template_name = templates[template_idx]

    # Copy template
    template_dir = os.path.join(templates_dir, template_name)
    shutil.copytree(template_dir, project_name)

    print(f"Project '{project_name}' initialized with template '{template_name}'.")
