from typing import List
from models import Task
from storage import save_tasks
import time


def add_task(tasks: List[Task], title: str) -> None:
    if not title.strip():
        raise ValueError("Название задачи не может быть пустым")

    new_id = max((task.id for task in tasks), default=0) + 1
    new_task = Task(id=new_id, title=title.strip())
    tasks.append(new_task)
    save_tasks(tasks)
    print(f'Задача "{title}" добавлена с ID {new_id}!')


def list_tasks(tasks: List[Task]) -> None:
    if not tasks:
        print("Список задач пуст. Добавьте первую задачу!")
        return

    print("Список ваших задач:")
    for task in tasks:
        print(f"[{task.id}] {task.status}: {task.title}")


def done_task(tasks: List[Task], task_id: int) -> None:
    if task_id <= 0:
        raise ValueError("ID задачи должен быть положительным числом")

    for task in tasks:
        if task.id == task_id:
            task.status = 'completed'
            save_tasks(tasks)
            print(f"Задача с ID {task_id} отмечена как выполненная!")
            return

    print(f"Задача с ID {task_id} не найдена.")


def delete_task(tasks: List[Task], task_id: int) -> None:
    if task_id <= 0:
        raise ValueError("ID задачи должен быть положительным числом")

    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Задача с ID {task_id} удалена!")
            return

    print(f"Задача с ID {task_id} не найдена.")


def focus_timer(minutes: int) -> None:
    total_seconds = minutes * 60

    print(f"Фокус-сессия началась! Таймер на {minutes} минут.")
    print("Нажмите Ctrl+C для прерывания.")

    try:
        for remaining in range(total_seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            time_display = f"{mins:02d}:{secs:02d}"
            print(f"Осталось: {time_display}", end='\r')
            time.sleep(1)

        print("\n\nВремя вышло! Фокус-сессия завершена. 🎉")
        print("\a")

    except KeyboardInterrupt:
        print("\n\nФокус-сессия прервана.")
