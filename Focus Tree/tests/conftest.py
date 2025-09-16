import pytest
import os
from storage import TASKS_FILE


@pytest.fixture(autouse=True)
def clean_tasks_file():

    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
    yield

    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
