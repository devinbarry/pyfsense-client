#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Set default dry-run mode to false
DRY_RUN=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --old-commit) OLD_COMMIT_HASH="$2"; shift ;;
        --new-commit) NEW_COMMIT_HASH="$2"; shift ;;
        --file) TARGET_FILE_PATH="$2"; shift ;;
        --dry-run) DRY_RUN=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Ensure necessary parameters are provided
if [ -z "$OLD_COMMIT_HASH" ] || [ -z "$NEW_COMMIT_HASH" ] || [ -z "$TARGET_FILE_PATH" ]; then
    echo "Error: --old-commit, --new-commit, and --file parameters are required."
    exit 1
fi

# Function to create a backup of the repository
create_backup() {
    local backup_dir="../$(basename "$(pwd)")_backup_$(date +%Y%m%d_%H%M%S)"
    echo "Creating a backup of the repository at $backup_dir"
    cp -R . "$backup_dir"
    echo "Backup created successfully."
}

# Function to get the new content of the file
get_new_file_content() {
    git show "$NEW_COMMIT_HASH:$TARGET_FILE_PATH"
}

# Main rewrite function
rewrite_history() {
    local new_content
    new_content=$(get_new_file_content)

    # Encode the new content to avoid issues with special characters
    # Use printf to ensure newlines are preserved
    local encoded_content
    encoded_content=$(printf '%s' "$new_content" | base64 | tr -d '\n')

    # Use git filter-branch to rewrite history
    git filter-branch --force --index-filter '
        git ls-files -z | while IFS= read -r -d "" path; do
            if [ "$path" = "'"$TARGET_FILE_PATH"'" ]; then
                content=$(echo "'"$encoded_content"'" | base64 -d)
                blob_id=$(printf "%s" "$content" | git hash-object -w --stdin)
                mode=$(git ls-files -s "$path" | cut -d " " -f 1)
                printf "%s %s\t%s\0" "$mode" "$blob_id" "$path"
            else
                git ls-files -s -z "$path"
            fi
        done | git update-index --index-info
    ' --tag-name-filter cat -- --all
}

# Dry run function
dry_run() {
    local new_content
    new_content=$(get_new_file_content)
    echo "Dry run mode. The following content would replace $TARGET_FILE_PATH in all commits:"
    echo "----------------------------------------"
    echo "$new_content"
    echo "----------------------------------------"
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
