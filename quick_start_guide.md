# Gmail Summary Tool - Quick Start Guide

This guide provides step-by-step instructions to get the Gmail Summary Tool up and running quickly.

## Installation Steps

### Step 1: Install Required Python Packages

```bash
pip install -r requirements.txt
```

This will install all the necessary dependencies including:
- Google API client libraries
- Data processing libraries (pandas, numpy)
- Natural language processing tools (nltk)
- Visualization and reporting tools

### Step 2: Set Up Google Cloud Project

Follow these steps to create a Google Cloud Project and enable the Gmail API:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project named "Gmail Summary Tool"
3. Enable the Gmail API for your project
4. Configure the OAuth consent screen
   - Set the app name to "Gmail Summary Tool"
   - Add your email as a test user
5. Create OAuth credentials for a desktop application
6. Download the credentials file as `credentials.json`

Detailed instructions are available in the `gmail_setup_guide.md` file.

### Step 3: Place Credentials File

Place the downloaded `credentials.json` file in the same directory as the `gmail_summary.py` script.

## Running the Tool

### First Run

```bash
python gmail_summary.py
```

On the first run:
1. A browser window will open asking you to sign in to your Google account
2. You'll be asked to grant permission for the app to access your Gmail
3. After granting permission, the authentication token will be saved locally for future use

### Using the Tool

When you run the tool, you'll be prompted to specify how many recent emails you want to analyze (default is 100).

The tool will then:
1. Retrieve the specified number of emails from your Gmail inbox
2. Analyze and categorize them
3. Generate summaries of email content
4. Create a comprehensive report

### Viewing the Results

The tool generates a report file named `gmail_summary_report.md` that contains:
- Statistics about your email usage
- High-priority emails that need attention
- Recent emails with summaries
- Categorized emails (work, personal, financial, etc.)
- Recommendations for email management

You can open this file with any Markdown viewer or text editor.

## Privacy Note

- The tool runs entirely on your local machine
- Your email data never leaves your computer
- Authentication is handled securely through Google's OAuth2
- The application only has read-only access to your Gmail