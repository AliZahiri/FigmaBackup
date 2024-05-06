import requests
import re  # For regex

def fetch_csv_data(url):
    """Fetches CSV data from the given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad requests
    return response.text

def extract_figma_ids(csv_data):
    """Extracts Figma project IDs from CSV data."""
    # Use regex to find patterns that match Figma project URLs
    figma_urls = re.findall(r'https://www.figma.com/files/project/(\d+)', csv_data)
    return figma_urls

# URL of the published Google Sheets CSV
sheet_url = ""

# Fetch and process the data
csv_data = fetch_csv_data(sheet_url)
figma_ids = extract_figma_ids(csv_data)

print("Extracted Figma Project IDs:")
for id in figma_ids:
    print(id)