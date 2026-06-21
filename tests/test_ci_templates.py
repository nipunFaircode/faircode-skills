from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "skills" / "faircode-cicd-guardrails" / "templates"


def test_github_template_runs_tests_and_coverage():
    y = (TPL / "github" / "erpnext-ci.yml").read_text()
    assert "run-tests" in y
    assert "coverage" in y.lower()
    assert "ruff" in y or "flake8" in y


def test_gitlab_template_runs_tests_and_coverage():
    y = (TPL / "gitlab" / ".gitlab-ci.yml").read_text()
    assert "run-tests" in y
    assert "coverage" in y.lower()
    assert "ruff" in y
