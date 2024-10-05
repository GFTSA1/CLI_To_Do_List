from setuptools import setup, find_packages

setup(
    name = "todo",
    version = "0.0.1",
    packages = find_packages(),
    install_requires = [
        "click",
    ],
    entry_points = {
        'console_scripts': [
            "add=todo:add",
            "delete=todo:delete",
            "update=todo:update",
            "list-tasks=todo:list_tasks",
            "mark-in-progress=todo:mark_in_progress",
            "mark-done=todo:mark_done"
        ]
    }
)