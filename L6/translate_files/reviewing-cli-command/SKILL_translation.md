---
name: reviewing-cli-command
description: 提供用于审查 Typer CLI 命令实现的检查清单。涵盖结构、Annotated 语法、错误处理、退出码、display 模块用法、破坏性操作模式以及帮助文本约定。当用户请求审查/检查/验证 CLI 命令、希望获得实现反馈，或询问命令是否遵循最佳实践时使用。
---

# 审查 CLI 命令

用于审查 Typer CLI 命令实现的检查清单。

## 审查流程

1. 阅读命令文件
2. 逐项检查下方各节
3. 使用底部输出格式报告发现

## 结构

- [ ] 文件位于 `src/<cli_app>/commands/`
- [ ] 包含 `app = typer.Typer()` 和 `@app.command()`
- [ ] 命令组为每个子命令使用 `@app.command()`
- [ ] 在 `commands/__init__.py` 中通过 `add_typer()` 注册
- [ ] 单命令：`add_typer(app)`，不带 name
- [ ] 命令组：`add_typer(app, name="group")`

## 参数与选项

- [ ] 使用 `Annotated` 语法
- [ ] Arguments 用于必填的位置参数
- [ ] Options 用于可选的命名参数
- [ ] 在合适处使用短标志（`-f`、`-q`）
- [ ] 帮助文本：小写、无句号、简洁

```python
# GOOD:
name: Annotated[str, typer.Argument(help="item name")]
force: Annotated[bool, typer.Option("--force", "-f", help="skip confirmation")] = False

# BAD:
name: str = typer.Argument(..., help="The name of the item.")
```

## 错误处理

- [ ] 在处理前验证输入
- [ ] 退出码：0=成功，1=错误，2=无效输入
- [ ] 通过 `display.error()` 输出错误
- [ ] 错误后使用 `raise typer.Exit(code)`
- [ ] 取消时使用 `raise typer.Abort()`

```python
# GOOD:
if id < 1:
    display.error("ID must be positive")
    raise typer.Exit(EXIT_INVALID_INPUT)

# BAD:
if id < 1:
    print("Error: ID must be positive")
    return
```

## 输出

- [ ] 所有输出通过 `display` 模块
- [ ] 不使用 `print()`、`typer.echo()` 或 `console.print()`

```python
# GOOD:
display.success(f"Added '{task.title}'")

# BAD:
print(f"Added '{task.title}'")
```

## 破坏性操作

- [ ] 具有 `--force` / `-f` 标志
- [ ] `typer.confirm()` 使用 `default=False`
- [ ] 中止时显示 "Cancelled"

```python
# GOOD:
if not force:
    confirm = typer.confirm(f"Delete '{task.title}'?", default=False)
    if not confirm:
        display.info("Cancelled")
        raise typer.Abort()

# BAD: defaults to Yes
confirm = typer.confirm(f"Delete?", default=True)
```

## 帮助文本

- [ ] 存在 docstring
- [ ] 祈使语气（"Add a task" 而非 "Adds a task"）
- [ ] 首行少于 60 个字符

## 常见错误

| 错误 | 修复 |
|---------|-----|
| `print()` | `display.success/error/warning/info()` |
| 错误的退出码 | 0=成功，1=错误，2=无效 |
| 删除操作缺少 `--force` | 添加默认值为 False 的 force 选项 |
| 确认默认选 Yes | 在 `typer.confirm()` 中使用 `default=False` |
| 旧版 Typer 语法 | `Annotated[type, typer.Argument()]` |
| 缺少 `app = typer.Typer()` | 每个命令文件需要自己的 app |
| 未注册 | 在 `commands/__init__.py` 中调用 `add_typer(app)` |

## 审查输出格式

```
## Review: <command_name>

[OK] Uses Annotated syntax
[OK] Has docstring in imperative mood
[X] Missing --force flag on destructive command
[X] Uses print() instead of display module
[!] Help text could be shorter

### Summary
<brief summary of issues found>

### Suggested Fixes
<code suggestions if needed>
```
