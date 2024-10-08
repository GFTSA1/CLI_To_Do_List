import argparse
import json
from datetime import datetime

json_file = "json_file_argparse.json"


class Task:
    def __init__(self, task, string_time):
        self.description = task
        self.status = "Todo"
        self.time = string_time
        self.updated_time = 0


def add(task):
    with open(json_file, "a+") as task_file:
        task_file.seek(0)

        data_read = task_file.read().strip()
        if len(data_read) != 0:
            data = json.loads(data_read)
            id_key = int(list(data.keys())[-1]) + 1
        else:
            data = {}
            id_key = 1

        date = datetime.now()
        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        task_instance = Task(task, date_string)

        task_dictionary = {
            id_key: {
                "description": task_instance.description,
                "status": task_instance.status,
                "started_time": task_instance.time,
                "updated_time": task_instance.updated_time,
            }
        }
        if check_if_task_in_todolist(task, data):
            data.update(task_dictionary)

            with open(json_file, "w+") as task_file:
                json.dump(data, task_file)

            print(f"You have added {task}, its ID is {id_key}")


def check_if_task_in_todolist(task, data):
    for key_id in data.keys():
        if data[key_id]["description"] == task and data[key_id]["status"] == "Todo":
            print(f"{task} is already in list Todo. Its ID is {key_id}.")
            return False
    return True


def update(task_id, description):
    try:
        with open(json_file, "r+") as task_file:
            task_file.seek(0)
            data_read = task_file.read().strip()
            if len(data_read) != 0:
                data = json.loads(data_read)
            else:
                print("There is nothing to update")
                return
            if task_id not in data:
                print("There is no such task")
                return

            data[task_id]["description"] = description
            data[task_id]["updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(json_file, "w+") as task_file:
            json.dump(data, task_file)

        print(
            f"You have updated {task_id}. Its description now is {data[task_id]['description']}"
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            "There is nothing to delete. Please use add command to begin using this program"
        ) from None


def delete(task_id):
    try:
        with open(json_file, "r+") as task_file:
            data_read = task_file.read().strip()

            if len(data_read) == 0:
                print("There is nothing to delete")
                return

            data = json.loads(data_read)

            if task_id not in data:
                print("There is no such task")
                return

            data.pop(task_id)

            with open(json_file, "w+") as task_file:
                json.dump(data, task_file)

            print(f"You have deleted {task_id}")
    except FileNotFoundError:
        raise FileNotFoundError(
            "There is nothing to delete. Please use add command to begin using this program"
        ) from None


def mark_in_progress(task_id):
    try:
        with open(json_file, "r+") as task_file:
            data_read = task_file.read().strip()
            if len(data_read) != 0:
                data = json.loads(data_read)
            else:
                print("There is nothing to mark in progress")
                return

            if task_id not in data:
                print("There is no such task")
                return

            data[task_id]["status"] = "In Progress"
            data[task_id]["updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(json_file, "w+") as task_file:
            json.dump(data, task_file)

        print(f"You have marked {task_id} as In progress")
    except FileNotFoundError:
        raise FileNotFoundError(
            "There is nothing to delete. Please use add command to begin using this program"
        ) from None


def mark_done(task_id):
    try:
        with open(json_file, "r+") as task_file:
            data_read = task_file.read().strip()

            if len(data_read) == 0:
                print("There is nothing to mark in done")
                return

            data = json.loads(data_read)

            if task_id not in data:
                print("There is no such task")
                return

            data[task_id]["status"] = "Done"
            data[task_id]["updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(json_file, "w+") as task_file:
            json.dump(data, task_file)

        print(f"You have marked {task_id} as Done")
    except FileNotFoundError:
        raise FileNotFoundError(
            "There is nothing to delete. Please use add command to begin using this program"
        ) from None


def list_tasks(status):
    try:
        with open(json_file, "r+") as task_file:
            data_read = task_file.read().strip()
            if len(data_read) == 0:
                print("There list is empty")
                return

            data = json.loads(data_read)

            for key, value in data.items():
                if status == None:
                    print(
                        f"Key of task: {key} \n"
                        f"Name of task: {data[key]['description']} \n"
                        f"Status: {data[key]['status']} \n"
                        f"Started time: {data[key]['started_time']} \n"
                        f"Last updated time: {data[key]['updated_time']} \n"
                    )
                elif data[key]["status"] == status:
                    print(
                        f"Printing tasks with status {data[key]['status']}\n"
                        f"\n"
                        f"Key of task: {key}\n"
                        f"Name of task: {data[key]['description']} \n"
                        f"Started time: {data[key]['started_time']} \n"
                        f"Last updated time: {data[key]['updated_time']} \n"
                    )
    except FileNotFoundError:
        raise FileNotFoundError(
            "There is nothing to delete. Please use add command to begin using this program"
        ) from None


parser = argparse.ArgumentParser(description="Task Management CLI")
subparsers = parser.add_subparsers(dest="command")

parser_add = subparsers.add_parser("add")
parser_add.add_argument("task", help="Task description for add command")

parser_delete = subparsers.add_parser("delete")
parser_delete.add_argument("task_id", help="Task ID to delete")

parser_update = subparsers.add_parser("update")
parser_update.add_argument("task_id", help="Task ID to update")
parser_update.add_argument("description", help="Description to update", nargs="*")

parser_mark_in_progress = subparsers.add_parser("mark-in-progress")
parser_mark_in_progress.add_argument("task_id", help="Task ID to mark in progress")

parser_mark_done = subparsers.add_parser("mark-done")
parser_mark_done.add_argument("task_id", help="Task ID to mark in done")

parser_list = subparsers.add_parser("list")
parser_list.add_argument(
    "status",
    nargs="?",
    default=None,
    help="Status of tasks that you would like to show",
)

args = parser.parse_args()

if args.command == "add":
    add(args.task)

if args.command == "delete":
    delete(args.task_id)

if args.command == "update":
    update(args.task_id, args.description)

if args.command == "mark-done":
    mark_done(args.task_id)

if args.command == "mark-in-progress":
    mark_in_progress(args.task_id)

if args.command == "list":
    if args.status == "in-progress" or "In-progress" or "In_Progress":
        args.status = "In Progress"
    list_tasks(args.status)
