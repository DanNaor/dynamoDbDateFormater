#!/bin/bash

# Script to set up AWS credentials, create a virtual environment,
# install dependencies, and run Python script to update DynamoDB table to the correct format
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <AWS_ACCESS_KEY_ID> <AWS_SECRET_ACCESS_KEY> <AWS_SESSION_TOKEN> <TABLE_NAME>"
    exit 1
fi
# AWS credentials setup
export AWS_ACCESS_KEY_ID="$1"
export AWS_SECRET_ACCESS_KEY="$2"
export AWS_SESSION_TOKEN="$3"


# Define variables
VENV_DIR="venv"
PYTHON="python3"
SCRIPT="dateFormaterScript.py"
TABLE_NAME="$4"  

# Ensure virtual environment is activated or created
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Install dependencies
pip install boto3

# Run the Python script with the table name argument
$PYTHON $SCRIPT "$TABLE_NAME"

# Deactivate virtual environment
deactivate
