from github import Github, Auth, Organization
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    token: str  
    
envs = Settings()

def get_github_client():
    auth = Auth.Token(envs.token)
    github_client = Github(auth=auth)
    return github_client

def get_organization(g: Github):
    org = g.get_organization("AbhiFluxProject")
    return org

def get_repos(org: Organization):
    for repo in org.get_repos():
        print(f"  - {repo.name}")

def create_repo(org: Organization, name: str, description: str = "", private: bool = True):
    repo = org.create_repo(
        name=name,
        description=description,
        private=private,
    )
    print(f"Created repo: {repo.html_url}")
    return repo

def user_exists_in_org(g: Github, org: Organization, username: str) -> bool:
    try:
        user = g.get_user(username)
        return org.has_in_members(user)
    except Exception:
        return False

def write_file(g: Github, repo_name: str, path: str, content: str, message: str = "Update file"):
    repo = g.get_repo(repo_name)
    try:
        file = repo.get_contents(path)
        repo.update_file(path, message, content, file.sha)
    except:
        repo.create_file(path, message, content)

def read_file(g: Github, repo_name: str, path: str) -> str:
    repo = g.get_repo(repo_name)
    file = repo.get_contents(path)
    return file.decoded_content.decode("utf-8")

def delete_file(g: Github, repo_name: str, path: str, message: str = "Delete file"):
    repo = g.get_repo(repo_name)
    file = repo.get_contents(path)
    repo.delete_file(path, message, file.sha)

if __name__ == "__main__":
    g = get_github_client()
    org = get_organization(g)
    # create_repo(org, "test-repo", "This is a test repository")
    #print(user_exists_in_org(g, org, "SadineniAbhi"))
    write_file(g, "AbhiFluxProject/dummy", "README.md", "This is abhi's file")
    get_repos(org)