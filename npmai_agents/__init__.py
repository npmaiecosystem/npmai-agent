__version__ = "1.0.2"

from .npmai_agents import AgentBrain
from .core import (
    LLMBackend, Ollama_Local, OpenAIBackend, AnthropicBackend, GeminiBackend,
    GroqBackend, MistralBackend, CohereBackend, AzureOpenAIBackend,
    BedrockBackend, HuggingFaceBackend, LlamaCppBackend,
    CredStore, Workspace, ToolResult,
)
from .agent_core import Executor
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
