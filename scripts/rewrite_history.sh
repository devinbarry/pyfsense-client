#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Set default dry-run mode to false
DRY_RUN=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --old-commit) OLD_COMMIT="$2"; shift ;;
        --new-commit) NEW_COMMIT="$2"; shift ;;
        --file) TARGET_FILE="$2"; shift ;;
        --dry-run) DRY_RUN=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Ensure necessary parameters are provided
if [ -z "$OLD_COMMIT" ] || [ -z "$NEW_COMMIT" ] || [ -z "$TARGET_FILE" ]; then
    echo "Error: --old-commit, --new-commit, and --file parameters are required."
    exit 1
fi

# Check if git filter-repo is installed
if ! command -v git filter-repo &> /dev/null; then
    echo "Error: git-filter-repo is not installed. Please install it and try again."
    echo "You can install it via pip: pip install git-filter-repo"
    exit 1
fi

# Function to create a backup of the repository
create_backup() {
    local backup_dir="../$(basename $(pwd))_backup_$(date +%Y%m%d_%H%M%S)"
    echo "Creating a backup of the repository at $backup_dir"
    cp -R . "$backup_dir"
    echo "Backup created successfully."
}

# Function to create replacement expression
create_replacement_expression() {
    if ! python3 scripts/create_replacement.py "$OLD_COMMIT" "$NEW_COMMIT" "$TARGET_FILE"; then
        echo "Error: Failed to create replacement expression."
        exit 1
    fi
}

# Main rewrite function
rewrite_history() {
    create_replacement_expression

    if [ -f "replacements.txt" ]; then
        if ! git filter-repo --force --replace-text replacements.txt; then
            echo "Error: git filter-repo failed. Please check the replacements.txt file and try again."
            exit 1
        fi
        rm replacements.txt
    else
        echo "Error: replacements.txt file not found."
        exit 1
    fi
}

# Dry run function
dry_run() {
    create_replacement_expression
    echo "Dry run mode. The following replacement would be made:"
    cat replacements.txt
    rm replacements.txt
}

# Confirm action
confirm_action() {
    read -p "This action will rewrite your Git history. Are you sure you want to proceed? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled."
        exit 1
    fi
}

# Main execution
if [ "$DRY_RUN" = true ]; then
    dry_run
else
    confirm_action
    create_backup
    rewrite_history

    echo "History has been rewritten. Please review the changes."
    echo "To push the changes, use: git push --force-with-lease"
    echo "Warning: Force pushing can overwrite remote changes. Use with caution."
fi

echo "Operation completed."
