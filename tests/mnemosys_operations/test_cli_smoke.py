from __future__ import annotations

from mnemosys_operations import cli


def test_status_command_reports_placeholder(capsys: object) -> None:
    exit_code = cli.main(["status"])

    assert exit_code == 0

    captured = capsys.readouterr()
    assert "no operational commands implemented yet" in captured.out
