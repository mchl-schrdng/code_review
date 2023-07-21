import os
import openai
import subprocess

# Setup OpenAI SDK
openai.api_key = os.environ["OPENAI_API_KEY"]

def get_code_diff():
    try:
        # Get the diff for the last commit only
        result = subprocess.run(["git", "diff", "HEAD^", "--name-only"], capture_output=True, check=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError:
        # This could be the first commit, or there's an issue accessing the parent commit.
        return "First commit or no previous reference found."

def get_commit_message(diff):
    response = openai.Completion.create(
      engine="davinci",
      prompt=f"Explain the following code changes succinctly: {diff}",
      max_tokens=50
    )
    return response.choices[0].text.strip()

def main():
    diff = get_code_diff()
    commit_message = get_commit_message(diff)
    print(commit_message)  # This will print the commit message to standard output
    # Amend the latest commit with the generated message
    subprocess.run(["git", "commit", "--amend", "-m", commit_message], check=True)

if __name__ == "__main__":
    main()
