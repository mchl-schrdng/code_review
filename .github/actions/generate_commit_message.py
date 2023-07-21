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
        str: Generated commit message with an emoticon prefix and a body.
    """
    if diff == "init commit":
        return diff

    # Constructing a prompt to guide the model
    context = ("You are an AI code reviewer. Generate a commit message with a title and a body. "
               "The title should start with an appropriate emoticon: \n\n"
               "✨ for new features\n"
               "🐛 for bug fixes\n"
               "📚 for documentation updates\n"
               "🚀 for performance improvements\n"
               "🧹 for cleaning up code\n"
               "⚙️ for configuration changes\n\n"
               "Start with 'Title:' for the title and 'Body:' for the detailed description. Here are the code changes:")

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
                "content": f"{diff}"
            }
        ]
    )
    
    # Extracting the assistant's message from the response and parsing it
    message_from_assistant = response.choices[0].message['content']
    
    # Extract the title and body from the model's response
    title = message_from_assistant.split('Title:')[1].split('Body:')[0].strip()
    body = message_from_assistant.split('Body:')[1].strip()
    
    return title, body

def main():
    """Main function to generate and amend the commit message."""
    diff = get_code_diff()
    title, body = get_commit_message(diff)
    subprocess.run(["git", "commit", "--amend", "-m", title, "-m", body], check=True)

if __name__ == "__main__":
    main()
