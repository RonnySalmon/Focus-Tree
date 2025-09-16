import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from cli import main


def test_cli_add_command():

    test_args = ['cli.py', 'add', 'Test task']
    with patch('sys.argv', test_args):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            assert "добавлена" in output


def test_cli_list_command_empty():

    with patch('cli.load_tasks', return_value=[]):
        test_args = ['cli.py', 'list']
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "пуст" in output


def test_cli_done_command_nonexistent():

    test_args = ['cli.py', 'done', '999']
    with patch('sys.argv', test_args):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            assert "не найдена" in output


def test_cli_help_command():

    test_args = ['cli.py', '--help']
    with patch('sys.argv', test_args):
        with pytest.raises(SystemExit):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "помощник" in output
