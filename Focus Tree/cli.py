import argparse

tasks = []


def main():
    parser = argparse.ArgumentParser(
        description='Focus Tree - ваш личный помощник в продуктивности')

    subparsers = parser.add_subparsers(
        dest='command', help='Доступные команды')

    parser_add = subparsers.add_parser('add', help='Добавить новую задачу')

    parser_add.add_argument('title', type=str, help='Название задачи')

    subparsers.add_parser('list', help='Показать все задачи')

    args = parser.parse_args()

    if args.command == 'add':
        tasks.append(args.title)
        print(f'Задача "{args.title}" добавлена!')

    elif args.command == 'list':
        print('Здесь будет список задач')

    else:
        parser.print_help()

    print("Focus Tree активирован! Готов помочь вам с задачами.")


if __name__ == '__main__':
    main()
