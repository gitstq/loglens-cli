"""
Log parser module - handles multiple log formats automatically.
Supports JSON, logfmt, and plain text logs.
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class LogLevel(Enum):
    """Standard log levels with priority ordering."""
    DEBUG = ("DEBUG", 0, "dim")
    INFO = ("INFO", 1, "cyan")
    WARN = ("WARN", 2, "yellow")
    WARNING = ("WARNING", 2, "yellow")
    ERROR = ("ERROR", 3, "red")
    FATAL = ("FATAL", 4, "bright_red")
    CRITICAL = ("CRITICAL", 4, "bright_red")
    PANIC = ("PANIC", 5, "bright_red")
    TRACE = ("TRACE", -1, "dim")

    def __init__(self, label: str, priority: int, color: str):
        self.label = label
        self.priority = priority
        self.color = color

    @classmethod
    def from_string(cls, level_str: str) -> "LogLevel":
        """Parse log level from string."""
        level_upper = level_str.upper()
        for level in cls:
            if level.label == level_upper:
                return level
        return cls.INFO


@dataclass
class LogEntry:
    """Represents a single parsed log entry."""
    raw_line: str
    timestamp: Optional[datetime] = None
    level: LogLevel = LogLevel.INFO
    message: str = ""
    fields: Dict[str, Any] = None
    source: str = ""
    line_number: int = 0

    def __post_init__(self):
        if self.fields is None:
            self.fields = {}

    @property
    def formatted_time(self) -> str:
        """Format timestamp for display."""
        if self.timestamp:
            return self.timestamp.strftime("%H:%M:%S")
        return ""

    @property
    def level_icon(self) -> str:
        """Get icon for log level."""
        icons = {
            LogLevel.DEBUG: "🔍",
            LogLevel.INFO: "ℹ️ ",
            LogLevel.WARN: "⚠️ ",
            LogLevel.WARNING: "⚠️ ",
            LogLevel.ERROR: "❌",
            LogLevel.FATAL: "💥",
            LogLevel.CRITICAL: "💥",
            LogLevel.PANIC: "🔥",
            LogLevel.TRACE: "📋",
        }
        return icons.get(self.level, "•")


class LogParser:
    """Intelligent log parser that auto-detects format."""

    # Common timestamp patterns
    TIMESTAMP_PATTERNS = [
        # ISO 8601 with space: 2024-01-15 10:30:00
        (r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', '%Y-%m-%d %H:%M:%S'),
        # ISO 8601: 2024-01-15T10:30:00.123Z
        (r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)', '%Y-%m-%dT%H:%M:%S'),
        # Common: Jan 15 10:30:00
        (r'([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', '%b %d %H:%M:%S'),
        # Unix timestamp: 1705315800
        (r'(\d{10,13})', 'unix'),
    ]

    # Log level patterns
    LEVEL_PATTERN = re.compile(
        r'\b(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL|PANIC|TRACE)\b',
        re.IGNORECASE
    )

    def __init__(self):
        self.format_type: Optional[str] = None
        self.sample_lines: list = []

    def detect_format(self, lines: list) -> str:
        """Auto-detect log format from sample lines."""
        if not lines:
            return "plain"

        json_count = 0
        logfmt_count = 0

        for line in lines[:10]:
            line = line.strip()
            if not line:
                continue

            # Try JSON
            try:
                json.loads(line)
                json_count += 1
                continue
            except json.JSONDecodeError:
                pass

            # Try logfmt (key=value pairs)
            if re.search(r'\w+=[^\s]+', line):
                logfmt_count += 1

        if json_count >= len([l for l in lines[:10] if l.strip()]) * 0.5:
            return "json"
        elif logfmt_count >= len([l for l in lines[:10] if l.strip()]) * 0.5:
            return "logfmt"
        return "plain"

    def parse_timestamp(self, line: str) -> Tuple[Optional[datetime], str]:
        """Extract timestamp from log line."""
        for pattern, fmt in self.TIMESTAMP_PATTERNS:
            match = re.search(pattern, line)
            if match:
                ts_str = match.group(1)
                try:
                    if fmt == 'unix':
                        ts = datetime.fromtimestamp(int(ts_str[:10]))
                    else:
                        # Try with milliseconds
                        if '.' in ts_str and 'Z' not in ts_str:
                            ts_str = ts_str.split('.')[0]
                        ts = datetime.strptime(ts_str[:19], fmt)
                    return ts, line[:match.start()] + line[match.end():]
                except (ValueError, OSError):
                    continue
        return None, line

    def parse_level(self, line: str) -> Tuple[LogLevel, str]:
        """Extract log level from line."""
        match = self.LEVEL_PATTERN.search(line)
        if match:
            level = LogLevel.from_string(match.group(1))
            # Remove level from line for cleaner message
            cleaned = line[:match.start()] + line[match.end():]
            return level, cleaned.strip()
        return LogLevel.INFO, line

    def parse_json_line(self, line: str) -> LogEntry:
        """Parse a JSON formatted log line."""
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            return self.parse_plain_line(line)

        entry = LogEntry(raw_line=line, fields=data)

        # Extract timestamp
        for key in ['timestamp', 'time', 'ts', '@timestamp', 'datetime', 'date']:
            if key in data:
                ts_val = data[key]
                if isinstance(ts_val, (int, float)):
                    entry.timestamp = datetime.fromtimestamp(int(ts_val))
                elif isinstance(ts_val, str):
                    entry.timestamp, _ = self.parse_timestamp(ts_val)[0], None
                    if entry.timestamp is None:
                        try:
                            entry.timestamp = datetime.fromisoformat(ts_val.replace('Z', '+00:00'))
                        except ValueError:
                            pass
                break

        # Extract level
        for key in ['level', 'loglevel', 'severity', 'log_level', 'lvl']:
            if key in data:
                entry.level = LogLevel.from_string(str(data[key]))
                break

        # Extract message
        for key in ['message', 'msg', 'text', 'log', 'content', 'body']:
            if key in data:
                entry.message = str(data[key])
                break

        # If no message field, use the whole JSON
        if not entry.message:
            entry.message = line[:200]

        return entry

    def parse_logfmt_line(self, line: str) -> LogEntry:
        """Parse a logfmt formatted line (key=value pairs)."""
        entry = LogEntry(raw_line=line)
        fields = {}

        # Parse key=value pairs
        pattern = r'(\w+)=("(?:[^"\\]|\\.)*"|\S+)'
        for match in re.finditer(pattern, line):
            key = match.group(1)
            value = match.group(2)
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            fields[key] = value

        entry.fields = fields

        # Extract timestamp, level, message
        entry.timestamp, _ = self.parse_timestamp(line)

        if 'level' in fields:
            entry.level = LogLevel.from_string(fields['level'])
        else:
            entry.level, _ = self.parse_level(line)

        entry.message = fields.get('message', fields.get('msg', line))

        return entry

    def parse_plain_line(self, line: str) -> LogEntry:
        """Parse a plain text log line."""
        entry = LogEntry(raw_line=line)

        # Try to extract timestamp
        entry.timestamp, cleaned = self.parse_timestamp(line)
        if cleaned:
            line = cleaned

        # Try to extract level
        entry.level, line = self.parse_level(line)

        # Clean up common prefixes
        line = re.sub(r'^\s*[\[\(]?[^\]\)]*[\]\)]?\s*', '', line)
        line = line.strip(':-| ')

        entry.message = line[:500] if line else entry.raw_line[:500]

        return entry

    def parse_line(self, line: str, line_number: int = 0) -> LogEntry:
        """Parse a single log line with auto-format detection."""
        line = line.rstrip('\n\r')

        if self.format_type == "json":
            entry = self.parse_json_line(line)
        elif self.format_type == "logfmt":
            entry = self.parse_logfmt_line(line)
        else:
            entry = self.parse_plain_line(line)

        entry.line_number = line_number
        return entry

    def parse_lines(self, lines: list, line_offset: int = 0) -> list:
        """Parse multiple lines."""
        if self.format_type is None and lines:
            self.format_type = self.detect_format(lines)

        entries = []
        for i, line in enumerate(lines):
            if line.strip():
                entry = self.parse_line(line, line_offset + i + 1)
                entries.append(entry)

        return entries
