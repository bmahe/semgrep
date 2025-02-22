import shutil
import subprocess

import pytest
from click.testing import CliRunner

from semgrep.cli import cli


@pytest.fixture(scope="session", autouse=True)
def in_semgrep_rules_repo(tmpdir_factory):
    monkeypatch = pytest.MonkeyPatch()
    repo_dir = tmpdir_factory.mktemp("semgrep-rules")
    subprocess.check_output(
        [
            "git",
            "clone",
            "--depth=1",
            "https://github.com/returntocorp/semgrep-rules",
            repo_dir,
        ]
    )
    # Remove subdir that doesnt contain rules
    shutil.rmtree(repo_dir / "stats")
    monkeypatch.chdir(repo_dir)
    yield
    monkeypatch.undo()


@pytest.mark.slow
def test_semgrep_rules_repo__test(in_semgrep_rules_repo):
    runner = CliRunner()
    results = runner.invoke(
        cli,
        [
            "--disable-version-check",
            "--metrics=off",
            "--strict",
            "--test",
            "--test-ignore-todo",
        ],
    )
    print(results.output)
    assert results.exit_code == 0


@pytest.mark.slow
def test_semgrep_rules_repo__validate(in_semgrep_rules_repo):
    runner = CliRunner()
    results = runner.invoke(
        cli,
        [
            "--disable-version-check",
            "--metrics=off",
            "--strict",
            "--validate",
            "--config=.",
        ],
    )
    print(results.output)
    assert results.exit_code == 0
