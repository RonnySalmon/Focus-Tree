import json
import os
from typing import List
from models import Task

TASKS_FILE = 'tasks.json'


def load_tasks() -> list[Task]:
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, 'r') as f:
            data = json.load(f)
            return [Task(**task) for task in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks: list[Task]) -> None:
    with open(TASKS_FILE, 'w') as f:
        data = [{'id': task.id, 'title': task.title,
                 'status': task.status} for task in tasks]
        json.dump(data, f, indent=4)
