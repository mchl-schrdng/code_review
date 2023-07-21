import os
import openai
import subprocess

# Setup OpenAI SDK
openai.api_key = os.environ["OPENAI_API_KEY"]

def get_code_diff():
    commit_count = int(subprocess.getoutput("git rev-list --count HEAD"))
    if commit_count == 1:
        return "init commit"
    
    # Get the diff for the latest commit
    result = subprocess.getoutput("git diff HEAD^ --name-only")
    return result

def get_commit_message(diff):
    if diff == "init commit":
        return diff
    
    prompt = f"Describe these code changes in one sentence: {diff}"
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      max_tokens=15  # Limiting the length of the response to around 100 characters
    )
    return response.choices[0].text.strip()

def main():
    diff = get_code_diff()
    commit_message = get_commit_message(diff)
    subprocess.run(["git", "commit", "--amend", "-m", commit_message], check=True)

if __name__ == "__main__":
    main()
