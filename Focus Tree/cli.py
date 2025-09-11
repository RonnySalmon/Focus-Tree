import argparse
import json
import os

TASKS_FILE = 'tasks.json'


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description='Focus Tree - ваш личный помощник в продуктивности')

    subparsers = parser.add_subparsers(
        dest='command', help='Доступные команды')

    parser_add = subparsers.add_parser('add', help='Добавить новую задачу')

    parser_add.add_argument('title', type=str, help='Название задачи')

    parser_list = subparsers.add_parser('list', help='Показать все задачи')

    parser_done = subparsers.add_parser(
        'done', help='Отметить задачу как выполненную')
    parser_done.add_argument(
        'task_id', type=int, help='ID задачи для отметки как выполненной')

    parser_delete = subparsers.add_parser('delete', help='Удалить задачу')
    parser_delete.add_argument(
        'task_id', type=int, help='ID задачи для удаления')

    parser_focus = subparsers.add_parser(
        'focus', help='Запустить таймер фокус-сессии')
    parser_focus.add_argument('minutes', type=int, nargs='?',
                              default=25, help='Длительность в минутах (по умолчанию 25)')

    args = parser.parse_args()

    tasks = load_tasks()

    if args.command == 'add':
        if tasks:
            new_id = max(task['id'] for task in tasks) + 1
        else:
            new_id = 1

        new_task = {'id': new_id,
                    'title': args.title, 'status': 'active'}

        tasks.append(new_task)

        save_tasks(tasks)
        print(f'Задача "{args.title}" добавлена с ID {new_id}!')

    elif args.command == 'list':
        if not tasks:
            print("Список задач пуст. Добавьте первую задачу!")
        else:
            print("Список ваших задач:")
            for task in tasks:
                print(f"[{task['id']}] {task['status']}: {task['title']}")

    elif args.command == 'done':
        task_found = False
        for task in tasks:
            if task['id'] == args.task_id:
                task['status'] = 'completed'
                task_found = True
                break
        if task_found:
            save_tasks(tasks)
            print(f"Задача с ID {args.task_id} отмечена как выполненная!")
        else:
            print(f"Задача с ID {args.task_id} не найдена.")

    elif args.command == 'delete':
        task_found = False
        for task in tasks:
            if task['id'] == args.task_id:
                tasks.remove(task)
                task_found = True
                break

        if task_found:
            save_tasks(tasks)
            print(f"Задача с ID {args.task_id} удалена!")
        else:
            print(f"Задача с ID {args.task_id} не найдена.")

    elif args.command == 'focus':
        import time
        total_seconds = args.minutes * 60

        print(f"Фокус-сессия началась! Таймер на {args.minutes} минут.")
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

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
