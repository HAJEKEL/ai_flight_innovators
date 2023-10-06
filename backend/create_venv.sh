#!/bin/bash

# Get the absolute path to the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if the 'venv' directory already exists in the current directory
if [ -d "venv" ]; then
    echo "Virtual environment 'venv' already exists in the current directory."
else
    # Create a virtual environment
    python3 -m venv venv
    echo "Virtual environment 'venv' created in the current directory."

    # Activate the virtual environment
    source "venv/bin/activate"

    # Install packages from requirements.txt in the child directory
    CHILD_DIR="child_directory"
    cd "$CHILD_DIR"
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        echo "Packages installed from requirements.txt in the child directory."
    else
        echo "Error: 'requirements.txt' not found in the child directory."
        exit 1
    fi
fi

