from npmai import Ollama, Memory
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
              ("ollama",       "ollama"),
              ("openai",       "openai"),
              ("anthropic",    "anthropic"),
              ("genai",        "google.generativeai"),
              ("groq",        "groq"),
              ("huggingface_hub", "huggingface_hub"),
              ("cohere", "cohere"),
              ("mistralai", "mistralaiai"),
              ("boto3",      "boto3"),
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
        from mistralai.client import Mistral
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
