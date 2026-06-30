"""
tools_productivity.py — Productivity Tools for NPM Agent (NPMAI ECOSYSTEM)
Author: Sonu Kumar / NPMAI ECOSYSTEM
Tools: GoogleWorkspace, NotionAdvanced, Linear, Asana, Trello, ClickUp,
       Todoist, Obsidian, BookmarkManager, TimeTracking
"""

import os, sys, json, re, csv, time, sqlite3, subprocess, tempfile, traceback
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Optional, Any

# ── auto-install helpers ──────────────────────────────────────────────────────
def _ensure(pkg: str, import_name: str = None):
    n = import_name or pkg
    try:
        __import__(n)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"],
                       check=False)

for _pkg, _imp in [
    ("google-api-python-client", "googleapiclient"),
    ("google-auth-httplib2",     "google_auth_httplib2"),
    ("google-auth-oauthlib",     "google_auth_oauthlib"),
    ("google-auth",              "google.oauth2"),
    ("notion-client",            "notion_client"),
    ("requests",                 "requests"),
    ("asana",                    "asana"),
    ("todoist-api-python",       "todoist_api_python"),
    ("python-frontmatter",       "frontmatter"),
    ("beautifulsoup4",           "bs4"),
    ("playwright",               "playwright"),
    ("cryptography",             "cryptography"),
]:
    _ensure(_pkg, _imp)

from core import ToolResult, CredStore

# ═════════════════════════════════════════════════════════════════════════════
# 1. GoogleWorkspaceTool
# ═════════════════════════════════════════════════════════════════════════════

class GoogleWorkspaceTool:
    name = "google_workspace"
    description = (
        "Google Docs, Sheets, Drive, and Forms — create, read, write, "
        "share, export, upload, download, and manage files"
    )
    use = ("""
Name of Tool:- GoogleWorkspaceTool

Purpose of Tool:-
The GoogleWorkspaceTool provides a unified interface for programmatic interaction with core Google Workspace 
applications, including Google Docs, Sheets, Drive, and Forms. Utilizing service account credentials managed through a 
central store, it handles multi-scope OAuth2 authentication. The tool abstracts the complexity of separate Google API 
discovery clients into a single utility, enabling automated workflows for generating and editing text documents, reading 
and updating spreadsheets, adding data formatting or visual charts, managing cloud storage architectures (uploading, 
downloading, moving, and sharing assets), and constructing responsive online forms alongside retrieving user responses.

Methods:-
- docs_create: Instantiates a new cloud text document and initializes its primary contents.
- docs_get: Retrieves structural document maps and extracts an unformatted, plain text stream.
- docs_append: Evaluates the structural end index of a target document to append fresh string content.
- docs_replace_text: Performs optimized global find-and-replace text modifications across document structures.
- docs_export: Leverages Google Drive endpoint translations to stream and convert documents into localized file formats (e.g., PDF, DOCX).
- sheets_create: Initializes a multi-sheet spreadsheet workbook complete with explicit naming array declarations.
- sheets_read: Polls a defined spreadsheet string grid cell range to capture row values.
- sheets_write: Overwrites an target spreadsheet block matrix array using custom ingestion policies.
- sheets_append: Identifies the tail edge of a spreadsheet log array to append tracking metrics.
- sheets_format_cells: Injects structural design modifications into grid parameters.
- sheets_add_chart: Binds embedded visualization configurations to data range sources.
- drive_upload: Packages local files into chunked upload media requests to store them in Drive locations.
- drive_download: Streams binary file streams sequentially out of Drive cloud nodes into local destination layouts.
- drive_list: Queries storage indexes using parameter conditions to compile file asset metadata reports.
- drive_create_folder: Constructs structural collection nodes within a target folder layout.
- drive_share: Allocates identity access permissions over files to target emails with defined user roles.
- drive_move: Modifies parent structural mapping lists to change an item's file hierarchy location.
- forms_create: Generates interactive questionnaire matrices with various question styles (e.g., Radio, Checkbox, Scale).
- forms_get_responses: Downloads active submission histories recorded from user form entries.
- forms_list: Scans file metadata registries specifically filtering for active form assets.

How to use Tool Methods:-

1. docs_create:
   - Purpose: Creates a new document and inserts optional initial text contents.
   - Arguments:
     a) title: str - The visual filename title assigned to the document (required).
     b) content: str - Text payload string to insert at the first index (required).
     c) cred_key: str (default: "google") - Reference key for looking up service credentials.
   - Returns: ToolResult containing the generated unique "documentId".
   - How to call: GoogleWorkspaceTool.docs_create(title="Project Scope", content="Initial draft body...")

2. docs_get:
   - Purpose: Pulls down full document objects and isolates clean plain-text strings.
   - Arguments:
     a) doc_id: str - Target document identifier code string (required).
     b) cred_key: str (default: "google") - Storage key locator for API authentication.
   - Returns: ToolResult storing full schema maps alongside stripped "plain_text" values.
   - How to call: GoogleWorkspaceTool.docs_get(doc_id="1xA2bC3d...")

3. docs_append:
   - Purpose: Automatically finds the end boundary index of a document to attach new paragraphs.
   - Arguments:
     a) doc_id: str - Target document asset identifier code (required).
     b) content: str - String segment containing the text block additions (required).
     c) cred_key: str (default: "google") - Active service credential key name.
   - Returns: ToolResult reporting total characters successfully appended.
   - How to call: GoogleWorkspaceTool.docs_append(doc_id="1xA2bC3d...", content="\nUpdate: Section approved.")

4. docs_replace_text:
   - Purpose: Batch modifies text phrases throughout a document based on an input key-value dictionary.
   - Arguments:
     a) doc_id: str - Target document asset identifier (required).
     b) replacements: dict - Mapping dictionary of {"old text string": "new text string"} (required).
     c) cred_key: str (default: "google") - Reference key for lookup service account credentials.
   - Returns: ToolResult capturing API confirmation properties.
   - How to call: GoogleWorkspaceTool.docs_replace_text(doc_id="1xA2bC3d...", replacements={"[COMPANY]": "Acme Corp"})

5. docs_export:
   - Purpose: Converts Google Workspace document structures into downloadable desktop formats.
   - Arguments:
     a) doc_id: str - Target source cloud document id (required).
     b) format: str (default: "pdf") - Choice format export target type ("pdf", "docx", "txt", "html", "odt").
     c) output: str (default: "document.pdf") - Target local path where export bytes are saved.
     b) cred_key: str (default: "google") - Reference key for credentials lookup.
   - Returns: ToolResult confirming binary stream output path.
   - How to call: GoogleWorkspaceTool.docs_export(doc_id="1xA2bC3d...", format="docx", output="./downloads/final.docx")

6. sheets_create:
   - Purpose: Initializes empty spreadsheet container layouts with defined sheet names.
   - Arguments:
     a) title: str - Workbook title name identifier (required).
     b) sheets: list (default: None) - Array listing sub-tab names, e.g., ["Q1_Sales", "Q2_Sales"].
     c) cred_key: str (default: "google") - Associated credential lookup key.
   - Returns: ToolResult tracking "spreadsheetId" and access URL links.
   - How to call: GoogleWorkspaceTool.sheets_create(title="2026 Financials", sheets=["Revenue", "Expenses"])

7. sheets_read:
   - Purpose: Extracts row lists out of spreadsheets according to sheet names and block range indicators.
   - Arguments:
     a) spreadsheet_id: str - Target document workspace container id (required).
     b) range_: str (default: "Sheet1") - Target section layout coordinates (e.g., "Sheet1!A1:D20").
     c) cred_key: str (default: "google") - Service account store index key.
   - Returns: ToolResult enclosing row arrays.
   - How to call: GoogleWorkspaceTool.sheets_read(spreadsheet_id="1sH2eEt...", range_="Revenue!B2:C10")

8. sheets_write:
   - Purpose: Performs specific value matrix block overwrites starting at a given grid cell coordinate.
   - Arguments:
     a) spreadsheet_id: str - Target spreadsheet workspace identifier (required).
     b) range_: str - Cell coordinate target boundary start anchor (e.g., "Sheet1!A1") (required).
     c) values: list - Matrix list array outlining column block rows (required).
     d) value_input_option: str (default: "RAW") - Formatting parser standard ("RAW" or "USER_ENTERED").
     e) cred_key: str (default: "google") - Associated verification access identifier.
   - Returns: ToolResult confirming cell update lengths.
   - How to call: GoogleWorkspaceTool.sheets_write(spreadsheet_id="1sH2eEt...", range_="Sheet1!A1", values=[["Name", "Age"], ["Alice", 24]])

9. sheets_append:
   - Purpose: appends tracking metrics immediately below the last populated row in a table.
   - Arguments:
     a) spreadsheet_id: str - Target spreadsheet workspace container id (required).
     b) range_: str - Search table region filter anchor used to isolate targeted table lists (required).
     c) values: list - Dynamic row array listings to insert at the table bottom (required).
     d) cred_key: str (default: "google") - Active profile identity credential key.
   - Returns: ToolResult logging processed line changes.
   - How to call: GoogleWorkspaceTool.sheets_append(spreadsheet_id="1sH2eEt...", range_="Sheet1!A:B", values=[["Bob", 30]])

10. sheets_format_cells:
    - Purpose: Applies presentation formatting values across workbook coordinates.
    - Arguments:
      a) spreadsheet_id: str - Target workspace cloud workbook layout ID (required).
      b) range_: str - Coordinate region reference track block labels (required).
      c) format: dict - Configuration mapping parameters matching Sheets API CellFormat specifications (required).
      d) cred_key: str (default: "google") - Workspace context authorization profile lookup tag.
    - Returns: ToolResult tracking successful presentation styling updates.
    - How to call: GoogleWorkspaceTool.sheets_format_cells(spreadsheet_id="1sH2eEt...", range_="A1:A10", format={"textFormat": {"bold": True}})

11. sheets_add_chart:
    - Purpose: Attaches charts onto spreadsheet grid layers based on custom chart data source mappings.
    - Arguments:
      a) spreadsheet_id: str - Target workbook cloud reference workspace layout (required).
      b) sheet_id: int - Integer identifier targeting the specific sheet sub-tab (required).
      b) chart_config: dict - Configuration dictionary matching Sheets API AddChartRequest structures (required).
      c) cred_key: str (default: "google") - Active service context profile lookup token.
    - Returns: ToolResult confirming chart injection.
    - How to call: GoogleWorkspaceTool.sheets_add_chart(spreadsheet_id="1sH2eEt...", sheet_id=0, chart_config={...})

12. drive_upload:
    - Purpose: Streams local physical file buffers into managed Drive storage spaces.
    - Arguments:
      a) local_path: str - Target local computer file layout path (required).
      b) folder_id: str (default: None) - Optional cloud destination folder parent container code.
      c) mime_type: str (default: None) - Data content classification wrapper tag.
      d) cred_key: str (default: "google") - Storage credentials profile key.
    - Returns: ToolResult containing file reference data objects including cloud links.
    - How to call: GoogleWorkspaceTool.drive_upload(local_path="./reports/summary.csv", folder_id="fol_98765")

13. drive_download:
    - Purpose: Downloads binary files from the cloud into a specified local file path.
    - Arguments:
      a) file_id: str - Unique target cloud file reference node identifier (required).
      b) output_path: str - Target local disk pathway location mapping destination (required).
      c) cred_key: str (default: "google") - Storage lookup credential access identifier.
    - Returns: ToolResult documenting file receipt verification tracking metrics.
    - How to call: GoogleWorkspaceTool.drive_download(file_id="drv_fl123...", output_path="./local_mirror.zip")

14. drive_list:
    - Purpose: Queries Drive file metadata registries using search filters and ordering fields.
    - Arguments:
      a) folder_id: str (default: None) - Targets searches exclusively within a specific parent node folder.
      b) query: str (default: None) - Search query statement criteria matching Drive API formats (e.g., "name contains 'Invoice'").
      c) order_by: str (default: "name") - Sorting criteria key instruction ("name", "modifiedTime", etc.).
      d) cred_key: str (default: "google") - Account credentials lookup index name pointer.
    - Returns: ToolResult wrapping file lists with names, sizes, modtimes, and links.
    - How to call: GoogleWorkspaceTool.drive_list(query="mimeType='application/pdf'", order_by="modifiedTime desc")

15. drive_create_folder:
    - Purpose: Sets up specialized collection nodes within Drive filesystem hierarchies.
    - Arguments:
      a) name: str - Target foldernaming label string (required).
      b) parent_id: str (default: None) - Optional parent identifier string to build nested architectures.
      c) cred_key: str (default: "google") - Target credentials access map identifier pointer.
    - Returns: ToolResult tracking the created folder instance configuration objects.
    - How to call: GoogleWorkspaceTool.drive_create_folder(name="Archive_2026", parent_id="fol_root55")

16. drive_share:
    - Purpose: Assigns user collaboration roles over designated cloud files.
    - Arguments:
      a) file_id: str - Target file unique asset identifier code (required).
      b) email: str - User target contact email address (required).
      c) role: str (default: "reader") - Authorized permission standard ("reader", "writer", "commenter", "owner").
      d) cred_key: str (default: "google") - Service context profile lookup credential token.
    - Returns: ToolResult monitoring target credential validation maps.
    - How to call: GoogleWorkspaceTool.drive_share(file_id="drv_fl123...", email="partner@example.com", role="writer")

17. drive_move:
    - Purpose: Changes folder parent tracking variables to move files between directories.
    - Arguments:
      a) file_id: str - Target file unique asset identifier code string (required).
      b) new_parent_id: str - Target folder destination container identifier layout reference (required).
      c) cred_key: str (default: "google") - Target credential reference verification key.
    - Returns: ToolResult confirming parent node updates.
    - How to call: GoogleWorkspaceTool.drive_move(file_id="drv_fl123...", new_parent_id="fol_processed77")

18. forms_create:
    - Purpose: Constructs a new Form layout filled with diverse structural item questions.
    - Arguments:
      a) title: str - Questionnaire visual heading label (required).
      b) items: list - Collection map dictionaries configuring text fields, multiple-choice options, or checkboxes (required).
      c) cred_key: str (default: "google") - Associated authorization profile lookup parameter tag.
    - Returns: ToolResult including "formId" along with public user-facing "responderUri" URLs.
    - How to call: GoogleWorkspaceTool.forms_create(title="Feedback Survey", items=[{"title": "Full Name", "type": "TEXT"}, {"title": "Rating", "type": "SCALE"}])

19. forms_get_responses:
    - Purpose: Retrieves active submission records collected from user form entries.
    - Arguments:
      a) form_id: str - Target questionnaire structural container code key (required).
      b) cred_key: str (default: "google") - System profile lookup reference credentials validation block.
    - Returns: ToolResult bundling all response data tracking logs.
    - How to call: GoogleWorkspaceTool.forms_get_responses(form_id="frm_abc123...")

20. forms_list:
    - Purpose: Queries localized storage layouts to discover and report active Form file components.
    - Arguments:
      a) cred_key: str (default: "google") - Active credentials profile system access code lookup.
    - Returns: ToolResult listing metadata summaries for discovered forms.
    - How to call: GoogleWorkspaceTool.forms_list()
""")
       
    # ── internal helpers ──────────────────────────────────────────────────

    @staticmethod
    def _creds(cred_key: str = "google"):
        """Return google.oauth2 Credentials from stored service-account JSON."""
        from google.oauth2.service_account import Credentials
        data = CredStore.load(cred_key)
        if not data:
            raise ValueError("No Google credentials. Store service-account JSON under 'google'.")
        scopes = [
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/forms",
        ]
        return Credentials.from_service_account_info(data, scopes=scopes)

    @staticmethod
    def _docs_service(cred_key: str = "google"):
        from googleapiclient.discovery import build
        return build("docs", "v1", credentials=GoogleWorkspaceTool._creds(cred_key))

    @staticmethod
    def _sheets_service(cred_key: str = "google"):
        from googleapiclient.discovery import build
        return build("sheets", "v4", credentials=GoogleWorkspaceTool._creds(cred_key))

    @staticmethod
    def _drive_service(cred_key: str = "google"):
        from googleapiclient.discovery import build
        return build("drive", "v3", credentials=GoogleWorkspaceTool._creds(cred_key))

    @staticmethod
    def _forms_service(cred_key: str = "google"):
        from googleapiclient.discovery import build
        return build("forms", "v1", credentials=GoogleWorkspaceTool._creds(cred_key))

    # ── Docs ─────────────────────────────────────────────────────────────

    @staticmethod
    def docs_create(title: str, content: str, cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._docs_service(cred_key)
            doc = svc.documents().create(body={"title": title}).execute()
            doc_id = doc["documentId"]
            if content:
                requests_ = [{"insertText": {"location": {"index": 1}, "text": content}}]
                svc.documents().batchUpdate(documentId=doc_id,
                                            body={"requests": requests_}).execute()
            return ToolResult(True, f"✓ Doc created: {doc_id}",
                              {"documentId": doc_id, "title": title})
        except Exception as e:
            return ToolResult(False, f"✗ docs_create failed: {e}")

    @staticmethod
    def docs_get(doc_id: str, cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._docs_service(cred_key)
            doc = svc.documents().get(documentId=doc_id).execute()
            # extract plain text
            text_parts = []
            for el in doc.get("body", {}).get("content", []):
                for run in el.get("paragraph", {}).get("elements", []):
                    t = run.get("textRun", {}).get("content", "")
                    if t:
                        text_parts.append(t)
            plain = "".join(text_parts)
            return ToolResult(True, f"✓ Doc fetched ({len(plain)} chars)",
                              {"doc": doc, "plain_text": plain})
        except Exception as e:
            return ToolResult(False, f"✗ docs_get failed: {e}")

    @staticmethod
    def docs_append(doc_id: str, content: str, cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._docs_service(cred_key)
            doc = svc.documents().get(documentId=doc_id).execute()
            end_index = doc["body"]["content"][-1]["endIndex"] - 1
            requests_ = [{"insertText": {"location": {"index": end_index}, "text": content}}]
            svc.documents().batchUpdate(documentId=doc_id,
                                        body={"requests": requests_}).execute()
            return ToolResult(True, f"✓ Appended {len(content)} chars to {doc_id}")
        except Exception as e:
            return ToolResult(False, f"✗ docs_append failed: {e}")

    @staticmethod
    def docs_replace_text(doc_id: str, replacements: dict,
                          cred_key: str = "google") -> ToolResult:
        """replacements: {old_text: new_text, ...}"""
        try:
            svc = GoogleWorkspaceTool._docs_service(cred_key)
            requests_ = [
                {"replaceAllText": {
                    "containsText": {"text": old, "matchCase": True},
                    "replaceText": new
                }}
                for old, new in replacements.items()
            ]
            result = svc.documents().batchUpdate(documentId=doc_id,
                                                  body={"requests": requests_}).execute()
            return ToolResult(True, f"✓ Replaced {len(replacements)} text(s)", result)
        except Exception as e:
            return ToolResult(False, f"✗ docs_replace_text failed: {e}")

    @staticmethod
    def docs_export(doc_id: str, format: str = "pdf",
                    output: str = "document.pdf", cred_key: str = "google") -> ToolResult:
        """format: pdf | docx | txt | html | odt"""
        try:
            mime_map = {
                "pdf":  "application/pdf",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "txt":  "text/plain",
                "html": "text/html",
                "odt":  "application/vnd.oasis.opendocument.text",
            }
            mime = mime_map.get(format.lower(), "application/pdf")
            svc = GoogleWorkspaceTool._drive_service(cred_key)
            content_bytes = svc.files().export_media(fileId=doc_id,
                                                      mimeType=mime).execute()
            Path(output).write_bytes(content_bytes)
            return ToolResult(True, f"✓ Exported to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ docs_export failed: {e}")

    # ── Sheets ────────────────────────────────────────────────────────────

    @staticmethod
    def sheets_create(title: str, sheets: list = None,
                      cred_key: str = "google") -> ToolResult:
        """sheets: list of sheet names, e.g. ['Sheet1','Data']"""
        try:
            svc = GoogleWorkspaceTool._sheets_service(cred_key)
            body = {"properties": {"title": title}}
            if sheets:
                body["sheets"] = [{"properties": {"title": s}} for s in sheets]
            ss = svc.spreadsheets().create(body=body).execute()
            return ToolResult(True, f"✓ Spreadsheet created: {ss['spreadsheetId']}",
                              {"spreadsheetId": ss["spreadsheetId"],
                               "url": ss["spreadsheetUrl"]})
        except Exception as e:
            return ToolResult(False, f"✗ sheets_create failed: {e}")

    @staticmethod
    def sheets_read(spreadsheet_id: str, range_: str = "Sheet1",
                    cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._sheets_service(cred_key)
            resp = svc.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_).execute()
            values = resp.get("values", [])
            return ToolResult(True, f"✓ Read {len(values)} rows", values)
        except Exception as e:
            return ToolResult(False, f"✗ sheets_read failed: {e}")

    @staticmethod
    def sheets_write(spreadsheet_id: str, range_: str,
                     values: list, value_input_option: str = "RAW",
                     cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._sheets_service(cred_key)
            body = {"values": values}
            resp = svc.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range=range_,
                valueInputOption=value_input_option, body=body).execute()
            return ToolResult(True, f"✓ Written {resp.get('updatedCells',0)} cells")
        except Exception as e:
            return ToolResult(False, f"✗ sheets_write failed: {e}")

    @staticmethod
    def sheets_append(spreadsheet_id: str, range_: str, values: list,
                      cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._sheets_service(cred_key)
            body = {"values": values}
            resp = svc.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id, range=range_,
                valueInputOption="RAW", insertDataOption="INSERT_ROWS",
                body=body).execute()
            return ToolResult(True, f"✓ Appended rows",
                              resp.get("updates", {}))
        except Exception as e:
            return ToolResult(False, f"✗ sheets_append failed: {e}")

    @staticmethod
    def sheets_clear(spreadsheet_id: str, range_: str,
                     cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._sheets_service(cred_key)
            svc.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id, range=range_, body={}).execute()
            return ToolResult(True, f"✓ Cleared {range_}")
        except Exception as e:
            return ToolResult(False, f"✗ sheets_clear failed: {e}")

    @staticmethod
    def sheets_format_cells(spreadsheet_id: str, range_: str,
                            format: dict, cred_key: str = "google") -> ToolResult:
        """format: CellFormat dict e.g. {'backgroundColor': {'red':1,'green':0,'blue':0}}"""
        try:
            svc = GoogleWorkspaceTool._sheets_service(cred_key)
            # Parse range to get sheet id
            meta = svc.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheet_id = meta["sheets"][0]["properties"]["sheetId"]
            requests_ = [{
                "repeatCell": {
                    "range": {"sheetId": sheet_id},
                    "cell": {"userEnteredFormat": format},
                    "fields": "userEnteredFormat"
                }
            }]
            svc.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                           body={"requests": requests_}).execute()
            return ToolResult(True, f"✓ Format applied to {range_}")
        except Exception as e:
            return ToolResult(False, f"✗ sheets_format_cells failed: {e}")

    @staticmethod
    def sheets_add_chart(spreadsheet_id: str, sheet_id: int,
                         chart_config: dict, cred_key: str = "google") -> ToolResult:
        """chart_config: AddChartRequest spec dict from Sheets API"""
        try:
            svc = GoogleWorkspaceTool._sheets_service(cred_key)
            requests_ = [{"addChart": {"chart": chart_config}}]
            resp = svc.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": requests_}).execute()
            return ToolResult(True, "✓ Chart added", resp)
        except Exception as e:
            return ToolResult(False, f"✗ sheets_add_chart failed: {e}")

    # ── Drive ─────────────────────────────────────────────────────────────

    @staticmethod
    def drive_upload(local_path: str, folder_id: str = None,
                     mime_type: str = None, cred_key: str = "google") -> ToolResult:
        try:
            from googleapiclient.http import MediaFileUpload
            svc = GoogleWorkspaceTool._drive_service(cred_key)
            name = Path(local_path).name
            meta = {"name": name}
            if folder_id:
                meta["parents"] = [folder_id]
            media = MediaFileUpload(local_path, mimetype=mime_type,
                                    resumable=True)
            f = svc.files().create(body=meta, media_body=media,
                                   fields="id,name,webViewLink").execute()
            return ToolResult(True, f"✓ Uploaded {name}", f)
        except Exception as e:
            return ToolResult(False, f"✗ drive_upload failed: {e}")

    @staticmethod
    def drive_download(file_id: str, output_path: str,
                       cred_key: str = "google") -> ToolResult:
        try:
            import io
            from googleapiclient.http import MediaIoBaseDownload
            svc = GoogleWorkspaceTool._drive_service(cred_key)
            request = svc.files().get_media(fileId=file_id)
            buf = io.BytesIO()
            dl = MediaIoBaseDownload(buf, request)
            done = False
            while not done:
                _, done = dl.next_chunk()
            Path(output_path).write_bytes(buf.getvalue())
            return ToolResult(True, f"✓ Downloaded to {output_path}")
        except Exception as e:
            return ToolResult(False, f"✗ drive_download failed: {e}")

    @staticmethod
    def drive_list(folder_id: str = None, query: str = None,
                   order_by: str = "name", cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._drive_service(cred_key)
            q_parts = []
            if folder_id:
                q_parts.append(f"'{folder_id}' in parents")
            if query:
                q_parts.append(query)
            q_parts.append("trashed=false")
            q_str = " and ".join(q_parts)
            results = svc.files().list(
                q=q_str, orderBy=order_by,
                fields="files(id,name,mimeType,size,modifiedTime,webViewLink)"
            ).execute()
            files = results.get("files", [])
            return ToolResult(True, f"✓ {len(files)} files", files)
        except Exception as e:
            return ToolResult(False, f"✗ drive_list failed: {e}")

    @staticmethod
    def drive_create_folder(name: str, parent_id: str = None,
                            cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._drive_service(cred_key)
            meta = {"name": name,
                    "mimeType": "application/vnd.google-apps.folder"}
            if parent_id:
                meta["parents"] = [parent_id]
            folder = svc.files().create(body=meta,
                                        fields="id,name").execute()
            return ToolResult(True, f"✓ Folder created: {folder['id']}", folder)
        except Exception as e:
            return ToolResult(False, f"✗ drive_create_folder failed: {e}")

    @staticmethod
    def drive_share(file_id: str, email: str, role: str = "reader",
                    cred_key: str = "google") -> ToolResult:
        """role: reader | writer | commenter | owner"""
        try:
            svc = GoogleWorkspaceTool._drive_service(cred_key)
            perm = {"type": "user", "role": role, "emailAddress": email}
            resp = svc.permissions().create(fileId=file_id, body=perm,
                                            sendNotificationEmail=True).execute()
            return ToolResult(True, f"✓ Shared {file_id} with {email} as {role}", resp)
        except Exception as e:
            return ToolResult(False, f"✗ drive_share failed: {e}")

    @staticmethod
    def drive_move(file_id: str, new_parent_id: str,
                   cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._drive_service(cred_key)
            f = svc.files().get(fileId=file_id, fields="parents").execute()
            old_parents = ",".join(f.get("parents", []))
            svc.files().update(fileId=file_id,
                               addParents=new_parent_id,
                               removeParents=old_parents,
                               fields="id,parents").execute()
            return ToolResult(True, f"✓ Moved {file_id} to {new_parent_id}")
        except Exception as e:
            return ToolResult(False, f"✗ drive_move failed: {e}")

    # ── Forms ─────────────────────────────────────────────────────────────

    @staticmethod
    def forms_create(title: str, items: list,
                     cred_key: str = "google") -> ToolResult:
        """
        items: list of dicts, e.g.
          [{"title": "Name?", "type": "TEXT"},
           {"title": "Age?",  "type": "TEXT"},
           {"title": "Color?","type":"RADIO","options":["Red","Blue"]}]
        """
        try:
            svc = GoogleWorkspaceTool._forms_service(cred_key)
            form = svc.forms().create(
                body={"info": {"title": title, "documentTitle": title}}
            ).execute()
            form_id = form["formId"]
            requests_ = []
            for idx, item in enumerate(items):
                q_type = item.get("type", "TEXT").upper()
                question: dict = {}
                if q_type == "TEXT":
                    question = {"textQuestion": {"paragraph": False}}
                elif q_type == "RADIO":
                    opts = [{"value": o} for o in item.get("options", [])]
                    question = {"choiceQuestion": {"type": "RADIO",
                                                   "options": opts}}
                elif q_type == "CHECKBOX":
                    opts = [{"value": o} for o in item.get("options", [])]
                    question = {"choiceQuestion": {"type": "CHECKBOX",
                                                   "options": opts}}
                elif q_type == "SCALE":
                    question = {"scaleQuestion": {"low": 1, "high": 5}}
                requests_.append({
                    "createItem": {
                        "item": {
                            "title": item.get("title", f"Question {idx+1}"),
                            "questionItem": {"question": question}
                        },
                        "location": {"index": idx}
                    }
                })
            if requests_:
                svc.forms().batchUpdate(formId=form_id,
                                        body={"requests": requests_}).execute()
            return ToolResult(True, f"✓ Form created: {form_id}",
                              {"formId": form_id,
                               "responderUri": form.get("responderUri", "")})
        except Exception as e:
            return ToolResult(False, f"✗ forms_create failed: {e}")

    @staticmethod
    def forms_get_responses(form_id: str,
                            cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._forms_service(cred_key)
            resp = svc.forms().responses().list(formId=form_id).execute()
            responses = resp.get("responses", [])
            return ToolResult(True, f"✓ {len(responses)} responses", responses)
        except Exception as e:
            return ToolResult(False, f"✗ forms_get_responses failed: {e}")

    @staticmethod
    def forms_list(cred_key: str = "google") -> ToolResult:
        try:
            svc = GoogleWorkspaceTool._drive_service(cred_key)
            results = svc.files().list(
                q="mimeType='application/vnd.google-apps.form' and trashed=false",
                fields="files(id,name,modifiedTime,webViewLink)"
            ).execute()
            forms = results.get("files", [])
            return ToolResult(True, f"✓ {len(forms)} forms", forms)
        except Exception as e:
            return ToolResult(False, f"✗ forms_list failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 2. NotionAdvancedTool
# ═════════════════════════════════════════════════════════════════════════════

class NotionAdvancedTool:
    name = "notion_advanced"
    description = (
        "Advanced Notion operations — databases, pages, blocks, tables, "
        "kanban views, CSV import/export, templates, and page duplication"
    )
    use = ("""
Name of Tool: NotionAdvancedTool

Purpose of Tool:
The NotionAdvancedTool acts as an advanced wrapper around the official Notion API client (`notion_client`). 
It streamlines programmatic workflows for workspace administration by abstracting raw HTTP/SDK patterns into 
clean, reusable static methods. This tool handles database design and operations (querying, adding items, tracking property 
updates, and bulk archiving), layout rendering (pages and block elements), custom data structure formatting (native 
tables and Kanban pipelines), bulk data management (CSV import/export mechanisms), and content orchestration 
(template building and structural page duplication).

Methods:
- search: Queries workspace objects matching specific text parameters and sort orders.
- get_database: Pulls the structural schema mapping for a target database ID.
- query_database: Polls database entries based on pagination criteria, filters, and sorting parameters.
- create_database: Constructs a structured database matching defined custom schema types.
- add_database_item: Injects a new workspace row entry filled with mapped properties.
- update_database_item: Overwrites specific property values on an existing database item page.
- delete_database_item: Sets the page archive state flag to drop items from active workspace views.
- create_page: Generates a blank canvas or standard layout page context populated with block children arrays.
- get_page: Pulls structural properties and system metadata fields from a designated page node.
- update_page: Alters page header titles and general system properties.
- append_blocks: Chains structural content components to the bottom of a block layout.
- get_blocks: Iterates over layout child elements to return structured content streams.
- delete_block: Targets and deletes a content component by ID.
- create_table: Transforms basic string vectors into formatted child row matrix block layouts.
- create_kanban_view: Injects task pipeline choices ("Todo", "In Progress", "Done") into database schemas.
- export_database_to_csv: Processes pagination streams to serialize database values into flat CSV sheets.
- import_csv_to_database: Maps dynamic CSV input streams into standardized rich-text database properties.
- create_template: Packages custom headers, emoji icons, structural covers, and boilerplate blocks into template layouts.
- duplicate_page: Deep-copies page states and block children arrays while pruning read-only metadata fields.

How to use Tool Methods:

1. search:
   - Purpose: Searches for matching page or database items across the user's workspace.
   - Arguments:
     a) query: str - Text search term query string (required).
     b) filter_type: str (default: None) - Scopes objects by type ("page" or "database").
     c) sort: str (default: "last_edited_time") - Target timestamp mapping anchor.
     d) cred_key: str (default: "notion") - Vault key location for authentication.
   - Returns: ToolResult containing matching search result payload lists.
   - How to call: NotionAdvancedTool.search(query="2026 Roadmap", filter_type="database")

2. get_database:
   - Purpose: Pulls the data structure and schema metadata of a database.
   - Arguments:
     a) database_id: str - target database identifier code string (required).
     b) cred_key: str (default: "notion") - Vault authentication lookup index.
   - Returns: ToolResult tracking full schema definitions.
   - How to call: NotionAdvancedTool.get_database(database_id="db_abc123...")

3. query_database:
   - Purpose: Searches and filters records within a specific database.
   - Arguments:
     a) database_id: str - target database workspace container ID (required).
     b) filter: dict (default: None) - Structured payload matching Notion API compound filter styles.
     c) sorts: list (default: None) - Sorting parameter maps.
     d) page_size: int (default: 100) - Caps maximum returned records.
     e) cred_key: str (default: "notion") - Active workspace authorization token tag.
   - Returns: ToolResult holding rows extracted from the query.
   - How to call: NotionAdvancedTool.query_database(database_id="db_abc123...", filter={"property": "Status", "select": {"equals": "Done"}})

4. create_database:
   - Purpose: Initializes a new structural database matching user property requirements.
   - Arguments:
     a) parent_id: str - Target parent page location anchor ID (required).
     b) title: str - Database display header title string (required).
     c) properties: dict - Schema mapping properties defining names and cell type shapes (required).
     d) cred_key: str (default: "notion") - Storage lookup credential access identifier.
   - Returns: ToolResult tracking generated structural schemas.
   - How to call: NotionAdvancedTool.create_database(parent_id="pg_xyz987...", title="Bug Tracker", properties={"Bug Name": {"title": {}}, "Severity": {"select": {}}})

5. add_database_item:
   - Purpose: Appends a newly populated page entry record row to a database.
   - Arguments:
     a) database_id: str - Target structural database workspace container ID (required).
     b) properties: dict - Value mapping properties populated to match targeted schemas (required).
     c) cred_key: str (default: "notion") - Active credential identification key locator.
   - Returns: ToolResult reporting target object entry confirmations.
   - How to call: NotionAdvancedTool.add_database_item(database_id="db_abc123...", properties={"Bug Name": {"title": [{"text": {"content": "Login Timeout"}}]}})

6. update_database_item:
   - Purpose: Updates cell properties for a single database entry page.
   - Arguments:
     a) page_id: str - Target data page row tracking entry ID (required).
     b) properties: dict - Property maps grouping structural updates (required).
     c) cred_key: str (default: "notion") - Target verification access profile tracker.
   - Returns: ToolResult confirming updated entry records.
   - How to call: NotionAdvancedTool.update_database_item(page_id="pg_row11...", properties={"Severity": {"select": {"name": "Critical"}}})

7. delete_database_item:
   - Purpose: Moves an entry page row from active views into the workspace trash archive.
   - Arguments:
     a) page_id: str - Target tracking record identity node string (required).
     b) cred_key: str (default: "notion") - Token storage profile reference map key.
   - Returns: ToolResult reporting successful target record deletion.
   - How to call: NotionAdvancedTool.delete_database_item(page_id="pg_row11...")

8. create_page:
   - Purpose: Generates blank canvas spaces or rich custom sub-page layers.
   - Arguments:
     a) parent_id: str - Parent container page id (required).
     b) title: str - Document title name string header (required).
     c) content_blocks: list (default: None) - Structural block array configuring paragraph or visual parts.
     d) cred_key: str (default: "notion") - Account lookup configuration index verification keys.
   - Returns: ToolResult containing the generated public URL web access path.
   - How to call: NotionAdvancedTool.create_page(parent_id="pg_xyz987...", title="Meeting Minutes", content_blocks=[{"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "Notes"}}]}}])

9. get_page:
   - Purpose: Resolves layout definitions and metadata indexes associated with a page.
   - Arguments:
     a) page_id: str - target page locator identity node (required).
     b) cred_key: str (default: "notion") - Verification credentials registry reference link.
   - Returns: ToolResult enclosing structural meta mapping arrays.
   - How to call: NotionAdvancedTool.get_page(page_id="pg_xyz987...")

10. update_page:
    - Purpose: Updates structural page layouts or top-level titles.
    - Arguments:
      a) page_id: str - Target page unique container block identifier (required).
      b) properties: dict - Structural value properties updating key locations (required).
      d) cred_key: str (default: "notion") - Associated authorization verification identity parameter.
    - Returns: ToolResult tracking layout property changes.
    - How to call: NotionAdvancedTool.update_page(page_id="pg_xyz987...", properties={"title": {"title": [{"text": {"content": "Archived Minutes"}}]}})

11. append_blocks:
    - Purpose: Attaches a batch of layout blocks to a target page canvas or callout block.
    - Arguments:
      a) block_id: str - Target structural layout container ID anchor block (required).
      b) children: list - Block arrays detailing layout additions (required).
      c) cred_key: str (default: "notion") - Identity profile connection lookup variables.
    - Returns: ToolResult reporting validation updates.
    - How to call: NotionAdvancedTool.append_blocks(block_id="pg_xyz987...", children=[{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "New line"}}]}}])

12. get_blocks:
    - Purpose: Returns the layout child blocks belonging to a parent page block container.
    - Arguments:
      a) block_id: str - target structure container component reference code (required).
      b) cred_key: str (default: "notion") - Reference credentials verification key token.
    - Returns: ToolResult delivering localized layout element configurations.
    - How to call: NotionAdvancedTool.get_blocks(block_id="pg_xyz987...")

13. delete_block:
    - Purpose: Deletes a specific block layout element from a page canvas.
    - Arguments:
      a) block_id: str - Unique target block component element ID (required).
      b) cred_key: str (default: "notion") - Profile authorization token tracking lookup.
    - Returns: ToolResult logging the deleted elements.
    - How to call: NotionAdvancedTool.delete_block(block_id="blk_99887...")

14. create_table:
    - Purpose: Builds inline, formatted layout table rows inside a parent block workspace canvas.
    - Arguments:
      a) parent_id: str - Target canvas page container identifier layout ID (required).
      b) headers: list - Core headers string label vector (required).
      c) rows: list - Multi-level grid string array rows to display in the table cells (required).
      d) cred_key: str (default: "notion") - Core credential verification pointer index.
    - Returns: ToolResult detailing the processed cell structures.
    - How to call: NotionAdvancedTool.create_table(parent_id="pg_xyz987...", headers=["Task", "Owner"], rows=[["Setup Auth", "Dev A"], ["Tests", "Dev B"]])

15. create_kanban_view:
    - Purpose: Sets up workflow status trackers within custom item databases.
    - Arguments:
      a) database_id: str - target structural schema mapping container (required).
      b) cred_key: str (default: "notion") - Associated authorization profile lookup configuration token.
    - Returns: ToolResult tracking structural board column definitions.
    - How to call: NotionAdvancedTool.create_kanban_view(database_id="db_abc123...")

16. export_database_to_csv:
    - Purpose: flattens structural cell types into standard, downloadable CSV spreadsheets.
    - Arguments:
      a) database_id: str - Target structural schema layout block database ID (required).
      b) output: str - Target file path where local data is written (required).
      c) cred_key: str (default: "notion") - Active server login profiles authentication map.
    - Returns: ToolResult validating flat layout entries.
    - How to call: NotionAdvancedTool.export_database_to_csv(database_id="db_abc123...", output="./backups/vault.csv")

17. import_csv_to_database:
    - Purpose: Parses flat local files to generate matching database items.
    - Arguments:
      a) database_id: str - Target structural schema repository ID location (required).
      b) csv_path: str - Local spreadsheet location directory mapping path (required).
      c) property_mapping: dict (default: None) - Dictionary mapping CSV column headers to Notion properties.
      d) cred_key: str (default: "notion") - Storage lookup authorization index token pointers.
    - Returns: ToolResult displaying the imported dataset counts.
    - How to call: NotionAdvancedTool.import_csv_to_database(database_id="db_abc123...", csv_path="./data/users.csv", property_mapping={"User Name": "Title"})

18. create_template:
    - Purpose: Assembles design placeholders, emoji markers, canvas headers, and content layout blocks into a reusable template page.
    - Arguments:
      a) parent_id: str - Target directory layout storage parent ID (required).
      b) template_data: dict - Dictionary holding page properties (`title`, `content_blocks`, `icon`, `cover`) (required).
      c) cred_key: str (default: "notion") - Target service access certificate keys.
    - Returns: ToolResult verifying design template canvas properties.
    - How to call: NotionAdvancedTool.create_template(parent_id="pg_xyz987...", template_data={"title": "Weekly Sprint Boilerplate", "icon": "🚀"})

19. duplicate_page:
    - Purpose: Deep-copies page assets and nested blocks to a target destination directory while stripping system fields.
    - Arguments:
      a) page_id: str - Target page asset design profile template code key (required).
      b) parent_id: str - Target destination parent directory location id (required).
      c) cred_key: str (default: "notion") - Active client system tokens connection access validation.
    - Returns: ToolResult providing entry path access URLs for the duplicated asset canvas.
    - How to call: NotionAdvancedTool.duplicate_page(page_id="pg_source77...", parent_id="pg_dest88...")
""")
       
    @staticmethod
    def _client(cred_key: str = "notion"):
        from notion_client import Client
        token = CredStore.load(cred_key).get("token", "")
        if not token:
            raise ValueError("No Notion token. Store under 'notion' key.")
        return Client(auth=token)

    @staticmethod
    def _rich_text(s: str) -> list:
        return [{"type": "text", "text": {"content": s}}]

    # ── Search / Database ────────────────────────────────────────────────

    @staticmethod
    def search(query: str, filter_type: str = None,
               sort: str = "last_edited_time",
               cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            body: dict = {"query": query,
                          "sort": {"direction": "descending",
                                   "timestamp": sort}}
            if filter_type:
                body["filter"] = {"value": filter_type, "property": "object"}
            resp = n.search(**body)
            results = resp.get("results", [])
            return ToolResult(True, f"✓ {len(results)} results", results)
        except Exception as e:
            return ToolResult(False, f"✗ search failed: {e}")

    @staticmethod
    def get_database(database_id: str,
                     cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            db = n.databases.retrieve(database_id=database_id)
            return ToolResult(True, "✓ Database retrieved", db)
        except Exception as e:
            return ToolResult(False, f"✗ get_database failed: {e}")

    @staticmethod
    def query_database(database_id: str, filter: dict = None,
                       sorts: list = None, page_size: int = 100,
                       cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            kwargs: dict = {"database_id": database_id,
                            "page_size": page_size}
            if filter:
                kwargs["filter"] = filter
            if sorts:
                kwargs["sorts"] = sorts
            resp = n.databases.query(**kwargs)
            rows = resp.get("results", [])
            return ToolResult(True, f"✓ {len(rows)} rows", rows)
        except Exception as e:
            return ToolResult(False, f"✗ query_database failed: {e}")

    @staticmethod
    def create_database(parent_id: str, title: str, properties: dict,
                        cred_key: str = "notion") -> ToolResult:
        """
        properties: Notion property schema dict, e.g.
          {"Name": {"title": {}}, "Status": {"select": {}}}
        """
        try:
            n = NotionAdvancedTool._client(cred_key)
            db = n.databases.create(
                parent={"type": "page_id", "page_id": parent_id},
                title=NotionAdvancedTool._rich_text(title),
                properties=properties
            )
            return ToolResult(True, f"✓ Database created: {db['id']}", db)
        except Exception as e:
            return ToolResult(False, f"✗ create_database failed: {e}")

    @staticmethod
    def add_database_item(database_id: str, properties: dict,
                          cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            page = n.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            return ToolResult(True, f"✓ Item added: {page['id']}", page)
        except Exception as e:
            return ToolResult(False, f"✗ add_database_item failed: {e}")

    @staticmethod
    def update_database_item(page_id: str, properties: dict,
                              cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            page = n.pages.update(page_id=page_id, properties=properties)
            return ToolResult(True, f"✓ Item updated: {page_id}", page)
        except Exception as e:
            return ToolResult(False, f"✗ update_database_item failed: {e}")

    @staticmethod
    def delete_database_item(page_id: str,
                             cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            n.pages.update(page_id=page_id, archived=True)
            return ToolResult(True, f"✓ Item archived/deleted: {page_id}")
        except Exception as e:
            return ToolResult(False, f"✗ delete_database_item failed: {e}")

    # ── Pages ─────────────────────────────────────────────────────────────

    @staticmethod
    def create_page(parent_id: str, title: str,
                    content_blocks: list = None,
                    cred_key: str = "notion") -> ToolResult:
        """
        content_blocks: list of Notion block dicts.
        If None, a simple paragraph is created.
        """
        try:
            n = NotionAdvancedTool._client(cred_key)
            children = content_blocks or [{
                "object": "block", "type": "paragraph",
                "paragraph": {"rich_text": NotionAdvancedTool._rich_text("")}
            }]
            page = n.pages.create(
                parent={"page_id": parent_id},
                properties={"title": {"title": NotionAdvancedTool._rich_text(title)}},
                children=children
            )
            return ToolResult(True, f"✓ Page created: {page['url']}", page)
        except Exception as e:
            return ToolResult(False, f"✗ create_page failed: {e}")

    @staticmethod
    def get_page(page_id: str, cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            page = n.pages.retrieve(page_id=page_id)
            return ToolResult(True, "✓ Page retrieved", page)
        except Exception as e:
            return ToolResult(False, f"✗ get_page failed: {e}")

    @staticmethod
    def update_page(page_id: str, properties: dict,
                    cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            page = n.pages.update(page_id=page_id, properties=properties)
            return ToolResult(True, f"✓ Page updated: {page_id}", page)
        except Exception as e:
            return ToolResult(False, f"✗ update_page failed: {e}")

    # ── Blocks ────────────────────────────────────────────────────────────

    @staticmethod
    def append_blocks(block_id: str, children: list,
                      cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            resp = n.blocks.children.append(block_id=block_id,
                                            children=children)
            return ToolResult(True, f"✓ Blocks appended", resp)
        except Exception as e:
            return ToolResult(False, f"✗ append_blocks failed: {e}")

    @staticmethod
    def get_blocks(block_id: str, cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            resp = n.blocks.children.list(block_id=block_id)
            return ToolResult(True, f"✓ {len(resp.get('results',[]))} blocks",
                              resp.get("results", []))
        except Exception as e:
            return ToolResult(False, f"✗ get_blocks failed: {e}")

    @staticmethod
    def delete_block(block_id: str, cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            n.blocks.delete(block_id=block_id)
            return ToolResult(True, f"✓ Block deleted: {block_id}")
        except Exception as e:
            return ToolResult(False, f"✗ delete_block failed: {e}")

    # ── Special structures ────────────────────────────────────────────────

    @staticmethod
    def create_table(parent_id: str, headers: list, rows: list,
                     cred_key: str = "notion") -> ToolResult:
        """headers: ['Col1','Col2'...], rows: [['v1','v2'...], ...]"""
        try:
            n = NotionAdvancedTool._client(cred_key)
            table_width = len(headers)

            def _cell(text: str) -> list:
                return [{"type": "text", "text": {"content": text}}]

            table_rows = []
            # header row
            table_rows.append({
                "type": "table_row", "object": "block",
                "table_row": {"cells": [_cell(h) for h in headers]}
            })
            # data rows
            for row in rows:
                cells = [_cell(str(v)) for v in row]
                while len(cells) < table_width:
                    cells.append(_cell(""))
                table_rows.append({
                    "type": "table_row", "object": "block",
                    "table_row": {"cells": cells[:table_width]}
                })
            block = {
                "object": "block", "type": "table",
                "table": {
                    "table_width": table_width,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": table_rows
                }
            }
            resp = n.blocks.children.append(block_id=parent_id,
                                            children=[block])
            return ToolResult(True, f"✓ Table created with {len(rows)} rows", resp)
        except Exception as e:
            return ToolResult(False, f"✗ create_table failed: {e}")

    @staticmethod
    def create_kanban_view(database_id: str,
                           cred_key: str = "notion") -> ToolResult:
        """Adds a 'Status' select property and board view to the database."""
        try:
            n = NotionAdvancedTool._client(cred_key)
            # Ensure Status property exists
            n.databases.update(
                database_id=database_id,
                properties={
                    "Status": {
                        "select": {
                            "options": [
                                {"name": "Todo",        "color": "gray"},
                                {"name": "In Progress", "color": "blue"},
                                {"name": "Done",        "color": "green"},
                            ]
                        }
                    }
                }
            )
            return ToolResult(True, "✓ Kanban Status property added to database")
        except Exception as e:
            return ToolResult(False, f"✗ create_kanban_view failed: {e}")

    @staticmethod
    def export_database_to_csv(database_id: str, output: str,
                               cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            rows = []
            cursor = None
            while True:
                kwargs: dict = {"database_id": database_id, "page_size": 100}
                if cursor:
                    kwargs["start_cursor"] = cursor
                resp = n.databases.query(**kwargs)
                rows.extend(resp.get("results", []))
                if not resp.get("has_more"):
                    break
                cursor = resp.get("next_cursor")

            if not rows:
                return ToolResult(True, "✓ No rows to export", [])

            # Flatten properties
            all_keys: set = set()
            flat_rows = []
            for row in rows:
                flat: dict = {"id": row["id"]}
                for prop_name, prop_val in row.get("properties", {}).items():
                    ptype = prop_val.get("type", "")
                    if ptype == "title":
                        val = "".join(t["text"]["content"]
                                      for t in prop_val.get("title", []))
                    elif ptype == "rich_text":
                        val = "".join(t["text"]["content"]
                                      for t in prop_val.get("rich_text", []))
                    elif ptype == "select":
                        val = (prop_val.get("select") or {}).get("name", "")
                    elif ptype == "multi_select":
                        val = ", ".join(o["name"] for o in prop_val.get("multi_select", []))
                    elif ptype == "checkbox":
                        val = str(prop_val.get("checkbox", False))
                    elif ptype == "number":
                        val = str(prop_val.get("number", ""))
                    elif ptype == "date":
                        d = prop_val.get("date") or {}
                        val = d.get("start", "")
                    elif ptype == "url":
                        val = prop_val.get("url", "") or ""
                    elif ptype == "email":
                        val = prop_val.get("email", "") or ""
                    elif ptype == "phone_number":
                        val = prop_val.get("phone_number", "") or ""
                    else:
                        val = str(prop_val)
                    flat[prop_name] = val
                    all_keys.add(prop_name)
                flat_rows.append(flat)

            cols = ["id"] + sorted(all_keys)
            with open(output, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
                w.writeheader()
                w.writerows(flat_rows)
            return ToolResult(True, f"✓ Exported {len(flat_rows)} rows to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ export_database_to_csv failed: {e}")

    @staticmethod
    def import_csv_to_database(database_id: str, csv_path: str,
                                property_mapping: dict = None,
                                cred_key: str = "notion") -> ToolResult:
        """
        property_mapping: {csv_col: notion_property_name} — defaults to identity.
        All values imported as rich_text unless column name is 'title'/'Title'.
        """
        try:
            n = NotionAdvancedTool._client(cred_key)
            mapping = property_mapping or {}
            added = 0
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    props: dict = {}
                    for col, val in row.items():
                        notion_col = mapping.get(col, col)
                        if notion_col.lower() == "title":
                            props[notion_col] = {
                                "title": [{"text": {"content": val or ""}}]}
                        else:
                            props[notion_col] = {
                                "rich_text": [{"text": {"content": val or ""}}]}
                    n.pages.create(
                        parent={"database_id": database_id},
                        properties=props
                    )
                    added += 1
            return ToolResult(True, f"✓ Imported {added} rows")
        except Exception as e:
            return ToolResult(False, f"✗ import_csv_to_database failed: {e}")

    @staticmethod
    def create_template(parent_id: str, template_data: dict,
                        cred_key: str = "notion") -> ToolResult:
        """
        template_data: {title, content_blocks, icon, cover}
        Creates a page intended as a reusable template.
        """
        try:
            n = NotionAdvancedTool._client(cred_key)
            body: dict = {
                "parent": {"page_id": parent_id},
                "properties": {
                    "title": {
                        "title": NotionAdvancedTool._rich_text(
                            template_data.get("title", "Template"))
                    }
                },
            }
            if template_data.get("icon"):
                body["icon"] = {"type": "emoji",
                                "emoji": template_data["icon"]}
            if template_data.get("cover"):
                body["cover"] = {"type": "external",
                                 "external": {"url": template_data["cover"]}}
            if template_data.get("content_blocks"):
                body["children"] = template_data["content_blocks"]
            page = n.pages.create(**body)
            return ToolResult(True, f"✓ Template created: {page['url']}", page)
        except Exception as e:
            return ToolResult(False, f"✗ create_template failed: {e}")

    @staticmethod
    def duplicate_page(page_id: str, parent_id: str,
                       cred_key: str = "notion") -> ToolResult:
        try:
            n = NotionAdvancedTool._client(cred_key)
            orig = n.pages.retrieve(page_id=page_id)
            blocks_resp = n.blocks.children.list(block_id=page_id)
            children = blocks_resp.get("results", [])
            # strip server-managed fields from blocks
            clean_children = []
            skip_keys = {"id", "created_time", "last_edited_time",
                         "created_by", "last_edited_by", "has_children"}
            for b in children:
                cb = {k: v for k, v in b.items() if k not in skip_keys}
                clean_children.append(cb)
            new_page = n.pages.create(
                parent={"page_id": parent_id},
                properties=orig.get("properties", {}),
                children=clean_children[:100]  # API limit
            )
            return ToolResult(True, f"✓ Page duplicated: {new_page['url']}", new_page)
        except Exception as e:
            return ToolResult(False, f"✗ duplicate_page failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 3. LinearTool
# ═════════════════════════════════════════════════════════════════════════════

class LinearTool:
    name = "linear"
    description = (
        "Linear project management — issues, teams, projects, labels, "
        "cycles, members, and comments via GraphQL API"
    )
    use = ("""
Name of Tool: LinearTool

Purpose of Tool:
The LinearTool is a streamlined wrapper around Linear's GraphQL API, providing synchronous management 
for Agile software engineering projects. It translates complex GraphQL queries and mutations into clean 
Python static methods. This tool enables automation scripts to manage the full issue lifecycle (creating, 
filtering, updating, closing, and deleting tickets), organize spatial workspace frameworks (teams and projects), 
and orchestrate precise execution structures like development cycles (sprints), user management, taxonomy labels, 
and context-driven comment threads.

Methods:
- list_issues: Queries issues based on criteria like team, state, assignee, priority, or labels.
- get_issue: Fetches a single issue's deep information including state, priority, metadata, and comments.
- create_issue: Generates a new tracking issue with specific priority configurations, tags, and assignments.
- update_issue: Patches metadata attributes, title details, descriptions, or relational bindings on an issue.
- close_issue: Automates issue state conversion by resolving the parent team's active 'completed' workflow node.
- delete_issue: Erases an active tracking issue permanently from the workspace registry.
- list_teams: Extracts all accessible engineering teams alongside system profile keys and descriptions.
- get_team: Gathers individual team identities, structural descriptors, and nested member profiles.
- list_projects: Returns cross-team initiative groups or drills down into specific tracking project clusters.
- create_project: Establishes a major project timeline or feature roadmap tracked against targeted target dates.
- update_project: Overwrites specific operational milestones or descriptive headers on a project.
- list_members: Resolves member name indexes and internal communications tracking emails for a team.
- list_labels: Pulls custom scoping labels and visual color schemes applied across issue fields.
- create_label: Generates specific classification metadata or taxonomy tags for issues.
- list_cycles: Retrieves historical, current, and upcoming development cycles (sprints) detailing timeline spans.
- create_cycle: Launches a dedicated team sprint sequence bound by a start and end date.
- add_issue_to_cycle: Moves an operational tracking ticket directly into a target development sprint.
- get_comments: Fetches the raw text stream and author identity footprints of a ticket's comments.
- add_comment: Appends an absolute markdown contextual comment directly onto an active ticket.

How to use Tool Methods:

1. list_issues:
   - Purpose: Polls workspace issues matching specific parameters or structural scopes.
   - Arguments:
     a) team_id: str (default: None) - Structural team scope identifier string.
     b) state: str (default: None) - Workflow condition name query token matching target labels (e.g., "In Progress").
     c) assignee: str (default: None) - Identity pointer tracking a specific engineer.
     d) priority: int (default: None) - Numerical rank indexing priority severity.
     e) label: str (default: None) - Issue classification tag name filter.
     f) cred_key: str (default: "linear") - System credential key used to extract the API token.
   - Returns: ToolResult mapping matching issue dictionaries containing fundamental properties.
   - How to call: LinearTool.list_issues(team_id="team-xyz", state="In Progress", priority=1)

2. get_issue:
   - Purpose: Resolves complete contextual properties and operational comment blocks for a ticket.
   - Arguments:
     a) issue_id: str - Target issue identifier key string (required).
     b) cred_key: str (default: "linear") - Secure system vault key index location.
   - Returns: ToolResult holding complete descriptive nested schemas.
   - How to call: LinearTool.get_issue(issue_id="ISSUE-101")

3. create_issue:
   - Purpose: Adds a new issue payload record directly into Linear's active issue graph.
   - Arguments:
     a) title: str - Primary issue context abstract summary heading string (required).
     b) description: str (default: "") - Core structural problem reproduction notes.
     c) team_id: str (default: "") - Unique destination project team reference path.
     d) priority: int (default: 0) - Priority tier level rank indicator.
     e) assignee_id: str (default: None) - Core workspace engineer ID code block.
     f) label_ids: list (default: None) - Array of category labels strings to attach.
     g) due_date: str (default: None) - Target date tracking calendar deadline (YYYY-MM-DD format).
     h) cred_key: str (default: "linear") - Target execution vault client verification profile.
   - Returns: ToolResult validating transaction execution properties.
   - How to call: LinearTool.create_issue(title="Fix Session Timeout", team_id="team-abc", priority=1)

4. update_issue:
   - Purpose: Performs selective property structural mutations against a target tracking ticket.
   - Arguments:
     a) id: str - Target unique tracking node issue tracking ID (required).
     b) data: dict - Input mutation values matching Linear's 'IssueUpdateInput' structures (required).
     c) cred_key: str (default: "linear") - Account authentication lookups key profile pointer.
   - Returns: ToolResult checking return property results.
   - How to call: LinearTool.update_issue(id="ISSUE-101", data={"title": "Updated Session Timeout Title"})

5. close_issue:
   - Purpose: Moves an issue to its team's defined 'completed' state automatically.
   - Arguments:
     a) id: str - Target issue identifier alphanumeric sequence (required).
     b) resolution: str (default: "Done") - Resolution workflow status label lookup.
     c) cred_key: str (default: "linear") - Key mapping configuration reference pointers.
   - Returns: ToolResult providing update execution confirmations.
   - How to call: LinearTool.close_issue(id="ISSUE-101")

6. delete_issue:
   - Purpose: Drops an analytical project tracking issue from database indexes completely.
   - Arguments:
     a) id: str - Target issue tracking asset key string (required).
     b) cred_key: str (default: "linear") - Active workspace workspace integration profile key.
   - Returns: ToolResult displaying task success status.
   - How to call: LinearTool.delete_issue(id="ISSUE-101")

7. list_teams:
   - Purpose: Lists teams linked with a user workspace setup profile.
   - Arguments:
     a) cred_key: str (default: "linear") - Authorization store reference access key.
   - Returns: ToolResult containing array structures parsing operational profiles.
   - How to call: LinearTool.list_teams()

8. get_team:
   - Purpose: Pulls deep system architecture metrics and team details.
   - Arguments:
     a) team_id: str - Target corporate architecture team node ID code block (required).
     b) cred_key: str (default: "linear") - Internal credential lookup tracking directory index.
   - Returns: ToolResult verifying organizational details lists.
   - How to call: LinearTool.get_team(team_id="team-xyz")

9. list_projects:
   - Purpose: Collects cross-functional structural projects active in the product engine ecosystem.
   - Arguments:
     a) team_id: str (default: None) - Optional target team scope filter.
     b) cred_key: str (default: "linear") - Active repository identity credential access link maps.
   - Returns: ToolResult tracking structural project arrays.
   - How to call: LinearTool.list_projects(team_id="team-xyz")

10. create_project:
    - Purpose: Launches large-scale features or cross-sprint track items.
    - Arguments:
      a) name: str - Target scope initiative descriptor text (required).
      b) team_id: str - Core parent group tracker team container code link (required).
      c) description: str (default: "") - Operational objectives overview detailing plans.
      d) target_date: str (default: None) - Target completion calendar mapping (YYYY-MM-DD).
      e) cred_key: str (default: "linear") - System validation profile credentials pointer.
    - Returns: ToolResult logging the generated project metadata.
    - How to call: LinearTool.create_project(name="Migration 2026", team_id="team-abc", target_date="2026-12-31")

11. update_project:
    - Purpose: Updates general operational parameters or deadline dates across existing projects.
    - Arguments:
      a) id: str - Project identification asset tracking reference code (required).
      b) data: dict - Map definitions parsing 'ProjectUpdateInput' criteria mutations (required).
      c) cred_key: str (default: "linear") - Target network service connection profile key tags.
    - Returns: ToolResult verifying project state overrides.
    - How to call: LinearTool.update_project(id="proj-999", data={"description": "Updated roadmap details."})

12. list_members:
    - Purpose: Extracts engineers linked with a specified engineering tracking cluster.
    - Arguments:
      a) team_id: str - Target group cluster configuration path identifier (required).
      b) cred_key: str (default: "linear") - Reference integration verification workspace token.
    - Returns: ToolResult containing engineer profiles array definitions.
    - How to call: LinearTool.list_members(team_id="team-xyz")

13. list_labels:
    - Purpose: Pulls taxonomy scoping keys applied to differentiate work modules.
    - Arguments:
      a) team_id: str - Core targeted infrastructure group profile container key (required).
      b) cred_key: str (default: "linear") - Active credentials profile store key selector.
    - Returns: ToolResult providing dynamic categorization fields listings.
    - How to call: LinearTool.list_labels(team_id="team-xyz")

14. create_label:
    - Purpose: Registers new scope keywords or triage classification labels.
    - Arguments:
      a) name: str - Scoping name design label identifier text (required).
      b) color: str - Hex color code string format defining workspace display elements (required).
      c) team_id: str - Target architecture tracker profile group key code block (required).
      d) cred_key: str (default: "linear") - Server connection authentication locator array map keys.
    - Returns: ToolResult logging newly built category attributes.
    - How to call: LinearTool.create_label(name="Security Risk", color="#FF0000", team_id="team-xyz")

15. list_cycles:
    - Purpose: Returns timeline intervals mapping development work sprint cycles.
    - Arguments:
      a) team_id: str - Parent team tracker profile code block string (required).
      b) cred_key: str (default: "linear") - Verification credentials database token path locator.
    - Returns: ToolResult packaging nested roadmap tracking intervals.
    - How to call: LinearTool.list_cycles(team_id="team-xyz")

16. create_cycle:
    - Purpose: Initiates scheduled work intervals within team delivery tracks.
    - Arguments:
      a) name: str - Title header identification sequence identifying delivery sprints (required).
      b) team_id: str - Core parent production tracker group identifier token code (required).
      c) start_date: str - Sequence deployment commencement index tracking point (required).
      d) end_date: str - Sequence termination timeframe reference date (required).
      e) cred_key: str (default: "linear") - Security account authorization validation token tags.
    - Returns: ToolResult logging deployment schedule boundaries.
    - How to call: LinearTool.create_cycle(name="Cycle 14", team_id="team-xyz", start_date="2026-07-01", end_date="2026-07-14")

17. add_issue_to_cycle:
    - Purpose: Pins an orphan development ticket into a specific execution period schedule.
    - Arguments:
      a) cycle_id: str - Target structural sprint interval framework tracking index (required).
      b) issue_id: str - Target individual tracking node item key code string (required).
      c) cred_key: str (default: "linear") - Vault credentials collection storage index access markers.
    - Returns: ToolResult verifying track schedule reallocation.
    - How to call: LinearTool.add_issue_to_cycle(cycle_id="cycle-44", issue_id="ISSUE-101")

18. get_comments:
    - Purpose: Pulls asynchronous dialogue documentation history entries from an active tracking task card.
    - Arguments:
      a) issue_id: str - Target problem description tracking document id (required).
      b) cred_key: str (default: "linear") - Network endpoint profile reference token pointers.
    - Returns: ToolResult packaging dialog log structures array entries.
    - How to call: LinearTool.get_comments(issue_id="ISSUE-101")

19. add_comment:
    - Purpose: Encodes analytical observations, execution status logs, or links onto tickets.
    - Arguments:
      a) issue_id: str - Destination item card workspace container identifier node string (required).
      b) body: str - Main communication content note block format using markdown styling options (required).
      c) cred_key: str (default: "linear") - Vault database index profile interface access tokens.
    - Returns: ToolResult confirming dialogue stream integration updates.
    - How to call: LinearTool.add_comment(issue_id="ISSUE-101", body="PR merged successfully. Ready to verify.")
""")
       
    @staticmethod
    def _gql(query: str, variables: dict = None,
             cred_key: str = "linear") -> dict:
        import requests
        token = CredStore.load(cred_key).get("api_key", "")
        if not token:
            raise ValueError("No Linear API key. Store under 'linear' key.")
        resp = requests.post(
            "https://api.linear.app/graphql",
            json={"query": query, "variables": variables or {}},
            headers={"Authorization": token,
                     "Content-Type": "application/json"},
            timeout=20
        )
        resp.raise_for_status()
        data = resp.json()
        if "errors" in data:
            raise ValueError(data["errors"][0].get("message", "GraphQL error"))
        return data.get("data", {})

    # ── Issues ────────────────────────────────────────────────────────────

    @staticmethod
    def list_issues(team_id: str = None, state: str = None,
                    assignee: str = None, priority: int = None,
                    label: str = None,
                    cred_key: str = "linear") -> ToolResult:
        try:
            filters = []
            if team_id:
                filters.append(f'team: {{id: {{eq: "{team_id}"}}}}')
            if state:
                filters.append(f'state: {{name: {{eq: "{state}"}}}}')
            if assignee:
                filters.append(f'assignee: {{id: {{eq: "{assignee}"}}}}')
            if priority is not None:
                filters.append(f"priority: {{eq: {priority}}}")
            filter_str = ("{" + ", ".join(filters) + "}") if filters else ""
            filter_arg = f"(filter: {filter_str})" if filter_str else "(first: 50)"
            q = f"""
            query {{
              issues{filter_arg} {{
                nodes {{
                  id title state {{ name }} priority
                  assignee {{ name }}
                  labels {{ nodes {{ name }} }}
                  dueDate createdAt url
                }}
              }}
            }}"""
            data = LinearTool._gql(q, cred_key=cred_key)
            issues = data.get("issues", {}).get("nodes", [])
            return ToolResult(True, f"✓ {len(issues)} issues", issues)
        except Exception as e:
            return ToolResult(False, f"✗ list_issues failed: {e}")

    @staticmethod
    def get_issue(issue_id: str, cred_key: str = "linear") -> ToolResult:
        try:
            q = """
            query($id: String!) {
              issue(id: $id) {
                id title description state { name } priority
                assignee { name email }
                labels { nodes { name } }
                dueDate createdAt updatedAt url
                comments { nodes { id body createdAt user { name } } }
              }
            }"""
            data = LinearTool._gql(q, {"id": issue_id}, cred_key)
            return ToolResult(True, "✓ Issue retrieved", data.get("issue"))
        except Exception as e:
            return ToolResult(False, f"✗ get_issue failed: {e}")

    @staticmethod
    def create_issue(title: str, description: str = "",
                     team_id: str = "", priority: int = 0,
                     assignee_id: str = None, label_ids: list = None,
                     due_date: str = None,
                     cred_key: str = "linear") -> ToolResult:
        try:
            m = """
            mutation($input: IssueCreateInput!) {
              issueCreate(input: $input) {
                success issue { id title url }
              }
            }"""
            inp: dict = {"title": title, "description": description,
                         "teamId": team_id, "priority": priority}
            if assignee_id:
                inp["assigneeId"] = assignee_id
            if label_ids:
                inp["labelIds"] = label_ids
            if due_date:
                inp["dueDate"] = due_date
            data = LinearTool._gql(m, {"input": inp}, cred_key)
            result = data.get("issueCreate", {})
            return ToolResult(result.get("success", False),
                              f"✓ Issue created" if result.get("success")
                              else "✗ Creation failed",
                              result.get("issue"))
        except Exception as e:
            return ToolResult(False, f"✗ create_issue failed: {e}")

    @staticmethod
    def update_issue(id: str, data: dict,
                     cred_key: str = "linear") -> ToolResult:
        try:
            m = """
            mutation($id: String!, $input: IssueUpdateInput!) {
              issueUpdate(id: $id, input: $input) {
                success issue { id title }
              }
            }"""
            resp = LinearTool._gql(m, {"id": id, "input": data}, cred_key)
            result = resp.get("issueUpdate", {})
            return ToolResult(result.get("success", False),
                              "✓ Issue updated" if result.get("success")
                              else "✗ Update failed",
                              result.get("issue"))
        except Exception as e:
            return ToolResult(False, f"✗ update_issue failed: {e}")

    @staticmethod
    def close_issue(id: str, resolution: str = "Done",
                    cred_key: str = "linear") -> ToolResult:
        try:
            # Get the "Done" state id for the issue's team
            q = """
            query($id: String!) {
              issue(id: $id) { team { id } }
            }"""
            d = LinearTool._gql(q, {"id": id}, cred_key)
            team_id = d["issue"]["team"]["id"]
            sq = """
            query($filter: WorkflowStateFilter) {
              workflowStates(filter: $filter) {
                nodes { id name type }
              }
            }"""
            sd = LinearTool._gql(
                sq,
                {"filter": {"team": {"id": {"eq": team_id}},
                            "type": {"eq": "completed"}}},
                cred_key
            )
            states = sd.get("workflowStates", {}).get("nodes", [])
            state_id = states[0]["id"] if states else None
            inp: dict = {}
            if state_id:
                inp["stateId"] = state_id
            return LinearTool.update_issue(id, inp, cred_key)
        except Exception as e:
            return ToolResult(False, f"✗ close_issue failed: {e}")

    @staticmethod
    def delete_issue(id: str, cred_key: str = "linear") -> ToolResult:
        try:
            m = """
            mutation($id: String!) {
              issueDelete(id: $id) { success }
            }"""
            data = LinearTool._gql(m, {"id": id}, cred_key)
            ok = data.get("issueDelete", {}).get("success", False)
            return ToolResult(ok, "✓ Deleted" if ok else "✗ Delete failed")
        except Exception as e:
            return ToolResult(False, f"✗ delete_issue failed: {e}")

    # ── Teams / Projects ──────────────────────────────────────────────────

    @staticmethod
    def list_teams(cred_key: str = "linear") -> ToolResult:
        try:
            q = "query { teams { nodes { id name key description } } }"
            data = LinearTool._gql(q, cred_key=cred_key)
            teams = data.get("teams", {}).get("nodes", [])
            return ToolResult(True, f"✓ {len(teams)} teams", teams)
        except Exception as e:
            return ToolResult(False, f"✗ list_teams failed: {e}")

    @staticmethod
    def get_team(team_id: str, cred_key: str = "linear") -> ToolResult:
        try:
            q = """
            query($id: String!) {
              team(id: $id) { id name key description members { nodes { id name } } }
            }"""
            data = LinearTool._gql(q, {"id": team_id}, cred_key)
            return ToolResult(True, "✓ Team retrieved", data.get("team"))
        except Exception as e:
            return ToolResult(False, f"✗ get_team failed: {e}")

    @staticmethod
    def list_projects(team_id: str = None,
                      cred_key: str = "linear") -> ToolResult:
        try:
            if team_id:
                q = """
                query($id: String!) {
                  team(id: $id) { projects { nodes { id name state description } } }
                }"""
                data = LinearTool._gql(q, {"id": team_id}, cred_key)
                projects = (data.get("team", {})
                            .get("projects", {})
                            .get("nodes", []))
            else:
                q = "query { projects { nodes { id name state } } }"
                data = LinearTool._gql(q, cred_key=cred_key)
                projects = data.get("projects", {}).get("nodes", [])
            return ToolResult(True, f"✓ {len(projects)} projects", projects)
        except Exception as e:
            return ToolResult(False, f"✗ list_projects failed: {e}")

    @staticmethod
    def create_project(name: str, team_id: str, description: str = "",
                       target_date: str = None,
                       cred_key: str = "linear") -> ToolResult:
        try:
            m = """
            mutation($input: ProjectCreateInput!) {
              projectCreate(input: $input) {
                success project { id name url }
              }
            }"""
            inp: dict = {"name": name, "teamIds": [team_id],
                         "description": description}
            if target_date:
                inp["targetDate"] = target_date
            data = LinearTool._gql(m, {"input": inp}, cred_key)
            result = data.get("projectCreate", {})
            return ToolResult(result.get("success", False),
                              "✓ Project created",
                              result.get("project"))
        except Exception as e:
            return ToolResult(False, f"✗ create_project failed: {e}")

    @staticmethod
    def update_project(id: str, data: dict,
                       cred_key: str = "linear") -> ToolResult:
        try:
            m = """
            mutation($id: String!, $input: ProjectUpdateInput!) {
              projectUpdate(id: $id, input: $input) {
                success project { id name }
              }
            }"""
            resp = LinearTool._gql(m, {"id": id, "input": data}, cred_key)
            result = resp.get("projectUpdate", {})
            return ToolResult(result.get("success", False),
                              "✓ Project updated", result.get("project"))
        except Exception as e:
            return ToolResult(False, f"✗ update_project failed: {e}")

    # ── Members / Labels / Cycles ─────────────────────────────────────────

    @staticmethod
    def list_members(team_id: str, cred_key: str = "linear") -> ToolResult:
        try:
            q = """
            query($id: String!) {
              team(id: $id) { members { nodes { id name email } } }
            }"""
            data = LinearTool._gql(q, {"id": team_id}, cred_key)
            members = (data.get("team", {})
                       .get("members", {})
                       .get("nodes", []))
            return ToolResult(True, f"✓ {len(members)} members", members)
        except Exception as e:
            return ToolResult(False, f"✗ list_members failed: {e}")

    @staticmethod
    def list_labels(team_id: str, cred_key: str = "linear") -> ToolResult:
        try:
            q = """
            query($id: String!) {
              team(id: $id) { labels { nodes { id name color } } }
            }"""
            data = LinearTool._gql(q, {"id": team_id}, cred_key)
            labels = (data.get("team", {})
                      .get("labels", {})
                      .get("nodes", []))
            return ToolResult(True, f"✓ {len(labels)} labels", labels)
        except Exception as e:
            return ToolResult(False, f"✗ list_labels failed: {e}")

    @staticmethod
    def create_label(name: str, color: str, team_id: str,
                     cred_key: str = "linear") -> ToolResult:
        try:
            m = """
            mutation($input: IssueLabelCreateInput!) {
              issueLabelCreate(input: $input) {
                success issueLabel { id name color }
              }
            }"""
            data = LinearTool._gql(
                m, {"input": {"name": name, "color": color,
                              "teamId": team_id}}, cred_key)
            result = data.get("issueLabelCreate", {})
            return ToolResult(result.get("success", False),
                              "✓ Label created", result.get("issueLabel"))
        except Exception as e:
            return ToolResult(False, f"✗ create_label failed: {e}")

    @staticmethod
    def list_cycles(team_id: str, cred_key: str = "linear") -> ToolResult:
        try:
            q = """
            query($id: String!) {
              team(id: $id) { cycles { nodes { id name number startsAt endsAt } } }
            }"""
            data = LinearTool._gql(q, {"id": team_id}, cred_key)
            cycles = (data.get("team", {})
                      .get("cycles", {})
                      .get("nodes", []))
            return ToolResult(True, f"✓ {len(cycles)} cycles", cycles)
        except Exception as e:
            return ToolResult(False, f"✗ list_cycles failed: {e}")

    @staticmethod
    def create_cycle(name: str, team_id: str, start_date: str,
                     end_date: str, cred_key: str = "linear") -> ToolResult:
        try:
            m = """
            mutation($input: CycleCreateInput!) {
              cycleCreate(input: $input) {
                success cycle { id name startsAt endsAt }
              }
            }"""
            data = LinearTool._gql(
                m, {"input": {"name": name, "teamId": team_id,
                              "startsAt": start_date,
                              "endsAt": end_date}}, cred_key)
            result = data.get("cycleCreate", {})
            return ToolResult(result.get("success", False),
                              "✓ Cycle created", result.get("cycle"))
        except Exception as e:
            return ToolResult(False, f"✗ create_cycle failed: {e}")

    @staticmethod
    def add_issue_to_cycle(cycle_id: str, issue_id: str,
                           cred_key: str = "linear") -> ToolResult:
        try:
            m = """
            mutation($id: String!, $input: IssueUpdateInput!) {
              issueUpdate(id: $id, input: $input) { success }
            }"""
            data = LinearTool._gql(
                m, {"id": issue_id, "input": {"cycleId": cycle_id}}, cred_key)
            ok = data.get("issueUpdate", {}).get("success", False)
            return ToolResult(ok, "✓ Issue added to cycle" if ok
                              else "✗ Failed")
        except Exception as e:
            return ToolResult(False, f"✗ add_issue_to_cycle failed: {e}")

    # ── Comments ──────────────────────────────────────────────────────────

    @staticmethod
    def get_comments(issue_id: str, cred_key: str = "linear") -> ToolResult:
        try:
            q = """
            query($id: String!) {
              issue(id: $id) {
                comments { nodes { id body createdAt user { name } } }
              }
            }"""
            data = LinearTool._gql(q, {"id": issue_id}, cred_key)
            comments = (data.get("issue", {})
                        .get("comments", {})
                        .get("nodes", []))
            return ToolResult(True, f"✓ {len(comments)} comments", comments)
        except Exception as e:
            return ToolResult(False, f"✗ get_comments failed: {e}")

    @staticmethod
    def add_comment(issue_id: str, body: str,
                    cred_key: str = "linear") -> ToolResult:
        try:
            m = """
            mutation($input: CommentCreateInput!) {
              commentCreate(input: $input) {
                success comment { id body }
              }
            }"""
            data = LinearTool._gql(
                m, {"input": {"issueId": issue_id, "body": body}}, cred_key)
            result = data.get("commentCreate", {})
            return ToolResult(result.get("success", False),
                              "✓ Comment added", result.get("comment"))
        except Exception as e:
            return ToolResult(False, f"✗ add_comment failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 4. AsanaTool
# ═════════════════════════════════════════════════════════════════════════════

class AsanaTool:
    name = "asana"
    description = (
        "Asana project management — workspaces, projects, tasks, subtasks, "
        "sections, tags, and comments"
    )
    use = ("""
Name of Tool: AsanaTool

Purpose of Tool:
The AsanaTool is a synchronous python wrapper around the official Asana python SDK. It simplifies complex workspace, 
project, task, subtask, section, tag, and conversation story interactions into accessible static methods. It abstracts 
authentication mechanics using a centralized credential storage system (`CredStore`), safely packages API actions inside 
a standardized transactional return model (`ToolResult`), and offers an automation-friendly matrix for cross-functional 
project management pipelines.

Methods:
- list_workspaces: Retrieves available primary workspaces or collaborative organizational units.
- list_projects: Returns scoped projects mapped to specific workspaces or teams.
- get_project: Retrieves exact operational definitions, settings, and metadata profiles for an active project.
- create_project: provisions a brand new container project inside a dedicated target workspace architecture.
- list_tasks: Polls active work item registries applying custom assignment, project, or schedule limits.
- get_task: Fetches comprehensive field configurations, state mappings, and core profiles of a specific item task card.
- create_task: Injects a brand new deliverable task directly into a defined target workspace cluster.
- update_task: Performs partial patch property replacements across mutable field sets on an active task.
- complete_task: Quickly transitions a targeted task card status into a finalized "completed" validation state.
- delete_task: Permanently drops a work tracking item entry from active database records.
- add_subtask: Spawns an execution dependency child task tracking element directly beneath an existing parent card.
- list_subtasks: Extracts an ordered list collection identifying child dependency elements under a target task.
- add_comment: Posts an informative thread entry (story node) to capture communication context directly onto a card.
- list_comments: Filters through raw task histories to extract purely textual human comment entry points.
- list_sections: Identifies organizational tracking pipelines (kanban stages/list groupings) inside a target project.
- create_section: Injects an isolated sorting header stage or column inside an explicit project dashboard canvas.
- move_task_to_section: Relocates an execution task item card laterally into a different operational lifecycle phase.
- list_tags: Queries global categorization labels or taxonomy chips indexing a parent workspace structure.
- add_tag_to_task: Pins an indexing taxonomy classification label directly onto an active target item.

How to use Tool Methods:

1. list_workspaces:
   - Purpose: Lists accessible workspaces mapped to the integration context profile.
   - Arguments:
     a) cred_key: str (default: "asana") - Token mapping index key located within the system configuration vault.
   - Returns: ToolResult holding an array of workspace summary dictionary items.
   - How to call: AsanaTool.list_workspaces()

2. list_projects:
   - Purpose: Extracts projects filtered across specified structural containers.
   - Arguments:
     a) workspace_id: str (default: None) - Global identifier parsing a target workspace node.
     b) team_id: str (default: None) - Filter constraint isolating a targeted workspace group tracker.
     c) cred_key: str (default: "asana") - Integration vault validation access identity lookup indicator.
   - Returns: ToolResult storing array maps describing match project profiles.
   - How to call: AsanaTool.list_projects(workspace_id="12345")

3. get_project:
   - Purpose: Pulls deep system metadata parameters referencing an established workspace project.
   - Arguments:
     a) project_id: str - Target identification system string mapping a live project entry (required).
     b) cred_key: str (default: "asana") - Encryption store profile lookup indicator mapping key tokens.
   - Returns: ToolResult containing key-value configurations indexing the target project node.
   - How to call: AsanaTool.get_project(project_id="98765")

4. create_project:
   - Purpose: Instantiates a distinct tracking blueprint module inside a user workspace environment.
   - Arguments:
     a) name: str - Target title header classifying the newly generated project space (required).
     b) workspace_id: str - Absolute parent infrastructure identity token block string (required).
     c) team_id: str (default: None) - Sub-group team architecture alignment pointer sequence.
     d) notes: str (default: "") - Operational objectives description overview log detailing context.
     e) color: str (default: "none") - Theme element hex styling token color keyword tracker.
     f) public: bool (default: True) - Visibility access permissions state control indicator.
     g) cred_key: str (default: "asana") - System gateway authorization credentials validation key.
   - Returns: ToolResult packing transaction results alongside properties of the new workspace instance.
   - How to call: AsanaTool.create_project(name="Q3 Product Roadmap", workspace_id="12345", color="dark-blue")

5. list_tasks:
   - Purpose: Fetches matching action items based on contextual parameters.
   - Arguments:
     a) project_id: str (default: None) - Scope identifier limiting results to a single workspace grid canvas.
     b) assignee: str (default: None) - Identity lookup filtering elements specifically assigned to an engineer.
     c) completed: bool (default: False) - Flag toggling the exclusion of archive closed actions lists.
     d) due_on: str (default: None) - Target completion deadline milestone tracker (YYYY-MM-DD).
     e) cred_key: str (default: "asana") - Core authentication credential profile identifier code string.
   - Returns: ToolResult packaging matched array entries tracking task parameters.
   - How to call: AsanaTool.list_tasks(project_id="98765", assignee="user_abc_77")

6. get_task:
   - Purpose: Exposes explicit property states, custom metric fields, and descriptions of a specific ticket.
   - Arguments:
     a) task_id: str - Unique entity global mapping tracking identifier code block sequence (required).
     b) cred_key: str (default: "asana") - Security parameters client context lookup locator token.
   - Returns: ToolResult detailing complete internal variable settings defining the target node card.
   - How to call: AsanaTool.get_task(task_id="112233")

7. create_task:
   - Purpose: Builds a discrete tracking card module mapping operational actions into active records.
   - Arguments:
     a) name: str - Title header description labeling the target core deliverable action item (required).
     b) workspace_id: str - Core parent architecture container reference link index string (required).
     c) project_id: str (default: None) - Optional secondary project map list assignment index array.
     d) assignee: str (default: None) - Target identity engineer parameter mapping primary ownership.
     d) notes: str (default: "") - Problem log descriptions, reproduction pathways, or goal text.
     e) due_on: str (default: None) - Calendar target limit constraints configuration values (YYYY-MM-DD).
     f) custom_fields: dict (default: None) - Map parameters defining company metadata workspace fields.
     g) cred_key: str (default: "asana") - System access key validation token reference profile.
   - Returns: ToolResult logging the generated output asset attributes tracking codes.
   - How to call: AsanaTool.create_task(name="Refactor Auth Middleware", workspace_id="12345", project_id="98765")

8. update_task:
   - Purpose: Mutates specific parameters directly across a running project management ticket asset.
   - Arguments:
     a) id: str - Target global asset identity tracking code sequence index value (required).
     b) data: dict - Map payload detailing specific field attributes to selectively replace (required).
     c) cred_key: str (default: "asana") - Connection store verification directory key string.
   - Returns: ToolResult confirming updated state schemas data returns.
   - How to call: AsanaTool.update_task(id="112233", data={"notes": "Updated engineering deployment notes."})

9. complete_task:
   - Purpose: Shifts task configuration parameter values to mark items as resolved.
   - Arguments:
     a) id: str - Target ticket card global instance validation code locator (required).
     b) cred_key: str (default: "asana") - Access profiles infrastructure registry store tag.
   - Returns: ToolResult detailing updated metadata properties showing success state.
   - How to call: AsanaTool.complete_task(id="112233")

10. delete_task:
    - Purpose: Removes an active task module record configuration map out of workspace registers.
    - Arguments:
      a) id: str - Targeted asset database unique mapping index identifier key code (required).
      b) cred_key: str (default: "asana") - Active workspace security server profile access verification keys.
    - Returns: ToolResult validating task deletion execution properties.
    - How to call: AsanaTool.delete_task(id="112233")

11. add_subtask:
    - Purpose: Attaches structural workflow dependency items hierarchically directly underneath a target card.
    - Arguments:
      a) parent_task_id: str - Target parent tracking card index system identifier path (required).
      b) name: str - Title text defining scope tracking elements assigned to subtasks (required).
      c) assignee: str (default: None) - Selected engineer profile reference tracking identity.
      d) notes: str (default: "") - Descriptive criteria text providing details for subtasks.
      e) cred_key: str (default: "asana") - Active internal connection mapping access credential token keys.
    - Returns: ToolResult verifying new nested deployment item generation tracking codes.
    - How to call: AsanaTool.add_subtask(parent_task_id="112233", name="Write Unit Tests")

12. list_subtasks:
    - Purpose: Extracts nested sub-tier work assignments clustered under an active tracking task card.
    - Arguments:
      a) task_id: str - Base parent node ticket index reference verification identifier code (required).
      b) cred_key: str (default: "asana") - Corporate credentials storage vault system reference directory.
    - Returns: ToolResult enclosing data arrays detailing subtask summary elements.
    - How to call: AsanaTool.list_subtasks(task_id="112233")

13. add_comment:
    - Purpose: Appends dialogue documentation remarks directly into active team tracking communication logs.
    - Arguments:
      a) task_id: str - Target context documentation workspace card identity sequence (required).
      b) text: str - Textual communication block layout outlining status changes or remarks (required).
      c) cred_key: str (default: "asana") - Network endpoints validation verification access key string.
    - Returns: ToolResult reporting transaction confirmations over created story nodes.
    - How to call: AsanaTool.add_comment(task_id="112233", text="Code review completed; awaiting deployment approvals.")

14. list_comments:
    - Purpose: Traverses task history records to fetch operational dialogue remarks while discarding system actions logs.
    - Arguments:
      a) task_id: str - Base platform infrastructure data tracking lookup asset key (required).
      b) cred_key: str (default: "asana") - Network channel connection verification workspace key profiles.
    - Returns: ToolResult parsing filtered conversational story item list configurations.
    - How to call: AsanaTool.list_comments(task_id="112233")

15. list_sections:
    - Purpose: Displays workflow progression lanes mapped to the architectural design of a specified project canvas.
    - Arguments:
      a) project_id: str - Target project layout configuration system identification string (required).
      b) cred_key: str (default: "asana") - Internal integration token lookup location pointer profile.
    - Returns: ToolResult packing array collections sorting column block lane identities.
    - How to call: AsanaTool.list_sections(project_id="98765")

16. create_section:
    - Purpose: Adds structured pipeline stages or categorizations inside project canvas layouts.
    - Arguments:
      a) project_id: str - Target design container interface registry locator path (required).
      b) name: str - Unique staging text phrase identifying pipeline milestones (required).
      c) cred_key: str (default: "asana") - Account configuration integration interface secret locator indices.
    - Returns: ToolResult verifying step stage generation metadata.
    - How to call: AsanaTool.create_section(project_id="98765", name="Awaiting QA")

17. move_task_to_section:
    - Purpose: Shifts task assignments horizontally across workflow stages in list or board tracking configurations.
    - Arguments:
      a) task_id: str - Core individual tracking card element lookup code string (required).
      b) section_id: str - Destination column milestone framework structural reference parameter (required).
      c) cred_key: str (default: "asana") - Vault data repository credential interface access profiles.
    - Returns: ToolResult tracking pipeline state reassignment validations.
    - How to call: AsanaTool.move_task_to_section(task_id="112233", section_id="sec_554433")

18. list_tags:
    - Purpose: Pulls taxonomy labels applied across a broad corporate workspace environment.
    - Arguments:
      a) workspace_id: str - Base parent architecture tracking system group path code blocks (required).
      b) cred_key: str (default: "asana") - Identity interface verification workspace database token keys.
    - Returns: ToolResult detailing available workspace taxonomy keyword chips.
    - How to call: AsanaTool.list_tags(workspace_id="12345")

19. add_tag_to_task:
    - Purpose: Links an existing categorization tag token element onto an active target tracking item.
    - Arguments:
      a) task_id: str - Destination tracking card item system identifier lookup sequence (required).
      b) tag_id: str - Targeted cross-project triage categorization reference code tag (required).
      c) cred_key: str (default: "asana") - Authentication store system server security configuration records.
    - Returns: ToolResult mapping successful completion status logs.
    - How to call: AsanaTool.add_tag_to_task(task_id="112233", tag_id="tag_776655")
""")
       
    @staticmethod
    def _client(cred_key: str = "asana"):
        import asana
        token = CredStore.load(cred_key).get("access_token", "")
        if not token:
            raise ValueError("No Asana token. Store under 'asana' key.")
        config = asana.Configuration()
        config.access_token = token
        return asana.ApiClient(config)

    @staticmethod
    def list_workspaces(cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.WorkspacesApi(client)
            ws = list(api.get_workspaces({}))
            return ToolResult(True, f"✓ {len(ws)} workspaces", ws)
        except Exception as e:
            return ToolResult(False, f"✗ list_workspaces failed: {e}")

    @staticmethod
    def list_projects(workspace_id: str = None, team_id: str = None,
                      cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.ProjectsApi(client)
            opts: dict = {}
            if workspace_id:
                opts["workspace"] = workspace_id
            if team_id:
                opts["team"] = team_id
            projects = list(api.get_projects(opts))
            return ToolResult(True, f"✓ {len(projects)} projects", projects)
        except Exception as e:
            return ToolResult(False, f"✗ list_projects failed: {e}")

    @staticmethod
    def get_project(project_id: str, cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.ProjectsApi(client)
            proj = api.get_project(project_id, {})
            return ToolResult(True, "✓ Project retrieved", proj)
        except Exception as e:
            return ToolResult(False, f"✗ get_project failed: {e}")

    @staticmethod
    def create_project(name: str, workspace_id: str,
                       team_id: str = None, notes: str = "",
                       color: str = "none", public: bool = True,
                       cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.ProjectsApi(client)
            body: dict = {
                "data": {"name": name, "workspace": workspace_id,
                         "notes": notes, "color": color,
                         "public": public}
            }
            if team_id:
                body["data"]["team"] = team_id
            proj = api.create_project(body, {})
            return ToolResult(True, f"✓ Project created: {proj.get('gid','')}", proj)
        except Exception as e:
            return ToolResult(False, f"✗ create_project failed: {e}")

    @staticmethod
    def list_tasks(project_id: str = None, assignee: str = None,
                   completed: bool = False, due_on: str = None,
                   cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.TasksApi(client)
            opts: dict = {"completed_since": "now" if not completed else ""}
            if project_id:
                opts["project"] = project_id
            if assignee:
                opts["assignee"] = assignee
            if due_on:
                opts["due_on"] = due_on
            tasks = list(api.get_tasks(opts))
            return ToolResult(True, f"✓ {len(tasks)} tasks", tasks)
        except Exception as e:
            return ToolResult(False, f"✗ list_tasks failed: {e}")

    @staticmethod
    def get_task(task_id: str, cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.TasksApi(client)
            task = api.get_task(task_id, {})
            return ToolResult(True, "✓ Task retrieved", task)
        except Exception as e:
            return ToolResult(False, f"✗ get_task failed: {e}")

    @staticmethod
    def create_task(name: str, workspace_id: str,
                    project_id: str = None, assignee: str = None,
                    notes: str = "", due_on: str = None,
                    custom_fields: dict = None,
                    cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.TasksApi(client)
            body: dict = {
                "data": {"name": name, "workspace": workspace_id,
                         "notes": notes}
            }
            if project_id:
                body["data"]["projects"] = [project_id]
            if assignee:
                body["data"]["assignee"] = assignee
            if due_on:
                body["data"]["due_on"] = due_on
            if custom_fields:
                body["data"]["custom_fields"] = custom_fields
            task = api.create_task(body, {})
            return ToolResult(True, f"✓ Task created: {task.get('gid','')}", task)
        except Exception as e:
            return ToolResult(False, f"✗ create_task failed: {e}")

    @staticmethod
    def update_task(id: str, data: dict,
                    cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.TasksApi(client)
            task = api.update_task({"data": data}, id, {})
            return ToolResult(True, "✓ Task updated", task)
        except Exception as e:
            return ToolResult(False, f"✗ update_task failed: {e}")

    @staticmethod
    def complete_task(id: str, cred_key: str = "asana") -> ToolResult:
        return AsanaTool.update_task(id, {"completed": True}, cred_key)

    @staticmethod
    def delete_task(id: str, cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.TasksApi(client)
            api.delete_task(id)
            return ToolResult(True, f"✓ Task deleted: {id}")
        except Exception as e:
            return ToolResult(False, f"✗ delete_task failed: {e}")

    @staticmethod
    def add_subtask(parent_task_id: str, name: str,
                    assignee: str = None, notes: str = "",
                    cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.TasksApi(client)
            body: dict = {"data": {"name": name, "notes": notes}}
            if assignee:
                body["data"]["assignee"] = assignee
            subtask = api.create_subtask_for_task(body, parent_task_id, {})
            return ToolResult(True, f"✓ Subtask created: {subtask.get('gid','')}", subtask)
        except Exception as e:
            return ToolResult(False, f"✗ add_subtask failed: {e}")

    @staticmethod
    def list_subtasks(task_id: str, cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.TasksApi(client)
            subs = list(api.get_subtasks_for_task(task_id, {}))
            return ToolResult(True, f"✓ {len(subs)} subtasks", subs)
        except Exception as e:
            return ToolResult(False, f"✗ list_subtasks failed: {e}")

    @staticmethod
    def add_comment(task_id: str, text: str,
                    cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.StoriesApi(client)
            story = api.create_story_for_task(
                {"data": {"text": text}}, task_id, {})
            return ToolResult(True, "✓ Comment added", story)
        except Exception as e:
            return ToolResult(False, f"✗ add_comment failed: {e}")

    @staticmethod
    def list_comments(task_id: str, cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.StoriesApi(client)
            stories = list(api.get_stories_for_task(task_id, {}))
            comments = [s for s in stories
                        if s.get("type") == "comment"]
            return ToolResult(True, f"✓ {len(comments)} comments", comments)
        except Exception as e:
            return ToolResult(False, f"✗ list_comments failed: {e}")

    @staticmethod
    def list_sections(project_id: str, cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.SectionsApi(client)
            secs = list(api.get_sections_for_project(project_id, {}))
            return ToolResult(True, f"✓ {len(secs)} sections", secs)
        except Exception as e:
            return ToolResult(False, f"✗ list_sections failed: {e}")

    @staticmethod
    def create_section(project_id: str, name: str,
                       cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.SectionsApi(client)
            sec = api.create_section_for_project(
                {"data": {"name": name}}, project_id, {})
            return ToolResult(True, f"✓ Section created: {name}", sec)
        except Exception as e:
            return ToolResult(False, f"✗ create_section failed: {e}")

    @staticmethod
    def move_task_to_section(task_id: str, section_id: str,
                              cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.SectionsApi(client)
            api.add_task_for_section(
                {"data": {"task": task_id}}, section_id, {})
            return ToolResult(True, f"✓ Task moved to section")
        except Exception as e:
            return ToolResult(False, f"✗ move_task_to_section failed: {e}")

    @staticmethod
    def list_tags(workspace_id: str, cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.TagsApi(client)
            tags = list(api.get_tags_for_workspace(workspace_id, {}))
            return ToolResult(True, f"✓ {len(tags)} tags", tags)
        except Exception as e:
            return ToolResult(False, f"✗ list_tags failed: {e}")

    @staticmethod
    def add_tag_to_task(task_id: str, tag_id: str,
                        cred_key: str = "asana") -> ToolResult:
        try:
            import asana
            client = AsanaTool._client(cred_key)
            api = asana.TasksApi(client)
            api.add_tag_for_task({"data": {"tag": tag_id}}, task_id, {})
            return ToolResult(True, f"✓ Tag added to task")
        except Exception as e:
            return ToolResult(False, f"✗ add_tag_to_task failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 5. TrelloTool
# ═════════════════════════════════════════════════════════════════════════════

class TrelloTool:
    name = "trello"
    description = (
        "Trello board management — boards, lists, cards, checklists, "
        "labels, members, comments, and attachments"
    )
    use = ("""
Name of Tool: TrelloTool

Purpose of Tool:
The TrelloTool is a streamlined Python wrapper around the Trello REST API (v1). It abstracts HTTP requests 
and authorization configuration parameters to expose clean, synchronous static methods for managing Kanban-style 
project ecosystems. The tool maps operations cleanly across Trello's primary structural layers—boards, lists, 
cards, checklists, comments, attachments, membership states, and classification labels. Every interaction automatically 
resolves system authentication fields via `CredStore` and reports transaction statuses inside a standardized `ToolResult` container.

Methods:
- list_boards: Returns summary profiles for all workspace boards accessible by a target member.
- get_board: Resolves structural properties and unique variable states for a target board.
- create_board: Provisions a fresh board canvas workspace, optionally pre-seeded with target operational default columns.
- list_lists: Extracts the pipeline column nodes mapped inside an explicit board interface.
- create_list: Spawns an isolated vertical phase lane or column category header at a target board coordinate.
- archive_list: Toggles the closed status flag to move a targeted tracking pipeline list into workspace archives.
- list_cards: Polls active work tokens across list canvas elements or wide parent board views.
- get_card: Fetches granular variable configurations, data links, and description properties mapping a specific ticket.
- create_card: Injects a brand new task card record directly into a specified pipeline tracking list lane.
- update_card: Dispatches partial patch property modifications across generic field elements on an active card.
- move_card: Relocates an execution ticket card laterally into an alternative structural processing list column.
- archive_card: Flags a target task node as closed to remove it from live dashboard lists.
- add_checklist: Attaches discrete checklist blocks containing multiple sub-tier item actions to a parent card.
- check_checklist_item: Modifies individual checkbox states within a nested task card checklist collection.
- add_comment: Posts text logs or discussion stream threads directly onto an active card's log structure.
- add_attachment: Uploads local asset binary records or binds network resource URLs to a target task card.
- list_members: Resolves collaborator membership arrays linked directly with a board workspace context.
- add_member: Welcomes a fresh collaborator into a board workspace cluster via email configuration routes.
- create_label: Declares specialized metadata taxonomy tokens and chips inside a parent board configuration.
- add_label_to_card: Attaches an indexing taxonomy label element directly onto a target execution card.

How to use Tool Methods:

1. list_boards:
   - Purpose: Polls active boards belonging to a specified collaborator identity string.
   - Arguments:
     a) member_id: str (default: "me") - Target collaborator ID code or alias token.
     b) cred_key: str (default: "trello") - System integration lookup validation profile key.
   - Returns: ToolResult packing dictionaries tracking available workspace board architectures.
   - How to call: TrelloTool.list_boards(member_id="user_id_123")

2. get_board:
   - Purpose: Exposes exact internal settings data, descriptions, and state values for a target board registry.
   - Arguments:
     a) board_id: str - Target identification system string mapping an active board entry (required).
     b) cred_key: str (default: "trello") - Secret vault entry configuration lookup path locator.
   - Returns: ToolResult matching the returned JSON schema definitions from the target board node.
   - How to call: TrelloTool.get_board(board_id="board_xyz_789")

3. create_board:
   - Purpose: Registers a completely new primary board canvas frame into the user's active workspace.
   - Arguments:
     a) name: str - Target title descriptor labeling the fresh board interface (required).
     b) desc: str (default: "") - Core functional summary tracking the goals of the board.
     c) default_lists: bool (default: True) - Toggles pre-populating standard To Do/Doing/Done column lanes.
     d) cred_key: str (default: "trello") - Security channel identity integration validation profile.
   - Returns: ToolResult logging execution successes and provisioning parameters.
   - How to call: TrelloTool.create_board(name="Sprint Backlog 2026", desc="Engineering deliverables tracker", default_lists=False)

4. list_lists:
   - Purpose: Retrieves workflow phase columns structured horizontally inside a designated board frame.
   - Arguments:
     a) board_id: str - Unique target structural container reference identifier string (required).
     b) cred_key: str (default: "trello") - Active security client context configuration directory keys.
   - Returns: ToolResult packaging matched list columns schemas.
   - How to call: TrelloTool.list_lists(board_id="board_xyz_789")

5. create_list:
   - Purpose: appends a fresh stage column node category onto an operational project board environment.
   - Arguments:
     a) board_id: str - Destination board asset system identifier code string (required).
     b) name: str - Operational tracking lane summary header labeling the new column list (required).
     c) pos: str (default: "bottom") - Positioning grid sorting parameter ("top", "bottom", or a float index number).
     d) cred_key: str (default: "trello") - System validation account credentials pointer string.
   - Returns: ToolResult returning newly populated list structure identities.
   - How to call: TrelloTool.create_list(board_id="board_xyz_789", name="Code Review Phase", pos="top")

6. archive_list:
   - Purpose: Cleans up the workspace board view by shifting an entire column lane out of active layouts.
   - Arguments:
     a) list_id: str - Target lane mapping system location indicator sequence (required).
     b) cred_key: str (default: "trello") - Central authorization profile configuration selector keys.
   - Returns: ToolResult showing transaction status confirmations.
   - How to call: TrelloTool.archive_list(list_id="list_555_abc")

7. list_cards:
   - Purpose: Gathers tracking tickets indexed inside a particular workflow list column or broad parent board.
   - Arguments:
     a) list_or_board_id: str - Base container identifier tracking either an explicit list lane or wide board structure (required).
     b) filter: str (default: "open") - Visibility query restriction rule (e.g., "open", "closed", "all").
     c) cred_key: str (default: "trello") - Core access credentials repository storage path selector.
   - Returns: ToolResult enclosing data arrays detailing matched card data nodes.
   - How to call: TrelloTool.list_cards(list_or_board_id="list_555_abc", filter="all")

8. get_card:
   - Purpose: Resolves highly complete property parameters, metadata chips, and field descriptions for a ticket.
   - Arguments:
     a) card_id: str - Alphanumeric unique platform item identity code tracker (required).
     b) cred_key: str (default: "trello") - Integration store authorization directory lookup token.
   - Returns: ToolResult detailing complete internal variable settings defining the card.
   - How to call: TrelloTool.get_card(card_id="card_999_xyz")

9. create_card:
   - Purpose: Deploys a distinct action item card directly into an existing tracking column list lane.
   - Arguments:
     a) list_id: str - Primary parent tracker line column container reference key (required).
     b) name: str - Summary caption title labeling the newly generated execution task card (required).
     c) desc: str (default: "") - Descriptive documentation text reproduction logs or acceptance criteria.
     d) due: str (default: None) - Iso-formatted calendar target date tracking constraints (YYYY-MM-DDTHH:MM:SSZ).
     e) labels: list (default: None) - Array collection pooling target classification label ID string keys.
     f) members: list (default: None) - Array sequence collecting assigned engineer profile tracking codes.
     g) attachments: list (default: None) - String array listing initial resource URLs to fetch and link.
     h) cred_key: str (default: "trello") - Security channel connection endpoint key profile tags.
   - Returns: ToolResult tracking property responses validating card injection.
   - How to call: TrelloTool.create_card(list_id="list_555_abc", name="Resolve API Leak", desc="Patch memory logs immediately")

10. update_card:
    - Purpose: Patches arbitrary field definitions across an existing project tracking card record.
    - Arguments:
      a) id: str - Unique global node tracker asset identity code string (required).
      b) data: dict - Map definitions containing specific property parameters values to update (required).
      c) cred_key: str (default: "trello") - Internal database authentication channel access keys profile.
    - Returns: ToolResult packaging full return structures matching mutated variables.
    - How to call: TrelloTool.update_card(id="card_999_xyz", data={"desc": "Updated acceptance criteria logs."})

11. move_card:
    - Purpose: Transitions a single work ticket horizontally into an alternative workspace column status lane.
    - Arguments:
      a) card_id: str - Core individual tracking card asset lookup sequence code (required).
      b) list_id: str - Target destination pipeline list layout framework reference key (required).
      c) cred_key: str (default: "trello") - Validation secure storage integration registry profile index.
    - Returns: ToolResult tracking state override update confirmations.
    - How to call: TrelloTool.move_card(card_id="card_999_xyz", list_id="list_777_completed")

12. archive_card:
    - Purpose: Removes an active card from project canvas pipelines without deleting raw data logs permanently.
    - Arguments:
      a) card_id: str - Target task global item reference verification identification string (required).
      b) cred_key: str (default: "trello") - Vault repository security credential registry pointers.
    - Returns: ToolResult evaluating successful transition changes.
    - How to call: TrelloTool.archive_card(card_id="card_999_xyz")

13. add_checklist:
    - Purpose: Pins a fresh sub-tier tracking list framework container onto an explicit task module card.
    - Arguments:
      a) card_id: str - Destination tracking card element instance validation key sequence (required).
      b) name: str - Section heading header classifying sub-tier checklist expectations (required).
      c) items: list (default: None) - String array containing title texts for individual checkboxes to instantiate.
      d) cred_key: str (default: "trello") - Corporate connection authorization workspace key profiles store indicators.
    - Returns: ToolResult logging the generated output asset attributes tracking codes.
    - How to call: TrelloTool.add_checklist(card_id="card_999_xyz", name="QA Verification Blocks", items=["Test Edge Cases", "Validate schema"])

14. check_checklist_item:
    - Purpose: Toggles completion states for granular checkboxes structured inside nested task checklists.
    - Arguments:
      a) card_id: str - Base parent node ticket verification container path code block (required).
      b) checklist_id: str - Nested checklist framework asset grouping tracking directory lookup key (required).
      c) item_id: str - Absolute checkbox node structural reference token sequence (required).
      d) checked: bool (default: True) - State flag setting item status to 'complete' if True or 'incomplete' if False.
      d) cred_key: str (default: "trello") - Verification key data location pointers configuration mapping.
    - Returns: ToolResult mapping successful completion status logging tracks.
    - How to call: TrelloTool.check_checklist_item(card_id="card_999_xyz", checklist_id="cl_111", item_id="item_222", checked=True)

15. add_comment:
    - Purpose: Appends dialogue remarks directly inside the asynchronous activity stream on a ticket asset card.
    - Arguments:
      a) card_id: str - Target dialogue logging task document container identifier node string (required).
      b) text: str - Main textual communication note body text formatting status statements (required).
      c) cred_key: str (default: "trello") - Secure corporate interface server authorization validation details.
    - Returns: ToolResult confirming dialogue track mutation results schemas.
    - How to call: TrelloTool.add_comment(card_id="card_999_xyz", text="Hotfix deployed to staging. Testing confirms fix.")

16. add_attachment:
    - Purpose: Uploads local disk binary files or attaches external hyperlink reference paths directly onto a card file asset.
    - Arguments:
      a) card_id: str - Target task container system structural reference identification coordinate (required).
      b) url_or_path: str - Absolute network resource path hyperlink or local operating system disk path lookup string (required).
      c) name: str (default: "") - Visual descriptor alias labeling the resource inside the file tray context view.
      d) cred_key: str (default: "trello") - Active credentials profile store directory location parameters.
    - Returns: ToolResult validating transmission logs payload metadata maps.
    - How to call: TrelloTool.add_attachment(card_id="card_999_xyz", url_or_path="./logs/error_stack.txt", name="Crash Log Trace")

17. list_members:
    - Purpose: Queries identity maps tracking profiles validly attached onto a specific board environment setup.
    - Arguments:
      a) board_id: str - Base platform framework layout identifier path verification block code (required).
      b) cred_key: str (default: "trello") - Authorization vault system index selector tracking directories.
    - Returns: ToolResult packaging matched engineer profiles array sets data maps.
    - How to call: TrelloTool.list_members(board_id="board_xyz_789")

18. add_member:
    - Purpose: Attaches additional team collaborators directly onto an active board canvas infrastructure ecosystem.
    - Arguments:
      a) board_id: str - Target design infrastructure workspace container reference key token (required).
      b) email: str - Target corporate inbox communications identity string mapping a developer account (required).
      c) type: str (default: "normal") - System access permission role tier settings ("admin", "normal", "observer").
      d) cred_key: str (default: "trello") - Network endpoints validation verification access profiles mapping.
    - Returns: ToolResult tracking membership provisioning response statuses.
    - How to call: TrelloTool.add_member(board_id="board_xyz_789", email="engineer@company.com", type="normal")

19. create_label:
    - Purpose: Declares fresh cross-card classification chips and tags inside a board's global sorting palette.
    - Arguments:
      a) board_id: str - Targeted project board setup container system tracking layout identifier (required).
      b) name: str - Text phrase distinguishing taxonomy properties labeling the new chip keyword (required).
      c) color: str - Color name keyword identifying workspace visual layout accent lanes (e.g., "red", "blue", "orange").
      d) cred_key: str (default: "trello") - Identity interface verification workspace repository database credentials access keys.
    - Returns: ToolResult mapping generated label parameters metadata structures.
    - How to call: TrelloTool.create_label(board_id="board_xyz_789", name="Blocker Risk", color="red")

20. add_label_to_card:
    - Purpose: Chains a pre-existing taxonomy sorting keyword or categorization chip label onto a running card.
    - Arguments:
      a) card_id: str - Destination tracking card item system locator path identifier code sequence (required).
      b) label_id: str - Targeted cross-project triage classification asset reference code token (required).
      c) cred_key: str (default: "trello") - Secure credentials storage vault database registry lookup values.
    - Returns: ToolResult checking return property execution results logs.
    - How to call: TrelloTool.add_label_to_card(card_id="card_999_xyz", label_id="label_id_000")
""")
       
    @staticmethod
    def _api(method: str, path: str, cred_key: str = "trello",
             **kwargs) -> Any:
        import requests
        creds = CredStore.load(cred_key)
        key = creds.get("api_key", "")
        token = creds.get("token", "")
        if not key or not token:
            raise ValueError("No Trello credentials. Store 'api_key' and 'token' under 'trello'.")
        url = f"https://api.trello.com/1/{path.lstrip('/')}"
        params = kwargs.pop("params", {})
        params.update({"key": key, "token": token})
        fn = getattr(requests, method.lower())
        resp = fn(url, params=params, timeout=20, **kwargs)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    @staticmethod
    def list_boards(member_id: str = "me",
                    cred_key: str = "trello") -> ToolResult:
        try:
            boards = TrelloTool._api(
                "get", f"members/{member_id}/boards",
                cred_key,
                params={"fields": "id,name,desc,url,closed"})
            return ToolResult(True, f"✓ {len(boards)} boards", boards)
        except Exception as e:
            return ToolResult(False, f"✗ list_boards failed: {e}")

    @staticmethod
    def get_board(board_id: str, cred_key: str = "trello") -> ToolResult:
        try:
            board = TrelloTool._api("get", f"boards/{board_id}", cred_key)
            return ToolResult(True, "✓ Board retrieved", board)
        except Exception as e:
            return ToolResult(False, f"✗ get_board failed: {e}")

    @staticmethod
    def create_board(name: str, desc: str = "",
                     default_lists: bool = True,
                     cred_key: str = "trello") -> ToolResult:
        try:
            board = TrelloTool._api(
                "post", "boards", cred_key,
                json={"name": name, "desc": desc,
                      "defaultLists": default_lists})
            return ToolResult(True, f"✓ Board created: {board.get('id')}", board)
        except Exception as e:
            return ToolResult(False, f"✗ create_board failed: {e}")

    @staticmethod
    def list_lists(board_id: str, cred_key: str = "trello") -> ToolResult:
        try:
            lists = TrelloTool._api("get", f"boards/{board_id}/lists",
                                    cred_key)
            return ToolResult(True, f"✓ {len(lists)} lists", lists)
        except Exception as e:
            return ToolResult(False, f"✗ list_lists failed: {e}")

    @staticmethod
    def create_list(board_id: str, name: str, pos: str = "bottom",
                    cred_key: str = "trello") -> ToolResult:
        try:
            lst = TrelloTool._api(
                "post", "lists", cred_key,
                json={"name": name, "idBoard": board_id, "pos": pos})
            return ToolResult(True, f"✓ List created: {lst.get('id')}", lst)
        except Exception as e:
            return ToolResult(False, f"✗ create_list failed: {e}")

    @staticmethod
    def archive_list(list_id: str, cred_key: str = "trello") -> ToolResult:
        try:
            TrelloTool._api("put", f"lists/{list_id}/closed", cred_key,
                            json={"value": True})
            return ToolResult(True, f"✓ List archived: {list_id}")
        except Exception as e:
            return ToolResult(False, f"✗ archive_list failed: {e}")

    @staticmethod
    def list_cards(list_or_board_id: str, filter: str = "open",
                   cred_key: str = "trello") -> ToolResult:
        try:
            # Try list first, fall back to board
            try:
                cards = TrelloTool._api(
                    "get", f"lists/{list_or_board_id}/cards",
                    cred_key, params={"filter": filter})
            except Exception:
                cards = TrelloTool._api(
                    "get", f"boards/{list_or_board_id}/cards",
                    cred_key, params={"filter": filter})
            return ToolResult(True, f"✓ {len(cards)} cards", cards)
        except Exception as e:
            return ToolResult(False, f"✗ list_cards failed: {e}")

    @staticmethod
    def get_card(card_id: str, cred_key: str = "trello") -> ToolResult:
        try:
            card = TrelloTool._api("get", f"cards/{card_id}", cred_key)
            return ToolResult(True, "✓ Card retrieved", card)
        except Exception as e:
            return ToolResult(False, f"✗ get_card failed: {e}")

    @staticmethod
    def create_card(list_id: str, name: str, desc: str = "",
                    due: str = None, labels: list = None,
                    members: list = None, attachments: list = None,
                    cred_key: str = "trello") -> ToolResult:
        try:
            body: dict = {"idList": list_id, "name": name, "desc": desc}
            if due:
                body["due"] = due
            if labels:
                body["idLabels"] = labels
            if members:
                body["idMembers"] = members
            card = TrelloTool._api("post", "cards", cred_key, json=body)
            if attachments:
                for att in attachments:
                    TrelloTool._api(
                        "post", f"cards/{card['id']}/attachments",
                        cred_key, json={"url": att, "name": att})
            return ToolResult(True, f"✓ Card created: {card.get('id')}", card)
        except Exception as e:
            return ToolResult(False, f"✗ create_card failed: {e}")

    @staticmethod
    def update_card(id: str, data: dict,
                    cred_key: str = "trello") -> ToolResult:
        try:
            card = TrelloTool._api("put", f"cards/{id}", cred_key, json=data)
            return ToolResult(True, "✓ Card updated", card)
        except Exception as e:
            return ToolResult(False, f"✗ update_card failed: {e}")

    @staticmethod
    def move_card(card_id: str, list_id: str,
                  cred_key: str = "trello") -> ToolResult:
        return TrelloTool.update_card(card_id, {"idList": list_id}, cred_key)

    @staticmethod
    def archive_card(card_id: str, cred_key: str = "trello") -> ToolResult:
        return TrelloTool.update_card(card_id, {"closed": True}, cred_key)

    @staticmethod
    def add_checklist(card_id: str, name: str, items: list = None,
                      cred_key: str = "trello") -> ToolResult:
        try:
            cl = TrelloTool._api(
                "post", "checklists", cred_key,
                json={"idCard": card_id, "name": name})
            cl_id = cl["id"]
            for item in (items or []):
                TrelloTool._api(
                    "post", f"checklists/{cl_id}/checkItems",
                    cred_key, json={"name": item})
            return ToolResult(True, f"✓ Checklist '{name}' added", cl)
        except Exception as e:
            return ToolResult(False, f"✗ add_checklist failed: {e}")

    @staticmethod
    def check_checklist_item(card_id: str, checklist_id: str,
                              item_id: str, checked: bool = True,
                              cred_key: str = "trello") -> ToolResult:
        try:
            state = "complete" if checked else "incomplete"
            TrelloTool._api(
                "put",
                f"cards/{card_id}/checkItem/{item_id}",
                cred_key, json={"state": state})
            return ToolResult(True, f"✓ Item marked {state}")
        except Exception as e:
            return ToolResult(False, f"✗ check_checklist_item failed: {e}")

    @staticmethod
    def add_comment(card_id: str, text: str,
                    cred_key: str = "trello") -> ToolResult:
        try:
            resp = TrelloTool._api(
                "post", f"cards/{card_id}/actions/comments",
                cred_key, json={"text": text})
            return ToolResult(True, "✓ Comment added", resp)
        except Exception as e:
            return ToolResult(False, f"✗ add_comment failed: {e}")

    @staticmethod
    def add_attachment(card_id: str, url_or_path: str,
                       name: str = "", cred_key: str = "trello") -> ToolResult:
        try:
            import requests as req
            p = Path(url_or_path)
            creds = CredStore.load(cred_key)
            key = creds.get("api_key", "")
            token_val = creds.get("token", "")
            url = f"https://api.trello.com/1/cards/{card_id}/attachments"
            if p.exists():
                with open(url_or_path, "rb") as f:
                    resp = req.post(url,
                                    params={"key": key, "token": token_val},
                                    files={"file": (name or p.name, f)},
                                    timeout=30)
            else:
                resp = req.post(url,
                                params={"key": key, "token": token_val},
                                json={"url": url_or_path, "name": name},
                                timeout=20)
            resp.raise_for_status()
            return ToolResult(True, "✓ Attachment added", resp.json())
        except Exception as e:
            return ToolResult(False, f"✗ add_attachment failed: {e}")

    @staticmethod
    def list_members(board_id: str, cred_key: str = "trello") -> ToolResult:
        try:
            members = TrelloTool._api(
                "get", f"boards/{board_id}/members", cred_key)
            return ToolResult(True, f"✓ {len(members)} members", members)
        except Exception as e:
            return ToolResult(False, f"✗ list_members failed: {e}")

    @staticmethod
    def add_member(board_id: str, email: str, type: str = "normal",
                   cred_key: str = "trello") -> ToolResult:
        try:
            resp = TrelloTool._api(
                "put", f"boards/{board_id}/members", cred_key,
                json={"email": email, "type": type})
            return ToolResult(True, f"✓ Member {email} added", resp)
        except Exception as e:
            return ToolResult(False, f"✗ add_member failed: {e}")

    @staticmethod
    def create_label(board_id: str, name: str, color: str,
                     cred_key: str = "trello") -> ToolResult:
        try:
            label = TrelloTool._api(
                "post", "labels", cred_key,
                json={"name": name, "color": color,
                      "idBoard": board_id})
            return ToolResult(True, f"✓ Label created: {label.get('id')}", label)
        except Exception as e:
            return ToolResult(False, f"✗ create_label failed: {e}")

    @staticmethod
    def add_label_to_card(card_id: str, label_id: str,
                           cred_key: str = "trello") -> ToolResult:
        try:
            TrelloTool._api(
                "post", f"cards/{card_id}/idLabels",
                cred_key, json={"value": label_id})
            return ToolResult(True, "✓ Label added to card")
        except Exception as e:
            return ToolResult(False, f"✗ add_label_to_card failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 6. ClickUpTool
# ═════════════════════════════════════════════════════════════════════════════

class ClickUpTool:
    name = "clickup"
    description = (
        "ClickUp workspace management — spaces, folders, lists, tasks, "
        "comments, checklists, time tracking, and views"
    )
    use = ("""
Name of Tool: ClickUpTool

Purpose of Tool:
The ClickUpTool is a robust Python programmatic wrapper designed to interface with the ClickUp REST API (v2). 
It encapsulates the underlying connection protocols and simplifies workspace hierarchy management by exposing 
clean methods to interact with spaces, folders, lists, and tasks. Beyond basic CRUD operations, it provides 
integrated productivity utilities including time-tracking mechanics, collaborative comment injection streams, 
checklist provisioning, and layout data rendering workflows across custom views.

Methods:
- list_spaces: Pulls unarchived workplace environment spaces mapped under a target team workspace account ID.
- list_folders: Queries and builds a list collection of directory folders organized within a single parent space.
- list_lists: Retrieves task lists configured inside a given folder directory structure.
- get_tasks: Queries tasks localized inside an active list, with selective server-side status and assignee sorting.
- get_task: Fetches detailed task record attributes and field schemas mapped to a unique task token ID.
- create_task: Deploys a brand new action ticket into a target tracking column canvas list.
- update_task: Mutates precise key-value attributes on a target task across a specified JSON field map payload.
- delete_task: Drops a targeted task item entry directly out of the active operational workspace.
- set_task_status: Alters the life-cycle stage text identifier tracking the progress of an explicit task.
- add_comment: Posts collaborative messaging items directly onto a targeted task profile's commentary trail.
- list_comments: Gathers historical message logs from the activity string associated with a single task.
- create_checklist: Provisions an empty checkbox structural cluster sub-group onto an active task ticket.
- add_checklist_item: Injects precise single-line checkbox item markers into a designated parent sub-checklist.
- track_time: Commits localized duration time-tracking blocks into the ledger metrics profile of a target task.
- get_time_entries: Fetches explicit historical labor logs tracked and registered inside a target task identity.
- list_views: Pulls alternative organizational interface layout views registered over an individual project list.
- get_view_tasks: Resolves task elements currently being monitored from inside a target custom view matrix.

How to use Tool Methods:

1. list_spaces:
   - Purpose: Lists all unarchived spaces available to the defined team identity profile.
   - Arguments:
     a) team_id: str - Unique organization workplace identifier target code (required).
     b) cred_key: str (default: "clickup") - Target database routing entry string tracking local API tokens.
   - Returns: ToolResult container resolving dictionaries matching live workspace environment entries.
   - How to call: ClickUpTool.list_spaces(team_id="1234567")

2. list_folders:
   - Purpose: Retrieves all unarchived folders configured inside a targeted space.
   - Arguments:
     a) space_id: str - The specific target space identification reference string (required).
     b) cred_key: str (default: "clickup") - Registry look-up parameter indexing secure access keys.
   - Returns: ToolResult mapping active container profiles linked to the destination directory.
   - How to call: ClickUpTool.list_folders(space_id="space_abc_999")

3. list_lists:
   - Purpose: Collects active project task columns or sub-lists running inside a folder.
   - Arguments:
     a) folder_id: str - Unique identification number string targeting a parent directory container (required).
     b) cred_key: str (default: "clickup") - Secure credentials storage validation dictionary indicator.
   - Returns: ToolResult holding structural payload details mapping out all target lists.
   - How to call: ClickUpTool.list_lists(folder_id="folder_555666")

4. get_tasks:
   - Purpose: Polls and queries task indices out of a single collection list with selective parameter logic.
   - Arguments:
     a) list_id: str - Location coordinate mapping the parent list node container (required).
     b) assignees: list (default: None) - Array collecting target user identification ID sequences.
     c) statuses: list (default: None) - Limits retrieved records to items matching structural tier names.
     d) due_date: str (default: None) - Boolean filter target string shifting timeline evaluations.
     e) page: int (default: 0) - Pagination index tracking the continuous scroll layout matrix.
     f) cred_key: str (default: "clickup") - Primary secure integration lookup pointer value string.
   - Returns: ToolResult carrying filtered data nodes representing active task states.
   - How to call: ClickUpTool.get_tasks(list_id="list_7890", statuses=["In Progress", "Review"])

5. get_task:
   - Purpose: Resolves exact comprehensive data attributes detailing a specific system task.
   - Arguments:
     a) task_id: str - Core targeted task element routing index identification value (required).
     b) cred_key: str (default: "clickup") - Target token credentials mapping vault keys directory.
   - Returns: ToolResult detailing standard and custom parameters attached to the task target.
   - How to call: ClickUpTool.get_task(task_id="task_click_55a")

6. create_task:
   - Purpose: Injects an isolated task entry directly inside a specified production list path.
   - Arguments:
     a) list_id: str - Unique target list destination identification index code (required).
     b) name: str - Text summary header defining the task title string value (required).
     c) description: str (default: "") - Extended instruction detail block or markdown formatting context notes.
     d) assignees: list (default: None) - User ID keys array mapping accounts targeted for completion.
     e) status: str (default: None) - Context progress tier labels string token (e.g., "in progress").
     f) priority: int (default: None) - System importance weight values grading from 1 (Urgent) through 4 (Low).
     g) due_date: str (default: None) - ISO standard timestamp format string representing completion targets.
     h) tags: list (default: None) - String tokens array applying organizational categorization variables.
     i) cred_key: str (default: "clickup") - Registry configuration parameter indexing standard security keys.
   - Returns: ToolResult evaluating creation states alongside tracking copies of the server-side generated map parameters.
   - How to call: ClickUpTool.create_task(list_id="9001", name="Deploy API Gateway Patch", priority=1, status="To Do")

7. update_task:
   - Purpose: Commits raw property modifications across arbitrary target field keys using dictionary payloads.
   - Arguments:
     a) id: str - Unique system identification tracking string pointing to the target task (required).
     b) data: dict - Structural data map organizing property alterations (required).
     c) cred_key: str (default: "clickup") - Data vault token identification handle indicator.
   - Returns: ToolResult enclosing server-returned updated object attributes profiles.
   - How to call: ClickUpTool.update_task(id="task_x12", data={"description": "Updated scope guidelines"})

8. delete_task:
   - Purpose: Destroys a target task instance and drops it from the active workspace interface.
   - Arguments:
     a) id: str - Unique task signature code string targeting deletion (required).
     b) cred_key: str (default: "clickup") - Authentication security reference dictionary router key.
   - Returns: ToolResult reporting explicit execution successes or configuration failures.
   - How to call: ClickUpTool.delete_task(id="task_z99")

9. set_task_status:
   - Purpose: Shifts a task's development lifecycle stage using an inline string shortcut wrapper.
   - Arguments:
     a) id: str - Target task unique string sequence signature key (required).
     b) status: str - Destination tracking phase name token string value (required).
     c) cred_key: str (default: "clickup") - Target core client access vault mapping indicator.
   - Returns: ToolResult verifying completion actions alongside execution payload metadata maps.
   - How to call: ClickUpTool.set_task_status(id="task_abc11", status="Complete")

10. add_comment:
    - Purpose: Attaches text message communication objects onto a targeted task profile.
    - Arguments:
      a) task_id: str - target project task identity identifier code string (required).
      b) comment_text: str - Core written text payload forming the communication post body (required).
      c) notify_all: bool (default: False) - Dispatches alerts targeting every watcher attached to the file.
      d) cred_key: str (default: "clickup") - Connection routing security token profile directory indicator.
    - Returns: ToolResult confirming messaging deployment states over the network interface.
    - How to call: ClickUpTool.add_comment(task_id="task_j33", comment_text="PR approved, merging now.", notify_all=True)

11. list_comments:
    - Purpose: Pulls the historical text dialogue ledger belonging to a designated task profile.
    - Arguments:
      a) task_id: str - target workspace task reference string index tag (required).
      b) cred_key: str (default: "clickup") - Secure token repository destination pointer registry map.
    - Returns: ToolResult housing lists tracking individual message objects and authors.
    - How to call: ClickUpTool.list_comments(task_id="task_y44")

12. create_checklist:
    - Purpose: Appends a standalone checkbox array tracking structural unit cluster onto an active task canvas.
    - Arguments:
      a) task_id: str - Destination task index location tracker code string (required).
      b) name: str - Descriptive clear structural heading tag for the custom checkbox grouping (required).
      c) cred_key: str (default: "clickup") - Core system authentication directory tracking lookup paths.
    - Returns: ToolResult embedding the full parameters dictionary describing the generated checklist container.
    - How to call: ClickUpTool.create_checklist(task_id="task_u71", name="Pre-flight Verification Steps")

13. add_checklist_item:
    - Purpose: Provisions sub-task operational single-line item points into an existing parent checklist element.
    - Arguments:
      a) checklist_id: str - target checklist instance parent reference key string (required).
      b) name: str - Summary text outlining the individual actionable checklist step item (required).
      c) assignee: str (default: None) - User signature token routing target responsibility mapping paths.
      d) cred_key: str (default: "clickup") - Client authentication credential store destination handle.
    - Returns: ToolResult logging deployment confirmations detailing newly created sub-item tracking vectors.
    - How to call: ClickUpTool.add_checklist_item(checklist_id="check_9921", name="Verify SSL cert expiration")

14. track_time:
    - Purpose: Logs a precise labor time ledger event block context onto a configured task reference tracking sheet.
    - Arguments:
      a) task_id: str - Explicit task tracking index reference code target (required).
      b) duration: int - Exact elapsed execution time value measured completely in millisecond blocks (required).
      c) start: str (default: None) - ISO string representation tracking the launch milestone of the log block.
      d) end: str (default: None) - ISO string representation tracking the close milestone of the log block.
      d) description: str (default: "") - Commentary notation outlining specific actions taken throughout the duration period.
      e) cred_key: str (default: "clickup") - Security authentication credential store destination routing handle.
    - Returns: ToolResult verifying successful record persistence alongside execution confirmations.
    - How to call: ClickUpTool.track_time(task_id="abc888", duration=7200000, description="Debugging memory leak profiles")

15. get_time_entries:
    - Purpose: Retrieves all granular recorded durations and time logs associated with a single task file.
    - Arguments:
      a) task_id: str - Targeted project task unique tracking identification key (required).
      b) cred_key: str (default: "clickup") - Authentication security storage access lookup parameters map.
    - Returns: ToolResult exposing an array layout of individual duration entries and logging timestamps.
    - How to call: ClickUpTool.get_time_entries(task_id="task_w44")

16. list_views:
    - Purpose: Extracts metadata parameters identifying alternate layouts and project visualization formats configured inside a list.
    - Arguments:
      a) list_id: str - Destination project task group column list pointer string (required).
      b) cred_key: str (default: "clickup") - Core system authentication directory tracking lookup paths.
    - Returns: ToolResult summarizing functional viewing configurations like calendars, boards, or Gantt layouts.
    - How to call: ClickUpTool.list_views(list_id="list_v12")

17. get_view_tasks:
    - Purpose: Isolates and collects target active task items explicitly visible inside a configured custom framework view layout.
    - Arguments:
      a) view_id: str - Target specific interface canvas view layout index identification code string (required).
      b) cred_key: str (default: "clickup") - Target securely configured client access repository data path index.
    - Returns: ToolResult returning clean data objects cataloging the specific subsets tracked inside the targeted view block.
    - How to call: ClickUpTool.get_view_tasks(view_id="view_matrix_777")
""")
       
    @staticmethod
    def _api(method: str, path: str, cred_key: str = "clickup",
             **kwargs) -> Any:
        import requests
        token = CredStore.load(cred_key).get("api_token", "")
        if not token:
            raise ValueError("No ClickUp token. Store under 'clickup' key.")
        url = f"https://api.clickup.com/api/v2/{path.lstrip('/')}"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        fn = getattr(requests, method.lower())
        resp = fn(url, headers=headers, timeout=20, **kwargs)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    @staticmethod
    def list_spaces(team_id: str, cred_key: str = "clickup") -> ToolResult:
        try:
            data = ClickUpTool._api("get", f"team/{team_id}/space", cred_key,
                                    params={"archived": "false"})
            spaces = data.get("spaces", [])
            return ToolResult(True, f"✓ {len(spaces)} spaces", spaces)
        except Exception as e:
            return ToolResult(False, f"✗ list_spaces failed: {e}")

    @staticmethod
    def list_folders(space_id: str, cred_key: str = "clickup") -> ToolResult:
        try:
            data = ClickUpTool._api("get", f"space/{space_id}/folder",
                                    cred_key, params={"archived": "false"})
            folders = data.get("folders", [])
            return ToolResult(True, f"✓ {len(folders)} folders", folders)
        except Exception as e:
            return ToolResult(False, f"✗ list_folders failed: {e}")

    @staticmethod
    def list_lists(folder_id: str, cred_key: str = "clickup") -> ToolResult:
        try:
            data = ClickUpTool._api("get", f"folder/{folder_id}/list",
                                    cred_key, params={"archived": "false"})
            lists = data.get("lists", [])
            return ToolResult(True, f"✓ {len(lists)} lists", lists)
        except Exception as e:
            return ToolResult(False, f"✗ list_lists failed: {e}")

    @staticmethod
    def get_tasks(list_id: str, assignees: list = None,
                  statuses: list = None, due_date: str = None,
                  page: int = 0, cred_key: str = "clickup") -> ToolResult:
        try:
            params: dict = {"page": page}
            if assignees:
                params["assignees[]"] = assignees
            if statuses:
                params["statuses[]"] = statuses
            if due_date:
                params["due_date_gt"] = 0
            data = ClickUpTool._api("get", f"list/{list_id}/task",
                                    cred_key, params=params)
            tasks = data.get("tasks", [])
            return ToolResult(True, f"✓ {len(tasks)} tasks", tasks)
        except Exception as e:
            return ToolResult(False, f"✗ get_tasks failed: {e}")

    @staticmethod
    def get_task(task_id: str, cred_key: str = "clickup") -> ToolResult:
        try:
            task = ClickUpTool._api("get", f"task/{task_id}", cred_key)
            return ToolResult(True, "✓ Task retrieved", task)
        except Exception as e:
            return ToolResult(False, f"✗ get_task failed: {e}")

    @staticmethod
    def create_task(list_id: str, name: str, description: str = "",
                    assignees: list = None, status: str = None,
                    priority: int = None, due_date: str = None,
                    tags: list = None, cred_key: str = "clickup") -> ToolResult:
        try:
            body: dict = {"name": name, "description": description}
            if assignees:
                body["assignees"] = assignees
            if status:
                body["status"] = status
            if priority is not None:
                body["priority"] = priority
            if due_date:
                # convert ISO date to ms timestamp
                dt = datetime.fromisoformat(due_date)
                body["due_date"] = int(dt.timestamp() * 1000)
            if tags:
                body["tags"] = tags
            task = ClickUpTool._api("post", f"list/{list_id}/task",
                                    cred_key, json=body)
            return ToolResult(True, f"✓ Task created: {task.get('id')}", task)
        except Exception as e:
            return ToolResult(False, f"✗ create_task failed: {e}")

    @staticmethod
    def update_task(id: str, data: dict,
                    cred_key: str = "clickup") -> ToolResult:
        try:
            task = ClickUpTool._api("put", f"task/{id}", cred_key, json=data)
            return ToolResult(True, "✓ Task updated", task)
        except Exception as e:
            return ToolResult(False, f"✗ update_task failed: {e}")

    @staticmethod
    def delete_task(id: str, cred_key: str = "clickup") -> ToolResult:
        try:
            ClickUpTool._api("delete", f"task/{id}", cred_key)
            return ToolResult(True, f"✓ Task deleted: {id}")
        except Exception as e:
            return ToolResult(False, f"✗ delete_task failed: {e}")

    @staticmethod
    def set_task_status(id: str, status: str,
                        cred_key: str = "clickup") -> ToolResult:
        return ClickUpTool.update_task(id, {"status": status}, cred_key)

    @staticmethod
    def add_comment(task_id: str, comment_text: str,
                    notify_all: bool = False,
                    cred_key: str = "clickup") -> ToolResult:
        try:
            resp = ClickUpTool._api(
                "post", f"task/{task_id}/comment", cred_key,
                json={"comment_text": comment_text,
                      "notify_all": notify_all})
            return ToolResult(True, "✓ Comment added", resp)
        except Exception as e:
            return ToolResult(False, f"✗ add_comment failed: {e}")

    @staticmethod
    def list_comments(task_id: str, cred_key: str = "clickup") -> ToolResult:
        try:
            data = ClickUpTool._api("get", f"task/{task_id}/comment", cred_key)
            comments = data.get("comments", [])
            return ToolResult(True, f"✓ {len(comments)} comments", comments)
        except Exception as e:
            return ToolResult(False, f"✗ list_comments failed: {e}")

    @staticmethod
    def create_checklist(task_id: str, name: str,
                         cred_key: str = "clickup") -> ToolResult:
        try:
            resp = ClickUpTool._api(
                "post", f"task/{task_id}/checklist",
                cred_key, json={"name": name})
            return ToolResult(True, f"✓ Checklist created",
                              resp.get("checklist"))
        except Exception as e:
            return ToolResult(False, f"✗ create_checklist failed: {e}")

    @staticmethod
    def add_checklist_item(checklist_id: str, name: str,
                           assignee: str = None,
                           cred_key: str = "clickup") -> ToolResult:
        try:
            body: dict = {"name": name}
            if assignee:
                body["assignee"] = assignee
            resp = ClickUpTool._api(
                "post", f"checklist/{checklist_id}/checklist_item",
                cred_key, json=body)
            return ToolResult(True, "✓ Checklist item added", resp)
        except Exception as e:
            return ToolResult(False, f"✗ add_checklist_item failed: {e}")

    @staticmethod
    def track_time(task_id: str, duration: int,
                   start: str = None, end: str = None,
                   description: str = "",
                   cred_key: str = "clickup") -> ToolResult:
        try:
            body: dict = {"duration": duration, "description": description}
            if start:
                dt = datetime.fromisoformat(start)
                body["start"] = int(dt.timestamp() * 1000)
            if end:
                dt = datetime.fromisoformat(end)
                body["end"] = int(dt.timestamp() * 1000)
            resp = ClickUpTool._api(
                "post", f"task/{task_id}/time", cred_key, json=body)
            return ToolResult(True, "✓ Time tracked", resp)
        except Exception as e:
            return ToolResult(False, f"✗ track_time failed: {e}")

    @staticmethod
    def get_time_entries(task_id: str, cred_key: str = "clickup") -> ToolResult:
        try:
            data = ClickUpTool._api("get", f"task/{task_id}/time", cred_key)
            entries = data.get("data", [])
            return ToolResult(True, f"✓ {len(entries)} time entries", entries)
        except Exception as e:
            return ToolResult(False, f"✗ get_time_entries failed: {e}")

    @staticmethod
    def list_views(list_id: str, cred_key: str = "clickup") -> ToolResult:
        try:
            data = ClickUpTool._api("get", f"list/{list_id}/view", cred_key)
            views = data.get("views", [])
            return ToolResult(True, f"✓ {len(views)} views", views)
        except Exception as e:
            return ToolResult(False, f"✗ list_views failed: {e}")

    @staticmethod
    def get_view_tasks(view_id: str, cred_key: str = "clickup") -> ToolResult:
        try:
            data = ClickUpTool._api("get", f"view/{view_id}/task", cred_key)
            tasks = data.get("tasks", [])
            return ToolResult(True, f"✓ {len(tasks)} tasks in view", tasks)
        except Exception as e:
            return ToolResult(False, f"✗ get_view_tasks failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 7. TodoistTool
# ═════════════════════════════════════════════════════════════════════════════

class TodoistTool:
    name = "todoist"
    description = (
        "Todoist task and project management — projects, tasks, labels, "
        "comments, quick-add, activity log, and productivity stats"
    )
    use = ("""
Name of Tool: TodoistTool

Purpose of Tool:
The TodoistTool is a unified Python interface that interacts with the Todoist environment. 
It utilizes a hybrid infrastructure, routing basic task and project operations through the official 
Todoist Python SDK client, while offloading high-velocity natural language processing, system audit logging, 
and performance metric tracking onto direct Todoist Sync API (v9) network communication routes. 
The tool manages user workflows by handling structural project trees, task lifecycles, global context tags, 
and task discussions inside a centralized execution frame.

Methods:
- get_projects: Extracts summary configurations and color palettes defining all active project folders.
- add_project: Appends a completely fresh tracking container node into the user's project collection directory.
- update_project: Dispatches property modifications across parameter targets on a configured project tracker.
- delete_project: Purges an explicit project directory folder container along with its nested tracking lines.
- get_tasks: Queries open task components using various filtering arrays, label flags, or urgency variables.
- add_task: Injects an explicit action task ticket token directly into a designated target project directory.
- update_task: Alters configuration values mapping a specific task identity record within the active queue.
- complete_task: Resolves and closes an active task context tracking record, clearing it from active boards.
- delete_task: Permanently drops an individual task instance record out of the active user database workspace.
- reopen_task: Restores a previously finalized task back into the operational active project processing queue.
- get_comments: Resolves dialogue log lines posted inside a specific task item's communication stream.
- add_comment: Attaches fresh documentation annotations or asset objects onto an active target task.
- get_labels: Returns a structured summary listing of all user-defined metadata classification tags.
- add_label: Provisions a global categorization index tag equipped with a distinctive interface color marker.
- quick_add: Decodes casual, natural language syntax inputs to instantly generate pre-configured task items.
- get_activity_log: Tracks historical workflow mutation logs across the organization workspace.
- get_productivity_stats: Resolves telemetry tracking data mapping user streak limits and total karma achievements.

How to use Tool Methods:

1. get_projects:
   - Purpose: Fetches metadata for all active, unarchived projects within the account workspace.
   - Arguments:
     a) cred_key: str (default: "todoist") - System validation token lookup path key.
   - Returns: ToolResult mapping active project names, matching IDs, and assigned interface colors.
   - How to call: TodoistTool.get_projects()

2. add_project:
   - Purpose: Injects a brand-new target project container or nested sub-folder into the ledger matrix.
   - Arguments:
     a) name: str - Primary visual text header title naming the project (required).
     b) color: str (default: "charcoal") - Interface custom aesthetic color label palette selection.
     c) parent_id: str (default: None) - Identity pointer string used for establishing hierarchical parent-child configurations.
     d) cred_key: str (default: "todoist") - Vault storage credential mapping target key parameter string.
   - Returns: ToolResult detailing creation confirmation alongside the resulting unique project ID sequence.
   - How to call: TodoistTool.add_project(name="Marketing Q3", color="ruby")

3. update_project:
   - Purpose: Commits direct property mutations over explicit attributes using a dynamic dictionary payload.
   - Arguments:
     a) id: str - Unique target project identity routing token index string (required).
     b) data: dict - Map schema bundling field mutations (e.g., {"name": "New Title", "color": "blue"}) (required).
     c) cred_key: str (default: "todoist") - Vault routing signature token profile indicator lookup paths.
   - Returns: ToolResult logging modification tracking confirmations.
   - How to call: TodoistTool.update_project(id="220011", data={"color": "emerald"})

4. delete_project:
   - Purpose: Destroys a targeted project directory folder block along with all associated active task line items.
   - Arguments:
     a) id: str - Unique identifier key of the targeted project item (required).
     b) cred_key: str (default: "todoist") - Connection security token profile map handle lookup index.
   - Returns: ToolResult registering successful execution actions.
   - How to call: TodoistTool.delete_project(id="220011")

5. get_tasks:
   - Purpose: Pulls filtered arrays listing currently active task items according to parameters.
   - Arguments:
     a) project_id: str (default: None) - Filters results to an isolated project directory container string.
     b) filter: str (default: None) - Advanced evaluation strings (e.g., "overdue | today", "p1 & #Work").
     c) label: str (default: None) - Isolates item lists matching a targeted categorization tag string name.
     d) priority: int (default: None) - Targets a precise urgency ranking system token scale tier from 1 to 4.
     e) cred_key: str (default: "todoist") - Target connection configuration vault directory parameter indicator.
   - Returns: ToolResult container carrying structured collections representing targeted open task records.
   - How to call: TodoistTool.get_tasks(project_id="11223344", priority=4)

6. add_task:
   - Purpose: Provisions an isolated single work ticket task tracking token directly into a designated target directory.
   - Arguments:
     a) content: str - Primary headline summary text defining the task action (required).
     b) description: str (default: "") - Extended instruction detail block or descriptive context notes data.
     c) project_id: str (default: None) - Target parent project unique tracking reference coordinate locator key.
     d) due_string: str (default: None) - Human-readable calendar timeline targets interpreter (e.g., "next Monday at 4pm").
     e) priority: int (default: 1) - Numeric urgency ranking scale level extending from 1 (lowest) to 4 (highest).
     f) labels: list (default: None) - Custom array collection assigning visual categorization tag tokens.
     g) cred_key: str (default: "todoist") - Target database routing entry string tracking local API access tokens.
   - Returns: ToolResult tracking creation states alongside the server-side generated object parameters map.
   - How to call: TodoistTool.add_task(content="Renew server certificates", due_string="tomorrow at midnight", priority=3)

7. update_task:
   - Purpose: Alters specific property keys across a task target using an arbitrary data map payload.
   - Arguments:
     a) id: str - System unique tracking identity key sequence signature targeting the task (required).
     b) data: dict - Key-value properties mapping operational changes (e.g., {"content": "Revised title text"}) (required).
     c) cred_key: str (default: "todoist") - Target secure configuration lookup directory data block.
   - Returns: ToolResult verifying completion actions alongside execution confirmation flags.
   - How to call: TodoistTool.update_task(id="77334411", data={"priority": 2, "description": "Scope finalized."})

8. complete_task:
   - Purpose: Closes out an open action ticket item, removing it from active workflow visualizations.
   - Arguments:
     a) id: str - Unique target task item location reference string key (required).
     b) cred_key: str (default: "todoist") - System validation profile configuration identifier path handle.
   - Returns: ToolResult validating completion status operations across the service layer.
   - How to call: TodoistTool.complete_task(id="77334411")

9. delete_task:
   - Purpose: Erases a task record comprehensively out of the production database instance ledger.
   - Arguments:
     a) id: str - Unique core task tracking key target matching deletion filters (required).
     b) cred_key: str (default: "todoist") - Secure credentials vault entry system validation parameter key.
   - Returns: ToolResult logging deployment success statuses over the server interface.
   - How to call: TodoistTool.delete_task(id="88445522")

10. reopen_task:
    - Purpose: Restores a previously completed task record back into active list frameworks.
    - Arguments:
      a) id: str - Target finished task identifier reference unique string key (required).
      b) cred_key: str (default: "todoist") - Registry configuration parameter indexing standard security keys.
    - Returns: ToolResult confirming re-injection profiles over live workflow targets.
    - How to call: TodoistTool.reopen_task(id="88445522")

11. get_comments:
    - Purpose: Polls historical conversation streams tracking dialogue updates directly attached to a single task item.
    - Arguments:
      a) task_id: str - Explicit task item identifier key target (required).
      b) cred_key: str (default: "todoist") - Secure token repository destination pointer registry map index.
    - Returns: ToolResult framing structured lists of text communication strings and posting dates.
    - How to call: TodoistTool.get_comments(task_id="99556633")

12. add_comment:
    - Purpose: Appends text annotations or optional file links directly to a specific task's collaborative log stream.
    - Arguments:
      a) task_id: str - target project task identity identifier code string (required).
      b) content: str - Core written text payload forming the communication post body (required).
      c) attachment: dict (default: None) - Dictionary properties metadata mapping external files or uploaded document assets.
      d) cred_key: str (default: "todoist") - Connection routing security token profile directory indicator.
    - Returns: ToolResult verifying messaging deployment states over the network interface.
    - How to call: TodoistTool.add_comment(task_id="99556633", content="Logs attached for review.")

13. get_labels:
    - Purpose: Extracts all custom metadata categorization tags available inside the user profile.
    - Arguments:
      a) cred_key: str (default: "todoist") - Core client configuration vault routing index tag string.
    - Returns: ToolResult gathering data indexes matching tag identifiers and assigned label colors.
    - How to call: TodoistTool.get_labels()

14. add_label:
    - Purpose: Provisions a brand-new semantic metadata tag indicator with an explicit display color tag.
    - Arguments:
      a) name: str - Target literal text tag string defining the context grouping label (required).
      b) color: str (default: "charcoal") - Aesthetic display highlight visual classification parameter token.
      c) cred_key: str (default: "todoist") - Secure credentials storage validation dictionary indicator.
    - Returns: ToolResult mapping validation tracking details matching the generated tag asset node.
    - How to call: TodoistTool.add_label(name="Blocked-External", color="magenta")

15. quick_add:
    - Purpose: Injects structured tasks instantly using conversational natural language syntax strings.
    - Arguments:
      a) text: str - Casual raw phrase configuring task body, deadlines, priority, and labels (required).
      b) cred_key: str (default: "todoist") - Routing index target point mapping security token maps.
    - Returns: ToolResult presenting the server-side parsed dictionary properties of the created task asset.
    - How to call: TodoistTool.quick_add(text="Submit financial audits Friday at noon p1 #Accounting")

16. get_activity_log:
    - Purpose: Queries historical execution activity trails monitoring systemic operations occurring across the account workspace.
    - Arguments:
      a) event_type: str (default: None) - Limits output logs to a precise action category (e.g., "added", "completed", "deleted").
      b) object_type: str (default: None) - Filters results matching system item structures (e.g., "item", "project", "note").
      c) since: str (default: None) - ISO formatted calendar deadline date bounding the chronological lookup depth.
      d) cred_key: str (default: "todoist") - Access validation key parameter routing string pointer maps.
    - Returns: ToolResult collecting sequential dictionary entries mapping execution streams.
    - How to call: TodoistTool.get_activity_log(event_type="completed", object_type="item")

17. get_productivity_stats:
    - Purpose: Extracts user account productivity tracking analytics and performance metric summaries.
    - Arguments:
      a) cred_key: str (default: "todoist") - System validation token folder location tracking handle.
    - Returns: ToolResult rendering diagnostic payload records detailing daily streaks and karma histories.
    - How to call: TodoistTool.get_productivity_stats()
""")
       
    @staticmethod
    def _api(cred_key: str = "todoist"):
        from todoist_api_python.api import TodoistAPI
        token = CredStore.load(cred_key).get("api_token", "")
        if not token:
            raise ValueError("No Todoist token. Store under 'todoist' key.")
        return TodoistAPI(token)

    @staticmethod
    def get_projects(cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            projects = api.get_projects()
            data = [{"id": p.id, "name": p.name,
                     "color": p.color} for p in projects]
            return ToolResult(True, f"✓ {len(data)} projects", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_projects failed: {e}")

    @staticmethod
    def add_project(name: str, color: str = "charcoal",
                    parent_id: str = None,
                    cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            kwargs: dict = {"name": name, "color": color}
            if parent_id:
                kwargs["parent_id"] = parent_id
            proj = api.add_project(**kwargs)
            return ToolResult(True, f"✓ Project created: {proj.id}",
                              {"id": proj.id, "name": proj.name})
        except Exception as e:
            return ToolResult(False, f"✗ add_project failed: {e}")

    @staticmethod
    def update_project(id: str, data: dict,
                       cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            ok = api.update_project(id, **data)
            return ToolResult(ok, "✓ Project updated" if ok else "✗ Update failed")
        except Exception as e:
            return ToolResult(False, f"✗ update_project failed: {e}")

    @staticmethod
    def delete_project(id: str, cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            ok = api.delete_project(id)
            return ToolResult(ok, "✓ Project deleted" if ok else "✗ Delete failed")
        except Exception as e:
            return ToolResult(False, f"✗ delete_project failed: {e}")

    @staticmethod
    def get_tasks(project_id: str = None, filter: str = None,
                  label: str = None, priority: int = None,
                  cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            kwargs: dict = {}
            if project_id:
                kwargs["project_id"] = project_id
            if filter:
                kwargs["filter"] = filter
            if label:
                kwargs["label"] = label
            if priority is not None:
                kwargs["priority"] = priority
            tasks = api.get_tasks(**kwargs)
            data = [{"id": t.id, "content": t.content,
                     "due": t.due, "priority": t.priority,
                     "project_id": t.project_id} for t in tasks]
            return ToolResult(True, f"✓ {len(data)} tasks", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_tasks failed: {e}")

    @staticmethod
    def add_task(content: str, description: str = "",
                 project_id: str = None, due_string: str = None,
                 priority: int = 1, labels: list = None,
                 cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            kwargs: dict = {"content": content, "description": description,
                            "priority": priority}
            if project_id:
                kwargs["project_id"] = project_id
            if due_string:
                kwargs["due_string"] = due_string
            if labels:
                kwargs["labels"] = labels
            task = api.add_task(**kwargs)
            return ToolResult(True, f"✓ Task added: {task.id}",
                              {"id": task.id, "content": task.content})
        except Exception as e:
            return ToolResult(False, f"✗ add_task failed: {e}")

    @staticmethod
    def update_task(id: str, data: dict,
                    cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            ok = api.update_task(id, **data)
            return ToolResult(ok, "✓ Task updated" if ok else "✗ Update failed")
        except Exception as e:
            return ToolResult(False, f"✗ update_task failed: {e}")

    @staticmethod
    def complete_task(id: str, cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            ok = api.close_task(id)
            return ToolResult(ok, "✓ Task completed" if ok else "✗ Failed")
        except Exception as e:
            return ToolResult(False, f"✗ complete_task failed: {e}")

    @staticmethod
    def delete_task(id: str, cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            ok = api.delete_task(id)
            return ToolResult(ok, "✓ Task deleted" if ok else "✗ Failed")
        except Exception as e:
            return ToolResult(False, f"✗ delete_task failed: {e}")

    @staticmethod
    def reopen_task(id: str, cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            ok = api.reopen_task(id)
            return ToolResult(ok, "✓ Task reopened" if ok else "✗ Failed")
        except Exception as e:
            return ToolResult(False, f"✗ reopen_task failed: {e}")

    @staticmethod
    def get_comments(task_id: str, cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            comments = api.get_comments(task_id=task_id)
            data = [{"id": c.id, "content": c.content,
                     "posted_at": c.posted_at} for c in comments]
            return ToolResult(True, f"✓ {len(data)} comments", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_comments failed: {e}")

    @staticmethod
    def add_comment(task_id: str, content: str,
                    attachment: dict = None,
                    cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            kwargs: dict = {"task_id": task_id, "content": content}
            if attachment:
                kwargs["attachment"] = attachment
            comment = api.add_comment(**kwargs)
            return ToolResult(True, f"✓ Comment added: {comment.id}",
                              {"id": comment.id})
        except Exception as e:
            return ToolResult(False, f"✗ add_comment failed: {e}")

    @staticmethod
    def get_labels(cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            labels = api.get_labels()
            data = [{"id": l.id, "name": l.name,
                     "color": l.color} for l in labels]
            return ToolResult(True, f"✓ {len(data)} labels", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_labels failed: {e}")

    @staticmethod
    def add_label(name: str, color: str = "charcoal",
                  cred_key: str = "todoist") -> ToolResult:
        try:
            api = TodoistTool._api(cred_key)
            label = api.add_label(name=name, color=color)
            return ToolResult(True, f"✓ Label added: {label.id}",
                              {"id": label.id, "name": label.name})
        except Exception as e:
            return ToolResult(False, f"✗ add_label failed: {e}")

    @staticmethod
    def quick_add(text: str, cred_key: str = "todoist") -> ToolResult:
        """Natural language quick add, e.g. 'Buy milk tomorrow p1 #shopping'"""
        try:
            import requests
            token = CredStore.load(cred_key).get("api_token", "")
            resp = requests.post(
                "https://api.todoist.com/sync/v9/quick/add",
                headers={"Authorization": f"Bearer {token}"},
                json={"text": text}, timeout=10)
            resp.raise_for_status()
            item = resp.json()
            return ToolResult(True, f"✓ Quick-added: {item.get('content','')}", item)
        except Exception as e:
            return ToolResult(False, f"✗ quick_add failed: {e}")

    @staticmethod
    def get_activity_log(event_type: str = None, object_type: str = None,
                         since: str = None,
                         cred_key: str = "todoist") -> ToolResult:
        try:
            import requests
            token = CredStore.load(cred_key).get("api_token", "")
            params: dict = {"limit": 50}
            if event_type:
                params["event_type"] = event_type
            if object_type:
                params["object_type"] = object_type
            if since:
                params["since"] = since
            resp = requests.get(
                "https://api.todoist.com/sync/v9/activity/get",
                headers={"Authorization": f"Bearer {token}"},
                params=params, timeout=15)
            resp.raise_for_status()
            events = resp.json().get("events", [])
            return ToolResult(True, f"✓ {len(events)} events", events)
        except Exception as e:
            return ToolResult(False, f"✗ get_activity_log failed: {e}")

    @staticmethod
    def get_productivity_stats(cred_key: str = "todoist") -> ToolResult:
        try:
            import requests
            token = CredStore.load(cred_key).get("api_token", "")
            resp = requests.get(
                "https://api.todoist.com/sync/v9/user/get_productivity_stats",
                headers={"Authorization": f"Bearer {token}"},
                timeout=15)
            resp.raise_for_status()
            return ToolResult(True, "✓ Stats retrieved", resp.json())
        except Exception as e:
            return ToolResult(False, f"✗ get_productivity_stats failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 8. ObsidianTool
# ═════════════════════════════════════════════════════════════════════════════

class ObsidianTool:
    name = "obsidian"
    description = (
        "Obsidian vault operations — read/write/search notes, manage tags, "
        "backlinks, daily notes, canvases, and sync folders to vault"
    )
    use = ("""
Name of Tool: ObsidianTool

Purpose of Tool:
The ObsidianTool provides a comprehensive programmatic interface to manage local Obsidian note-taking vaults. 
It facilitates CRUD operations on Markdown notes containing YAML frontmatter metadata structures, builds bidirectional 
linking maps (backlinks and outlinks), implements targeted system indexing and note searching, manages semantic classification 
tag logs, interacts with programmatic canvas components, and automates content syncing routines from external local directories.

Methods:
- read_note: Extracts structured metadata, raw strings, and body content from a target Markdown file.
- create_note: Provisions a completely fresh Markdown note file featuring isolated YAML frontmatter data blocks.
- update_note: Modifies text content within an existing file via substitution, appending, or prepending modes.
- delete_note: Safely unlinks and destroys a targeted note file within the operational local workspace.
- search_notes: Evaluates the directory tree applying content, tag, or frontmatter metadata payload filters.
- list_notes: Recursively catalogs relative path sequences identifying notes tracking in specified directories.
- get_backlinks: Gathers all unique source file records linking directly back to a targeted note path signature.
- get_outlinks: Decodes regular expression patterns to isolate outgoing link names embedded inside a note file.
- add_tag: Appends unique classification tokens directly into the tags array within the target's YAML header.
- remove_tag: Filters out specific categorization tokens running inside the frontmatter collection.
- create_daily_note: Provisions structured temporal logging journals pre-populated with baseline tracking headers.
- append_to_daily_note: Hotloaded wrapper targeting rapid task injection logs on current chronological notes.
- create_canvas: Generates native Obsidian layout elements utilizing nodes, edge indicators, and coordinate JSON blocks.
- get_graph_data: Builds network topologies mapping node intersections across all linked files inside a vault path.
- sync_folder_to_vault: Imports external local assets into the vault environment matching strict extension criteria.

How to use Tool Methods:

1. read_note:
   - Purpose: Extracts structural segments from a target note, resolving metadata maps and content values.
   - Arguments:
     a) vault_path: str - Absolute file path tracking the location of the host Obsidian vault (required).
     b) note_path: str - Relative sub-path routing targets to the precise file name (required).
   - Returns: ToolResult presenting extracted dictionary entries mapped under frontmatter, content, and raw text.
   - How to call: ObsidianTool.read_note(vault_path="/Users/workspace/vault", note_path="Engineering/Architecture")

2. create_note:
   - Purpose: Provisions a brand-new Markdown file complete with a clean header structure.
   - Arguments:
     a) vault_path: str - Base file directory coordinate string hosting the vault (required).
     b) note_path: str - Destination folder and file name assignment targets (required).
     c) content: str - Baseline textual body context deployed inside the new file (required).
     d) frontmatter_data: dict (default: None) - Key-value payload schema specifying YAML metadata parameters.
   - Returns: ToolResult logging deployment states alongside absolute system generation logs.
   - How to call: ObsidianTool.create_note(vault_path="/vault", note_path="Ideas", content="Text", frontmatter_data={"status": "draft"})

3. update_note:
   - Purpose: Alters content payloads in-place across target entities using explicit positioning layout parameters.
   - Arguments:
     a) vault_path: str - Targeted repository system absolute location string (required).
     b) note_path: str - Relative tracking file path target pointer (required).
     c) content: str - Text sequence injected into the target workspace node (required).
     d) merge_mode: str (default: "replace") - Positional operational flag selecting 'replace', 'append', or 'prepend'.
   - Returns: ToolResult assessing updates or automated instantiation tracking results.
   - How to call: ObsidianTool.update_note(vault_path="/vault", note_path="Logs", content="- New entry", merge_mode="append")

4. delete_note:
   - Purpose: Erases target markdown notes comprehensively out of local disk storage tracks.
   - Arguments:
     a) vault_path: str - Host structural project storage destination path (required).
     b) note_path: str - Location file identification code targeting deletion filters (required).
   - Returns: ToolResult evaluating system unlinking status verifications.
   - How to call: ObsidianTool.delete_note(vault_path="/vault", note_path="TempNote")

5. search_notes:
   - Purpose: Queries and filters files matching text query sequences, text labels, or explicit metadata metrics.
   - Arguments:
     a) vault_path: str - Target environment directory path holding the vault structure (required).
     b) query: str (default: "") - Literal string token evaluation match pattern targeting titles or content blocks.
     c) tags: list (default: None) - Limits lookups to nodes matching defined custom label criteria strings.
     d) frontmatter_filter: dict (default: None) - Structural parameters validating key-value compliance states.
   - Returns: ToolResult containing an array layout of individual metadata summaries for matching hits.
   - How to call: ObsidianTool.search_notes(vault_path="/vault", query="AI", tags=["research"])

6. list_notes:
   - Purpose: Builds a localized list record cataloging matching documents running inside folder matrices.
   - Arguments:
     a) vault_path: str - Parent target environment location code path (required).
     b) folder: str (default: "") - Scope constraints matching a precise internal vault branch folder.
   - Returns: ToolResult collecting sequential string entries documenting matching relative system paths.
   - How to call: ObsidianTool.list_notes(vault_path="/vault", folder="Templates", recursive=False)

7. get_backlinks:
   - Purpose: Evaluates tracking states to locate reference files highlighting the destination file token.
   - Arguments:
     a) vault_path: str - Core targeted repository base path identifier (required).
     b) note_path: str - Target coordinate node path evaluated for incoming intersections (required).
   - Returns: ToolResult housing lists tracking individual tracking source references.
   - How to call: ObsidianTool.get_backlinks(vault_path="/vault", note_path="Index")

8. get_outlinks:
   - Purpose: Scans internal documents to list explicit targets parsed out of native linking syntax rules.
   - Arguments:
     a) vault_path: str - Base file system infrastructure location sequence string (required).
     b) note_path: str - File system note signature pointer evaluated for outward paths (required).
   - Returns: ToolResult resolving flat string arrays of unique discovered reference names.
   - How to call: ObsidianTool.get_outlinks(vault_path="/vault", note_path="ProjectScope")

9. add_tag:
   - Purpose: Injects structural indexing tags directly onto frontmatter array parameters without duplicating data rows.
   - Arguments:
     a) vault_path: str - Main host file directory coordinate pointer path (required).
     b) note_path: str - Unique document reference key mapping target files (required).
     c) tags: list - Collection tracking text context markers assigned for addition (required).
   - Returns: ToolResult tracking field update confirmation states.
   - How to call: ObsidianTool.add_tag(vault_path="/vault", note_path="Recipes/Cake", tags=["baking", "dessert"])

10. remove_tag:
    - Purpose: Strips targeted classification indicator strings from note profiles.
    - Arguments:
      a) vault_path: str - Root storage environment context handle tracking paths (required).
      b) note_path: str - Relative link path target tracking the host documentation file (required).
      c) tags: list - Isolated text markers targeted for target frontmatter removal actions (required).
    - Returns: ToolResult logging modification tracking confirmations.
    - How to call: ObsidianTool.remove_tag(vault_path="/vault", note_path="Recipes/Cake", tags=["experimental"])

11. create_daily_note:
    - Purpose: Standardizes logging metrics by provisioning date-based tracking logs via pre-formatted templates.
    - Arguments:
      a) vault_path: str - Host repository root folder mapping (required).
      b) date: str (default: None) - ISO timestamp sequence tracking calendar names (defaults to active runtime date).
      c) template: str (default: "") - Alternative layout context blocks parsing baseline system configurations.
    - Returns: ToolResult mapping active creation confirmations matching generated document nodes.
    - How to call: ObsidianTool.create_daily_note(vault_path="/vault", date="2026-06-18")

12. append_to_daily_note:
    - Purpose: Commits rapid operational records onto current chronological text tracking tracks.
    - Arguments:
      a) vault_path: str - Root base repository path string reference (required).
      b) content: str - Custom data content layout strings committed to daily log streams (required).
      c) date: str (default: None) - Selects target ledger timelines based on structural input string names.
    - Returns: ToolResult evaluating system execution logs across underlying file operations.
    - How to call: ObsidianTool.append_to_daily_note(vault_path="/vault", content="## Review\n- Finished tests.")

13. create_canvas:
    - Purpose: Deploys unified diagram canvas workspaces capturing topological relationship systems.
    - Arguments:
      a) vault_path: str - Root destination folder path sequence token (required).
      b) canvas_path: str - Output naming coordinates mapping destination layout tracks (required).
      c) nodes: list - Complex coordinate structural items mapping item placements (required).
      d) edges: list (default: None) - Intersection arrays setting connection side profiles.
    - Returns: ToolResult confirming operational structure creations across host disk layouts.
    - How to call: ObsidianTool.create_canvas(vault_path="/vault", canvas_path="Boards/Main", nodes=[{"id":"1", "type":"text", "text":"Root"}])

14. get_graph_data:
    - Purpose: Generates global mapping metrics reflecting interconnectivity arrays tracking across all vault points.
    - Arguments:
      a) vault_path: str - Main vault entry routing point string parameter (required).
    - Returns: ToolResult resolving nodes lists alongside associated relational edge configurations.
    - How to call: ObsidianTool.get_graph_data(vault_path="/vault")

15. sync_folder_to_vault:
    - Purpose: Replicates collections matching tracking extensions from exterior endpoints to internal destinations.
    - Arguments:
      a) local_folder: str - Origin directory target track running files outside the system (required).
      b) vault_path: str - Base repository vault installation destination path target (required).
      b) subfolder: str (default: "") - Internal folder paths capturing tracking elements.
      c) file_types: list (default: None) - Limits copy routines to defined type selectors (e.g., [".md", ".png"]).
    - Returns: ToolResult processing operational verification logs accounting for copied tracking files.
    - How to call: ObsidianTool.sync_folder_to_vault(local_folder="/User/Desktop/Notes", vault_path="/vault", subfolder="Inbox")
""")
       
    @staticmethod
    def _note_path(vault_path: str, note_path: str) -> Path:
        p = Path(vault_path) / note_path
        if not str(p).endswith(".md"):
            p = Path(str(p) + ".md")
        return p

    @staticmethod
    def read_note(vault_path: str, note_path: str) -> ToolResult:
        try:
            import frontmatter
            p = ObsidianTool._note_path(vault_path, note_path)
            if not p.exists():
                return ToolResult(False, f"✗ Note not found: {p}")
            post = frontmatter.load(str(p))
            return ToolResult(True, f"✓ Read {p.name}",
                              {"frontmatter": dict(post.metadata),
                               "content": post.content,
                               "raw": p.read_text(encoding="utf-8")})
        except Exception as e:
            return ToolResult(False, f"✗ read_note failed: {e}")

    @staticmethod
    def create_note(vault_path: str, note_path: str, content: str,
                    frontmatter_data: dict = None) -> ToolResult:
        try:
            import frontmatter
            p = ObsidianTool._note_path(vault_path, note_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            if p.exists():
                return ToolResult(False, f"✗ Note already exists: {p}")
            post = frontmatter.Post(content,
                                    **(frontmatter_data or {}))
            p.write_text(frontmatter.dumps(post), encoding="utf-8")
            return ToolResult(True, f"✓ Note created: {p}")
        except Exception as e:
            return ToolResult(False, f"✗ create_note failed: {e}")

    @staticmethod
    def update_note(vault_path: str, note_path: str, content: str,
                    merge_mode: str = "replace") -> ToolResult:
        """merge_mode: replace | append | prepend"""
        try:
            import frontmatter
            p = ObsidianTool._note_path(vault_path, note_path)
            if not p.exists():
                return ObsidianTool.create_note(vault_path, note_path, content)
            post = frontmatter.load(str(p))
            if merge_mode == "append":
                post.content = post.content + "\n" + content
            elif merge_mode == "prepend":
                post.content = content + "\n" + post.content
            else:
                post.content = content
            p.write_text(frontmatter.dumps(post), encoding="utf-8")
            return ToolResult(True, f"✓ Note updated ({merge_mode}): {p}")
        except Exception as e:
            return ToolResult(False, f"✗ update_note failed: {e}")

    @staticmethod
    def delete_note(vault_path: str, note_path: str) -> ToolResult:
        try:
            p = ObsidianTool._note_path(vault_path, note_path)
            if p.exists():
                p.unlink()
                return ToolResult(True, f"✓ Deleted: {p}")
            return ToolResult(False, f"✗ Not found: {p}")
        except Exception as e:
            return ToolResult(False, f"✗ delete_note failed: {e}")

    @staticmethod
    def search_notes(vault_path: str, query: str = "",
                     tags: list = None,
                     frontmatter_filter: dict = None) -> ToolResult:
        try:
            import frontmatter as fm
            vault = Path(vault_path)
            results = []
            for md in vault.rglob("*.md"):
                try:
                    post = fm.load(str(md))
                    text = post.content.lower()
                    meta = {k.lower(): v
                            for k, v in post.metadata.items()}

                    # text query
                    if query and query.lower() not in text:
                        if query.lower() not in md.name.lower():
                            continue

                    # tag filter
                    if tags:
                        note_tags = meta.get("tags", [])
                        if isinstance(note_tags, str):
                            note_tags = [note_tags]
                        if not any(t in note_tags for t in tags):
                            continue

                    # frontmatter filter
                    if frontmatter_filter:
                        match = all(
                            str(meta.get(k, "")).lower() == str(v).lower()
                            for k, v in frontmatter_filter.items()
                        )
                        if not match:
                            continue

                    results.append({
                        "path": str(md.relative_to(vault)),
                        "title": md.stem,
                        "tags": meta.get("tags", []),
                    })
                except Exception:
                    continue
            return ToolResult(True, f"✓ {len(results)} notes found", results)
        except Exception as e:
            return ToolResult(False, f"✗ search_notes failed: {e}")

    @staticmethod
    def list_notes(vault_path: str, folder: str = "",
                   recursive: bool = True) -> ToolResult:
        try:
            base = Path(vault_path) / folder
            if not base.exists():
                return ToolResult(False, f"✗ Folder not found: {base}")
            fn = base.rglob if recursive else base.glob
            notes = [str(p.relative_to(vault_path))
                     for p in fn("*.md")]
            return ToolResult(True, f"✓ {len(notes)} notes", notes)
        except Exception as e:
            return ToolResult(False, f"✗ list_notes failed: {e}")

    @staticmethod
    def get_backlinks(vault_path: str, note_path: str) -> ToolResult:
        try:
            target = ObsidianTool._note_path(vault_path, note_path)
            note_name = target.stem
            vault = Path(vault_path)
            backlinks = []
            patterns = [f"[[{note_name}]]",
                        f"[[{note_name}|",
                        f"[{note_name}]"]
            for md in vault.rglob("*.md"):
                if md == target:
                    continue
                try:
                    text = md.read_text(encoding="utf-8", errors="replace")
                    if any(p in text for p in patterns):
                        backlinks.append(str(md.relative_to(vault)))
                except Exception:
                    continue
            return ToolResult(True, f"✓ {len(backlinks)} backlinks", backlinks)
        except Exception as e:
            return ToolResult(False, f"✗ get_backlinks failed: {e}")

    @staticmethod
    def get_outlinks(vault_path: str, note_path: str) -> ToolResult:
        try:
            p = ObsidianTool._note_path(vault_path, note_path)
            text = p.read_text(encoding="utf-8", errors="replace")
            links = re.findall(r'\[\[([^\]|#]+)', text)
            unique = list(dict.fromkeys(links))
            return ToolResult(True, f"✓ {len(unique)} outlinks", unique)
        except Exception as e:
            return ToolResult(False, f"✗ get_outlinks failed: {e}")

    @staticmethod
    def add_tag(vault_path: str, note_path: str,
                tags: list) -> ToolResult:
        try:
            import frontmatter
            p = ObsidianTool._note_path(vault_path, note_path)
            post = frontmatter.load(str(p))
            existing = post.metadata.get("tags", [])
            if isinstance(existing, str):
                existing = [existing]
            merged = list(dict.fromkeys(existing + tags))
            post.metadata["tags"] = merged
            p.write_text(frontmatter.dumps(post), encoding="utf-8")
            return ToolResult(True, f"✓ Tags added: {tags}")
        except Exception as e:
            return ToolResult(False, f"✗ add_tag failed: {e}")

    @staticmethod
    def remove_tag(vault_path: str, note_path: str,
                   tags: list) -> ToolResult:
        try:
            import frontmatter
            p = ObsidianTool._note_path(vault_path, note_path)
            post = frontmatter.load(str(p))
            existing = post.metadata.get("tags", [])
            if isinstance(existing, str):
                existing = [existing]
            post.metadata["tags"] = [t for t in existing
                                     if t not in tags]
            p.write_text(frontmatter.dumps(post), encoding="utf-8")
            return ToolResult(True, f"✓ Tags removed: {tags}")
        except Exception as e:
            return ToolResult(False, f"✗ remove_tag failed: {e}")

    @staticmethod
    def create_daily_note(vault_path: str, date: str = None,
                          template: str = "") -> ToolResult:
        try:
            day = date or datetime.now().strftime("%Y-%m-%d")
            note_path = f"Daily/{day}"
            content = template or f"# {day}\n\n## Tasks\n\n## Notes\n"
            return ObsidianTool.create_note(
                vault_path, note_path, content,
                {"date": day, "tags": ["daily"]})
        except Exception as e:
            return ToolResult(False, f"✗ create_daily_note failed: {e}")

    @staticmethod
    def append_to_daily_note(vault_path: str, content: str,
                              date: str = None) -> ToolResult:
        try:
            day = date or datetime.now().strftime("%Y-%m-%d")
            note_path = f"Daily/{day}"
            p = ObsidianTool._note_path(vault_path, note_path)
            if not p.exists():
                ObsidianTool.create_daily_note(vault_path, day)
            return ObsidianTool.update_note(
                vault_path, note_path, content, merge_mode="append")
        except Exception as e:
            return ToolResult(False, f"✗ append_to_daily_note failed: {e}")

    @staticmethod
    def create_canvas(vault_path: str, canvas_path: str,
                      nodes: list, edges: list = None) -> ToolResult:
        """
        nodes: [{"id":"1","type":"text","text":"Hello","x":0,"y":0,"width":200,"height":60}]
        edges: [{"id":"e1","fromNode":"1","toNode":"2","fromSide":"right","toSide":"left"}]
        """
        try:
            p = Path(vault_path) / canvas_path
            if not str(p).endswith(".canvas"):
                p = Path(str(p) + ".canvas")
            p.parent.mkdir(parents=True, exist_ok=True)
            canvas_data = {"nodes": nodes, "edges": edges or []}
            p.write_text(json.dumps(canvas_data, indent=2), encoding="utf-8")
            return ToolResult(True, f"✓ Canvas created: {p}")
        except Exception as e:
            return ToolResult(False, f"✗ create_canvas failed: {e}")

    @staticmethod
    def get_graph_data(vault_path: str) -> ToolResult:
        """Returns nodes and edges for the full vault graph."""
        try:
            vault = Path(vault_path)
            nodes = []
            edges = []
            all_notes = {p.stem: str(p.relative_to(vault))
                         for p in vault.rglob("*.md")}
            for md in vault.rglob("*.md"):
                try:
                    stem = md.stem
                    rel = str(md.relative_to(vault))
                    nodes.append({"id": stem, "path": rel})
                    text = md.read_text(encoding="utf-8", errors="replace")
                    links = re.findall(r'\[\[([^\]|#]+)', text)
                    for lk in links:
                        lk = lk.strip()
                        if lk in all_notes:
                            edges.append({"from": stem, "to": lk})
                except Exception:
                    continue
            return ToolResult(True, f"✓ Graph: {len(nodes)} nodes, {len(edges)} edges",
                              {"nodes": nodes, "edges": edges})
        except Exception as e:
            return ToolResult(False, f"✗ get_graph_data failed: {e}")

    @staticmethod
    def sync_folder_to_vault(local_folder: str, vault_path: str,
                              subfolder: str = "",
                              file_types: list = None) -> ToolResult:
        try:
            exts = file_types or [".md", ".txt", ".png", ".jpg", ".pdf"]
            src = Path(local_folder)
            dest_base = Path(vault_path) / subfolder
            dest_base.mkdir(parents=True, exist_ok=True)
            copied = 0
            for ext in exts:
                for f in src.rglob(f"*{ext}"):
                    rel = f.relative_to(src)
                    dest = dest_base / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    import shutil
                    shutil.copy2(str(f), str(dest))
                    copied += 1
            return ToolResult(True, f"✓ Synced {copied} files to vault")
        except Exception as e:
            return ToolResult(False, f"✗ sync_folder_to_vault failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 9. BookmarkManagerTool
# ═════════════════════════════════════════════════════════════════════════════

class BookmarkManagerTool:
    name = "bookmarks"
    description = (
        "Browser bookmark manager — import/export HTML, add/remove/search, "
        "organize by domain, check broken links, archive pages, "
        "generate reading lists, bulk screenshots, AI tagging, deduplication"
    )
    use = ("""
Name of Tool: BookmarkManagerTool

Purpose of Tool:
The BookmarkManagerTool is a browser bookmark management suite. It processes standard Netscape-style 
HTML bookmark files for importing and exporting, handles basic programmatic CRUD operations inside a local 
JSON datastore, groups resources by domain mappings, audits URL accessibility to detect dead links, captures full-page 
HTML archives and screenshots via headless browser automation, handles automatic AI meta-tagging via local LLMs, 
and cleans up datasets using normalizer deduplication structures.

Methods:
- import_bookmarks: Extracts and parses raw bookmark dictionaries out of an uploaded browser HTML document.
- export_bookmarks: Renders a collection of links into a standard Netscape-style bookmark HTML page structure.
- add_bookmark: Persists a fresh link record along with custom tags and routing flags inside the local ledger file.
- remove_bookmark: Purges saved link objects from the local JSON registry by filtering out specific URL entries.
- search_bookmarks: Queries the link store using literal text query sequences, target directory locations, or tag labels.
- organize_by_domain: Parses and strips URL host strings to group bookmarks into isolated domain-keyed dictionaries.
- check_broken_links: Audits live URLs via HTTP HEAD requests to detect connection timeouts or errors (status >= 400).
- archive_page: Launches a headless browser to capture an immutable full-page text content dump and visual layout PNG.
- generate_reading_list: Scrapes linked page properties to output a Markdown summary file embedded with meta descriptions.
- bulk_screenshot: Sequentially captures snapshot graphics of multiple website viewports using headless execution streams.
- tag_with_ai: Offloads contextual tag generation tasks onto a local Ollama LLM endpoint using prompt structures.
- deduplicate: Strips trailing characters and normalizes case strings to clean duplicate targets out of a link array.

How to use Tool Methods:

1. import_bookmarks:
   - Purpose: Imports unstructured, exported browser bookmark lines into system-parsable dictionary records.
   - Arguments:
     a) html_file: str - Target system absolute path locating the exported source bookmark file (required).
   - Returns: ToolResult presenting parsed dictionary entries mapped under url, title, add_date, and tags keys.
   - How to call: BookmarkManagerTool.import_bookmarks(html_file="/Users/downloads/chrome_bookmarks.html")

2. export_bookmarks:
   - Purpose: Assembles a collection of bookmark rows into a standard Netscape-compatible web document.
   - Arguments:
     a) bookmarks: list - Target collection array filled with dictionary rows matching the system schema (required).
     b) output_html: str - Absolute file system generation layout target destination track path (required).
   - Returns: ToolResult logging deployment success validations alongside target path strings.
   - How to call: BookmarkManagerTool.export_bookmarks(bookmarks=my_links, output_html="/backups/bookmarks.html")

3. add_bookmark:
   - Purpose: Appends a specific, separate resource node tracking record inside the user's home registry.
   - Arguments:
     a) url: str - Valid internet address destination locator string target (required).
     b) title: str (default: "") - Display string name indicator used for explicit identification.
     b) folder: str (default: "") - Parent directory location label managing target structural paths.
     c) tags: str (default: "") - Comma-delimited descriptor strings classifying the connection record.
     d) description: str (default: "") - Extended annotations or text notes documenting the resource node.
   - Returns: ToolResult validating local transaction tracking states.
   - How to call: BookmarkManagerTool.add_bookmark(url="https://arxiv.org", title="arXiv", tags="science,research")

4. remove_bookmark:
   - Purpose: Drops matching link elements out of the internal persistent JSON datastore layer.
   - Arguments:
     a) url: str - Targeted primary location address link key used to identify deletion records (required).
   - Returns: ToolResult declaring total counts matching deleted link entities.
   - How to call: BookmarkManagerTool.remove_bookmark(url="https://arxiv.org")

5. search_bookmarks:
   - Purpose: Runs lookups across deep resource lists using mixed literal text search matches.
   - Arguments:
     a) bookmarks: list (default: None) - Array parsed manually; defaults to reading the local store file.
     b) query: str (default: "") - Evaluates case-insensitive content hits across URL, title, or description strings.
     c) tags: str (default: "") - Constraints searching to paths containing the specified tag phrase.
     d) folder: str (default: "") - Isolates outputs matching precise folder destination tags.
   - Returns: ToolResult holding structural match arrays containing matched context fields.
   - How to call: BookmarkManagerTool.search_bookmarks(query="machine learning", tags="python")

6. organize_by_domain:
   - Purpose: Groups links chronologically into matching web resource origin host trees.
   - Arguments:
     a) bookmarks: list - Collection tracking raw bookmark entries to pass to the sorter route (required).
   - Returns: ToolResult housing dictionary mappings partitioned by isolated domain name strings.
   - How to call: BookmarkManagerTool.organize_by_domain(bookmarks=link_dataset)

7. check_broken_links:
   - Purpose: Probes website states across live servers to track and catalog broken tracking routes.
   - Arguments:
     a) bookmarks: list - Array gathering target links intended for active testing checks (required).
     b) timeout: int (default: 10) - Network response connection boundaries set in elapsed seconds.
   - Returns: ToolResult sorting structural operational tallies against failed record objects.
   - How to call: BookmarkManagerTool.check_broken_links(bookmarks=link_dataset, timeout=5)

8. archive_page:
   - Purpose: Generates local historical records capturing text markup alongside deep visual screenshots.
   - Arguments:
     a) url: str - Active network locator address target routed into the browser runner (required).
     b) output_folder: str - File destination folder directory hosting saved data components (required).
   - Returns: ToolResult pointing to system absolute generation points on disk layout trees.
   - How to call: BookmarkManagerTool.archive_page(url="https://wikipedia.org", output_folder="/archives/wiki")

9. generate_reading_list:
   - Purpose: Scrapes target web document headers to structure a readable Markdown summary table on disk.
   - Arguments:
     a) urls: list - Plain text collection strings holding target web address links (required).
     b) output_md: str - Document destination path tracking file layout generations (required).
   - Returns: ToolResult logging file system output updates.
   - How to call: BookmarkManagerTool.generate_reading_list(urls=["https://github.com"], output_md="./reading.md")

10. bulk_screenshot:
    - Purpose: Concurrently fires browser viewport capture loops across large arrays of links.
    - Arguments:
      a) bookmarks: list - Collection capturing raw targets to route into the browser viewport snapshot loop (required).
      b) output_folder: str - Folder location index storing produced image formats (required).
    - Returns: ToolResult mapping absolute numbers tracing successfully captured link views.
    - How to call: BookmarkManagerTool.bulk_screenshot(bookmarks=my_links, output_folder="/user/images")

11. tag_with_ai:
    - Purpose: Generates context-aware categorization tokens using a local Ollama model framework.
    - Arguments:
      a) bookmarks: list - Input array grouping items to send to the local generation endpoint (required).
      b) model: str (default: "mistral:7b") - Active model indicator flag loaded inside the local running daemon.
    - Returns: ToolResult containing an updated array with generated string elements under 'ai_tags'.
    - How to call: BookmarkManagerTool.tag_with_ai(bookmarks=unlabeled_data, model="llama3")

12. deduplicate:
    - Purpose: Scrubs tracking arrays to clear out duplicate website address link definitions.
    - Arguments:
      a) bookmarks: list - Core input link data records evaluated for duplicate removal (required).
    - Returns: ToolResult mapping unique data elements while returning filtered link summaries.
    - How to call: BookmarkManagerTool.deduplicate(bookmarks=dirty_dataset)
""")
       
    # ── Helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def _parse_html_bookmarks(html_file: str) -> list:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(Path(html_file).read_text(errors="replace"),
                             "html.parser")
        bookmarks = []
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if href.startswith("http"):
                bookmarks.append({
                    "url": href,
                    "title": a.get_text(strip=True),
                    "add_date": a.get("add_date", ""),
                    "tags": a.get("tags", ""),
                    "folder": ""
                })
        return bookmarks

    # ── Core methods ──────────────────────────────────────────────────────

    @staticmethod
    def import_bookmarks(html_file: str) -> ToolResult:
        try:
            bookmarks = BookmarkManagerTool._parse_html_bookmarks(html_file)
            return ToolResult(True, f"✓ Imported {len(bookmarks)} bookmarks",
                              bookmarks)
        except Exception as e:
            return ToolResult(False, f"✗ import_bookmarks failed: {e}")

    @staticmethod
    def export_bookmarks(bookmarks: list, output_html: str) -> ToolResult:
        try:
            lines = [
                "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
                '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
                "<TITLE>Bookmarks</TITLE>",
                "<H1>Bookmarks</H1>",
                "<DL><p>"
            ]
            for bm in bookmarks:
                title = bm.get("title", bm.get("url", ""))
                url = bm.get("url", "")
                tags = bm.get("tags", "")
                lines.append(
                    f'    <DT><A HREF="{url}" TAGS="{tags}">{title}</A>')
            lines.append("</DL><p>")
            Path(output_html).write_text("\n".join(lines), encoding="utf-8")
            return ToolResult(True, f"✓ Exported {len(bookmarks)} bookmarks to {output_html}")
        except Exception as e:
            return ToolResult(False, f"✗ export_bookmarks failed: {e}")

    @staticmethod
    def add_bookmark(url: str, title: str = "", folder: str = "",
                     tags: str = "", description: str = "") -> ToolResult:
        try:
            store_path = Path.home() / ".npmai_agent" / "bookmarks.json"
            store_path.parent.mkdir(exist_ok=True)
            bms = json.loads(store_path.read_text()) if store_path.exists() else []
            bms.append({
                "url": url, "title": title or url,
                "folder": folder, "tags": tags,
                "description": description,
                "added": datetime.now().isoformat()
            })
            store_path.write_text(json.dumps(bms, indent=2))
            return ToolResult(True, f"✓ Bookmark added: {url}")
        except Exception as e:
            return ToolResult(False, f"✗ add_bookmark failed: {e}")

    @staticmethod
    def remove_bookmark(url: str) -> ToolResult:
        try:
            store_path = Path.home() / ".npmai_agent" / "bookmarks.json"
            if not store_path.exists():
                return ToolResult(False, "No bookmark store found.")
            bms = json.loads(store_path.read_text())
            before = len(bms)
            bms = [b for b in bms if b.get("url") != url]
            store_path.write_text(json.dumps(bms, indent=2))
            return ToolResult(True, f"✓ Removed {before - len(bms)} bookmark(s)")
        except Exception as e:
            return ToolResult(False, f"✗ remove_bookmark failed: {e}")

    @staticmethod
    def search_bookmarks(bookmarks: list = None, query: str = "",
                         tags: str = "", folder: str = "") -> ToolResult:
        try:
            if bookmarks is None:
                store_path = Path.home() / ".npmai_agent" / "bookmarks.json"
                bookmarks = (json.loads(store_path.read_text())
                             if store_path.exists() else [])
            results = []
            for bm in bookmarks:
                if (query.lower() in bm.get("url", "").lower() or
                        query.lower() in bm.get("title", "").lower() or
                        query.lower() in bm.get("description", "").lower()):
                    if tags and tags not in bm.get("tags", ""):
                        continue
                    if folder and folder not in bm.get("folder", ""):
                        continue
                    results.append(bm)
            return ToolResult(True, f"✓ {len(results)} matches", results)
        except Exception as e:
            return ToolResult(False, f"✗ search_bookmarks failed: {e}")

    @staticmethod
    def organize_by_domain(bookmarks: list) -> ToolResult:
        try:
            from urllib.parse import urlparse
            organized: dict = {}
            for bm in bookmarks:
                try:
                    domain = urlparse(bm.get("url", "")).netloc
                    domain = domain.replace("www.", "")
                    organized.setdefault(domain, []).append(bm)
                except Exception:
                    organized.setdefault("other", []).append(bm)
            return ToolResult(True,
                              f"✓ Organized into {len(organized)} domains",
                              organized)
        except Exception as e:
            return ToolResult(False, f"✗ organize_by_domain failed: {e}")

    @staticmethod
    def check_broken_links(bookmarks: list, timeout: int = 10) -> ToolResult:
        try:
            import requests
            broken = []
            ok_count = 0
            for bm in bookmarks:
                url = bm.get("url", "")
                try:
                    resp = requests.head(url, timeout=timeout,
                                        allow_redirects=True,
                                        headers={"User-Agent": "Mozilla/5.0"})
                    if resp.status_code >= 400:
                        broken.append({**bm,
                                       "status": resp.status_code})
                    else:
                        ok_count += 1
                except Exception as ex:
                    broken.append({**bm, "error": str(ex)})
            return ToolResult(True,
                              f"✓ {ok_count} OK, {len(broken)} broken",
                              broken)
        except Exception as e:
            return ToolResult(False, f"✗ check_broken_links failed: {e}")

    @staticmethod
    def archive_page(url: str, output_folder: str) -> ToolResult:
        try:
            from playwright.sync_api import sync_playwright
            out = Path(output_folder)
            out.mkdir(parents=True, exist_ok=True)
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', url)[:80]
            html_path = out / f"{safe_name}.html"
            with sync_playwright() as pw:
                b = pw.chromium.launch(headless=True)
                pg = b.new_page()
                pg.goto(url, timeout=30000,
                        wait_until="networkidle")
                html_path.write_text(pg.content(), encoding="utf-8")
                pg.screenshot(path=str(out / f"{safe_name}.png"),
                              full_page=True)
                b.close()
            return ToolResult(True, f"✓ Archived to {html_path}")
        except Exception as e:
            return ToolResult(False, f"✗ archive_page failed: {e}")

    @staticmethod
    def generate_reading_list(urls: list, output_md: str) -> ToolResult:
        try:
            import requests
            from bs4 import BeautifulSoup
            lines = ["# Reading List\n",
                     f"_Generated: {datetime.now().strftime('%Y-%m-%d')}_\n"]
            for i, url in enumerate(urls, 1):
                try:
                    resp = requests.get(url,
                                        headers={"User-Agent": "Mozilla/5.0"},
                                        timeout=10)
                    soup = BeautifulSoup(resp.text, "html.parser")
                    title = soup.title.string.strip() if soup.title else url
                    desc_tag = soup.find("meta", attrs={"name": "description"})
                    desc = (desc_tag.get("content", "")[:200]
                            if desc_tag else "")
                    lines.append(f"\n## {i}. [{title}]({url})\n")
                    if desc:
                        lines.append(f"> {desc}\n")
                except Exception:
                    lines.append(f"\n## {i}. [{url}]({url})\n")
            Path(output_md).write_text("\n".join(lines), encoding="utf-8")
            return ToolResult(True, f"✓ Reading list saved to {output_md}")
        except Exception as e:
            return ToolResult(False, f"✗ generate_reading_list failed: {e}")

    @staticmethod
    def bulk_screenshot(bookmarks: list, output_folder: str) -> ToolResult:
        try:
            from playwright.sync_api import sync_playwright
            out = Path(output_folder)
            out.mkdir(parents=True, exist_ok=True)
            saved = 0
            with sync_playwright() as pw:
                b = pw.chromium.launch(headless=True)
                pg = b.new_page()
                for bm in bookmarks:
                    url = bm.get("url", "")
                    if not url:
                        continue
                    safe = re.sub(r'[^a-zA-Z0-9_-]', '_', url)[:60]
                    try:
                        pg.goto(url, timeout=15000,
                                wait_until="domcontentloaded")
                        pg.screenshot(path=str(out / f"{safe}.png"),
                                      full_page=False)
                        saved += 1
                    except Exception:
                        pass
                b.close()
            return ToolResult(True, f"✓ Saved {saved} screenshots to {output_folder}")
        except Exception as e:
            return ToolResult(False, f"✗ bulk_screenshot failed: {e}")

    @staticmethod
    def tag_with_ai(bookmarks: list, model: str = "mistral:7b") -> ToolResult:
        """Use local Ollama to auto-tag bookmarks based on title+URL."""
        try:
            import requests
            tagged = []
            for bm in bookmarks:
                url = bm.get("url", "")
                title = bm.get("title", url)
                try:
                    resp = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": model,
                            "prompt": (
                                f"Suggest 3-5 short tags for this bookmark. "
                                f"Reply ONLY with comma-separated tags, nothing else.\n"
                                f"Title: {title}\nURL: {url}"
                            ),
                            "stream": False
                        },
                        timeout=30
                    )
                    tags = resp.json().get("response", "").strip()
                    tagged.append({**bm, "ai_tags": tags})
                except Exception:
                    tagged.append(bm)
            return ToolResult(True, f"✓ Tagged {len(tagged)} bookmarks", tagged)
        except Exception as e:
            return ToolResult(False, f"✗ tag_with_ai failed: {e}")

    @staticmethod
    def deduplicate(bookmarks: list) -> ToolResult:
        try:
            seen: dict = {}
            dupes = 0
            for bm in bookmarks:
                url = bm.get("url", "").rstrip("/").lower()
                if url not in seen:
                    seen[url] = bm
                else:
                    dupes += 1
            unique = list(seen.values())
            return ToolResult(True,
                              f"✓ {len(unique)} unique, {dupes} removed",
                              unique)
        except Exception as e:
            return ToolResult(False, f"✗ deduplicate failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 10. TimeTrackingTool
# ═════════════════════════════════════════════════════════════════════════════

class TimeTrackingTool:
    name = "time_tracking"
    description = (
        "Time and productivity tracking — local SQLite timer, Toggl + Clockify "
        "integration, timesheets, billing, and invoice export"
    )
    use = ("""
Name of Tool: TimeTrackingTool

Purpose of Tool:
The TimeTrackingTool provides a comprehensive solution for managing time logs, calculating client billing, 
generating markdown timesheets or structured invoices, and integrating with third-party tracking services 
like Toggl and Clockify. It maintains a local SQLite database configuration containing relational architectures 
tracking historical work items and active in-flight running timers.

Methods:
- start_timer: Resets active state tracking entries inside the registry to record a brand-new live work event.
- stop_timer: Commits active running properties to permanent ledger tables by evaluating calculated session duration flags.
- pause_timer: Dynamically pauses an ongoing timing task or modifies its starting offset during resume triggers.
- get_current_timer: Returns status calculations defining elapsed runtime attributes for an open running transaction.
- list_time_entries: Performs conditional relational operations extracting historical tracking rows across criteria filters.
- add_manual_entry: Directly injects a retroactively closed historical logging record onto target transaction scopes.
- delete_entry: Purges explicit session entries using specific database integer row index target assignments.
- generate_timesheet: Groups and rolls up multi-row tracking metadata into a presentable, sorted Markdown ledger output.
- get_project_summary: Provides a numeric overview of logged hours, task weights, and execution allocations per project.
- calculate_billing: Computes decimal financial amounts due from tracked time arrays using a baseline numeric multiplier rate.
- export_to_invoice: Generates an formatted Markdown document summarizing billing tallies and transactional deep-dives.
- connect_toggl: Caches API authorization credentials safely on local disk systems for Toggl platform contexts.
- toggl_list_projects: Queries workspace configurations out of remote Toggl API systems using cached credentials.
- toggl_start_timer: Dispatches synchronous creation structures onto active remote Toggl work project channels.
- connect_clockify: Authenticates secure credential state maps targeted at Clockify API operational loops.
- clockify_list_projects: Fetches functional tracking group records from remote Clockify workspace index patterns.
- clockify_time_entry: Registers a completed historical event item using explicit Clockify API request signatures.

How to use Tool Methods:

1. start_timer:
   - Purpose: Initializes a new tracking state record in the local ephemeral database tracker.
   - Arguments:
     a) project: str - Project domain category identifier targeted for the new tracker instance (required).
     b) task: str (default: "") - Specific assignment segment context name tracking the actual effort item.
     c) description: str (default: "") - Detailed supplemental logs defining the current scope items.
   - Returns: ToolResult mapping validation notes alongside generation timestamp metadata profiles.
   - How to call: TimeTrackingTool.start_timer(project="Internal Auth API", task="Bugfix", description="Fixing JWT validation leaks")

2. stop_timer:
   - Purpose: Computes final elapsed durations and moves active timer data flags into permanent entry arrays.
   - Arguments: None.
   - Returns: ToolResult holding precision transaction maps indicating duration properties calculated in minutes and seconds.
   - How to call: TimeTrackingTool.stop_timer()

3. pause_timer:
   - Purpose: Freezes tracking sequences without losing tracking progress, or normalizes starts during subsequent resume requests.
   - Arguments: None.
   - Returns: ToolResult flagging current mutation states ("Timer paused" vs "Timer resumed").
   - How to call: TimeTrackingTool.pause_timer()

4. get_current_timer:
   - Purpose: Inspects state machines to return active tracking context properties alongside computed operational values.
   - Arguments: None.
   - Returns: ToolResult indicating missing items or an payload dictionary reflecting runtime metadata details.
   - How to call: TimeTrackingTool.get_current_timer()

5. list_time_entries:
   - Purpose: Scans background datastore targets to retrieve a timeline of tracking records.
   - Arguments:
     a) date_from: str (default: None) - Lower ISO date threshold parsing matching logs.
     b) date_to: str (default: None) - Upper boundary date parameter checking tracking lists.
     c) project: str (default: None) - Substring lookup literal filtering targeted project labels.
   - Returns: ToolResult delivering an array containing structured tracking item dict details.
   - How to call: TimeTrackingTool.list_time_entries(date_from="2026-06-01", project="Auth")

6. add_manual_entry:
   - Purpose: Manually appends explicit retrospective record models directly onto database backend sheets.
   - Arguments:
     a) project: str - Core category tag indicating the parent task boundary node (required).
     b) task: str - Named tracking key for the targeted work item (required).
     c) description: str - Annotations contextualizing retrospective actions (required).
     d) start: str - ISO formatted initial boundary timestamp marker string (required).
     e) end: str - ISO formatted concluding boundary timestamp marker string (required).
   - Returns: ToolResult displaying operational statuses alongside calculated length metrics.
   - How to call: TimeTrackingTool.add_manual_entry(project="Docs", task="Wiki", description="Updated readme", start="2026-06-18T10:00:00", end="2026-06-18T11:30:00")

7. delete_entry:
   - Purpose: Permanently eliminates a transactional entry instance matching a specific integer record index.
   - Arguments:
     a) entry_id: int - Primary database row ID locating target data entities slated for extraction (required).
   - Returns: ToolResult asserting structural clearing transformations.
   - How to call: TimeTrackingTool.delete_entry(entry_id=42)

8. generate_timesheet:
   - Purpose: Collates historical row fields to output standard readable ledger layouts.
   - Arguments:
     a) date_from: str - Start criteria date threshold checking targeted items (required).
     b) date_to: str - End criteria date threshold mapping historical logs (required).
     c) group_by: str (default: "project") - Object structural item property sorting aggregated logs ("project" or "task").
     d) output: str (default: None) - Optional absolute system route path exporting raw text layouts onto disk storage.
   - Returns: ToolResult carrying compiled string configurations alongside master aggregate calculation properties.
   - How to call: TimeTrackingTool.generate_timesheet(date_from="2026-06-10", date_to="2026-06-17", output="./timesheet.md")

9. get_project_summary:
   - Purpose: Tallies high-level performance metrics broken down across task dimensions inside specified scopes.
   - Arguments:
     a) project: str - Target project label analyzed by database summary functions (required).
     b) date_range: tuple (default: None) - An optional 2-element tuple mapping string ISO bounds (start, end).
   - Returns: ToolResult enclosing structural dictionaries reflecting comprehensive duration metrics and numeric work rates.
   - How to call: TimeTrackingTool.get_project_summary(project="Auth API", date_range=("2026-01-01", "2026-06-18"))

10. calculate_billing:
    - Purpose: Performs conversion mathematics mapping tracked work quantities to financial numbers.
    - Arguments:
      a) date_from: str - Initial range threshold bounding the lookup (required).
      b) date_to: str - Terminating range threshold bounding the lookup (required).
      c) hourly_rate: float - Financial value constant factored against fractional hour counters (required).
      d) project: str (default: None) - Isolates lookup ranges to match specific project keys.
    - Returns: ToolResult indicating overall hours worked and monetary conclusions.
    - How to call: TimeTrackingTool.calculate_billing(date_from="2026-06-01", date_to="2026-06-15", hourly_rate=125.0, project="Auth")

11. export_to_invoice:
    - Purpose: Merges time logs and balance parameters into a formatted markdown receipt file.
    - Arguments:
      a) date_from: str - Start range window defining raw logging constraints (required).
      b) date_to: str - End range window defining raw logging constraints (required).
      c) client: str - Display identifier detailing the client entity receiving the document (required).
      d) rate: float - Monetary compensation value per calculated tracking hour units (required).
      e) output: str - Targeted absolute storage track path writing out generated markdown file configurations (required).
    - Returns: ToolResult showing transaction deployment records alongside calculated summary outputs.
    - How to call: TimeTrackingTool.export_to_invoice(date_from="2026-05-01", date_to="2026-05-31", client="Acme Corp", rate=150.0, output="invoice_may.md")

12. connect_toggl:
    - Purpose: Saves authorization credentials safely inside local system storage managers.
    - Arguments:
      a) api_token: str - Client authentication key provided by Toggl profile dashboards (required).
    - Returns: ToolResult confirming safe record persistence.
    - How to call: TimeTrackingTool.connect_toggl(api_token="t0ggl_sec_api_tok_xyz")

13. toggl_list_projects:
    - Purpose: Connects with remote network entities to retrieve configured project entities.
    - Arguments:
      a) cred_key: str (default: "toggl") - Configuration identifier used to retrieve local disk storage paths.
    - Returns: ToolResult providing arrays containing raw JSON payloads direct from Toggl channels.
    - How to call: TimeTrackingTool.toggl_list_projects()

14. toggl_start_timer:
    - Purpose: Invokes active network timers on target web infrastructure layers via remote execution pathways.
    - Arguments:
      a) project_id: int - Platform explicit ID used to bind the remote creation query (required).
      b) description: str (default: "") - Informational annotation passed down to distant server endpoints.
      c) cred_key: str (default: "toggl") - Storage key context identifying active API assets.
    - Returns: ToolResult showing generated server asset references.
    - How to call: TimeTrackingTool.toggl_start_timer(project_id=987654, description="Refactoring UI")

15. connect_clockify:
    - Purpose: Registers integration authentication keys tailored to Clockify dashboard backends.
    - Arguments:
      a) api_token: str - Authentication code mapping secure API client targets (required).
    - Returns: ToolResult showing creation metrics.
    - How to call: TimeTrackingTool.connect_clockify(api_token="cl0ck1fy_tok_abc")

16. clockify_list_projects:
    - Purpose: Reads available project indexes out of Clockify enterprise storage views.
    - Arguments:
      a) workspace_id: str (default: None) - Platform identifier tracking target boundaries; drops down to default nodes if omitted.
      b) cred_key: str (default: "clockify") - Key pointing to correct configuration credentials.
    - Returns: ToolResult containing multi-project payload tracking structures.
    - How to call: TimeTrackingTool.clockify_list_projects(workspace_id="wsp_abc123")

17. clockify_time_entry:
    - Purpose: Writes a explicit completed time item block onto external Clockify workspace ledgers.
    - Arguments:
      a) workspace_id: str - target destination account directory identifier (required).
      b) project_id: str - Project identity node tracing the tracking resource target (required).
      c) description: str - Notes contextually validating current log targets (required).
      d) start: str - ISO initialization time tracking bounds string (required).
      e) end: str - ISO termination time tracking bounds string (required).
      b) cred_key: str (default: "clockify") - Profile identifier managing authorization credentials.
    - Returns: ToolResult wrapping downstream verification data maps returned from server systems.
    - How to call: TimeTrackingTool.clockify_time_entry(workspace_id="w1", project_id="p1", description="Review", start="2026-06-18T14:00:00", end="2026-06-18T15:00:00")
""")
       
    _DB = Path.home() / ".npmai_agent" / "time_tracker.db"

    # ── Database init ─────────────────────────────────────────────────────

    @staticmethod
    def _conn() -> sqlite3.Connection:
        TimeTrackingTool._DB.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(TimeTrackingTool._DB))
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                project  TEXT NOT NULL,
                task     TEXT,
                description TEXT,
                start    TEXT NOT NULL,
                end      TEXT,
                duration INTEGER,
                source   TEXT DEFAULT 'local'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS current_timer (
                id      INTEGER PRIMARY KEY,
                project TEXT,
                task    TEXT,
                description TEXT,
                start   TEXT,
                paused  INTEGER DEFAULT 0,
                pause_start TEXT
            )
        """)
        conn.commit()
        return conn

    # ── Local timer ───────────────────────────────────────────────────────

    @staticmethod
    def start_timer(project: str, task: str = "",
                    description: str = "") -> ToolResult:
        try:
            conn = TimeTrackingTool._conn()
            conn.execute("DELETE FROM current_timer")
            now = datetime.now().isoformat()
            conn.execute(
                "INSERT INTO current_timer(project,task,description,start) "
                "VALUES(?,?,?,?)",
                (project, task, description, now))
            conn.commit()
            return ToolResult(True,
                              f"✓ Timer started: {project}/{task} at {now}")
        except Exception as e:
            return ToolResult(False, f"✗ start_timer failed: {e}")

    @staticmethod
    def stop_timer() -> ToolResult:
        try:
            conn = TimeTrackingTool._conn()
            row = conn.execute(
                "SELECT * FROM current_timer LIMIT 1").fetchone()
            if not row:
                return ToolResult(False, "No active timer.")
            now = datetime.now()
            start = datetime.fromisoformat(row["start"])
            duration_secs = int((now - start).total_seconds())
            conn.execute(
                "INSERT INTO entries(project,task,description,start,end,duration) "
                "VALUES(?,?,?,?,?,?)",
                (row["project"], row["task"], row["description"],
                 row["start"], now.isoformat(), duration_secs))
            conn.execute("DELETE FROM current_timer")
            conn.commit()
            mins = duration_secs // 60
            return ToolResult(True,
                              f"✓ Timer stopped: {row['project']} — {mins} min",
                              {"duration_seconds": duration_secs,
                               "duration_minutes": mins})
        except Exception as e:
            return ToolResult(False, f"✗ stop_timer failed: {e}")

    @staticmethod
    def pause_timer() -> ToolResult:
        try:
            conn = TimeTrackingTool._conn()
            row = conn.execute(
                "SELECT * FROM current_timer LIMIT 1").fetchone()
            if not row:
                return ToolResult(False, "No active timer.")
            if row["paused"]:
                # resume
                paused_secs = int(
                    (datetime.now() -
                     datetime.fromisoformat(row["pause_start"])
                     ).total_seconds())
                # extend start by paused duration to not count it
                new_start = (datetime.fromisoformat(row["start"]) +
                             timedelta(seconds=paused_secs)).isoformat()
                conn.execute(
                    "UPDATE current_timer SET paused=0, pause_start=NULL, start=?",
                    (new_start,))
                conn.commit()
                return ToolResult(True, "✓ Timer resumed")
            else:
                conn.execute(
                    "UPDATE current_timer SET paused=1, pause_start=?",
                    (datetime.now().isoformat(),))
                conn.commit()
                return ToolResult(True, "✓ Timer paused")
        except Exception as e:
            return ToolResult(False, f"✗ pause_timer failed: {e}")

    @staticmethod
    def get_current_timer() -> ToolResult:
        try:
            conn = TimeTrackingTool._conn()
            row = conn.execute(
                "SELECT * FROM current_timer LIMIT 1").fetchone()
            if not row:
                return ToolResult(True, "No active timer", None)
            elapsed = int(
                (datetime.now() -
                 datetime.fromisoformat(row["start"])).total_seconds())
            data = {k: row[k] for k in row.keys()}
            data["elapsed_seconds"] = elapsed
            data["elapsed_minutes"] = elapsed // 60
            return ToolResult(True,
                              f"✓ Running: {row['project']} — {elapsed//60} min",
                              data)
        except Exception as e:
            return ToolResult(False, f"✗ get_current_timer failed: {e}")

    @staticmethod
    def list_time_entries(date_from: str = None, date_to: str = None,
                          project: str = None) -> ToolResult:
        try:
            conn = TimeTrackingTool._conn()
            q = "SELECT * FROM entries WHERE 1=1"
            params: list = []
            if date_from:
                q += " AND start >= ?"
                params.append(date_from)
            if date_to:
                q += " AND start <= ?"
                params.append(date_to + "T23:59:59")
            if project:
                q += " AND project LIKE ?"
                params.append(f"%{project}%")
            q += " ORDER BY start DESC"
            rows = conn.execute(q, params).fetchall()
            entries = [dict(r) for r in rows]
            return ToolResult(True, f"✓ {len(entries)} entries", entries)
        except Exception as e:
            return ToolResult(False, f"✗ list_time_entries failed: {e}")

    @staticmethod
    def add_manual_entry(project: str, task: str, description: str,
                         start: str, end: str) -> ToolResult:
        try:
            conn = TimeTrackingTool._conn()
            s = datetime.fromisoformat(start)
            e = datetime.fromisoformat(end)
            duration = int((e - s).total_seconds())
            conn.execute(
                "INSERT INTO entries(project,task,description,start,end,duration) "
                "VALUES(?,?,?,?,?,?)",
                (project, task, description, start, end, duration))
            conn.commit()
            return ToolResult(True,
                              f"✓ Entry added: {project} {duration//60} min")
        except Exception as e:
            return ToolResult(False, f"✗ add_manual_entry failed: {e}")

    @staticmethod
    def delete_entry(entry_id: int) -> ToolResult:
        try:
            conn = TimeTrackingTool._conn()
            conn.execute("DELETE FROM entries WHERE id=?", (entry_id,))
            conn.commit()
            return ToolResult(True, f"✓ Entry {entry_id} deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_entry failed: {e}")

    @staticmethod
    def generate_timesheet(date_from: str, date_to: str,
                           group_by: str = "project",
                           output: str = None) -> ToolResult:
        try:
            result = TimeTrackingTool.list_time_entries(date_from, date_to)
            if not result.success:
                return result
            entries = result.data or []
            # group
            groups: dict = {}
            for e in entries:
                key = e.get(group_by, "unknown")
                groups.setdefault(key, []).append(e)

            lines = [f"# Timesheet: {date_from} → {date_to}\n"]
            total_secs = 0
            for key, grp in sorted(groups.items()):
                secs = sum(e.get("duration", 0) for e in grp)
                total_secs += secs
                h, m = secs // 3600, (secs % 3600) // 60
                lines.append(f"\n## {key}  ({h}h {m}m)")
                for e in grp:
                    d = e.get("duration", 0)
                    lines.append(
                        f"  - {e.get('start','')[:16]}  "
                        f"{e.get('task','')} — {d//60} min  "
                        f"{e.get('description','')}")

            th, tm = total_secs // 3600, (total_secs % 3600) // 60
            lines.append(f"\n**Total: {th}h {tm}m**")
            text = "\n".join(lines)
            if output:
                Path(output).write_text(text, encoding="utf-8")
            return ToolResult(True,
                              f"✓ Timesheet: {th}h {tm}m total",
                              {"text": text,
                               "total_seconds": total_secs})
        except Exception as e:
            return ToolResult(False, f"✗ generate_timesheet failed: {e}")

    @staticmethod
    def get_project_summary(project: str,
                            date_range: tuple = None) -> ToolResult:
        try:
            df = date_range[0] if date_range else None
            dt = date_range[1] if date_range else None
            result = TimeTrackingTool.list_time_entries(df, dt, project)
            if not result.success:
                return result
            entries = result.data or []
            total = sum(e.get("duration", 0) for e in entries)
            tasks: dict = {}
            for e in entries:
                t = e.get("task", "general")
                tasks[t] = tasks.get(t, 0) + e.get("duration", 0)
            summary = {
                "project": project,
                "total_seconds": total,
                "total_hours": round(total / 3600, 2),
                "entry_count": len(entries),
                "by_task": {k: {"seconds": v,
                                "hours": round(v / 3600, 2)}
                            for k, v in tasks.items()}
            }
            return ToolResult(True,
                              f"✓ {project}: {round(total/3600,2)}h",
                              summary)
        except Exception as e:
            return ToolResult(False, f"✗ get_project_summary failed: {e}")

    @staticmethod
    def calculate_billing(date_from: str, date_to: str,
                          hourly_rate: float, project: str = None) -> ToolResult:
        try:
            result = TimeTrackingTool.list_time_entries(
                date_from, date_to, project)
            if not result.success:
                return result
            entries = result.data or []
            total_secs = sum(e.get("duration", 0) for e in entries)
            hours = total_secs / 3600
            amount = round(hours * hourly_rate, 2)
            return ToolResult(True,
                              f"✓ {round(hours,2)}h × ${hourly_rate}/h = ${amount}",
                              {"hours": round(hours, 2),
                               "rate": hourly_rate,
                               "amount": amount,
                               "currency": "USD"})
        except Exception as e:
            return ToolResult(False, f"✗ calculate_billing failed: {e}")

    @staticmethod
    def export_to_invoice(date_from: str, date_to: str, client: str,
                          rate: float, output: str) -> ToolResult:
        try:
            billing = TimeTrackingTool.calculate_billing(
                date_from, date_to, rate)
            if not billing.success:
                return billing
            bd = billing.data
            timesheet = TimeTrackingTool.generate_timesheet(date_from, date_to)
            ts_text = timesheet.data.get("text", "") if timesheet.data else ""
            invoice = f"""# INVOICE

**To:** {client}
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Period:** {date_from} — {date_to}

---

## Summary

| Hours | Rate | Amount |
|-------|------|--------|
| {bd['hours']}h | ${bd['rate']}/h | ${bd['amount']} |

---

## Detail

{ts_text}

---

**TOTAL DUE: ${bd['amount']} USD**
"""
            Path(output).write_text(invoice, encoding="utf-8")
            return ToolResult(True,
                              f"✓ Invoice saved to {output} — ${bd['amount']}",
                              bd)
        except Exception as e:
            return ToolResult(False, f"✗ export_to_invoice failed: {e}")

    # ── Toggl ─────────────────────────────────────────────────────────────

    @staticmethod
    def connect_toggl(api_token: str) -> ToolResult:
        try:
            CredStore.save("toggl", {"api_token": api_token})
            return ToolResult(True, "✓ Toggl API token saved")
        except Exception as e:
            return ToolResult(False, f"✗ connect_toggl failed: {e}")

    @staticmethod
    def toggl_list_projects(cred_key: str = "toggl") -> ToolResult:
        try:
            import requests
            token = CredStore.load(cred_key).get("api_token", "")
            if not token:
                return ToolResult(False, "No Toggl token.")
            # get workspace id first
            me = requests.get(
                "https://api.track.toggl.com/api/v9/me",
                auth=(token, "api_token"), timeout=10).json()
            wid = me.get("default_workspace_id")
            resp = requests.get(
                f"https://api.track.toggl.com/api/v9/workspaces/{wid}/projects",
                auth=(token, "api_token"), timeout=10)
            resp.raise_for_status()
            projects = resp.json()
            return ToolResult(True, f"✓ {len(projects)} Toggl projects",
                              projects)
        except Exception as e:
            return ToolResult(False, f"✗ toggl_list_projects failed: {e}")

    @staticmethod
    def toggl_start_timer(project_id: int, description: str = "",
                          cred_key: str = "toggl") -> ToolResult:
        try:
            import requests
            token = CredStore.load(cred_key).get("api_token", "")
            me = requests.get(
                "https://api.track.toggl.com/api/v9/me",
                auth=(token, "api_token"), timeout=10).json()
            wid = me.get("default_workspace_id")
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            body = {
                "created_with": "npmai-agent",
                "description": description,
                "project_id": project_id,
                "start": now,
                "duration": -1,
                "workspace_id": wid
            }
            resp = requests.post(
                f"https://api.track.toggl.com/api/v9/workspaces/{wid}/time_entries",
                auth=(token, "api_token"), json=body, timeout=10)
            resp.raise_for_status()
            entry = resp.json()
            return ToolResult(True, f"✓ Toggl timer started: {entry.get('id')}", entry)
        except Exception as e:
            return ToolResult(False, f"✗ toggl_start_timer failed: {e}")

    # ── Clockify ──────────────────────────────────────────────────────────

    @staticmethod
    def connect_clockify(api_token: str) -> ToolResult:
        try:
            CredStore.save("clockify", {"api_token": api_token})
            return ToolResult(True, "✓ Clockify API token saved")
        except Exception as e:
            return ToolResult(False, f"✗ connect_clockify failed: {e}")

    @staticmethod
    def clockify_list_projects(workspace_id: str = None,
                                cred_key: str = "clockify") -> ToolResult:
        try:
            import requests
            token = CredStore.load(cred_key).get("api_token", "")
            if not token:
                return ToolResult(False, "No Clockify token.")
            headers = {"X-Api-Key": token}
            if not workspace_id:
                user = requests.get(
                    "https://api.clockify.me/api/v1/user",
                    headers=headers, timeout=10).json()
                workspace_id = user.get("defaultWorkspace", "")
            resp = requests.get(
                f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects",
                headers=headers, timeout=10)
            resp.raise_for_status()
            projects = resp.json()
            return ToolResult(True, f"✓ {len(projects)} Clockify projects",
                              projects)
        except Exception as e:
            return ToolResult(False, f"✗ clockify_list_projects failed: {e}")

    @staticmethod
    def clockify_time_entry(workspace_id: str, project_id: str,
                             description: str,
                             start: str, end: str,
                             cred_key: str = "clockify") -> ToolResult:
        try:
            import requests
            token = CredStore.load(cred_key).get("api_token", "")
            headers = {"X-Api-Key": token,
                       "Content-Type": "application/json"}

            def _fmt(dt_str: str) -> str:
                return (datetime.fromisoformat(dt_str)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"))

            body = {
                "start": _fmt(start),
                "end": _fmt(end),
                "description": description,
                "projectId": project_id
            }
            resp = requests.post(
                f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/time-entries",
                headers=headers, json=body, timeout=10)
            resp.raise_for_status()
            entry = resp.json()
            return ToolResult(True,
                              f"✓ Clockify entry logged: {entry.get('id')}",
                              entry)
        except Exception as e:
            return ToolResult(False, f"✗ clockify_time_entry failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Registry
# ─────────────────────────────────────────────────────────────────────────────

PRODUCTIVITY_TOOLS = {
    GoogleWorkspaceTool.name:  GoogleWorkspaceTool,
    NotionAdvancedTool.name:   NotionAdvancedTool,
    LinearTool.name:           LinearTool,
    AsanaTool.name:            AsanaTool,
    TrelloTool.name:           TrelloTool,
    ClickUpTool.name:          ClickUpTool,
    TodoistTool.name:          TodoistTool,
    ObsidianTool.name:         ObsidianTool,
    BookmarkManagerTool.name:  BookmarkManagerTool,
    TimeTrackingTool.name:     TimeTrackingTool,
}

PRODUCTIVITY_TOOLS_SUMMARY = "\n".join(
    f"- {k}: {v.description}"
    for k, v in PRODUCTIVITY_TOOLS.items()
)
