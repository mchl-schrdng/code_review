import os
import openai
from github import Github
import git
import json

# Set the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to read the content of a file
def get_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to fetch the files changed in a pull request
def get_changed_files(pr):
    # Clone the repository and checkout the PR branch
    repo = git.Repo.clone_from(pr.base.repo.clone_url, to_path='./repo', branch=pr.head.ref)

    # Get the difference between the PR branch and the base branch
    base_ref = f"origin/{pr.base.ref}"
    head_ref = f"origin/{pr.head.ref}"
    diffs = repo.git.diff(base_ref, head_ref, name_only=True).split('\n')

    # Initialize an empty dictionary to store file contents
    files = {}
    for file_path in diffs:
        try:
            # Fetch each file's content and store it in the files dictionary
            files[file_path] = get_file_content('./repo/' + file_path)
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")

    return files

# Function to send the changed files to OpenAI for review
def send_to_openai(files):
    # Concatenate all the files into a single string
    code = '\n'.join(files.values())

    # Send a message to OpenAI with the code for review
    message = openai.ChatCompletion.create(
        model="gpt-4", # use the latest GPT model available
        messages=[
            {
                "role": "user", 
                "content": "You are acting as a code reviewer. Your task is to review the following code and provide suggestions for improvement, point out potential issues, and evaluate the overall following code quality:\n" + code"
            }
        ],
    )

    # Return the OpenAI's assistant's reply
    return message['choices'][0]['message']['content']

# Function to post a comment on the pull request with the review
def post_comment(pr, comment):
    # Post the OpenAI's response as a comment on the PR
    pr.create_issue_comment(comment)

# Main function to orchestrate the above operations
def main():
    # Get the pull request event JSON
    with open(os.getenv('GITHUB_EVENT_PATH')) as json_file:
        event = json.load(json_file)
    
    # Instantiate the Github object using the Github token
    # and get the pull request object
    pr = Github(os.getenv('GITHUB_TOKEN')).get_repo(event['repository']['full_name']).get_pull(event['number'])

    # Get the changed files in the pull request
    files = get_changed_files(pr)

    # Send the files to OpenAI for review
    review = send_to_openai(files)

    # Post the review as a comment on the pull request
    post_comment(pr, review)

if __name__ == "__main__":
    main()  # Execute the main function
