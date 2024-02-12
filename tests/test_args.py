import pytest
from confstore.cli.args import parse_args


def test_parse_args_default():
    """Test that default values are applied."""

    (sockpath, log_out, verbose) = parse_args()

    assert sockpath == "/usr/local/var/run/controller.sock"
    assert log_out is False
    assert verbose is False


def test_parse_args_sockpath():
    (sockpath, _, _) = parse_args(["-s", "/dev/null"])

    assert sockpath == "/dev/null"


def test_parse_args_verbose():
    (_, _, verbose) = parse_args(["-v"])

    assert verbose is True


def test_parse_args_log_out():
    (_, log_out, _) = parse_args(["-o"])

    assert log_out is True


def test_parse_args_help(capsys):
    with pytest.raises(SystemExit):
        (_, _, _) = parse_args(["-h"])
    out, _ = capsys.readouterr()

    assert "show this help message and exit" in out


def test_parse_args_error(capsys):
    with pytest.raises(SystemExit):
        (_, _, _) = parse_args(["-T", "invalid"])
    _, err = capsys.readouterr()

    assert "unrecognized arguments" in err
