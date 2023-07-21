import os
import openai
import subprocess

# Setup OpenAI SDK
openai.api_key = os.environ["OPENAI_API_KEY"]

def get_code_diff():
    # Checkout the previous commit
    subprocess.run(["git", "checkout", "HEAD^1"], check=True)
    # Get the diff
    result = subprocess.run(["git", "diff", "--name-only", "HEAD.."], capture_output=True, check=True, text=True)
    return result.stdout

def get_commit_message(diff):
    response = openai.Completion.create(
      engine="davinci",
      prompt=f"Explain the following code changes: {diff}",
      max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    diff = get_code_diff()
    commit_message = get_commit_message(diff)
    # Amend the latest commit with the generated message
    subprocess.run(["git", "commit", "--amend", "-m", commit_message], check=True)

if __name__ == "__main__":
    main()
