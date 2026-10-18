from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from audit_engine import audit_repository
from llm_report import generate_ai_report
from repo_loader import cleanup_cloned_repository, clone_public_github_repo


app = FastAPI(
    title="RepoGuard AI",
    description="An AI-powered repository auditing API.",
    version="1.0.0",
)


class AuditRequest(BaseModel):
    repo_path: str | None = Field(
        default=None,
        description="Local path of a repository to audit",
    )
    github_url: str | None = Field(
        default=None,
        description="Public GitHub HTTPS repository URL to audit",
    )


@app.get("/")
def home():
    return {
        "message": "Welcome to RepoGuard AI",
        "purpose": "Audit repositories and generate AI improvement reports.",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/audit")
def audit(request: AuditRequest):
    if not request.repo_path and not request.github_url:
        raise HTTPException(
            status_code=400,
            detail="Provide either repo_path or github_url.",
        )

    if request.repo_path and request.github_url:
        raise HTTPException(
            status_code=400,
            detail="Provide only one: repo_path or github_url.",
        )

    cloned_repo = None

    try:
        if request.github_url:
            cloned_repo = clone_public_github_repo(request.github_url)
            report = audit_repository(str(cloned_repo))
            report["source_url"] = request.github_url
        else:
            report = audit_repository(request.repo_path)

        report["ai_report"] = generate_ai_report(report)
        return report

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    finally:
        if cloned_repo:
            cleanup_cloned_repository(cloned_repo)