name: Generate Commit Message

on:
  push:
    branches:
      - main

jobs:
  generate-message:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        with:
          fetch-depth: 0  # Fetches all commits (needed to access prior commits)

      - name: Set Git identity
        run: |
          git config user.email "action@github.com"
          git config user.name "GitHub Action"

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install OpenAI SDK
        run: pip install openai

      - name: Run script to generate commit message
        run: python .github/actions/generate_commit_message.py
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
