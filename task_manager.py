# Handles repetitive tasks
from pathlib import Path
import csv
import requests


from jira_automation_framework.utils.logger import setup_logger


class TaskManager:
    def __init__(self, jira_client):
        self.jira_client = jira_client

    def clean_and_upload(self, issue_key, file_path):
        """
        Deletes existing attachments and uploads a new file to a Jira issue.

        Args:
            issue_key (str): Jira ticket ID.
            file_path (str): Path to the file to upload.
        """
        if self.delete_attachments(issue_key):
            self.upload_attachment(issue_key, file_path)

    def delete_attachments(self, issue_key):
        """
        Deletes all attachments from a given Jira issue.

        Args:
            issue_key (str): Jira ticket ID.
        """
        issue = self.jira_client.get_issue(issue_key)
        if not issue:
            print(f"Issue {issue_key} not found.")
            return False

        attachments = issue.get("fields", {}).get("attachment", [])
        for attachment in attachments:
            if self.jira_client.delete_attachment(attachment["id"]):
                print(f"Deleted attachment: {attachment['filename']}")
            else:
                print(f"Failed to delete attachment: {attachment['filename']}")
        return True
    
    def upload_attachment(self, issue_key, file_path):
        """
        Uploads an attachment to a given Jira issue.

        Args:
            issue_key (str): Jira ticket ID.
            file_path (str): Path to the file to upload.
        """
        if self.jira_client.add_attachment(issue_key, file_path):
            print(f"Uploaded file {file_path} to issue {issue_key}.")
            return True
        else:
            print(f"Failed to upload file {file_path} to issue {issue_key}.")
            return False

    def add_comment_to_issue(self, issue_key, comment_body):
        """
        Add a comment to the given Jira issue.

        Args:
            issue_key (str): Jira ticket ID.
            comment_body (str): Comment text.
        """
        response = self.jira_client.add_comment(issue_key, comment_body)
        print(f"Added comment to {issue_key}: {response.get('body')}")

    def delete_comment_from_issue(self, issue_key, comment_id):
        """
        Deletes a comment from a Jira issue.

        Args:
            issue_key (str): Jira ticket ID.
            comment_id (str): ID of the comment to delete.
        """
        if self.jira_client.delete_comment(issue_key, comment_id):
            print(f"Deleted comment {comment_id} from {issue_key}.")
        else:
            print(f"Failed to delete comment {comment_id} from {issue_key}.")

    def download_attachments_from_csv(self, csv_file, target_folder):
        """
        Maps Jira tickets from a CSV file and downloads attachments.

        Args:
            csv_file (str): Path to the CSV file containing Jira tickets and function names.
            target_folder (str): Path to the folder where attachments will be saved.

        Returns:
            None
        """
        try:
            # Ensure the target folder exists
            target_folder_path = Path(target_folder)
            target_folder_path.mkdir(parents=True, exist_ok=True)

            with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    ticket = row.get("Ticket")
                    if not ticket:
                        print(f"Skipping row due to missing ticket: {row}")
                        continue

                    print(f"Processing ticket: {ticket}")

                    # Get the list of attachments from JiraClient
                    attachments = self.jira_client.get_attachments(ticket)

                    if not attachments:
                        print(f"No attachments found for ticket {ticket}.")
                        continue

                    # Download each attachment
                    for attachment in attachments:
                        try:
                            self.jira_client.download_attachment(attachment, target_folder_path)
                        except Exception as e:
                            print(f"Error downloading attachment {attachment['filename']} for ticket {ticket}: {e}")

        except Exception as e:
            print(f"Error processing the CSV file: {e}")
