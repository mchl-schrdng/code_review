import os
import openai
import git

openai.api_key = os.environ.get('OPENAI_API_KEY')

def get_diffs_for_file(repo, base_ref, head_ref, file_path):
    """Gets the git diff for a specific file between two references."""
    return repo.git.diff(base_ref, head_ref, file_path)

def get_changed_files_diffs():
    """Fetch the diffs of files that were changed in the latest commit."""
    repo = git.Repo('./')  # Assumes the current directory is the repository

    # Get the difference between the latest commit and its parent
    base_ref = "HEAD^"
    head_ref = "HEAD"
    
    changed_files = repo.git.diff(base_ref, head_ref, name_only=True).split('\n')

    diffs = {}
    for file_path in changed_files:
        diffs[file_path] = get_diffs_for_file(repo, base_ref, head_ref, file_path)

    # Combine all diffs into a single string
    all_diffs = "\n".join(diffs.values())
    return all_diffs

def infer_emoji_from_message(message):
    """Infer an appropriate emoji based on the content of the commit message."""
    lower_message = message.lower()
    if "fix" in lower_message:
        return "🔧"  # Wrench for fixes
    elif "update" in lower_message:
        return "🔄"  # Arrows for updates
    elif "delete" in lower_message or "remove" in lower_message:
        return "❌"  # Cross mark for deletions
    else:
        return "✨"  # Sparkles for general enhancements

def generate_commit_message(chunk):
    """Generate a concise commit message based on the given code changes."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI designed to generate concise and informative commit messages based on provided code changes."
            },
            {
                "role": "user",
                "content": f"Given the code changes, provide a concise and descriptive commit message:\n{chunk}"
            }
        ],
    )
    
    # Extract the content of the assistant's message from the response
    message = response['choices'][0]['message']['content']
    emoji = infer_emoji_from_message(message)
    
    # Truncate the message if it's too long (e.g., limit to 50 characters)
    max_length = 50
    if len(message) > max_length:
        message = message[:max_length - 3] + "..."
    
    return f"{emoji} {message}"

if __name__ == "__main__":
    diff = get_changed_files_diffs()
    commit_message = generate_commit_message(diff)
    print(f"::set-output name=message::{commit_message}")
