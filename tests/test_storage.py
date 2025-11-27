import json
import tempfile
from pathlib import Path

import pytest

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


def test_load_empty_file(temp_json):
    assert storage.load_tasks() == []


def test_save_and_load(temp_json):
    data = [{"title": "A", "done": False}]
    storage.save_tasks(data)
    assert storage.load_tasks() == data


def test_load_invalid_json(temp_json):
    temp_json.write_text("{ this is broken json", encoding="utf-8")
    assert storage.load_tasks() == []


def test_save_creates_file(temp_json):
    temp_json.unlink()
    storage.save_tasks([])
    assert storage.DATA_FILE.exists()


def test_save_overwrites(temp_json):
    storage.save_tasks([{"title": "A", "done": False}])
    storage.save_tasks([{"title": "B", "done": True}])
    data = json.loads(storage.DATA_FILE.read_text())
    assert data[0]["title"] == "B"


def test_load_returns_list(temp_json):
    storage.save_tasks([])
    assert isinstance(storage.load_tasks(), list)


def test_load_with_multiple_items(temp_json):
    items = [{"title": f"T{i}", "done": False} for i in range(5)]
    storage.save_tasks(items)
    assert len(storage.load_tasks()) == 5


def test_save_handles_unicode(temp_json):
    storage.save_tasks([{"title": "سلام", "done": False}])
    data = storage.load_tasks()
    assert data[0]["title"] == "سلام"
