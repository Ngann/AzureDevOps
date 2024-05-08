import requests
import base64

# Azure DevOps Personal Access Token
token = 'YOUR-PERSONAL-ACCESS-TOKEN'

# Azure DevOps organization URL and project name
org_url = 'https://dev.azure.com/YourOrganization'
project_name = 'YourProject'

# Keyword to search and replace
keyword = 'old_keyword'
new_keyword = 'new_keyword'

# Headers for API requests
headers = {
    'Authorization': 'Basic ' + base64.b64encode(bytes(':' + token, 'ascii')).decode('ascii')
}

# Search for files containing the keyword
search_url = f'{org_url}/{project_name}/_apis/search/codesearchresults?api-version=6.0-preview.1&searchText={keyword}'
search_response = requests.get(search_url, headers=headers)
search_data = search_response.json()

# Update files containing the keyword
if 'results' in search_data:
    for result in search_data['results']:
        repo_id = result['repository']['id']
        file_path = result['path']

        # Get file content
        file_url = f'{org_url}/_apis/git/repositories/{repo_id}/items?path={file_path}&api-version=6.0'
        file_response = requests.get(file_url, headers=headers)
        file_data = file_response.json()

        # Modify file content
        file_content = base64.b64decode(file_data['content']).decode('utf-8')
        updated_content = file_content.replace(keyword, new_keyword)

        # Commit changes
        commit_url = f'{org_url}/_apis/git/repositories/{repo_id}/pushes?api-version=6.0'
        commit_data = {
            "refUpdates": [{
                "name": "refs/heads/master",
                "oldObjectId": file_data['commitId']
            }],
            "commits": [{
                "comment": f"Updated keyword from {keyword} to {new_keyword}",
                "changes": [{
                    "changeType": "edit",
                    "item": {
                        "path": file_path
                    },
                    "newContent": {
                        "content": base64.b64encode(updated_content.encode()).decode(),
                        "contentType": "rawtext"
                    }
                }]
            }]
        }

        commit_response = requests.post(commit_url, json=commit_data, headers=headers)
        if commit_response.status_code == 200:
            print(f"File {file_path} updated successfully.")
        else:
            print(f"Failed to update file {file_path}. Error: {commit_response.text}")
