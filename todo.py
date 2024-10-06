import click
import json
from datetime import datetime

json_file = "json_file.json"


class Task:
    def __init__(self, task, string_time):
        self.description = task
        self.status = "Todo"
        self.time = string_time
        self.updated_time = 0


@click.command("add")
@click.argument("task")
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

            click.echo(f"You have added {task}, its ID is {id_key}")


def check_if_task_in_todolist(task, data):
    for key_id in data.keys():
        if data[key_id]["description"] == task and data[key_id]["status"] == "Todo":
            click.echo(f"{task} is already in list Todo. Its ID is {key_id}.")
            return False
    return True


@click.command("update")
@click.argument("task_id")
@click.argument("description")
def update(task_id, description):
    try:
        with open(json_file, "r+") as task_file:
            task_file.seek(0)
            data_read = task_file.read().strip()
            if len(data_read) != 0:
                data = json.loads(data_read)
            else:
                click.echo("There is nothing to update")
                return
            if task_id not in data:
                click.echo("There is no such task")
                return

            data[task_id]["description"] = description
            data[task_id]["updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(json_file, "w+") as task_file:
            json.dump(data, task_file)

        click.echo(
            f"You have updated {task_id}. Its description now is {data[task_id]['description']}"
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            "There is nothing to delete. Please use add command to begin using this program"
        ) from None


@click.command("delete")
@click.argument("task_id")
def delete(task_id):
    try:
        with open(json_file, "r+") as task_file:
            data_read = task_file.read().strip()

            if len(data_read) == 0:
                click.echo("There is nothing to delete")
                return

            data = json.loads(data_read)

            if task_id not in data:
                click.echo("There is no such task")
                return

            data.pop(task_id)

            with open(json_file, "w+") as task_file:
                json.dump(data, task_file)

            click.echo(f"You have deleted {task_id}")
    except FileNotFoundError:
        raise FileNotFoundError(
            "There is nothing to delete. Please use add command to begin using this program"
        ) from None


@click.command("mark-in-progress")
@click.argument("task_id")
def mark_in_progress(task_id):
    try:
        with open(json_file, "r+") as task_file:
            data_read = task_file.read().strip()
            if len(data_read) != 0:
                data = json.loads(data_read)
            else:
                click.echo("There is nothing to mark in progress")
                return

            if task_id not in data:
                click.echo("There is no such task")
                return

            data[task_id]["status"] = "In Progress"
            data[task_id]["updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(json_file, "w+") as task_file:
            json.dump(data, task_file)

        click.echo(f"You have marked {task_id} as In progress")
    except FileNotFoundError:
        raise FileNotFoundError(
            "There is nothing to delete. Please use add command to begin using this program"
        ) from None


@click.command("mark-done")
@click.argument("task_id")
def mark_done(task_id):
    try:
        with open(json_file, "r+") as task_file:
            data_read = task_file.read().strip()

            if len(data_read) == 0:
                click.echo("There is nothing to mark in done")
                return

            data = json.loads(data_read)

            if task_id not in data:
                click.echo("There is no such task")
                return

            data[task_id]["status"] = "Done"
            data[task_id]["updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(json_file, "w+") as task_file:
            json.dump(data, task_file)

        click.echo(f"You have marked {task_id} as Done")
    except FileNotFoundError:
        raise FileNotFoundError(
            "There is nothing to delete. Please use add command to begin using this program"
        ) from None


@click.command("list-tasks")
@click.option("--todo", "status", flag_value="Todo")
@click.option("--in-progress", "status", flag_value="In Progress")
@click.option("--done", "status", flag_value="Done")
def list_tasks(status):
    try:
        with open(json_file, "r+") as task_file:
            data_read = task_file.read().strip()
            if len(data_read) == 0:
                click.echo("There list is empty")
                return

            data = json.loads(data_read)

            for key, value in data.items():
                if status == None:
                    click.echo(
                        f"Key of task: {key} \n"
                        f"Name of task: {data[key]['description']} \n"
                        f"Status: {data[key]['status']} \n"
                        f"Started time: {data[key]['started_time']} \n"
                        f"Last updated time: {data[key]['updated_time']} \n"
                    )
                elif data[key]["status"] == status:
                    click.echo(
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
