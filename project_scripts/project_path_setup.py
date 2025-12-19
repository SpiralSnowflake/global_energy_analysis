#script to handle relative paths so scripts and notebooks can find modules data
"""
project_path_setup.py

Sets up relative paths for the project so scripts and notebooks can use them.
"""

import sys
from pathlib import Path

# Define project root relative to this file
project_root = Path(__file__).parent.parent.resolve()

# Add project_scripts to sys.path for easy imports
project_scripts = project_root / "project_scripts"
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(project_scripts) not in sys.path:
    sys.path.insert(0, str(project_scripts))

print("Project paths set up successfully!")
print("project_root:", project_root)
print("project_scripts:", project_scripts)
