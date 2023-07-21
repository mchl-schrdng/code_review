import os
import subprocess
import openai

openai.api_key = os.environ.get('CHATGPT_API_KEY')

def get_code_diff():
    """Retrieve the code difference for the latest commit."""
    diff_command = ["git", "diff", "HEAD~1"]
    return subprocess.check_output(diff_command).decode('utf-8')

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
    diff = get_code_diff()
    commit_message = generate_commit_message(diff)
    print(f"::set-output name=message::{commit_message}")
