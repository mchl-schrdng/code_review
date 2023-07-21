import os
import openai
import subprocess

# Setup OpenAI SDK
openai.api_key = os.environ["OPENAI_API_KEY"]

def get_code_diff():
    # Check if there are at least two commits in the repo
    commit_count = subprocess.run(["git", "rev-list", "--count", "HEAD"], capture_output=True, check=True, text=True).stdout.strip()
    if int(commit_count) < 2:
        # If it's the first commit, just return a string indicating this
        return "First commit to the repository."
    
    # If there are prior commits, get the diff
    subprocess.run(["git", "checkout", "HEAD^1"], check=True)
    result = subprocess.run(["git", "diff", "--name-only", "HEAD.."], capture_output=True, check=True, text=True)
    return result.stdout

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
