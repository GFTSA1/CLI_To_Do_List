# CLI_To_Do_List

This is simple CLI that allows to store data in json file. The user is able to:

-Add, Update, and Delete tasks 
-Mark a task as in progress or done
-List all tasks
-List all tasks that are done
-List all tasks that are not done
-List all tasks that are in progress

There are two versions of this programm: first, on main uses Click, and second version on another branch uses Argparse, which is a built-in module.  

Commands that are availiabe:
-add (Ads task) its argument is task;
-update - arguments are id of the task and description that is updated
-delete 
-list - show all tasks. You can use keys(--done, --in-progress, --todo) to show tasks with specific status.

If json file is not created none of those commands will work. First you have to use command add to start using this CLI.
Project URL: https://roadmap.sh/projects/task-tracker. 
