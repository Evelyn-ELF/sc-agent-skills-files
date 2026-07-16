---
name: generating-cli-tests
description: 为 Typer CLI 命令生成 pytest 测试。包含 fixtures（temp_storage、sample_data）、CliRunner 模式、确认处理（y/n/--force）以及边界情况覆盖。当用户请求「为……编写测试」「测试我的 CLI」「添加测试覆盖」或任何 CLI + 测试相关需求时使用。
---

# 生成 CLI 测试

用于为 Typer CLI 命令生成测试的模式与示例。

## 工作流

1. 确定命令类型（Create/Read/Update/Delete/Bulk）
2. 确保 `conftest.py` 中已有 fixtures
3. 使用下方场景编写测试
4. 运行测试进行验证

## Fixtures（conftest.py）

```python
import json
import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner():
    """CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    """Empty storage for testing."""
    storage_dir = tmp_path / ".task"
    storage_dir.mkdir()
    storage_file = storage_dir / "tasks.json"
    storage_file.write_text(json.dumps({"version": 1, "tasks": []}))
    monkeypatch.setenv("TASK_STORAGE_PATH", str(storage_file))
    return storage_file


@pytest.fixture
def sample_data(temp_storage):
    """Pre-populated storage."""
    data = {
        "version": 1,
        "tasks": [
            {"title": "First task", "done": False, "priority": "low", "created_at": "2025-01-01T10:00:00", "due_date": None},
            {"title": "Second task", "done": True, "priority": "high", "created_at": "2025-01-01T11:00:00", "due_date": None},
        ]
    }
    temp_storage.write_text(json.dumps(data))
    return data
```

## 测试结构（AAA）

```python
def test_<command>_<scenario>(runner, temp_storage):
    # Arrange - via fixtures

    # Act
    result = runner.invoke(app, ["<command>", "<args>"])

    # Assert
    assert result.exit_code == 0
    assert "<expected>" in result.output
```

## CliRunner 用法

```python
from typer.testing import CliRunner
from task.main import app

runner = CliRunner()

# Basic
result = runner.invoke(app, ["add", "New task"])

# With options
result = runner.invoke(app, ["add", "Task", "--priority", "high"])

# With confirmation
result = runner.invoke(app, ["clear", "1"], input="y\n")  # Accept
result = runner.invoke(app, ["clear", "1"], input="n\n")  # Decline

# Skip confirmation
result = runner.invoke(app, ["clear", "1", "--force"])
```

## 按命令类型的测试场景

### Create/Add

```python
class TestAdd:
    def test_adds_task(self, runner, temp_storage):
        result = runner.invoke(app, ["add", "New task"])
        assert result.exit_code == 0
        assert "Added" in result.output

    def test_with_priority(self, runner, temp_storage):
        result = runner.invoke(app, ["add", "Task", "--priority", "high"])
        assert result.exit_code == 0

    def test_empty_title_shows_error(self, runner, temp_storage):
        result = runner.invoke(app, ["add", ""])
        assert result.exit_code == 2
```

### Read/List

```python
class TestList:
    def test_shows_tasks(self, runner, sample_data):
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "First task" in result.output

    def test_empty_state(self, runner, temp_storage):
        result = runner.invoke(app, ["list"])
        assert "No tasks" in result.output or "empty" in result.output.lower()

    def test_with_filter(self, runner, sample_data):
        result = runner.invoke(app, ["list", "--done"])
        assert result.exit_code == 0
```

### Update/Done

```python
class TestDone:
    def test_marks_done(self, runner, sample_data):
        result = runner.invoke(app, ["done", "1"])
        assert result.exit_code == 0

    def test_not_found(self, runner, temp_storage):
        result = runner.invoke(app, ["done", "999"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()
```

### Delete/Clear

```python
class TestClear:
    def test_confirmed(self, runner, sample_data):
        result = runner.invoke(app, ["clear", "1"], input="y\n")
        assert result.exit_code == 0
        assert "Deleted" in result.output

    def test_declined(self, runner, sample_data):
        result = runner.invoke(app, ["clear", "1"], input="n\n")
        assert "Cancelled" in result.output

    def test_force(self, runner, sample_data):
        result = runner.invoke(app, ["clear", "1", "--force"])
        assert result.exit_code == 0

    def test_not_found(self, runner, temp_storage):
        result = runner.invoke(app, ["clear", "999", "--force"])
        assert result.exit_code == 1
```

## 需覆盖的边界情况

| 类别 | 测试用例 |
|----------|------------|
| Invalid Input | 空字符串、错误类型、超出范围 |
| Not Found | ID 不存在 |
| Boundary | 零、负数、首项/末项 |
| State | 已完成、空存储 |
| Confirmation | 接受（y）、拒绝（n）、force 标志 |

## 检查清单

- [ ] 测试文件：`tests/test_<command>.py`
- [ ] Fixtures 位于 `conftest.py`
- [ ] 使用 `typer.testing` 中的 `CliRunner`
- [ ] AAA 结构（Arrange、Act、Assert）
- [ ] 测试退出码：0、1、2
- [ ] 破坏性命令：测试 y/n 和 `--force`
- [ ] 输出断言检查预期消息

## 运行测试

```bash
uv run pytest                       # All tests
uv run pytest -v                    # Verbose
uv run pytest tests/test_add.py    # Specific file
```
