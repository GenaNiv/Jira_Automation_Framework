import argparse
import json
import csv
from pathlib import Path

from jira_automation_framework.task_manager import TaskManager
from jira_automation_framework.jira_client import JiraClient


def load_and_validate_config(config_path="config.json"):
    """
    Load and validate the configuration from the specified JSON file.

    Args:
        config_path (str): Path to the configuration JSON file.

    Returns:
        dict: The validated configuration data.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If required configuration parameters are missing.
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Validate required parameters
    required_keys = ["jira_base_url", "jira_username", "jira_api_token"]
    missing_keys = [key for key in required_keys if key not in config or not config[key]]
    if missing_keys:
        raise ValueError(f"Missing required configuration parameters: {', '.join(missing_keys)}")
    
    return config


def upload_command(args):
    """
    Handles the `upload` command to upload a file to a Jira issue.

    Args:
        args (Namespace): Parsed command-line arguments.
    """
    try:
        # Load and validate configuration
        config = load_and_validate_config()

        # Extract configuration parameters
        jira_base_url = config["jira_base_url"]
        jira_username = config["jira_username"]
        jira_api_token = config["jira_api_token"]

        # Initialize TaskManager
        jira_client = JiraClient(jira_base_url, jira_username, jira_api_token)
        task_manager = TaskManager(jira_client)

        # Perform the upload
        print(f"Uploading file '{args.file_path}' to issue '{args.issue_key}'...")
        task_manager.clean_and_upload(args.issue_key, args.file_path)
        print("Upload completed.")

    except Exception as e:
        print(f"Error: {e}")

def add_comment_command(args):
    """
    Handles the `add-comment` command to add a comment to a Jira ticket.

    Args:
        args (Namespace): Parsed command-line arguments.
    """
    try:
        # Load and validate configuration
        config = load_and_validate_config()

        # Extract configuration parameters
        jira_base_url = config["jira_base_url"]
        jira_username = config["jira_username"]
        jira_api_token = config["jira_api_token"]

        # Initialize TaskManager
        jira_client = JiraClient(jira_base_url, jira_username, jira_api_token)
        task_manager = TaskManager(jira_client)

        # Perform the add comment operation
        print(f"Adding comment to issue '{args.issue_key}'...")
        task_manager.add_comment_to_issue(args.issue_key, args.comment)
        print("Comment added successfully.")

    except Exception as e:
        print(f"Error: {e}")

def delete_comment_command(args):
    """
    Handles the `delete-comment` command to delete a comment from a Jira ticket.

    Args:
        args (Namespace): Parsed command-line arguments.
    """
    try:
        # Load and validate configuration
        config = load_and_validate_config()

        # Extract configuration parameters
        jira_base_url = config["jira_base_url"]
        jira_username = config["jira_username"]
        jira_api_token = config["jira_api_token"]

        # Initialize TaskManager
        jira_client = JiraClient(jira_base_url, jira_username, jira_api_token)
        task_manager = TaskManager(jira_client)

        # Perform the delete comment operation
        print(f"Deleting comment '{args.comment_id}' from issue '{args.issue_key}'...")
        task_manager.delete_comment_from_issue(args.issue_key, args.comment_id)
        print("Comment deleted successfully.")

    except Exception as e:
        print(f"Error: {e}")

def upload_multiple_files(args):
    """
    Handles uploading multiple files to corresponding Jira tickets based on the ticket file mapping.

    Args:
        args (Namespace): Parsed command-line arguments.
    """
    try:
        # Load and validate configuration
        config = load_and_validate_config()

        # Extract configuration parameters
        jira_base_url = config["jira_base_url"]
        jira_username = config["jira_username"]
        jira_api_token = config["jira_api_token"]

        # Initialize TaskManager
        jira_client = JiraClient(jira_base_url, jira_username, jira_api_token)
        task_manager = TaskManager(jira_client)

        # Parse the ticket file
        ticket_file_path = Path(args.ticket_file)
        if not ticket_file_path.exists():
            raise FileNotFoundError(f"Ticket file not found: {ticket_file_path}")

        folder_path = Path(args.folder)
        if not folder_path.exists() or not folder_path.is_dir():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        file_mappings = {}
        with open(ticket_file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                ticket = row.get("Ticket")
                function_name = row.get("Function name")
                if ticket and function_name:
                    file_mappings[function_name] = ticket

        if not file_mappings:
            raise ValueError("No valid mappings found in the ticket file.")

        # Upload files to Jira
        uploaded_count = 0
        skipped_count = 0
        skipped_entries = []

        for function_name, ticket in file_mappings.items():
            file_name = f"{function_name}_v0.csv"
            file_path = folder_path / file_name

            if not file_path.exists():
                print(f"File not found for function '{function_name}': {file_name}. Skipping...")
                skipped_count += 1
                skipped_entries.append((function_name, ticket))
                continue

            print(f"Uploading file '{file_name}' to Jira ticket '{ticket}'...")
            task_manager.clean_and_upload(ticket, file_path)
            print(f"File '{file_name}' uploaded successfully to ticket '{ticket}'.")
            uploaded_count += 1

        # Print summary report
        print("\nUpload Summary:")
        print(f"- Files successfully uploaded: {uploaded_count}")
        print(f"- Files skipped: {skipped_count}")

        if skipped_entries:
            print("\nSkipped Entries:")
            for function_name, ticket in skipped_entries:
                print(f"- Function: {function_name}, Ticket: {ticket}")

    except Exception as e:
        print(f"Error: {e}")

def upload_file_command(args):
    """
    Handles the `upload` command to upload a file to a Jira issue.

    Args:
        args (Namespace): Parsed command-line arguments.
    """
    try:
        # Load and validate configuration
        config = load_and_validate_config()

        # Extract configuration parameters
        jira_base_url = config["jira_base_url"]
        jira_username = config["jira_username"]
        jira_api_token = config["jira_api_token"]

        # Initialize TaskManager
        jira_client = JiraClient(jira_base_url, jira_username, jira_api_token)
        task_manager = TaskManager(jira_client)

        # Perform the upload
        print(f"Uploading file '{args.file_path}' to issue '{args.issue_key}'...")
        task_manager.upload_attachment(args.issue_key, args.file_path)
        print("Upload completed.")

    except Exception as e:
        print(f"Error: {e}")


def delete_attachments_command(args):
    """
    Handles the `delete-attachments` command to delete all attachments from a Jira issue.

    Args:
        args (Namespace): Parsed command-line arguments.
    """
    try:
        # Load and validate configuration
        config = load_and_validate_config()

        # Extract configuration parameters
        jira_base_url = config["jira_base_url"]
        jira_username = config["jira_username"]
        jira_api_token = config["jira_api_token"]

        # Initialize TaskManager
        jira_client = JiraClient(jira_base_url, jira_username, jira_api_token)
        task_manager = TaskManager(jira_client)

        # Delete all attachments
        print(f"Deleting all attachments from issue '{args.issue_key}'...")
        task_manager.delete_attachments(args.issue_key)
        print("All attachments deleted.")

    except Exception as e:
        print(f"Error: {e}")

def download_attachments_command(args):
    """
    Handles the `download-attachments` command to download files from Jira tickets.

    Args:
        args (Namespace): Parsed command-line arguments.
    """
    try:
        # Load and validate configuration
        config = load_and_validate_config()

        # Initialize JiraClient and TaskManager
        jira_client = JiraClient(
            base_url=config["jira_base_url"],
            username=config["jira_username"],
            api_token=config["jira_api_token"],
        )
        task_manager = TaskManager(jira_client)

        # Download attachments
        task_manager.download_attachments_from_csv(args.csv_file, args.target_folder)

    except Exception as e:
        print(f"Error: {e}")

def main():
    """
    Main entry point for the CLI.
    """
    parser = argparse.ArgumentParser(description="Jira Automation Framework CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Upload multiple files command
    upload_multiple_parser = subparsers.add_parser("upload-multiple", help="Upload multiple files to Jira tickets based on a mapping file")
    upload_multiple_parser.add_argument("--folder", required=True, help="Path to the folder containing .csv files")
    upload_multiple_parser.add_argument("--ticket-file", required=True, help="Path to the file containing Jira ticket mappings")
    upload_multiple_parser.set_defaults(func=upload_multiple_files)

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload a file to a Jira ticket")
    upload_parser.add_argument("--issue-key", required=True, help="Jira issue key (e.g., PROJ-123)")
    upload_parser.add_argument("--file-path", required=True, help="Path to the file to upload")
    upload_parser.set_defaults(func=upload_file_command)

    # Delete attachments command
    delete_parser = subparsers.add_parser("delete-attachments", help="Delete all attachments from a Jira ticket")
    delete_parser.add_argument("--issue-key", required=True, help="Jira issue key (e.g., PROJ-123)")
    delete_parser.set_defaults(func=delete_attachments_command)


    # Add comment command
    add_comment_parser = subparsers.add_parser("add-comment", help="Add a comment to a Jira ticket")
    add_comment_parser.add_argument("--issue-key", required=True, help="Jira issue key (e.g., PROJ-123)")
    add_comment_parser.add_argument("--comment", required=True, help="The comment text to add")
    add_comment_parser.set_defaults(func=add_comment_command)

    # Delete comment command
    delete_comment_parser = subparsers.add_parser("delete-comment", help="Delete a comment from a Jira ticket")
    delete_comment_parser.add_argument("--issue-key", required=True, help="Jira issue key (e.g., PROJ-123)")
    delete_comment_parser.add_argument("--comment-id", required=True, help="The ID of the comment to delete")
    delete_comment_parser.set_defaults(func=delete_comment_command)

    # Download attachments command
    download_parser = subparsers.add_parser("download-attachments", help="Download attachments from Jira tickets based on a mapping CSV")
    download_parser.add_argument("--csv-file", required=True, help="Path to the CSV file containing Jira ticket mappings")
    download_parser.add_argument("--target-folder", required=True, help="Path to the folder to save downloaded attachments")
    download_parser.set_defaults(func=download_attachments_command)


    # Parse arguments
    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()



if __name__ == "__main__":
    main()
