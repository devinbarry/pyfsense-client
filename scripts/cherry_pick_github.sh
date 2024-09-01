#!/bin/bash

# Function to print usage information
print_usage() {
    echo "Usage: $0 [-d|--dry-run] <source_branch>"
    echo "  -d, --dry-run    Perform a dry run without actually cherry-picking"
    exit 1
}

# Parse command line arguments
dry_run=false
source_branch=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dry-run)
            dry_run=true
            shift
            ;;
        *)
            if [[ -z "$source_branch" ]]; then
                source_branch=$1
            else
                print_usage
            fi
            shift
            ;;
    esac
done

# Check if a branch name was provided
if [[ -z "$source_branch" ]]; then
    print_usage
fi

current_branch=$(git rev-parse --abbrev-ref HEAD)

# Get the common ancestor of the current branch and the source branch
common_ancestor=$(git merge-base $current_branch $source_branch)

# Get all commit hashes from dependabot in the specified branch that are not in the current branch
commit_hashes=$(git log $common_ancestor..$source_branch --author="dependabot\[bot\]" --pretty=format:"%H")

# Check if there are any commits to cherry-pick
if [[ -z "$commit_hashes" ]]; then
    echo "No new dependabot commits found in branch $source_branch"
    exit 0
fi

# Function to process commits
process_commits() {
    local action=$1
    for commit in $commit_hashes; do
        # Check if the commit already exists in the current branch
        if git branch --contains $commit | grep -q "$current_branch"; then
            echo "Commit $commit already exists in the current branch. Skipping."
        else
            commit_message=$(git log -1 --pretty=format:"%s" $commit)
            if [[ "$action" == "dry-run" ]]; then
                echo "Would cherry-pick: $commit - $commit_message"
            elif [[ "$action" == "cherry-pick" ]]; then
                if git cherry-pick $commit; then
                    echo "Successfully cherry-picked commit $commit - $commit_message"
                else
                    echo "Failed to cherry-pick commit $commit - $commit_message"
                    echo "Please resolve the conflict manually, then run:"
                    echo "git add ."
                    echo "git cherry-pick --continue"
                    echo "After resolving the conflict, rerun this script to continue with remaining commits."
                    exit 1
                fi
            fi
        fi
    done
}

# Execute based on dry-run flag
if $dry_run; then
    echo "Dry run mode. The following commits would be cherry-picked:"
    process_commits "dry-run"
else
    echo "Cherry-picking commits:"
    process_commits "cherry-pick"
    echo "Cherry-picking complete. All new dependabot commits have been applied."
fi
