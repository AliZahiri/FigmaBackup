import requests
import re
import subprocess
import os
import json
import hashlib
from datetime import datetime, timedelta
import logging

def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='backup.log',
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def fetch_csv_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("CSV data fetched successfully from the URL.")
        return response.text
    except requests.RequestException as e:
        logging.error("Failed to fetch CSV data", exc_info=True)
        raise

def extract_figma_ids(csv_data):
    try:
        project_ids = re.findall(r'https://www.figma.com/files/project/(\d+)', csv_data)
        logging.info(f"Extracted {len(project_ids)} project IDs successfully.")
        return project_ids
    except Exception as e:
        logging.error("Failed to extract project IDs", exc_info=True)
        raise

def backup_project(project_id, email, password, access_token, backup_dir):
    date_str = datetime.now().strftime("%Y-%m-%d")
    project_backup_dir = os.path.join(backup_dir, date_str, str(project_id))
    os.makedirs(project_backup_dir, exist_ok=True)
    command = f"figma-backup -e \"{email}\" -p \"{password}\" -t \"{access_token}\" --projects-ids {project_id}"
    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f"Backup completed successfully for project ID {project_id} in {project_backup_dir}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Backup failed for project ID {project_id}.", exc_info=True)

def cleanup_old_backups(backup_dir, retention_days=7):
    try:
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        for folder_name in os.listdir(backup_dir):
            folder_path = os.path.join(backup_dir, folder_name)
            folder_date = datetime.strptime(folder_name, "%Y-%m-%d")
            if folder_date < cutoff_date:
                os.rmdir(folder_path)
                logging.info(f"Deleted old backup: {folder_path}")
    except Exception as e:
        logging.error("Failed to clean up old backups", exc_info=True)

def main():
    setup_logging()
    try:
        sheet_url = "your_public_google_sheet_csv_url"
        email = "your_email_here"
        password = "your_password_here"
        access_token = "your_figma_access_token"
        backup_dir = "path_to_your_backup_directory"

        # Fetch project IDs from CSV
        csv_data = fetch_csv_data(sheet_url)
        project_ids = extract_figma_ids(csv_data)

        # Backup each project
        for project_id in project_ids:
            backup_project(project_id, email, password, access_token, backup_dir)

        # Cleanup old backups
        cleanup_old_backups(backup_dir)

    except Exception as e:
        logging.exception("An error occurred during the backup process.")

if __name__ == '__main__':
    main()