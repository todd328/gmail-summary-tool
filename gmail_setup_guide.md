# Gmail API Authentication Setup Guide

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click on "New Project"
4. Enter a name for your project (e.g., "Gmail Summary Tool")
5. Click "Create"
6. Wait for the project to be created and then select it from the dropdown

## Step 2: Enable the Gmail API

1. In your new project, go to the navigation menu (☰) and select "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click on "Gmail API" in the results
4. Click "Enable"

## Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Select "External" as the user type (unless you have a Google Workspace account)
3. Click "Create"
4. Fill in the required information:
   - App name: "Gmail Summary Tool"
   - User support email: Your email address
   - Developer contact information: Your email address
5. Click "Save and Continue"
6. On the Scopes page, click "Add or Remove Scopes"
7. Add the scope: `https://www.googleapis.com/auth/gmail.readonly`
8. Click "Save and Continue"
9. Add your email address as a test user
10. Click "Save and Continue"
11. Review your settings and click "Back to Dashboard"

## Step 4: Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Desktop app" as the application type
4. Name your OAuth client (e.g., "Gmail Summary Client")
5. Click "Create"
6. Download the JSON file by clicking the download button
7. Rename the downloaded file to `credentials.json`

## Step 5: Prepare for the Next Steps

1. Keep the `credentials.json` file safe - you'll need it for the authentication process
2. In the next steps, we'll use this file to authenticate and access your Gmail data