---
name: adding-cli-command
description: 提供 Typer 模板、处理注册并确保一致性。在添加或修改 CLI 命令时务必使用此 skill。当用户请求添加/创建/实现/构建/编写新命令（例如「添加 edit 命令」「创建 search 功能」）或更新/修改/更改/编辑现有命令时使用。
---

# 添加 CLI 命令

用于添加或更新 Typer CLI 命令的模板与工作流。

`<cli_app>` 指你的 CLI 应用名称（例如 `task`、`myapp`、`todo`）。

## 工作流

1. 确定命令类型（单命令、命令组或破坏性命令）
2. 在 `src/<cli_app>/commands/<command>.py` 中创建文件
3. 使用下方对应模板
4. 在 `src/<cli_app>/commands/__init__.py` 中注册


## 模板 A：单命令

适用于直接接收参数的命令（`<cli_app> add "item"`）。

```python
import typer
from typing import Annotated

from <cli_app>.storage import add_task
from <cli_app>.display import display
from <cli_app>.constants import EXIT_INVALID_INPUT

app = typer.Typer()


@app.command()
def add(
    title: Annotated[str, typer.Argument(help="task title")],
    priority: Annotated[str, typer.Option("--priority", "-p", help="priority level")] = "low",
):
    """Add a new task."""
    if not title.strip():
        display.error("Title cannot be empty")
        raise typer.Exit(EXIT_INVALID_INPUT)

    task = add_task(title=title, priority=priority)
    display.success(f"Added '{task.title}'")
```

## 模板 B：命令组

适用于带子命令的命令（`<cli_app> db migrate`、`<cli_app> db status`）。

```python
import typer

from <cli_app>.storage import storage
from <cli_app>.display import display

app = typer.Typer(help="Database operations.")


@app.command()
def migrate():
    """Run database migrations."""
    storage.migrate()
    display.success("Migrations complete")


@app.command()
def status():
    """Show database status."""
    info = storage.get_status()
    display.info(f"Version: {info.version}")
```

## 模板 C：破坏性命令

适用于带确认步骤的删除操作。

```python
import typer
from typing import Annotated

from <cli_app>.storage import get_task, delete_task
from <cli_app>.display import display
from <cli_app>.constants import EXIT_ERROR

app = typer.Typer()


@app.command()
def clear(
    task_id: Annotated[int, typer.Argument(help="task ID to delete")],
    force: Annotated[bool, typer.Option("--force", "-f", help="skip confirmation")] = False,
):
    """Delete a task permanently."""
    task = get_task(task_id)
    if not task:
        display.error(f"Task {task_id} not found")
        raise typer.Exit(EXIT_ERROR)

    if not force:
        confirm = typer.confirm(f"Delete '{task.title}'?", default=False)
        if not confirm:
            display.info("Cancelled")
            raise typer.Abort()

    delete_task(task_id)
    display.success(f"Deleted '{task.title}'")
```

## 注册

在 `commands/__init__.py` 中注册：

```python
import typer

from .add import app as add_app
from .clear import app as clear_app

app = typer.Typer(help="<cli_app> CLI.", no_args_is_help=True)

# Single commands - add WITHOUT name
app.add_typer(add_app)
app.add_typer(clear_app)

# Command groups - add WITH name
# app.add_typer(db_app, name="db")
```

## 约定

| 规则 | 示例 |
|------|------|
| Arguments | `Annotated[str, typer.Argument(help="...")]` |
| Options | `Annotated[str, typer.Option("--name", "-n", help="...")]` |
| Docstrings | 祈使语气，少于 60 个字符 |
| Output | 始终通过 `display` 模块输出 |
| Exit codes | 0=成功，1=错误，2=无效输入 |
| Destructive | 必须有 `--force` 标志，确认默认值为 `False` |
