# Gmail Summary Tool

This tool connects to your Gmail account using the Gmail API and generates a comprehensive summary of your emails. It categorizes emails by importance, sender domain, and content type, and provides summaries of email content.

## Features

- Secure authentication using OAuth2 (no password sharing)
- Retrieves and analyzes your recent emails
- Categorizes emails by sender, importance, and content
- Generates summaries of email content using NLP
- Creates a comprehensive report with statistics and recommendations
- Identifies high-priority emails that need attention
- Suggests potential spam/promotional emails to unsubscribe from

## Setup Instructions

### 1. Set Up Google Cloud Project and Enable Gmail API

Follow the detailed instructions in the `gmail_setup_guide.md` file to:
- Create a Google Cloud Project
- Enable the Gmail API
- Configure the OAuth consent screen
- Create OAuth credentials
- Download the credentials.json file

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Run the Tool

```bash
python gmail_summary.py
```

The first time you run the tool, it will open a browser window asking you to authorize the application to access your Gmail. After authorization, the tool will:

1. Retrieve your recent emails (you can specify how many)
2. Analyze and categorize them
3. Generate summaries of email content
4. Create a comprehensive report saved as `gmail_summary_report.md`

## Understanding the Report

The generated report includes:
- Overall statistics about your emails
- Breakdown of email sources (domains)
- High-priority emails that need attention
- Recent emails with summaries
- Emails categorized by type (work, personal, financial, etc.)
- Recommendations for email management

## Privacy and Security

- This tool runs locally on your machine
- Your email data never leaves your computer
- Authentication is handled securely through Google's OAuth2
- The tool only requests read-only access to your Gmail
- No data is stored or transmitted to any third parties

## Troubleshooting

If you encounter any issues:

1. Ensure you've completed all steps in the `gmail_setup_guide.md`
2. Verify that the `credentials.json` file is in the same directory as the script
3. Check that all required packages are installed
4. If authentication fails, delete the `token.pickle` file (if it exists) and try again