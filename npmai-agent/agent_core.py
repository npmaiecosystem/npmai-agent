import os, sys, json, re, shutil, subprocess, tempfile, traceback
import threading, time, smtplib, imaplib, email as email_lib
import hashlib, base64, platform, glob, zipfile, tarfile
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional
from abc import ABC, abstractmethod


def _ensure(pkg, import_name=None):
    n = import_name or pkg
    try:
        __import__(n)
    except ImportError:
        subprocess.run([sys.executable,"-m","pip","install",pkg,"-q"],check=False)

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

from npmai import Ollama, Memory, Rag
from langchain_core.output_parsers import StrOutputParser

#L LLM Backend
""" 
This is just a abstract which is used for a type of validation and attachment.
"""
class LLMBackend(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        ...


# 1. Ollama — (local models) 
"""
THIS WILL USE LOCAL COMPUTE IF YOU WANT TO USE NPMAI WHICH WILL RUN ON CLOUD NOT YOUR MACHINE THEN DO NOT PASS ANY THING IN 
LLM PIPELINE NPMAI IS USED HERE BY DEFAULT.
"""
class Ollama_Local(LLMBackend):
    def __init__(self, model="llama3.2:3b", temperature=0.2):
        import ollama
        self.client = ollama
        self.model = model
        self.temperature = temperature

    def invoke(self, prompt: str) -> str:
        r = self.client.generate(model=self.model, prompt=prompt,
                                  options={"temperature": self.temperature})
        return r["response"]


# 2. OpenAI (GPT-4o, GPT-4, etc.)
class OpenAIBackend(LLMBackend):
    def __init__(self, api_key, model="gpt-4o"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def invoke(self, prompt: str) -> str:
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content


# 3. Anthropic (Claude)
class AnthropicBackend(LLMBackend):
    def __init__(self, api_key, model="claude-sonnet-4-6"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def invoke(self, prompt: str) -> str:
        r = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return "".join(b.text for b in r.content if b.type == "text")


# 4. Google Gemini
class GeminiBackend(LLMBackend):
    def __init__(self, api_key, model="gemini-2.0-flash"):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def invoke(self, prompt: str) -> str:
        r = self.model.generate_content(prompt)
        return r.text


# 5. Groq (fast inference — Llama, Mixtral hosted)
class GroqBackend(LLMBackend):
    def __init__(self, api_key, model="llama-3.3-70b-versatile"):
        from groq import Groq
        self.client = Groq(api_key=api_key)
        self.model = model

    def invoke(self, prompt: str) -> str:
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content


# 6. Mistral (their own API)
class MistralBackend(LLMBackend):
    def __init__(self, api_key, model="mistral-large-latest"):
        from mistralai import Mistral
        self.client = Mistral(api_key=api_key)
        self.model = model

    def invoke(self, prompt: str) -> str:
        r = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content


# 7. Cohere
class CohereBackend(LLMBackend):
    def __init__(self, api_key, model="command-r-plus"):
        import cohere
        self.client = cohere.Client(api_key)
        self.model = model

    def invoke(self, prompt: str) -> str:
        r = self.client.chat(model=self.model, message=prompt)
        return r.text


# 8. Azure OpenAI (enterprise OpenAI via Azure)
class AzureOpenAIBackend(LLMBackend):
    def __init__(self, api_key, endpoint, deployment, api_version="2024-08-01-preview"):
        from openai import AzureOpenAI
        self.client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint,
                                   api_version=api_version)
        self.deployment = deployment

    def invoke(self, prompt: str) -> str:
        r = self.client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content


# 9. AWS Bedrock (Claude/Llama/Titan hosted on AWS)
class BedrockBackend(LLMBackend):
    def __init__(self, model_id="anthropic.claude-3-sonnet-20240229-v1:0", region="us-east-1"):
        import boto3, json as _json
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = model_id
        self._json = _json

    def invoke(self, prompt: str) -> str:
        body = self._json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        })
        r = self.client.invoke_model(modelId=self.model_id, body=body)
        result = self._json.loads(r["body"].read())
        return result["content"][0]["text"]


# 10. HuggingFace Inference API (any open model hosted there)
class HuggingFaceBackend(LLMBackend):
    def __init__(self, api_key, model="meta-llama/Llama-3.1-8B-Instruct"):
        from huggingface_hub import InferenceClient
        self.client = InferenceClient(model=model, token=api_key)

    def invoke(self, prompt: str) -> str:
        return self.client.text_generation(prompt, max_new_tokens=512)


# 11. Local llama.cpp server (fully offline, no API key)
class LlamaCppBackend(LLMBackend):
    def __init__(self, base_url="http://localhost:8080"):
        import requests
        self.requests = requests
        self.base_url = base_url

    def invoke(self, prompt: str) -> str:
        r = self.requests.post(f"{self.base_url}/completion", json={"prompt": prompt})
        return r.json()["content"]


class CredStore(ensure):
    """Encrypts credentials with a machine-specific key and stores locally."""
    _PATH = Path.home() / ".npmai_agent" / "creds.json"

    def __init__(self):
        super().__init__()

    @staticmethod
    def _key() -> bytes:
        from cryptography.fernet import Fernet
        kf = Path.home() / ".npmai_agent" / ".key"
        kf.parent.mkdir(exist_ok=True)
        if kf.exists():
            return kf.read_bytes()
        k = Fernet.generate_key()
        kf.write_bytes(k)
        kf.chmod(0o600)
        return k

    @classmethod
    def save(cls, name: str, data: dict):
        from cryptography.fernet import Fernet
        f = Fernet(cls._key())
        store = {}
        if cls._PATH.exists():
            try: store = json.loads(f.decrypt(cls._PATH.read_bytes()))
            except: store = {}
        store[name] = data
        cls._PATH.write_bytes(f.encrypt(json.dumps(store).encode()))

    @classmethod
    def load(cls, name: str) -> dict:
        from cryptography.fernet import Fernet
        if not cls._PATH.exists(): return {}
        try:
            f = Fernet(cls._key())
            store = json.loads(f.decrypt(cls._PATH.read_bytes()))
            return store.get(name, {})
        except: return {}

    @classmethod
    def all_keys(cls) -> list:
        from cryptography.fernet import Fernet
        if not cls._PATH.exists(): return []
        try:
            f = Fernet(cls._key())
            return list(json.loads(f.decrypt(cls._PATH.read_bytes())).keys())
        except: return []

class Workspace(ensure):
    """Scans the file system and builds a context profile for the agent."""
    _PATH = Path.home() / ".npmai_agent" / "workspace.json"

    def __init__(self):
        self._PATH.parent.mkdir(exist_ok=True)
        self.data = self._load()

    def _load(self) -> dict:
        if self._PATH.exists():
            try: return json.loads(self._PATH.read_text())
            except: pass
        return {}

    def scan(self):
        home = Path.home()
        scan_dirs = {
            "desktop":   home/"Desktop",
            "downloads": home/"Downloads",
            "documents": home/"Documents",
            "pictures":  home/"Pictures",
            "videos":    home/"Videos",
            "music":     home/"Music",
        }
        found = {}
        for name, path in scan_dirs.items():
            if path.exists():
                files = []
                try:
                    for f in path.iterdir():
                        if f.is_file():
                            files.append({"name":f.name,"size":f.stat().st_size,
                                          "modified":datetime.fromtimestamp(f.stat().st_mtime).isoformat()})
                except: pass
                found[name] = {"path":str(path),"files":files[:40]}
        self.data["paths"]   = found
        self.data["home"]    = str(home)
        self.data["os"]      = platform.system()
        self.data["python"]  = sys.version
        self.data["scanned"] = datetime.now().isoformat()
        self._save()
        return self.data

    def update_profile(self, key, value):
        self.data[key] = value
        self._save()

    def _save(self):
        self._PATH.write_text(json.dumps(self.data, indent=2))

    def context_summary(self) -> str:
        """Returns a short text summary passed to the planner LLM."""
        lines = [f"OS: {self.data.get('os','unknown')}", f"Home: {self.data.get('home','~')}"]
        for k,v in self.data.get("paths",{}).items():
            lines.append(f"{k.capitalize()}: {v.get('path','')}  ({len(v.get('files',[]))} files)")
        if "user_name" in self.data:
            lines.append(f"User: {self.data['user_name']}")
        return "\n".join(lines)

class ToolResult(ensure):
    def __init__(self, success:bool, output:str, data=None):
        super().__init__()
        self.success = success
        self.output  = output
        self.data    = data
    def __str__(self): return self.output


class Executor(ensure):
    """Writes code to temp file, runs as child process, streams output."""

    def __init__(self, log_cb:Callable=None, timeout:int=120):
        super().__init__()
        self._log     = log_cb or print
        self._timeout = timeout
        self._proc    = None
        self._killed  = False

    def run(self, code:str) -> tuple:
        """Returns (success:bool, full_output:str)"""
        self._killed = False
        tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False,
                                         mode="w", encoding="utf-8")
        tmp.write(code); tmp.close()
        output_lines = []
        try:
            self._proc = subprocess.Popen(
                [sys.executable, tmp.name],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            for line in self._proc.stdout:
                line = line.rstrip()
                output_lines.append(line)
                self._log(f'<font color="#8E8AAE">{line}</font>')
            self._proc.wait(timeout=self._timeout)
            success = (self._proc.returncode == 0) and not self._killed
            return success, "\n".join(output_lines)
        except subprocess.TimeoutExpired:
            self.kill()
            return False, "TIMEOUT: Script exceeded time limit."
        except Exception as e:
            return False, f"EXECUTOR ERROR: {e}"
        finally:
            try: os.unlink(tmp.name)
            except: pass
            self._proc = None

    def kill(self):
        self._killed = True
        if self._proc:
            try: self._proc.kill()
            except: pass

class AgentBrain(ensure):
    """
    Full pipeline:
    Intent → Plan → [for each step: Generate → Audit → Execute → Verify] → Done
    """
    PARSER = StrOutputParser()

    TOOLS = {
    "email":       EmailTool,
    "files":       FileTool,
    "pdf":         PDFTool,
    "web":         WebTool,
    "spreadsheet": SpreadsheetTool,
    "github":      GitHubTool,
    "slack":       SlackTool,
    "discord":     DiscordTool,
    "whatsapp":    WhatsAppTool,
    "notion":      NotionTool,
    "twitter":     TwitterTool,
    "system":      SystemTool,
    "image":       ImageTool,
    "scheduler":   SchedulerTool,
    "jira":        JiraTool,
    "telegram":    TelegramTool,
    "qr":          QRTool,
    "voice":       VoiceTool,
    "watcher":     WatcherTool,
    "rag":         RAGTool,
    "ssh":         SSHTool,
    }

    TOOLS_SUMMARY = "\n".join(
        f"- {k}: {v.description}" for k,v in TOOLS.items()
        )

    def __init__(self, log_cb:Callable=None, progress_cb:Callable=None,
                 status_cb:Callable=None, planner: LLMBackend = None, tool_manager: LLMBackend = None, coder: LLMBackend = None,
                 auditor: LLMBackend = None, verifier: LLMBackend = None, chatter: LLMBackend = None):
        super().__init__()
        self._log      = log_cb      or print
        self._progress = progress_cb or (lambda v: None)
        self._status   = status_cb   or (lambda s: None)
        self.workspace = Workspace()
        self.executor  = Executor(log_cb=log_cb)
        for i  in [planner,tool_manager,coder,auditor,verifier,chatter]:
            if i is None:
                break
            elif i:
                if not isinstance(i, LLMBackend):
                    raise TypeError(f"{i} must implement LLMBackend (i.e. have .invoke(prompt)->str)")
            
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
        self.tool_manager = Memory("agent_plan")
        self.mem_code  = Memory("agent_code")
        self.mem_chat  = Memory("agent_chat")
        self.mem_tasks = Memory("agent_tasks")

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

    def tool_manager(self, task:str) -> str:
        self.tool_manager.save_context("task", task)f
        hist = self.tool_manager.load_memory_variables()
        prompt = f"""You are NPMAI Agent, an advanced AI assistant powered by NPMAI ECOSYSTEM.
        You help w

        #UNDER DEVELOPMENT 
        """

    def plan(self, task:str) -> list:
        ws = self.workspace.context_summary()
        tool_list = TOOLS_SUMMARY
        prompt = f"""You are a task planner. Break the following user task into 2-5 clear,
atomic executable steps. Each step should be independently verifiable.

User's computer context:
{ws}

Available tools (Python modules):
{tool_list}

User Task: {task}

Return ONLY a JSON array of step strings, no explanation:
["step 1 description", "step 2 description", ...]"""
        raw = self.planner.invoke(prompt)
        try:
            match = re.search(r'\[.*?\]', raw, re.DOTALL)
            if match:
                steps = json.loads(match.group())
                return [str(s) for s in steps]
        except: pass
        return [task]

    def generate_code(self, step:str, task:str, prev_globals:str="",
                      error:str="") -> str:
        ws  = self.workspace.context_summary()
        fix = f"\nPrevious error to fix:\n{error}" if error else ""
        reuse = f"\nPreviously executed globals available:\n{prev_globals}" if prev_globals else ""
        prompt = f"""You are an expert Python code generator for a desktop automation agent.
Write ONLY executable Python code — NO explanations outside # comments.
Install any missing libraries via subprocess pip install in the code.
Your entire response goes into a .py file run by Python subprocess.
Do NOT use exec() — write complete standalone scripts.

User's system:
{ws}

Available tool templates you can import and use:
from agent_core import EmailTool, FileTool, WebTool, SpreadsheetTool
from agent_core import GitHubTool, SlackTool, PDFTool, ImageTool
from agent_core import SystemTool, TelegramTool, QRTool, RAGTool, SSHTool
from agent_core import CredStore, Workspace

Full task context: {task}
This specific step to implement: {step}
{reuse}{fix}

Write complete Python code:"""
        raw = self.coder.invoke(prompt)
        return self._clean_code(raw)

    def audit(self, code:str) -> tuple:
        """Returns (is_safe:bool, reason:str)"""
        prompt = f"""[SECURITY AUDITOR] Analyze this Python code.
HIGH RISK — answer 'BLOCK': deleting system files unprompted, stealing credentials/passwords/cookies,
reverse shells, fork bombs, obfuscated destructive code, accessing /etc/passwd or Windows SAM.
SAFE — answer 'ALLOW': file operations, web scraping, sending emails, pip installs,
reading user files, making API calls, browser automation for user tasks.

CODE:
{code}

Answer format: ALLOW or BLOCK followed by one line reason."""
        r = self.auditor.invoke(prompt).strip()
        safe = r.upper().startswith("ALLOW")
        return safe, r

    def verify(self, step:str, output:str, success:bool) -> tuple:
        """Returns (verified:bool, feedback:str)"""
        if not success:
            return False, output
        prompt = f"""Did this step complete successfully?
Step: {step}
Execution output: {output[:500]}

Answer 'YES' if step completed, 'NO' if it clearly failed. One word only."""
        r = self.verifier.invoke(prompt).strip().upper()
        return r.startswith("YES"), output

    def run_task(self, task:str, killed_flag:list=None) -> bool:
        """Main entry point. killed_flag=[False] passed from UI kill button."""
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
        steps = self.plan(task)
        self._emit(f"▸ Plan: {len(steps)} step(s)", "#A78BFA")
        for i,s in enumerate(steps):
            self._emit(f"  {i+1}. {s}", "#4E4B6A")
        self._progress(20)

        total_steps = len(steps)
        prev_globals = ""

        for step_idx, step in enumerate(steps):
            if killed_flag[0]:
                self._emit("✗ Task cancelled by user.", "#FF6B9D"); return False

            step_num = step_idx + 1
            prog_base = 20 + int((step_idx / total_steps) * 70)
            self._emit(f"\n▸ Step {step_num}/{total_steps}: {step}", "#00E5FF")
            self._status(f"Step {step_num}/{total_steps}…")

            tried = 0
            max_retries = 12
            last_error  = ""

            while tried < max_retries:
                if killed_flag[0]:
                    self._emit("✗ Cancelled.", "#FF6B9D"); return False

                self._emit(f"  → Generating code (attempt {tried+1})…", "#4E4B6A")
                self._progress(prog_base + 2)
                code = self.generate_code(step, task, prev_globals, last_error)
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
                    prev_globals += f"\n# After step {step_num}:\n{output[:300]}"
                    self.mem_plan.save_context(f"step_{step_num}", "DONE: "+output[:200])
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
        self._emit("\n✓ ─── All steps completed successfully ───", "#2AFFA0")
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
