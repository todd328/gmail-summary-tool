# Uploading the Gmail Summary Tool to GitHub

This guide will walk you through the process of uploading the Gmail Summary Tool to your GitHub account.

## Prerequisites

1. A GitHub account (create one at [github.com](https://github.com) if you don't have one)
2. Git installed on your computer (download from [git-scm.com](https://git-scm.com/downloads))
3. Basic familiarity with command line operations

## Step 1: Create a New Repository on GitHub

1. Log in to your GitHub account
2. Click the "+" icon in the top-right corner and select "New repository"
3. Name your repository (e.g., "gmail-summary-tool")
4. Add a description (optional): "A tool to summarize and analyze Gmail emails"
5. Choose "Public" or "Private" visibility (Private is recommended for personal tools)
6. Do NOT initialize the repository with a README, .gitignore, or license (we'll add these later)
7. Click "Create repository"

## Step 2: Prepare Your Local Files

Before uploading to GitHub, let's make sure we don't include any sensitive information:

1. Create a .gitignore file to exclude sensitive files:

```bash
# Create a .gitignore file
echo "credentials.json
token.pickle
__pycache__/
*.pyc
gmail_summary_report.md" > .gitignore
```

2. Make sure you don't have any credentials.json or token.pickle files in your directory

## Step 3: Initialize Git Repository Locally

Navigate to the directory containing your Gmail Summary Tool files and run:

```bash
# Initialize a new Git repository
git init

# Add all files to the repository (except those in .gitignore)
git add .

# Commit the files
git commit -m "Initial commit of Gmail Summary Tool"
```

## Step 4: Connect to GitHub and Push Files

Now, connect your local repository to GitHub and upload your files:

```bash
# Add the GitHub repository as a remote
git remote add origin https://github.com/YOUR_USERNAME/gmail-summary-tool.git

# Push your files to GitHub
git push -u origin master
```

Replace `YOUR_USERNAME` with your actual GitHub username.

If you're using a newer version of Git, you might need to use `main` instead of `master`:

```bash
git push -u origin main
```

## Step 5: Verify the Upload

1. Go to your GitHub repository page (https://github.com/YOUR_USERNAME/gmail-summary-tool)
2. You should see all your files uploaded and displayed in the repository

## Security Considerations

1. **NEVER upload credentials.json or token.pickle to GitHub**
   - These files contain sensitive authentication information
   - The .gitignore file should prevent this, but double-check

2. **Consider adding a note about security in your README.md**
   - Remind users to keep their credentials secure
   - Explain that each user needs to create their own credentials.json file

## Making Changes

After your initial upload, you can make changes to your files locally and then:

```bash
# Add changed files
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Cloning to Another Computer

To download your tool on another computer:

```bash
git clone https://github.com/YOUR_USERNAME/gmail-summary-tool.git
cd gmail-summary-tool
pip install -r requirements.txt
```

Remember that you'll need to set up credentials.json on each new computer.