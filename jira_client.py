# Wrapper around Atlassian API
import requests
from atlassian import Jira
import base64

class JiraClient:
    def __init__(self, base_url, username, api_token):
        self.client = Jira(url=base_url, username=username, password=api_token)
        # Define headers for custom REST API calls
        credentials = f"{username}:{api_token}".encode("utf-8")
        b64_encoded_credentials = base64.b64encode(credentials).decode("utf-8")
        self.headers = {
            "Authorization": f"Basic {b64_encoded_credentials}",
            "Content-Type": "application/json",
        }

    def get_issue(self, issue_key):
        return self.client.get_issue(issue_key)

    #def delete_attachment(self, attachment_id):
    #    return self.client.delete_attachment(attachment_id)

    def delete_attachment(self, attachment_id):
        """
        Deletes an attachment from a Jira issue.

        Args:
            attachment_id (str): The ID of the attachment to delete.

        Returns:
            bool: True if the attachment was deleted successfully, False otherwise.
        """
        try:
            url = f"{self.client.url}/rest/api/2/attachment/{attachment_id}"
            response = requests.delete(url, headers=self.headers)
            if response.status_code == 204:
                print(f"Successfully deleted attachment {attachment_id}.")
                return True
            else:
                print(f"Failed to delete attachment {attachment_id}. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"Error deleting attachment {attachment_id}: {e}")
            return False


    def add_attachment(self, issue_key, file_path):
        return self.client.add_attachment(issue_key=issue_key, filename=file_path)

    def add_comment(self, issue_key, comment_body):
        """
        Add a comment to the specified Jira issue.

        Args:
            issue_key (str): The Jira ticket ID (e.g., PROJ-123).
            comment_body (str): The comment text to be added.

        Returns:
            dict: Response from the Jira API.
        """
        return self.client.issue_add_comment(issue_key=issue_key, comment=comment_body)
    
    #def delete_comment(self, issue_key, comment_id):
    #    """
    #    Deletes a comment from a Jira issue.
#
    #    Args:
    #        issue_key (str): The Jira ticket ID (e.g., PROJ-123).
    #        comment_id (str): The ID of the comment to delete.
#
    #    Returns:
    #        bool: True if successful, False otherwise.
    #    """
    #    return self.client.issue_delete_comment(issue_key=issue_key, comment_id=comment_id)

    def delete_comment(self, issue_key, comment_id):
        """
        Deletes a comment from a Jira issue using the REST API.

        Args:
            issue_key (str): The Jira ticket ID (e.g., PROJ-123).
            comment_id (str): The ID of the comment to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        url = f"{self.client.url}/rest/api/2/issue/{issue_key}/comment/{comment_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            print(f"Successfully deleted comment {comment_id} from {issue_key}.")
            return True
        else:
            print(f"Failed to delete comment {comment_id} from {issue_key}.")
            print(f"Response: {response.status_code} - {response.text}")
            return False


    def get_comments(self, issue_key):
        """
        Retrieves all comments for the given Jira ticket.

        Args:
            issue_key (str): The Jira ticket ID (e.g., PROJ-123).

        Returns:
            list: A list of comments, where each comment contains the ID and body.
        """
        issue = self.client.get_issue(issue_key)
        return issue['fields']['comment']['comments']
    
    def get_attachments(self, issue_key):
        """
        Retrieves the list of attachments for a given Jira issue.

        Args:
            issue_key (str): The Jira ticket ID.

        Returns:
            list: A list of attachment metadata dictionaries.
        """
        try:
            url = f"{self.client.url}/rest/api/2/issue/{issue_key}"
            response = requests.get(url, headers=self.headers)

            if response.status_code != 200:
                print(f"Failed to fetch issue {issue_key}. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return []

            issue = response.json()
            return issue.get("fields", {}).get("attachment", [])
        except Exception as e:
            print(f"Error fetching attachments for issue {issue_key}: {e}")
            return []

    def download_attachment(self, attachment, target_folder):
        """
        Downloads a single attachment from Jira.

        Args:
            attachment (dict): The attachment metadata.
            target_folder (Path): Path to the folder where the attachment will be saved.

        Returns:
            None
        """
        try:
            attachment_name = attachment["filename"]
            attachment_url = attachment["content"]
            save_path = target_folder / attachment_name

            print(f"Downloading attachment: {attachment_name}...")
            response = requests.get(attachment_url, headers=self.headers)

            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    file.write(response.content)
                print(f"Attachment saved to: {save_path}")
            else:
                print(f"Failed to download attachment {attachment_name}. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error downloading attachment {attachment['filename']}: {e}")