from github import Github, Auth, Repository, NamedUser
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    token: str  
    
envs = Settings()

def get_github_client() -> Github:
    """Create and return an authenticated GitHub client."""
    auth = Auth.Token(envs.token)
    github_client = Github(auth=auth)
    return github_client

def get_user(g: Github) -> NamedUser:
    """Get the authenticated user from the GitHub client."""
    user = g.get_user()
    return user

def get_repo(user: NamedUser, name: str) -> Repository:
    """Get a repository by name for the given user."""
    repo = user.get_repo(name)
    return repo

def create_repo(user: NamedUser, name: str, description: str = "", private: bool = True):
    """Create a new repository under the user's account."""
    repo = user.create_repo(
        name=name,
        description=description,
        private=private,
    )
    print(f"Created repo: {repo.html_url}")
    return repo

def write_file(repo: Repository, path: str, content: str, message: str = "Update file"):
    """Create or update a file in the repository."""
    try:
        file = repo.get_contents(path)
        repo.update_file(path, message, content, file.sha)
    except:
        repo.create_file(path, message, content)

def read_file(repo: Repository, path: str) -> str:
    """Read and return the contents of a file from the repository."""
    file = repo.get_contents(path)
    return file.decoded_content.decode("utf-8")

def upload_file(repo: Repository, local_path: str, repo_path: str, message: str = "Add file"):
    """Upload a local file to the repository."""
    with open(local_path, "rb") as f:
        content = f.read()
    repo.create_file(repo_path, message, content)

def delete_repo(repo: Repository):
    """Delete the given repository."""
    repo.delete()
    print(f"Deleted repo: {repo.html_url}")

def list_token_scopes(g: Github) -> list[str]:
    """Return the OAuth scopes available for the current token."""
    g.get_user().login 
    scopes = g.oauth_scopes or []
    return scopes

if __name__ == "__main__":
    g = get_github_client()
    user = get_user(g)
    create_repo(user, "test2004", "This is abhi's test repository")