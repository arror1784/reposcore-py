from typer.testing import CliRunner

import main

runner = CliRunner()


def test_format_option_is_case_insensitive(monkeypatch):
    def fake_load_or_fetch_contributions(
        repos,
        token,
        output,
        no_cache=False,
        since=None,
        until=None,
        page_size=100,
    ):
        return [[] for _ in repos]

    monkeypatch.setattr(
        main,
        "_load_or_fetch_contributions",
        fake_load_or_fetch_contributions,
    )

    result = runner.invoke(
        main.app,
        ["oss2026hnu/reposcore-py", "--format", "CSV", "--token", "dummy-token"],
    )

    assert result.exit_code == 0


def test_page_size_option_is_passed_to_loader(monkeypatch):
    captured = {}

    def fake_load_or_fetch_contributions(
        repos,
        token,
        output,
        no_cache=False,
        since=None,
        until=None,
        page_size=100,
    ):
        captured["page_size"] = page_size
        return [[] for _ in repos]

    monkeypatch.setattr(
        main,
        "_load_or_fetch_contributions",
        fake_load_or_fetch_contributions,
    )

    result = runner.invoke(
        main.app,
        ["oss2026hnu/reposcore-py", "--token", "dummy-token", "--page-size", "25"],
    )

    assert result.exit_code == 0
    assert captured["page_size"] == 25


def test_page_size_envvar_is_passed_to_loader(monkeypatch):
    captured = {}

    def fake_load_or_fetch_contributions(
        repos,
        token,
        output,
        no_cache=False,
        since=None,
        until=None,
        page_size=100,
    ):
        captured["page_size"] = page_size
        return [[] for _ in repos]

    monkeypatch.setattr(
        main,
        "_load_or_fetch_contributions",
        fake_load_or_fetch_contributions,
    )

    result = runner.invoke(
        main.app,
        ["oss2026hnu/reposcore-py", "--token", "dummy-token"],
        env={"REPOSCORE_PAGE_SIZE": "30"},
    )

    assert result.exit_code == 0
    assert captured["page_size"] == 30
