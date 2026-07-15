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
              ("pywin32",      "win32api") if platform.system()=="Windows" else ("",""),
              ]:
              if _p: _ensure(_p, _i)
        return "Done all requirements are ensured."

from npmai import Ollama, Memory, Rag
from langchain_core.output_parsers import StrOutputParser


class Executor(ensure):
    """Writes code to temp file, runs as child process, streams output."""
    from .Tools_Developer_CLI import GitTool, GitHubTool, GitLabTool, DockerTool, PackageManagerTool, VSCodeTool, TerminalTool, MakefileTool, CMakeTool, DebuggerTool
    from .Tools_business import StripeTool, RazorpayTool, ShopifyTool, InvoiceTool, AccountingTool, CRMTool, EmailMarketingTool, AnalyticsTool, InventoryTool, ContractTool
    from .Tools_cloud_devops import AWSS3Tool, AWSLambdaTool, AWSECSTool, CloudflareTool, VercelTool, NetlifyTool, RailwayTool, KubernetesTool, TerraformTool, MonitoringTool
    from .Tools_communication_extended import MicrosoftTeamsTool, ZoomTool, TwilioTool, SendGridTool, PushNotificationTool, RSSFeedTool, WebhookTool, CalendarTool, ChatOpsAutomationTool, SMTPAdvancedTool
    from .Tools_creative import FigmaTool, BlenderTool, SVGTool, CanvaTool, FontTool, ColorTool, IconTool, DiagramTool, PrintTool, ThreeDTool
    from .Tools_data_research import DataAnalysisTool, VisualizationTool, WebScrapingAdvancedTool, SearchResearchTool, FinancialDataTool, SocialMediaDataTool, WeatherGeoTool, TextAnalyticsTool, DatabaseTool, ReportGeneratorTool
    from .Tools_media import FFmpegTool, YouTubeDownloaderTool, AudioTool, ImageAdvancedTool, ScreenRecorderTool, TextToSpeechTool, VideoEditingTool, PodcastTool, StreamingTool, MediaMetadataTool
    from .Tools_productivity import GoogleWorkspaceTool, NotionAdvancedTool, LinearTool, AsanaTool, TrelloTool, ClickUpTool, TodoistTool, ObsidianTool, BookmarkManagerTool, TimeTrackingTool
    from .Tools_security_ai import SecurityScannerTool, CryptographyTool, PenetrationTestingTool, AIImageGenerationTool, AITextGenerationAdvancedTool, MLModelTool, SpeechAITool, ComputerVisionTool, AutomationWorkflowTool, KnowledgeBaseTool
    from .Tools_system_hardware import SystemAdvancedTool, NetworkAdvancedTool, FileSystemAdvancedTool, ProcessAutomationTool, PrinterTool, ClipboardAdvancedTool, HardwareMonitorTool, RaspberryPiTool, MQTTIoTTool, VirtualizationTool

    def __init__(self, log_cb:Callable=None, timeout:int=120):
        super().__init__()
        self._log     = log_cb or print
        self._timeout = timeout
        self._proc    = None
        self._killed  = False

    def run(self, code:str) -> tuple:
        """Returns (success:bool, full_output:str)"""
        self._killed = False
        self.current_package_dir = os.path.dirname(os.path.abspath(__file__))
        tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False,
                                         mode="w", encoding="utf-8", dir=self.current_package_dir)
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
