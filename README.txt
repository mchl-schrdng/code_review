def get_changed_files(pr):
    """
    This function fetches the files that were changed in a pull request.

    Args:
        pr (PullRequest): The pull request object.

    Returns:
        dict: A dictionary containing the file paths as keys and their content as values.
    """
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
