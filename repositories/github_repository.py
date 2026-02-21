import asyncio
from typing import cast
from github import Github, Auth
from github.Repository import Repository
from github.AuthenticatedUser import AuthenticatedUser
from utils.logger import get_logger 

logger = get_logger(__name__)

class GithubClient:
    def __init__(self, token: str):
        self.token = token
        auth = Auth.Token(self.token)
        self.github_client = Github(auth=auth)

    async def get_github_user(self) -> AuthenticatedUser:
        """Get the authenticated user from the GitHub client."""
        def _get_user_sync(): 
            user = self.github_client.get_user()
            return cast(AuthenticatedUser, user)

        logger.info("Fetching authenticated GitHub user")
        user = await asyncio.to_thread(_get_user_sync)
        logger.info("Authenticated as GitHub user: %s", user.login)
        return user

    async def get_repo(self, repo_name: str) -> Repository:
        """Get a repository by name for the given user."""
        user = await self.get_github_user()

        def _get_repo_sync(repo_name: str) -> Repository:
            repo = user.get_repo(repo_name)
            return repo

        logger.info("Fetching repository: %s", repo_name)
        repo = await asyncio.to_thread(_get_repo_sync, repo_name)
        logger.info("Fetched repository: %s", repo.full_name)
        return repo

    async def create_repo(self, repo_name: str, description: str = "", private: bool = True) -> Repository:
        """Create a new repository under the authenticated user's account."""
        user = await self.get_github_user()

        def _create_repo_sync(repo_name: str, description: str, private: bool) -> Repository:
            repo = user.create_repo(
                name=repo_name,
                description=description,
                private=private,
            )
            return repo

        logger.info("Creating repository: %s (private=%s)", repo_name, private)
        repo = await asyncio.to_thread(_create_repo_sync, repo_name, description, private)
        logger.info("Created repository: %s", repo.full_name)
        return repo

    async def write_file(self, repo_name: str, path: str, content: str, message: str = "Update file") -> None:
        """Create or update a file in the repository."""
        repo = await self.get_repo(repo_name)

        def _write_file_sync(path: str, content: str, message: str) -> None:
            try:
                file = repo.get_contents(path)
                if isinstance(file, list):
                    raise ValueError(f"Path {path} is a directory, not a file")
                logger.info("Updating existing file: %s in %s", path, repo_name)
                repo.update_file(path, message, content, file.sha)
            except ValueError as e:
                raise e
            except Exception:
                logger.info("Creating new file: %s in %s", path, repo_name)
                repo.create_file(path, message, content)

        await asyncio.to_thread(_write_file_sync, path, content, message)
        logger.info("Write complete: %s in %s", path, repo_name)

    async def read_file(self, repo_name: str, path: str) -> str:
        """Read and return the contents of a file from the repository."""
        repo = await self.get_repo(repo_name)

        def _read_file_sync(path: str) -> str:
            file = repo.get_contents(path)
            if isinstance(file, list):
                raise ValueError(f"File {path} does not exist")
            return file.decoded_content.decode("utf-8")

        logger.info("Reading file: %s from %s", path, repo_name)
        content = await asyncio.to_thread(_read_file_sync, path)
        logger.info("Read file: %s from %s (%d bytes)", path, repo_name, len(content))
        return content

    async def upload_file(self, repo_name: str, local_path: str, repo_path: str, message: str = "Add file") -> None:
        """Upload a local file to the repository."""
        repo = await self.get_repo(repo_name)

        def _upload_file_sync(local_path: str, repo_path: str, message: str) -> None:
            with open(local_path, "rb") as f:
                content = f.read()
            repo.create_file(repo_path, message, content)

        logger.info("Uploading file: %s -> %s in %s", local_path, repo_path, repo_name)
        await asyncio.to_thread(_upload_file_sync, local_path, repo_path, message)
        logger.info("Upload complete: %s in %s", repo_path, repo_name)

    async def delete_repo(self, repo_name: str) -> None:
        """Delete the given repository."""
        repo = await self.get_repo(repo_name)

        def _delete_repo_sync() -> None:
            repo.delete()

        logger.info("Deleting repository: %s", repo.full_name)
        await asyncio.to_thread(_delete_repo_sync)
        logger.info("Deleted repository: %s", repo.full_name)

if __name__ == "__main__":
    client = GithubClient(token="") # test with a valid token