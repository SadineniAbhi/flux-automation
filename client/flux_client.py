import os
import asyncio

class Flux:

    def __init__(self, kubeconfig_path: str, github_token: str):
        self.kubeconfig_path = kubeconfig_path
        self.github_token = github_token

    async def _run_command(
        self,
        cmd: list[str],
        env: dict[str, str] | None = None,
        cwd: str | None = None
    ) -> tuple[int, str, str]:

        """Execute an arbitrary command with optional environment variables."""
        full_env = {**os.environ, **(env or {})}

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=full_env,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        if proc.returncode is None:
            raise RuntimeError(f"unexpected error: command {cmd} terminated without a return code")

        return proc.returncode, stdout.decode(), stderr.decode()


    async def flux_bootstrap_github(
        self,
        owner_name: str, 
        repository_name: str, 
        install_path: str, 
    ) -> tuple[int, str, str]:

        code, out, err = await self._run_command(
            cmd = [
                "flux", 
                "bootstrap", 
                "github", 
                "token-auth",
                f"--owner={owner_name}",
                f"--repository={repository_name}",
                "--branch=main",
                f"--path={install_path}",
                f"--kubeconfig={self.kubeconfig_path}", 
                "--personal"
            ],
            env = {
                "GITHUB_TOKEN": self.github_token
            }
        )
        return code, out, err

    async def flux_uninstall(self) -> tuple[int, str, str]:
        code, out, err = await self._run_command(
            cmd = [
                "flux", 
                "uninstall", 
                f"--kubeconfig={self.kubeconfig_path}",
                "--silent"  # skip confirmation prompt
            ],
        )
        return code, out, err

    async def flux_cleanup(self):
        if self.kubeconfig_path:
            os.remove(self.kubeconfig_path)


if __name__ == "__main__":
    pass
