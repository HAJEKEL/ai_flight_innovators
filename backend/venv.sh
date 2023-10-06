#!/bin/bash

# Get the absolute path to the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if the 'venv' directory exists in the same directory as this script
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "Activating virtual environment in $SCRIPT_DIR/venv"
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Error: Virtual environment 'venv' not found in the same directory as this script."
    exit 1
fi

