<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a1a,30:0d0d2b,60:1a0a3a,100:0d1b4a&height=240&section=header&text=npmai_agents&fontSize=82&fontColor=00f5ff&fontAlignY=38&desc=1%2C371%20Tools.%20100%20Classes.%20One%20Package.%20Zero%20Cost.&descColor=a78bfa&descAlignY=60&animation=twinkling" width="100%"/>

<a href="https://npmai.netlify.app">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2500&pause=800&color=00F5FF&center=true&vCenter=true&multiline=false&width=800&lines=1%2C371+verified+tools+across+100+classes;5-role+autonomous+LLM+pipeline+%E2%86%92+Plan+%E2%86%92+Select+%E2%86%92+Code+%E2%86%92+Audit+%E2%86%92+Verify;12+LLM+providers+%E2%80%94+NPMAI%2C+OpenAI%2C+Groq%2C+Anthropic%2C+Gemini+%26+more;Built+by+Sonu+Kumar+%C2%B7+NPMAI+ECOSYSTEM+%C2%B7+Free+Forever" alt="Typing SVG"/>
</a>

<br/>
<br/>

<img src="https://img.shields.io/badge/PyPI-npmai__agents-00f5ff?style=for-the-badge&logo=pypi&logoColor=white&labelColor=0a0a1a"/>
<img src="https://img.shields.io/badge/Version-1.0.2-a78bfa?style=for-the-badge&labelColor=0a0a1a"/>
<img src="https://img.shields.io/badge/Python-3.9%2B-00f5ff?style=for-the-badge&logo=python&logoColor=white&labelColor=0a0a1a"/>
<img src="https://img.shields.io/badge/License-MIT-2affa0?style=for-the-badge&labelColor=0a0a1a"/>
<img src="https://img.shields.io/badge/Status-Production%20Stable-2affa0?style=for-the-badge&labelColor=0a0a1a"/>

<br/>

<img src="https://img.shields.io/badge/Tools-1%2C371-ff6b9d?style=for-the-badge&labelColor=0a0a1a"/>
<img src="https://img.shields.io/badge/Classes-100-a78bfa?style=for-the-badge&labelColor=0a0a1a"/>
<img src="https://img.shields.io/badge/LLM%20Roles-5-00f5ff?style=for-the-badge&labelColor=0a0a1a"/>
<img src="https://img.shields.io/badge/LLM%20Providers-12-ff6b9d?style=for-the-badge&labelColor=0a0a1a"/>
<img src="https://img.shields.io/badge/NPMAI-ECOSYSTEM-00f5ff?style=for-the-badge&labelColor=0a0a1a"/>

<br/>
<br/>

**[`🌐 Website`](https://npmai.netlify.app)** · **[`📦 PyPI`](https://pypi.org/project/npmai_agents)** · **[`🐙 GitHub`](https://github.com/sonuramashishnpm/npmai-agent)** · **[`👤 Founder`](https://github.com/sonuramashishnpm)** 
. **[![PyPI Downloads](https://static.pepy.tech/personalized-badge/npmai-agents?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/npmai-agents)**

</div>

---

## ✦ What is npmai_agents?

**npmai_agents** is a production-grade, open-source autonomous AI agent framework with **1,371 verified tools across 100 classes** — the largest open-source local tool registry ever built. A **5-role LLM pipeline** (Planner → Tool Manager → Coder → Auditor → Verifier) autonomously executes any plain-English task on your computer using **12 supported LLM providers** including NPMAI free LLMs, OpenAI, Groq, Anthropic, Gemini, and more.

The core insight: LLMs waste most of their context reverse-engineering API documentation instead of solving your actual problem. Every class in npmai_agents ships a `use` variable — pre-compiled, structured tool knowledge that the pipeline reads on-demand. The Planner sees a one-line index of all 100 classes. The Tool Manager drills into full documentation only for classes the task actually needs. The Coder receives exact method signatures and call examples. Zero hallucination on API shapes. Maximum intelligence on task logic.

---

## 🏛️ NPMAI ECOSYSTEM

<table>
<tr>
<td width="55%">

**npmai_agents** is a product of the **[NPMAI ECOSYSTEM](https://npmai.netlify.app)** — a free, open-source AI research and development platform founded by **Sonu Kumar** (Bihar Viral Boy), a 15-year-old self-taught AI developer, TEDx Speaker, and constitutional researcher from Bihar, India.

</td>
<td width="45%">

| Metric | Value |
|---|---|
| PyPI Downloads | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/npmai?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/npmai) |
| Daily Requests | `80,000+` |
| Free LLMs | `45+` |
| Monthly Cost | `₹0` |

</td>
<td width="45%">
  
| Metric | Value |
|---|---|
| PyPI Downloads | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/npmai-agents?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/npmai-agents) |
| Tools | `1,371` |

</td>
</tr>
</table>

[![Website](https://img.shields.io/badge/Website-npmai.netlify.app-0a0a1a?style=flat-square&logo=netlify&logoColor=2affa0)](https://npmai.netlify.app)
[![GitHub](https://img.shields.io/badge/GitHub-sonuramashishnpm-0a0a1a?style=flat-square&logo=github&logoColor=00f5ff)](https://github.com/sonuramashishnpm)
[![PyPI npmai](https://img.shields.io/badge/PyPI-npmai-0a0a1a?style=flat-square&logo=pypi&logoColor=a78bfa)](https://pypi.org/project/npmai)

---

## ⚡ Installation

```bash
# Minimal — agent auto-installs tool dependencies at runtime
pip install npmai_agents

# Full — all 1,371 tool dependencies pre-installed
pip install npmai_agents[full]
```

### Quick Start

```bash
# Pull the image
docker pull sonuramashishnpm/npmai-agent:latest

# See available commands
docker run --rm sonuramashishnpm/npmai-agent --help

# Run any task
docker run --rm -v "$(pwd):/workspace" -w /workspace \
  sonuramashishnpm/npmai-agent run "Analyze my sales.csv and create a revenue report"
```
### Tags

- `latest` — Latest stable version
- `v1` — Version 1.0.1


### 📦 Import System

All 100 tool classes, every LLM backend, and the agent brain itself are exposed from a single top-level namespace: `npmai_agents`. Internally the code is split across many files by domain (`core.py`, `agent_core.py`, `Tools_business.py`, `Tools_creative.py`, etc.) — that split is for maintainability on our side. As a user you never need to know or care which file anything actually lives in. The package's `__init__.py` re-exports every public class at the top level, so a single import line reaches everything:

```python
# Agent brain only
from npmai_agents import AgentBrain

# Specific tools, no matter which internal file they live in
from npmai_agents import StripeTool, GitHubTool, FFmpegTool

# LLM backends
from npmai_agents import GroqBackend, OpenAIBackend, AnthropicBackend

# Core infra
from npmai_agents import CredStore, Workspace, LLMBackend

# Everything at once (not recommended for large projects — namespace gets crowded)
from npmai_agents import *
```

You will **never** need to write `from Tools_business import StripeTool` or `from core import LLMBackend` yourself — those are internal file paths used only inside the package's own source code. Every public class, from every file, is reachable directly via `from npmai_agents import <ClassName>`.

---

## 🖥️ CLI — Complete Reference

Install gives you the `npmai` terminal command globally.

```bash
npmai --help
```

### 🛠️ Troubleshooting: CLI Command Not Found (PATH Issue)

If you get a warning during installation stating that the script is installed in a directory which is **not on PATH**, your terminal will not recognize the command. Follow the solution for your operating system below.

---

#### 🪟 On Windows
If you see a warning referencing `AppData\Roaming\Python\...`

**Solution:**
Open **PowerShell as an Administrator** and run:
```powershell
[Environment]::SetEnvironmentVariable("Path", \$env:Path + ";C:\Users\digiccsammunnat8\AppData\Roaming\Python\Python312\Scripts", "User")
```
*Note: Restart your terminal window after running this command.*

---

#### 🐧 On Linux
If you see a warning referencing `~/.local/bin`

**Solution:**
Open your terminal and run:
```bash
echo 'export PATH="HOME/.local/bin:PATH"' >> ~/.bashrc && source ~/.bashrc
```
*Note: If you use Zsh instead of Bash, replace `~/.bashrc` with `~/.zshrc`.*

---

#### 🍏 On macOS
If you see a warning referencing `~/Library/Python/...`

**Solution:**
Open your terminal and run (replace `3.12` with your actual Python version):
```bash
echo 'export PATH="HOME/Library/Python/3.12/bin:PATH"' >> ~/.zshrc && source ~/.zshrc
```
*Note: If you use Bash instead of Zsh on older macOS versions, replace `~/.zshrc` with `~/.bash_profile`.*

---

#### 💡 Pro Tip: Avoid PATH Issues Entirely
Use a virtual environment for your project so dependencies and paths are isolated automatically:
```bash
# Create and activate the environment
python -m venv venv
source venv/bin/activate  # On Windows PowerShell use: .\venv\Scripts\activate

# Install your package cleanly
pip install npmai-agents
```

> **Session model:** each `npmai <command>` invocation is its own standalone process — there is no config file, no state file, and nothing written to disk between commands (by design, so the framework never has to manage extra files on top of everything else it already manages). This means `run` and `chat` accept the LLM provider/model for every role directly as flags on the same call, rather than relying on a separate "configure once" step that would silently reset between processes anyway. If you omit the flags, every role defaults to the free NPMAI-hosted models — zero setup, zero cost.

---

### `npmai run` — Execute Any Task

Runs a plain-English task through the full 5-role autonomous pipeline. LLM provider/model for each role can be set per-call; anything left unset falls back to the NPMAI free-tier default for that role.

| Parameter | Type | Default | Required | Description |
|---|---|---|---|---|
| `task` | `str` | — | ✅ | Plain-English description of what to do |
| `--planner-model` | `str` | `llama3.2:3b` | ❌ | Model for the Planner role |
| `--planner-provider` | `str` | `npmai` | ❌ | Provider for the Planner role |
| `--tool-manager-provider` | `str` | `npmai` | ❌ | Provider for Tool_Manager role who select tools |
| `--tool-manager-model` | `str` | `npmai` | ❌ | Model for Tool_Manager role who select tools |
| `--coder-model` | `str` | `codellama:7b-instruct` | ❌ | Model for the Coder role |
| `--coder-provider` | `str` | `npmai` | ❌ | Provider for the Coder role |
| `--auditor-model` | `str` | `qwen2.5-coder:7b` | ❌ | Model for the Auditor role |
| `--auditor-provider` | `str` | `npmai` | ❌ | Provider for the Auditor role |
| `--verifier-model` | `str` | `llama3.2:3b` | ❌ | Model for the Verifier role |
| `--verifier-provider` | `str` | `npmai` | ❌ | Provider for the Verifier role |
| `--chatter-model` | `str` | `granite3.3:2b` | ❌ | Model for the Chatter role |
| `--chatter-provider` | `str` | `npmai` | ❌ | Provider for the Chatter role |

```bash
# Zero-config — all roles run on free NPMAI models
npmai run "Scrape the top 10 AI papers from arXiv today, summarise each in 3 sentences, save to Excel, and email it to me"

npmai run "Find all duplicate files in my Downloads folder and delete them"

# Mixing providers per role — Groq for planning/coding, defaults for the rest
npmai run "Pull latest from my GitHub repo, run the tests, and post results to Slack #dev" \
  --planner-provider groq --planner-model llama-3.3-70b-versatile \
  --coder-provider groq --coder-model llama-3.3-70b-versatile

npmai run "Create a Stripe customer for john@example.com and generate an invoice for 5000 rupees" \
  --auditor-provider anthropic --auditor-model claude-sonnet-4-6
```

**Output:** Streamed logs showing each pipeline stage — Planning → Tool Selection → Code Generation → Security Audit → Execution → Verification. Final `✓ All steps completed successfully` on success.

**Provider Reference** (same values work for every `--*-provider` flag above):

| Provider | `--*-provider` value | Example model | Save credentials first |
|---|---|---|---|
| NPMAI Free | `npmai` | `llama3.2:3b` | Not required |
| Local Ollama | `local` | `llama3.2:3b` | Not required |
| OpenAI | `openai` | `gpt-4o` | `npmai save-credentials openai '{"api_key":"sk-xxx"}'` |
| Groq | `groq` | `llama-3.3-70b-versatile` | `npmai save-credentials groq '{"api_key":"gsk_xxx"}'` |
| Anthropic | `anthropic` | `claude-sonnet-4-6` | `npmai save-credentials anthropic '{"api_key":"sk-ant-xxx"}'` |
| Gemini | `gemini` | `gemini-2.0-flash` | `npmai save-credentials gemini '{"api_key":"AIza-xxx"}'` |
| Mistral | `mistral` | `mistral-large-latest` | `npmai save-credentials mistral '{"api_key":"xxx"}'` |
| Cohere | `cohere` | `command-r-plus` | `npmai save-credentials cohere '{"api_key":"xxx"}'` |
| Azure OpenAI | `azure` | `gpt-4o` | `npmai save-credentials azure '{"api_key":"xxx","endpoint":"https://xxx.openai.azure.com","deployment":"gpt-4o"}'` |
| AWS Bedrock | `bedrock` | `anthropic.claude-3-sonnet` | `npmai save-credentials bedrock '{"aws_access_key":"xxx","aws_secret_key":"xxx","region":"us-east-1"}'` |
| HuggingFace | `hf` | `mistralai/Mistral-7B-Instruct-v0.3` | `npmai save-credentials hf '{"api_key":"hf_xxx"}'` |
| llama.cpp | `llamacpp` | `/path/to/model.gguf` | Not required |

---

### `npmai chat` — Conversational Mode

Sends a message to the conversational chatter LLM without triggering the full 5-role agent pipeline. Only the chatter role's provider/model can be set — the other 4 roles aren't invoked at all in this mode.

| Parameter | Type | Default | Required | Description |
|---|---|---|---|---|
| `user_msg` | `str` | — | ✅ | Your message or question |
| `--chatter-model` | `str` | `granite3.3:2b` | ❌ | Model for the Chatter role |
| `--chatter-provider` | `str` | `npmai` | ❌ | Provider for the Chatter role |

```bash
npmai chat "What is the LARA RAG architecture?"

npmai chat "How do I use StripeTool to create a subscription?"

npmai chat "Explain what Tool Manager does in the pipeline" --chatter-provider groq --chatter-model llama-3.3-70b-versatile
```

**Output:** Direct conversational response, printed to the terminal.

---

### `npmai save-credentials` — Store API Keys

Saves credentials encrypted with a Fernet machine-specific key to `~/.npmai_agent/creds.json`. This is the only thing npmai_agents persists to disk — deliberately, since credentials are the one thing that genuinely needs to survive across separate CLI invocations.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | `str` | ✅ | Credential name/identifier |
| `data` | `str` | ✅ | JSON string of credential data |

```bash
npmai save-credentials github '{"token":"ghp_xxxxxxxxxxxx"}'
npmai save-credentials openai '{"api_key":"sk-xxxxxxxxxxxx"}'
npmai save-credentials groq '{"api_key":"gsk_xxxxxxxxxxxx"}'
npmai save-credentials stripe '{"secret_key":"sk_live_xxxxxxxxxxxx"}'
npmai save-credentials slack '{"bot_token":"xoxb-xxxxxxxxxxxx"}'
npmai save-credentials anthropic '{"api_key":"sk-ant-xxxxxxxxxxxx"}'
npmai save-credentials sendgrid '{"api_key":"SG.xxxxxxxxxxxx"}'
npmai save-credentials notion '{"token":"secret_xxxxxxxxxxxx"}'
```

> ⚠️ Rotate any key that's ever been typed into a shared terminal, chat log, or screen-share. `save-credentials` stores it encrypted at rest, but that doesn't protect a key that already leaked before it was saved.

---

### `npmai load-credentials` — Retrieve Stored Credentials

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | `str` | ✅ | Credential name to retrieve |

```bash
npmai load-credentials github
# Output: {"token": "ghp_xxxxxxxxxxxx"}

npmai load-credentials stripe
# Output: {"secret_key": "sk_live_xxxxxxxxxxxx"}
```

---

### `npmai all-credentials` — List All Stored Credential Names

```bash
npmai all-credentials
# Output: ['github', 'openai', 'groq', 'stripe', 'slack', 'sendgrid']
```

---

### `npmai workspace-scan` — Scan File System

Scans your file system and builds a workspace profile fed to the Planner before every task.

```bash
npmai workspace-scan
# Output: {"os": "Linux", "home": "/home/sonu", "desktop": [...], "documents": [...], ...}
```

---

### `npmai workspace-update` — Update Workspace Profile

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | `str` | ✅ | Profile key to update |
| `value` | `str` | ✅ | New value |

```bash
npmai workspace-update preferred_language Python
npmai workspace-update project_root /home/sonu/npmai-agent
```

---

### `npmai workspace-context` — View Context Summary

Shows the text summary sent to the Planner LLM before every task.

```bash
npmai workspace-context
# Output: "OS: Linux | Home: /home/sonu | Python: 3.11 | Projects: npmai-agent, npmai..."
```

---

## 🏗️ Pipeline Architecture

```
User Plain-English Task
         │
         ▼
┌──────────────────────────────┐
│   WORKSPACE SCANNER          │  scans Desktop/Documents/Downloads
│   Workspace.scan()           │  builds context for Planner
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   1. PLANNER LLM             │  sees: 100-class one-line index only
│   default: llama3.2:3b       │  returns: task summary + 2-5 steps
└──────────────┬───────────────┘
               │ (concise task summary)
               ▼
┌──────────────────────────────┐
│   2. TOOL MANAGER LLM        │  phase 1: shortlists 2-6 classes
│   default: llama3.2          │  phase 2: reads full `use` docs
└──────────────┬───────────────┘  returns: selected class docs only
               │ (selected tool docs)
               ▼
    ╔══════════════════════════╗
    ║   PER-STEP LOOP          ║  up to 12 retries per step
    ║                          ║  error fed back to Coder
    ║  3. CODER LLM            ║  sees: selected tool docs only
    ║  default: codellama:7b   ║  writes: complete executable .py
    ║                          ║
    ║  4. AUDITOR LLM          ║  sees: code only (security focus)
    ║  default: qwen2.5-coder  ║  ALLOW or BLOCK + reason
    ║                          ║
    ║  5. SUBPROCESS EXECUTOR  ║  isolated process execution
    ║                          ║
    ║  6. VERIFIER LLM         ║  sees: step + output only
    ║  default: llama3.2:3b    ║  YES (continue) or NO (retry)
    ╚══════════════════════════╝
               │
               ▼
         Task Complete ✓
```

| Role | Default Model | Fallback | Sees | Returns |
|---|---|---|---|---|
| 🗺️ Planner | `llama3.2:3b` | `mistral:7b` | 100-class one-line index | Task summary + steps |
| 🔎 Tool Manager | `llama3.2` | `gemma3:12b` | Index → selected `use` docs | Final tool documentation |
| 💻 Coder | `codellama:7b-instruct` | `deepseek-coder:6.7b` | Selected `use` docs only | Executable Python code |
| 🛡️ Auditor | `qwen2.5-coder:7b` | `falcon:7b-instruct` | Code only | ALLOW / BLOCK + reason |
| ✅ Verifier | `llama3.2:3b` | `mistral:7b` | Step + output only | YES / NO |

---

## 🔐 CredStore — Encrypted Credential Vault

Stores all API keys encrypted at `~/.npmai_agent/creds.json` using a machine-specific Fernet key. All 100 tool classes read credentials from here automatically.

**4 tools:** `save` · `load` · `all_keys` · `delete`

```python
from npmai_agents import CredStore

CredStore.save("stripe",    {"secret_key": "sk_live_xxxx"})
CredStore.save("github",    {"token": "ghp_xxxx"})
CredStore.save("openai",    {"api_key": "sk-xxxx"})
CredStore.save("sendgrid",  {"api_key": "SG.xxxx"})

creds  = CredStore.load("stripe")       # {"secret_key": "sk_live_xxxx"}
keys   = CredStore.all_keys()           # ['stripe', 'github', 'openai', 'sendgrid']
CredStore.delete("openai")
```

---

## 🖥️ Workspace

Scans user file system and builds context fed to Planner before every task.

**3 tools:** `scan` · `update_profile` · `context_summary`

```python
from npmai_agents import Workspace

ws = Workspace()
profile = ws.scan()
ws.update_profile("project_root", "/home/sonu/npmai")
print(ws.context_summary())
```

---

## 🛠️ Complete Tool Reference — 1,371 Tools Across 100 Classes

---

## ◈ Developer & CLI Tools — 155 Tools

---

### GitTool — 24 Tools
Local git version control — complete workflow from init to rebase.

```python
from npmai_agents import GitTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `init` | Initialise new repo | `path` |
| `clone` | Clone remote repo | `url, dest` |
| `status` | Show working tree status | `path` |
| `add` | Stage files | `path, files="."` |
| `commit` | Commit staged changes | `path, message` |
| `push` | Push to remote | `path, branch="main"` |
| `pull` | Pull from remote | `path, branch="main"` |
| `fetch` | Fetch remote changes | `path, remote="origin"` |
| `create_branch` | Create new branch | `path, branch_name` |
| `checkout` | Switch branch | `path, branch` |
| `merge` | Merge branch into current | `path, branch` |
| `log` | Show commit history | `path, limit=10` |
| `diff` | Show unstaged changes | `path` |
| `stash` | Stash working directory | `path` |
| `stash_pop` | Pop stash | `path` |
| `tag` | Create tag | `path, tag_name` |
| `reset` | Reset to commit | `path, commit="HEAD", mode="mixed"` |
| `rebase` | Rebase onto branch | `path, branch` |
| `cherry_pick` | Cherry-pick commit | `path, commit_hash` |
| `blame` | Show line authorship | `path, file` |
| `show` | Show commit details | `path, commit` |
| `remote_add` | Add remote | `path, name, url` |
| `remote_list` | List remotes | `path` |
| `submodule_init` | Init submodules | `path` |

```python
GitTool.init("/home/sonu/project")
GitTool.clone("https://github.com/sonuramashishnpm/npmai.git", "/home/sonu/npmai")
GitTool.add("/home/sonu/npmai", ".")
GitTool.commit("/home/sonu/npmai", "feat: add tool manager LLM role")
GitTool.create_branch("/home/sonu/npmai", "feature/tool-manager")
GitTool.push("/home/sonu/npmai", "feature/tool-manager")
GitTool.log("/home/sonu/npmai", limit=5)
```

---

### GitHubTool — 24 Tools
Full GitHub API — repos, issues, PRs, releases, Actions, files.

```python
from npmai_agents import GitHubTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_repo` | Create new repository | `name, private=False, description=""` |
| `delete_repo` | Delete repository | `owner, repo` |
| `fork_repo` | Fork a repository | `owner, repo` |
| `create_issue` | Create issue | `owner_repo, title, body, labels=[]` |
| `close_issue` | Close issue | `owner_repo, issue_number` |
| `list_issues` | List open issues | `owner_repo, state="open"` |
| `create_pr` | Create pull request | `owner_repo, title, base, head, body=""` |
| `merge_pr` | Merge pull request | `owner_repo, pr_number` |
| `list_prs` | List pull requests | `owner_repo, state="open"` |
| `review_pr` | Submit PR review | `owner_repo, pr_number, body, event` |
| `push_file` | Create/update file | `owner_repo, path, content, message` |
| `delete_file` | Delete file | `owner_repo, path, message` |
| `get_file` | Get file content | `owner_repo, path` |
| `list_files` | List directory contents | `owner_repo, path=""` |
| `create_release` | Create release | `owner_repo, tag, name, body=""` |
| `get_actions_status` | Get workflow runs | `owner_repo` |
| `trigger_workflow` | Trigger workflow | `owner_repo, workflow_file, ref="main"` |
| `list_branches` | List branches | `owner_repo` |
| `protect_branch` | Add branch protection | `owner_repo, branch` |
| `add_collaborator` | Add collaborator | `owner_repo, username, permission="push"` |
| `create_gist` | Create gist | `description, files, public=True` |
| `get_user_info` | Get user profile | `username` |
| `star_repo` | Star repository | `owner_repo` |
| `watch_repo` | Watch repository | `owner_repo` |

```python
GitHubTool.create_issue("sonuramashishnpm/npmai-agent", "Tool Manager integration", "Implement 2-phase tool selection", labels=["enhancement"])
GitHubTool.create_pr("sonuramashishnpm/npmai-agent", "feat: tool manager", "main", "feature/tool-manager")
GitHubTool.push_file("sonuramashishnpm/npmai-agent", "README.md", readme_content, "docs: update README to v1.0.0")
GitHubTool.create_release("sonuramashishnpm/npmai-agent", "v1.0.0", "Production Release", "1,371 tools across 100 classes")
GitHubTool.trigger_workflow("sonuramashishnpm/npmai-agent", "publish.yml")
```

---

### GitLabTool — 16 Tools
GitLab API — projects, issues, MRs, pipelines, members.

```python
from npmai_agents import GitLabTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_project` | Create new project | `name, description="", visibility="private"` |
| `list_projects` | List projects | `owned=True` |
| `get_project` | Get project details | `project_id` |
| `create_issue` | Create issue | `project_id, title, description=""` |
| `close_issue` | Close issue | `project_id, issue_iid` |
| `create_mr` | Create merge request | `project_id, title, source, target` |
| `merge_mr` | Merge MR | `project_id, mr_iid` |
| `list_pipelines` | List pipelines | `project_id` |
| `trigger_pipeline` | Trigger pipeline | `project_id, ref="main"` |
| `get_pipeline_jobs` | Get pipeline jobs | `project_id, pipeline_id` |
| `retry_job` | Retry failed job | `project_id, job_id` |
| `push_file` | Create/update file | `project_id, path, content, message` |
| `list_branches` | List branches | `project_id` |
| `create_branch` | Create branch | `project_id, branch, ref="main"` |
| `list_members` | List project members | `project_id` |
| `add_member` | Add member | `project_id, user_id, access_level=30` |

```python
GitLabTool.create_project("npmai-mirror", description="Mirror of npmai-agent", visibility="private")
GitLabTool.create_issue("12345678", "Add MCP hosting support", description="Expose search_tools/execute_tool")
GitLabTool.create_mr("12345678", "feat: mcp hosting", source="feature/mcp", target="main")
GitLabTool.trigger_pipeline("12345678", ref="main")
```

---

### DockerTool — 26 Tools
Full Docker control — images, containers, networks, volumes, Compose.

```python
from npmai_agents import DockerTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `build_image` | Build image from Dockerfile | `context_path, tag, dockerfile="Dockerfile"` |
| `push_image` | Push to registry | `tag` |
| `pull_image` | Pull from registry | `image` |
| `tag_image` | Tag image | `source, target` |
| `remove_image` | Remove image | `image, force=False` |
| `list_images` | List local images | — |
| `run_container` | Run container | `image, name="", ports={}, env={}, volumes={}` |
| `stop_container` | Stop container | `name` |
| `start_container` | Start stopped container | `name` |
| `remove_container` | Remove container | `name, force=False` |
| `exec_in_container` | Run command in container | `name, command` |
| `get_logs` | Get container logs | `name, tail=100` |
| `list_containers` | List containers | `all=False` |
| `inspect_container` | Full container details | `name` |
| `create_network` | Create network | `name, driver="bridge"` |
| `list_networks` | List networks | — |
| `remove_network` | Remove network | `name` |
| `create_volume` | Create volume | `name` |
| `list_volumes` | List volumes | — |
| `remove_volume` | Remove volume | `name, force=False` |
| `compose_up` | docker-compose up | `path, detach=True` |
| `compose_down` | docker-compose down | `path` |
| `compose_logs` | View compose logs | `path, service=""` |
| `compose_ps` | List compose services | `path` |
| `login` | Login to registry | `username, password, registry=""` |
| `system_prune` | Remove unused resources | `force=False` |

```python
DockerTool.build_image("/home/sonu/app", tag="npmai-app:1.0.0")
DockerTool.run_container("npmai-app:1.0.0", name="npmai", ports={"8080": "80"}, env={"DEBUG": "false"})
DockerTool.exec_in_container("npmai", "python manage.py migrate")
DockerTool.get_logs("npmai", tail=50)
DockerTool.compose_up("/home/sonu/app")
```

---

### PackageManagerTool — 22 Tools
pip, npm, yarn, cargo, go — all in one class.

```python
from npmai_agents import PackageManagerTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `pip_install` | Install Python package | `package, version=""` |
| `pip_uninstall` | Uninstall package | `package` |
| `pip_list` | List installed packages | — |
| `pip_show` | Show package info | `package` |
| `pip_freeze` | Export requirements | `output_file=""` |
| `npm_install` | npm install | `package="", save_dev=False` |
| `npm_uninstall` | npm uninstall | `package` |
| `npm_run` | Run npm script | `script, cwd="."` |
| `npm_build` | npm build | `cwd="."` |
| `npm_publish` | npm publish | `cwd="."` |
| `npm_list` | List npm packages | `cwd="."` |
| `npm_update` | Update packages | `cwd="."` |
| `npm_audit` | Security audit | `cwd="."` |
| `yarn_install` | yarn install | `cwd="."` |
| `yarn_add` | Add package | `package, dev=False, cwd="."` |
| `yarn_remove` | Remove package | `package, cwd="."` |
| `cargo_build` | Build Rust project | `cwd=".", release=False` |
| `cargo_test` | Run Rust tests | `cwd="."` |
| `cargo_run` | Run Rust binary | `cwd="."` |
| `go_build` | Build Go project | `cwd="."` |
| `go_test` | Run Go tests | `cwd="."` |
| `go_get` | Get Go package | `package` |

```python
PackageManagerTool.pip_install("requests", version=">=2.31.0")
PackageManagerTool.npm_install(cwd="/home/sonu/frontend")
PackageManagerTool.npm_run("build", cwd="/home/sonu/frontend")
PackageManagerTool.cargo_build(cwd="/home/sonu/rust-tool", release=True)
```

---

### VSCodeTool — 13 Tools
Control VS Code programmatically.

```python
from npmai_agents import VSCodeTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `open_file` | Open file in VS Code | `file_path` |
| `open_folder` | Open folder | `folder_path` |
| `install_extension` | Install extension | `extension_id` |
| `uninstall_extension` | Uninstall extension | `extension_id` |
| `list_extensions` | List installed extensions | — |
| `run_task` | Run defined task | `task_name, cwd="."` |
| `open_terminal` | Open integrated terminal | — |
| `apply_settings` | Apply settings JSON | `settings: dict` |
| `get_settings` | Get current settings | — |
| `format_file` | Format file | `file_path` |
| `lint_workspace` | Lint workspace | `cwd="."` |
| `create_workspace` | Create .code-workspace | `name, folders: list` |
| `open_workspace` | Open workspace file | `workspace_path` |

```python
VSCodeTool.open_folder("/home/sonu/npmai-agent")
VSCodeTool.install_extension("ms-python.python")
VSCodeTool.format_file("/home/sonu/npmai-agent/npmai_agent/cli.py")
```

---

### TerminalTool — 15 Tools
Shell execution, environment variables, process management.

```python
from npmai_agents import TerminalTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `run` | Execute shell command | `command, cwd=".", timeout=60` |
| `run_interactive` | Run interactive command | `command, cwd="."` |
| `run_script` | Execute script file | `script_path, interpreter="bash"` |
| `run_in_new_terminal` | Open new terminal window | `command` |
| `set_env_var` | Set environment variable | `key, value` |
| `get_env_var` | Get environment variable | `key` |
| `list_env_vars` | List all env vars | — |
| `source_file` | Source env file | `file_path` |
| `which` | Find command path | `command` |
| `is_installed` | Check if tool installed | `command` |
| `install_via_package_manager` | Auto-install tool | `package` |
| `create_alias` | Create shell alias | `name, command` |
| `list_processes` | List running processes | `filter=""` |
| `kill_process` | Kill process by name/PID | `target` |
| `get_process_info` | Get process details | `pid` |

```python
TerminalTool.run("pytest tests/ -v", cwd="/home/sonu/npmai-agent")
TerminalTool.set_env_var("GROQ_API_KEY", "gsk_xxxx")
TerminalTool.is_installed("docker")
```

---

### MakefileTool — 4 Tools

```python
from npmai_agents import MakefileTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `run_target` | Run make target | `target, cwd="."` |
| `list_targets` | List available targets | `cwd="."` |
| `create_makefile` | Create new Makefile | `path, targets: dict` |
| `add_target` | Add target to Makefile | `path, name, commands: list, deps=[]` |

```python
MakefileTool.create_makefile("/home/sonu/app", targets={"build": ["go build ."], "test": ["go test ./..."]})
MakefileTool.run_target("test", cwd="/home/sonu/app")
```

---

### CMakeTool — 5 Tools

```python
from npmai_agents import CMakeTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `configure` | Run cmake configure | `source_dir, build_dir, options={}` |
| `build` | Build project | `build_dir, target="", jobs=4` |
| `install` | Install build | `build_dir, prefix=""` |
| `clean` | Clean build dir | `build_dir` |
| `run_ctest` | Run tests | `build_dir, verbose=False` |

```python
CMakeTool.configure("/home/sonu/cpp-proj", "/home/sonu/cpp-proj/build")
CMakeTool.build("/home/sonu/cpp-proj/build", jobs=8)
CMakeTool.run_ctest("/home/sonu/cpp-proj/build", verbose=True)
```

---

### DebuggerTool — 6 Tools

```python
from npmai_agents import DebuggerTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `run_python_with_pdb` | Run with pdb debugger | `script_path, breakpoints=[]` |
| `analyze_traceback` | Parse and explain traceback | `traceback_text` |
| `profile_script` | Profile script performance | `script_path, output=""` |
| `memory_profile` | Profile memory usage | `script_path` |
| `find_deadlocks` | Detect thread deadlocks | `pid` |
| `strace_process` | Trace system calls | `pid, output=""` |

```python
DebuggerTool.analyze_traceback(captured_traceback_text)
DebuggerTool.profile_script("/home/sonu/npmai-agent/npmai_agent/npmai_agents.py")
```

---

## ◈ Business & Payments — 152 Tools

---

### StripeTool — 29 Tools
Complete Stripe payments — customers, intents, subscriptions, invoices, payouts.

```python
from npmai_agents import StripeTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_customer` | Create customer | `email, name, phone=""` |
| `get_customer` | Get customer | `customer_id` |
| `update_customer` | Update customer | `customer_id, **kwargs` |
| `list_customers` | List customers | `limit=10, email=""` |
| `delete_customer` | Delete customer | `customer_id` |
| `create_payment_intent` | Create payment intent | `amount, currency="inr", customer_id=""` |
| `confirm_payment` | Confirm payment intent | `payment_intent_id, payment_method` |
| `create_charge` | Create charge | `amount, currency, source, description=""` |
| `capture_charge` | Capture authorised charge | `charge_id` |
| `refund_charge` | Refund charge | `charge_id, amount=None` |
| `list_charges` | List charges | `limit=10, customer_id=""` |
| `create_subscription` | Create subscription | `customer_id, price_id` |
| `cancel_subscription` | Cancel subscription | `subscription_id` |
| `update_subscription` | Update subscription | `subscription_id, **kwargs` |
| `list_subscriptions` | List subscriptions | `customer_id=""` |
| `create_product` | Create product | `name, description=""` |
| `create_price` | Create price | `product_id, amount, currency, interval=""` |
| `create_invoice` | Create invoice | `customer_id, auto_advance=True` |
| `finalize_invoice` | Finalise invoice | `invoice_id` |
| `pay_invoice` | Pay invoice | `invoice_id` |
| `list_invoices` | List invoices | `customer_id=""` |
| `send_invoice` | Email invoice to customer | `invoice_id` |
| `create_coupon` | Create coupon | `percent_off, duration="once"` |
| `apply_coupon` | Apply coupon to customer | `customer_id, coupon_id` |
| `create_payment_link` | Create payment link | `price_id, quantity=1` |
| `list_payment_methods` | List saved payment methods | `customer_id, type="card"` |
| `get_balance` | Get account balance | — |
| `list_transactions` | List balance transactions | `limit=10` |
| `create_payout` | Create payout | `amount, currency="inr"` |

```python
cid = StripeTool.create_customer(email="sonu@npmai.ai", name="Sonu Kumar")["id"]
StripeTool.create_subscription(customer_id=cid, price_id="price_xxxxx")
inv = StripeTool.create_invoice(customer_id=cid)["id"]
StripeTool.finalize_invoice(invoice_id=inv)
StripeTool.pay_invoice(invoice_id=inv)
StripeTool.create_payout(amount=50000, currency="inr")
```

---

### RazorpayTool — 18 Tools
Indian payment gateway — orders, capture, refunds, subscriptions, QR codes.

```python
from npmai_agents import RazorpayTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_order` | Create payment order | `amount, currency="INR", notes={}` |
| `get_order` | Get order details | `order_id` |
| `list_orders` | List orders | `count=10` |
| `fetch_payment` | Fetch payment details | `payment_id` |
| `capture_payment` | Capture payment | `payment_id, amount` |
| `refund_payment` | Refund payment | `payment_id, amount=None` |
| `list_payments` | List payments | `count=10` |
| `create_refund` | Create refund | `payment_id, amount, notes={}` |
| `create_customer` | Create customer | `name, email, contact` |
| `get_customer` | Get customer | `customer_id` |
| `create_subscription` | Create subscription | `plan_id, customer_id, total_count` |
| `create_plan` | Create billing plan | `period, interval, name, amount, currency="INR"` |
| `list_plans` | List plans | `count=10` |
| `create_payment_link` | Create payment link | `amount, currency="INR", description=""` |
| `list_payment_links` | List payment links | `count=10` |
| `create_qr_code` | Create QR for payment | `type="upi_qr", name="", description=""` |
| `get_settlements` | Get settlements | — |
| `get_settlement_transactions` | Get settlement TXNs | `settlement_id` |

```python
order = RazorpayTool.create_order(amount=50000, currency="INR", notes={"purpose": "invoice #221"})
RazorpayTool.create_qr_code(type="upi_qr", name="Sonu Store")
RazorpayTool.refund_payment(payment_id="pay_xxxx")
```

---

### ShopifyTool — 25 Tools
Complete Shopify store — products, orders, customers, inventory, discounts.

```python
from npmai_agents import ShopifyTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `list_products` | List products | `limit=50` |
| `get_product` | Get product | `product_id` |
| `create_product` | Create product | `title, body_html="", vendor="", product_type=""` |
| `update_product` | Update product | `product_id, **kwargs` |
| `delete_product` | Delete product | `product_id` |
| `list_variants` | List product variants | `product_id` |
| `update_variant` | Update variant | `variant_id, **kwargs` |
| `list_orders` | List orders | `status="any", limit=50` |
| `get_order` | Get order | `order_id` |
| `update_order` | Update order | `order_id, **kwargs` |
| `cancel_order` | Cancel order | `order_id, reason=""` |
| `fulfill_order` | Fulfill order | `order_id, tracking_number=""` |
| `list_customers` | List customers | `limit=50` |
| `get_customer` | Get customer | `customer_id` |
| `create_customer` | Create customer | `first_name, last_name, email` |
| `search_customers` | Search customers | `query` |
| `list_customer_orders` | Get customer orders | `customer_id` |
| `get_inventory_levels` | Get inventory | `location_id=""` |
| `adjust_inventory` | Adjust stock level | `inventory_item_id, location_id, adjustment` |
| `list_collections` | List collections | — |
| `create_collection` | Create collection | `title, body_html=""` |
| `create_discount` | Create discount code | `code, value, value_type="percentage"` |
| `get_shop_info` | Get shop details | — |
| `list_locations` | List store locations | — |
| `get_analytics` | Get sales analytics | `period="day"` |

```python
ShopifyTool.create_product(title="NPMAI Hoodie", vendor="NPMAI Merch", product_type="Apparel")
ShopifyTool.adjust_inventory(inventory_item_id="123", location_id="456", adjustment=-2)
ShopifyTool.create_discount(code="NPMAI10", value=10, value_type="percentage")
```

---

### InvoiceTool — 8 Tools

```python
from npmai_agents import InvoiceTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_invoice` | Generate PDF invoice | `client, items: list, output_path` |
| `create_quote` | Generate quote | `client, items: list, output_path` |
| `create_receipt` | Generate receipt | `client, items: list, output_path` |
| `create_purchase_order` | Generate PO | `vendor, items: list, output_path` |
| `send_invoice_email` | Email invoice | `invoice_path, to_email, subject=""` |
| `batch_create_invoices` | Bulk invoice generation | `data: list, output_dir` |
| `extract_invoice_data` | AI extract from image/PDF | `file_path` |
| `create_recurring_invoice` | Set recurring invoice | `client, items, interval="monthly"` |

```python
InvoiceTool.create_invoice(client="Acme Pvt Ltd", items=[{"desc": "Consulting", "qty": 1, "rate": 25000}], output_path="invoice_221.pdf")
InvoiceTool.send_invoice_email("invoice_221.pdf", to_email="acme@example.com", subject="Invoice #221")
```

---

### AccountingTool — 10 Tools

```python
from npmai_agents import AccountingTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `calculate_gst` | Calculate GST | `amount, rate=18, inclusive=False` |
| `calculate_vat` | Calculate VAT | `amount, rate, inclusive=False` |
| `generate_profit_loss` | P&L statement | `revenue: list, expenses: list, period=""` |
| `generate_balance_sheet` | Balance sheet | `assets: dict, liabilities: dict` |
| `generate_cash_flow` | Cash flow statement | `operations: list, investing: list, financing: list` |
| `depreciation_schedule` | Asset depreciation | `asset_cost, salvage, life, method="straight_line"` |
| `currency_convert` | Convert currencies | `amount, from_currency, to_currency` |
| `get_exchange_rates` | Get current FX rates | `base="INR"` |
| `track_expenses` | Log expense | `amount, category, description, date=""` |
| `calculate_tax_liability` | Tax calculation | `income, deductions: dict, regime="new"` |

```python
AccountingTool.calculate_gst(amount=10000, rate=18)
AccountingTool.currency_convert(amount=100, from_currency="USD", to_currency="INR")
AccountingTool.calculate_tax_liability(income=1200000, deductions={"80C": 150000}, regime="new")
```

---

### CRMTool — 18 Tools
Local SQLite CRM — contacts, deals, pipeline, activities, reports.

```python
from npmai_agents import CRMTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `add_contact` | Add contact | `name, email, phone="", company=""` |
| `update_contact` | Update contact | `contact_id, **kwargs` |
| `delete_contact` | Delete contact | `contact_id` |
| `list_contacts` | List all contacts | `search=""` |
| `search_contacts` | Search contacts | `query` |
| `import_contacts_csv` | Import from CSV | `csv_path` |
| `export_contacts` | Export to CSV | `output_path` |
| `merge_duplicate_contacts` | Merge duplicates | `contact_id_1, contact_id_2` |
| `add_deal` | Add deal to pipeline | `title, value, contact_id, stage="lead"` |
| `update_deal` | Update deal | `deal_id, **kwargs` |
| `close_deal` | Mark deal closed/won | `deal_id, won=True` |
| `list_deals` | List all deals | `stage=""` |
| `get_pipeline_value` | Total pipeline value | `stage=""` |
| `add_activity` | Log activity | `contact_id, type, notes=""` |
| `list_activities` | List activities | `contact_id=""` |
| `set_reminder` | Set follow-up reminder | `contact_id, date, message` |
| `generate_sales_report` | Sales summary | `period="month"` |
| `get_conversion_rate` | Lead conversion rate | `period="month"` |

```python
cid = CRMTool.add_contact(name="Ravi Sharma", email="ravi@example.com", company="Acme")
CRMTool.add_deal(title="Enterprise plan", value=200000, contact_id=cid, stage="negotiation")
CRMTool.generate_sales_report(period="month")
```

---

### EmailMarketingTool — 13 Tools

```python
from npmai_agents import EmailMarketingTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_campaign` | Create email campaign | `name, subject, list_id, template_id` |
| `schedule_campaign` | Schedule campaign | `campaign_id, send_time` |
| `send_campaign_now` | Send immediately | `campaign_id` |
| `create_list` | Create subscriber list | `name` |
| `add_subscriber` | Add subscriber | `list_id, email, name=""` |
| `remove_subscriber` | Remove subscriber | `list_id, email` |
| `import_subscribers` | Bulk import | `list_id, csv_path` |
| `get_campaign_stats` | Get campaign metrics | `campaign_id` |
| `get_list_stats` | Get list stats | `list_id` |
| `create_automation` | Create email automation | `name, trigger, emails: list` |
| `create_template` | Create email template | `name, html_content` |
| `unsubscribe` | Unsubscribe email | `email` |
| `get_unsubscribes` | Get unsubscribe list | `list_id` |

```python
lid = EmailMarketingTool.create_list("npmai-newsletter")
EmailMarketingTool.add_subscriber(list_id=lid, email="reader@example.com")
EmailMarketingTool.create_campaign(name="July Update", subject="What's new in npmai_agents", list_id=lid, template_id="tmpl_1")
```

---

### AnalyticsTool — 9 Tools

```python
from npmai_agents import AnalyticsTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `connect_google_analytics` | Connect GA4 | `property_id, credentials_path` |
| `get_sessions` | Get session data | `start_date, end_date` |
| `get_top_pages` | Top pages by views | `start_date, end_date, limit=10` |
| `get_traffic_sources` | Traffic source breakdown | `start_date, end_date` |
| `get_conversions` | Conversion events | `start_date, end_date, event=""` |
| `get_realtime_users` | Realtime active users | — |
| `create_custom_report` | Custom dimensions report | `dimensions: list, metrics: list, date_range` |
| `generate_weekly_report` | Auto weekly report | `output_path=""` |
| `track_event` | Track custom event | `event_name, params={}` |

```python
AnalyticsTool.connect_google_analytics(property_id="123456789", credentials_path="/home/sonu/ga.json")
AnalyticsTool.get_top_pages("2026-06-01", "2026-06-30", limit=5)
AnalyticsTool.generate_weekly_report(output_path="weekly_report.pdf")
```

---

### InventoryTool — 12 Tools

```python
from npmai_agents import InventoryTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `add_product` | Add product to inventory | `name, sku, quantity, cost, price` |
| `update_stock` | Update stock level | `sku, quantity, operation="set"` |
| `get_stock_level` | Get stock for SKU | `sku` |
| `list_low_stock` | Items below threshold | `threshold=10` |
| `list_out_of_stock` | Out of stock items | — |
| `get_inventory_value` | Total inventory value | — |
| `record_sale` | Record a sale | `sku, quantity, price` |
| `record_purchase` | Record a purchase | `sku, quantity, cost` |
| `generate_stock_report` | Full stock report | `output_path=""` |
| `forecast_demand` | Demand forecasting | `sku, days_ahead=30` |
| `export_inventory` | Export to CSV/Excel | `output_path` |
| `import_inventory` | Import from CSV | `csv_path` |

```python
InventoryTool.add_product(name="NPMAI T-Shirt", sku="TSHIRT-001", quantity=100, cost=150, price=499)
InventoryTool.record_sale(sku="TSHIRT-001", quantity=2, price=499)
InventoryTool.list_low_stock(threshold=10)
```

---

### ContractTool — 10 Tools

```python
from npmai_agents import ContractTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_nda` | Generate NDA | `party_1, party_2, duration="1 year", output_path=""` |
| `create_service_agreement` | Service agreement | `provider, client, services: list, rate, output_path=""` |
| `create_employment_contract` | Employment contract | `employee, employer, role, salary, output_path=""` |
| `fill_template` | Fill contract template | `template_path, variables: dict, output_path` |
| `extract_key_terms` | AI extract key terms | `contract_path` |
| `summarize_contract` | AI summarise contract | `contract_path, max_words=300` |
| `check_contract_dates` | Check expiry dates | `contract_path` |
| `compare_contracts` | Compare two contracts | `path_1, path_2` |
| `add_signature_field` | Add signature field | `contract_path, page, x, y` |
| `verify_signature` | Verify digital signature | `contract_path` |

```python
ContractTool.create_nda(party_1="NPMAI Ecosystem", party_2="Contractor Name", duration="2 years", output_path="nda.pdf")
ContractTool.extract_key_terms("nda.pdf")
```

---

## ◈ Cloud & DevOps — 149 Tools

---

### AWSS3Tool — 16 Tools

```python
from npmai_agents import AWSS3Tool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_bucket` | Create S3 bucket | `bucket_name, region="ap-south-1"` |
| `delete_bucket` | Delete bucket | `bucket_name` |
| `upload_file` | Upload file | `bucket, local_path, s3_key=""` |
| `upload_folder` | Upload directory | `bucket, local_dir, s3_prefix=""` |
| `download_file` | Download file | `bucket, s3_key, local_path` |
| `download_folder` | Download prefix | `bucket, s3_prefix, local_dir` |
| `list_objects` | List objects | `bucket, prefix=""` |
| `delete_object` | Delete object | `bucket, s3_key` |
| `copy_object` | Copy object | `src_bucket, src_key, dst_bucket, dst_key` |
| `get_presigned_url` | Generate presigned URL | `bucket, s3_key, expires=3600` |
| `set_bucket_policy` | Set bucket policy | `bucket, policy: dict` |
| `enable_static_website` | Enable static hosting | `bucket, index="index.html"` |
| `sync_folder` | Sync local↔S3 | `bucket, local_dir, s3_prefix=""` |
| `get_object_metadata` | Get object metadata | `bucket, s3_key` |
| `list_buckets` | List all buckets | — |
| `get_bucket_size` | Get total bucket size | `bucket` |

```python
AWSS3Tool.create_bucket("npmai-agent-assets")
AWSS3Tool.upload_file("npmai-agent-assets", "/home/sonu/build.zip", s3_key="releases/build.zip")
AWSS3Tool.get_presigned_url("npmai-agent-assets", "releases/build.zip", expires=3600)
```

---

### AWSLambdaTool — 12 Tools

```python
from npmai_agents import AWSLambdaTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_function` | Create Lambda function | `name, runtime, handler, zip_path, role_arn` |
| `update_function_code` | Update function code | `name, zip_path` |
| `update_function_config` | Update config | `name, **kwargs` |
| `invoke_function` | Invoke function | `name, payload={}` |
| `delete_function` | Delete function | `name` |
| `list_functions` | List all functions | — |
| `get_function` | Get function details | `name` |
| `add_layer` | Attach Lambda layer | `function_name, layer_arn` |
| `create_trigger_s3` | Add S3 trigger | `function_name, bucket, events=["s3:ObjectCreated:*"]` |
| `create_trigger_api_gateway` | Add API Gateway trigger | `function_name, api_id` |
| `get_logs` | Get CloudWatch logs | `function_name, limit=100` |
| `list_versions` | List function versions | `function_name` |

```python
AWSLambdaTool.create_function(name="npmai-webhook", runtime="python3.12", handler="app.handler", zip_path="lambda.zip", role_arn="arn:aws:iam::123:role/lambda-exec")
AWSLambdaTool.invoke_function(name="npmai-webhook", payload={"event": "test"})
```

---

### AWSECSTool — 11 Tools

```python
from npmai_agents import AWSECSTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_cluster` | Create ECS cluster | `name` |
| `delete_cluster` | Delete cluster | `name` |
| `register_task_definition` | Register task def | `family, containers: list, cpu="256", memory="512"` |
| `run_task` | Run task | `cluster, task_definition, launch_type="FARGATE"` |
| `stop_task` | Stop task | `cluster, task_arn` |
| `list_tasks` | List running tasks | `cluster, status="RUNNING"` |
| `create_service` | Create service | `cluster, name, task_def, desired_count=1` |
| `update_service` | Update service | `cluster, name, desired_count=None, task_def=""` |
| `delete_service` | Delete service | `cluster, name` |
| `describe_tasks` | Describe tasks | `cluster, task_arns: list` |
| `get_task_logs` | Get task logs | `cluster, task_arn` |

```python
AWSECSTool.create_cluster("npmai-cluster")
AWSECSTool.create_service("npmai-cluster", name="agent-api", task_def="agent-task:1", desired_count=2)
```

---

### CloudflareTool — 20 Tools

```python
from npmai_agents import CloudflareTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `list_zones` | List zones | — |
| `get_zone` | Get zone details | `zone_id` |
| `create_dns_record` | Create DNS record | `zone_id, type, name, content, ttl=1` |
| `update_dns_record` | Update DNS record | `zone_id, record_id, **kwargs` |
| `delete_dns_record` | Delete DNS record | `zone_id, record_id` |
| `list_dns_records` | List DNS records | `zone_id, type=""` |
| `purge_cache` | Purge all cache | `zone_id, urls=[]` |
| `get_analytics` | Zone analytics | `zone_id, period="-10080"` |
| `create_worker` | Create Worker | `name, script` |
| `update_worker` | Update Worker | `name, script` |
| `delete_worker` | Delete Worker | `name` |
| `list_workers` | List Workers | — |
| `set_worker_route` | Set Worker route | `zone_id, pattern, worker_name` |
| `create_kv_namespace` | Create KV namespace | `title` |
| `write_kv` | Write KV value | `namespace_id, key, value` |
| `read_kv` | Read KV value | `namespace_id, key` |
| `delete_kv` | Delete KV key | `namespace_id, key` |
| `list_kv` | List KV keys | `namespace_id` |
| `get_firewall_rules` | Get firewall rules | `zone_id` |
| `create_firewall_rule` | Create firewall rule | `zone_id, expression, action="block"` |

```python
CloudflareTool.create_dns_record(zone_id="abc123", type="A", name="agent.npmai.ai", content="1.2.3.4")
CloudflareTool.purge_cache(zone_id="abc123")
CloudflareTool.create_worker(name="edge-router", script=worker_js_code)
```

---

### VercelTool — 13 Tools · NetlifyTool — 13 Tools · RailwayTool — 10 Tools

```python
from npmai_agents import VercelTool, NetlifyTool, RailwayTool
```

**VercelTool:** `deploy` · `list_deployments` · `get_deployment` · `delete_deployment` · `list_projects` · `create_project` · `delete_project` · `set_env_var` · `list_env_vars` · `get_deployment_logs` · `rollback` · `add_domain` · `list_domains`

**NetlifyTool:** `list_sites` · `create_site` · `delete_site` · `deploy_folder` · `list_deploys` · `rollback_deploy` · `lock_deploy` · `set_env_var` · `list_env_vars` · `delete_env_var` · `add_domain` · `list_forms` · `get_form_submissions`

**RailwayTool:** `deploy` · `list_projects` · `create_project` · `list_services` · `deploy_service` · `restart_service` · `set_env_var` · `list_env_vars` · `get_logs` · `get_deployments`

```python
VercelTool.deploy("/home/sonu/npmai-web")
NetlifyTool.deploy_folder("/home/sonu/npmai-web/dist", site_id="xyz")
RailwayTool.deploy_service(project_id="proj_1", service_id="svc_1")
```

---

### KubernetesTool — 24 Tools

```python
from npmai_agents import KubernetesTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `apply` | Apply YAML manifest | `manifest_path` |
| `delete_resource` | Delete resource | `resource_type, name, namespace="default"` |
| `get_pods` | List pods | `namespace="default", label=""` |
| `describe_pod` | Describe pod | `name, namespace="default"` |
| `get_pod_logs` | Get pod logs | `name, namespace="default", tail=100` |
| `exec_in_pod` | Execute in pod | `name, command, namespace="default"` |
| `get_deployments` | List deployments | `namespace="default"` |
| `scale_deployment` | Scale deployment | `name, replicas, namespace="default"` |
| `rollout_restart` | Restart deployment | `name, namespace="default"` |
| `rollout_status` | Check rollout status | `name, namespace="default"` |
| `get_services` | List services | `namespace="default"` |
| `port_forward` | Port forward | `resource, local_port, remote_port, namespace="default"` |
| `get_nodes` | List nodes | — |
| `cordon_node` | Cordon node | `node_name` |
| `drain_node` | Drain node | `node_name` |
| `apply_secret` | Create/update secret | `name, data: dict, namespace="default"` |
| `get_configmap` | Get ConfigMap | `name, namespace="default"` |
| `create_namespace` | Create namespace | `name` |
| `list_namespaces` | List namespaces | — |
| `get_resource_usage` | Get resource usage | `namespace="default"` |
| `helm_install` | Helm chart install | `release_name, chart, values={}` |
| `helm_upgrade` | Helm chart upgrade | `release_name, chart, values={}` |
| `helm_uninstall` | Helm chart uninstall | `release_name` |
| `helm_list` | List Helm releases | — |

```python
KubernetesTool.apply("/home/sonu/k8s/deployment.yaml")
KubernetesTool.scale_deployment("agent-api", replicas=3, namespace="prod")
KubernetesTool.get_pod_logs("agent-api-6f9d", namespace="prod", tail=200)
```

---

### TerraformTool — 16 Tools · MonitoringTool — 14 Tools

```python
from npmai_agents import TerraformTool, MonitoringTool
```

**TerraformTool:** `init` · `plan` · `apply` · `destroy` · `validate` · `fmt` · `show` · `output` · `state_list` · `state_show` · `state_rm` · `import_resource` · `graph` · `workspace_list` · `workspace_new` · `workspace_select`

**MonitoringTool:** `get_cpu_usage` · `get_memory_info` · `get_disk_usage` · `get_network_io` · `get_process_list` · `kill_process` · `get_gpu_info` · `watch_file_changes` · `get_open_ports` · `check_service_health` · `send_alert` · `get_system_info` · `tail_log_file` · `parse_log_file`

```python
TerraformTool.init("/home/sonu/infra")
TerraformTool.plan("/home/sonu/infra")
TerraformTool.apply("/home/sonu/infra")
MonitoringTool.check_service_health("npmai-agent-api")
MonitoringTool.send_alert("Disk usage above 90% on prod-1")
```

---

## ◈ Communication — 95 Tools

---

### TwilioTool — 12 Tools

```python
from npmai_agents import TwilioTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `send_sms` | Send SMS | `to, body, from_=""` |
| `send_bulk_sms` | Bulk SMS | `numbers: list, body` |
| `make_call` | Voice call with TTS | `to, message, from_=""` |
| `get_call_status` | Check call status | `call_sid` |
| `send_whatsapp` | Send WhatsApp message | `to, body` |
| `send_whatsapp_template` | Template WhatsApp | `to, template_sid, variables: list` |
| `get_message_status` | Check message status | `message_sid` |
| `list_messages` | List messages | `limit=20` |
| `verify_phone` | Send OTP | `to, channel="sms"` |
| `check_verification` | Check OTP | `to, code` |
| `create_subaccount` | Create subaccount | `friendly_name` |
| `get_account_balance` | Get balance | — |

```python
TwilioTool.send_sms(to="+919876543210", body="Your NPMAI order has shipped.")
TwilioTool.verify_phone(to="+919876543210", channel="sms")
TwilioTool.check_verification(to="+919876543210", code="123456")
```

---

### SendGridTool — 14 Tools

```python
from npmai_agents import SendGridTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `send_email` | Send transactional email | `to, subject, body, from_email=""` |
| `send_bulk` | Bulk email send | `recipients: list, subject, body` |
| `send_with_template` | Template email | `to, template_id, data: dict` |
| `create_template` | Create email template | `name, html_content` |
| `update_template` | Update template | `template_id, html_content` |
| `list_templates` | List templates | — |
| `create_contact_list` | Create contact list | `name` |
| `add_contacts` | Add contacts to list | `list_id, contacts: list` |
| `create_campaign` | Create campaign | `title, subject, list_ids: list, template_id` |
| `schedule_campaign` | Schedule send | `campaign_id, send_at` |
| `get_stats` | Email statistics | `start_date, end_date` |
| `get_bounces` | List bounced emails | — |
| `delete_bounce` | Remove from bounce list | `email` |
| `get_spam_reports` | List spam reports | — |

```python
SendGridTool.send_email(to="sonu@npmai.ai", subject="Weekly Revenue Report", body="See attached.")
SendGridTool.get_stats("2026-06-01", "2026-06-30")
```

---

### CalendarTool — 11 Tools

```python
from npmai_agents import CalendarTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `list_events` | List upcoming events | `max_results=10, calendar_id="primary"` |
| `create_event` | Create event | `summary, start, end, description="", attendees=[]` |
| `update_event` | Update event | `event_id, **kwargs` |
| `delete_event` | Delete event | `event_id, calendar_id="primary"` |
| `quick_add_event` | Natural language add | `text, calendar_id="primary"` |
| `list_calendars` | List all calendars | — |
| `create_calendar` | Create new calendar | `summary, timezone="Asia/Kolkata"` |
| `find_free_slots` | Find free time | `duration_minutes=60, days_ahead=7, working_hours=(9,18)` |
| `send_invite` | Send event invite | `event_id, email` |
| `sync_to_local` | Export to local ICS | `output_path, max_results=100` |
| `import_ical` | Import ICS file | `ical_path, calendar_id="primary"` |

```python
CalendarTool.quick_add_event("Team sync tomorrow 5pm")
CalendarTool.find_free_slots(duration_minutes=30, days_ahead=3)
```

---

### ZoomTool — 10 Tools · MicrosoftTeamsTool — 5 Tools · TwilioTool (above) · PushNotificationTool — 7 Tools · RSSFeedTool — 9 Tools · WebhookTool — 8 Tools · ChatOpsAutomationTool — 9 Tools · SMTPAdvancedTool — 10 Tools

```python
from npmai_agents import ZoomTool, MicrosoftTeamsTool, PushNotificationTool
from npmai_agents import RSSFeedTool, WebhookTool, ChatOpsAutomationTool, SMTPAdvancedTool
```

**ZoomTool:** `create_meeting` · `list_meetings` · `get_meeting` · `update_meeting` · `delete_meeting` · `get_meeting_participants` · `get_recording` · `list_recordings` · `create_webinar` · `get_registrants`

**MicrosoftTeamsTool:** `send_message` · `send_adaptive_card` · `send_file_notification` · `create_channel_message_with_mention` · `send_approval_request`

**PushNotificationTool:** `send_fcm` · `send_fcm_bulk` · `send_fcm_topic` · `send_apns` · `send_web_push` · `send_pushbullet` · `send_pushover`

**RSSFeedTool:** `parse_feed` · `monitor_feed` · `compare_feeds` · `get_new_items` · `create_rss_feed` · `aggregate_feeds` · `search_in_feed` · `export_feed_items` · `subscribe_and_notify`

**WebhookTool:** `start_webhook_server` · `verify_signature` · `register_webhook` · `list_registered_webhooks` · `test_webhook` · `replay_webhook` · `create_webhook_proxy` · `inspect_webhook_payload`

**ChatOpsAutomationTool:** `route_alert` · `create_incident` · `post_deployment_notification` · `send_daily_standup_reminder` · `collect_standup_responses` · `create_approval_workflow` · `check_approval_status` · `broadcast_announcement` · `schedule_message`

**SMTPAdvancedTool:** `send_html_email` · `send_template_email` · `monitor_inbox` · `search_emails` · `download_attachments` · `auto_reply` · `forward_emails` · `mark_as_read` · `delete_emails` · `create_filter_rule`

```python
ZoomTool.create_meeting(topic="NPMAI Team Sync", start_time="2026-07-10T15:00:00")
MicrosoftTeamsTool.send_message(channel_id="general", text="Deploy complete ✅")
WebhookTool.start_webhook_server(port=8000, secret="whsec_xxx")
SMTPAdvancedTool.monitor_inbox(folder="INBOX", callback=lambda msg: print(msg.subject))
```

---

## ◈ Creative & Design — 97 Tools

---

### FigmaTool — 13 Tools

```python
from npmai_agents import FigmaTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `get_file` | Get Figma file | `file_key` |
| `get_node` | Get specific node | `file_key, node_id` |
| `list_files` | List project files | `project_id` |
| `export_asset` | Export asset | `file_key, node_id, format="PNG", scale=1` |
| `export_all_assets` | Export all assets | `file_key, output_dir, format="PNG"` |
| `get_components` | Get components | `file_key` |
| `get_styles` | Get styles | `file_key` |
| `get_comments` | Get comments | `file_key` |
| `post_comment` | Post comment | `file_key, message, x, y` |
| `create_webhook` | Create webhook | `team_id, event_type, endpoint` |
| `list_projects` | List team projects | `team_id` |
| `get_team_components` | Team component library | `team_id` |
| `get_versions` | File version history | `file_key` |

```python
FigmaTool.export_all_assets(file_key="abc123", output_dir="/home/sonu/assets", format="PNG")
FigmaTool.get_components(file_key="abc123")
```

---

### DiagramTool — 10 Tools

```python
from npmai_agents import DiagramTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_flowchart` | Flowchart from steps | `steps: list, output_path` |
| `create_er_diagram` | ER diagram | `tables: dict, output_path` |
| `create_sequence_diagram` | Sequence diagram | `actors: list, messages: list, output_path` |
| `create_class_diagram` | UML class diagram | `classes: dict, output_path` |
| `create_network_diagram` | Network topology | `nodes: list, edges: list, output_path` |
| `create_gantt` | Gantt chart | `tasks: list, output_path` |
| `create_mindmap` | Mind map | `root, branches: dict, output_path` |
| `create_org_chart` | Org chart | `structure: dict, output_path` |
| `render_mermaid` | Render Mermaid syntax | `mermaid_code, output_path` |
| `render_plantuml` | Render PlantUML | `plantuml_code, output_path` |

```python
DiagramTool.create_flowchart(steps=["Receive task", "Plan", "Select tools", "Code", "Audit", "Execute", "Verify"], output_path="pipeline.png")
DiagramTool.render_mermaid(mermaid_code="graph TD; A-->B; B-->C;", output_path="flow.png")
```

---

### SVGTool — 10 Tools · BlenderTool — 11 Tools · CanvaTool — 9 Tools · FontTool — 10 Tools · ColorTool — 11 Tools · IconTool — 7 Tools · PrintTool — 8 Tools · ThreeDTool — 8 Tools

```python
from npmai_agents import SVGTool, BlenderTool, CanvaTool, FontTool
from npmai_agents import ColorTool, IconTool, PrintTool, ThreeDTool
```

**SVGTool:** `create_svg` · `add_element` · `convert_to_png` · `convert_to_pdf` · `optimize` · `animate` · `batch_convert` · `create_icon_set` · `trace_bitmap` · `merge_svgs`

**BlenderTool:** `render_image` · `render_animation` · `import_obj` · `import_fbx` · `export_obj` · `export_fbx` · `export_gltf` · `convert_format` · `apply_material` · `batch_render` · `create_turntable_video`

**CanvaTool:** `list_designs` · `get_design` · `create_design` · `export_design` · `list_brand_kits` · `get_brand_kit` · `list_assets` · `upload_asset` · `create_from_template`

**FontTool:** `list_system_fonts` · `install_font` · `remove_font` · `render_text_image` · `create_text_animation_frames` · `generate_font_preview` · `convert_font` · `subset_font` · `get_font_info` · `pair_fonts_suggestion`

**ColorTool:** `generate_palette` · `extract_palette_from_image` · `convert_color` · `find_complementary` · `create_gradient` · `check_contrast_ratio` · `suggest_accessible_combination` · `create_color_wheel` · `generate_brand_palette` · `export_palette` · `analyze_image_colors`

**IconTool:** `generate_icon` · `create_app_icon_set` · `resize_icon` · `convert_ico` · `create_favicon_package` · `batch_convert_icons` · `add_badge`

**PrintTool:** `create_business_card` · `create_flyer` · `create_poster` · `create_brochure` · `create_certificate` · `create_label_sheet` · `create_letterhead` · `add_bleed_marks`

**ThreeDTool:** `view_model` · `get_model_info` · `convert_model` · `optimize_mesh` · `center_model` · `scale_model` · `merge_models` · `generate_thumbnail`

```python
SVGTool.convert_to_png("logo.svg", output_path="logo.png", scale=2)
BlenderTool.render_image("scene.blend", output_path="render.png")
ColorTool.generate_palette(base_color="#00f5ff", count=5)
IconTool.create_app_icon_set("logo.png", output_dir="/home/sonu/icons")
```

---

## ◈ Data & Research — 137 Tools

---

### DataAnalysisTool — 15 Tools

```python
from npmai_agents import DataAnalysisTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `load` | Load CSV/Excel/JSON | `file_path` |
| `save` | Save to file | `file_path, format="csv"` |
| `profile` | Statistical profile | — |
| `clean` | Auto data cleaning | `remove_nulls=True, remove_duplicates=True` |
| `transform` | Transform columns | `operations: dict` |
| `filter_data` | Filter rows | `conditions: dict` |
| `merge_files` | Merge datasets | `file_paths: list, on, how="inner"` |
| `pivot` | Pivot table | `index, columns, values, aggfunc="sum"` |
| `time_series_analysis` | Time series stats | `date_col, value_col` |
| `correlation_matrix` | Correlation heatmap | `output_path=""` |
| `outlier_detection` | Find outliers | `method="iqr"` |
| `feature_importance` | Feature importance | `target_col` |
| `cluster_data` | K-means clustering | `n_clusters=3, features: list` |
| `natural_language_query` | Query in plain English | `question` |
| `auto_visualize` | Auto-generate charts | `out_dir=""` |

```python
DataAnalysisTool.load("sales.csv")
DataAnalysisTool.clean(remove_nulls=True, remove_duplicates=True)
DataAnalysisTool.pivot(index="region", columns="month", values="revenue", aggfunc="sum")
DataAnalysisTool.natural_language_query("what were the top 5 customers by revenue last quarter?")
```

---

### VisualizationTool — 15 Tools

```python
from npmai_agents import VisualizationTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `bar_chart` | Bar chart | `data, x, y, title="", output_path=""` |
| `line_chart` | Line chart | `data, x, y, title="", output_path=""` |
| `scatter_plot` | Scatter plot | `data, x, y, color="", output_path=""` |
| `pie_chart` | Pie chart | `data, labels, values, title="", output_path=""` |
| `heatmap` | Correlation heatmap | `data, output_path=""` |
| `histogram` | Histogram | `data, column, bins=20, output_path=""` |
| `box_plot` | Box plot | `data, columns: list, output_path=""` |
| `violin_plot` | Violin plot | `data, x, y, output_path=""` |
| `geographic_map` | Choropleth map | `data, location_col, value_col, output_path=""` |
| `create_dashboard` | Multi-chart dashboard | `charts: list, output_path` |
| `sankey_diagram` | Sankey flow diagram | `source: list, target: list, value: list, output_path=""` |
| `treemap` | Treemap chart | `data, path: list, values, output_path=""` |
| `sunburst` | Sunburst chart | `data, path: list, values, output_path=""` |
| `waterfall_chart` | Waterfall chart | `categories: list, values: list, output_path=""` |
| `candlestick_chart` | OHLC candlestick | `data, output_path=""` |

```python
VisualizationTool.bar_chart(data=df, x="month", y="revenue", title="Monthly Revenue", output_path="revenue.png")
VisualizationTool.create_dashboard(charts=["revenue.png", "churn.png"], output_path="dashboard.png")
```

---

### DatabaseTool — 22 Tools

```python
from npmai_agents import DatabaseTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `connect_postgres` | Connect PostgreSQL | `host, db, user, password, port=5432` |
| `execute_query` | Execute SQL query | `query, params=()` |
| `execute_transaction` | Execute transaction | `queries: list` |
| `backup_postgres` | Backup database | `output_path` |
| `restore_postgres` | Restore backup | `backup_path` |
| `get_schema` | Get DB schema | — |
| `connect_mysql` | Connect MySQL | `host, db, user, password, port=3306` |
| `connect_mongodb` | Connect MongoDB | `uri, db_name` |
| `mongo_find` | Find documents | `collection, query={}, limit=0` |
| `mongo_insert` | Insert document(s) | `collection, data` |
| `mongo_update` | Update documents | `collection, query, update` |
| `mongo_delete` | Delete documents | `collection, query` |
| `connect_redis` | Connect Redis | `host="localhost", port=6379, db=0` |
| `redis_set` | Set key | `key, value, expire=None` |
| `redis_get` | Get key | `key` |
| `redis_hset` | Set hash field | `name, key, value` |
| `redis_hget` | Get hash field | `name, key` |
| `redis_lpush` | Push to list | `name, *values` |
| `export_to_csv` | Export query to CSV | `query, output_path` |
| `import_from_csv` | Import CSV to table | `csv_path, table_name` |
| `create_sqlite_db` | Create SQLite DB | `db_path` |
| `query_sqlite` | Query SQLite | `db_path, query` |

```python
DatabaseTool.connect_postgres(host="localhost", db="npmai", user="postgres", password="xxxx")
DatabaseTool.execute_query("SELECT * FROM users WHERE active = true")
DatabaseTool.redis_set("session:123", "active", expire=3600)
```

---

### SearchResearchTool — 11 Tools · FinancialDataTool — 14 Tools · SocialMediaDataTool — 14 Tools · WeatherGeoTool — 12 Tools · TextAnalyticsTool — 14 Tools · WebScrapingAdvancedTool — 12 Tools · ReportGeneratorTool — 8 Tools

```python
from npmai_agents import SearchResearchTool, FinancialDataTool, SocialMediaDataTool
from npmai_agents import WeatherGeoTool, TextAnalyticsTool, WebScrapingAdvancedTool, ReportGeneratorTool
```

**SearchResearchTool:** `search_arxiv` · `get_arxiv_paper` · `search_pubmed` · `search_semantic_scholar` · `get_citations` · `search_wikipedia` · `get_wikipedia_page` · `search_google_scholar` · `search_news` · `get_trending_topics` · `search_patents`

**FinancialDataTool:** `get_stock_price` · `get_multiple_stocks` · `get_company_info` · `get_financial_statements` · `get_earnings_calendar` · `get_economic_indicators` · `get_crypto_price` · `get_crypto_info` · `get_forex_rate` · `get_commodity_prices` · `calculate_technical_indicators` · `screen_stocks` · `get_options_chain` · `portfolio_analysis`

**SocialMediaDataTool:** `get_twitter_user` · `get_twitter_timeline` · `search_twitter` · `get_twitter_trends` · `get_reddit_posts` · `search_reddit` · `get_reddit_comments` · `get_subreddit_info` · `get_youtube_video_info` · `get_youtube_channel_info` · `get_youtube_comments` · `search_youtube` · `get_instagram_profile` · `get_hackernews_top`

**WeatherGeoTool:** `get_current_weather` · `get_forecast` · `get_historical_weather` · `get_weather_alerts` · `geocode` · `reverse_geocode` · `get_timezone` · `calculate_distance` · `get_elevation` · `get_nearby_places` · `get_air_quality` · `get_uv_index`

**TextAnalyticsTool:** `sentiment_analysis` · `classify_text` · `extract_entities` · `extract_keywords` · `summarize` · `translate` · `detect_language` · `check_grammar` · `calculate_readability` · `topic_modeling` · `text_similarity` · `generate_embeddings` · `semantic_search` · `detect_plagiarism`

**WebScrapingAdvancedTool:** `scrape_with_js` · `scrape_paginated` · `scrape_login_protected` · `extract_structured_data` · `monitor_page_changes` · `bulk_scrape` · `extract_emails_phones` · `map_website_structure` · `take_full_screenshot` · `extract_all_links` · `download_all_images` · `fill_and_submit_form`

**ReportGeneratorTool:** `create_pdf_report` · `create_word_report` · `create_excel_report` · `create_presentation` · `generate_research_report` · `schedule_report` · `create_dashboard_report` · `generate_from_template`

```python
SearchResearchTool.search_arxiv("retrieval augmented generation", max_results=10)
FinancialDataTool.get_stock_price("TCS.NS")
SocialMediaDataTool.get_reddit_posts(subreddit="MachineLearning", limit=25)
WeatherGeoTool.get_current_weather(city="Kota, Rajasthan")
TextAnalyticsTool.sentiment_analysis("This product completely exceeded my expectations.")
WebScrapingAdvancedTool.scrape_with_js("https://example.com/dashboard")
ReportGeneratorTool.create_pdf_report(title="Weekly Ops Report", sections=[...], output_path="report.pdf")
```

---

## ◈ Media & Audio/Video — 123 Tools

---

### FFmpegTool — 32 Tools
Most comprehensive video/audio processing class — 32 tools.

```python
from npmai_agents import FFmpegTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `trim` | Trim video/audio | `input, output, start, end` |
| `merge` | Merge files | `inputs: list, output` |
| `compress_video` | Compress video | `input, output, crf=23` |
| `compress_audio` | Compress audio | `input, output, bitrate="128k"` |
| `convert` | Convert format | `input, output` |
| `extract_audio` | Extract audio track | `input, output` |
| `replace_audio` | Replace audio | `video, audio, output` |
| `add_subtitles` | Burn subtitles | `input, srt, output` |
| `extract_subtitles` | Extract subtitles | `input, output` |
| `resize` | Resize video | `input, output, width, height` |
| `crop` | Crop video | `input, output, x, y, width, height` |
| `add_watermark` | Add watermark | `input, watermark, output, position="bottomright"` |
| `change_speed` | Change playback speed | `input, output, speed=2.0` |
| `reverse` | Reverse video | `input, output` |
| `loop` | Loop video | `input, output, count=3` |
| `concatenate_with_transition` | Join with transition | `inputs: list, output, transition="fade"` |
| `extract_frames` | Extract frames | `input, output_dir, fps=1` |
| `create_from_frames` | Video from frames | `frames_dir, output, fps=24` |
| `add_intro_outro` | Add intro/outro | `main, intro, outro, output` |
| `picture_in_picture` | PiP overlay | `main, overlay, output, position="topright"` |
| `normalize_audio` | Normalise loudness | `input, output` |
| `denoise_audio` | Audio denoising | `input, output` |
| `get_metadata` | Get file metadata | `input` |
| `get_duration` | Get duration | `input` |
| `get_resolution` | Get resolution | `input` |
| `create_thumbnail` | Generate thumbnail | `input, output, time="00:00:05"` |
| `create_gif` | Create GIF | `input, output, start=0, duration=5` |
| `split_by_duration` | Split into segments | `input, output_dir, segment_duration=60` |
| `add_text_overlay` | Add text | `input, output, text, x, y` |
| `stabilize_video` | Video stabilisation | `input, output` |
| `color_grade` | Colour grading | `input, output, preset="cinematic"` |
| `create_slideshow` | Images to video | `images_dir, output, duration_per_image=3` |

```python
FFmpegTool.compress_video("/home/sonu/raw.mp4", "compressed.mp4", crf=28)
FFmpegTool.create_gif("/home/sonu/demo.mp4", "demo.gif", start=5, duration=8)
FFmpegTool.add_subtitles("/home/sonu/video.mp4", "/home/sonu/subs.srt", "final.mp4")
FFmpegTool.split_by_duration("/home/sonu/lecture.mp4", "/home/sonu/parts", segment_duration=300)
```

---

### AudioTool — 15 Tools · YouTubeDownloaderTool — 9 Tools · ImageAdvancedTool — 20 Tools

```python
from npmai_agents import AudioTool, YouTubeDownloaderTool, ImageAdvancedTool
```

**AudioTool:** `convert` · `split` · `merge` · `normalize` · `change_pitch` · `change_tempo` · `remove_silence` · `apply_eq` · `fade_in_out` · `detect_bpm` · `get_waveform_data` · `record_microphone` · `play_audio` · `transcribe` · `translate_audio`

**YouTubeDownloaderTool:** `download_video` · `download_audio` · `download_playlist` · `get_video_info` · `download_subtitles` · `get_available_formats` · `download_thumbnail` · `search_videos` · `get_channel_videos`

**ImageAdvancedTool:** `batch_resize` · `batch_convert` · `create_collage` · `remove_background` · `replace_background` · `upscale` · `restore_old_photo` · `face_detect` · `blur_faces` · `add_border` · `add_shadow` · `create_gif_from_images` · `optimize_for_web` · `extract_dominant_colors` · `create_palette` · `compare_images` · `create_sprite_sheet` · `watermark_batch` · `convert_to_ico` · `create_favicon`

```python
AudioTool.transcribe("/home/sonu/interview.mp3")
YouTubeDownloaderTool.download_video("https://youtube.com/watch?v=xxxx", quality="1080p")
ImageAdvancedTool.remove_background("/home/sonu/photo.jpg", output_path="photo_nobg.png")
```

---

### ScreenRecorderTool — 7 Tools · TextToSpeechTool — 7 Tools · VideoEditingTool — 10 Tools · PodcastTool — 8 Tools · StreamingTool — 6 Tools · MediaMetadataTool — 9 Tools

```python
from npmai_agents import ScreenRecorderTool, TextToSpeechTool, VideoEditingTool
from npmai_agents import PodcastTool, StreamingTool, MediaMetadataTool
```

**ScreenRecorderTool:** `screenshot` · `screenshot_all_monitors` · `record_screen` · `record_with_cursor` · `capture_window` · `list_windows` · `create_screencast_gif`

**TextToSpeechTool:** `generate` · `list_voices` · `generate_ssml` · `clone_voice` · `generate_batch` · `add_background_music` · `translate_and_speak`

**VideoEditingTool:** `auto_cut_silences` · `jump_cut` · `auto_color_correct` · `auto_denoise` · `create_highlight_reel` · `add_chapter_markers` · `export_for_platform` · `create_vertical_from_horizontal` · `batch_process` · `apply_lut`

**PodcastTool:** `record_episode` · `edit_raw_recording` · `clean_audio` · `generate_transcript` · `generate_show_notes` · `create_chapters` · `export_to_formats` · `generate_rss_feed`

**StreamingTool:** `stream_to_youtube` · `stream_to_twitch` · `stream_to_multiple` · `capture_stream` · `get_stream_info` · `download_live_stream`

**MediaMetadataTool:** `read_metadata` · `write_metadata` · `bulk_rename_by_metadata` · `fix_dates` · `add_album_art` · `extract_album_art` · `generate_nfo` · `create_m3u_playlist` · `scan_folder`

```python
ScreenRecorderTool.record_screen(output_path="demo.mp4", duration=60)
TextToSpeechTool.generate("Welcome to NPMAI Ecosystem", output_path="intro.mp3")
VideoEditingTool.auto_cut_silences("/home/sonu/podcast_raw.mp4", output_path="podcast_edited.mp4")
PodcastTool.generate_show_notes("/home/sonu/episode12.mp3")
```

---

## ◈ Productivity & Project Management — 176 Tools

---

### GoogleWorkspaceTool — 21 Tools

```python
from npmai_agents import GoogleWorkspaceTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `docs_create` | Create Google Doc | `title, content=""` |
| `docs_get` | Get Doc content | `doc_id` |
| `docs_append` | Append text to Doc | `doc_id, text` |
| `docs_replace_text` | Find and replace in Doc | `doc_id, old, new` |
| `docs_export` | Export Doc | `doc_id, format="pdf", output_path=""` |
| `sheets_create` | Create Spreadsheet | `title` |
| `sheets_read` | Read sheet range | `sheet_id, range_` |
| `sheets_write` | Write to sheet | `sheet_id, range_, data: list` |
| `sheets_append` | Append rows | `sheet_id, range_, data: list` |
| `sheets_clear` | Clear range | `sheet_id, range_` |
| `sheets_format_cells` | Format cells | `sheet_id, range_, format: dict` |
| `sheets_add_chart` | Add chart to sheet | `sheet_id, chart_type, data_range` |
| `drive_upload` | Upload to Drive | `local_path, folder_id=""` |
| `drive_download` | Download from Drive | `file_id, output_path` |
| `drive_list` | List Drive files | `folder_id="", query=""` |
| `drive_create_folder` | Create folder | `name, parent_id=""` |
| `drive_share` | Share file | `file_id, email, role="reader"` |
| `drive_move` | Move file | `file_id, folder_id` |
| `forms_create` | Create Google Form | `title, questions: list` |
| `forms_get_responses` | Get form responses | `form_id` |
| `forms_list` | List forms | — |

```python
GoogleWorkspaceTool.sheets_create("Q3 Revenue")
GoogleWorkspaceTool.sheets_write(sheet_id="abc123", range_="A1:C1", data=[["Month", "Revenue", "Growth"]])
GoogleWorkspaceTool.drive_share(file_id="abc123", email="team@npmai.ai", role="writer")
```

---

### NotionAdvancedTool — 19 Tools · LinearTool — 19 Tools · AsanaTool — 19 Tools · TrelloTool — 20 Tools

```python
from npmai_agents import NotionAdvancedTool, LinearTool, AsanaTool, TrelloTool
```

**NotionAdvancedTool:** `search` · `get_database` · `query_database` · `create_database` · `add_database_item` · `update_database_item` · `delete_database_item` · `create_page` · `get_page` · `update_page` · `append_blocks` · `get_blocks` · `delete_block` · `create_table` · `create_kanban_view` · `export_database_to_csv` · `import_csv_to_database` · `create_template` · `duplicate_page`

**LinearTool:** `list_issues` · `get_issue` · `create_issue` · `update_issue` · `close_issue` · `delete_issue` · `list_teams` · `get_team` · `list_projects` · `create_project` · `update_project` · `list_members` · `list_labels` · `create_label` · `list_cycles` · `create_cycle` · `add_issue_to_cycle` · `get_comments` · `add_comment`

**AsanaTool:** `list_workspaces` · `list_projects` · `get_project` · `create_project` · `list_tasks` · `get_task` · `create_task` · `update_task` · `complete_task` · `delete_task` · `add_subtask` · `list_subtasks` · `add_comment` · `list_comments` · `list_sections` · `create_section` · `move_task_to_section` · `list_tags` · `add_tag_to_task`

**TrelloTool:** `list_boards` · `get_board` · `create_board` · `list_lists` · `create_list` · `archive_list` · `list_cards` · `get_card` · `create_card` · `update_card` · `move_card` · `archive_card` · `add_checklist` · `check_checklist_item` · `add_comment` · `add_attachment` · `list_members` · `add_member` · `create_label` · `add_label_to_card`

```python
NotionAdvancedTool.create_page(title="Sprint 12 Notes", content="...")
LinearTool.create_issue(team_id="team_1", title="Fix select_tools regex", description="Non-greedy match breaks on prefixed text")
AsanaTool.create_task(project_id="proj_1", name="Deploy MCP hosting", notes="search_tools + execute_tool")
TrelloTool.create_card(list_id="list_1", name="Write test suite for Tools_business.py")
```

---

### ClickUpTool — 17 Tools · TodoistTool — 17 Tools · ObsidianTool — 15 Tools · BookmarkManagerTool — 12 Tools · TimeTrackingTool — 17 Tools

```python
from npmai_agents import ClickUpTool, TodoistTool, ObsidianTool, BookmarkManagerTool, TimeTrackingTool
```

**ClickUpTool:** `list_spaces` · `list_folders` · `list_lists` · `get_tasks` · `get_task` · `create_task` · `update_task` · `delete_task` · `set_task_status` · `add_comment` · `list_comments` · `create_checklist` · `add_checklist_item` · `track_time` · `get_time_entries` · `list_views` · `get_view_tasks`

**TodoistTool:** `get_projects` · `add_project` · `update_project` · `delete_project` · `get_tasks` · `add_task` · `update_task` · `complete_task` · `delete_task` · `reopen_task` · `get_comments` · `add_comment` · `get_labels` · `add_label` · `quick_add` · `get_activity_log` · `get_productivity_stats`

**ObsidianTool:** `read_note` · `create_note` · `update_note` · `delete_note` · `search_notes` · `list_notes` · `get_backlinks` · `get_outlinks` · `add_tag` · `remove_tag` · `create_daily_note` · `append_to_daily_note` · `create_canvas` · `get_graph_data` · `sync_folder_to_vault`

**BookmarkManagerTool:** `import_bookmarks` · `export_bookmarks` · `add_bookmark` · `remove_bookmark` · `search_bookmarks` · `organize_by_domain` · `check_broken_links` · `archive_page` · `generate_reading_list` · `bulk_screenshot` · `tag_with_ai` · `deduplicate`

**TimeTrackingTool:** `start_timer` · `stop_timer` · `pause_timer` · `get_current_timer` · `list_time_entries` · `add_manual_entry` · `delete_entry` · `generate_timesheet` · `get_project_summary` · `calculate_billing` · `export_to_invoice` · `connect_toggl` · `toggl_list_projects` · `toggl_start_timer` · `connect_clockify` · `clockify_list_projects` · `clockify_time_entry`

```python
TodoistTool.quick_add("Review PR #42 tomorrow at 5pm p1")
ObsidianTool.create_daily_note()
BookmarkManagerTool.check_broken_links()
TimeTrackingTool.start_timer(project_id="npmai-agent", task="Fix cli.py globals")
```

---

## ◈ Security & AI — 122 Tools

---

### CryptographyTool — 16 Tools

```python
from npmai_agents import CryptographyTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `generate_rsa_keypair` | Generate RSA keys | `bits=4096, out_dir=""` |
| `encrypt_with_public_key` | RSA encrypt | `data, public_key_path` |
| `decrypt_with_private_key` | RSA decrypt | `encrypted_data, private_key_path` |
| `sign_data` | Sign with private key | `data, private_key_path` |
| `verify_signature` | Verify signature | `data, signature, public_key_path` |
| `aes_encrypt` | AES-256 encrypt file | `file_path, key, output=""` |
| `aes_decrypt` | AES-256 decrypt file | `file_path, key, output=""` |
| `generate_random_password` | Secure password | `length=32, special=True` |
| `hash_password` | bcrypt hash | `password` |
| `verify_password` | Verify bcrypt hash | `password, hash` |
| `generate_totp_secret` | TOTP 2FA setup | `issuer, account` |
| `verify_totp` | Verify TOTP code | `secret, code` |
| `create_ssl_certificate` | Sign SSL cert | `csr_path, ca_key, ca_cert, output=""` |
| `create_self_signed_cert` | Self-signed cert | `domain, days=365, output_dir=""` |
| `pgp_encrypt` | PGP encrypt | `data, recipient_key` |
| `pgp_decrypt` | PGP decrypt | `encrypted_data, private_key, passphrase` |

```python
keys = CryptographyTool.generate_rsa_keypair(bits=4096, out_dir="/home/sonu/keys")
CryptographyTool.hash_password("super-secret-password")
CryptographyTool.generate_totp_secret(issuer="NPMAI", account="sonu@npmai.ai")
```

---

### KnowledgeBaseTool — 14 Tools

```python
from npmai_agents import KnowledgeBaseTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `create_kb` | Create knowledge base | `name` |
| `add_documents` | Add document files | `kb_name, file_paths: list` |
| `add_url_to_kb` | Add webpage | `kb_name, url` |
| `add_text` | Add raw text | `kb_name, text, source=""` |
| `query_kb` | Query with RAG | `kb_name, question` |
| `search_kb` | Keyword search | `kb_name, query, top_k=5` |
| `update_document` | Update document | `kb_name, doc_id, new_content` |
| `delete_document` | Delete document | `kb_name, doc_id` |
| `list_documents` | List KB documents | `kb_name` |
| `get_kb_stats` | KB statistics | `kb_name` |
| `export_kb` | Export KB | `kb_name, output_path` |
| `import_kb` | Import KB | `kb_path` |
| `create_qa_pairs` | Generate Q&A pairs | `kb_name, source_doc` |
| `answer_with_sources` | Answer with citations | `kb_name, question` |

```python
KnowledgeBaseTool.create_kb("npmai-docs")
KnowledgeBaseTool.add_documents("npmai-docs", file_paths=["README.md", "architecture.pdf"])
KnowledgeBaseTool.query_kb("npmai-docs", "How does the Tool Manager select classes?")
```

---

### SecurityScannerTool — 14 Tools · PenetrationTestingTool — 11 Tools · AIImageGenerationTool — 8 Tools · AITextGenerationAdvancedTool — 12 Tools · MLModelTool — 11 Tools · SpeechAITool — 8 Tools · ComputerVisionTool — 14 Tools · AutomationWorkflowTool — 14 Tools

```python
from npmai_agents import SecurityScannerTool, PenetrationTestingTool
from npmai_agents import AIImageGenerationTool, AITextGenerationAdvancedTool
from npmai_agents import MLModelTool, SpeechAITool, ComputerVisionTool, AutomationWorkflowTool
```

**SecurityScannerTool:** `check_virustotal` · `scan_file_virustotal` · `shodan_search` · `shodan_host` · `check_haveibeenpwned` · `check_password_breach` · `nmap_scan` · `port_scan_common` · `whois_lookup` · `check_ssl_grade` · `check_dns_leak` · `scan_url_safe_browsing` · `check_reputation` · `get_threat_intel`

**PenetrationTestingTool:** `subdomain_enumeration` · `directory_bruteforce` · `check_common_vulnerabilities` · `check_http_headers` · `check_cors` · `sql_injection_test` · `xss_test` · `check_ssl_vulnerabilities` · `check_outdated_software` · `generate_security_report` · `create_pentest_checklist`

**AIImageGenerationTool:** `generate_image_stability` · `generate_image_dalle` · `generate_image_local_sd` · `inpaint_image` · `img_to_img` · `upscale_image_ai` · `remove_background_ai` · `create_image_variations`

**AITextGenerationAdvancedTool:** `chain_prompts` · `few_shot_generate` · `generate_structured_json` · `debate_topic` · `brainstorm` · `critique_and_improve` · `generate_code` · `explain_code` · `generate_test_cases` · `refactor_code` · `translate_text` · `summarize_long_document`

**MLModelTool:** `train_classifier` · `train_regressor` · `predict` · `evaluate_model` · `feature_importance` · `cross_validate` · `hyperparameter_tune` · `save_model` · `load_and_predict` · `deploy_model_api` · `explain_prediction`

**SpeechAITool:** `transcribe_realtime` · `transcribe_file` · `speaker_diarization` · `voice_activity_detection` · `clone_and_speak` · `real_time_translation` · `command_recognition` · `keyword_detection`

**ComputerVisionTool:** `detect_objects` · `track_objects` · `recognize_faces` · `detect_emotions` · `read_text_ocr` · `read_table_from_image` · `scan_qr_barcode` · `generate_qr_with_style` · `classify_image` · `compare_faces` · `count_objects` · `segment_image` · `measure_object` · `extract_text_from_pdf_image`

**AutomationWorkflowTool:** `create_workflow` · `run_workflow` · `schedule_workflow` · `list_scheduled_workflows` · `cancel_scheduled_workflow` · `get_workflow_history` · `create_trigger_on_file_change` · `create_trigger_on_email` · `create_trigger_on_webhook` · `chain_workflows` · `create_conditional_branch` · `retry_on_failure` · `run_parallel` · `create_loop_workflow`

```python
SecurityScannerTool.check_haveibeenpwned("sonu@npmai.ai")
PenetrationTestingTool.check_http_headers("https://npmai.netlify.app")
AITextGenerationAdvancedTool.explain_code(open("agent_core.py").read())
ComputerVisionTool.read_text_ocr("/home/sonu/scanned_invoice.png")
AutomationWorkflowTool.create_trigger_on_file_change("/home/sonu/Downloads", workflow_name="auto-sort")
```

---

## ◈ System & Hardware — 165 Tools

---

### SystemAdvancedTool — 22 Tools

```python
from npmai_agents import SystemAdvancedTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `get_full_system_info` | Full system report | — |
| `get_hardware_info` | Hardware details | — |
| `manage_service` | Start/stop/restart service | `service_name, action` |
| `list_services` | List system services | `status=""` |
| `create_cron_job` | Add cron job | `name, schedule, command` |
| `list_cron_jobs` | List cron jobs | — |
| `remove_cron_job` | Remove cron job | `name` |
| `manage_firewall` | Firewall rule | `action, port, protocol="tcp"` |
| `create_startup_item` | Add startup program | `name, command` |
| `remove_startup_item` | Remove startup item | `name` |
| `manage_hosts_file` | Edit hosts file | `action, ip, hostname` |
| `flush_dns` | Flush DNS cache | — |
| `get_installed_programs` | List installed apps | `search=""` |
| `uninstall_program` | Uninstall program | `name` |
| `create_restore_point` | Create restore point | `description=""` |
| `list_restore_points` | List restore points | — |
| `set_system_volume` | Set volume | `level: int` |
| `get_battery_info` | Battery status | — |
| `set_screen_brightness` | Set brightness | `level: int` |
| `list_usb_devices` | List USB devices | — |
| `eject_drive` | Eject drive | `drive_path` |
| `format_drive` | Format drive | `drive_path, filesystem="ext4"` |

```python
SystemAdvancedTool.create_cron_job(name="daily-backup", schedule="0 2 * * *", command="npmai run 'backup my documents to S3'")
SystemAdvancedTool.manage_firewall(action="allow", port=8080, protocol="tcp")
```

---

### ProcessAutomationTool — 20 Tools
Desktop GUI automation — find windows, click, type, drag, macros.

```python
from npmai_agents import ProcessAutomationTool
```

| Method | Purpose | Key Parameters |
|---|---|---|
| `find_window` | Find window by title | `title` |
| `focus_window` | Focus window | `title` |
| `minimize_window` | Minimise window | `title` |
| `maximize_window` | Maximise window | `title` |
| `click_at` | Click coordinates | `x, y, button="left"` |
| `type_text` | Type text | `text, interval=0.05` |
| `press_key` | Press key | `key` |
| `drag_and_drop` | Drag and drop | `start_x, start_y, end_x, end_y` |
| `scroll` | Mouse scroll | `x, y, clicks=3, direction="down"` |
| `take_screenshot_region` | Screenshot region | `x, y, width, height, output=""` |
| `find_image_on_screen` | Find image on screen | `image_path, confidence=0.9` |
| `click_image` | Click image on screen | `image_path, confidence=0.9` |
| `wait_for_image` | Wait for image | `image_path, timeout=30` |
| `run_application` | Launch application | `app_path, args=[]` |
| `close_application` | Close application | `title` |
| `get_active_window` | Get active window | — |
| `get_all_windows` | List all windows | — |
| `send_hotkey` | Send hotkey combo | `*keys` |
| `record_macro` | Record macro | `output_path` |
| `play_macro` | Play recorded macro | `macro_path` |

```python
ProcessAutomationTool.run_application("/usr/bin/gimp")
ProcessAutomationTool.wait_for_image("save_button.png", timeout=15)
ProcessAutomationTool.click_image("save_button.png")
```

---

### NetworkAdvancedTool — 21 Tools · FileSystemAdvancedTool — 17 Tools · PrinterTool — 11 Tools · ClipboardAdvancedTool — 15 Tools · HardwareMonitorTool — 13 Tools · RaspberryPiTool — 17 Tools · MQTTIoTTool — 12 Tools · VirtualizationTool — 17 Tools

```python
from npmai_agents import NetworkAdvancedTool, FileSystemAdvancedTool, PrinterTool
from npmai_agents import ClipboardAdvancedTool, HardwareMonitorTool
from npmai_agents import RaspberryPiTool, MQTTIoTTool, VirtualizationTool
```

**NetworkAdvancedTool:** `ping` · `traceroute` · `port_scan` · `check_port_open` · `dns_lookup` · `reverse_dns` · `whois_lookup` · `get_local_ip` · `get_public_ip` · `get_network_interfaces` · `check_ssl_certificate` · `get_ssl_expiry` · `http_test` · `bandwidth_test` · `capture_packets` · `get_arp_table` · `get_routing_table` · `set_dns_servers` · `check_domain_health` · `monitor_uptime` · `create_ssh_tunnel`

**FileSystemAdvancedTool:** `watch_folder` · `sync_folders` · `find_duplicates` · `remove_duplicates` · `encrypt_file` · `decrypt_file` · `secure_delete` · `split_file` · `join_files` · `compress_folder` · `scan_for_malware` · `find_large_files` · `change_permissions_recursive` · `change_owner_recursive` · `mount_remote_folder` · `verify_checksum` · `generate_checksum_file`

**PrinterTool:** `list_printers` · `get_default_printer` · `set_default_printer` · `print_file` · `print_pdf` · `print_image` · `get_print_queue` · `cancel_job` · `get_printer_status` · `install_printer` · `export_to_pdf`

**ClipboardAdvancedTool:** `get_text` · `set_text` · `get_image` · `set_image` · `get_files` · `set_files` · `get_html` · `set_html` · `monitor` · `get_history` · `clear_history` · `copy_formatted_table` · `copy_rich_text` · `paste_as_plain_text` · `transform_clipboard`

**HardwareMonitorTool:** `get_cpu_temperature` · `get_gpu_temperature` · `get_disk_temperature` · `get_fan_speeds` · `get_voltages` · `get_power_consumption` · `get_memory_slots` · `get_storage_devices_smart` · `benchmark_cpu` · `benchmark_memory` · `benchmark_disk` · `get_system_events_log` · `monitor_thresholds`

**RaspberryPiTool:** `setup_pin` · `read_pin` · `write_pin` · `setup_pwm` · `set_pwm_duty` · `read_i2c` · `write_i2c` · `read_spi` · `write_spi` · `read_temperature_sensor` · `control_servo` · `control_stepper` · `read_hcsr04_distance` · `display_on_lcd` · `read_button` · `capture_camera` · `stream_camera`

**MQTTIoTTool:** `connect` · `publish` · `subscribe` · `publish_json` · `listen_once` · `publish_sensor_data` · `send_command` · `get_device_state` · `control_home_assistant_entity` · `create_automation` · `monitor_topics` · `replay_messages`

**VirtualizationTool:** `list_vms` · `start_vm` · `stop_vm` · `restart_vm` · `suspend_vm` · `resume_vm` · `create_snapshot` · `restore_snapshot` · `delete_snapshot` · `list_snapshots` · `get_vm_info` · `set_vm_resources` · `clone_vm` · `export_vm` · `run_in_vm` · `copy_to_vm` · `create_vm`

```python
NetworkAdvancedTool.ping("8.8.8.8")
FileSystemAdvancedTool.find_duplicates("/home/sonu/Downloads")
PrinterTool.print_pdf("invoice_221.pdf")
ClipboardAdvancedTool.get_text()
HardwareMonitorTool.get_cpu_temperature()
RaspberryPiTool.read_temperature_sensor(pin=4)
MQTTIoTTool.publish(topic="home/livingroom/light", payload="ON")
VirtualizationTool.start_vm("dev-vm")
```

---

## 🔢 Verified Tool Count

| Category | File | Classes | Tools |
|---|---|---|---|
| Developer & CLI | `Tools_Developer_CLI.py` | 10 | 155 |
| Business & Payments | `Tools_business.py` | 10 | 152 |
| Cloud & DevOps | `Tools_cloud_devops.py` | 10 | 149 |
| Communication | `Tools_communication_extended.py` | 10 | 95 |
| Creative & Design | `Tools_creative.py` | 10 | 97 |
| Data & Research | `Tools_data_research.py` | 10 | 137 |
| Media & Audio/Video | `Tools_media.py` | 10 | 123 |
| Productivity & PM | `Tools_productivity.py` | 10 | 176 |
| Security & AI | `Tools_security_ai.py` | 10 | 122 |
| System & Hardware | `Tools_system_hardware.py` | 10 | 165 |
| **TOTAL** | **10 files** | **100** | **1,371** |

> Count verified programmatically from source code. Each public method = 1 tool. `__init__` excluded from count.

---

## 🚀 End-to-End Workflow

```bash
# 1. Install
pip install npmai_agents

# 2. Save your credentials (once — this is the only thing persisted to disk)
npmai save-credentials openai '{"api_key":"sk-xxxx"}'
npmai save-credentials github '{"token":"ghp_xxxx"}'
npmai save-credentials stripe '{"secret_key":"sk_live_xxxx"}'
npmai save-credentials slack '{"bot_token":"xoxb-xxxx"}'
npmai save-credentials sendgrid '{"api_key":"SG.xxxx"}'

# 3. Run any task in plain English — zero-config uses free NPMAI models,
#    or pass provider/model flags inline for any role you want on a different backend
npmai run "Analyse the CSV files in my Downloads folder,
           find the top 5 customers by revenue,
           create an Excel report with charts,
           and email it to sonu@npmai.ai with subject 'Weekly Revenue Report'" \
  --planner-provider groq --planner-model llama-3.3-70b-versatile
```

```
▸ Starting task...
▸ Scanning workspace...
▸ Planning steps...
▸ Plan: 4 step(s)
  1. Load and analyse CSV files from Downloads using DataAnalysisTool
  2. Identify top 5 customers by revenue
  3. Create Excel report with charts using ReportGeneratorTool
  4. Send email with attachment using SendGridTool

▸ Tool Manager selecting tools...
  ✓ Selected: ['DataAnalysisTool', 'VisualizationTool', 'ReportGeneratorTool', 'SendGridTool']

▸ Step 1/4: Load and analyse CSV files
  → Generating code (attempt 1)...
  → Security audit...
  ✓ Audit passed
  → Executing...
  ✓ Step 1 complete

▸ Step 2/4: Identify top 5 customers
  ✓ Step 2 complete

▸ Step 3/4: Create Excel report with charts
  ✓ Step 3 complete

▸ Step 4/4: Send email with attachment
  ✓ Step 4 complete

✓ ─── All steps completed successfully ───
```

---

## 📋 Version History

| Version | Status | Notes |
|---|---|---|
| `1.0.2` | ✅ Docker release and Bug Fixed | Production Stable | 1,371 tools · 100 classes · CLI · Docker · 5-role pipeline · Tool Manager Fixed · 12 LLM Providers |
| `1.0.1` | ✅ Bug Fixed | Production Stable | 1,371 tools · 100 classes · CLI · 5-role pipeline ·Tool Manager · 12 LLM providers |
| `1.0.0` | ✅ Production Stable | 1,371 tools · 100 classes · 5-role pipeline · Tool Manager · 12 LLM providers · CLI |
| `0.0.1` | 🗄️ Archived | Initial alpha — 21 tool classes · 4-role pipeline |

---

## 📜 License

MIT — free to use, modify, and distribute.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1b4a,50:1a0a3a,100:0a0a1a&height=160&section=footer&text=NPMAI+ECOSYSTEM&fontSize=32&fontColor=00f5ff&fontAlignY=55&desc=Open+Source+AI+Research+%26+Development+%C2%B7+Free+Forever&descColor=a78bfa&descSize=14&descAlignY=78" width="100%"/>

**Built with ❤️ by [Sonu Kumar](https://github.com/sonuramashishnpm) · [npmai.netlify.app](https://npmai.netlify.app)**

*"Promoting AI tools to every nation's village — free and open forever."*

</div>

- [JMT x402 Agent Tools](https://jmt-x402-proxy.jmthomasofficial.workers.dev) — 25 paid x402 endpoints on Base mainnet: web search, AI analysis, crypto/stock data, SEC filings, company intel, news, sentiment, macro dashboard. $0.001-$0.15/call USDC. Local LLM-powered.