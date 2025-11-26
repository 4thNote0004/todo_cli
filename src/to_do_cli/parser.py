import argparse
from argparse import Namespace

from to_do_cli.tasks import add_task, list_tasks


def add_task_wrapper(args: Namespace) -> None:
    add_task(args.title)


def list_tasks_wrapper(_: Namespace) -> None:
    list_tasks()


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=" to-do cli App")
    sub = parser.add_subparsers(dest="command")

    add_cmd = sub.add_parser("add", help="add a task")
    add_cmd.add_argument("--title", required=True)
    add_cmd.set_defaults(func=add_task_wrapper)

    list_cmd = sub.add_parser("list", help="list all tasks")
    list_cmd.set_defaults(func=list_tasks_wrapper)

    return parser
