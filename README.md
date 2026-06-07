# 🎯 LogLens-CLI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License MIT">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square" alt="Platform">
</p>

<p align="center">
  <b>A lightweight, intelligent terminal log analyzer with interactive TUI</b><br>
  <i>Parse JSON, logfmt, and plain text logs with real-time filtering and beautiful visualization</i>
</p>

---

## 🌍 Language Switch

- [English](#english)
- [简体中文](#simplified-chinese)
- [繁體中文](#traditional-chinese)

---

<a id="english"></a>
## English

### 🎉 Introduction

LogLens-CLI is a **smart terminal log viewer** designed for developers who need to quickly analyze and understand log files. Unlike traditional log viewers that require complex configuration, LogLens works **out of the box** with zero setup.

**Key differentiators:**
- 🧠 **Intelligent Format Detection** - Auto-detects JSON, logfmt, and plain text formats
- ⚡ **Lightning Fast** - Written in Python with optimized parsing algorithms
- 🎨 **Beautiful TUI** - Interactive terminal interface with syntax highlighting
- 🔍 **Smart Filtering** - Real-time search across all log fields
- 📊 **Instant Statistics** - Error/warning/info breakdown at a glance

**Inspiration:** Born from the frustration of juggling multiple tools (`jq`, `grep`, `awk`, `less`) just to understand what's happening in application logs.

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📁 **Multi-Format Support** | JSON, logfmt, and plain text logs - all handled automatically |
| 🎛️ **Interactive TUI** | Full-screen terminal UI with keyboard navigation |
| 🔎 **Real-Time Filtering** | Filter by level, message content, or any field |
| 📈 **Live Statistics** | Error/warning/info counts with visual bar charts |
| 🌈 **Syntax Highlighting** | Color-coded log levels for instant visual recognition |
| 📤 **Export to JSON** | Convert any log format to structured JSON |
| 🔄 **Pipe Support** | Works with `tail -f`, `kubectl logs`, `docker logs` |
| ⌨️ **Vim-Style Keys** | Familiar navigation for terminal power users |

### 🚀 Quick Start

#### Requirements
- Python 3.8 or higher
- pip package manager

#### Installation

```bash
# Install from PyPI (coming soon)
pip install loglens-cli

# Or install from source
git clone https://github.com/gitstq/loglens-cli.git
cd loglens-cli
pip install -e .
```

#### Basic Usage

```bash
# Launch TUI with a log file
loglens -f app.log

# Show statistics
loglens stats -f app.log

# Filter errors only
loglens filter -f app.log --level ERROR

# Search for specific text
loglens filter -f app.log --search "database"

# Pipe from other commands
tail -f app.log | loglens
kubectl logs -f my-pod | loglens
```

#### Keyboard Shortcuts (TUI Mode)

| Key | Action |
|-----|--------|
| `q` / `Ctrl+C` | Quit |
| `f` | Focus filter input |
| `c` | Clear all logs |
| `r` | Refresh |
| `e` | Show errors only |
| `w` | Show warnings and errors |
| `?` | Show help |

### 📖 Detailed Usage Guide

#### Supported Log Formats

**JSON Logs:**
```json
{"timestamp": "2024-01-15T10:30:00Z", "level": "ERROR", "message": "Connection failed", "service": "api"}
```

**Logfmt Logs:**
```
time=2024-01-15T10:30:00Z level=info msg="Request processed" duration=45ms
```

**Plain Text Logs:**
```
2024-01-15 10:30:00 INFO Application started successfully
```

#### CLI Commands

```bash
# Statistics overview
loglens stats -f /var/log/app.log

# Filter with multiple criteria
loglens filter -f app.log --level ERROR --search "timeout" --limit 50

# Export to JSON for further processing
loglens export -f app.log > output.json
```

### 💡 Design Philosophy

**Why LogLens?**

Modern applications generate massive amounts of structured logs, but most developers still rely on primitive tools like `grep` and `tail`. Existing solutions like ELK stack or Grafana Loki are powerful but require significant infrastructure investment.

LogLens fills the gap by providing:
- **Zero-configuration** log analysis
- **Terminal-native** workflow (no browser needed)
- **Instant startup** (no Docker, no services)
- **Universal format support** (works with any logging framework)

**Future Roadmap:**
- [ ] Log pattern clustering and anomaly detection
- [ ] Integration with popular log aggregation services
- [ ] Custom color themes and formatting rules
- [ ] Log comparison and diff view
- [ ] Performance metrics extraction

### 📦 Packaging & Deployment

```bash
# Build distribution
make build

# Install locally
pip install dist/loglens-cli-*.whl

# Run tests
make test

# Format code
make format
```

### 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

**Commit Message Convention:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test changes

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a id="simplified-chinese"></a>
## 简体中文

### 🎉 项目介绍

LogLens-CLI 是一款**智能终端日志分析器**，专为需要快速分析和理解日志文件的开发者设计。与传统需要复杂配置的日志查看器不同，LogLens **开箱即用**，零配置即可工作。

**核心差异化亮点：**
- 🧠 **智能格式识别** - 自动识别 JSON、logfmt 和普通文本格式
- ⚡ **极速解析** - 基于 Python 编写，采用优化的解析算法
- 🎨 **精美 TUI** - 交互式终端界面，支持语法高亮
- 🔍 **智能过滤** - 跨所有日志字段的实时搜索
- 📊 **即时统计** - 错误/警告/信息一目了然

**灵感来源：** 源于开发者在使用 `jq`、`grep`、`awk`、`less` 等多个工具来理解应用日志时的挫败感。

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📁 **多格式支持** | JSON、logfmt、纯文本日志 - 全部自动处理 |
| 🎛️ **交互式 TUI** | 全屏终端界面，支持键盘导航 |
| 🔎 **实时过滤** | 按级别、消息内容或任意字段过滤 |
| 📈 **实时统计** | 错误/警告/信息计数，带可视化条形图 |
| 🌈 **语法高亮** | 颜色编码的日志级别，即时视觉识别 |
| 📤 **导出 JSON** | 将任意日志格式转换为结构化 JSON |
| 🔄 **管道支持** | 与 `tail -f`、`kubectl logs`、`docker logs` 配合使用 |
| ⌨️ **Vim 风格按键** | 终端高级用户熟悉的导航方式 |

### 🚀 快速开始

#### 环境要求
- Python 3.8 或更高版本
- pip 包管理器

#### 安装

```bash
# 从 PyPI 安装（即将推出）
pip install loglens-cli

# 或从源码安装
git clone https://github.com/gitstq/loglens-cli.git
cd loglens-cli
pip install -e .
```

#### 基本用法

```bash
# 使用 TUI 打开日志文件
loglens -f app.log

# 显示统计信息
loglens stats -f app.log

# 仅过滤错误
loglens filter -f app.log --level ERROR

# 搜索特定文本
loglens filter -f app.log --search "database"

# 从其他命令管道输入
tail -f app.log | loglens
kubectl logs -f my-pod | loglens
```

#### 键盘快捷键（TUI 模式）

| 按键 | 操作 |
|------|------|
| `q` / `Ctrl+C` | 退出 |
| `f` | 聚焦过滤输入框 |
| `c` | 清除所有日志 |
| `r` | 刷新 |
| `e` | 仅显示错误 |
| `w` | 显示警告和错误 |
| `?` | 显示帮助 |

### 📖 详细使用指南

#### 支持的日志格式

**JSON 日志：**
```json
{"timestamp": "2024-01-15T10:30:00Z", "level": "ERROR", "message": "Connection failed", "service": "api"}
```

**Logfmt 日志：**
```
time=2024-01-15T10:30:00Z level=info msg="Request processed" duration=45ms
```

**纯文本日志：**
```
2024-01-15 10:30:00 INFO Application started successfully
```

#### CLI 命令

```bash
# 统计概览
loglens stats -f /var/log/app.log

# 多条件过滤
loglens filter -f app.log --level ERROR --search "timeout" --limit 50

# 导出为 JSON 以便进一步处理
loglens export -f app.log > output.json
```

### 💡 设计思路与迭代规划

**为什么选择 LogLens？**

现代应用生成大量结构化日志，但大多数开发者仍然依赖 `grep` 和 `tail` 等原始工具。ELK 堆栈或 Grafana Loki 等现有解决方案功能强大，但需要大量的基础设施投入。

LogLens 填补了空白，提供：
- **零配置**日志分析
- **终端原生**工作流（无需浏览器）
- **即时启动**（无需 Docker，无需服务）
- **通用格式支持**（适用于任何日志框架）

**后续迭代计划：**
- [ ] 日志模式聚类和异常检测
- [ ] 与主流日志聚合服务集成
- [ ] 自定义颜色主题和格式化规则
- [ ] 日志对比和差异视图
- [ ] 性能指标提取

### 📦 打包与部署

```bash
# 构建分发包
make build

# 本地安装
pip install dist/loglens-cli-*.whl

# 运行测试
make test

# 格式化代码
make format
```

### 🤝 贡献指南

欢迎贡献！请遵循以下规范：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feat/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feat/amazing-feature`)
5. 发起 Pull Request

**提交信息规范：**
- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试变更

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a id="traditional-chinese"></a>
## 繁體中文

### 🎉 專案介紹

LogLens-CLI 是一款**智慧終端機日誌分析器**，專為需要快速分析和理解日誌檔案的開發者設計。與傳統需要複雜設定的日誌檢視器不同，LogLens **開箱即用**，零設定即可工作。

**核心差異化亮點：**
- 🧠 **智慧格式識別** - 自動識別 JSON、logfmt 和普通文字格式
- ⚡ **極速解析** - 基於 Python 編寫，採用最佳化的解析演算法
- 🎨 **精美 TUI** - 互動式終端機介面，支援語法高亮
- 🔍 **智慧過濾** - 跨所有日誌欄位的即時搜尋
- 📊 **即時統計** - 錯誤/警告/資訊一目瞭然

**靈感來源：** 源於開發者在使用 `jq`、`grep`、`awk`、`less` 等多個工具來理解應用日誌時的挫敗感。

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📁 **多格式支援** | JSON、logfmt、純文字日誌 - 全部自動處理 |
| 🎛️ **互動式 TUI** | 全螢幕終端機介面，支援鍵盤導航 |
| 🔎 **即時過濾** | 按級別、訊息內容或任意欄位過濾 |
| 📈 **即時統計** | 錯誤/警告/資訊計數，帶視覺化長條圖 |
| 🌈 **語法高亮** | 顏色編碼的日誌級別，即時視覺識別 |
| 📤 **匯出 JSON** | 將任意日誌格式轉換為結構化 JSON |
| 🔄 **管道支援** | 與 `tail -f`、`kubectl logs`、`docker logs` 配合使用 |
| ⌨️ **Vim 風格按鍵** | 終端機高階使用者熟悉的導航方式 |

### 🚀 快速開始

#### 環境要求
- Python 3.8 或更高版本
- pip 套件管理器

#### 安裝

```bash
# 從 PyPI 安裝（即將推出）
pip install loglens-cli

# 或從原始碼安裝
git clone https://github.com/gitstq/loglens-cli.git
cd loglens-cli
pip install -e .
```

#### 基本用法

```bash
# 使用 TUI 開啟日誌檔案
loglens -f app.log

# 顯示統計資訊
loglens stats -f app.log

# 僅過濾錯誤
loglens filter -f app.log --level ERROR

# 搜尋特定文字
loglens filter -f app.log --search "database"

# 從其他命令管道輸入
tail -f app.log | loglens
kubectl logs -f my-pod | loglens
```

#### 鍵盤快捷鍵（TUI 模式）

| 按鍵 | 操作 |
|------|------|
| `q` / `Ctrl+C` | 退出 |
| `f` | 聚焦過濾輸入框 |
| `c` | 清除所有日誌 |
| `r` | 重新整理 |
| `e` | 僅顯示錯誤 |
| `w` | 顯示警告和錯誤 |
| `?` | 顯示說明 |

### 📖 詳細使用指南

#### 支援的日誌格式

**JSON 日誌：**
```json
{"timestamp": "2024-01-15T10:30:00Z", "level": "ERROR", "message": "Connection failed", "service": "api"}
```

**Logfmt 日誌：**
```
time=2024-01-15T10:30:00Z level=info msg="Request processed" duration=45ms
```

**純文字日誌：**
```
2024-01-15 10:30:00 INFO Application started successfully
```

#### CLI 命令

```bash
# 統計概覽
loglens stats -f /var/log/app.log

# 多條件過濾
loglens filter -f app.log --level ERROR --search "timeout" --limit 50

# 匯出為 JSON 以便進一步處理
loglens export -f app.log > output.json
```

### 💡 設計思路與迭代規劃

**為什麼選擇 LogLens？**

現代應用生成大量結構化日誌，但大多數開發者仍然依賴 `grep` 和 `tail` 等原始工具。ELK 堆疊或 Grafana Loki 等現有解決方案功能強大，但需要大量的基礎設施投入。

LogLens 填補了空白，提供：
- **零設定**日誌分析
- **終端機原生**工作流（無需瀏覽器）
- **即時啟動**（無需 Docker，無需服務）
- **通用格式支援**（適用於任何日誌框架）

**後續迭代計劃：**
- [ ] 日誌模式聚類和異常檢測
- [ ] 與主流日誌聚合服務整合
- [ ] 自定義顏色主題和格式化規則
- [ ] 日誌對比和差異檢視
- [ ] 效能指標提取

### 📦 打包與部署

```bash
# 構建分發包
make build

# 本地安裝
pip install dist/loglens-cli-*.whl

# 執行測試
make test

# 格式化程式碼
make format
```

### 🤝 貢獻指南

歡迎貢獻！請遵循以下規範：

1. Fork 倉庫
2. 建立功能分支 (`git checkout -b feat/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feat/amazing-feature`)
5. 發起 Pull Request

**提交資訊規範：**
- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 測試變更

### 📄 開源協議

本專案採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 檔案。
