import streamlit as st

from audit_engine import audit_repository
from llm_report import generate_ai_report
from repo_loader import cleanup_cloned_repository, clone_public_github_repo


st.set_page_config(
    page_title="RepoGuard AI",
    page_icon="🛡️",
    layout="wide",
)


st.markdown(
    """
    <style>
        .stApp {
            background: #f7f8fc;
            color: #172033;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }

        .hero {
            padding: 2.2rem;
            border-radius: 22px;
            background: linear-gradient(135deg, #172554 0%, #312e81 55%, #4f46e5 100%);
            color: white;
            margin-bottom: 1.4rem;
            box-shadow: 0 14px 35px rgba(49, 46, 129, 0.22);
        }

        .hero h1 {
            margin: 0;
            font-size: 2.2rem;
            letter-spacing: -0.04em;
        }

        .hero p {
            color: #dbeafe;
            font-size: 1.05rem;
            margin-bottom: 0;
        }

        .eyebrow {
            color: #bfdbfe;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        .metric-card {
            background: white;
            border: 1px solid #e7eaf3;
            border-radius: 16px;
            padding: 1.2rem 1.3rem;
            min-height: 118px;
            box-shadow: 0 5px 18px rgba(20, 30, 60, 0.05);
        }

        .metric-label {
            color: #667085;
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .metric-value {
            color: #172033;
            font-size: 1.85rem;
            font-weight: 800;
            margin-top: 0.25rem;
        }

        .section-title {
            color: #172033;
            font-size: 1.25rem;
            font-weight: 800;
            margin-top: 1.8rem;
            margin-bottom: 0.3rem;
        }

        .section-text {
            color: #667085;
            margin-bottom: 1rem;
        }

        .stButton > button {
            width: 100%;
            border: 0;
            border-radius: 10px;
            background: #4f46e5;
            color: white !important;
            font-weight: 700;
            padding: 0.7rem 1rem;
        }

        .stButton > button:hover {
            background: #3730a3;
            color: white !important;
        }

        .check-pass {
            color: #047857;
            font-weight: 700;
        }

        .check-fail {
            color: #b42318;
            font-weight: 700;
        }

        .footer-note {
            color: #667085;
            font-size: 0.86rem;
            margin-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def audit_github_repository(github_url: str) -> dict:
    """Clone, audit, generate an AI report, then remove the temporary clone."""
    cloned_repo = None

    try:
        cloned_repo = clone_public_github_repo(github_url)
        report = audit_repository(str(cloned_repo))

        report["source_url"] = github_url
        report["display_name"] = github_url.rstrip("/").split("/")[-1]
        report["ai_report"] = generate_ai_report(report)

        return report

    finally:
        if cloned_repo:
            cleanup_cloned_repository(cloned_repo)


def score_color(score: int) -> str:
    if score >= 80:
        return "#047857"
    if score >= 60:
        return "#b45309"
    return "#b42318"


if "report" not in st.session_state:
    st.session_state.report = None


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">AI-powered engineering review</div>
        <h1>RepoGuard AI</h1>
        <p>Audit a public GitHub repository and receive an evidence-based quality score with practical AI recommendations.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Audit a public repository")

github_url = st.text_input(
    "Public GitHub repository URL",
    placeholder="https://github.com/username/project-name",
)

st.caption(
    "RepoGuard only performs a read-only audit. It does not run or modify the target project's code."
)

if st.button("Audit repository", type="primary"):
    if not github_url.strip():
        st.error("Please paste a public GitHub repository URL first.")
    else:
        try:
            with st.spinner("Cloning repository, running checks, and generating AI recommendations..."):
                st.session_state.report = audit_github_repository(github_url)

            st.success("Audit complete.")

        except ValueError as error:
            st.error(str(error))

        except Exception:
            st.error(
                "The audit could not be completed. Check that the repository is public and try again."
            )


report = st.session_state.report

if report:
    score = report["score"]
    passed_checks = sum(1 for check in report["checks"] if check["passed"])
    total_checks = len(report["checks"])

    st.markdown(
        f"""
        <div class="section-title">Audit results</div>
        <div class="section-text">
            Evidence-based review for <b>{report["display_name"]}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    first, second, third = st.columns(3)

    with first:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Repository score</div>
                <div class="metric-value" style="color:{score_color(score)};">{score}/100</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with second:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Health status</div>
                <div class="metric-value">{report["health"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with third:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Checks passed</div>
                <div class="metric-value">{passed_checks}/{total_checks}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Engineering checks</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-text">Every result includes direct evidence from the repository.</div>',
        unsafe_allow_html=True,
    )

    for check in report["checks"]:
        status = "Passed" if check["passed"] else "Needs work"
        status_class = "check-pass" if check["passed"] else "check-fail"
        icon = "✓" if check["passed"] else "!"

        with st.expander(f"{icon}  {check['name']} — {status}", expanded=False):
            st.markdown(
                f'<span class="{status_class}">{check["evidence"]}</span>',
                unsafe_allow_html=True,
            )
            st.write(check["recommendation"])

    st.markdown('<div class="section-title">AI improvement report</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-text">Generated from the repository audit results.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(report["ai_report"])

    st.markdown(
        f"""
        <div class="footer-note">
            Audited source: <a href="{report["source_url"]}" target="_blank">{report["source_url"]}</a>
        </div>
        """,
        unsafe_allow_html=True,
    )