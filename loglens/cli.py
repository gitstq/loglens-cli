"""
Command-line interface for LogLens.
Provides both TUI and CLI modes for log analysis.
"""

import sys
import os
import click
from pathlib import Path
from typing import Optional, List
import json

from .parser import LogParser, LogEntry, LogLevel
from .tui import run_tui


@click.group(invoke_without_command=True)
@click.option('--file', '-f', type=click.Path(exists=True), help='Log file to analyze')
@click.option('--follow', '-F', is_flag=True, help='Follow log file for new entries')
@click.option('--tui', '-t', is_flag=True, default=True, help='Launch interactive TUI (default)')
@click.option('--format', 'fmt', type=click.Choice(['auto', 'json', 'logfmt', 'plain']), 
              default='auto', help='Log format')
@click.version_option(version='1.0.0', prog_name='loglens')
@click.pass_context
def main(ctx, file, follow, tui, fmt):
    """
    🎯 LogLens - Smart Terminal Log Analyzer
    
    Analyze and visualize logs with intelligent filtering,
    real-time monitoring, and beautiful terminal UI.
    
    Examples:
        loglens -f app.log              # Analyze log file with TUI
        loglens -f app.log --no-tui     # CLI mode output
        tail -f app.log | loglens       # Pipe mode
        loglens stats -f app.log        # Show statistics
    """
    if ctx.invoked_subcommand is None:
        if file:
            if tui:
                run_tui(log_file=file, follow=follow)
            else:
                # CLI mode
                analyze_cli(file, fmt)
        else:
            # Check if stdin has data
            if not sys.stdin.isatty():
                # Pipe mode
                if tui:
                    run_tui(log_file=sys.stdin, follow=follow)
                else:
                    analyze_stream(sys.stdin, fmt)
            else:
                # No input, show help
                click.echo(ctx.get_help())
                ctx.exit()


@main.command()
@click.option('--file', '-f', required=True, type=click.Path(exists=True), help='Log file')
@click.option('--format', 'fmt', type=click.Choice(['auto', 'json', 'logfmt', 'plain']), 
              default='auto', help='Log format')
def stats(file, fmt):
    """📊 Show log statistics."""
    parser = LogParser()
    
    try:
        with open(file, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        if fmt != 'auto':
            parser.format_type = fmt
        
        entries = parser.parse_lines(lines)
        
        # Calculate statistics
        total = len(entries)
        levels = {}
        for entry in entries:
            levels[entry.level.label] = levels.get(entry.level.label, 0) + 1
        
        # Output
        click.echo(f"\n📄 Log Statistics for: {file}")
        click.echo("=" * 50)
        click.echo(f"Total Entries: {total}")
        click.echo()
        click.echo("By Level:")
        for level, count in sorted(levels.items(), key=lambda x: -x[1]):
            bar = "█" * int(count / max(levels.values()) * 30) if levels else ""
            click.echo(f"  {level:10} {count:6} {bar}")
        
        # Time range
        timestamps = [e.timestamp for e in entries if e.timestamp]
        if timestamps:
            click.echo(f"\nTime Range:")
            click.echo(f"  From: {min(timestamps)}")
            click.echo(f"  To:   {max(timestamps)}")
        
        click.echo()
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--file', '-f', required=True, type=click.Path(exists=True), help='Log file')
@click.option('--level', '-l', type=click.Choice(['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']),
              help='Filter by log level')
@click.option('--search', '-s', help='Search string')
@click.option('--limit', '-n', default=100, help='Limit output lines')
@click.option('--format', 'fmt', type=click.Choice(['auto', 'json', 'logfmt', 'plain']), 
              default='auto', help='Log format')
def filter(file, level, search, limit, fmt):
    """🔍 Filter and display log entries."""
    parser = LogParser()
    
    try:
        with open(file, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        if fmt != 'auto':
            parser.format_type = fmt
        
        entries = parser.parse_lines(lines)
        
        # Apply filters
        filtered = entries
        if level:
            filtered = [e for e in filtered if e.level.label == level]
        if search:
            search_lower = search.lower()
            filtered = [e for e in filtered if search_lower in e.message.lower()]
        
        # Output
        click.echo(f"\n🔍 Filtered Results ({len(filtered)} entries):")
        click.echo("=" * 70)
        
        for entry in filtered[:limit]:
            time_str = entry.formatted_time or ""
            level_str = entry.level.label
            
            color = {
                'DEBUG': 'dim',
                'INFO': 'cyan',
                'WARN': 'yellow',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'FATAL': 'bright_red',
                'CRITICAL': 'bright_red',
            }.get(level_str, '')
            
            prefix = f"[{time_str}] {level_str:8} | " if time_str else f"{level_str:8} | "
            
            click.echo(click.style(prefix, fg=color, dim=(color == 'dim')), nl=False)
            click.echo(entry.message[:200])
        
        if len(filtered) > limit:
            click.echo(f"\n... and {len(filtered) - limit} more entries")
        
        click.echo()
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--file', '-f', required=True, type=click.Path(exists=True), help='Log file')
@click.option('--format', 'fmt', type=click.Choice(['auto', 'json', 'logfmt', 'plain']), 
              default='auto', help='Log format')
def export(file, fmt):
    """📤 Export logs to JSON format."""
    parser = LogParser()
    
    try:
        with open(file, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        if fmt != 'auto':
            parser.format_type = fmt
        
        entries = parser.parse_lines(lines)
        
        output = []
        for entry in entries:
            output.append({
                'line_number': entry.line_number,
                'timestamp': entry.timestamp.isoformat() if entry.timestamp else None,
                'level': entry.level.label,
                'message': entry.message,
                'fields': entry.fields,
            })
        
        click.echo(json.dumps(output, indent=2, ensure_ascii=False))
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


def analyze_cli(file_path: str, fmt: str):
    """Analyze logs in CLI mode."""
    parser = LogParser()
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    if fmt != 'auto':
        parser.format_type = fmt
    
    entries = parser.parse_lines(lines)
    
    click.echo(f"\n📄 Analyzing: {file_path}")
    click.echo(f"Total entries: {len(entries)}\n")
    
    for entry in entries[:50]:
        time_str = entry.formatted_time or ""
        level_str = entry.level.label
        
        color = {
            'DEBUG': 'dim',
            'INFO': 'cyan',
            'WARN': 'yellow',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'FATAL': 'bright_red',
            'CRITICAL': 'bright_red',
        }.get(level_str, '')
        
        prefix = f"[{time_str}] {level_str:8} | " if time_str else f"{level_str:8} | "
        
        click.echo(click.style(prefix, fg=color, dim=(color == 'dim')), nl=False)
        click.echo(entry.message[:150])


def analyze_stream(stream, fmt: str):
    """Analyze logs from stream."""
    parser = LogParser()
    
    lines = stream.readlines()
    
    if fmt != 'auto':
        parser.format_type = fmt
    
    entries = parser.parse_lines(lines)
    
    click.echo(f"Total entries: {len(entries)}\n")
    
    for entry in entries[:50]:
        time_str = entry.formatted_time or ""
        level_str = entry.level.label
        
        color = {
            'DEBUG': 'dim',
            'INFO': 'cyan',
            'WARN': 'yellow',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'FATAL': 'bright_red',
            'CRITICAL': 'bright_red',
        }.get(level_str, '')
        
        prefix = f"[{time_str}] {level_str:8} | " if time_str else f"{level_str:8} | "
        
        click.echo(click.style(prefix, fg=color, dim=(color == 'dim')), nl=False)
        click.echo(entry.message[:150])


if __name__ == '__main__':
    main()
