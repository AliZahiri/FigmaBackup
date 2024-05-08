

# Figma Project Incremental Backup & Rotation

## Introduction

This tool automates the backup of Figma projects by fetching project IDs from a Google Sheet, checking if the projects have been updated, and performing incremental backups. It keeps backups for one week with a rotating deletion policy to manage storage efficiently.

## Features

- **Automated Backups**: Fetches Figma project IDs from a public Google Sheets CSV and backs up projects.
- **Incremental Backups**: Only backs up projects if there have been changes since the last backup.
- **Weekly Rotation**: Old backups are deleted after one week to free up storage.

## Prerequisites

Before you run this tool, ensure you have the following installed:
- Python 3.6 or higher
- `requests` library
- `figma-backup` installed and configured to run from the command line

You will also need:
- A valid Figma API token
- Access to a publicly accessible Google Sheet with project URLs

## Installation

### 1. Clone the Repository:
```bash
git clone https://github.com/yourusername/figma-backup-project.git
cd figma-backup-project
```


### 2. Install Dependencies:
```bash
pip install requests
```
### 3. Set Up figma-backup:

Follow the installation instructions for figma-backup available at:
```bash
https://github.com/mimshins/figma-backup
```

## Configuration

Edit the config.py file (create this based on config.example.py provided) to include your details:

```bash
ACCESS_TOKEN = 'your_figma_access_token'
SHEET_URL = 'your_public_google_sheet_csv_url'
BACKUP_DIRECTORY = '/path/to/your/backup_directory'
```

## Usage

Run the script using Python:

```bash
python backup_script.py
```
This will fetch project IDs from the specified Google Sheet, check for changes using hash comparisons, and perform backups to the designated directory. It will also clean up backups older than one week.

## Backup Structure

Backups are stored in directories named after the backup date (YYYY-MM-DD) under the specified backup directory. Each project's backup is stored in a subdirectory named after the project ID.

## Cleaning Up Old Backups

The script automatically deletes backups older than one week. Ensure that your system's date and time settings are correct, as this affects the backup rotation logic.

## Troubleshooting

Permissions Issues: Make sure the script has the necessary permissions to access the backup directory.
Dependency Errors: Ensure all required Python packages are installed.
API Rate Limits: Be aware of the Figma API's rate limits and adjust the frequency of backups if needed.
