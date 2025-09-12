import argparse
from storage import load_tasks
import commands


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

    try:
        if args.command == 'add':
            commands.add_task(tasks, args.title)
        elif args.command == 'list':
            commands.list_tasks(tasks)
        elif args.command == 'done':
            commands.done_task(tasks, args.task_id)
        elif args.command == 'delete':
            commands.delete_task(tasks, args.task_id)
        elif args.command == 'focus':
            commands.focus_timer(args.minutes)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
