import os
import tempfile
import pytest
from storage import load_tasks, save_tasks
from models import Task


def test_load_tasks_nonexistent_file():

    assert load_tasks('nonexistent_file_12345.json') == []


def test_save_and_load_tasks():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        tmp_name = tmp.name

    try:
        test_tasks = [Task(id=1, title="Test 1", status="active"),
                      Task(id=2, title="Test 2", status="completed")]

        save_tasks(test_tasks, tmp_name)

        loaded_tasks = load_tasks(tmp_name)

        assert len(loaded_tasks) == 2
        assert loaded_tasks[0].id == 1
        assert loaded_tasks[0].title == "Test 1"
        assert loaded_tasks[0].status == "active"
        assert loaded_tasks[1].id == 2
        assert loaded_tasks[1].title == "Test 2"
        assert loaded_tasks[1].status == "completed"

    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def test_load_tasks_invalid_json():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        tmp.write('invalid json content')
        tmp_name = tmp.name

    try:
        assert load_tasks(tmp_name) == []

    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
