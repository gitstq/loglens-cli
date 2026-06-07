"""
Unit tests for LogLens parser module.
"""

import pytest
from datetime import datetime
from loglens.parser import LogParser, LogEntry, LogLevel


class TestLogLevel:
    """Test LogLevel enum."""
    
    def test_from_string(self):
        assert LogLevel.from_string("ERROR") == LogLevel.ERROR
        assert LogLevel.from_string("error") == LogLevel.ERROR
        assert LogLevel.from_string("INFO") == LogLevel.INFO
        assert LogLevel.from_string("unknown") == LogLevel.INFO
    
    def test_level_properties(self):
        assert LogLevel.ERROR.priority == 3
        assert LogLevel.ERROR.color == "red"
        assert LogLevel.DEBUG.priority == 0


class TestLogParser:
    """Test LogParser functionality."""
    
    @pytest.fixture
    def parser(self):
        return LogParser()
    
    def test_detect_json_format(self, parser):
        lines = [
            '{"level": "info", "message": "test"}',
            '{"level": "error", "message": "fail"}',
        ]
        assert parser.detect_format(lines) == "json"
    
    def test_detect_logfmt_format(self, parser):
        lines = [
            'level=info msg="test"',
            'level=error msg="fail"',
        ]
        assert parser.detect_format(lines) == "logfmt"
    
    def test_detect_plain_format(self, parser):
        lines = [
            'This is a plain log line',
            'Another plain line',
        ]
        assert parser.detect_format(lines) == "plain"
    
    def test_parse_json_line(self, parser):
        line = '{"timestamp": "2024-01-15T10:30:00Z", "level": "ERROR", "message": "Something failed"}'
        entry = parser.parse_json_line(line)
        
        assert entry.level == LogLevel.ERROR
        assert entry.message == "Something failed"
        assert entry.timestamp is not None
    
    def test_parse_logfmt_line(self, parser):
        line = 'level=WARN msg="Disk space low" ts=2024-01-15T10:30:00Z'
        entry = parser.parse_logfmt_line(line)
        
        assert entry.level == LogLevel.WARN
        assert "Disk space low" in entry.message
    
    def test_parse_plain_line(self, parser):
        line = "2024-01-15 10:30:00 ERROR Something went wrong"
        entry = parser.parse_plain_line(line)
        
        assert entry.level == LogLevel.ERROR
        assert "Something went wrong" in entry.message
        assert entry.timestamp is not None
    
    def test_parse_line_with_level_detection(self, parser):
        line = "INFO Application started successfully"
        entry = parser.parse_plain_line(line)
        
        assert entry.level == LogLevel.INFO
    
    def test_parse_lines_batch(self, parser):
        lines = [
            '{"level": "info", "message": "msg1"}',
            '{"level": "error", "message": "msg2"}',
            '',  # Empty line should be skipped
            '{"level": "warn", "message": "msg3"}',
        ]
        entries = parser.parse_lines(lines)
        
        assert len(entries) == 3
        assert entries[0].level == LogLevel.INFO
        assert entries[1].level == LogLevel.ERROR
        assert entries[2].level == LogLevel.WARN


class TestLogEntry:
    """Test LogEntry dataclass."""
    
    def test_formatted_time(self):
        entry = LogEntry(
            raw_line="test",
            timestamp=datetime(2024, 1, 15, 10, 30, 0)
        )
        assert entry.formatted_time == "10:30:00"
    
    def test_formatted_time_none(self):
        entry = LogEntry(raw_line="test")
        assert entry.formatted_time == ""
    
    def test_level_icon(self):
        entry = LogEntry(raw_line="test", level=LogLevel.ERROR)
        assert entry.level_icon == "❌"
        
        entry = LogEntry(raw_line="test", level=LogLevel.INFO)
        assert entry.level_icon == "ℹ️ "
