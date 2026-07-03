from npmai import Ollama, Memory
from core import LLMBackend, Ollama_Local, OpenAIBackend, AnthropicBackend, GeminiBackend, GroqBackend, MistralBackend, CohereBackend, AzureOpenAIBackend, BedrockBackend, HuggingFaceBackend, LlamaCppBackend, CredStore, Workspace, ToolResult
from agent_core import Executor
import os, sys, json, re, shutil, subprocess, tempfile, traceback
import threading, time, smtplib, imaplib, email as email_lib
from langchain_core.output_parsers import StrOutputParser
import hashlib, base64, platform, glob, zipfile, tarfile
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional
from abc import ABC, abstractmethod

#Package_Imports_Ensurements
def _ensure(pkg, import_name=None):
    n = import_name or pkg
    try:
        __import__(n)
    except:
        try:
          subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"], check=False)
        except:
          print(f"Some packages is not installed properly in your environment due to some reasons these are the packages {n}")
class ensure:

    already = False
    def __init__(self):
        if ensure.already:
          return
        else:
          ensure.already = True
          for _p,_i in [
              ("npmai",        "npmai"),
              ("requests",     "requests"),
              ("beautifulsoup4","bs4"),
              ("playwright",   "playwright"),
              ("PyGithub",     "github"),
              ("slack-sdk",    "slack_sdk"),
              ("gspread",      "gspread"),
              ("google-auth",  "google.auth"),
              ("openpyxl",     "openpyxl"),
              ("pandas",       "pandas"),
              ("Pillow",       "PIL"),
              ("pypdf",        "pypdf"),
              ("python-docx",  "docx"),
              ("pyttsx3",      "pyttsx3"),
              ("SpeechRecognition","speech_recognition"),
              ("pyperclip",    "pyperclip"),
              ("schedule",     "schedule"),
              ("psutil",       "psutil"),
              ("watchdog",     "watchdog"),
              ("tweepy",       "tweepy"),
              ("pywhatkit",    "pywhatkit"),
              ("qrcode",       "qrcode"),
              ("cryptography", "cryptography"),
              ("paramiko",     "paramiko"),
              ("python-dotenv","dotenv"),
              ("pyautogui",    "pyautogui"),
              ("opencv-python","cv2"),
              ("pytesseract",  "pytesseract"),
              ("youtube-dl",   "youtube_dl"),
              ("yt-dlp",       "yt_dlp"),
              ("discord.py",   "discord"),
              ("telethon",     "telethon"),
              ("notion-client","notion_client"),
              ("todoist-api-python","todoist_api_python"),
              ("jira",         "jira"),
              ("trello",       "trello"),
              ("pywin32",      "win32api") if platform.system()=="Windows" else ("",""),
              ]:
              if _p: _ensure(_p, _i)
        return "Done all requirements are ensured."

class AgentBrain(ensure):
    """
    Full pipeline:
    Intent → Plan → [for each step: Generate → Audit → Execute → Verify] → Done
    """
    PARSER = StrOutputParser()

    """ This TOOLS_SUMMARY was defined for 0.0.1 but because we do developments in this repo therefore for future uses we
    are not removing this
    
    TOOLS_SUMMARY = "\n".join(
        f"- {k}: {v.description}" for k,v in TOOLS.items()
        )"""

    def __init__(self, log_cb:Callable=None, progress_cb:Callable=None,
                 status_cb:Callable=None, planner: LLMBackend = None, tool_manager: LLMBackend = None, coder: LLMBackend = None,
                 auditor: LLMBackend = None, verifier: LLMBackend = None, chatter: LLMBackend = None):
        super().__init__()
        self._log      = log_cb      or print
        self._progress = progress_cb or (lambda v: None)
        self._status   = status_cb   or (lambda s: None)
        self.workspace = Workspace()
        self.executor  = Executor(log_cb=log_cb)
        for role_name, backend in [
            ("planner",      planner),
            ("tool_manager", tool_manager),
            ("coder",        coder),
            ("auditor",      auditor),
            ("verifier",     verifier),
            ("chatter",      chatter),
        ]:
            if backend is not None and not isinstance(backend, LLMBackend):
                raise TypeError(
                    f"'{role_name}' must implement LLMBackend (have .invoke(prompt)->str). "
                    f"Got {type(backend).__name__}."
                )
            
        self.planner   = planner or Ollama(model="llama3.2:3b", temperature=0.2,
                                                   change=True, Models=["mistral:7b"])
        self.tool_manager = tool_manager or Ollama(model="llama3.2", temperature=0.3,
                                                   change=True, Models=["gemma3:12b"])
        self.coder     = coder or Ollama(model="codellama:7b-instruct", temperature=0.3,
                                                   change=True, Models=["deepseek-coder:6.7b"])
        self.auditor   = auditor or Ollama(model="qwen2.5-coder:7b", temperature=0.1,
                                                   change=True, Models=["falcon:7b-instruct"])
        self.verifier  = verifier or Ollama(model="llama3.2:3b", temperature=0.1,
                                                   change=True, Models=["mistral:7b"])
        self.chatter   = chatter or Ollama(model="granite3.3:2b", temperature=0.7,
                                                   change=True, Models=["llama3.2:1b"])
        self.mem_plan  = Memory("agent_plan")
        self.mem_tool_manager = Memory("agent_tools")
        self.mem_code  = Memory("agent_code")
        self.mem_chat  = Memory("agent_chat")
        self.mem_tasks = Memory("agent_tasks")
        self.tool_registry = self.build_tool_registry()
        self.TOOL_INDEX = """
=== DEVELOPER & CLI TOOLS ===
1.  GitTool: Local git operations — init, clone, commit, push, pull, branch, merge, rebase, stash, diff, log
2.  GitHubTool: GitHub API — create/delete repos, issues, PRs, releases, files, Actions triggers, collaborators
3.  GitLabTool: GitLab API — projects, issues, merge requests, pipelines, branches, members
4.  DockerTool: Docker operations — build/push/pull images, run/stop/exec containers, compose, networks, volumes
5.  PackageManagerTool: pip, npm, yarn, cargo, go — install, uninstall, build, publish, audit packages
6.  VSCodeTool: VS Code control — open files/folders, install extensions, run tasks, apply settings, format files
7.  TerminalTool: Shell command execution — run scripts, set env vars, manage processes, check installed tools
8.  MakefileTool: Makefile build system — run targets, list targets, create and edit Makefiles
9.  CMakeTool: CMake build system — configure, build, install, clean, run ctest
10. DebuggerTool: Python debugging — pdb sessions, traceback analysis, profiling, memory profiling, deadlock detection
 
=== BUSINESS & PAYMENTS ===
11. StripeTool: Stripe payments — customers, payment intents, charges, subscriptions, invoices, coupons, payouts
12. RazorpayTool: Razorpay Indian payments — orders, capture, refunds, subscriptions, payment links, QR codes
13. ShopifyTool: Shopify store — products, variants, orders, fulfillment, customers, inventory, discounts, analytics
14. InvoiceTool: Invoice/quote/receipt generation — create, send via email, batch create, AI data extraction
15. AccountingTool: Financial calculations — GST, VAT, P&L, balance sheet, cash flow, depreciation, tax liability
16. CRMTool: Local SQLite CRM — contacts, deals, pipeline, activities, reminders, sales reports
17. EmailMarketingTool: Mailchimp campaigns — lists, subscribers, campaigns, schedules, automations, templates, stats
18. AnalyticsTool: Google Analytics 4 — sessions, top pages, traffic sources, conversions, realtime users, custom reports
19. InventoryTool: Stock management — add products, update stock, record sales/purchases, low stock alerts, forecasting
20. ContractTool: Legal document automation — NDA, service agreements, employment contracts, template fill, key term extraction
 
=== CLOUD & DEVOPS ===
21. AWSS3Tool: AWS S3 — create buckets, upload/download files, presigned URLs, static site hosting, folder sync
22. AWSLambdaTool: AWS Lambda — create/deploy/invoke functions, layers, S3/API Gateway triggers, logs
23. AWSECSTool: AWS ECS/Fargate — clusters, task definitions, run tasks, services, logs
24. CloudflareTool: Cloudflare — DNS records, cache purge, Workers deploy, KV store, firewall rules, analytics
25. VercelTool: Vercel deployment — deploy projects, manage domains, env vars, logs, rollback
26. NetlifyTool: Netlify deployment — sites, deploys, env vars, custom domains, form submissions
27. RailwayTool: Railway.app deployment — projects, services, env vars, restart, logs
28. KubernetesTool: Kubernetes — pods, deployments, services, scaling, rollouts, secrets, helm, nodes
29. TerraformTool: Infrastructure as Code — init, plan, apply, destroy, state management, workspaces
30. MonitoringTool: System monitoring — CPU, memory, disk, network, processes, log parsing, health checks, alerts
 
=== COMMUNICATION ===
31. MicrosoftTeamsTool: Teams messaging — send messages, adaptive cards, file notifications, approvals, mentions
32. ZoomTool: Zoom meetings — create, list, update, delete meetings, participants, recordings, webinars
33. TwilioTool: Twilio SMS/calls — send SMS, bulk SMS, make calls, WhatsApp messages, phone verification
34. SendGridTool: SendGrid email — send, bulk, templates, contact lists, campaigns, schedules, stats, bounces
35. PushNotificationTool: Push notifications — FCM (Android), APNS (iOS), web push, Pushbullet, Pushover
36. RSSFeedTool: RSS feeds — parse, monitor, compare, aggregate, create, search, export, notify on new items
37. WebhookTool: Webhooks — start server, verify signatures, register, test, replay, proxy, inspect payloads
38. CalendarTool: Google Calendar — list/create/update/delete events, find free slots, send invites, import iCal
39. ChatOpsAutomationTool: ChatOps workflows — route alerts, incidents, deployment notifications, standups, approvals
40. SMTPAdvancedTool: Advanced SMTP/IMAP — HTML emails, templates, monitor inbox, search, auto-reply, filters
 
=== CREATIVE & DESIGN ===
41. FigmaTool: Figma API — get files/nodes, export assets, components, styles, comments, webhooks
42. BlenderTool: Blender 3D — render images/animations, import/export OBJ/FBX/GLTF, apply materials, batch render
43. SVGTool: SVG manipulation — create, add elements, convert to PNG/PDF, optimize, animate, batch convert
44. CanvaTool: Canva API — list/create designs, export, brand kits, asset upload, templates
45. FontTool: Font management — list/install/remove fonts, render text images, convert formats, pair suggestions
46. ColorTool: Color tools — generate palettes, extract from images, convert formats, contrast ratios, brand palettes
47. IconTool: Icon generation — create icons, app icon sets, resize, convert to ICO, favicons, badges
48. DiagramTool: Diagram creation — flowcharts, ER diagrams, sequence, class, network, Gantt, mindmaps, Mermaid, PlantUML
49. PrintTool: Print design — business cards, flyers, posters, brochures, certificates, labels, letterheads
50. ThreeDTool: 3D model operations — view, convert, optimize mesh, scale, merge models, generate thumbnails
 
=== DATA & RESEARCH ===
51. DataAnalysisTool: Data analysis — load/clean/transform CSV/Excel, pivot, time series, clustering, NL queries, auto-visualize
52. VisualizationTool: Chart generation — bar, line, scatter, pie, heatmap, histogram, maps, dashboards, candlestick
53. WebScrapingAdvancedTool: Web scraping — JS pages, pagination, login-protected, structured extraction, bulk scrape, form submission
54. SearchResearchTool: Academic/web research — arXiv, PubMed, Semantic Scholar, Wikipedia, Google Scholar, patents, news
55. FinancialDataTool: Financial data — stock prices, company info, financial statements, crypto, forex, technicals, options
56. SocialMediaDataTool: Social media data — Twitter/X timelines, Reddit posts, YouTube info, Instagram profiles, HackerNews
57. WeatherGeoTool: Weather and geo — current weather, forecasts, historical data, geocoding, timezone, distance, air quality
58. TextAnalyticsTool: NLP — sentiment, classification, NER, keywords, summarize, translate, grammar check, embeddings
59. DatabaseTool: Databases — PostgreSQL, MySQL, MongoDB, Redis, SQLite — query, backup, schema, transactions
60. ReportGeneratorTool: Report generation — PDF, Word, Excel, PowerPoint reports from data; schedule and dashboard reports
 
=== MEDIA & AUDIO/VIDEO ===
61. FFmpegTool: FFmpeg video/audio — trim, merge, compress, convert, subtitles, watermark, speed, GIF, thumbnails, stabilize
62. YouTubeDownloaderTool: yt-dlp downloads — video, audio, playlist, subtitles, thumbnails, channel videos, format selection
63. AudioTool: Audio processing — convert, split, merge, normalize, pitch/tempo change, EQ, BPM detect, transcribe
64. ImageAdvancedTool: Advanced image — batch resize/convert, collage, remove background, upscale, face detect, GIF creation
65. ScreenRecorderTool: Screen capture — screenshot, multi-monitor, screen recording, window capture, cursor highlight, GIF
66. TextToSpeechTool: TTS — generate speech, list voices, SSML, voice cloning, batch generate, background music
67. VideoEditingTool: Smart video editing — auto-cut silences, color correct, denoise, highlight reel, chapter markers, platform export
68. PodcastTool: Podcast production — record, edit, clean audio, transcribe, show notes, chapters, RSS feed export
69. StreamingTool: Live streaming — stream to YouTube/Twitch, multi-platform stream, capture live stream, stream info
70. MediaMetadataTool: Media metadata — read/write ID3/EXIF tags, bulk rename, fix dates, album art, M3U playlists
 
=== PRODUCTIVITY & PROJECT MANAGEMENT ===
71. GoogleWorkspaceTool: Google Workspace — Docs, Sheets, Drive (create/read/write/share), Forms — full CRUD
72. NotionAdvancedTool: Notion — search, databases, pages, blocks, kanban views, CSV import/export, templates
73. LinearTool: Linear issues — create/update/close issues, teams, projects, cycles, labels, comments
74. AsanaTool: Asana tasks — workspaces, projects, tasks, subtasks, sections, comments, tags
75. TrelloTool: Trello boards — boards, lists, cards, checklists, attachments, members, labels, move cards
76. ClickUpTool: ClickUp tasks — spaces, folders, lists, tasks, status, comments, time tracking, views
77. TodoistTool: Todoist — projects, tasks, subtasks, labels, quick add, comments, productivity stats
78. ObsidianTool: Obsidian notes — read/create/update notes, search, backlinks, tags, daily notes, graph data
79. BookmarkManagerTool: Bookmark management — import/export, add/search, check broken links, archive, AI tagging
80. TimeTrackingTool: Time tracking — start/stop timers, timesheets, billing, Toggl and Clockify integration
 
=== SECURITY & AI ===
81. SecurityScannerTool: Security scanning — VirusTotal, Shodan, HIBP, nmap, SSL grade, DNS leak, URL reputation, threat intel
82. CryptographyTool: Cryptography — RSA keypairs, AES encrypt/decrypt, password hashing, TOTP, SSL certs, PGP
83. PenetrationTestingTool: Pen testing — subdomain enum, directory brute force, HTTP headers, CORS, SQLi, XSS, SSL vulns
84. AIImageGenerationTool: AI image generation — Stability AI, DALL-E, local Stable Diffusion, inpaint, img2img, upscale
85. AITextGenerationAdvancedTool: Advanced LLM tasks — chain prompts, few-shot, structured JSON, debate, brainstorm, code gen/explain/refactor
86. MLModelTool: ML training — train classifiers/regressors, evaluate, cross-validate, hyperparameter tune, deploy as API
87. SpeechAITool: Speech AI — realtime transcription, file transcription, speaker diarization, voice cloning, keyword detection
88. ComputerVisionTool: Computer vision — object detection, face recognition, OCR, QR/barcode, image classification, segmentation
89. AutomationWorkflowTool: Workflow automation — create/run/schedule workflows, file/email/webhook triggers, conditionals, parallel runs
90. KnowledgeBaseTool: RAG knowledge base — create KB, add docs/URLs, query, search, update, export, Q&A with sources
 
=== SYSTEM & HARDWARE ===
91. SystemAdvancedTool: System administration — services, cron jobs, firewall, startup items, hosts file, volume, battery, USB
92. NetworkAdvancedTool: Network tools — ping, traceroute, port scan, DNS lookup, SSL check, bandwidth test, SSH tunnel
93. FileSystemAdvancedTool: File system — folder sync, find/remove duplicates, encrypt/decrypt files, secure delete, split/join, checksums
94. ProcessAutomationTool: Desktop automation — find/click windows, type text, keyboard shortcuts, drag-drop, image recognition on screen
95. PrinterTool: Printer management — list printers, print files/PDFs/images, manage queue, cancel jobs, export to PDF
96. ClipboardAdvancedTool: Clipboard — get/set text/images/files/HTML, monitor changes, clipboard history, transform content
97. HardwareMonitorTool: Hardware monitoring — CPU/GPU/disk temperatures, fan speeds, voltages, SMART data, benchmarks
98. RaspberryPiTool: Raspberry Pi GPIO — pins, PWM, I2C, SPI, temperature sensors, servo/stepper motors, LCD, camera
99. MQTTIoTTool: MQTT/IoT — connect broker, publish/subscribe, send sensor data, device commands, Home Assistant control
100.VirtualizationTool: VM management — list/start/stop/snapshot VMs, clone, export, run commands in VM, set resources
""".strip()

    def build_tool_registry(self):
        import importlib, inspect
        registry = {}
        modules = [
            "Tools_Developer_CLI",
            "Tools_business",
            "Tools_cloud_devops",
            "Tools_communication_extended",
            "Tools_creative",
            "Tools_data_research",
            "Tools_media",
            "Tools_productivity",
            "Tools_security_ai",
            "Tools_system_hardware",
        ]
        for mod_name in modules:
            try:
                mod = importlib.import_module(mod_name)
                for name, obj in inspect.getmembers(mod, inspect.isclass):
                    if name.endswith('Tool'):
                        registry[name] = obj
            except ImportError:
                pass  
        return registry
    
    def build_planner_prompt(self, task: str, workspace_summary: str) -> str:
        return f"""You are a task planner for an AI automation agent.
        Your job: break the user's task into 2-5 clear atomic steps AND write a concise task summary.
        
        User's system:
        {workspace_summary}
 
        Available tool classes (one line each — Tool Manager will provide full details):
        {self.TOOL_INDEX}
 
        User Task: {task}
 
        Instructions:
        - Write a concise 1-2 sentence task summary (this goes to Tool Manager)
        - Break the task into 2-5 atomic steps
        - Each step should mention which tool class to use (from the index above)
        - Steps must be independently executable and verifiable
 
        Return ONLY this JSON, no explanation:
        
        {{
        "summary": "concise 1-2 sentence description of what needs to be done and which tools",
        "steps": [
        "Step 1: [action] using [ClassName]",
        "Step 2: [action] using [ClassName]",
        ...
        ]
        }}"""
        

    def build_tool_manager_phase1_prompt(self, task_summary: str) -> str:
        return f"""You are a Tool Selector for an AI agent with access to 100 tool classes.
 
Task to accomplish:
{task_summary}
 
Tool Index (100 classes, one line each):
{self.TOOL_INDEX}
 
Instructions:
- Read the task carefully
- Select tool classes that are most likely needed
- Be precise — only select tools genuinely required, not tangentially related ones
- If the task clearly needs only 1-2 tools, select only those
 
Return ONLY a JSON array of class names, no explanation:
["ClassName1", "ClassName2", ...]"""

    def build_tool_manager_phase2_prompt(self, task_summary: str, use_docs: str) -> str:
        return f"""You are a Tool Selector. Review the detailed docs of shortlisted tools.
Your job: confirm which tools are genuinely needed and reject any that are not.
 
Task:
{task_summary}
 
Detailed tool documentation:
{use_docs}
 
Instructions:
- Keep tools that are clearly needed for this task
- Reject tools that were shortlisted but aren't actually needed
- For kept tools, preserve their FULL documentation exactly as shown
- Do not summarize or shorten — Coder needs the full method details
 
If you need to check another tool not in this list, say:
NEED_MORE: ClassName1, ClassName2"""

    def build_coder_prompt(self, step: str, task: str, selected_tool_docs: str, workspace_summary: str, prev_globals: str = "", error: str = "") -> str:
        fix = f"\nPrevious error to fix:\n{error}" if error else ""
        reuse = f"\nPreviously available globals from prior steps:\n{prev_globals}" if prev_globals else ""
    
        return f"""You are an expert Python code generator for a desktop automation agent.
Write ONLY executable Python code — NO explanations outside # comments.
Your entire response goes into a .py file executed by Python subprocess.
Do NOT use exec() — write complete standalone scripts.
Install any missing libraries with subprocess pip install at the top if needed.
 
User's system:
{workspace_summary}

Follow what instruction to use tools here given:-

Tool classes available to import and use:

Follow what instruction to use tools here given:-

{selected_tool_docs}
 
Import Syntax:-
from Tools_Developer_CLI import GitTool, GitHubTool, GitLabTool, DockerTool, PackageManagerTool, VSCodeTool, TerminalTool, MakefileTool, CMakeTool, DebuggerTool
from Tools_business import StripeTool, RazorpayTool, ShopifyTool, InvoiceTool, AccountingTool, CRMTool, EmailMarketingTool, AnalyticsTool, InventoryTool, ContractTool
from Tools_cloud_devops import AWSS3Tool, AWSLambdaTool, AWSECSTool, CloudflareTool, VercelTool, NetlifyTool, RailwayTool, KubernetesTool, TerraformTool, MonitoringTool
from Tools_communication_extended import MicrosoftTeamsTool, ZoomTool, TwilioTool, SendGridTool, PushNotificationTool, RSSFeedTool, WebhookTool, CalendarTool, ChatOpsAutomationTool, SMTPAdvancedTool
from Tools_creative import FigmaTool, BlenderTool, SVGTool, CanvaTool, FontTool, ColorTool, IconTool, DiagramTool, PrintTool, ThreeDTool
from Tools_data_research import DataAnalysisTool, VisualizationTool, WebScrapingAdvancedTool, SearchResearchTool, FinancialDataTool, SocialMediaDataTool, WeatherGeoTool, TextAnalyticsTool, DatabaseTool, ReportGeneratorTool
from Tools_media import FFmpegTool, YouTubeDownloaderTool, AudioTool, ImageAdvancedTool, ScreenRecorderTool, TextToSpeechTool, VideoEditingTool, PodcastTool, StreamingTool, MediaMetadataTool
from Tools_productivity import GoogleWorkspaceTool, NotionAdvancedTool, LinearTool, AsanaTool, TrelloTool, ClickUpTool, TodoistTool, ObsidianTool, BookmarkManagerTool, TimeTrackingTool
from Tools_security_ai import SecurityScannerTool, CryptographyTool, PenetrationTestingTool, AIImageGenerationTool, AITextGenerationAdvancedTool, MLModelTool, SpeechAITool, ComputerVisionTool, AutomationWorkflowTool, KnowledgeBaseTool
from Tools_system_hardware import SystemAdvancedTool, NetworkAdvancedTool, FileSystemAdvancedTool, ProcessAutomationTool, PrinterTool, ClipboardAdvancedTool, HardwareMonitorTool, RaspberryPiTool, MQTTIoTTool, VirtualizationTool
 as per need Use

Full task context: {task}
This specific step to implement: {step}
{reuse}{fix}
 
Rules:
- Use ONLY the methods documented in the tool docs above
- Use EXACT method signatures shown — do not guess parameters
- Handle errors gracefully with try/except
- Print progress so Verifier can confirm success
- Follow what instruction to use tools here given:
 
Write complete Python code:"""

    def build_auditor_prompt(self, code: str) -> str:
        return f"""[SECURITY AUDITOR] You analyze Python code for dangerous operations only.
 
BLOCK if code contains:
- Deleting system files without explicit user request (rm -rf /, del /s /q C:\\)
- Stealing credentials, passwords, cookies, tokens, or SSH keys
- Reverse shells or remote access backdoors
- Fork bombs or infinite resource consumption
- Accessing /etc/passwd, /etc/shadow, Windows SAM or registry credential stores
- Obfuscated or encoded executable payloads
- Exfiltrating user data to unknown external endpoints
 
ALLOW if code contains:
- Normal file operations (read, write, create, delete user files)
- Web scraping or API calls
- Sending emails or messages the user requested
- pip installs for required libraries
- Browser automation for user-directed tasks
- Database queries or data processing
- Standard system information retrieval
 
CODE TO AUDIT:
{code}
 
Answer format: first word must be ALLOW or BLOCK, then one line reason.
Example: ALLOW safe file read and email send operation
Example: BLOCK attempts to read /etc/shadow credential store"""

    def build_verifier_prompt(self, step: str, output: str) -> str:
        return f"""Did this automation step complete successfully?
 
Step that was supposed to run:
{step}
 
Execution output:
{output[:600]}
 
Answer YES if:
- The output shows the action was completed
- There are success messages, file paths, IDs, or confirmation text
- No Python exceptions or error tracebacks in output
 
Answer NO if:
- Output contains Python exceptions, tracebacks, or ImportError
- Output shows authentication failures or permission denied
- Output is empty when output was expected
- The step clearly did not accomplish its goal
 
Reply with ONE word only: YES or NO"""

    def build_use_docs_for_classes(self, class_names: list, tool_registry: dict) -> str:
        """
tool_registry: flat dict of {ClassName: ClassObject} built from all 10 tool files.
Returns combined use strings for requested class names.
"""

        docs = []
        for name in class_names:
            cls = tool_registry.get(name)
            if cls and hasattr(cls, 'use'):
                docs.append(f"=== {name} ===\n{cls.use}")
            elif cls:
                # fallback if use variable missing — use description + method list
                import inspect
                methods = [m for m in dir(cls)
                           if not m.startswith('_') and callable(getattr(cls, m))]
                desc = getattr(cls, 'description', 'No description')
                docs.append(f"=== {name} ===\nPurpose: {desc}\nMethods: {', '.join(methods)}")

            else:
                docs.append(f"=== {name} ===\nClass not found in registry.")

        return "\n\n".join(docs)
    
    def _emit(self, msg, color="#8E8AAE"):
        self._log(f'<font color="{color}">{msg}</font>')

    def _clean_code(self, raw:str) -> str:
        s = raw.strip()
        for tag in ("```python","```"):
            if s.startswith(tag): s = s[len(tag):]
        if s.endswith("```"): s = s[:-3]
        return s.strip()

    def chat(self, user_msg:str) -> str:
        self.mem_chat.save_context("user", user_msg)
        hist = self.mem_chat.load_memory_variables()
        prompt = f"""You are NPM Agent, an advanced AI assistant powered by NPMAI Ecosystem.
You help with coding, automation, analysis, and general questions.
Be concise, helpful, and friendly. If the user wants to run something on their computer,
tell them to phrase it as a task (e.g. "do X on my computer").

Conversation history:
{hist}

User: {user_msg}
Assistant:"""
        resp = self.chatter.invoke(prompt)
        self.mem_chat.save_context("assistant", resp)
        return resp

    def select_tools(self, task_summary: str) -> str:
        import re, json as _json
 
        p1 = self.build_tool_manager_phase1_prompt(task_summary)
        raw = self.tool_manager.invoke(p1)
        self.mem_tool_manager.save_context("phase1_raw", raw)
    
        try:
            match = re.search(r'\[.*?\]', raw, re.DOTALL)
            shortlist = _json.loads(match.group()) if match else []
            shortlist = [s for s in shortlist if isinstance(s, str)]
        except:
            shortlist = []
 
        self._emit(f"  → Tool Manager shortlisted: {shortlist}", "#A78BFA")
 
        if not shortlist:
            return ""
 
        use_docs = self.build_use_docs_for_classes(shortlist, self.tool_registry)
        p2 = self.build_tool_manager_phase2_prompt(task_summary, use_docs)
        final_docs = self.tool_manager.invoke(p2)
        self.mem_tool_manager.save_context("phase2_selected", final_docs)
 
        if "NEED_MORE:" in final_docs:
            import re as _re
            need_line = _re.search(r'NEED_MORE:\s*(.+)', final_docs)
            if need_line:
                extra_names = [n.strip() for n in need_line.group(1).split(',')]
                self._emit(f"  → Tool Manager requesting more docs: {extra_names}", "#A78BFA")
                extra_docs = self.build_use_docs_for_classes(extra_names, self.tool_registry)
                combined = use_docs + "\n\n" + extra_docs
                p2b = self.build_tool_manager_phase2_prompt(task_summary, combined)
                final_docs = self.tool_manager.invoke(p2b)
                self.mem_tool_manager.save_context("phase2b_final", final_docs)
 
        return final_docs

    def plan(self, task: str) -> tuple:
        import re, json as _json
        ws = self.workspace.context_summary()
        prompt = self.build_planner_prompt(task, ws)
        raw = self.planner.invoke(prompt)
        self.mem_plan.save_context("plan_raw", raw)
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                parsed = _json.loads(match.group())
                summary = parsed.get("summary", task)
                steps   = [str(s) for s in parsed.get("steps", [task])]
                return summary, steps
        except:
            pass
        return task, [task]

    
    def generate_code(self, step: str, task: str, selected_tool_docs: str,
                      prev_globals: str = "", error: str = "") -> str:
        ws = self.workspace.context_summary()
        prompt = self.build_coder_prompt(step, task, selected_tool_docs, ws, prev_globals, error)
        raw = self.coder.invoke(prompt)
        return self._clean_code(raw)

    
    def audit(self, code: str) -> tuple:
        prompt = self.build_auditor_prompt(code)
        r = self.auditor.invoke(prompt).strip()
        safe = r.upper().startswith("ALLOW")
        return safe, r
         

    def verify(self, step: str, output: str, success: bool) -> tuple:
        if not success:
            return False, output
        prompt = self.build_verifier_prompt(step, output)
        r = self.verifier.invoke(prompt).strip().upper()
        return r.startswith("YES"), output
        

    def run_task(self, task: str, killed_flag: list = None) -> bool:
        if killed_flag is None: killed_flag = [False]
 
        self._emit(f"▸ Starting task: {task}", "#00E5FF")
        self._progress(5)
 
        if len(task.split()) < 4 and "?" in task:
            resp = self.chat(task)
            self._emit(resp, "#F0EEFF")
            self._progress(100)
            return True
 
        self._emit("▸ Scanning workspace…", "#4E4B6A")
        try: self.workspace.scan()
        except: pass
        self._progress(10)
        self._status("Planning…")
        self._emit("▸ Planning steps…", "#A78BFA")
        task_summary, steps = self.plan(task)
        self._emit(f"▸ Task summary: {task_summary}", "#4E4B6A")
        self._emit(f"▸ Plan: {len(steps)} step(s)", "#A78BFA")
        for i, s in enumerate(steps):
            self._emit(f"  {i+1}. {s}", "#4E4B6A")
        self._progress(20)
        self._status("Selecting tools…")
        self._emit("▸ Tool Manager selecting tools…", "#A78BFA")
        selected_tool_docs = self.select_tools(task_summary)
        if selected_tool_docs:
            import re
            selected_names = re.findall(r'=== (\w+) ===', selected_tool_docs)
            self._emit(f"  ✓ Selected: {selected_names}", "#2AFFA0")
        else:
            self._emit("  → No specific tools selected, Coder uses general knowledge", "#4E4B6A")
        self._progress(30)
        total_steps  = len(steps)
        prev_globals = ""
 
        for step_idx, step in enumerate(steps):
            if killed_flag[0]:
                self._emit("✗ Task cancelled by user.", "#FF6B9D"); return False
 
            step_num  = step_idx + 1
            prog_base = 30 + int((step_idx / total_steps) * 60)
            self._emit(f"\\n▸ Step {step_num}/{total_steps}: {step}", "#00E5FF")
            self._status(f"Step {step_num}/{total_steps}…")
 
            tried     = 0
            max_retries = 12
            last_error  = ""
 
            while tried < max_retries:
                if killed_flag[0]:
                    self._emit("✗ Cancelled.", "#FF6B9D"); return False
 
                self._emit(f"  → Generating code (attempt {tried+1})…", "#4E4B6A")
                self._progress(prog_base + 2)
                code = self.generate_code(step, task, selected_tool_docs,
                                          prev_globals, last_error)
                self.mem_code.save_context(step, code)
 
                self._emit("  → Security audit…", "#A78BFA")
                safe, reason = self.audit(code)
                if not safe:
                    self._emit(f"  🚫 BLOCKED: {reason}", "#FF6B9D")
                    self._progress(100)
                    return False
 
                self._emit("  ✓ Audit passed", "#2AFFA0")
                self._progress(prog_base + 6)
 
                self._emit("  → Executing…", "#4E4B6A")
                self._status("Executing…")
                success, output = self.executor.run(code)
                self._progress(prog_base + 10)
 
                verified, feedback = self.verify(step, output, success)
 
                if verified:
                    self._emit(f"  ✓ Step {step_num} complete", "#2AFFA0")
                    prev_globals += f"\\n# After step {step_num}:\\n{output[:300]}"
                    self.mem_plan.save_context(f"step_{step_num}", "DONE: " + output[:200])
                    break
                else:
                    tried += 1
                    last_error = output
                    self._emit(f"  ⚠ Retry {tried}/{max_retries}: {output[:120]}", "#FFB347")
                    self._progress(prog_base + 5 + tried)
 
            else:
                self._emit(f"  ✗ Step {step_num} failed after {max_retries} attempts.", "#FF6B9D")
                self._status("Failed")
                self._save_task_history(task, False)
                return False
 
        self._progress(100)
        self._status("Done ✓")
        self._emit("\\n✓ ─── All steps completed successfully ───", "#2AFFA0")
        self._save_task_history(task, True)
        return True

    def _save_task_history(self, task:str, success:bool):
        hist_path = Path.home()/".npmai_agent"/"history.json"
        hist_path.parent.mkdir(exist_ok=True)
        history = []
        if hist_path.exists():
            try: history = json.loads(hist_path.read_text())
            except: history = []
        history.insert(0,{
            "task":   task,
            "success":success,
            "time":   datetime.now().isoformat(),
        })
        history = history[:50]
        hist_path.write_text(json.dumps(history,indent=2))

    @staticmethod
    def load_task_history() -> list:
        p = Path.home()/".npmai_agent"/"history.json"
        if p.exists():
            try: return json.loads(p.read_text())
            except: pass
        return []
