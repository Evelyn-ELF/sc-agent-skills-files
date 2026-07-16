from typing import Annotated

import typer

from task import display
from task.constants import EXIT_ERROR, EXIT_INVALID_INPUT
from task.models import Priority
from task.storage import load_tasks, save_tasks

app = typer.Typer()


@app.command()
def edit(
    task_id: Annotated[int, typer.Argument(help="task ID to edit")],
    title: Annotated[
        str | None, typer.Option("--title", "-t", help="new task title")
    ] = None,
    priority: Annotated[
        str | None, typer.Option("--priority", "-p", help="new priority level")
    ] = None,
) -> None:
    """Edit a task's title or priority."""
    # Check if any edits were specified
    if title is None and priority is None:
        display.warning("no edits were done, specify title or priority")
        raise typer.Exit(EXIT_INVALID_INPUT)

    tasks = load_tasks()

    # Validate task ID (1-indexed)
    if task_id < 1:
        display.error("Task ID must be positive")
        raise typer.Exit(EXIT_INVALID_INPUT)

    if task_id > len(tasks):
        display.error(f"Task {task_id} not found")
        raise typer.Exit(EXIT_INVALID_INPUT)

    task = tasks[task_id - 1]

    # Validate and update title
    if title is not None:
        if not title.strip():
            display.error("Title cannot be empty")
            raise typer.Exit(EXIT_INVALID_INPUT)
        task.title = title.strip()

    # Validate and update priority
    if priority is not None:
        try:
            task.priority = Priority(priority.lower())
        except ValueError:
            display.error(f"Invalid priority: {priority}. Use low, medium, or high")
            raise typer.Exit(EXIT_INVALID_INPUT)

    save_tasks(tasks)

    display.success(f"Updated task {task_id}")
    display.table(tasks)
