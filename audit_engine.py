import json
import sys
from pathlib import Path


def has_test_files(repo: Path) -> bool:
    """Check whether the project has Python test files."""
    tests_folder = repo / "tests"

    if not tests_folder.exists():
        return False

    return any(tests_folder.rglob("test_*.py"))


def has_github_actions(repo: Path) -> bool:
    """Check whether the project has a GitHub Actions workflow."""
    workflows_folder = repo / ".github" / "workflows"

    if not workflows_folder.exists():
        return False

    return any(workflows_folder.glob("*.yml")) or any(
        workflows_folder.glob("*.yaml")
    )


def audit_repository(repo_path: str) -> dict:
    """
    Audit a local repository for practical engineering standards.
    Returns an evidence-based score and prioritized improvements.
    """
    repo = Path(repo_path).resolve()

    if not repo.exists() or not repo.is_dir():
        raise ValueError(f"Repository folder not found: {repo}")

    checks = [
        {
            "name": "README documentation",
            "points": 15,
            "passed": (repo / "README.md").exists(),
            "expected": "README.md",
            "recommendation": "Add a clear README with project purpose, setup, and usage.",
        },
        {
            "name": "Automated tests",
            "points": 20,
            "passed": has_test_files(repo),
            "expected": "tests/test_*.py",
            "recommendation": "Add pytest tests for the important project features.",
        },
        {
            "name": "Dependency file",
            "points": 10,
            "passed": (repo / "requirements.txt").exists()
            or (repo / "pyproject.toml").exists(),
            "expected": "requirements.txt or pyproject.toml",
            "recommendation": "Add a dependency file so another developer can run the project.",
        },
        {
            "name": "Git ignore rules",
            "points": 10,
            "passed": (repo / ".gitignore").exists(),
            "expected": ".gitignore",
            "recommendation": "Add .gitignore to keep secrets and virtual environments out of Git.",
        },
        {
            "name": "Docker support",
            "points": 15,
            "passed": (repo / "Dockerfile").exists(),
            "expected": "Dockerfile",
            "recommendation": "Add a Dockerfile for consistent local and cloud deployment.",
        },
        {
            "name": "Continuous integration",
            "points": 15,
            "passed": has_github_actions(repo),
            "expected": ".github/workflows/*.yml",
            "recommendation": "Add GitHub Actions to run tests automatically on every push.",
        },
        {
            "name": "Environment example",
            "points": 5,
            "passed": (repo / ".env.example").exists(),
            "expected": ".env.example",
            "recommendation": "Add .env.example without real secret values.",
        },
        {
            "name": "Open-source licence",
            "points": 10,
            "passed": (repo / "LICENSE").exists() or (repo / "LICENSE.md").exists(),
            "expected": "LICENSE",
            "recommendation": "Add an MIT licence so others know how the code may be used.",
        },
    ]

    score = sum(check["points"] for check in checks if check["passed"])

    if score >= 80:
        health = "Strong"
    elif score >= 60:
        health = "Needs Improvement"
    else:
        health = "Needs Attention"

    issues = []
    for check in checks:
        check["evidence"] = (
            f"Found: {check['expected']}"
            if check["passed"]
            else f"Missing: {check['expected']}"
        )

        if not check["passed"]:
            issues.append(
                {
                    "issue": check["name"],
                    "priority": "High" if check["points"] >= 15 else "Medium",
                    "evidence": check["evidence"],
                    "recommendation": check["recommendation"],
                }
            )

    return {
        "repository": repo.name,
        "score": score,
        "health": health,
        "checks": checks,
        "issues": issues,
    }


if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    report = audit_repository(target_path)
    print(json.dumps(report, indent=2))