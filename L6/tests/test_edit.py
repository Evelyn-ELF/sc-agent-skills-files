"""Tests for the edit command."""

import json

from task.commands import app


class TestEdit:
    """Test suite for edit command."""

    def test_edit_title_only(self, runner, sample_data):
        """Test editing only the title of a task."""
        result = runner.invoke(app, ["edit", "1", "--title", "Updated title"])

        assert result.exit_code == 0
        assert "Updated task 1" in result.output

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].title == "Updated title"
        # Priority should remain unchanged
        assert tasks[0].priority.value == "low"

    def test_edit_priority_only(self, runner, sample_data):
        """Test editing only the priority of a task."""
        result = runner.invoke(app, ["edit", "1", "--priority", "high"])

        assert result.exit_code == 0
        assert "Updated task 1" in result.output

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].priority.value == "high"
        # Title should remain unchanged
        assert tasks[0].title == "First task"

    def test_edit_both_title_and_priority(self, runner, sample_data):
        """Test editing both title and priority at the same time."""
        result = runner.invoke(
            app, ["edit", "1", "--title", "New title", "--priority", "medium"]
        )

        assert result.exit_code == 0
        assert "Updated task 1" in result.output

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].title == "New title"
        assert tasks[0].priority.value == "medium"

    def test_no_options_shows_warning(self, runner, sample_data):
        """Test that no options shows a warning message."""
        result = runner.invoke(app, ["edit", "1"])

        assert result.exit_code == 2
        assert "no edits were done, specify title or priority" in result.output

    def test_invalid_task_id_too_high(self, runner, sample_data):
        """Test that task ID beyond range shows error."""
        result = runner.invoke(app, ["edit", "999", "--title", "New"])

        assert result.exit_code == 2
        assert "Task 999 not found" in result.output

    def test_invalid_task_id_zero(self, runner, sample_data):
        """Test that task ID of 0 shows error."""
        result = runner.invoke(app, ["edit", "0", "--title", "New"])

        assert result.exit_code == 2
        assert "Task ID must be positive" in result.output

    def test_invalid_priority_value(self, runner, sample_data):
        """Test that invalid priority shows error."""
        result = runner.invoke(app, ["edit", "1", "--priority", "urgent"])

        assert result.exit_code == 2
        assert "Invalid priority: urgent" in result.output
        assert "Use low, medium, or high" in result.output

    def test_empty_title_shows_error(self, runner, sample_data):
        """Test that empty title shows error."""
        result = runner.invoke(app, ["edit", "1", "--title", ""])

        assert result.exit_code == 2
        assert "Title cannot be empty" in result.output

    def test_whitespace_only_title_shows_error(self, runner, sample_data):
        """Test that whitespace-only title shows error."""
        result = runner.invoke(app, ["edit", "1", "--title", "   "])

        assert result.exit_code == 2
        assert "Title cannot be empty" in result.output

    def test_short_flag_title(self, runner, sample_data):
        """Test editing title with -t short flag."""
        result = runner.invoke(app, ["edit", "1", "-t", "Short flag title"])

        assert result.exit_code == 0
        assert "Updated task 1" in result.output

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].title == "Short flag title"

    def test_short_flag_priority(self, runner, sample_data):
        """Test editing priority with -p short flag."""
        result = runner.invoke(app, ["edit", "1", "-p", "medium"])

        assert result.exit_code == 0
        assert "Updated task 1" in result.output

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].priority.value == "medium"

    def test_short_flags_both(self, runner, sample_data):
        """Test editing both with short flags."""
        result = runner.invoke(
            app, ["edit", "1", "-t", "Both short", "-p", "high"]
        )

        assert result.exit_code == 0
        assert "Updated task 1" in result.output

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].title == "Both short"
        assert tasks[0].priority.value == "high"

    def test_priority_case_insensitive_upper(self, runner, sample_data):
        """Test that priority is case-insensitive (uppercase)."""
        result = runner.invoke(app, ["edit", "1", "--priority", "HIGH"])

        assert result.exit_code == 0

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].priority.value == "high"

    def test_priority_case_insensitive_mixed(self, runner, sample_data):
        """Test that priority is case-insensitive (mixed case)."""
        result = runner.invoke(app, ["edit", "1", "--priority", "Medium"])

        assert result.exit_code == 0

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].priority.value == "medium"

    def test_title_whitespace_is_stripped(self, runner, sample_data):
        """Test that title whitespace is stripped on edit."""
        result = runner.invoke(app, ["edit", "1", "--title", "  Stripped title  "])

        assert result.exit_code == 0

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].title == "Stripped title"

    def test_edit_last_task(self, runner, sample_data):
        """Test editing the last task in the list (boundary case)."""
        result = runner.invoke(app, ["edit", "2", "--title", "Edited last"])

        assert result.exit_code == 0
        assert "Updated task 2" in result.output

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[1].title == "Edited last"

    def test_edit_preserves_done_status(self, runner, sample_data):
        """Test that editing does not change the done status."""
        # sample_data task 2 is done=True
        result = runner.invoke(app, ["edit", "2", "--title", "Still done"])

        assert result.exit_code == 0

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[1].done is True
        assert tasks[1].title == "Still done"

    def test_edit_preserves_due_date(self, runner, sample_data):
        """Test that editing does not change the due date."""
        # sample_data task 2 has due_date set
        result = runner.invoke(app, ["edit", "2", "--priority", "low"])

        assert result.exit_code == 0

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[1].due_date is not None

    def test_edit_displays_table_after_success(self, runner, sample_data):
        """Test that the task table is displayed after a successful edit."""
        result = runner.invoke(app, ["edit", "1", "--title", "Table test"])

        assert result.exit_code == 0
        # The table should show the updated task
        assert "Table test" in result.output

    def test_edit_on_empty_storage(self, runner, temp_storage):
        """Test editing when no tasks exist."""
        result = runner.invoke(app, ["edit", "1", "--title", "New"])

        assert result.exit_code == 2
        assert "Task 1 not found" in result.output

    def test_edit_does_not_affect_other_tasks(self, runner, sample_data):
        """Test that editing one task does not affect other tasks."""
        result = runner.invoke(app, ["edit", "1", "--title", "Changed"])

        assert result.exit_code == 0

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].title == "Changed"
        # Second task should be unchanged
        assert tasks[1].title == "Second task"
        assert tasks[1].priority.value == "high"
        assert tasks[1].done is True

    def test_edit_priority_low(self, runner, sample_data):
        """Test editing priority to low."""
        result = runner.invoke(app, ["edit", "2", "--priority", "low"])

        assert result.exit_code == 0

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[1].priority.value == "low"

    def test_edit_priority_medium(self, runner, sample_data):
        """Test editing priority to medium."""
        result = runner.invoke(app, ["edit", "1", "--priority", "medium"])

        assert result.exit_code == 0

        from task.storage import load_tasks
        tasks = load_tasks()
        assert tasks[0].priority.value == "medium"
