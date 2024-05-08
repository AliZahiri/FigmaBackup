import requests
import re
import subprocess
import os
import json
import hashlib
from datetime import datetime, timedelta

def fetch_csv_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_figma_ids(csv_data):
    return re.findall(r'https://www.figma.com/files/project/(\d+)', csv_data)

def generate_hash(data):
    return hashlib.md5(data.encode()).hexdigest()

def fetch_project_metadata(project_id, access_token):
    headers = {'X-Figma-Token': access_token}
    response = requests.get(f'https://api.figma.com/v1/projects/{project_id}/files', headers=headers)
    response.raise_for_status()
    return response.json()

def load_previous_hashes(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_hashes(hashes, file_path):
    with open(file_path, 'w') as file:
        json.dump(hashes, file)

def backup_project(project_id, access_token, backup_dir):
    date_str = datetime.now().strftime("%Y-%m-%d")
    project_backup_dir = os.path.join(backup_dir, date_str, str(project_id))
    os.makedirs(project_backup_dir, exist_ok=True)
    
    command = f"figma-backup --token {access_token} --project-id {project_id} --output-dir {project_backup_dir}"
    subprocess.run(command, shell=True, check=True)
    print(f"Backup completed for project ID {project_id} in {project_backup_dir}")

def cleanup_old_backups(backup_dir, retention_days=7):
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    for folder_name in os.listdir(backup_dir):
        folder_path = os.path.join(backup_dir, folder_name)
        folder_date = datetime.strptime(folder_name, "%Y-%m-%d")
        if folder_date < cutoff_date:
            subprocess.run(f"rm -rf {folder_path}", shell=True, check=True)
            print(f"Deleted old backup: {folder_path}")

def main():
    sheet_url = "your_public_google_sheet_csv_url"
    access_token = "your_figma_access_token"
    backup_dir = "path_to_your_backup_directory"
    hash_file_path = "path_to_your_hash_store.json"

    # Fetch project IDs from CSV
    csv_data = fetch_csv_data(sheet_url)
    project_ids = extract_figma_ids(csv_data)
    
    # Load previous hashes
    previous_hashes = load_previous_hashes(hash_file_path)
    current_hashes = {}

    # Process each project
    for project_id in project_ids:
        metadata = fetch_project_metadata(project_id, access_token)
        metadata_str = json.dumps(metadata, sort_keys=True)
        current_hash = generate_hash(metadata_str)
        current_hashes[project_id] = current_hash

        if previous_hashes.get(project_id) != current_hash:
            backup_project(project_id, access_token, backup_dir)
    
    # Save current hashes
    save_hashes(current_hashes, hash_file_path)

    # Cleanup old backups
    cleanup_old_backups(backup_dir)

if __name__ == '__main__':
    main()