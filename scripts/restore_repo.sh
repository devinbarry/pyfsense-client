#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to echo in color
echo_color() {
    local color=$1
    shift
    echo -e "\033[${color}m$@\033[0m"
}

# Get the original repo name
if [ $# -eq 0 ]; then
    original_repo_name=$(basename "$PWD")
else
    original_repo_name=$1
fi

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo_color "31" "Error: Not in a git repository. Please run this script from the root of your git repository."
    exit 1
fi

# Move to parent directory
cd ..

# Find the most recent backup
backup_dir=$(ls -d *_backup_* 2>/dev/null | sort -r | head -n 1)

if [ -z "$backup_dir" ]; then
    echo_color "31" "Error: No backup directory found."
    exit 1
fi

echo_color "32" "Found latest backup dir: $backup_dir"
echo_color "33" "Replacing $original_repo_name with backup"

# Remove the current repo and replace with backup
rm -rf "$original_repo_name"
mv "$backup_dir" "$original_repo_name"

# Enter the restored repository
cd "$original_repo_name"

echo_color "32" "Repository restored successfully."
echo_color "36" "Current directory: $(pwd)"
echo_color "36" "Git status:"
git status

echo_color "36" "Recent git log:"
git log -n 5 --oneline
