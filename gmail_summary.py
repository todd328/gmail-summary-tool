#!/usr/bin/env python3
"""
Gmail Summary Tool - Authenticates with Gmail API and summarizes emails
"""

import os
import pickle
import base64
import re
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    """Authenticate with Gmail API using OAuth2"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_emails(service, max_results=100):
    """Retrieve emails from Gmail"""
    print(f"Retrieving up to {max_results} emails...")
    
    # Get messages from inbox
    results = service.users().messages().list(
        userId='me', 
        labelIds=['INBOX'], 
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        print("No messages found.")
        return []
    
    print(f"Found {len(messages)} messages. Fetching details...")
    
    # Get detailed information for each message
    emails = []
    for message in tqdm(messages):
        msg = service.users().messages().get(
            userId='me', 
            id=message['id'],
            format='full'
        ).execute()
        
        # Extract email details
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
        
        # Extract email body
        body = get_email_body(msg)
        
        # Add to emails list
        emails.append({
            'id': message['id'],
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': body,
            'labels': msg['labelIds']
        })
    
    return emails

def get_email_body(message):
    """Extract the body text from an email message"""
    if 'parts' in message['payload']:
        for part in message['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif 'parts' in part:
                for subpart in part['parts']:
                    if subpart['mimeType'] == 'text/plain':
                        if 'data' in subpart['body']:
                            return base64.urlsafe_b64decode(subpart['body']['data']).decode('utf-8')
    elif 'body' in message['payload'] and 'data' in message['payload']['body']:
        return base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
    
    return "No body content found"

def categorize_emails(emails):
    """Categorize emails by sender domain and importance"""
    print("Categorizing emails...")
    
    # Extract domains from sender emails
    for email in emails:
        sender = email['sender']
        domain_match = re.search(r'@([\w.-]+)', sender)
        if domain_match:
            email['domain'] = domain_match.group(1)
        else:
            email['domain'] = 'unknown'
    
    # Group by domain
    domain_groups = defaultdict(list)
    for email in emails:
        domain_groups[email['domain']].append(email)
    
    # Sort domains by count
    sorted_domains = sorted(domain_groups.items(), key=lambda x: len(x[1]), reverse=True)
    
    # Determine importance (simple heuristic)
    for email in emails:
        # Check if it's from a frequent sender
        frequent_domain = email['domain'] in [d[0] for d in sorted_domains[:5]]
        
        # Check for urgent keywords in subject
        urgent_keywords = ['urgent', 'important', 'action', 'required', 'immediately', 'asap']
        has_urgent_keywords = any(keyword in email['subject'].lower() for keyword in urgent_keywords)
        
        # Check if user is directly addressed (simple check)
        directly_addressed = 'to:' in email['body'].lower()[:100]
        
        # Assign importance score (0-5)
        importance = 0
        if 'IMPORTANT' in email.get('labels', []):
            importance += 2
        if frequent_domain:
            importance += 1
        if has_urgent_keywords:
            importance += 1
        if directly_addressed:
            importance += 1
            
        email['importance'] = min(importance, 5)  # Cap at 5
    
    return emails, sorted_domains

def summarize_text(text, num_sentences=3):
    """Generate a summary of the text using extractive summarization"""
    # Download NLTK resources if not already downloaded
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    
    # Clean and tokenize the text
    text = re.sub(r'\s+', ' ', text)
    sentences = sent_tokenize(text)
    
    # If there are fewer sentences than requested, return all sentences
    if len(sentences) <= num_sentences:
        return ' '.join(sentences)
    
    # Create similarity matrix
    stop_words = set(stopwords.words('english'))
    
    def sentence_similarity(sent1, sent2):
        words1 = [word.lower() for word in sent1.split() if word.lower() not in stop_words]
        words2 = [word.lower() for word in sent2.split() if word.lower() not in stop_words]
        
        all_words = list(set(words1 + words2))
        
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
        
        for word in words1:
            if word in all_words:
                vector1[all_words.index(word)] += 1
                
        for word in words2:
            if word in all_words:
                vector2[all_words.index(word)] += 1
                
        if sum(vector1) == 0 or sum(vector2) == 0:
            return 0.0
        
        return 1 - cosine_distance(vector1, vector2)
    
    # Create similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j])
    
    # Use PageRank algorithm to rank sentences
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    
    # Get top sentences
    ranked_sentences = sorted([(scores[i], sentences[i]) for i in range(len(sentences))], reverse=True)
    summary = ' '.join([ranked_sentences[i][1] for i in range(min(num_sentences, len(ranked_sentences)))])
    
    return summary

def generate_email_summaries(emails):
    """Generate summaries for each email"""
    print("Generating email summaries...")
    
    for email in tqdm(emails):
        if len(email['body']) > 200:  # Only summarize longer emails
            email['summary'] = summarize_text(email['body'])
        else:
            email['summary'] = email['body']
    
    return emails

def create_summary_report(emails, domain_stats):
    """Create a comprehensive summary report"""
    print("Creating summary report...")
    
    # Sort emails by date (newest first)
    try:
        emails_sorted = sorted(emails, key=lambda x: datetime.datetime.strptime(
            re.search(r'(\d{1,2}\s+\w+\s+\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2})', x['date']).group(0),
            '%d %b %Y %H:%M:%S'
        ), reverse=True)
    except:
        # Fallback if date parsing fails
        emails_sorted = emails
    
    # Group by importance
    importance_groups = defaultdict(list)
    for email in emails_sorted:
        importance_groups[email['importance']].append(email)
    
    # Create report
    report = "# Gmail Summary Report\n\n"
    report += f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Total emails analyzed: {len(emails)}\n\n"
    
    # Domain statistics
    report += "## Email Sources\n\n"
    report += "| Domain | Count | Percentage |\n"
    report += "|--------|-------|------------|\n"
    
    for domain, emails_list in domain_stats[:10]:  # Top 10 domains
        percentage = (len(emails_list) / len(emails)) * 100
        report += f"| {domain} | {len(emails_list)} | {percentage:.1f}% |\n"
    
    # Important emails
    report += "\n## High Priority Emails\n\n"
    
    high_priority = []
    for importance in range(5, 2, -1):  # 5, 4, 3
        high_priority.extend(importance_groups[importance])
    
    if high_priority:
        for email in high_priority[:10]:  # Top 10 important emails
            report += f"### {email['subject']}\n"
            report += f"**From:** {email['sender']}\n"
            report += f"**Date:** {email['date']}\n"
            report += f"**Importance:** {'★' * email['importance']}\n\n"
            report += f"{email['summary']}\n\n"
            report += "---\n\n"
    else:
        report += "No high priority emails found.\n\n"
    
    # Recent emails
    report += "## Recent Emails\n\n"
    
    for email in emails_sorted[:15]:  # 15 most recent emails
        if email not in high_priority[:10]:  # Avoid duplication
            report += f"### {email['subject']}\n"
            report += f"**From:** {email['sender']}\n"
            report += f"**Date:** {email['date']}\n"
            report += f"**Importance:** {'★' * email['importance']}\n\n"
            report += f"{email['summary']}\n\n"
            report += "---\n\n"
    
    # Email categories
    categories = {
        'Work': ['work', 'project', 'task', 'meeting', 'deadline', 'report'],
        'Personal': ['family', 'friend', 'home', 'personal'],
        'Financial': ['payment', 'invoice', 'bill', 'transaction', 'bank', 'credit'],
        'Shopping': ['order', 'delivery', 'shipped', 'tracking', 'purchase'],
        'Social': ['invitation', 'event', 'party', 'social', 'network'],
        'Newsletters': ['newsletter', 'subscribe', 'update', 'weekly', 'monthly']
    }
    
    report += "## Email Categories\n\n"
    
    for category, keywords in categories.items():
        category_emails = []
        for email in emails:
            if any(keyword in email['subject'].lower() or keyword in email['body'].lower()[:500] for keyword in keywords):
                category_emails.append(email)
        
        if category_emails:
            report += f"### {category} ({len(category_emails)})\n\n"
            for email in category_emails[:5]:  # Top 5 per category
                report += f"- **{email['subject']}** from {email['sender'].split('<')[0].strip()}\n"
            report += "\n"
    
    # Recommendations
    report += "## Recommendations\n\n"
    
    # Find potential spam or promotional emails
    potential_spam = []
    for email in emails:
        if 'SPAM' in email.get('labels', []) or 'CATEGORY_PROMOTIONS' in email.get('labels', []):
            potential_spam.append(email)
    
    if potential_spam:
        report += "### Potential Spam/Promotional Emails\n\n"
        report += "Consider unsubscribing from these senders:\n\n"
        
        spam_domains = defaultdict(int)
        for email in potential_spam:
            spam_domains[email['domain']] += 1
        
        for domain, count in sorted(spam_domains.items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"- {domain} ({count} emails)\n"
        
        report += "\n"
    
    # Identify unread important emails
    unread_important = []
    for email in emails:
        if 'UNREAD' in email.get('labels', []) and email['importance'] >= 3:
            unread_important.append(email)
    
    if unread_important:
        report += "### Unread Important Emails\n\n"
        report += "These emails appear important and are still unread:\n\n"
        
        for email in unread_important[:10]:
            report += f"- **{email['subject']}** from {email['sender'].split('<')[0].strip()}\n"
        
        report += "\n"
    
    return report

def main():
    """Main function to run the Gmail summary tool"""
    print("Gmail Summary Tool")
    print("------------------")
    
    try:
        # Authenticate with Gmail API
        print("Authenticating with Gmail API...")
        service = authenticate()
        
        # Get emails
        max_results = int(input("How many recent emails would you like to analyze? (default: 100): ") or "100")
        emails = get_emails(service, max_results)
        
        if not emails:
            print("No emails to analyze. Exiting.")
            return
        
        # Categorize emails
        emails, domain_stats = categorize_emails(emails)
        
        # Generate summaries
        emails = generate_email_summaries(emails)
        
        # Create report
        report = create_summary_report(emails, domain_stats)
        
        # Save report
        report_file = "gmail_summary_report.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\nSummary report generated and saved to {report_file}")
        print(f"Open this file to view your email summary.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()