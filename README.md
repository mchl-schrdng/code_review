def main():
    """
    The main function orchestrates the operations of:
    1. Fetching changed files from a PR
    2. Sending those files to OpenAI for review
    3. Posting the review as a comment on the PR
    """
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
