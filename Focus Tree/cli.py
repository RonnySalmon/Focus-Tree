import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Focus Tree - ваш личный помощник в продуктивности')

    args = parser.parse_args()

    print("Focus Tree активирован! Готов помочь вам с задачами.")


if __name__ == '__main__':
    main()
