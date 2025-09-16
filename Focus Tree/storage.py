import json
import os
from typing import List
from models import Task

TASKS_FILE = 'tasks.json'


def load_tasks(filename='tasks.json') -> List[Task]:

    if not os.path.exists(filename):
        return []

    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return [Task(**task) for task in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks: List[Task], filename='tasks.json') -> None:

    with open(filename, 'w') as f:
        data = [{'id': task.id, 'title': task.title, 'status': task.status}
                for task in tasks]
        json.dump(data, f, indent=4)
