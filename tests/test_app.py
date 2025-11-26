import json
import tempfile
from pathlib import Path

import pytest

import to_do_cli.storage as storage
import to_do_cli.tasks as tasks


# ایجاد فایل JSON موقت و patch کردن DATA_FILE
@pytest.fixture
def temp_json_file(monkeypatch):
    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        tf.write("[]")
        tf.flush()
        temp_path = Path(tf.name)

    # جایگزینی مسیر DATA_FILE داخل to_do_cli.storage
    monkeypatch.setattr(storage, "DATA_FILE", temp_path)

    yield temp_path

    temp_path.unlink(missing_ok=True)


# ------------------------------
# تست add_task()
# ------------------------------
def test_add_task(temp_json_file, capfd):
    tasks.add_task("Test Task 1")

    captured = capfd.readouterr()
    assert "✔ Task added: Test Task 1" in captured.out

    with open(temp_json_file, encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["title"] == "Test Task 1"
    assert data[0]["done"] is False


# ------------------------------
# تست list_tasks()
# ------------------------------
def test_list_tasks(temp_json_file, capfd):
    test_data = [
        {"title": "Task A", "done": False},
        {"title": "Task B", "done": True},
    ]

    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=4)

    tasks.list_tasks()
    captured = capfd.readouterr()

    assert "1. [✗] Task A" in captured.out
    assert "2. [✓] Task B" in captured.out
