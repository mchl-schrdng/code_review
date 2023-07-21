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

        # Constructing a prompt to guide the model in choosing the right emoticon
    context = ("You are an AI code reviewer. Your task is to understand the nature of "
               "the code changes and provide a concise commit message. Use emoticons to "
               "add context: \n\n"
               "✨ for new features\n"
               "🐛 for bug fixes\n"
               "📚 for documentation updates\n"
               "🚀 for performance improvements\n"
               "🧹 for cleaning up code\n"
               "⚙️ for configuration changes\n\n"
               "Based on the following code changes, what would be the appropriate commit message?")

    # Using the ChatCompletion interface to interact with gpt-3.5-turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": f"Code changes: {diff}"
            }
        ]
    )
    
    # Extracting the assistant's message from the response
    message_from_assistant = response.choices[0].message['content']
    
    return message_from_assistant.strip()

def main():
    """Main function to generate and amend the commit message."""
    diff = get_code_diff()
    commit_message = get_commit_message(diff)
    subprocess.run(["git", "commit", "--amend", "-m", commit_message], check=True)

if __name__ == "__main__":
    main()
