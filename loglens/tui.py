"""
Interactive TUI for LogLens using Textual.
Provides real-time log viewing with filtering and analysis.
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import (
    DataTable, Input, Static, Header, Footer, 
    Log, Label, Button, ProgressBar, Checkbox
)
from textual.binding import Binding
from textual.reactive import reactive
from textual.color import Color
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax
import asyncio
from typing import List, Optional, Callable
from datetime import datetime

from .parser import LogParser, LogEntry, LogLevel


class LogLine(Static):
    """Widget to display a single log line with formatting."""
    
    def __init__(self, entry: LogEntry, **kwargs):
        self.entry = entry
        super().__init__(**kwargs)
    
    def render(self) -> Text:
        """Render the log entry with rich formatting."""
        parts = []
        
        # Timestamp
        if self.entry.formatted_time:
            parts.append((f"[{self.entry.formatted_time}] ", "dim"))
        
        # Level with color
        level_str = f"{self.entry.level.label:8}"
        parts.append((level_str, self.entry.level.color))
        parts.append((" | ", "dim"))
        
        # Message
        msg = self.entry.message[:200]
        if len(self.entry.message) > 200:
            msg += "..."
        parts.append((msg, ""))
        
        # Build text
        text = Text()
        for content, style in parts:
            text.append(content, style=style)
        
        return text


class StatsPanel(Static):
    """Panel showing log statistics."""
    
    total_logs = reactive(0)
    error_count = reactive(0)
    warn_count = reactive(0)
    info_count = reactive(0)
    debug_count = reactive(0)
    
    def compose(self) -> ComposeResult:
        with Container():
            yield Label("📊 Log Statistics", classes="stats-title")
            yield Label("Total: 0", id="total-label")
            yield Label("❌ Errors: 0", id="error-label")
            yield Label("⚠️  Warnings: 0", id="warn-label")
            yield Label("ℹ️  Info: 0", id="info-label")
            yield Label("🔍 Debug: 0", id="debug-label")
    
    def watch_total_logs(self, value: int):
        label = self.query_one("#total-label", Label)
        label.update(f"📄 Total: {value}")
    
    def watch_error_count(self, value: int):
        label = self.query_one("#error-label", Label)
        label.update(f"❌ Errors: {value}")
        if value > 0:
            label.styles.color = "red"
    
    def watch_warn_count(self, value: int):
        label = self.query_one("#warn-label", Label)
        label.update(f"⚠️  Warnings: {value}")
        if value > 0:
            label.styles.color = "yellow"
    
    def watch_info_count(self, value: int):
        label = self.query_one("#info-label", Label)
        label.update(f"ℹ️  Info: {value}")
    
    def watch_debug_count(self, value: int):
        label = self.query_one("#debug-label", Label)
        label.update(f"🔍 Debug: {value}")


class FilterBar(Container):
    """Filter input bar."""
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Input(placeholder="🔍 Filter logs... (press / to focus)", id="filter-input")
            yield Button("❌ Clear", id="clear-filter", variant="error")
    
    def on_mount(self):
        self.query_one("#filter-input", Input).focus()


class LogTable(DataTable):
    """Table widget for displaying logs."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entries: List[LogEntry] = []
        self.filtered_entries: List[LogEntry] = []
        self.parser = LogParser()
    
    def on_mount(self):
        self.add_columns("Time", "Level", "Message")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.styles.height = "100%"
    
    def add_log_entry(self, entry: LogEntry):
        """Add a single log entry to the table."""
        self.entries.append(entry)
        
        time_str = entry.formatted_time or "--:--:--"
        level_str = entry.level.label
        message = entry.message[:100]
        if len(entry.message) > 100:
            message += "..."
        
        # Style based on level
        style = entry.level.color
        
        self.add_row(
            time_str,
            level_str,
            message,
            key=str(entry.line_number),
        )
    
    def filter_logs(self, query: str):
        """Filter logs by query string."""
        if not query:
            self.filtered_entries = self.entries[:]
        else:
            query_lower = query.lower()
            self.filtered_entries = [
                e for e in self.entries
                if query_lower in e.message.lower()
                or query_lower in e.level.label.lower()
                or any(query_lower in str(v).lower() for v in (e.fields or {}).values())
            ]
        
        self.clear()
        for entry in self.filtered_entries[-1000:]:  # Show last 1000
            time_str = entry.formatted_time or "--:--:--"
            level_str = entry.level.label
            message = entry.message[:100]
            if len(entry.message) > 100:
                message += "..."
            
            self.add_row(
                time_str,
                level_str,
                message,
                key=str(entry.line_number),
            )
    
    def clear_logs(self):
        """Clear all logs."""
        self.entries.clear()
        self.filtered_entries.clear()
        self.clear()


class LogLensApp(App):
    """Main LogLens TUI Application."""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    #main-container {
        width: 100%;
        height: 100%;
    }
    
    #left-panel {
        width: 20%;
        height: 100%;
        border: solid green;
        padding: 1;
    }
    
    #right-panel {
        width: 80%;
        height: 100%;
        border: solid blue;
    }
    
    #stats-panel {
        height: 40%;
        border: solid yellow;
        padding: 1;
    }
    
    #log-table {
        height: 85%;
        border: solid $primary;
    }
    
    #filter-bar {
        height: 15%;
        border: solid $secondary;
        padding: 1;
    }
    
    #filter-input {
        width: 80%;
    }
    
    #clear-filter {
        width: 20%;
    }
    
    .stats-title {
        text-align: center;
        text-style: bold;
        color: $primary;
    }
    
    DataTable {
        border: solid $primary;
    }
    
    DataTable > .datatable--cursor {
        background: $primary-darken-2;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("ctrl+c", "quit", "Quit"),
        Binding("f", "focus_filter", "Focus Filter"),
        Binding("c", "clear_logs", "Clear"),
        Binding("r", "refresh", "Refresh"),
        Binding("e", "filter_errors", "Errors Only"),
        Binding("w", "filter_warnings", "Warnings+"),
        Binding("?", "help", "Help"),
    ]
    
    def __init__(self, log_source=None, follow_mode=False, **kwargs):
        self.log_source = log_source
        self.follow_mode = follow_mode
        self.parser = LogParser()
        self.entries: List[LogEntry] = []
        self.filter_query = ""
        super().__init__(**kwargs)
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Horizontal(id="main-container"):
            with Vertical(id="left-panel"):
                yield StatsPanel(id="stats-panel")
            
            with Vertical(id="right-panel"):
                with Container(id="filter-bar"):
                    with Horizontal():
                        yield Input(
                            placeholder="🔍 Type to filter logs...",
                            id="filter-input"
                        )
                        yield Button("❌ Clear", id="clear-btn", variant="error")
                
                yield LogTable(id="log-table")
        
        yield Footer()
    
    def on_mount(self):
        """Called when app is mounted."""
        self.title = "🎯 LogLens - Smart Log Viewer"
        self.sub_title = "Ready"
        
        if self.log_source:
            self.load_logs(self.log_source)
        
        if self.follow_mode:
            self.set_interval(1, self.poll_new_logs)
    
    def load_logs(self, source):
        """Load logs from file or stream."""
        table = self.query_one("#log-table", LogTable)
        stats = self.query_one("#stats-panel", StatsPanel)
        
        try:
            if hasattr(source, 'readlines'):
                lines = source.readlines()
            else:
                with open(source, 'r', encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()
            
            entries = self.parser.parse_lines(lines)
            
            for entry in entries:
                table.add_log_entry(entry)
                self.entries.append(entry)
            
            self.update_stats()
            self.sub_title = f"Loaded {len(entries)} entries"
            
        except Exception as e:
            self.sub_title = f"Error: {e}"
    
    def update_stats(self):
        """Update statistics panel."""
        stats = self.query_one("#stats-panel", StatsPanel)
        
        entries = self.entries
        if self.filter_query:
            entries = [
                e for e in entries
                if self.filter_query.lower() in e.message.lower()
            ]
        
        stats.total_logs = len(entries)
        stats.error_count = sum(1 for e in entries if e.level.priority >= 3)
        stats.warn_count = sum(1 for e in entries if e.level in (LogLevel.WARN, LogLevel.WARNING))
        stats.info_count = sum(1 for e in entries if e.level == LogLevel.INFO)
        stats.debug_count = sum(1 for e in entries if e.level == LogLevel.DEBUG)
    
    def on_input_changed(self, event: Input.Changed):
        """Handle filter input changes."""
        if event.input.id == "filter-input":
            self.filter_query = event.value
            table = self.query_one("#log-table", LogTable)
            table.filter_logs(self.filter_query)
            self.update_stats()
    
    def on_button_pressed(self, event: Button.Pressed):
        """Handle button presses."""
        if event.button.id == "clear-btn":
            self.action_clear_logs()
    
    def action_focus_filter(self):
        """Focus the filter input."""
        self.query_one("#filter-input", Input).focus()
    
    def action_clear_logs(self):
        """Clear all logs."""
        table = self.query_one("#log-table", LogTable)
        table.clear_logs()
        self.entries.clear()
        self.update_stats()
        self.sub_title = "Cleared"
    
    def action_refresh(self):
        """Refresh logs."""
        if self.log_source:
            self.load_logs(self.log_source)
    
    def action_filter_errors(self):
        """Show only errors."""
        inp = self.query_one("#filter-input", Input)
        inp.value = "ERROR"
        self.filter_query = "ERROR"
        table = self.query_one("#log-table", LogTable)
        table.filter_logs("ERROR")
        self.update_stats()
    
    def action_filter_warnings(self):
        """Show warnings and errors."""
        inp = self.query_one("#filter-input", Input)
        inp.value = "WARN"
        self.filter_query = "WARN"
        table = self.query_one("#log-table", LogTable)
        table.filter_logs("WARN")
        self.update_stats()
    
    def action_help(self):
        """Show help."""
        self.notify(
            "Shortcuts:\n"
            "q/Ctrl+C - Quit\n"
            "f - Focus filter\n"
            "c - Clear logs\n"
            "r - Refresh\n"
            "e - Errors only\n"
            "w - Warnings+\n"
            "? - This help",
            title="⌨️ Keyboard Shortcuts",
            timeout=10
        )
    
    def poll_new_logs(self):
        """Poll for new logs in follow mode."""
        # Placeholder for follow mode implementation
        pass


def run_tui(log_file=None, follow=False):
    """Run the LogLens TUI application."""
    app = LogLensApp(log_source=log_file, follow_mode=follow)
    app.run()
