# RepoGuard AI

An AI-powered repository auditing tool that reviews a public GitHub repository for practical engineering standards and generates evidence-based improvement recommendations.

RepoGuard AI safely performs a shallow, read-only clone of a public repository. It never runs or modifies the target project's code.

## Why this project?

Many beginner and student projects work locally but lack important engineering practices such as tests, dependency management, CI, Docker, documentation, and safe environment configuration.

RepoGuard AI makes those gaps visible by providing:

- A score out of 100
- Evidence for every engineering check
- Prioritised improvement recommendations
- An AI-generated Markdown review report

## Features

- Audits any valid public GitHub HTTPS repository URL
- Safely clones repositories into a temporary folder
- Checks for eight engineering quality signals
- Generates a quality score and health status
- Shows clear evidence for each passed or missing item
- Uses Groq LLM to create a concise improvement report
- Includes a FastAPI API and professional Streamlit dashboard
- Includes automated tests, GitHub Actions CI, Docker support, `.gitignore`, and `.env.example`

## Engineering checks

| Check | Points |
| --- | ---: |
| README documentation | 15 |
| Automated tests | 20 |
| Dependency file | 10 |
| Git ignore rules | 10 |
| Docker support | 15 |
| Continuous integration | 15 |
| Environment example | 5 |
| Open-source licence | 10 |
| **Total** | **100** |

## Tech stack

- Python
- FastAPI
- Streamlit
- Groq API
- Pydantic
- pytest
- GitHub Actions
- Docker

## Project structure

```text
repoguard-ai/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_audit_engine.py
├── .dockerignore
├── .env.example
├── .gitignore
├── app.py
├── audit_engine.py
├── Dockerfile
├── LICENSE
├── llm_report.py
├── README.md
├── repo_loader.py
├── requirements.txt
└── streamlit_app.py
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/zarnab123/repoguard-ai.git
cd repoguard-ai
```

### 2. Create and activate a virtual environment

**Windows Command Prompt:**

```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a file named `.env` in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Do not commit `.env`. It is already included in `.gitignore`.

## Run the application

### Streamlit dashboard

```cmd
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

### FastAPI API

```cmd
.\.venv\Scripts\python.exe -m uvicorn app:app --reload
```

Open API documentation:

```text
http://127.0.0.1:8000/docs
```

## API usage

Send a `POST` request to `/audit`:

```json
{
  "github_url": "https://github.com/zarnab123/n8n-automation-portfolio"
}
```

The API returns:

- Repository name
- Score and health status
- Individual engineering checks
- Prioritised issues
- AI-generated improvement report

## Run tests

```cmd
.\.venv\Scripts\python.exe -m pytest -v
```

Current result:

```text
3 passed
```

## Docker

Build the application image:

```cmd
docker build -t repoguard-ai .
```

Run the container:

```cmd
docker run --rm -p 8501:8501 --env-file .env repoguard-ai
```

Then open:

```text
http://localhost:8501
```

## Continuous integration

GitHub Actions automatically runs on every push and pull request. It:

1. Sets up Python
2. Installs dependencies
3. Runs the pytest test suite
4. Builds the Docker image

## Security and safety

- Only valid public GitHub HTTPS repository URLs are accepted.
- Repositories are cloned with `--depth 1`.
- Target code is not executed.
- Cloned repositories are deleted after the audit.
- API keys remain local in `.env` and are excluded from Git.

## Quality verification

RepoGuard AI audits its own repository against the same eight engineering checks.

**Self-audit result: 100/100 — Strong**

## Future improvements

- Add repository language and framework detection
- Add more security and code-quality checks
- Add downloadable PDF audit reports
- Add historical audit comparison for repositories

## Author

**Zarnab Javed**  
Aspiring AI Engineer and Data Scientist

GitHub: [zarnab123](https://github.com/zarnab123)