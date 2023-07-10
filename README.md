# Code Review with OpenAI

This repository contains code that enables you to perform code reviews using OpenAI's language model. The code utilizes the OpenAI API, along with the GitHub Actions workflow, to automate the process of reviewing code changes in pull requests.

## Prerequisites

Before using this code, make sure you have the following:

- OpenAI API key: You need an API key to interact with OpenAI's language model. If you don't have one, sign up for OpenAI and obtain your API key.
- GitHub repository: You should have a GitHub repository where you want to enable code reviews. Ensure that you have the necessary permissions to add workflows and access pull requests.

## Setup

Follow these steps to set up code review with OpenAI:

1. Clone the repository: Clone the repository to your local machine or navigate to the existing repository where you want to add code review functionality.

2. Configure API key: Set up the OpenAI API key by assigning it to the `OPENAI_API_KEY` environment variable. You can do this by adding the following line to your environment variables or secrets:


3. Configure GitHub token: To enable the workflow to access your GitHub repository, you need to set up a GitHub token and assign it to the `GITHUB_TOKEN` environment variable or secret. Ensure the token has the necessary permissions to access pull requests and post comments.

4. Install dependencies: Ensure you have Python 3.9 installed. In the root directory of the repository, run the following command to install the required dependencies:

## Usage

To use the code review functionality, follow these steps:

1. Create a workflow file: In your repository, navigate to the `.github/workflows/` directory and create a new file called `code_review.yml`. Copy and paste the provided YAML code into this file.

2. Configure workflow triggers: By default, the workflow triggers on every pull request event. If you want to customize the triggering conditions, modify the `on` section in the `code_review.yml` file.

3. Run the review: Whenever a pull request is opened or updated, the workflow will automatically execute. It will clone the repository, install the dependencies, and run the `code_review.py` script. The script performs the following steps:

- Fetches the changed files from the pull request.
- Sends the files to OpenAI for review.
- Posts the review as a comment on the pull request.

4. View the review: After the workflow completes, you can visit the pull request on GitHub to see the code review posted as a comment. The review includes recommendations for enhancement, identification of problematic code snippets, highlighting of potential issues, and an overall evaluation of the code.

## Customization

You can customize the behavior of the code review process by modifying the `code_review.py` file. Here are a few possible modifications:

- Adjusting the token limit: The `TOKEN_LIMIT` variable sets the maximum token limit for the language model. You can modify this value according to your requirements.

- Modifying the review prompt: The initial user message to OpenAI can be customized by modifying the `content` field in the `messages` list.

- Adding error handling: You can enhance the error handling logic in the code to handle specific scenarios or exceptions more effectively.

- Extending the review process: If you want to perform additional actions based on the review, you can modify the `post_comment` function or add new functions as needed.

## Warning

While leveraging the power of the ChatGPT API and external services like OpenAI can be incredibly beneficial, it's crucial to exercise caution when dealing with sensitive code. The ChatGPT model processes data externally, which means the code you submit for review is shared with the OpenAI infrastructure. It's essential to ensure that the code being reviewed does not contain any sensitive information that you are not comfortable sharing with an external company.

## Conclusion

With this code and workflow configuration, you can automate code reviews using OpenAI's language model. The system will generate reviews for pull requests, helping to identify problematic code, highlight potential issues, and evaluate the overall quality of the code. Customize the code and workflow to suit your specific needs and improve your code review process.

