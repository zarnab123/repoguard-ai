import re
import shutil
import subprocess
import tempfile
from pathlib import Path


GITHUB_URL_PATTERN = re.compile(
    r"^https://github\.com/[\w.-]+/[\w.-]+/?$"
)


def clone_public_github_repo(repo_url: str) -> Path:
    """Clone one public GitHub repository into a temporary folder."""
    clean_url = repo_url.strip().rstrip("/")

    if not GITHUB_URL_PATTERN.match(clean_url):
        raise ValueError(
            "Please enter a valid public GitHub HTTPS repository URL."
        )

    temporary_folder = Path(tempfile.mkdtemp(prefix="repoguard_"))
    destination = temporary_folder / "repository"

    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", clean_url, str(destination)],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except FileNotFoundError:
        shutil.rmtree(temporary_folder, ignore_errors=True)
        raise ValueError("Git is not installed on this computer.")
    except subprocess.CalledProcessError as error:
        shutil.rmtree(temporary_folder, ignore_errors=True)
        message = error.stderr.strip() or "Unknown Git clone error."
        raise ValueError(f"Could not clone this public repository: {message}")

    return destination


def cleanup_cloned_repository(cloned_repo: Path) -> None:
    """Delete the temporary cloned repository after the audit."""
    shutil.rmtree(cloned_repo.parent, ignore_errors=True)