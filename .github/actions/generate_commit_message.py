import os
import openai
import subprocess

def get_code_diff():
    """
    Get the difference in code for the most recent commit.

    Returns:
        str: Description of the diff or 'init commit' for the first commit.
    """
    commit_count = int(subprocess.getoutput("git rev-list --count HEAD"))
    
    if commit_count == 1:
        return "init commit"

    # Return the list of changed files for the latest commit
    return subprocess.getoutput("git diff HEAD^ --name-only")

def get_commit_message(diff):
    """
    Get the commit message using OpenAI for the provided code difference.

    Args:
        diff (str): Description of code difference.

    Returns:
        str: Generated commit message.
    """
    if diff == "init commit":
        return diff

    prompt = f"Describe these code changes in one sentence: {diff}"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=15  # Limit to 15 tokens for brevity
    )
    
    return response.choices[0].text.strip()

def main():
    """Main function to generate and amend the commit message."""
    diff = get_code_diff()
    commit_message = get_commit_message(diff)
    subprocess.run(["git", "commit", "--amend", "-m", commit_message], check=True)

if __name__ == "__main__":
    main()
