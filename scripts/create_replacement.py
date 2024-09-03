import subprocess
import re
import sys

def escape_for_regex(text):
    """
    Escape special characters for use in a regex pattern.
    This is a more thorough escaping than re.escape() to handle multiline content.
    """
    return re.sub(r'([\\.*+?^${}()|[\]])', r'\\\1', text)

def create_replacement_expression(old_commit, new_commit, target_file):
    """
    Create a single replacement expression based on the content of a file in two different commits.

    :param old_commit: Hash of the old commit
    :param new_commit: Hash of the new commit
    :param target_file: Path of the file to examine
    :return: A tuple (old_content, new_content) for replacement
    """
    # Get the content of the file in the old commit
    old_content = subprocess.check_output(f"git show {old_commit}:{target_file}", shell=True, text=True)

    # Get the content of the file in the new commit
    new_content = subprocess.check_output(f"git show {new_commit}:{target_file}", shell=True, text=True)

    return old_content.strip(), new_content.strip()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 create_replacement.py <old_commit> <new_commit> <target_file>")
        sys.exit(1)

    old_commit = sys.argv[1]
    new_commit = sys.argv[2]
    target_file = sys.argv[3]

    old_content, new_content = create_replacement_expression(old_commit, new_commit, target_file)

    # Escape special regex characters in old_content
    escaped_old_content = escape_for_regex(old_content)

    with open("replacements.txt", "w") as f:
        f.write(f"regex:(?s){escaped_old_content}==>{new_content}\n")

    print(f"Replacement expression written to replacements.txt")
