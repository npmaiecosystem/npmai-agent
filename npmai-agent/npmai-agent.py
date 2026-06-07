import os, sys, json, re, shutil, subprocess, tempfile, traceback
import threading, time, smtplib, imaplib, email as email_lib
import hashlib, base64, platform, glob, zipfile, tarfile
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Callable, Optional


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

class EmailTool(ensure):
    name = "email"
    description = "Send emails via Gmail/SMTP, read inbox via IMAP, bulk email from CSV"

    def __init__(self):
        super().__init__()

    @staticmethod
    def send(to:str, subject:str, body:str, attachments:list=None,
             cred_key:str="gmail") -> ToolResult:
        creds = CredStore.load(cred_key)
        user  = creds.get("email","")
        pwd   = creds.get("password","")
        host  = creds.get("smtp_host","smtp.gmail.com")
        port  = int(creds.get("smtp_port",587))
        if not user or not pwd:
            return ToolResult(False,"No email credentials. Add them in Settings → Credentials.")
        try:
            msg = MIMEMultipart()
            msg["From"] = user; msg["To"] = to; msg["Subject"] = subject
            msg.attach(MIMEText(body,"html"))
            if attachments:
                for fp in attachments:
                    with open(fp,"rb") as fh:
                        part = MIMEBase("application","octet-stream")
                        part.set_payload(fh.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition",f"attachment; filename={Path(fp).name}")
                    msg.attach(part)
            with smtplib.SMTP(host,port) as s:
                s.starttls(); s.login(user,pwd); s.sendmail(user,to,msg.as_string())
            return ToolResult(True,f"✓ Email sent to {to}")
        except Exception as e:
            return ToolResult(False,f"✗ Email failed: {e}")

    @staticmethod
    def send_bulk(csv_path:str, subject:str, body_template:str,
                  name_col:str="name", email_col:str="email",
                  cred_key:str="gmail") -> ToolResult:
        import pandas as pd
        try:
            df = pd.read_csv(csv_path)
            sent,failed = 0,0
            for _,row in df.iterrows():
                body = body_template.replace("{name}", str(row.get(name_col,"")))
                for col in df.columns:
                    body = body.replace(f"{{{col}}}", str(row.get(col,"")))
                r = EmailTool.send(str(row[email_col]),subject,body,cred_key=cred_key)
                if r.success: sent+=1
                else: failed+=1
                time.sleep(0.5)
            return ToolResult(True,f"✓ Sent {sent} emails, {failed} failed")
        except Exception as e:
            return ToolResult(False,f"✗ Bulk email failed: {e}")

    @staticmethod
    def read_inbox(count:int=10, cred_key:str="gmail") -> ToolResult:
        creds = CredStore.load(cred_key)
        user  = creds.get("email",""); pwd = creds.get("password","")
        host  = creds.get("imap_host","imap.gmail.com")
        if not user: return ToolResult(False,"No credentials.")
        try:
            mail = imaplib.IMAP4_SSL(host)
            mail.login(user,pwd); mail.select("inbox")
            _,ids = mail.search(None,"ALL")
            msgs = []
            for mid in ids[0].split()[-count:]:
                _,data = mail.fetch(mid,"(RFC822)")
                msg = email_lib.message_from_bytes(data[0][1])
                msgs.append({"from":msg["From"],"subject":msg["Subject"],"date":msg["Date"]})
            mail.logout()
            return ToolResult(True,f"✓ Fetched {len(msgs)} emails",msgs)
        except Exception as e:
            return ToolResult(False,f"✗ IMAP failed: {e}")

class FileTool(ensure):
    name = "files"
    description = "Rename, move, copy, zip, unzip, search, organize, convert files"

    def __init__(self):
        super().__init__()

    @staticmethod
    def bulk_rename(folder:str, pattern:str="*", prefix:str="",
                    suffix:str="", add_date:bool=False) -> ToolResult:
        p = Path(folder); count = 0
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            for f in p.glob(pattern):
                if not f.is_file(): continue
                stem = f.stem; ext = f.suffix
                new_stem = f"{prefix}{today+'_' if add_date else ''}{stem}{suffix}"
                f.rename(p / f"{new_stem}{ext}")
                count += 1
            return ToolResult(True,f"✓ Renamed {count} files")
        except Exception as e:
            return ToolResult(False,f"✗ Rename failed: {e}")

    @staticmethod
    def zip_folder(source:str, dest:str=None) -> ToolResult:
        sp = Path(source)
        dp = Path(dest) if dest else sp.parent / f"{sp.name}.zip"
        try:
            with zipfile.ZipFile(dp,"w",zipfile.ZIP_DEFLATED) as zf:
                if sp.is_dir():
                    for f in sp.rglob("*"):
                        if f.is_file(): zf.write(f, f.relative_to(sp.parent))
                else:
                    zf.write(sp, sp.name)
            return ToolResult(True,f"✓ Zipped to {dp}")
        except Exception as e:
            return ToolResult(False,f"✗ Zip failed: {e}")

    @staticmethod
    def unzip(zip_path:str, dest:str=None) -> ToolResult:
        zp = Path(zip_path)
        dp = Path(dest) if dest else zp.parent / zp.stem
        try:
            with zipfile.ZipFile(zp,"r") as zf: zf.extractall(dp)
            return ToolResult(True,f"✓ Extracted to {dp}")
        except Exception as e:
            return ToolResult(False,f"✗ Unzip failed: {e}")

    @staticmethod
    def find_files(folder:str, pattern:str, recursive:bool=True) -> ToolResult:
        p = Path(folder)
        fn = p.rglob if recursive else p.glob
        files = [str(f) for f in fn(pattern) if f.is_file()]
        return ToolResult(True,f"✓ Found {len(files)} files", files)

    @staticmethod
    def organize_by_type(folder:str) -> ToolResult:
        type_map = {
            "Images":  [".jpg",".jpeg",".png",".gif",".bmp",".webp",".svg",".ico"],
            "Videos":  [".mp4",".avi",".mkv",".mov",".wmv",".flv"],
            "Audio":   [".mp3",".wav",".flac",".aac",".ogg"],
            "Docs":    [".pdf",".doc",".docx",".txt",".odt"],
            "Sheets":  [".xls",".xlsx",".csv",".ods"],
            "Code":    [".py",".js",".ts",".html",".css",".java",".cpp",".c"],
            "Archives":[".zip",".tar",".gz",".rar",".7z"],
        }
        p = Path(folder); moved = 0
        try:
            for f in p.iterdir():
                if not f.is_file(): continue
                for cat,exts in type_map.items():
                    if f.suffix.lower() in exts:
                        dest = p/cat; dest.mkdir(exist_ok=True)
                        shutil.move(str(f),str(dest/f.name))
                        moved += 1; break
            return ToolResult(True,f"✓ Organized {moved} files by type")
        except Exception as e:
            return ToolResult(False,f"✗ Organize failed: {e}")

    @staticmethod
    def read_file(path:str, max_chars:int=50000) -> ToolResult:
        try:
            content = Path(path).read_text(errors="replace")
            return ToolResult(True,f"✓ Read {len(content)} chars", content[:max_chars])
        except Exception as e:
            return ToolResult(False,f"✗ Read failed: {e}")

    @staticmethod
    def write_file(path:str, content:str) -> ToolResult:
        try:
            Path(path).parent.mkdir(parents=True,exist_ok=True)
            Path(path).write_text(content)
            return ToolResult(True,f"✓ Written to {path}")
        except Exception as e:
            return ToolResult(False,f"✗ Write failed: {e}")

    @staticmethod
    def duplicate_tree(src:str, dst:str) -> ToolResult:
        try:
            shutil.copytree(src,dst)
            return ToolResult(True,f"✓ Copied {src} → {dst}")
        except Exception as e:
            return ToolResult(False,f"✗ Copy tree failed: {e}")

class PDFTool(ensure):
    name = "pdf"
    description = "Merge, split, extract text, add watermark, rotate PDF pages"

    def __init__(self):
        super().__init__()

    @staticmethod
    def extract_text(path:str) -> ToolResult:
        try:
            from pypdf import PdfReader
            r = PdfReader(path)
            text = "\n".join(p.extract_text() or "" for p in r.pages)
            return ToolResult(True,f"✓ Extracted {len(text)} chars", text)
        except Exception as e:
            return ToolResult(False,f"✗ PDF extract failed: {e}")

    @staticmethod
    def merge(paths:list, out:str) -> ToolResult:
        try:
            from pypdf import PdfMerger
            m = PdfMerger()
            for p in paths: m.append(p)
            m.write(out); m.close()
            return ToolResult(True,f"✓ Merged {len(paths)} PDFs → {out}")
        except Exception as e:
            return ToolResult(False,f"✗ Merge failed: {e}")

    @staticmethod
    def split(path:str, out_dir:str) -> ToolResult:
        try:
            from pypdf import PdfReader, PdfWriter
            r = PdfReader(path); Path(out_dir).mkdir(exist_ok=True)
            for i,page in enumerate(r.pages):
                w = PdfWriter(); w.add_page(page)
                out = str(Path(out_dir)/f"page_{i+1}.pdf")
                with open(out,"wb") as fh: w.write(fh)
            return ToolResult(True,f"✓ Split into {len(r.pages)} pages in {out_dir}")
        except Exception as e:
            return ToolResult(False,f"✗ Split failed: {e}")

class WebTool(ensure):
    name = "web"
    description = "Scrape websites, search Google, download files, check URLs, take screenshots"

    def __init__(self):
        super().__init__()

    @staticmethod
    def scrape(url:str, selector:str=None) -> ToolResult:
        try:
            import requests
            from bs4 import BeautifulSoup
            r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"},timeout=15)
            soup = BeautifulSoup(r.text,"html.parser")
            if selector:
                items = [el.get_text(strip=True) for el in soup.select(selector)]
                return ToolResult(True,f"✓ Scraped {len(items)} items", items)
            return ToolResult(True,"✓ Page fetched", soup.get_text(separator="\n",strip=True)[:20000])
        except Exception as e:
            return ToolResult(False,f"✗ Scrape failed: {e}")

    @staticmethod
    def download_file(url:str, dest:str) -> ToolResult:
        try:
            import requests
            r = requests.get(url,stream=True,timeout=30)
            Path(dest).parent.mkdir(parents=True,exist_ok=True)
            with open(dest,"wb") as fh:
                for chunk in r.iter_content(8192): fh.write(chunk)
            return ToolResult(True,f"✓ Downloaded to {dest}")
        except Exception as e:
            return ToolResult(False,f"✗ Download failed: {e}")

    @staticmethod
    def screenshot_url(url:str, out:str="screenshot.png") -> ToolResult:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as pw:
                b = pw.chromium.launch(headless=True)
                pg = b.new_page(); pg.goto(url,timeout=20000)
                pg.screenshot(path=out,full_page=True); b.close()
            return ToolResult(True,f"✓ Screenshot saved to {out}")
        except Exception as e:
            return ToolResult(False,f"✗ Screenshot failed: {e}")

    @staticmethod
    def browser_action(url:str, actions:list) -> ToolResult:
        """actions: list of dicts like {type:'click',selector:'...'} or {type:'fill',selector:'...',value:'...'}"""
        try:
            from playwright.sync_api import sync_playwright
            results = []
            with sync_playwright() as pw:
                b = pw.chromium.launch(headless=False)
                pg = b.new_page(); pg.goto(url,timeout=20000)
                for act in actions:
                    t = act.get("type","")
                    sel = act.get("selector","")
                    if t=="click":
                        pg.click(sel); results.append(f"Clicked {sel}")
                    elif t=="fill":
                        pg.fill(sel,act.get("value","")); results.append(f"Filled {sel}")
                    elif t=="wait":
                        pg.wait_for_timeout(int(act.get("ms",1000)))
                    elif t=="screenshot":
                        pg.screenshot(path=act.get("path","action_shot.png"))
                    elif t=="extract":
                        val = pg.inner_text(sel); results.append(val)
                b.close()
            return ToolResult(True,"✓ Browser actions completed", results)
        except Exception as e:
            return ToolResult(False,f"✗ Browser action failed: {e}")

    @staticmethod
    def api_call(url:str, method:str="GET", headers:dict=None,
                 payload:dict=None) -> ToolResult:
        try:
            import requests
            fn = getattr(requests, method.lower())
            r  = fn(url, headers=headers or {}, json=payload, timeout=20)
            return ToolResult(True,f"✓ {method} {url} → {r.status_code}", r.json() if r.content else {})
        except Exception as e:
            return ToolResult(False,f"✗ API call failed: {e}")

class SpreadsheetTool(ensure):
    name = "spreadsheet"
    description = "Read/write Excel, CSV, Google Sheets; generate charts, pivot tables"


    def __init__(self):
        super().__init__()

    @staticmethod
    def read_csv(path:str) -> ToolResult:
        try:
            import pandas as pd
            df = pd.read_csv(path)
            return ToolResult(True,f"✓ {len(df)} rows × {len(df.columns)} cols",df)
        except Exception as e:
            return ToolResult(False,f"✗ CSV read failed: {e}")

    @staticmethod
    def write_excel(data, path:str, sheet:str="Sheet1") -> ToolResult:
        try:
            import pandas as pd
            df = data if hasattr(data,"to_excel") else pd.DataFrame(data)
            df.to_excel(path,index=False,sheet_name=sheet)
            return ToolResult(True,f"✓ Written to {path}")
        except Exception as e:
            return ToolResult(False,f"✗ Excel write failed: {e}")

    @staticmethod
    def google_sheets_read(sheet_id:str, range_:str="Sheet1",
                           cred_key:str="google") -> ToolResult:
        try:
            import gspread
            from google.oauth2.service_account import Credentials
            creds_data = CredStore.load(cred_key)
            if not creds_data:
                return ToolResult(False,"No Google credentials saved.")
            scopes = ["https://spreadsheets.google.com/feeds",
                      "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_info(creds_data,scopes=scopes)
            gc = gspread.authorize(creds)
            sh = gc.open_by_key(sheet_id)
            ws = sh.worksheet(range_)
            data = ws.get_all_records()
            return ToolResult(True,f"✓ {len(data)} rows from Google Sheets", data)
        except Exception as e:
            return ToolResult(False,f"✗ Sheets read failed: {e}")

class GitHubTool(ensure):
    name = "github"
    description = "Create issues, push files, read repos, manage PRs, search code"

    def __init__(self):
        super().__init__()

    @staticmethod
    def _gh(cred_key="github"):
        from github import Github
        t = CredStore.load(cred_key).get("token","")
        if not t: raise ValueError("No GitHub token. Add it in Settings → Credentials.")
        return Github(t)

    @staticmethod
    def create_issue(repo:str, title:str, body:str="",
                     labels:list=None, cred_key:str="github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            r  = gh.get_repo(repo)
            issue = r.create_issue(title=title, body=body,
                                   labels=labels or [])
            return ToolResult(True,f"✓ Issue #{issue.number} created: {issue.html_url}")
        except Exception as e:
            return ToolResult(False,f"✗ GitHub issue failed: {e}")

    @staticmethod
    def push_file(repo:str, path:str, content:str,
                  message:str="Update via NPM Agent",
                  cred_key:str="github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            r  = gh.get_repo(repo)
            try:
                existing = r.get_contents(path)
                r.update_file(path, message, content, existing.sha)
                return ToolResult(True,f"✓ Updated {path} in {repo}")
            except:
                r.create_file(path, message, content)
                return ToolResult(True,f"✓ Created {path} in {repo}")
        except Exception as e:
            return ToolResult(False,f"✗ Push failed: {e}")

    @staticmethod
    def list_issues(repo:str, state:str="open",
                    cred_key:str="github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            issues = gh.get_repo(repo).get_issues(state=state)
            data = [{"#":i.number,"title":i.title,"state":i.state,"url":i.html_url}
                    for i in issues]
            return ToolResult(True,f"✓ {len(data)} issues",data)
        except Exception as e:
            return ToolResult(False,f"✗ List issues failed: {e}")

    @staticmethod
    def get_readme(repo:str, cred_key:str="github") -> ToolResult:
        try:
            gh = GitHubTool._gh(cred_key)
            r  = gh.get_repo(repo)
            readme = r.get_readme()
            return ToolResult(True,"✓ README fetched",
                              base64.b64decode(readme.content).decode())
        except Exception as e:
            return ToolResult(False,f"✗ README failed: {e}")

    @staticmethod
    def clone_repo(url:str, dest:str) -> ToolResult:
        try:
            subprocess.run(["git","clone",url,dest],check=True,capture_output=True)
            return ToolResult(True,f"✓ Cloned to {dest}")
        except Exception as e:
            return ToolResult(False,f"✗ Clone failed: {e}")

    @staticmethod
    def git_commit_push(repo_path:str, message:str) -> ToolResult:
        try:
            for cmd in [["git","add","."],
                        ["git","commit","-m",message],
                        ["git","push"]]:
                subprocess.run(cmd,cwd=repo_path,check=True,capture_output=True)
            return ToolResult(True,f"✓ Committed and pushed: {message}")
        except Exception as e:
            return ToolResult(False,f"✗ Git push failed: {e}")

class SlackTool(ensure):
    name = "slack"
    description = "Send messages, read channels, post to threads, upload files"

    def __init__(self):
        super().__init__()


    @staticmethod
    def _client(cred_key="slack"):
        from slack_sdk import WebClient
        t = CredStore.load(cred_key).get("bot_token","")
        if not t: raise ValueError("No Slack bot token. Add in Settings → Credentials.")
        return WebClient(token=t)

    @staticmethod
    def send_message(channel:str, text:str,
                     cred_key:str="slack") -> ToolResult:
        try:
            c = SlackTool._client(cred_key)
            r = c.chat_postMessage(channel=channel,text=text)
            return ToolResult(True,f"✓ Sent to #{channel}")
        except Exception as e:
            return ToolResult(False,f"✗ Slack send failed: {e}")

    @staticmethod
    def read_channel(channel:str, limit:int=20,
                     cred_key:str="slack") -> ToolResult:
        try:
            c = SlackTool._client(cred_key)
            r = c.conversations_history(channel=channel,limit=limit)
            msgs = [{"user":m.get("user","?"),"text":m.get("text",""),
                     "ts":m.get("ts","")} for m in r["messages"]]
            return ToolResult(True,f"✓ {len(msgs)} messages",msgs)
        except Exception as e:
            return ToolResult(False,f"✗ Slack read failed: {e}")

    @staticmethod
    def upload_file(channel:str, file_path:str,
                    comment:str="", cred_key:str="slack") -> ToolResult:
        try:
            c = SlackTool._client(cred_key)
            c.files_upload(channels=channel,file=file_path,
                           initial_comment=comment)
            return ToolResult(True,f"✓ File uploaded to #{channel}")
        except Exception as e:
            return ToolResult(False,f"✗ Upload failed: {e}")

class DiscordTool(ensure):
    name = "discord"
    description = "Send messages to Discord channels via webhook or bot"

    def __init__(self):
        super().__init__()

    @staticmethod
    def send_webhook(webhook_url:str, content:str,
                     embeds:list=None) -> ToolResult:
        try:
            import requests
            payload = {"content":content}
            if embeds: payload["embeds"] = embeds
            r = requests.post(webhook_url,json=payload,timeout=10)
            return ToolResult(r.status_code in (200,204),
                              f"✓ Discord sent" if r.status_code in (200,204)
                              else f"✗ Discord failed: {r.status_code}")
        except Exception as e:
            return ToolResult(False,f"✗ Discord webhook failed: {e}")

class WhatsAppTool(ensure):
    name = "whatsapp"
    description = "Send WhatsApp messages (requires WhatsApp Web open)"

    def __init__(self):
        super().__init__()

    @staticmethod
    def send(phone:str, message:str, wait:int=15) -> ToolResult:
        try:
            import pywhatkit
            pywhatkit.sendwhatmsg_instantly(phone,message,wait_time=wait,tab_close=True)
            return ToolResult(True,f"✓ WhatsApp sent to {phone}")
        except Exception as e:
            return ToolResult(False,f"✗ WhatsApp failed: {e}")

class NotionTool(ensure):
    name = "notion"
    description = "Create/read Notion pages and database entries"

    def __init__(self):
        super().__init__()

    @staticmethod
    def create_page(parent_id:str, title:str, content:str,
                    cred_key:str="notion") -> ToolResult:
        try:
            from notion_client import Client
            token = CredStore.load(cred_key).get("token","")
            if not token: return ToolResult(False,"No Notion token.")
            n = Client(auth=token)
            page = n.pages.create(
                parent={"page_id":parent_id},
                properties={"title":{"title":[{"text":{"content":title}}]}},
                children=[{"object":"block","type":"paragraph",
                           "paragraph":{"rich_text":[{"text":{"content":content}}]}}]
            )
            return ToolResult(True,f"✓ Notion page created: {page['url']}")
        except Exception as e:
            return ToolResult(False,f"✗ Notion failed: {e}")

    @staticmethod
    def add_db_entry(db_id:str, props:dict,
                     cred_key:str="notion") -> ToolResult:
        try:
            from notion_client import Client
            token = CredStore.load(cred_key).get("token","")
            n = Client(auth=token)
            n.pages.create(parent={"database_id":db_id},properties=props)
            return ToolResult(True,"✓ Notion DB entry added")
        except Exception as e:
            return ToolResult(False,f"✗ Notion DB failed: {e}")

class TwitterTool(ensure):
    name = "twitter"
    description = "Post tweets, read timeline, search tweets"

    def __init__(self):
        super().__init__()

    @staticmethod
    def tweet(text:str, cred_key:str="twitter") -> ToolResult:
        try:
            import tweepy
            c = CredStore.load(cred_key)
            client = tweepy.Client(
                consumer_key=c.get("api_key",""),
                consumer_secret=c.get("api_secret",""),
                access_token=c.get("access_token",""),
                access_token_secret=c.get("access_token_secret","")
            )
            r = client.create_tweet(text=text)
            return ToolResult(True,f"✓ Tweeted: {r.data['id']}")
        except Exception as e:
            return ToolResult(False,f"✗ Tweet failed: {e}")

class SystemTool(ensure):
    name = "system"
    description = "Run shell commands, manage processes, clipboard, screenshots, notifications"

    def __init__(self):
        super().__init__()

    @staticmethod
    def run_command(cmd:str, cwd:str=None, timeout:int=60) -> ToolResult:
        try:
            r = subprocess.run(cmd,shell=True,cwd=cwd,capture_output=True,
                               text=True,timeout=timeout)
            out = r.stdout+r.stderr
            return ToolResult(r.returncode==0, out.strip() or "✓ Done")
        except subprocess.TimeoutExpired:
            return ToolResult(False,"✗ Command timed out")
        except Exception as e:
            return ToolResult(False,f"✗ Command failed: {e}")

    @staticmethod
    def get_clipboard() -> ToolResult:
        try:
            import pyperclip
            return ToolResult(True,"✓ Clipboard read", pyperclip.paste())
        except Exception as e:
            return ToolResult(False,f"✗ Clipboard failed: {e}")

    @staticmethod
    def set_clipboard(text:str) -> ToolResult:
        try:
            import pyperclip; pyperclip.copy(text)
            return ToolResult(True,"✓ Copied to clipboard")
        except Exception as e:
            return ToolResult(False,f"✗ Clipboard set failed: {e}")

    @staticmethod
    def screenshot(out:str="screenshot.png") -> ToolResult:
        try:
            import pyautogui
            img = pyautogui.screenshot(); img.save(out)
            return ToolResult(True,f"✓ Screenshot saved: {out}")
        except Exception as e:
            return ToolResult(False,f"✗ Screenshot failed: {e}")

    @staticmethod
    def get_processes() -> ToolResult:
        try:
            import psutil
            procs = [{"pid":p.pid,"name":p.name(),"cpu":p.cpu_percent(),
                      "mem_mb":round(p.memory_info().rss/1024/1024,1)}
                     for p in psutil.process_iter(["pid","name","cpu_percent","memory_info"])]
            return ToolResult(True,f"✓ {len(procs)} processes", procs)
        except Exception as e:
            return ToolResult(False,f"✗ Process list failed: {e}")

    @staticmethod
    def notify(title:str, message:str) -> ToolResult:
        try:
            os_name = platform.system()
            if os_name=="Windows":
                from win10toast import ToastNotifier
                ToastNotifier().show_toast(title,message,duration=5)
            elif os_name=="Darwin":
                subprocess.run(["osascript","-e",f'display notification "{message}" with title "{title}"'])
            else:
                subprocess.run(["notify-send",title,message])
            return ToolResult(True,"✓ Notification sent")
        except Exception as e:
            return ToolResult(False,f"✗ Notify failed: {e}")

class ImageTool(ensure):
    name = "image"
    description = "Resize, convert, compress, watermark images; OCR text from images"

    def __init__(self):
        super().__init__()

    @staticmethod
    def resize(path:str, width:int, height:int, out:str=None) -> ToolResult:
        try:
            from PIL import Image
            img = Image.open(path)
            img = img.resize((width,height), Image.LANCZOS)
            dest = out or path
            img.save(dest)
            return ToolResult(True,f"✓ Resized to {width}×{height}: {dest}")
        except Exception as e:
            return ToolResult(False,f"✗ Resize failed: {e}")

    @staticmethod
    def convert(path:str, format:str, out:str=None) -> ToolResult:
        try:
            from PIL import Image
            img = Image.open(path)
            dest = out or str(Path(path).with_suffix(f".{format.lower()}"))
            img.save(dest,format.upper())
            return ToolResult(True,f"✓ Converted to {dest}")
        except Exception as e:
            return ToolResult(False,f"✗ Convert failed: {e}")

    @staticmethod
    def ocr(path:str) -> ToolResult:
        try:
            import pytesseract
            from PIL import Image
            text = pytesseract.image_to_string(Image.open(path))
            return ToolResult(True,f"✓ OCR extracted {len(text)} chars", text)
        except Exception as e:
            return ToolResult(False,f"✗ OCR failed: {e}")

    @staticmethod
    def bulk_compress(folder:str, quality:int=75) -> ToolResult:
        from PIL import Image
        count=0
        for ext in ("*.jpg","*.jpeg","*.png"):
            for fp in Path(folder).glob(ext):
                try:
                    img = Image.open(fp)
                    img.save(fp,optimize=True,quality=quality)
                    count+=1
                except: pass
        return ToolResult(True,f"✓ Compressed {count} images")

class SchedulerTool(ensure):
    name = "scheduler"
    description = "Schedule tasks to run at specific times or intervals"
    _jobs = {}

    def __init__(self):
        super().__init__()

    @staticmethod
    def schedule_task(task_id:str, cron_like:str, callback:Callable) -> ToolResult:
        """cron_like: 'every 5 minutes' | 'every day at 09:00' | 'every monday at 08:00'"""
        try:
            import schedule
            parts = cron_like.lower().split()
            if "minutes" in parts:
                n = int(parts[1]); schedule.every(n).minutes.do(callback)
            elif "hours" in parts:
                n = int(parts[1]); schedule.every(n).hours.do(callback)
            elif "day" in parts and "at" in parts:
                t = parts[parts.index("at")+1]
                schedule.every().day.at(t).do(callback)
            elif "monday" in parts:
                t = parts[-1]; schedule.every().monday.at(t).do(callback)
            SchedulerTool._jobs[task_id] = callback

            def _run():
                while task_id in SchedulerTool._jobs:
                    schedule.run_pending(); time.sleep(30)
            threading.Thread(target=_run,daemon=True).start()
            return ToolResult(True,f"✓ Scheduled task '{task_id}': {cron_like}")
        except Exception as e:
            return ToolResult(False,f"✗ Schedule failed: {e}")

    @staticmethod
    def cancel_task(task_id:str) -> ToolResult:
        SchedulerTool._jobs.pop(task_id,None)
        return ToolResult(True,f"✓ Cancelled '{task_id}'")

class JiraTool(ensure):
    name = "jira"
    description = "Create/update Jira issues, list sprints, manage projects"

    def __init__(self):
        super().__init__()

    @staticmethod
    def create_issue(project:str, summary:str, description:str="",
                     issue_type:str="Task", cred_key:str="jira") -> ToolResult:
        try:
            from jira import JIRA
            c = CredStore.load(cred_key)
            j = JIRA(server=c.get("server",""),
                     basic_auth=(c.get("email",""),c.get("api_token","")))
            issue = j.create_issue(project=project,summary=summary,
                                   description=description,issuetype={"name":issue_type})
            return ToolResult(True,f"✓ Jira issue {issue.key} created")
        except Exception as e:
            return ToolResult(False,f"✗ Jira failed: {e}")

class TelegramTool(ensure):
    name = "telegram"
    description = "Send Telegram messages via bot token"

    def __init__(self):
        super().__init__()

    @staticmethod
    def send(chat_id:str, text:str, cred_key:str="telegram") -> ToolResult:
        try:
            import requests
            token = CredStore.load(cred_key).get("bot_token","")
            if not token: return ToolResult(False,"No Telegram token.")
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            r = requests.post(url,json={"chat_id":chat_id,"text":text},timeout=10)
            return ToolResult(r.ok,f"✓ Telegram sent" if r.ok else f"✗ {r.text}")
        except Exception as e:
            return ToolResult(False,f"✗ Telegram failed: {e}")

class QRTool(ensure):
    name = "qr"
    description = "Generate QR codes from any text or URL"

    def __init__(self):
        super().__init__()

    @staticmethod
    def generate(data:str, out:str="qrcode.png", size:int=10) -> ToolResult:
        try:
            import qrcode
            img = qrcode.make(data,box_size=size)
            img.save(out)
            return ToolResult(True,f"✓ QR code saved: {out}")
        except Exception as e:
            return ToolResult(False,f"✗ QR failed: {e}")

class VoiceTool(ensure):
    name = "voice"
    description = "Text-to-speech output and speech-to-text input"

    def __init__(self):
        super().__init__()

    @staticmethod
    def speak(text:str) -> ToolResult:
        try:
            import pyttsx3
            e = pyttsx3.init(); e.say(text); e.runAndWait()
            return ToolResult(True,"✓ Spoken")
        except Exception as e:
            return ToolResult(False,f"✗ TTS failed: {e}")

    @staticmethod
    def listen(seconds:int=5) -> ToolResult:
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as src:
                audio = r.listen(src,timeout=seconds)
                text  = r.recognize_google(audio)
            return ToolResult(True,"✓ Heard speech", text)
        except Exception as e:
            return ToolResult(False,f"✗ Listen failed: {e}")

class WatcherTool(ensure):
    name = "watcher"
    description = "Watch folders for file changes and trigger actions"

    def __init__(self):
        super().__init__()

    @staticmethod
    def watch(folder:str, callback:Callable, patterns:list=None) -> ToolResult:
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            class Handler(FileSystemEventHandler):
                def on_created(self,event):
                    if not event.is_directory: callback(event.src_path)
                def on_modified(self,event):
                    if not event.is_directory: callback(event.src_path)
            obs = Observer()
            obs.schedule(Handler(),folder,recursive=True)
            obs.start()
            return ToolResult(True,f"✓ Watching {folder}")
        except Exception as e:
            return ToolResult(False,f"✗ Watch failed: {e}")

class RAGTool(ensure):
    name = "rag"
    description = "Query large documents using RAG pipeline via npmai Rag class"

    def __init__(self):
        super().__init__()

    @staticmethod
    def query_document(doc_path:str, question:str,
                       chunk_size:int=500) -> ToolResult:
        try:
            rag = Rag()
            text = Path(doc_path).read_text(errors="replace")
            if doc_path.endswith(".pdf"):
                from pypdf import PdfReader
                text = "\n".join(p.extract_text() or "" for p in PdfReader(doc_path).pages)
            rag.load_text(text, chunk_size=chunk_size)
            answer = rag.query(question)
            return ToolResult(True,"✓ RAG query answered", answer)
        except Exception as e:
            return ToolResult(False,f"✗ RAG query failed: {e}")

    @staticmethod
    def summarize_large_file(path:str, model:str="mistral:7b") -> ToolResult:
        try:
            if path.endswith(".pdf"):
                from pypdf import PdfReader
                text = "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
            else:
                text = Path(path).read_text(errors="replace")
            chunks = [text[i:i+3000] for i in range(0,len(text),3000)]
            llm = Ollama(model=model, temperature=0.2,
                         change=True, Models=["llama3.2:3b"])
            summaries = []
            for ch in chunks[:10]:
                s = llm.invoke(f"Summarize this section briefly:\n{ch}")
                summaries.append(s)
            combined = "\n".join(summaries)
            final = llm.invoke(f"Create a final comprehensive summary from these section summaries:\n{combined}")
            return ToolResult(True,"✓ Document summarized", final)
        except Exception as e:
            return ToolResult(False,f"✗ Summarize failed: {e}")

class SSHTool(ensure):
    name = "ssh"
    description = "Run commands on remote servers via SSH, transfer files via SFTP"

    def __init__(self):
        super().__init__()

    @staticmethod
    def run(host:str, command:str, cred_key:str="ssh") -> ToolResult:
        try:
            import paramiko
            c = CredStore.load(cred_key)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host,username=c.get("user",""),
                           password=c.get("password",""),
                           key_filename=c.get("key_path",None))
            _,stdout,stderr = client.exec_command(command)
            out = stdout.read().decode(); err = stderr.read().decode()
            client.close()
            return ToolResult(True,out or "✓ Done", out+err)
        except Exception as e:
            return ToolResult(False,f"✗ SSH failed: {e}")

    @staticmethod
    def upload(host:str, local:str, remote:str, cred_key:str="ssh") -> ToolResult:
        try:
            import paramiko
            c = CredStore.load(cred_key)
            t = paramiko.Transport((host,22))
            t.connect(username=c.get("user",""),password=c.get("password",""))
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(local,remote); sftp.close(); t.close()
            return ToolResult(True,f"✓ Uploaded {local} → {remote}")
        except Exception as e:
            return ToolResult(False,f"✗ SFTP upload failed: {e}")


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
                 status_cb:Callable=None):
        super().__init__()
        self._log      = log_cb      or print
        self._progress = progress_cb or (lambda v: None)
        self._status   = status_cb   or (lambda s: None)
        self.workspace = Workspace()
        self.executor  = Executor(log_cb=log_cb)
        self.planner   = Ollama(model="llama3.2:3b", temperature=0.2,
                                change=True, Models=["mistral:7b"])
        self.coder     = Ollama(model="codellama:7b-instruct", temperature=0.3,
                                change=True, Models=["deepseek-coder:6.7b"])
        self.auditor   = Ollama(model="qwen2.5-coder:7b", temperature=0.1,
                                change=True, Models=["falcon:7b-instruct"])
        self.verifier  = Ollama(model="llama3.2:3b", temperature=0.1,
                                change=True, Models=["mistral:7b"])
        self.chatter   = Ollama(model="granite3.3:2b", temperature=0.7,
                                change=True, Models=["llama3.2:1b"])
        self.mem_plan  = Memory("agent_plan")
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
