import requests

# Azure DevOps Personal Access Token
token = 'YOUR-PERSONAL-ACCESS-TOKEN'

# Azure DevOps organization URL and project name
org_url = 'https://dev.azure.com/YourOrganization'
project_name = 'YourProject'

# Keyword to search
keyword = 'your_keyword'

# Headers for API requests
headers = {
    'Authorization': 'Basic ' + token
}

# Search for files containing the keyword
search_url = f'{org_url}/{project_name}/_apis/search/codesearchresults?api-version=6.0-preview.1&searchText={keyword}'
search_response = requests.get(search_url, headers=headers)
search_data = search_response.json()

# Handle search results
if 'results' in search_data:
    for result in search_data['results']:
        repo_name = result['repository']['name']
        file_path = result['path']
        print(f'Repository: {repo_name}, File: {file_path}')
else:
    print("No files found containing the keyword.")

