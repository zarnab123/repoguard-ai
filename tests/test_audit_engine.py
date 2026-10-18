import pytest

from audit_engine import audit_repository


def test_complete_repository_scores_100(tmp_path):
    (tmp_path / "README.md").write_text("# Demo")
    (tmp_path / "requirements.txt").write_text("fastapi")
    (tmp_path / ".gitignore").write_text(".env")
    (tmp_path / "Dockerfile").write_text("FROM python:3.13-slim")
    (tmp_path / ".env.example").write_text("GROQ_API_KEY=your_key_here")
    (tmp_path / "LICENSE").write_text("MIT License")

    tests_folder = tmp_path / "tests"
    tests_folder.mkdir()
    (tests_folder / "test_example.py").write_text("def test_example(): pass")

    workflows_folder = tmp_path / ".github" / "workflows"
    workflows_folder.mkdir(parents=True)
    (workflows_folder / "ci.yml").write_text("name: CI")

    report = audit_repository(str(tmp_path))

    assert report["score"] == 100
    assert report["health"] == "Strong"
    assert all(check["passed"] for check in report["checks"])


def test_empty_repository_gets_zero_score(tmp_path):
    report = audit_repository(str(tmp_path))

    assert report["score"] == 0
    assert report["health"] == "Needs Attention"
    assert len(report["issues"]) == 8


def test_invalid_folder_raises_error():
    with pytest.raises(ValueError):
        audit_repository("this-folder-does-not-exist")