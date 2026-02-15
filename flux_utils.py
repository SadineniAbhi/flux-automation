import os
import asyncio
from github_apis import Settings 

envs = Settings()

async def run_command(
    cmd: list[str],
    env: dict[str, str] | None = None,
    cwd: str | None = None,
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
    return proc.returncode, stdout.decode(), stderr.decode()


async def flux_bootstrap_github(owner_name: str, repository_name: str, install_path: str, kubeconfig_path: str) -> tuple[int, str, str]:
    code, out, err = await run_command(
        cmd = [
            "flux", 
            "bootstrap", 
            "github", 
            "token-auth",
            f"--owner={owner_name}",
            f"--repository={repository_name}",
            "--branch=main",
            f"--path={install_path}",
            f"--kubeconfig={kubeconfig_path}", 
            "--personal"
        ],
        env = {
            "GITHUB_TOKEN": envs.token
        }
    )
    return code, out, err

async def flux_uninstall(kubeconfig_path: str) -> tuple[int, str, str]:
    code, out, err = await run_command(
        cmd = [
            "flux", 
            "uninstall", 
            f"--kubeconfig={kubeconfig_path}",
            "--silent"  # skip confirmation prompt
        ]
    )
    return code, out, err
if __name__ == "__main__":
    #code, out, err = asyncio.run(flux_uninstall(kubeconfig_path="kubeconfig/gkeconfig"))
    code, out, err = asyncio.run(flux_bootstrap_github(owner_name="SadineniAbhi", repository_name="test2004", install_path="clusters/gke", kubeconfig_path="kubeconfig/gkeconfig"))
    print(out)
    print(err)
