import pytest
from commands import add_task, list_tasks, done_task, delete_task
from models import Task


def test_add_task():
    tasks = []

    add_task(tasks, "Test task")

    assert len(tasks) == 1
    assert tasks[0].title == "Test task"
    assert tasks[0].status == "active"
    assert tasks[0].id == 1


def test_add_task_empty_title():
    tasks = []

    with pytest.raises(ValueError, match="Название задачи не может быть пустым"):
        add_task(tasks, "    ")


def test_list_tasks_empty(capsys):

    tasks = []

    list_tasks(tasks)

    captured = capsys.readouterr()
    assert "Список задач пуст" in captured.out


def test_list_tasks_with_items(capsys):

    tasks = [Task(id=1, title="Task 1", status="active"),
             Task(id=2, title="Task 2", status="completed")]

    list_tasks(tasks)

    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out
    assert "active" in captured.out
    assert "completed" in captured.out


def test_done_task():

    tasks = [Task(id=1, title="Test task", status="active")]

    done_task(tasks, 1)

    assert tasks[0].status == "completed"


def test_done_task_nonexistent(capsys):

    tasks = [Task(id=1, title="Test task", status="active")]

    done_task(tasks, 999)

    captured = capsys.readouterr()
    assert "не найдена" in captured.out


def test_delete_task():

    tasks = [Task(id=1, title="Task 1", status="active"),
             Task(id=2, title="Task 2", status="active")]

    delete_task(tasks, 1)

    assert len(tasks) == 1
    assert tasks[0].id == 2


def test_delete_task_nonexistent(capsys):

    tasks = [Task(id=1, title="Test task", status="active")]

    delete_task(tasks, 999)

    captured = capsys.readouterr()
    assert "не найдена" in captured.out
