# npmai-agent

> **Part of the [NPMAI ECOSYSTEM](https://npmai.netlify.app) — Open Source AI Research & Development**

[![PyPI version](https://img.shields.io/badge/pypi-npmai--agent-blue?style=flat-square)](https://pypi.org/project/npmai-agent)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Built by NPMAI](https://img.shields.io/badge/built%20by-NPMAI%20ECOSYSTEM-purple?style=flat-square)](https://npmai.netlify.app)
[![Version](https://img.shields.io/badge/version-0.0.1-orange?style=flat-square)](https://pypi.org/project/npmai-agent)

**npmai-agent** (internally known as the **npmai-agent-suite**) is a production-grade AI agent framework built on top of the NPMAI ECOSYSTEM. It gives any Python developer a fully autonomous, multi-LLM agentic pipeline with 21 integrated tool classes — covering everything from email automation, file management, GitHub operations, browser control, spreadsheets, PDF processing, image manipulation, SSH, Telegram, Discord, Slack, Twitter, QR codes, voice, RAG, and more — all orchestrated by a four-role LLM pipeline (Planner → Coder → Auditor → Verifier) with Fernet-encrypted credential storage and LARA RAG integration.

No paid APIs required. Free forever. Built on 45+ open-source LLMs.

---



## Developed by NPMAI ECOSYSTEM

**npmai-agent** is a product of the **[NPMAI ECOSYSTEM](https://npmai.netlify.app)**, an open-source AI research and development community founded by **Sonu Kumar** (known online as **Bihar Viral Boy**).

> Sonu Kumar is a 14-year-old self-taught developer, TEDx speaker, and researcher from Bihar, India, currently studying in Kota, Rajasthan. He founded NPMAI ECOSYSTEM at age 14, building the entire infrastructure on free cloud services — Render, HuggingFace Spaces, Supabase, Netlify — which now serves hundreds of thousands of developers worldwide with 2 million+ PyPI downloads
and 45+ community-contributed LLMs.

**Founder:** Sonu Kumar · [GitHub](https://github.com/sonuramashishnpm) · [PyPI](https://pypi.org/project/npmai) · [sonuramashishnpm@gmail.com](mailto:sonuramashishnpm@gmail.com)

**Ecosystem Website:** [https://npmai.netlify.app](https://npmai.netlify.app)

---

## Table of Contents

- [What is npmai-agent?](#what-is-npmai-agent)
- [Why npmai-agent?](#why-npmai-agent)
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Configuration — CredStore](#configuration--credstore)
- [Tool Classes & Documentation](#tool-classes--documentation)
  - [CredStore](#credstore)
  - [Workspace](#workspace)
  - [EmailTool](#emailtool)
  - [FileTool](#filetool)
  - [PDFTool](#pdftool)
  - [WebTool](#webtool)
  - [SpreadsheetTool](#spreadsheettool)
  - [GitHubTool](#githubtool)
  - [SlackTool](#slacktool)
  - [DiscordTool](#discordtool)
  - [WhatsAppTool](#whatsapptool)
  - [NotionTool](#notiontool)
  - [TwitterTool](#twittertool)
  - [SystemTool](#systemtool)
  - [ImageTool](#imagetool)
  - [SchedulerTool](#schedulertool)
  - [JiraTool](#jiratool)
  - [TelegramTool](#telegramtool)
  - [QRTool](#qrtool)
  - [VoiceTool](#voicetool)
  - [WatcherTool](#watchertool)
  - [RAGTool](#ragtool)
  - [SSHTool](#sshtool)
- [AgentBrain — The Autonomous Pipeline](#agentbrain--the-autonomous-pipeline)
- [Executor](#executor)
- [Version](#version)
- [License](#license)

---

## What is npmai-agent?

`npmai-agent` is a **desktop automation + agentic AI framework** that lets you:

1. **Use individual tool classes directly** in your own Python scripts.
2. **Hand a plain-English task to `AgentBrain`** and have a multi-LLM pipeline autonomously plan, generate code, audit it for security, execute it, verify the result, and retry on failure — all without you writing a single line of task-specific code.

It is the backbone of the **npmai-agent-suite** desktop application and is designed to be equally powerful as a headless library.

---

## Why npmai-agent?

Most AI agent frameworks require you to pay for GPT-4, Claude, or Gemini API credits. `npmai-agent` runs entirely on the **NPMAI ECOSYSTEM load balancer** — 45+ open-source LLMs available for free via `pip install npmai`. No credit card. No rate-limit anxiety. No vendor lock-in.

| Pain Point | npmai-agent Solution |
|---|---|
| Paid LLM APIs | 45+ free LLMs via NPMAI load balancer |
| Single-model pipelines | 4 specialized LLM roles (Planner, Coder, Auditor, Verifier) |
| Manual tool integration | 21 ready-made tool classes, zero boilerplate |
| Plain-text credential storage | Fernet-encrypted `CredStore` with machine-specific key |
| No memory between runs | Persistent `Memory` sessions via `npmai.Memory` |
| Document Q&A | LARA RAG pipeline via `npmai.Rag` |
| Complex setup | Auto-installs all dependencies on first run |

---

## Features

- **21 integrated tool classes** — email, files, PDF, web, spreadsheets, GitHub, Slack, Discord, WhatsApp, Notion, Twitter, system, images, scheduler, Jira, Telegram, QR, voice, file watcher, RAG, SSH
- **Four-role autonomous LLM pipeline** — Planner, Coder, Auditor, Verifier each run a different model optimised for their role
- **Security auditor built-in** — every generated code block is scanned before execution; destructive or credential-stealing code is blocked
- **Fernet-encrypted credential store** — machine-specific AES key, credentials never stored in plain text
- **LARA RAG integration** — query and summarise large documents using the NPMAI RAG architecture
- **Persistent memory** — separate memory contexts for planning, coding, chat, and task history
- **Auto-dependency installer** — missing packages are pip-installed automatically at runtime
- **Up to 12 auto-retries per step** — failed steps are regenerated with the error context fed back to the coder LLM
- **Workspace scanner** — the agent scans your Desktop, Downloads, Documents, Pictures, Videos, and Music folders to build a live context profile before planning
- **Kill switch support** — long-running tasks can be cancelled mid-execution

---

## Architecture Overview

```
User Task (plain English)
        │
        ▼
┌─────────────────┐
│   AgentBrain    │
│                 │
│  1. Workspace   │  ← scans your file system for context
│     Scanner     │
│                 │
│  2. Planner LLM │  ← breaks task into 2–5 atomic steps
│  (llama3.2:3b)  │
│                 │
│  For each step: │
│  ┌───────────┐  │
│  │ 3. Coder  │  │  ← generates Python code (codellama:7b)
│  │    LLM    │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ 4. Auditor│  │  ← security scan (qwen2.5-coder:7b)
│  │    LLM    │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ 5.Executor│  │  ← subprocess runner with live stdout
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │6. Verifier│  │  ← confirms step success (llama3.2:3b)
│  │    LLM    │  │
│  └───────────┘  │
│  (retry ×12)    │
└─────────────────┘
        │
        ▼
   Task Complete ✓
```

All LLMs are served free via the NPMAI ECOSYSTEM load balancer (`npmai.Ollama` with `change=True`).

---

## Installation

```bash
pip install npmai-agent
```

> `npmai-agent` will automatically install all required dependencies on first run, including `npmai`, `requests`, `beautifulsoup4`, `playwright`, `PyGithub`, `slack-sdk`, `gspread`, `openpyxl`, `pandas`, `Pillow`, `pypdf`, `python-docx`, `pyttsx3`, `SpeechRecognition`, `pyperclip`, `schedule`, `psutil`, `watchdog`, `tweepy`, `pywhatkit`, `qrcode`, `cryptography`, `paramiko`, `python-dotenv`, `pyautogui`, `opencv-python`, `pytesseract`, `yt-dlp`, `discord.py`, `telethon`, `notion-client`, `todoist-api-python`, `jira`, and more.

---

## Configuration — CredStore

Before using any tool that requires authentication (email, GitHub, Slack, etc.), you must store your credentials using `CredStore`. Credentials are encrypted with a Fernet key derived from your machine and stored locally at `~/.npmai_agent/creds.json`. They are never stored in plain text.

### How CredStore Works

```python
from npmai-agent import CredStore

# Save credentials for a named service
CredStore.save("gmail", {
    "email": "you@gmail.com",
    "password": "your-app-password",   # Use Gmail App Password, not your login password
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "imap_host": "imap.gmail.com"
})

# Load credentials (returns a dict)
creds = CredStore.load("gmail")
print(creds["email"])

# List all saved credential keys
keys = CredStore.all_keys()
print(keys)  # ['gmail', 'github', 'slack', ...]
```

### Credential Reference by Tool

| Tool | `cred_key` | Required fields |
|---|---|---|
| `EmailTool` | `"gmail"` | `email`, `password`, `smtp_host`, `smtp_port`, `imap_host` |
| `GitHubTool` | `"github"` | `token` |
| `SlackTool` | `"slack"` | `bot_token` |
| `SpreadsheetTool` (Google Sheets) | `"google"` | Full service account JSON as dict |
| `NotionTool` | `"notion"` | `token` |
| `TwitterTool` | `"twitter"` | `api_key`, `api_secret`, `access_token`, `access_token_secret` |
| `JiraTool` | `"jira"` | `server`, `email`, `api_token` |
| `TelegramTool` | `"telegram"` | `bot_token` |
| `SSHTool` | `"ssh"` | `user`, `password` (or `key_path`) |

```python
# GitHub
CredStore.save("github", {"token": "ghp_xxxxxxxxxxxxxxxxxxxx"})

# Slack
CredStore.save("slack", {"bot_token": "xoxb-xxxxxxxxxxxx"})

# Notion
CredStore.save("notion", {"token": "secret_xxxxxxxxxxxx"})

# Twitter / X
CredStore.save("twitter", {
    "api_key": "...",
    "api_secret": "...",
    "access_token": "...",
    "access_token_secret": "..."
})

# Jira
CredStore.save("jira", {
    "server": "https://yourworkspace.atlassian.net",
    "email": "you@company.com",
    "api_token": "your-jira-api-token"
})

# Telegram
CredStore.save("telegram", {"bot_token": "1234567890:AAxxxxxxxxxxxxxx"})

# SSH
CredStore.save("ssh", {"user": "ubuntu", "password": "secret"})
# or with key file
CredStore.save("ssh", {"user": "ubuntu", "key_path": "/home/you/.ssh/id_rsa"})
```

---

## Tool Classes & Documentation

All tool classes extend `ensure`, which auto-installs required dependencies on first instantiation. Every method returns a `ToolResult` object with three fields:

```python
result.success  # bool — True if the operation succeeded
result.output   # str  — human-readable status message
result.data     # any  — the actual returned data (list, str, DataFrame, etc.)
```

---

### CredStore

Fernet-encrypted local credential vault.

```python
from npmai-agent import CredStore

# Store credentials
CredStore.save("service_name", {"key": "value"})

# Load credentials
data = CredStore.load("service_name")

# List all saved keys
print(CredStore.all_keys())
```

---

### Workspace

Scans the user's file system and builds a context profile used by `AgentBrain` during planning.

```python
from npmai-agent import Workspace

ws = Workspace()

# Scan Desktop, Downloads, Documents, Pictures, Videos, Music
profile = ws.scan()
print(profile["os"])         # 'Windows' / 'Darwin' / 'Linux'
print(profile["home"])       # '/home/sonu'
print(profile["paths"])      # dict of folder → files

# Update any custom profile field
ws.update_profile("user_name", "Sonu Kumar")

# Get a short text summary (used internally by the planner LLM)
print(ws.context_summary())
```

---

### EmailTool

Send emails via Gmail SMTP, read inbox via IMAP, and send bulk personalised emails from a CSV.

```python
from npmai-agent import EmailTool, CredStore

# Configure once
CredStore.save("gmail", {
    "email": "you@gmail.com",
    "password": "app-password-here",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "imap_host": "imap.gmail.com"
})

# Send a single email
result = EmailTool.send(
    to="friend@example.com",
    subject="Hello from npmai-agent",
    body="<h1>This was sent by an AI agent!</h1>"
)
print(result)  # ✓ Email sent to friend@example.com

# Send with attachments
result = EmailTool.send(
    to="boss@company.com",
    subject="Monthly Report",
    body="Please find the report attached.",
    attachments=["/home/sonu/report.pdf"]
)

# Read inbox (last 10 emails)
result = EmailTool.read_inbox(count=10)
if result.success:
    for msg in result.data:
        print(msg["from"], msg["subject"], msg["date"])

# Bulk email from CSV
# CSV must have 'name' and 'email' columns (configurable)
result = EmailTool.send_bulk(
    csv_path="contacts.csv",
    subject="Invitation to NPMAI Launch",
    body_template="<p>Hello {name}, you are invited!</p>",
    name_col="name",
    email_col="email"
)
print(result)  # ✓ Sent 42 emails, 0 failed
```

---

### FileTool

Rename, move, copy, zip, unzip, search, organize, read, and write files.

```python
from npmai-agent import FileTool

# Bulk rename all .txt files in a folder
result = FileTool.bulk_rename(
    folder="/home/sonu/Documents",
    pattern="*.txt",
    prefix="NPMAI_",
    suffix="_v1",
    add_date=True
)
print(result)  # ✓ Renamed 12 files

# Zip a folder
result = FileTool.zip_folder(
    source="/home/sonu/project",
    dest="/home/sonu/project_backup.zip"
)

# Unzip
result = FileTool.unzip(
    zip_path="/home/sonu/archive.zip",
    dest="/home/sonu/extracted"
)

# Find files recursively
result = FileTool.find_files(
    folder="/home/sonu",
    pattern="*.py",
    recursive=True
)
print(result.data)  # ['/home/sonu/agent_core.py', ...]

# Organize folder by file type (creates Images/, Videos/, Docs/, etc.)
result = FileTool.organize_by_type("/home/sonu/Downloads")
print(result)  # ✓ Organized 87 files by type

# Read a file
result = FileTool.read_file("/home/sonu/notes.txt")
print(result.data)  # file content as string

# Write a file
result = FileTool.write_file(
    path="/home/sonu/output/report.txt",
    content="Generated by npmai-agent."
)

# Copy entire directory tree
result = FileTool.duplicate_tree(
    src="/home/sonu/project",
    dst="/home/sonu/project_copy"
)
```

---

### PDFTool

Merge, split, and extract text from PDF files.

```python
from npmai-agent import PDFTool

# Extract all text from a PDF
result = PDFTool.extract_text("/home/sonu/research_paper.pdf")
print(result.data)  # extracted text string

# Merge multiple PDFs into one
result = PDFTool.merge(
    paths=["/home/sonu/chapter1.pdf", "/home/sonu/chapter2.pdf"],
    out="/home/sonu/full_book.pdf"
)
print(result)  # ✓ Merged 2 PDFs → /home/sonu/full_book.pdf

# Split a PDF into individual pages
result = PDFTool.split(
    path="/home/sonu/document.pdf",
    out_dir="/home/sonu/pages"
)
print(result)  # ✓ Split into 24 pages in /home/sonu/pages
```

---

### WebTool

Scrape websites, download files, take screenshots, automate browsers via Playwright, and make raw API calls.

```python
from npmai-agent import WebTool

# Scrape full page text
result = WebTool.scrape("https://npmai.netlify.app")
print(result.data[:500])

# Scrape specific elements using CSS selector
result = WebTool.scrape(
    url="https://example.com",
    selector="h2"
)
print(result.data)  # ['Heading 1', 'Heading 2', ...]

# Download a file
result = WebTool.download_file(
    url="https://example.com/file.pdf",
    dest="/home/sonu/downloads/file.pdf"
)

# Take a full-page screenshot (requires Playwright)
result = WebTool.screenshot_url(
    url="https://npmai.netlify.app",
    out="/home/sonu/npmai_screenshot.png"
)

# Automated browser actions (click, fill, extract)
result = WebTool.browser_action(
    url="https://example.com/login",
    actions=[
        {"type": "fill", "selector": "#username", "value": "sonu"},
        {"type": "fill", "selector": "#password", "value": "secret"},
        {"type": "click", "selector": "#login-btn"},
        {"type": "wait", "ms": 2000},
        {"type": "screenshot", "path": "after_login.png"}
    ]
)

# Make a raw HTTP API call
result = WebTool.api_call(
    url="https://api.example.com/data",
    method="POST",
    headers={"Authorization": "Bearer token"},
    payload={"query": "test"}
)
print(result.data)  # parsed JSON response
```

---

### SpreadsheetTool

Read/write CSV, Excel, and Google Sheets.

```python
from npmai-agent import SpreadsheetTool, CredStore

# Read a CSV file
result = SpreadsheetTool.read_csv("/home/sonu/data.csv")
df = result.data  # pandas DataFrame
print(f"{len(df)} rows")

# Write a DataFrame or list of dicts to Excel
data = [{"name": "Sonu", "age": 15}, {"name": "AI", "age": 0}]
result = SpreadsheetTool.write_excel(
    data=data,
    path="/home/sonu/output.xlsx",
    sheet="Founders"
)

# Read from Google Sheets (requires service account credentials)
CredStore.save("google", {
    "type": "service_account",
    "project_id": "...",
    "private_key_id": "...",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...",
    "client_email": "...",
    # ... full service account JSON
})

result = SpreadsheetTool.google_sheets_read(
    sheet_id="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
    range_="Sheet1"
)
print(result.data)  # list of row dicts
```

---

### GitHubTool

Create issues, push files, list issues, fetch READMEs, clone repos, commit and push.

```python
from npmai-agent import GitHubTool, CredStore

CredStore.save("github", {"token": "ghp_xxxxxxxxxxxxxxxxxxxx"})

# Create an issue
result = GitHubTool.create_issue(
    repo="sonuramashishnpm/npmai",
    title="Bug: model timeout on large inputs",
    body="Steps to reproduce...",
    labels=["bug", "llm"]
)
print(result)  # ✓ Issue #42 created: https://github.com/...

# Push (create or update) a file in a repo
result = GitHubTool.push_file(
    repo="sonuramashishnpm/npmai",
    path="docs/agent.md",
    content="# npmai-agent docs\n...",
    message="docs: add agent documentation"
)

# List open issues
result = GitHubTool.list_issues(repo="sonuramashishnpm/npmai", state="open")
for issue in result.data:
    print(issue["#"], issue["title"])

# Fetch README
result = GitHubTool.get_readme(repo="sonuramashishnpm/npmai")
print(result.data[:300])

# Clone a repository
result = GitHubTool.clone_repo(
    url="https://github.com/sonuramashishnpm/npmai.git",
    dest="/home/sonu/projects/npmai"
)

# Stage, commit, and push from a local repo
result = GitHubTool.git_commit_push(
    repo_path="/home/sonu/projects/npmai",
    message="feat: add new model endpoints"
)
```

---

### SlackTool

Send messages, read channel history, upload files to Slack.

```python
from npmai-agent import SlackTool, CredStore

CredStore.save("slack", {"bot_token": "xoxb-xxxxxxxxxxxx"})

# Send a message to a channel
result = SlackTool.send_message(
    channel="#general",
    text="npmai-agent task completed successfully ✓"
)

# Read last 20 messages from a channel
result = SlackTool.read_channel(channel="#dev-logs", limit=20)
for msg in result.data:
    print(msg["user"], ":", msg["text"])

# Upload a file
result = SlackTool.upload_file(
    channel="#reports",
    file_path="/home/sonu/report.pdf",
    comment="Weekly AI report"
)
```

---

### DiscordTool

Send messages and embeds to Discord channels via webhook.

```python
from npmai-agent import DiscordTool

WEBHOOK = "https://discord.com/api/webhooks/xxxx/yyyy"

# Send a plain message
result = DiscordTool.send_webhook(
    webhook_url=WEBHOOK,
    content="🚀 npmai-agent deployment complete!"
)

# Send with an embed
result = DiscordTool.send_webhook(
    webhook_url=WEBHOOK,
    content="Task update:",
    embeds=[{
        "title": "Step 3 Complete",
        "description": "All files organized successfully.",
        "color": 3066993
    }]
)
```

---

### WhatsAppTool

Send WhatsApp messages (requires WhatsApp Web to be open in the browser).

```python
from npmai-agent import WhatsAppTool

# Phone number must include country code, e.g. +91 for India
result = WhatsAppTool.send(
    phone="+919876543210",
    message="Hello from npmai-agent!",
    wait=15  # seconds to wait before sending
)
print(result)  # ✓ WhatsApp sent to +919876543210
```

---

### NotionTool

Create pages and add database entries in Notion.

```python
from npmai-agent import NotionTool, CredStore

CredStore.save("notion", {"token": "secret_xxxxxxxxxxxx"})

# Create a new page inside a parent page
result = NotionTool.create_page(
    parent_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    title="NPMAI Agent Research Notes",
    content="This page was created by npmai-agent automatically."
)
print(result)  # ✓ Notion page created: https://notion.so/...

# Add a row to a Notion database
result = NotionTool.add_db_entry(
    db_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    props={
        "Name": {"title": [{"text": {"content": "Task Completed"}}]},
        "Status": {"select": {"name": "Done"}}
    }
)
```

---

### TwitterTool

Post tweets using the Twitter v2 API.

```python
from npmai-agent import TwitterTool, CredStore

CredStore.save("twitter", {
    "api_key": "...",
    "api_secret": "...",
    "access_token": "...",
    "access_token_secret": "..."
})

result = TwitterTool.tweet(
    text="Just automated my workflow with npmai-agent by @NPMAIEcosystem 🤖 #OpenSource #AI"
)
print(result)  # ✓ Tweeted: 1234567890123456789
```

---

### SystemTool

Run shell commands, manage processes, use the clipboard, take screenshots, and send desktop notifications.

```python
from npmai-agent import SystemTool

# Run any shell command
result = SystemTool.run_command("ls -la /home/sonu", cwd="/home/sonu", timeout=30)
print(result.output)

# Get clipboard contents
result = SystemTool.get_clipboard()
print(result.data)

# Set clipboard contents
result = SystemTool.set_clipboard("Copied by npmai-agent")

# Take a screenshot
result = SystemTool.screenshot(out="/home/sonu/screen.png")

# List running processes
result = SystemTool.get_processes()
for proc in result.data[:5]:
    print(proc["name"], proc["cpu"], "%")

# Send a desktop notification
result = SystemTool.notify(
    title="npmai-agent",
    message="Your task has been completed!"
)
```

---

### ImageTool

Resize, convert, OCR, and bulk-compress images using Pillow and pytesseract.

```python
from npmai-agent import ImageTool

# Resize an image
result = ImageTool.resize(
    path="/home/sonu/photo.jpg",
    width=800,
    height=600,
    out="/home/sonu/photo_resized.jpg"
)

# Convert image format
result = ImageTool.convert(
    path="/home/sonu/photo.jpg",
    format="PNG",
    out="/home/sonu/photo.png"
)

# Extract text from an image (OCR)
result = ImageTool.ocr("/home/sonu/scanned_doc.png")
print(result.data)  # extracted text

# Bulk compress all JPGs/PNGs in a folder
result = ImageTool.bulk_compress(
    folder="/home/sonu/Pictures",
    quality=75
)
print(result)  # ✓ Compressed 34 images
```

---

### SchedulerTool

Schedule Python callbacks to run at specific times or intervals in background threads.

```python
from npmai-agent import SchedulerTool

def my_task():
    print("Running scheduled task!")

# Run every 5 minutes
result = SchedulerTool.schedule_task(
    task_id="heartbeat",
    cron_like="every 5 minutes",
    callback=my_task
)

# Run every day at 09:00
result = SchedulerTool.schedule_task(
    task_id="daily_report",
    cron_like="every day at 09:00",
    callback=my_task
)

# Run every Monday at 08:00
result = SchedulerTool.schedule_task(
    task_id="weekly_sync",
    cron_like="every monday at 08:00",
    callback=my_task
)

# Cancel a scheduled task
result = SchedulerTool.cancel_task("heartbeat")
```

---

### JiraTool

Create and manage Jira issues.

```python
from npmai-agent import JiraTool, CredStore

CredStore.save("jira", {
    "server": "https://yourworkspace.atlassian.net",
    "email": "you@company.com",
    "api_token": "your-jira-api-token"
})

# Create a Jira issue
result = JiraTool.create_issue(
    project="NPMAI",
    summary="Integrate agent v0.0.1 with desktop UI",
    description="The agent core needs to be wired to the PySide6 app.",
    issue_type="Task"
)
print(result)  # ✓ Jira issue NPMAI-17 created
```

---

### TelegramTool

Send messages via a Telegram bot.

```python
from npmai-agent import TelegramTool, CredStore

CredStore.save("telegram", {"bot_token": "1234567890:AAxxxxxxxxxxxxxx"})

# Send a message (chat_id can be a user ID or @channel)
result = TelegramTool.send(
    chat_id="123456789",
    text="✅ npmai-agent task complete: organized 87 files."
)
print(result)  # ✓ Telegram sent
```

---

### QRTool

Generate QR codes from any text or URL.

```python
from npmai-agent import QRTool

# Generate and save a QR code
result = QRTool.generate(
    data="https://npmai.netlify.app",
    out="/home/sonu/npmai_qr.png",
    size=10
)
print(result)  # ✓ QR code saved: /home/sonu/npmai_qr.png
```

---

### VoiceTool

Text-to-speech output and speech-to-text input.

```python
from npmai-agent import VoiceTool

# Speak text aloud
result = VoiceTool.speak("Task completed successfully. npmai-agent is ready.")
print(result)  # ✓ Spoken

# Listen for speech input (5 seconds)
result = VoiceTool.listen(seconds=5)
if result.success:
    print(result.data)  # recognised text from microphone
```

---

### WatcherTool

Watch a folder for file creation or modification events and trigger a callback.

```python
from npmai-agent import WatcherTool

def on_file_change(file_path):
    print(f"File changed: {file_path}")
    # trigger any action here

# Start watching a folder in a background thread
result = WatcherTool.watch(
    folder="/home/sonu/incoming",
    callback=on_file_change
)
print(result)  # ✓ Watching /home/sonu/incoming
```

---

### RAGTool

Query large documents and summarise long files using the NPMAI LARA RAG pipeline.

```python
from npmai-agent import RAGTool

# Query a document (PDF or plain text) using natural language
result = RAGTool.query_document(
    doc_path="/home/sonu/research_paper.pdf",
    question="What is the main contribution of this paper?",
    chunk_size=500
)
print(result.data)  # LLM-generated answer

# Summarise a large document (processes up to 10 × 3000-char chunks)
result = RAGTool.summarize_large_file(
    path="/home/sonu/thesis.pdf",
    model="mistral:7b"
)
print(result.data)  # comprehensive summary
```

---

### SSHTool

Run commands on remote servers and transfer files via SFTP.

```python
from npmai-agent import SSHTool, CredStore

CredStore.save("ssh", {
    "user": "ubuntu",
    "password": "your-server-password"
    # or use key_path instead of password:
    # "key_path": "/home/sonu/.ssh/id_rsa"
})

# Run a remote command
result = SSHTool.run(
    host="192.168.1.100",
    command="df -h && uptime"
)
print(result.data)  # command output

# Upload a file via SFTP
result = SSHTool.upload(
    host="192.168.1.100",
    local="/home/sonu/deploy.sh",
    remote="/home/ubuntu/deploy.sh"
)
print(result)  # ✓ Uploaded /home/sonu/deploy.sh → /home/ubuntu/deploy.sh
```

---

## AgentBrain — The Autonomous Pipeline

`AgentBrain` is the core orchestrator. Once your credentials are configured via `CredStore`, you can hand it any task in plain English and it will autonomously plan, code, audit, execute, verify, and retry until the task is done — using all 21 tool classes above as needed.

```python
from npmai-agent import AgentBrain

# Optional callbacks for logging, progress, and status
def log(msg): print(msg)
def progress(pct): print(f"Progress: {pct}%")
def status(s): print(f"Status: {s}")

brain = AgentBrain(
    log_cb=log,
    progress_cb=progress,
    status_cb=status
)
```

### Running a Task

```python
# Simple plain-English task — the agent figures out the rest
brain.run_task("Organize my Downloads folder by file type")

brain.run_task("Send an email to team@company.com saying the build passed")

brain.run_task("Scrape the titles of all articles from https://example.com/blog and save them to a CSV")

brain.run_task("Create a GitHub issue in sonuramashishnpm/npmai titled 'Add voice input support'")

brain.run_task("Read my last 5 emails and summarise them")
```

### Chat Mode (for questions, not computer tasks)

```python
response = brain.chat("What is the LARA RAG architecture?")
print(response)
```

### Task with Kill Switch

```python
import threading

killed = [False]

def run():
    brain.run_task("Download and process 500 PDFs from the server", killed_flag=killed)

t = threading.Thread(target=run)
t.start()

# Cancel at any time
killed[0] = True
```

### Task History

```python
history = AgentBrain.load_task_history()
for entry in history:
    status = "✓" if entry["success"] else "✗"
    print(f"{status} [{entry['time']}] {entry['task']}")
```

### How AgentBrain Uses All 21 Tools

`AgentBrain` exposes the complete tool registry to the Coder LLM. When generating code for each step, the LLM is provided with this import context:

```python
from npmai-agent import EmailTool, FileTool, WebTool, SpreadsheetTool
from npmai-agent import GitHubTool, SlackTool, PDFTool, ImageTool
from npmai-agent import SystemTool, TelegramTool, QRTool, RAGTool, SSHTool
from npmai-agent import DiscordTool, WhatsAppTool, NotionTool, TwitterTool
from npmai-agent import SchedulerTool, JiraTool, VoiceTool, WatcherTool
from npmai-agent import CredStore, Workspace
```

This means you don't call the tools yourself — you just configure credentials with `CredStore` and describe your task in plain English. `AgentBrain` selects the right tools, generates the code, audits it for security, executes it, verifies success, and retries on failure — up to 12 times per step.

### LLM Pipeline Details

| Role | Default Model | Fallback | Purpose |
|---|---|---|---|
| **Planner** | `llama3.2:3b` | `mistral:7b` | Breaks task into 2–5 atomic steps |
| **Coder** | `codellama:7b-instruct` | `deepseek-coder:6.7b` | Generates executable Python code |
| **Auditor** | `qwen2.5-coder:7b` | `falcon:7b-instruct` | Security scan before execution |
| **Verifier** | `llama3.2:3b` | `mistral:7b` | Confirms step completed successfully |
| **Chatter** | `granite3.3:2b` | `llama3.2:1b` | General Q&A / chat mode |

All models are served free via the NPMAI ECOSYSTEM load balancer with `change=True` for automatic fallback.

---

## Executor

`Executor` is used internally by `AgentBrain` but can be used standalone to safely run any Python code string as a subprocess with live stdout streaming.

```python
from npmai-agent import Executor

def log(line): print(line)

executor = Executor(log_cb=log, timeout=120)

code = """
import time
for i in range(5):
    print(f"Step {i+1}")
    time.sleep(0.5)
"""

success, output = executor.run(code)
print(f"Success: {success}")
print(f"Output: {output}")

# Kill a running executor
executor.kill()
```

---

## Version

**0.0.1** — Initial release of `npmai-agent`.

This is the first public release of the npmai-agent-suite as a distributable PyPI package. The core agent pipeline, all 21 tool classes, CredStore, Workspace, Executor, and AgentBrain are stable and production-ready.

---

## License

MIT License — free to use, modify, and distribute.

Built with ❤️ by **Sonu Kumar**, Founder of NPMAI ECOSYSTEM · [npmai.netlify.app](https://npmai.netlify.app)

> *"Promoting Individual Journalism to every nation's village so that the democratic values of a nation can be strengthened and we can achieve Representative Ideal Democracy."*
> — Sonu Kumar, Founder, NPMAI ECOSYSTEM
