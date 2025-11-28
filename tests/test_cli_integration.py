import json
import tempfile
from pathlib import Path

import pytest
import to_do_cli.main as cli_main
import to_do_cli.storage as storage


@pytest.fixture
def temp_json(monkeypatch):
    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        tf.write("[]")
        tf.flush()
        path = Path(tf.name)

    monkeypatch.setattr(storage, "DATA_FILE", path)
    yield path
    path.unlink(missing_ok=True)


def run_cli(args, capfd):
    cli_main.main(args)
    return capfd.readouterr().out


def test_cli_add(temp_json, capfd):
    out = run_cli(["add", "A"], capfd)
    data = json.loads(temp_json.read_text())
    assert data[0]["title"] == "A"
    assert "added" in out


def test_cli_list(temp_json, capfd):
    storage.save_tasks([{"title": "X", "done": False}])
    out = run_cli(["list"], capfd)
    assert "1. [✗] X" in out


def test_cli_update_title(temp_json, capfd):
    storage.save_tasks([{"title": "Old", "done": False}])
    run_cli(["update", "1", "--title", "New"], capfd)
    assert storage.load_tasks()[0]["title"] == "New"


def test_cli_update_done(temp_json, capfd):
    storage.save_tasks([{"title": "A", "done": False}])
    run_cli(["update", "1", "--done"], capfd)
    assert storage.load_tasks()[0]["done"] is True


def test_cli_delete(temp_json, capfd):
    storage.save_tasks(
        [
            {"title": "A", "done": False},
            {"title": "B", "done": False},
        ]
    )
    run_cli(["delete", "1"], capfd)
    assert storage.load_tasks()[0]["title"] == "B"


def test_cli_invalid_update(temp_json, capfd):
    out = run_cli(["update", "99", "--title", "X"], capfd)
    assert "invalid index" in out.lower()


def test_cli_invalid_delete(temp_json, capfd):
    out = run_cli(["delete", "88"], capfd)
    assert "invalid" in out.lower()
