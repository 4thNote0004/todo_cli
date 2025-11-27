import json
import tempfile
from pathlib import Path

import pytest

import to_do_cli.storage as storage
import to_do_cli.tasks as tasks


@pytest.fixture
def temp_json(monkeypatch):
    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        tf.write("[]")
        tf.flush()
        path = Path(tf.name)

    monkeypatch.setattr(storage, "DATA_FILE", path)
    yield path
    path.unlink(missing_ok=True)


def test_add_task(temp_json):
    tasks.add_task("Hello")
    data = json.loads(temp_json.read_text())
    assert data[0]["title"] == "Hello"
    assert data[0]["done"] is False


def test_list_tasks(temp_json, capfd):
    storage.save_tasks([
        {"title": "A", "done": False},
        {"title": "B", "done": True},
    ])
    tasks.list_tasks()
    out = capfd.readouterr().out
    assert "1. [✗] A" in out
    assert "2. [✓] B" in out


def test_list_tasks_empty(temp_json, capfd):
    tasks.list_tasks()
    assert "no tasks yet!" in capfd.readouterr().out


def test_update_title(temp_json):
    storage.save_tasks([{"title": "Old", "done": False}])
    tasks.update_task(0, new_title="New")
    assert storage.load_tasks()[0]["title"] == "New"


def test_update_done_true(temp_json):
    storage.save_tasks([{"title": "X", "done": False}])
    tasks.update_task(0, done=True)
    assert storage.load_tasks()[0]["done"] is True


def test_update_done_false(temp_json):
    storage.save_tasks([{"title": "X", "done": True}])
    tasks.update_task(0, done=False)
    assert storage.load_tasks()[0]["done"] is False


def test_update_invalid_index(temp_json, capfd):
    tasks.update_task(5, "x", True)
    assert "invalid index" in capfd.readouterr().out


def test_delete_task(temp_json):
    storage.save_tasks([
        {"title": "A", "done": False},
        {"title": "B", "done": False},
    ])
    tasks.delete_task(0)
    assert storage.load_tasks()[0]["title"] == "B"


def test_delete_invalid(temp_json, capfd):
    tasks.delete_task(10)
    assert "Invalid index" in capfd.readouterr().out


def test_update_no_fields(temp_json):
    storage.save_tasks([{"title": "A", "done": False}])
    tasks.update_task(0)
    assert storage.load_tasks()[0] == {"title": "A", "done": False}
