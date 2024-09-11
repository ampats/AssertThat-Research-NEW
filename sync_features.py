import requests
import os
import zipfile
import base64
from github import Github
from dotenv import load_dotenv

load_dotenv()
# AssertThat credentials
at_access_key = os.getenv("AT_ACCESS_KEY")
at_secret_key = os.getenv("AT_SECRET_KEY")
at_encoded_credentials = os.getenv("AT_ENCODED_CREDENTIALS")
at_project_id = os.getenv("AT_PROJECT_ID")
at_path = 'https://bdd.assertthat.app/rest/api/1/project/' + at_project_id + '/features'

# GitHub credentials
github_token = os.getenv("GITHUB_TOKEN")
github_repo = 'ampats/AssertThat-Research-NEW'

# Directory to store feature files
feature_directory = 'feature_files'

# Create a GitHub repository object
g = Github(github_token)
repo = g.get_repo(github_repo)

# Create a directory to store feature files if it doesn't exist
if not os.path.exists(feature_directory):
    os.makedirs(feature_directory)

# Fetch feature files from AssertThat
response = requests.get(
    f'{at_path}',
    headers={'Authorization': 'Basic NDc5OWZkYThiMzNhMDcxMGM5Mjg5OGYxMzI0MDAyNDAxZDk3ZWI2NmFkZmYyOTkxZGViOGM1ZDNiMTdmODczNDpiZmIwMDFjZWMzNjBlMDA2ZDdkYWM4MTY0MWE2YTVkZDc4MmRhZGMwM2VkMTA5M2EyMTAzOGI1ZDlmNmE0M2Rl'}
)

# response = requests.get(at_path,
#     auth=(at_access_key, at_secret_key)
# ) 
# NOTE: The example above is for Jira Data Center. In case you use cloud version the following URL should be used for downloading features: https://bdd.assertthat.app/rest/api/1/project/YOUR_ASSERT_THAT_PROJECT_ID/features
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {response.headers}")
print(f"Response Text: {response.text}")

if response.status_code == 200:
    # Save the feature files ZIP to the local directory
    zip_file_path = os.path.join(feature_directory, 'features.zip')
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(feature_directory)

    # Commit and push each extracted .feature file
    for root, _, files in os.walk(feature_directory):
        for file in files:
            if file.endswith(".feature"):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    content = f.read()
                    # Specify the file path within the repository
                    file_path_within_repo = os.path.relpath(file_path, feature_directory)
                    repo.create_file(
                        path=file_path_within_repo,
                        message=f'Update feature file: {file}',
                        content=content,
                        branch='sync-features-jira-github'
                    )

    # Clean up (delete the local files)
    os.remove(zip_file_path)
    for root, _, files in os.walk(feature_directory):
        for file in files:
            os.remove(os.path.join(root, file))
else:
    print(f'Failed to fetch feature files from AssertThat. Status code: {response.status_code}')
