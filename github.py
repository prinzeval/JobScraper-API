from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Model for the GitHub URL input
class RepoLink(BaseModel):
    url: str

# Function to fetch repository contents from GitHub API
def fetch_repo_contents(url: str):
    api_url = url.replace("https://github.com/", "https://api.github.com/repos/")
    contents_url = f"{api_url}/contents"
    response = requests.get(contents_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch repository contents")
    return response.json()

# Function to fetch file content from GitHub API
def fetch_file_content(file_url: str):
    response = requests.get(file_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch file content from {file_url}")
    return response.text

# Function to analyze repository contents and fetch file contents
def analyze_repo(contents):
    file_types = {}
    total_files = 0
    total_size = 0
    formatted_files_content = []
    
    for item in contents:
        if item['type'] == 'file':
            total_files += 1
            total_size += item['size']
            file_extension = item['name'].split('.')[-1]
            if file_extension not in file_types:
                file_types[file_extension] = 0
            file_types[file_extension] += 1
            
            # Fetch the file content
            file_content = fetch_file_content(item['download_url'])
            formatted_content = f"================================================\nFile: /{item['name']}\n================================================\n{file_content}\n"
            formatted_files_content.append(formatted_content)
            
    return {
        'total_files': total_files,
        'total_size': total_size,
        'file_types': file_types,
        'files_content': '\n'.join(formatted_files_content)
    }

# Endpoint to analyze GitHub repository and fetch file contents
@app.post("/analyze_repo/")
def analyze_repo_endpoint(repo_link: RepoLink):
    contents = fetch_repo_contents(repo_link.url)
    analysis = analyze_repo(contents)
    return analysis

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
