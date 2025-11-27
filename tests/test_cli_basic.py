import pytest

import to_do_cli.parser as parser


def test_add_parses_correctly():
    p = parser.create_parser()
    args = p.parse_args(["add", "Hello"])
    assert args.title == "Hello"
    assert callable(args.func)


def test_list_has_no_args():
    p = parser.create_parser()
    args = p.parse_args(["list"])
    assert callable(args.func)


def test_update_parse_title():
    p = parser.create_parser()
    args = p.parse_args(["update", "1", "--title", "New"])
    assert args.title == "New"


def test_update_parse_done_true():
    p = parser.create_parser()
    args = p.parse_args(["update", "1", "--done"])
    assert args.done is True


def test_update_parse_done_false():
    p = parser.create_parser()
    args = p.parse_args(["update", "1", "--undone"])
    assert args.done is False


def test_delete_parses_index():
    p = parser.create_parser()
    args = p.parse_args(["delete", "3"])
    assert args.index == 3


def test_missing_command_error():
    p = parser.create_parser()
    with pytest.raises(SystemExit) as e:
        p.parse_args([])
    assert e.type is SystemExit


def test_wrong_done_value():
    p = parser.create_parser()
    with pytest.raises(SystemExit) as e:
        p.parse_args(["update", "1", "--done", "maybe"])
    assert e.type is SystemExit
