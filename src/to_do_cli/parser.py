import argparse
from argparse import Namespace

from to_do_cli.tasks import add_task, delete_task, list_tasks, update_task


def str_to_bool(v: str) -> bool:
    return v.lower() == "true"


def add_task_wrapper(args: Namespace) -> None:
    add_task(args.title)


def list_tasks_wrapper(_: Namespace) -> None:
    list_tasks()


def update_task_wrapper(args: Namespace) -> None:
    done_value = None

    if args.done:
        done_value = True
    elif args.undone:
        done_value = False

    update_task(args.index - 1, args.title, done_value)


def delete_task_wrapper(args: Namespace) -> None:
    delete_task(args.index - 1)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="To-Do CLI App")
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    # add
    add_cmd = sub.add_parser("add", help="add a task")
    add_cmd.add_argument("title")
    add_cmd.set_defaults(func=add_task_wrapper)

    # list
    list_cmd = sub.add_parser("list", help="list all tasks")
    list_cmd.set_defaults(func=list_tasks_wrapper)

    # update
    update_cmd = sub.add_parser("update", help="update a task")
    update_cmd.add_argument("index", type=int)
    update_cmd.add_argument("--title")
    state_group = update_cmd.add_mutually_exclusive_group()
    state_group.add_argument("--done", action="store_true")
    state_group.add_argument("--undone", action="store_true")
    update_cmd.set_defaults(func=update_task_wrapper)

    # delete
    delete_cmd = sub.add_parser("delete", help="delete a task")
    delete_cmd.add_argument("index", type=int)
    delete_cmd.set_defaults(func=delete_task_wrapper)

    return parser
