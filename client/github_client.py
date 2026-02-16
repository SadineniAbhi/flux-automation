from github import Github, Auth, Repository, NamedUser

class GithubClient:
    def __init__(self, token: str):
        self.token = token
        auth = Auth.Token(self.token)
        self.github_client = Github(auth=auth)

    def get_user(self) -> NamedUser:
        """Get the authenticated user from the GitHub client."""
        user = self.github_client.get_user()
        return user

    def get_repo(self, user: NamedUser, name: str) -> Repository:
        """Get a repository by name for the given user."""
        repo = user.get_repo(name)
        return repo

    def create_repo(self, user: NamedUser, name: str, description: str = "", private: bool = True):
        """Create a new repository under the user's account."""
        repo = user.create_repo(
            name=name,
            description=description,
            private=private,
        )
        print(f"Created repo: {repo.html_url}")
        return repo

    def write_file(self, repo: Repository, path: str, content: str, message: str = "Update file"):
        """Create or update a file in the repository."""
        try:
            file = repo.get_contents(path)
            repo.update_file(path, message, content, file.sha)
        except:
            repo.create_file(path, message, content)

    def read_file(self, repo: Repository, path: str) -> str:
        """Read and return the contents of a file from the repository."""
        file = repo.get_contents(path)
        return file.decoded_content.decode("utf-8")

    def upload_file(self, repo: Repository, local_path: str, repo_path: str, message: str = "Add file"):
        """Upload a local file to the repository."""
        with open(local_path, "rb") as f:
            content = f.read()
        repo.create_file(repo_path, message, content)

    def delete_repo(self, repo: Repository):
        """Delete the given repository."""
        repo.delete()
        print(f"Deleted repo: {repo.html_url}")

    def list_token_scopes(self, user: NamedUser) -> list[str]:
        """Return the OAuth scopes available for the current token."""
        scopes = user.oauth_scopes or []
        return scopes


if __name__ == "__main__":
    pass