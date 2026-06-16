"""
tools_communication_extended.py
NPM Agent — NPMAI ECOSYSTEM by Sonu Kumar
Communication & Notification vertical: Teams, Zoom, Twilio, SendGrid,
Push Notifications, RSS, Webhooks, Calendar, ChatOps, SMTP Advanced
"""

import sys, subprocess

def _ensure(pkg: str, import_name: str = None):
    n = import_name or pkg
    try:
        __import__(n)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"], check=False)

for _p, _i in [
    ("requests",                  "requests"),
    ("twilio",                    "twilio"),
    ("sendgrid",                  "sendgrid"),
    ("firebase-admin",            "firebase_admin"),
    ("pywebpush",                 "pywebpush"),
    ("py-vapid",                  "py_vapid"),
    ("pushbullet.py",             "pushbullet"),
    ("feedparser",                "feedparser"),
    ("lxml",                      "lxml"),
    ("flask",                     "flask"),
    ("google-api-python-client",  "googleapiclient"),
    ("google-auth-oauthlib",      "google_auth_oauthlib"),
    ("google-auth-httplib2",      "google_auth_httplib2"),
    ("icalendar",                 "icalendar"),
    ("slack-sdk",                 "slack_sdk"),
    ("discord.py",                "discord"),
    ("pyTelegramBotAPI",          "telebot"),
    ("Jinja2",                    "jinja2"),
    ("cryptography",              "cryptography"),
]:
    if _p:
        _ensure(_p, _i)

from agent_core import ToolResult, CredStore


# ─────────────────────────────────────────────────────────────────────────────
# 1. MicrosoftTeamsTool
# ─────────────────────────────────────────────────────────────────────────────

class MicrosoftTeamsTool:
    name = "microsoft_teams"
    description = (
        "Microsoft Teams integration: send messages, adaptive cards, file notifications, "
        "mentions, and approval requests via Incoming Webhooks."
    )
    use = (
        """
Name of Tool:- MicrosoftTeamsTool,

Purpose of Tool:- 
The MicrosoftTeamsTool enables seamless integration with Microsoft Teams channels through Incoming Webhooks. 
It supports sending rich formatted messages using MessageCard format, Adaptive Cards, file sharing notifications, user mentions, and interactive approval request cards with action buttons. 
This tool is perfect for notifications, alerts, workflow approvals, file sharing updates, and team collaboration automation directly from agents or scripts without requiring full Graph API permissions.

Methods:-
- send_message: Sends a rich MessageCard with title, text, facts, and optional actions.
- send_adaptive_card: Sends a fully custom Adaptive Card payload.
- send_file_notification: Sends a notification about a shared file with direct open link.
- create_channel_message_with_mention: Sends a message that mentions a specific user by email.
- send_approval_request: Sends an interactive approval card with customizable action buttons.

How to use Tool Methods:-

1. send_message:
   - Purpose: Sends a standard rich MessageCard to a Teams channel with title, description, optional facts table, and action buttons.
   - Arguments:
     a) webhook_url: str - The Incoming Webhook URL for the target Teams channel (required).
     b) title: str - Main title of the message.
     c) text: str - Detailed message body.
     d) color: str (default: "0078D7") - Hex color code for the accent bar (without #).
     e) facts: list (default: None) - List of fact dictionaries (e.g., [{"name": "Status", "value": "Approved"}]).
     f) actions: list (default: None) - List of potentialAction objects for buttons.
   - How to call:
     MicrosoftTeamsTool.send_message(
         webhook_url="https://your-webhook-url",
         title="Deployment Completed",
         text="Version 2.3.1 has been deployed successfully.",
         color="00FF00",
         facts=[{"name": "Environment", "value": "Production"}]
     )

2. send_adaptive_card:
   - Purpose: Sends a completely custom Adaptive Card (more flexible layout, inputs, and actions).
   - Arguments:
     a) webhook_url: str - Teams webhook URL.
     b) card_json: dict - Full Adaptive Card JSON payload (must follow Adaptive Cards schema).
   - How to call: MicrosoftTeamsTool.send_adaptive_card(webhook_url=webhook, card_json={ "type": "AdaptiveCard", "body": [...], "actions": [...] })

3. send_file_notification:
   - Purpose: Sends a clean notification card when a file is ready for download or review, with a direct "Open File" button.
   - Arguments:
     a) webhook_url: str
     b) filename: str - Name of the file.
     c) url: str - Direct download or view URL for the file.
   - How to call: MicrosoftTeamsTool.send_file_notification(webhook_url=webhook, filename="report.pdf", url="https://example.com/report.pdf")

4. create_channel_message_with_mention:
   - Purpose: Sends a message that mentions a specific user (highlights their name and notifies them).
   - Arguments:
     a) webhook_url: str
     b) mention_email: str - Email address of the user to mention.
     c) message: str - The message content.
   - How to call: MicrosoftTeamsTool.create_channel_message_with_mention(webhook_url=webhook, mention_email="user@company.com", message="Please review the latest changes.")

5. send_approval_request:
   - Purpose: Sends an interactive approval card with action buttons (Approve/Reject or custom options). Note: Actual button responses require additional backend handling on the webhook side.
   - Arguments:
     a) webhook_url: str
     b) title: str - Approval title.
     c) description: str - Detailed request description.
     d) options: list (default: ["Approve", "Reject"]) - Custom button labels.
   - How to call: 
     MicrosoftTeamsTool.send_approval_request(
         webhook_url=webhook,
         title="Expense Approval",
         description="Request for $1500 travel reimbursement",
         options=["Approve", "Reject", "Need More Info"]
     )
""")
    
    @staticmethod
    def send_message(
        webhook_url: str,
        title: str,
        text: str,
        color: str = "0078D7",
        facts: list = None,
        actions: list = None,
    ) -> ToolResult:
        """Send a rich MessageCard to a Teams channel."""
        try:
            import requests

            card: dict = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "themeColor": color.lstrip("#"),
                "summary": title,
                "sections": [
                    {
                        "activityTitle": title,
                        "activityText": text,
                        "facts": facts or [],
                    }
                ],
            }
            if actions:
                card["potentialAction"] = actions

            r = requests.post(webhook_url, json=card, timeout=15)
            if r.status_code in (200, 204):
                return ToolResult(True, f"✓ Teams message sent: {title}")
            return ToolResult(False, f"✗ Teams responded {r.status_code}: {r.text[:200]}")
        except Exception as e:
            return ToolResult(False, f"✗ Teams send_message failed: {e}")

    @staticmethod
    def send_adaptive_card(webhook_url: str, card_json: dict) -> ToolResult:
        """Post a raw Adaptive Card payload to Teams."""
        try:
            import requests

            payload = {
                "type": "message",
                "attachments": [
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "content": card_json,
                    }
                ],
            }
            r = requests.post(webhook_url, json=payload, timeout=15)
            if r.status_code in (200, 204):
                return ToolResult(True, "✓ Adaptive card sent to Teams")
            return ToolResult(False, f"✗ Teams responded {r.status_code}: {r.text[:200]}")
        except Exception as e:
            return ToolResult(False, f"✗ Teams send_adaptive_card failed: {e}")

    @staticmethod
    def send_file_notification(
        webhook_url: str, filename: str, url: str
    ) -> ToolResult:
        """Notify a Teams channel that a file is available."""
        try:
            import requests

            card = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "themeColor": "0078D7",
                "summary": f"File ready: {filename}",
                "sections": [
                    {
                        "activityTitle": f"📎 {filename}",
                        "activitySubtitle": "A file has been shared with you.",
                    }
                ],
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": "Open File",
                        "targets": [{"os": "default", "uri": url}],
                    }
                ],
            }
            r = requests.post(webhook_url, json=card, timeout=15)
            if r.status_code in (200, 204):
                return ToolResult(True, f"✓ File notification sent for {filename}")
            return ToolResult(False, f"✗ Teams responded {r.status_code}: {r.text[:200]}")
        except Exception as e:
            return ToolResult(False, f"✗ Teams send_file_notification failed: {e}")

    @staticmethod
    def create_channel_message_with_mention(
        webhook_url: str, mention_email: str, message: str
    ) -> ToolResult:
        """Send a Teams message that mentions a specific user by email."""
        try:
            import requests

            card = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "themeColor": "FF5733",
                "summary": "Mention",
                "sections": [
                    {
                        "activityTitle": f"@{mention_email}",
                        "activityText": message,
                    }
                ],
            }
            r = requests.post(webhook_url, json=card, timeout=15)
            if r.status_code in (200, 204):
                return ToolResult(True, f"✓ Mention message sent to {mention_email}")
            return ToolResult(False, f"✗ Teams responded {r.status_code}: {r.text[:200]}")
        except Exception as e:
            return ToolResult(False, f"✗ Teams mention failed: {e}")

    @staticmethod
    def send_approval_request(
        webhook_url: str,
        title: str,
        description: str,
        options: list = None,
    ) -> ToolResult:
        """Send an approval-request card with action buttons to Teams."""
        try:
            import requests

            if options is None:
                options = ["Approve", "Reject"]

            actions = [
                {
                    "@type": "HttpPOST",
                    "name": opt,
                    "target": webhook_url,
                    "body": f'{{"response":"{opt}","title":"{title}"}}',
                }
                for opt in options
            ]
            card = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "themeColor": "FFA500",
                "summary": title,
                "sections": [
                    {
                        "activityTitle": f"🔔 Approval Required: {title}",
                        "activityText": description,
                    }
                ],
                "potentialAction": actions,
            }
            r = requests.post(webhook_url, json=card, timeout=15)
            if r.status_code in (200, 204):
                return ToolResult(True, f"✓ Approval request sent: {title}")
            return ToolResult(False, f"✗ Teams responded {r.status_code}: {r.text[:200]}")
        except Exception as e:
            return ToolResult(False, f"✗ Teams send_approval_request failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. ZoomTool
# ─────────────────────────────────────────────────────────────────────────────

class ZoomTool:
    name = "zoom"
    description = (
        "Zoom meeting automation: create/list/update/delete meetings, get participants, "
        "recordings, webinars, and registrants via Zoom OAuth2 API."
    )
    use = (
        """
Name of Tool:- ZoomTool,

Purpose of Tool:- 
The ZoomTool provides a comprehensive interface to the Zoom API for automating meeting and webinar management. 
It supports creating, listing, updating, deleting meetings and webinars, retrieving participant lists, accessing recordings, and managing registrants. 
Authentication is handled via Server-to-Server OAuth using Account Credentials (account_id, client_id, client_secret) stored in CredStore. 
This tool is ideal for scheduling automation, event management, post-meeting analytics, webinar operations, and agentic Zoom workflow integration.

Methods:-
- _get_token: Internal helper to obtain a fresh OAuth access token.
- _headers: Internal helper to generate authenticated headers.
- create_meeting: Creates a new scheduled Zoom meeting.
- list_meetings: Lists scheduled, live, or past meetings.
- get_meeting: Retrieves detailed information about a specific meeting.
- update_meeting: Updates settings of an existing meeting.
- delete_meeting: Deletes a meeting.
- get_meeting_participants: Gets participant list for a past meeting.
- get_recording: Retrieves recording information for a meeting.
- list_recordings: Lists recordings within a date range.
- create_webinar: Creates a new scheduled webinar.
- get_registrants: Retrieves list of webinar registrants.

How to use Tool Methods:-

1. _get_token (Internal Authentication Helper):
   - Purpose: Obtains a short-lived OAuth2 access token using Server-to-Server OAuth (Account Credentials flow).
   - Arguments: cred_key: str (default: "zoom")
   - Credential requirement in CredStore: {'account_id': '...', 'client_id': '...', 'client_secret': '...'}
   - Note: Called automatically by _headers(). Do not call directly.

2. _headers (Internal Helper):
   - Purpose: Returns authorization headers with a fresh Bearer token.
   - Arguments: cred_key: str (default: "zoom")
   - Note: Internal method used by all API calls.

3. create_meeting:
   - Purpose: Creates a new scheduled Zoom meeting with customizable settings.
   - Arguments:
     a) topic: str - Meeting title.
     b) start_time: str - Start time in ISO 8601 format (e.g., "2026-06-20T14:00:00Z").
     c) duration: int (default: 60) - Duration in minutes.
     d) agenda: str (default: "") - Meeting description.
     e) password: str (default: "") - Meeting password.
     f) waiting_room: bool (default: True) - Enable waiting room.
     g) cred_key: str (default: "zoom").
   - Returns: Full meeting details including join_url, start_url, ID, etc.
   - How to call: 
     ZoomTool.create_meeting(
         topic="Team Sync",
         start_time="2026-06-20T15:00:00Z",
         duration=45,
         waiting_room=True
     )

4. list_meetings:
   - Purpose: Lists meetings for the authenticated user.
   - Arguments:
     a) type: str (default: "scheduled") - "scheduled", "live", "upcoming", "previous".
     b) page_size: int (default: 30).
     c) cred_key.
   - Returns: List of meeting objects.
   - How to call: ZoomTool.list_meetings(type="scheduled")

5. get_meeting:
   - Purpose: Retrieves complete details of a specific meeting.
   - Arguments:
     a) meeting_id: str - Meeting ID or UUID.
     b) cred_key.
   - How to call: ZoomTool.get_meeting(meeting_id="123456789")

6. update_meeting:
   - Purpose: Updates settings of an existing meeting.
   - Arguments:
     a) meeting_id: str
     b) data: dict - Fields to update (topic, start_time, duration, settings, etc.).
     c) cred_key.
   - How to call: ZoomTool.update_meeting(meeting_id="123456789", data={"topic": "Updated Title", "duration": 90})

7. delete_meeting:
   - Purpose: Deletes a meeting permanently.
   - Arguments: meeting_id, cred_key.
   - How to call: ZoomTool.delete_meeting(meeting_id="123456789")

8. get_meeting_participants:
   - Purpose: Retrieves list of participants who joined a past meeting (requires past meeting ID).
   - Arguments: meeting_id, cred_key.
   - Returns: List of participants with name, email, join/leave time, duration, etc.
   - How to call: ZoomTool.get_meeting_participants(meeting_id="123456789")

9. get_recording:
   - Purpose: Gets recording details and download links for a meeting.
   - Arguments: meeting_id, cred_key.
   - How to call: ZoomTool.get_recording(meeting_id="123456789")

10. list_recordings:
    - Purpose: Lists all recordings for the user within a date range.
    - Arguments:
      a) from_date: str - Start date (YYYY-MM-DD).
      b) to_date: str - End date (YYYY-MM-DD).
      c) cred_key.
    - How to call: ZoomTool.list_recordings(from_date="2026-06-01", to_date="2026-06-30")

11. create_webinar:
    - Purpose: Creates a new scheduled webinar.
    - Arguments:
      a) topic: str
      b) start_time: str (ISO format)
      c) duration: int (default: 60)
      d) agenda: str (default: "")
      e) cred_key.
    - Returns: Webinar details including join_url and registration URL.
    - How to call: Similar to create_meeting.

12. get_registrants:
    - Purpose: Retrieves list of people who registered for a webinar.
    - Arguments: webinar_id, cred_key.
    - Returns: List of registrants with name, email, status, etc.
    - How to call: ZoomTool.get_registrants(webinar_id="987654321")
""")

    @staticmethod
    def _get_token(cred_key: str = "zoom") -> str:
        import requests

        creds = CredStore.load(cred_key)
        account_id    = creds.get("account_id", "")
        client_id     = creds.get("client_id", "")
        client_secret = creds.get("client_secret", "")
        if not all([account_id, client_id, client_secret]):
            raise ValueError("Missing Zoom credentials (account_id, client_id, client_secret).")
        r = requests.post(
            "https://zoom.us/oauth/token",
            params={"grant_type": "account_credentials", "account_id": account_id},
            auth=(client_id, client_secret),
            timeout=15,
        )
        r.raise_for_status()
        return r.json()["access_token"]

    @staticmethod
    def _headers(cred_key: str = "zoom") -> dict:
        return {"Authorization": f"Bearer {ZoomTool._get_token(cred_key)}",
                "Content-Type": "application/json"}

    @staticmethod
    def create_meeting(
        topic: str,
        start_time: str,
        duration: int = 60,
        agenda: str = "",
        password: str = "",
        waiting_room: bool = True,
        cred_key: str = "zoom",
    ) -> ToolResult:
        try:
            import requests

            payload = {
                "topic": topic,
                "type": 2,
                "start_time": start_time,
                "duration": duration,
                "agenda": agenda,
                "password": password,
                "settings": {
                    "waiting_room": waiting_room,
                    "join_before_host": not waiting_room,
                },
            }
            r = requests.post(
                "https://api.zoom.us/v2/users/me/meetings",
                headers=ZoomTool._headers(cred_key),
                json=payload,
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            return ToolResult(
                True,
                f"✓ Zoom meeting created: {data.get('join_url')}",
                data,
            )
        except Exception as e:
            return ToolResult(False, f"✗ Zoom create_meeting failed: {e}")

    @staticmethod
    def list_meetings(
        type: str = "scheduled",
        page_size: int = 30,
        cred_key: str = "zoom",
    ) -> ToolResult:
        try:
            import requests

            r = requests.get(
                "https://api.zoom.us/v2/users/me/meetings",
                headers=ZoomTool._headers(cred_key),
                params={"type": type, "page_size": page_size},
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            meetings = data.get("meetings", [])
            return ToolResult(True, f"✓ {len(meetings)} meetings found", meetings)
        except Exception as e:
            return ToolResult(False, f"✗ Zoom list_meetings failed: {e}")

    @staticmethod
    def get_meeting(meeting_id: str, cred_key: str = "zoom") -> ToolResult:
        try:
            import requests

            r = requests.get(
                f"https://api.zoom.us/v2/meetings/{meeting_id}",
                headers=ZoomTool._headers(cred_key),
                timeout=15,
            )
            r.raise_for_status()
            return ToolResult(True, "✓ Meeting details fetched", r.json())
        except Exception as e:
            return ToolResult(False, f"✗ Zoom get_meeting failed: {e}")

    @staticmethod
    def update_meeting(
        meeting_id: str, data: dict, cred_key: str = "zoom"
    ) -> ToolResult:
        try:
            import requests

            r = requests.patch(
                f"https://api.zoom.us/v2/meetings/{meeting_id}",
                headers=ZoomTool._headers(cred_key),
                json=data,
                timeout=15,
            )
            r.raise_for_status()
            return ToolResult(True, f"✓ Meeting {meeting_id} updated")
        except Exception as e:
            return ToolResult(False, f"✗ Zoom update_meeting failed: {e}")

    @staticmethod
    def delete_meeting(meeting_id: str, cred_key: str = "zoom") -> ToolResult:
        try:
            import requests

            r = requests.delete(
                f"https://api.zoom.us/v2/meetings/{meeting_id}",
                headers=ZoomTool._headers(cred_key),
                timeout=15,
            )
            r.raise_for_status()
            return ToolResult(True, f"✓ Meeting {meeting_id} deleted")
        except Exception as e:
            return ToolResult(False, f"✗ Zoom delete_meeting failed: {e}")

    @staticmethod
    def get_meeting_participants(
        meeting_id: str, cred_key: str = "zoom"
    ) -> ToolResult:
        try:
            import requests

            r = requests.get(
                f"https://api.zoom.us/v2/past_meetings/{meeting_id}/participants",
                headers=ZoomTool._headers(cred_key),
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            participants = data.get("participants", [])
            return ToolResult(True, f"✓ {len(participants)} participants", participants)
        except Exception as e:
            return ToolResult(False, f"✗ Zoom get_meeting_participants failed: {e}")

    @staticmethod
    def get_recording(meeting_id: str, cred_key: str = "zoom") -> ToolResult:
        try:
            import requests

            r = requests.get(
                f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings",
                headers=ZoomTool._headers(cred_key),
                timeout=15,
            )
            r.raise_for_status()
            return ToolResult(True, "✓ Recording info fetched", r.json())
        except Exception as e:
            return ToolResult(False, f"✗ Zoom get_recording failed: {e}")

    @staticmethod
    def list_recordings(
        from_date: str, to_date: str, cred_key: str = "zoom"
    ) -> ToolResult:
        try:
            import requests

            r = requests.get(
                "https://api.zoom.us/v2/users/me/recordings",
                headers=ZoomTool._headers(cred_key),
                params={"from": from_date, "to": to_date},
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            meetings = data.get("meetings", [])
            return ToolResult(True, f"✓ {len(meetings)} recording(s) found", meetings)
        except Exception as e:
            return ToolResult(False, f"✗ Zoom list_recordings failed: {e}")

    @staticmethod
    def create_webinar(
        topic: str,
        start_time: str,
        duration: int = 60,
        agenda: str = "",
        cred_key: str = "zoom",
    ) -> ToolResult:
        try:
            import requests

            payload = {
                "topic": topic,
                "type": 5,
                "start_time": start_time,
                "duration": duration,
                "agenda": agenda,
            }
            r = requests.post(
                "https://api.zoom.us/v2/users/me/webinars",
                headers=ZoomTool._headers(cred_key),
                json=payload,
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            return ToolResult(True, f"✓ Webinar created: {data.get('join_url')}", data)
        except Exception as e:
            return ToolResult(False, f"✗ Zoom create_webinar failed: {e}")

    @staticmethod
    def get_registrants(webinar_id: str, cred_key: str = "zoom") -> ToolResult:
        try:
            import requests

            r = requests.get(
                f"https://api.zoom.us/v2/webinars/{webinar_id}/registrants",
                headers=ZoomTool._headers(cred_key),
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            registrants = data.get("registrants", [])
            return ToolResult(True, f"✓ {len(registrants)} registrant(s)", registrants)
        except Exception as e:
            return ToolResult(False, f"✗ Zoom get_registrants failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. TwilioTool
# ─────────────────────────────────────────────────────────────────────────────

class TwilioTool:
    name = "twilio"
    description = (
        "Twilio SMS, voice calls, WhatsApp Business, verification, and subaccount management."
    )
    use  = (
        """
Name of Tool:- TwilioTool,

Purpose of Tool:- 
The TwilioTool provides a comprehensive interface to the Twilio API for communication automation. 
It supports sending SMS and WhatsApp messages (including templates), making voice calls, checking call and message status, bulk messaging, phone number verification (OTP), listing message history, creating subaccounts, and retrieving account balance. 
All operations use the official Twilio Python client with credentials (account_sid, auth_token, and optional from numbers / verify service) loaded from CredStore. 
This tool is ideal for customer notifications, marketing campaigns, 2FA/verification flows, voice broadcasting, and agentic communication workflows.

Methods:-
- _client: Internal helper to initialize the Twilio REST client.
- send_sms: Sends a standard SMS message.
- send_bulk_sms: Sends the same message to multiple recipients.
- make_call: Initiates an outbound voice call (with TwiML or URL).
- get_call_status: Retrieves the current status of a voice call.
- send_whatsapp: Sends a WhatsApp message (text or with media).
- send_whatsapp_template: Sends a WhatsApp Business template message.
- get_message_status: Checks delivery status of an SMS/WhatsApp message.
- list_messages: Lists recent messages with optional filters.
- verify_phone: Starts a phone number verification (OTP) via SMS or call.
- check_verification: Validates a verification code.
- create_subaccount: Creates a new Twilio subaccount.
- get_account_balance: Retrieves the current account balance.

How to use Tool Methods:-

1. _client (Internal Authentication Helper):
   - Purpose: Creates and returns an authenticated Twilio REST Client instance.
   - Arguments: cred_key: str (default: "twilio")
   - Credential requirement in CredStore: {'account_sid': '...', 'auth_token': '...', 'from_number': '...', 'whatsapp_from': '...', 'verify_service_sid': '...'}
   - Note: Internal method. Do not call directly.

2. send_sms:
   - Purpose: Sends a standard text SMS message.
   - Arguments:
     a) to: str - Recipient phone number in E.164 format (e.g., "+1234567890").
     b) body: str - Message content.
     c) from_number: str (default: None) - Override sender number from credentials.
     d) cred_key: str (default: "twilio").
   - Returns: Message SID on success.
   - How to call: TwilioTool.send_sms(to="+1234567890", body="Hello from NPM Agent!")

3. send_bulk_sms:
   - Purpose: Sends the same SMS to multiple recipients with individual error handling.
   - Arguments:
     a) numbers: list - List of phone numbers in E.164 format.
     b) message: str - Message body.
     c) from_number: str (optional).
     d) cred_key.
   - Returns: Detailed results array with success/failure per recipient.
   - How to call: TwilioTool.send_bulk_sms(numbers=["+1...", "+91..."], message="Promo alert!")

4. make_call:
   - Purpose: Initiates an outbound voice call.
   - Arguments:
     a) to: str - Recipient phone number.
     b) from_number: str (optional).
     c) url_or_twiml: str - Either a TwiML URL or raw TwiML XML string.
     d) cred_key.
   - Returns: Call SID.
   - How to call: TwilioTool.make_call(to="+1234567890", url_or_twiml="http://demo.twilio.com/docs/voice.xml")

5. get_call_status:
   - Purpose: Checks the real-time status of a voice call.
   - Arguments: call_sid: str, cred_key.
   - Returns: Status and duration.
   - How to call: TwilioTool.get_call_status(call_sid="CAxxxxxxxxxxxxxxxx")

6. send_whatsapp:
   - Purpose: Sends a WhatsApp message (text or with media attachment).
   - Arguments:
     a) to: str - Recipient WhatsApp number (without "whatsapp:").
     b) body: str - Message text.
     c) from_number: str (optional) - WhatsApp sender number from credentials.
     d) media_url: str (optional) - URL of image/video/document.
     e) cred_key.
   - How to call: TwilioTool.send_whatsapp(to="919876543210", body="Hello!", media_url="https://example.com/image.jpg")

7. send_whatsapp_template:
   - Purpose: Sends a pre-approved WhatsApp Business template message with variables.
   - Arguments:
     a) to: str
     b) template_sid: str - WhatsApp template SID.
     c) variables: dict (default: None) - Template parameters.
     d) from_number, cred_key.
   - How to call: TwilioTool.send_whatsapp_template(to="919876543210", template_sid="HX...", variables={"1": "John"})

8. get_message_status:
   - Purpose: Retrieves delivery status of an SMS or WhatsApp message.
   - Arguments: message_sid, cred_key.
   - How to call: TwilioTool.get_message_status(message_sid="SMxxxxxxxxxxxxxxxx")

9. list_messages:
   - Purpose: Retrieves a filtered list of sent/received messages.
   - Arguments:
     a) from_date: str (ISO) - Filter after this date.
     b) to_date: str (ISO)
     c) to: str - Recipient filter.
     d) from_num: str - Sender filter.
     e) cred_key.
   - Returns: List of message summaries.
   - How to call: TwilioTool.list_messages(from_date="2026-06-01", to="+1234567890")

10. verify_phone:
    - Purpose: Starts a verification process (OTP) via SMS or voice call.
    - Arguments:
      a) phone_number: str - Number to verify.
      b) channel: str (default: "sms") - "sms" or "call".
      c) cred_key (must have verify_service_sid).
    - How to call: TwilioTool.verify_phone(phone_number="+1234567890", channel="sms")

11. check_verification:
    - Purpose: Validates the OTP code entered by the user.
    - Arguments: phone, code, cred_key.
    - Returns: Approval status.
    - How to call: TwilioTool.check_verification(phone="+1234567890", code="123456")

12. create_subaccount:
    - Purpose: Creates a new Twilio subaccount for isolated billing/permissions.
    - Arguments: friendly_name: str, cred_key.
    - How to call: TwilioTool.create_subaccount(friendly_name="Marketing Campaign")

13. get_account_balance:
    - Purpose: Retrieves the current account balance and currency.
    - Arguments: cred_key.
    - How to call: TwilioTool.get_account_balance()
""")

    @staticmethod
    def _client(cred_key: str = "twilio"):
        from twilio.rest import Client

        creds = CredStore.load(cred_key)
        return Client(creds.get("account_sid", ""), creds.get("auth_token", ""))

    @staticmethod
    def send_sms(
        to: str,
        body: str,
        from_number: str = None,
        cred_key: str = "twilio",
    ) -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            from_num = from_number or CredStore.load(cred_key).get("from_number", "")
            msg = client.messages.create(body=body, from_=from_num, to=to)
            return ToolResult(True, f"✓ SMS sent to {to} (SID: {msg.sid})", {"sid": msg.sid})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio send_sms failed: {e}")

    @staticmethod
    def send_bulk_sms(
        numbers: list,
        message: str,
        from_number: str = None,
        cred_key: str = "twilio",
    ) -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            from_num = from_number or CredStore.load(cred_key).get("from_number", "")
            results = []
            for number in numbers:
                try:
                    msg = client.messages.create(body=message, from_=from_num, to=number)
                    results.append({"to": number, "sid": msg.sid, "status": "sent"})
                except Exception as ex:
                    results.append({"to": number, "error": str(ex), "status": "failed"})
            sent = sum(1 for r in results if r["status"] == "sent")
            return ToolResult(True, f"✓ Bulk SMS: {sent}/{len(numbers)} sent", results)
        except Exception as e:
            return ToolResult(False, f"✗ Twilio send_bulk_sms failed: {e}")

    @staticmethod
    def make_call(
        to: str,
        from_number: str = None,
        url_or_twiml: str = "http://demo.twilio.com/docs/voice.xml",
        cred_key: str = "twilio",
    ) -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            from_num = from_number or CredStore.load(cred_key).get("from_number", "")
            if url_or_twiml.strip().startswith("<"):
                from twilio.twiml.voice_response import VoiceResponse
                twiml_url = None
                twiml = url_or_twiml
                call = client.calls.create(twiml=twiml, from_=from_num, to=to)
            else:
                call = client.calls.create(url=url_or_twiml, from_=from_num, to=to)
            return ToolResult(True, f"✓ Call initiated to {to} (SID: {call.sid})", {"sid": call.sid})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio make_call failed: {e}")

    @staticmethod
    def get_call_status(call_sid: str, cred_key: str = "twilio") -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            call = client.calls(call_sid).fetch()
            return ToolResult(True, f"✓ Call status: {call.status}", {"status": call.status, "duration": call.duration})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio get_call_status failed: {e}")

    @staticmethod
    def send_whatsapp(
        to: str,
        body: str,
        from_number: str = None,
        media_url: str = None,
        cred_key: str = "twilio",
    ) -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            from_num = from_number or CredStore.load(cred_key).get("whatsapp_from", "")
            kwargs = {
                "body": body,
                "from_": f"whatsapp:{from_num}",
                "to": f"whatsapp:{to}",
            }
            if media_url:
                kwargs["media_url"] = [media_url]
            msg = client.messages.create(**kwargs)
            return ToolResult(True, f"✓ WhatsApp sent to {to} (SID: {msg.sid})", {"sid": msg.sid})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio send_whatsapp failed: {e}")

    @staticmethod
    def send_whatsapp_template(
        to: str,
        template_sid: str,
        variables: dict = None,
        from_number: str = None,
        cred_key: str = "twilio",
    ) -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            from_num = from_number or CredStore.load(cred_key).get("whatsapp_from", "")
            import json
            msg = client.messages.create(
                from_=f"whatsapp:{from_num}",
                to=f"whatsapp:{to}",
                content_sid=template_sid,
                content_variables=json.dumps(variables or {}),
            )
            return ToolResult(True, f"✓ WhatsApp template sent (SID: {msg.sid})", {"sid": msg.sid})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio send_whatsapp_template failed: {e}")

    @staticmethod
    def get_message_status(message_sid: str, cred_key: str = "twilio") -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            msg = client.messages(message_sid).fetch()
            return ToolResult(True, f"✓ Message status: {msg.status}", {"status": msg.status, "error_code": msg.error_code})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio get_message_status failed: {e}")

    @staticmethod
    def list_messages(
        from_date: str = None,
        to_date: str = None,
        to: str = None,
        from_num: str = None,
        cred_key: str = "twilio",
    ) -> ToolResult:
        try:
            from datetime import datetime
            client = TwilioTool._client(cred_key)
            kwargs = {}
            if from_date:
                kwargs["date_sent_after"] = datetime.fromisoformat(from_date)
            if to_date:
                kwargs["date_sent_before"] = datetime.fromisoformat(to_date)
            if to:
                kwargs["to"] = to
            if from_num:
                kwargs["from_"] = from_num
            messages = client.messages.list(**kwargs, limit=50)
            data = [{"sid": m.sid, "to": m.to, "from": m.from_, "status": m.status, "body": m.body[:80]} for m in messages]
            return ToolResult(True, f"✓ {len(data)} messages listed", data)
        except Exception as e:
            return ToolResult(False, f"✗ Twilio list_messages failed: {e}")

    @staticmethod
    def verify_phone(
        phone_number: str,
        channel: str = "sms",
        cred_key: str = "twilio",
    ) -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            service_sid = CredStore.load(cred_key).get("verify_service_sid", "")
            if not service_sid:
                return ToolResult(False, "✗ Missing verify_service_sid in credentials.")
            verification = client.verify.v2.services(service_sid).verifications.create(
                to=phone_number, channel=channel
            )
            return ToolResult(True, f"✓ Verification sent via {channel} to {phone_number}", {"status": verification.status})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio verify_phone failed: {e}")

    @staticmethod
    def check_verification(
        phone: str, code: str, cred_key: str = "twilio"
    ) -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            service_sid = CredStore.load(cred_key).get("verify_service_sid", "")
            check = client.verify.v2.services(service_sid).verification_checks.create(
                to=phone, code=code
            )
            approved = check.status == "approved"
            return ToolResult(approved, f"✓ Verification {'approved' if approved else 'failed'}", {"status": check.status})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio check_verification failed: {e}")

    @staticmethod
    def create_subaccount(
        friendly_name: str, cred_key: str = "twilio"
    ) -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            account = client.api.v2010.accounts.create(friendly_name=friendly_name)
            return ToolResult(True, f"✓ Subaccount created: {account.sid}", {"sid": account.sid, "friendly_name": account.friendly_name})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio create_subaccount failed: {e}")

    @staticmethod
    def get_account_balance(cred_key: str = "twilio") -> ToolResult:
        try:
            client = TwilioTool._client(cred_key)
            balance = client.api.v2010.balance.fetch()
            return ToolResult(True, f"✓ Balance: {balance.balance} {balance.currency}", {"balance": balance.balance, "currency": balance.currency})
        except Exception as e:
            return ToolResult(False, f"✗ Twilio get_account_balance failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. SendGridTool
# ─────────────────────────────────────────────────────────────────────────────

class SendGridTool:
    name = "sendgrid"
    description = (
        "SendGrid transactional email at scale: single/bulk sends, templates, contact lists, "
        "campaigns, scheduling, and stats."
    )
    use = (
        """
Name of Tool:- SendGridTool,

Purpose of Tool:- 
The SendGridTool provides a comprehensive interface to the SendGrid email delivery platform for transactional and marketing emails. 
It supports single and bulk email sending, dynamic templates, contact list management, campaign creation and scheduling, email statistics, and suppression list management (bounces and spam reports). 
All operations use the official SendGrid Python library and REST API with an API key stored in CredStore. 
This tool is ideal for automated customer notifications, marketing campaigns, transactional emails, deliverability monitoring, and agentic email communication workflows at scale.

Methods:-
- _api_key: Internal helper to retrieve the SendGrid API key from credentials.
- send_email: Sends a single rich HTML email with optional attachments.
- send_bulk: Sends personalized bulk emails to multiple recipients.
- send_with_template: Sends an email using a pre-designed SendGrid dynamic template.
- create_template: Creates a new dynamic email template.
- update_template: Updates an existing template.
- list_templates: Lists all dynamic templates.
- create_contact_list: Creates a new marketing contact list.
- add_contacts: Adds contacts to a marketing list.
- create_campaign: Creates a marketing campaign.
- schedule_campaign: Schedules a campaign for future sending.
- get_stats: Retrieves email performance statistics.
- get_bounces: Retrieves bounce records.
- delete_bounce: Removes a specific email from the bounce suppression list.
- get_spam_reports: Retrieves spam report records.

How to use Tool Methods:-

1. _api_key (Internal Authentication Helper):
   - Purpose: Retrieves the SendGrid API key from CredStore.
   - Arguments: cred_key: str (default: "sendgrid")
   - Credential requirement: CredStore must contain {'api_key': 'SG.xxxxxxxxxxxxxxxxxxxxxxx', 'from_email': 'noreply@example.com'}
   - Note: Internal method. Do not call directly.

2. send_email:
   - Purpose: Sends a single transactional or marketing email with HTML content and optional attachments.
   - Arguments:
     a) to: str - Recipient email address.
     b) subject: str - Email subject line.
     c) html_content: str - Full HTML body of the email.
     d) from_email: str (default: None) - Override sender email from credentials.
     e) from_name: str (default: "NPM Agent") - Sender display name.
     f) reply_to: str (default: None).
     g) attachments: list (default: None) - List of local file paths to attach.
     h) cred_key: str (default: "sendgrid").
   - Returns: Status code confirmation.
   - How to call: 
     SendGridTool.send_email(
         to="user@example.com",
         subject="Welcome to Our Platform",
         html_content="<h1>Hello!</h1><p>Welcome message...</p>",
         attachments=["/path/to/invoice.pdf"]
     )

3. send_bulk:
   - Purpose: Sends the same (or lightly personalized) email to multiple recipients efficiently.
   - Arguments:
     a) recipients: list - List of email strings or dicts containing email + substitution data.
     b) subject: str
     c) html_template: str - HTML content (can contain substitution placeholders).
     d) from_email: str (optional)
     e) substitutions: dict (optional) - Global substitutions.
     f) cred_key.
   - Returns: Success status and count of recipients.
   - How to call: SendGridTool.send_bulk(recipients=["a@example.com", "b@example.com"], subject="Promo", html_template=html)

4. send_with_template:
   - Purpose: Sends an email using a pre-built SendGrid dynamic template with dynamic data.
   - Arguments:
     a) to: str
     b) template_id: str - SendGrid template ID.
     c) dynamic_data: dict - Data to populate template variables.
     d) from_email: str (optional)
     e) cred_key.
   - How to call: SendGridTool.send_with_template(to="user@example.com", template_id="d-abc123", dynamic_data={"name": "John", "order_id": "12345"})

5. create_template:
   - Purpose: Creates a new dynamic template and its first version in SendGrid.
   - Arguments:
     a) name: str - Template name.
     b) subject: str - Default subject.
     c) html_content: str - HTML body.
     d) plain_content: str (default: "") - Plain text version.
     e) cred_key.
   - Returns: Template ID.
   - How to call: SendGridTool.create_template(name="Welcome Email", subject="Welcome!", html_content=html)

6. update_template:
   - Purpose: Updates an existing template's metadata.
   - Arguments:
     a) template_id: str
     b) data: dict - Fields to update.
     c) cred_key.
   - How to call: SendGridTool.update_template(template_id="d-abc123", data={"name": "New Name"})

7. list_templates:
   - Purpose: Lists all dynamic templates in the account.
   - Arguments: cred_key.
   - How to call: SendGridTool.list_templates()

8. create_contact_list:
   - Purpose: Creates a new marketing contact list.
   - Arguments: name: str, cred_key.
   - How to call: SendGridTool.create_contact_list(name="Newsletter Subscribers")

9. add_contacts:
   - Purpose: Adds one or more contacts to a marketing list.
   - Arguments:
     a) list_id: str
     b) contacts: list - List of contact dictionaries (email + custom fields).
     c) cred_key.
   - How to call: SendGridTool.add_contacts(list_id="list-abc123", contacts=[{"email": "user@example.com", "first_name": "John"}])

10. create_campaign:
    - Purpose: Creates a marketing campaign.
    - Arguments:
      a) name: str
      b) subject: str
      c) from_email: str
      d) html_content: str
      e) list_ids: list - Target contact list IDs.
      f) cred_key.
    - How to call: SendGridTool.create_campaign(name="Summer Sale", subject="Big Sale!", from_email="marketing@...", html_content=html, list_ids=["list1"])

11. schedule_campaign:
    - Purpose: Schedules a campaign to be sent at a future time.
    - Arguments:
      a) campaign_id: str
      b) send_at: str - ISO 8601 timestamp.
      c) cred_key.
    - How to call: SendGridTool.schedule_campaign(campaign_id="campaign-123", send_at="2026-06-20T10:00:00Z")

12. get_stats:
    - Purpose: Retrieves email performance statistics (opens, clicks, bounces, etc.).
    - Arguments:
      a) start_date: str (YYYY-MM-DD)
      b) end_date: str (YYYY-MM-DD)
      c) aggregated_by: str (default: "day")
      d) cred_key.
    - How to call: SendGridTool.get_stats(start_date="2026-06-01", end_date="2026-06-15")

13. get_bounces / delete_bounce / get_spam_reports:
    - Purpose: Manage suppression lists (bounces and spam reports) for better deliverability.
    - How to call: SendGridTool.get_bounces(start_date="2026-06-01") or SendGridTool.delete_bounce(email="bad@example.com")
""")
    
    @staticmethod
    def _api_key(cred_key: str = "sendgrid") -> str:
        key = CredStore.load(cred_key).get("api_key", "")
        if not key:
            raise ValueError("No SendGrid api_key in credentials.")
        return key

    @staticmethod
    def send_email(
        to: str,
        subject: str,
        html_content: str,
        from_email: str = None,
        from_name: str = "NPM Agent",
        reply_to: str = None,
        attachments: list = None,
        cred_key: str = "sendgrid",
    ) -> ToolResult:
        try:
            import sendgrid
            from sendgrid.helpers.mail import (
                Mail, To, From, ReplyTo, Attachment, FileContent,
                FileName, FileType, Disposition,
            )
            import base64, os

            creds = CredStore.load(cred_key)
            from_addr = from_email or creds.get("from_email", "noreply@example.com")

            message = Mail(
                from_email=From(from_addr, from_name),
                to_emails=To(to),
                subject=subject,
                html_content=html_content,
            )
            if reply_to:
                message.reply_to = ReplyTo(reply_to)
            if attachments:
                for path in attachments:
                    with open(path, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode()
                    att = Attachment(
                        FileContent(encoded),
                        FileName(os.path.basename(path)),
                        FileType("application/octet-stream"),
                        Disposition("attachment"),
                    )
                    message.attachment = att

            sg = sendgrid.SendGridAPIClient(api_key=SendGridTool._api_key(cred_key))
            response = sg.send(message)
            return ToolResult(
                response.status_code in (200, 202),
                f"✓ Email sent to {to} (status {response.status_code})",
                {"status_code": response.status_code},
            )
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid send_email failed: {e}")

    @staticmethod
    def send_bulk(
        recipients: list,
        subject: str,
        html_template: str,
        from_email: str = None,
        substitutions: dict = None,
        cred_key: str = "sendgrid",
    ) -> ToolResult:
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail, Personalization, To

            creds = CredStore.load(cred_key)
            from_addr = from_email or creds.get("from_email", "noreply@example.com")

            message = Mail(from_email=from_addr, subject=subject, html_content=html_template)
            for recipient in recipients:
                p = Personalization()
                email = recipient if isinstance(recipient, str) else recipient.get("email", "")
                p.add_to(To(email))
                if substitutions:
                    for key, val in substitutions.items():
                        p.add_substitution(key, val)
                if isinstance(recipient, dict):
                    for k, v in recipient.items():
                        if k != "email":
                            p.add_substitution(f"-{k}-", str(v))
                message.add_personalization(p)

            sg = sendgrid.SendGridAPIClient(api_key=SendGridTool._api_key(cred_key))
            response = sg.send(message)
            return ToolResult(
                response.status_code in (200, 202),
                f"✓ Bulk email sent to {len(recipients)} recipients",
                {"status_code": response.status_code},
            )
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid send_bulk failed: {e}")

    @staticmethod
    def send_with_template(
        to: str,
        template_id: str,
        dynamic_data: dict,
        from_email: str = None,
        cred_key: str = "sendgrid",
    ) -> ToolResult:
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail, DynamicTemplateData

            creds = CredStore.load(cred_key)
            from_addr = from_email or creds.get("from_email", "noreply@example.com")
            message = Mail(from_email=from_addr, to_emails=to)
            message.template_id = template_id
            message.dynamic_template_data = dynamic_data

            sg = sendgrid.SendGridAPIClient(api_key=SendGridTool._api_key(cred_key))
            response = sg.send(message)
            return ToolResult(
                response.status_code in (200, 202),
                f"✓ Template email sent to {to}",
            )
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid send_with_template failed: {e}")

    @staticmethod
    def create_template(
        name: str,
        subject: str,
        html_content: str,
        plain_content: str = "",
        cred_key: str = "sendgrid",
    ) -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}", "Content-Type": "application/json"}
            r = requests.post("https://api.sendgrid.com/v3/templates", headers=headers, json={"name": name, "generation": "dynamic"}, timeout=15)
            r.raise_for_status()
            template_id = r.json()["id"]

            version_payload = {
                "name": "Version 1",
                "subject": subject,
                "html_content": html_content,
                "plain_content": plain_content,
                "active": 1,
            }
            rv = requests.post(f"https://api.sendgrid.com/v3/templates/{template_id}/versions", headers=headers, json=version_payload, timeout=15)
            rv.raise_for_status()
            return ToolResult(True, f"✓ Template created: {template_id}", {"template_id": template_id})
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid create_template failed: {e}")

    @staticmethod
    def update_template(
        template_id: str, data: dict, cred_key: str = "sendgrid"
    ) -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}", "Content-Type": "application/json"}
            r = requests.patch(f"https://api.sendgrid.com/v3/templates/{template_id}", headers=headers, json=data, timeout=15)
            r.raise_for_status()
            return ToolResult(True, f"✓ Template {template_id} updated")
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid update_template failed: {e}")

    @staticmethod
    def list_templates(cred_key: str = "sendgrid") -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}"}
            r = requests.get("https://api.sendgrid.com/v3/templates?generations=dynamic", headers=headers, timeout=15)
            r.raise_for_status()
            templates = r.json().get("templates", [])
            return ToolResult(True, f"✓ {len(templates)} templates found", templates)
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid list_templates failed: {e}")

    @staticmethod
    def create_contact_list(name: str, cred_key: str = "sendgrid") -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}", "Content-Type": "application/json"}
            r = requests.post("https://api.sendgrid.com/v3/marketing/lists", headers=headers, json={"name": name}, timeout=15)
            r.raise_for_status()
            data = r.json()
            return ToolResult(True, f"✓ Contact list created: {data['id']}", data)
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid create_contact_list failed: {e}")

    @staticmethod
    def add_contacts(
        list_id: str, contacts: list, cred_key: str = "sendgrid"
    ) -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}", "Content-Type": "application/json"}
            payload = {"list_ids": [list_id], "contacts": contacts}
            r = requests.put("https://api.sendgrid.com/v3/marketing/contacts", headers=headers, json=payload, timeout=15)
            r.raise_for_status()
            return ToolResult(True, f"✓ {len(contacts)} contacts added to list {list_id}")
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid add_contacts failed: {e}")

    @staticmethod
    def create_campaign(
        name: str,
        subject: str,
        from_email: str,
        html_content: str,
        list_ids: list,
        cred_key: str = "sendgrid",
    ) -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}", "Content-Type": "application/json"}
            payload = {
                "name": name,
                "email_config": {
                    "subject": subject,
                    "sender_id": 1,
                    "html_content": html_content,
                    "plain_content": "",
                },
                "send_to": {"list_ids": list_ids},
            }
            r = requests.post("https://api.sendgrid.com/v3/marketing/campaigns", headers=headers, json=payload, timeout=15)
            r.raise_for_status()
            data = r.json()
            return ToolResult(True, f"✓ Campaign created: {data.get('id')}", data)
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid create_campaign failed: {e}")

    @staticmethod
    def schedule_campaign(
        campaign_id: str, send_at: str, cred_key: str = "sendgrid"
    ) -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}", "Content-Type": "application/json"}
            r = requests.post(
                f"https://api.sendgrid.com/v3/marketing/campaigns/{campaign_id}/schedule",
                headers=headers,
                json={"send_at": send_at},
                timeout=15,
            )
            r.raise_for_status()
            return ToolResult(True, f"✓ Campaign {campaign_id} scheduled at {send_at}")
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid schedule_campaign failed: {e}")

    @staticmethod
    def get_stats(
        start_date: str,
        end_date: str,
        aggregated_by: str = "day",
        cred_key: str = "sendgrid",
    ) -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}"}
            params = {"start_date": start_date, "end_date": end_date, "aggregated_by": aggregated_by}
            r = requests.get("https://api.sendgrid.com/v3/stats", headers=headers, params=params, timeout=15)
            r.raise_for_status()
            return ToolResult(True, "✓ Stats fetched", r.json())
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid get_stats failed: {e}")

    @staticmethod
    def get_bounces(
        start_date: str = None, end_date: str = None, cred_key: str = "sendgrid"
    ) -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}"}
            params = {}
            if start_date:
                params["start_time"] = start_date
            if end_date:
                params["end_time"] = end_date
            r = requests.get("https://api.sendgrid.com/v3/suppression/bounces", headers=headers, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            return ToolResult(True, f"✓ {len(data)} bounces fetched", data)
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid get_bounces failed: {e}")

    @staticmethod
    def delete_bounce(email: str, cred_key: str = "sendgrid") -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}"}
            r = requests.delete(f"https://api.sendgrid.com/v3/suppression/bounces/{email}", headers=headers, timeout=15)
            r.raise_for_status()
            return ToolResult(True, f"✓ Bounce deleted for {email}")
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid delete_bounce failed: {e}")

    @staticmethod
    def get_spam_reports(cred_key: str = "sendgrid") -> ToolResult:
        try:
            import requests

            headers = {"Authorization": f"Bearer {SendGridTool._api_key(cred_key)}"}
            r = requests.get("https://api.sendgrid.com/v3/suppression/spam_reports", headers=headers, timeout=15)
            r.raise_for_status()
            data = r.json()
            return ToolResult(True, f"✓ {len(data)} spam reports fetched", data)
        except Exception as e:
            return ToolResult(False, f"✗ SendGrid get_spam_reports failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. PushNotificationTool
# ─────────────────────────────────────────────────────────────────────────────

class PushNotificationTool:
    name = "push_notification"
    description = (
        "Mobile and web push notifications: FCM (Firebase), APNs, web push (VAPID), "
        "Pushbullet, and Pushover."
    )
    use = (
        """Name of Tool:- PushNotificationTool

Purpose of Tool:- 
The PushNotificationTool is a cross-platform messaging and alert dispatching utility designed to send alerts programmatically to mobile devices, web browsers, and desktop systems. It acts as a unified hub connecting back to premier transport frameworks including Firebase Cloud Messaging (FCM), Apple Push Notification service (APNs), decentralized web push configurations using VAPID keys, alongside personal notify streams like Pushbullet and Pushover. The tool enables direct transaction payloads, segmented channel multicasting, automated state updates, localized application routing, sound preferences, and visual asset integrations to handle modern contextual device alerting strategies cleanly.

Methods:-
- send_fcm: Dispatches a personalized rich push alert directly onto an Android or generic target device using an individual token register.
- send_fcm_bulk: Groups distinct target system IDs to concurrently fire massive arrays of push notification blocks.
- send_fcm_topic: Transmits contextual messaging assets across massive client categories registered under shared subscription tracking tags.
- send_apns: Uses JSON Web Tokens and HTTP/2 connections to securely transmit custom iOS payload blocks directly onto target Apple ecosystems.
- send_web_push: Signs web payload data packets over to secure browser service worker routines using VAPID protocols.
- send_pushbullet: Fires notes or redirect URLs directly to individual device channels tracked in a user's personal Pushbullet profile.
- send_pushover: Uses simple REST requests to immediately deliver high-priority contextual messages to a user's multi-platform Pushover dashboard.

How to use Tool Methods:-

1. send_fcm:
   - Purpose: Transmits individual notifications containing explicit graphics, action intents, and embedded payload values to an active device token.
   - Arguments:
     a) device_token: str - Target identification alphanumeric chain indicating a client terminal instance.
     b) title: str - Primary focal header text appearing inside active status trays.
     c) body: str - Main contextual notification text narrative block.
     d) data: dict (default: None) - Hidden transactional key-value pairs parsed during background run loops.
     e) image: str (default: None) - Live web URL string rendering large visual image banners in the notification.
     f) click_action: str (default: None) - System intent action target used to open predefined application windows.
     g) cred_key: str (default: "firebase") - Credential lookup pointer used to reference Firebase SDK certificate configurations.
   - Returns: ToolResult storing unique backend message transaction string IDs.
   - How to call: PushNotificationTool.send_fcm(device_token="bk3RNwM-E_...", title="Order Picked Up", body="Your rider is on the way!", image="https://cdn.io/map.jpg", click_action="OPEN_TRACKING_ACTIVITY")

2. send_fcm_bulk:
   - Purpose: Accelerates delivery across large audience fractions by processing a unified array block of targeting IDs in one network step.
   - Arguments:
     a) tokens: list - Array containing discrete device token string targets.
     b) title: str - Notification header context string.
     c) body: str - Main narrative textual data array block.
     d) data: dict (default: None) - Optional backend routing key-value configurations.
     e) cred_key: str (default: "firebase") - Internal credential storage index identifier.
   - Returns: ToolResult documenting successful versus failed delivery transaction tallies.
   - How to call: PushNotificationTool.send_fcm_bulk(tokens=["tok_1", "tok_2", "tok_3"], title="Flash Sale Alert!", body="Everything is 40% off for the next 20 minutes.")

3. send_fcm_topic:
   - Purpose: Simplifies high-volume broadcast notifications by letting the server target named channel pools rather than individual device tokens.
   - Arguments:
     a) topic: str - Subscription routing tag string target.
     b) title: str - Broadcast subject line.
     c) body: str - Main message body detail block.
     d) data: dict (default: None) - Context metadata mapping dictionary.
     e) cred_key: str (default: "firebase") - System validation token lookup map index.
   - Returns: ToolResult passing global message tracking strings.
   - How to call: PushNotificationTool.send_fcm_topic(topic="weather_alerts_city", title="Storm Warning", body="Severe weather expected at 4 PM IST.")

4. send_apns:
   - Purpose: Standardizes communication to Apple environments using customized JWT authentication keys and structured sandbox/production routing targets.
   - Arguments:
     a) device_token: str - Unique hexadecimal Apple terminal registration device code.
     b) title: str - Alert heading text.
     c) body: str - Contextual message narrative block.
     d) badge: int (default: 1) - Integer counter displayed directly over application home screen icons.
     e) sound: str (default: "default") - Target file audio string to fire on arrival.
     d) data: dict (default: None) - Extended JSON parameters loaded outside canonical `aps` scopes.
     g) cred_key: str (default: "apns") - Storage profile containing private keys, team IDs, and bundle IDs.
   - Returns: ToolResult verifying whether Apple's HTTP/2 systems validated and accepted the payload structure.
   - How to call: PushNotificationTool.send_apns(device_token="740fc5512...", title="New DM", body="Alex sent you a photo", badge=3, sound="ping.caf")

5. send_web_push:
   - Purpose: Delivers secure notifications onto user desktop and web browsers via pre-negotiated subscription signatures.
   - Arguments:
     a) subscription_info: dict - Browser client endpoint vectors, keys, and security parameters block.
     b) title: str - Browser popup header banner string text.
     c) body: str - Contextual content text.
     d) icon: str (default: "") - Web path linking small layout graphics display components.
     e) url: str (default: "") - Target hyperlink destination opened when users click the web element.
     f) vapid_private_key: str (default: None) - Raw private server identifier key string used to sign request headers.
     g) cred_key: str (default: "webpush") - Vault map lookup pointing to administrative contact addresses and defaults.
   - Returns: ToolResult certifying secure service worker receipt.
   - How to call: PushNotificationTool.send_web_push(subscription_info={"endpoint": "https://fcm.googleapis.com/...", "keys": {"p256dh": "...", "auth": "..."}}, title="Web App Update", body="Click to refresh and view your new workspace dashboards.", url="https://myapp.com/dashboard")

6. send_pushbullet:
   - Purpose: Pushes rapid logs, textual notes, or shared links to specific active devices linked to a user's personal profile.
   - Arguments:
     a) title: str - Core caption metadata text.
     b) body: str - Main note message or link explanation details.
     c) type: str (default: "note") - Transmit style identifier toggle defining message structural types ("note" or "link").
     d) url: str (default: "") - Active hyperlink destination path parameter passed during link dispatches.
     e) device_iden: str (default: None) - Target alphanumeric identifier filtering the push to an individual explicit screen.
     g) cred_key: str (default: "pushbullet") - Reference index defining user account API tokens.
   - Returns: ToolResult listing raw delivery mapping logs.
   - How to call: PushNotificationTool.send_pushbullet(title="Build Pipeline Failed", body="Error logs located at destination path", type="link", url="https://ci.server/logs/404")

7. send_pushover:
   - Purpose: Injects immediate system events or custom priority warnings directly into personal notification tracking setups.
   - Arguments:
     a) token: str - Administrative application authorization token string.
     b) user: str - Specific target user token address configuration key.
     c) message: str - Core text block dispatched down to recipient screens.
     d) title: str (default: "") - Optional layout header string text description.
     b) priority: int (default: 0) - Integer ranking value ranging from low-profile backgrounds up to emergency alarms.
     f) url: str (default: "") - Embedded fallback connection link.
     g) sound: str (default: "pushover") - Audio asset descriptor tag selecting specific system tones.
     h) cred_key: str (default: "pushover") - Profile credentials fallback store pointer.
   - Returns: ToolResult ensuring explicit message transmission and processing validation.
   - How to call: PushNotificationTool.send_pushover(token="", user="", message="Server CPU usage exceeded 95% on node-02", title="CRITICAL ALERT", priority=1, sound="alien")
   """)

    @staticmethod
    def send_fcm(
        device_token: str,
        title: str,
        body: str,
        data: dict = None,
        image: str = None,
        click_action: str = None,
        cred_key: str = "firebase",
    ) -> ToolResult:
        try:
            import firebase_admin
            from firebase_admin import credentials as fb_creds, messaging

            if not firebase_admin._apps:
                cred_data = CredStore.load(cred_key)
                if not cred_data:
                    return ToolResult(False, "✗ No Firebase credentials found.")
                cred = fb_creds.Certificate(cred_data)
                firebase_admin.initialize_app(cred)

            notification = messaging.Notification(title=title, body=body, image=image)
            android_config = messaging.AndroidConfig(
                notification=messaging.AndroidNotification(click_action=click_action)
            ) if click_action else None

            message = messaging.Message(
                notification=notification,
                data=data or {},
                token=device_token,
                android=android_config,
            )
            response = messaging.send(message)
            return ToolResult(True, f"✓ FCM push sent: {response}", {"message_id": response})
        except Exception as e:
            return ToolResult(False, f"✗ FCM send_fcm failed: {e}")

    @staticmethod
    def send_fcm_bulk(
        tokens: list,
        title: str,
        body: str,
        data: dict = None,
        cred_key: str = "firebase",
    ) -> ToolResult:
        try:
            import firebase_admin
            from firebase_admin import credentials as fb_creds, messaging

            if not firebase_admin._apps:
                cred_data = CredStore.load(cred_key)
                cred = fb_creds.Certificate(cred_data)
                firebase_admin.initialize_app(cred)

            messages = [
                messaging.Message(
                    notification=messaging.Notification(title=title, body=body),
                    data=data or {},
                    token=token,
                )
                for token in tokens
            ]
            batch_response = messaging.send_all(messages)
            success_count = batch_response.success_count
            failure_count = batch_response.failure_count
            return ToolResult(
                True,
                f"✓ FCM bulk: {success_count} sent, {failure_count} failed",
                {"success": success_count, "failure": failure_count},
            )
        except Exception as e:
            return ToolResult(False, f"✗ FCM send_fcm_bulk failed: {e}")

    @staticmethod
    def send_fcm_topic(
        topic: str,
        title: str,
        body: str,
        data: dict = None,
        cred_key: str = "firebase",
    ) -> ToolResult:
        try:
            import firebase_admin
            from firebase_admin import credentials as fb_creds, messaging

            if not firebase_admin._apps:
                cred_data = CredStore.load(cred_key)
                cred = fb_creds.Certificate(cred_data)
                firebase_admin.initialize_app(cred)

            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                data=data or {},
                topic=topic,
            )
            response = messaging.send(message)
            return ToolResult(True, f"✓ FCM topic '{topic}' push sent", {"message_id": response})
        except Exception as e:
            return ToolResult(False, f"✗ FCM send_fcm_topic failed: {e}")

    @staticmethod
    def send_apns(
        device_token: str,
        title: str,
        body: str,
        badge: int = 1,
        sound: str = "default",
        data: dict = None,
        cred_key: str = "apns",
    ) -> ToolResult:
        try:
            import requests, json, time, jwt

            creds = CredStore.load(cred_key)
            key_id      = creds.get("key_id", "")
            team_id     = creds.get("team_id", "")
            bundle_id   = creds.get("bundle_id", "")
            private_key = creds.get("private_key", "")
            sandbox     = creds.get("sandbox", False)

            token_data = {
                "iss": team_id,
                "iat": int(time.time()),
            }
            auth_token = jwt.encode(token_data, private_key, algorithm="ES256",
                                    headers={"kid": key_id, "alg": "ES256"})

            host = "api.sandbox.push.apple.com" if sandbox else "api.push.apple.com"
            url  = f"https://{host}/3/device/{device_token}"
            headers = {
                "authorization": f"bearer {auth_token}",
                "apns-push-type": "alert",
                "apns-topic": bundle_id,
            }
            payload = {
                "aps": {
                    "alert": {"title": title, "body": body},
                    "badge": badge,
                    "sound": sound,
                },
                **(data or {}),
            }
            r = requests.post(url, headers=headers, json=payload, timeout=15)
            if r.status_code == 200:
                return ToolResult(True, f"✓ APNs push sent to {device_token[:12]}…")
            return ToolResult(False, f"✗ APNs responded {r.status_code}: {r.text[:200]}")
        except Exception as e:
            return ToolResult(False, f"✗ APNs send_apns failed: {e}")

    @staticmethod
    def send_web_push(
        subscription_info: dict,
        title: str,
        body: str,
        icon: str = "",
        url: str = "",
        vapid_private_key: str = None,
        cred_key: str = "webpush",
    ) -> ToolResult:
        try:
            from pywebpush import webpush, WebPushException
            import json

            creds = CredStore.load(cred_key)
            priv_key = vapid_private_key or creds.get("vapid_private_key", "")
            claims_email = creds.get("vapid_claims_email", "mailto:admin@example.com")

            payload = json.dumps({"title": title, "body": body, "icon": icon, "url": url})
            webpush(
                subscription_info=subscription_info,
                data=payload,
                vapid_private_key=priv_key,
                vapid_claims={"sub": claims_email},
            )
            return ToolResult(True, "✓ Web push notification sent")
        except Exception as e:
            return ToolResult(False, f"✗ Web push send_web_push failed: {e}")

    @staticmethod
    def send_pushbullet(
        title: str,
        body: str,
        type: str = "note",
        url: str = "",
        device_iden: str = None,
        cred_key: str = "pushbullet",
    ) -> ToolResult:
        try:
            from pushbullet import Pushbullet

            api_key = CredStore.load(cred_key).get("api_key", "")
            if not api_key:
                return ToolResult(False, "✗ No Pushbullet api_key in credentials.")
            pb = Pushbullet(api_key)
            device = None
            if device_iden:
                device = next((d for d in pb.devices if d.device_iden == device_iden), None)

            if type == "link" and url:
                push = pb.push_link(title, url, body=body, device=device)
            else:
                push = pb.push_note(title, body, device=device)

            return ToolResult(True, f"✓ Pushbullet {type} sent: {push.get('iden', '')}", push)
        except Exception as e:
            return ToolResult(False, f"✗ Pushbullet send_pushbullet failed: {e}")

    @staticmethod
    def send_pushover(
        token: str,
        user: str,
        message: str,
        title: str = "",
        priority: int = 0,
        url: str = "",
        sound: str = "pushover",
        cred_key: str = "pushover",
    ) -> ToolResult:
        try:
            import requests

            creds = CredStore.load(cred_key)
            app_token = token or creds.get("token", "")
            user_key  = user  or creds.get("user", "")

            payload = {
                "token":    app_token,
                "user":     user_key,
                "message":  message,
                "title":    title,
                "priority": priority,
                "url":      url,
                "sound":    sound,
            }
            r = requests.post("https://api.pushover.net/1/messages.json", data=payload, timeout=15)
            data = r.json()
            if data.get("status") == 1:
                return ToolResult(True, "✓ Pushover notification sent", data)
            return ToolResult(False, f"✗ Pushover error: {data}")
        except Exception as e:
            return ToolResult(False, f"✗ Pushover send_pushover failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. RSSFeedTool
# ─────────────────────────────────────────────────────────────────────────────

class RSSFeedTool:
    name = "rss_feed"
    description = (
        "RSS/Atom feed operations: parse, monitor, compare, create, aggregate, search, export, "
        "and subscribe-and-notify."
    )
    use = (
        """
Name of Tool:- RSSFeedTool,

Purpose of Tool:- 
The RSSFeedTool provides a complete set of operations for working with RSS and Atom feeds. 
It supports parsing feeds, monitoring for new items, comparing feeds for changes, generating custom RSS feeds, aggregating multiple feeds, searching within feeds, exporting data, and setting up real-time subscriptions with notifications. 
Built on feedparser with additional utilities for monitoring, deduplication, and export, this tool is ideal for content aggregation, news monitoring, automated alerts, data pipelines, and agentic information gathering from web sources.

Methods:-
- parse_feed: Parses an RSS/Atom feed and extracts structured items.
- monitor_feed: Continuously monitors a feed for new items in a background thread.
- compare_feeds: Identifies new items by comparing current feed against previously seen items.
- get_new_items: Filters feed items published after a specific date.
- create_rss_feed: Generates a new RSS 2.0 feed XML file from a list of items.
- aggregate_feeds: Combines items from multiple feeds with optional deduplication.
- search_in_feed: Searches for keywords across feed items.
- export_feed_items: Exports parsed feed items to JSON or CSV.
- subscribe_and_notify: Subscribes to a feed and sends notifications on new items.

How to use Tool Methods:-

1. parse_feed:
   - Purpose: Parses a remote RSS/Atom feed and returns structured item data.
   - Arguments:
     a) url: str - Full URL of the RSS/Atom feed.
     b) limit: int (default: 20) - Maximum number of items to return.
     c) full_content: bool (default: False) - Whether to include full article content when available.
   - Returns: List of items with title, link, published date, summary, and optional content.
   - How to call: 
     RSSFeedTool.parse_feed(url="https://example.com/rss", limit=50, full_content=True)

2. monitor_feed:
   - Purpose: Starts a background thread that continuously polls a feed and calls a callback on new items.
   - Arguments:
     a) url: str - Feed URL.
     b) interval: int (default: 300) - Polling interval in seconds.
     c) callback: callable (optional) - Function to call with new entry.
     d) last_check: str (optional) - Not actively used in current implementation.
   - Returns: Confirmation that monitoring has started.
   - How to call: RSSFeedTool.monitor_feed(url="https://news.example.com/rss", interval=60, callback=my_callback)

3. compare_feeds:
   - Purpose: Detects new items by comparing current feed against a list of previously seen items.
   - Arguments:
     a) url: str - Feed URL.
     b) last_items: list - Previously seen items (dicts or objects with "link" key).
   - Returns: List of new entries.
   - How to call: RSSFeedTool.compare_feeds(url=feed_url, last_items=previous_items)

4. get_new_items:
   - Purpose: Returns only items published after a given ISO date.
   - Arguments:
     a) url: str - Feed URL.
     b) since_date: str - ISO datetime string (e.g., "2026-06-01T00:00:00").
   - Returns: List of new items.
   - How to call: RSSFeedTool.get_new_items(url=feed_url, since_date="2026-06-10")

5. create_rss_feed:
   - Purpose: Generates a valid RSS 2.0 XML file from a list of items.
   - Arguments:
     a) title: str - Channel title.
     b) link: str - Channel link.
     c) description: str - Channel description.
     d) items: list - List of item dictionaries (title, link, description, pubDate).
     e) output: str (default: "feed.xml") - Output file path.
   - How to call: RSSFeedTool.create_rss_feed(title="My Feed", link="https://...", description="...", items=my_items)

6. aggregate_feeds:
   - Purpose: Combines entries from multiple RSS feeds into a single unified list.
   - Arguments:
     a) urls: list - List of feed URLs.
     b) limit_per_feed: int (default: 10).
     c) deduplicate: bool (default: True) - Remove duplicate links.
   - Returns: Aggregated list of items with source information.
   - How to call: RSSFeedTool.aggregate_feeds(urls=["https://feed1", "https://feed2"], limit_per_feed=15)

7. search_in_feed:
   - Purpose: Searches for a keyword or phrase across titles and summaries in a feed.
   - Arguments:
     a) url: str - Feed URL.
     b) query: str - Search term (case-insensitive).
   - Returns: Matching items.
   - How to call: RSSFeedTool.search_in_feed(url=feed_url, query="AI")

8. export_feed_items:
   - Purpose: Parses a feed and exports items to JSON or CSV format.
   - Arguments:
     a) url: str - Feed URL.
     b) format: str (default: "json") - "json" or "csv".
     c) output: str (default: "feed_export.json") - Output file path.
   - How to call: RSSFeedTool.export_feed_items(url=feed_url, format="csv", output="news.csv")

9. subscribe_and_notify:
   - Purpose: Subscribes to a feed and automatically prints or sends notifications (Slack supported) when new items appear.
   - Arguments:
     a) url: str - Feed URL.
     b) notification_channel: str (default: "print") - "print" or "slack".
   - Returns: Confirmation that subscription is active.
   - How to call: RSSFeedTool.subscribe_and_notify(url=feed_url, notification_channel="slack")
""")

    @staticmethod
    def parse_feed(
        url: str, limit: int = 20, full_content: bool = False
    ) -> ToolResult:
        try:
            import feedparser

            feed = feedparser.parse(url)
            if feed.bozo and not feed.entries:
                return ToolResult(False, f"✗ Feed parse error: {feed.bozo_exception}")

            items = []
            for entry in feed.entries[:limit]:
                item = {
                    "title":   entry.get("title", ""),
                    "link":    entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                }
                if full_content:
                    content_list = entry.get("content", [])
                    item["content"] = content_list[0].get("value", "") if content_list else entry.get("summary", "")
                items.append(item)

            return ToolResult(True, f"✓ Parsed {len(items)} items from {feed.feed.get('title', url)}", items)
        except Exception as e:
            return ToolResult(False, f"✗ RSSFeed parse_feed failed: {e}")

    @staticmethod
    def monitor_feed(
        url: str,
        interval: int = 300,
        callback=None,
        last_check: str = None,
    ) -> ToolResult:
        try:
            import feedparser, threading, time
            from datetime import datetime

            def _watch():
                seen_links = set()
                while True:
                    try:
                        feed = feedparser.parse(url)
                        for entry in feed.entries:
                            link = entry.get("link", "")
                            if link and link not in seen_links:
                                seen_links.add(link)
                                if callback:
                                    callback(entry)
                    except Exception:
                        pass
                    time.sleep(interval)

            t = threading.Thread(target=_watch, daemon=True)
            t.start()
            return ToolResult(True, f"✓ Monitoring feed {url} every {interval}s")
        except Exception as e:
            return ToolResult(False, f"✗ RSSFeed monitor_feed failed: {e}")

    @staticmethod
    def compare_feeds(url: str, last_items: list) -> ToolResult:
        try:
            import feedparser

            feed  = feedparser.parse(url)
            current_links = {e.get("link", "") for e in feed.entries}
            old_links     = {item.get("link", "") if isinstance(item, dict) else item for item in last_items}
            new_links     = current_links - old_links

            new_entries = [
                {
                    "title":     e.get("title", ""),
                    "link":      e.get("link", ""),
                    "published": e.get("published", ""),
                }
                for e in feed.entries
                if e.get("link", "") in new_links
            ]
            return ToolResult(True, f"✓ {len(new_entries)} new item(s) since last check", new_entries)
        except Exception as e:
            return ToolResult(False, f"✗ RSSFeed compare_feeds failed: {e}")

    @staticmethod
    def get_new_items(url: str, since_date: str) -> ToolResult:
        try:
            import feedparser
            from datetime import datetime
            from email.utils import parsedate_to_datetime

            feed  = feedparser.parse(url)
            cutoff = datetime.fromisoformat(since_date)
            new_items = []
            for entry in feed.entries:
                try:
                    pub = parsedate_to_datetime(entry.get("published", ""))
                    if pub.replace(tzinfo=None) > cutoff:
                        new_items.append({
                            "title":     entry.get("title", ""),
                            "link":      entry.get("link", ""),
                            "published": entry.get("published", ""),
                        })
                except Exception:
                    pass
            return ToolResult(True, f"✓ {len(new_items)} new item(s) since {since_date}", new_items)
        except Exception as e:
            return ToolResult(False, f"✗ RSSFeed get_new_items failed: {e}")

    @staticmethod
    def create_rss_feed(
        title: str,
        link: str,
        description: str,
        items: list,
        output: str = "feed.xml",
    ) -> ToolResult:
        try:
            from pathlib import Path
            from datetime import datetime

            lines = [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<rss version="2.0">',
                "  <channel>",
                f"    <title>{title}</title>",
                f"    <link>{link}</link>",
                f"    <description>{description}</description>",
                f"    <lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>",
            ]
            for item in items:
                lines += [
                    "    <item>",
                    f"      <title>{item.get('title','')}</title>",
                    f"      <link>{item.get('link','')}</link>",
                    f"      <description>{item.get('description','')}</description>",
                    f"      <pubDate>{item.get('pubDate','')}</pubDate>",
                    "    </item>",
                ]
            lines += ["  </channel>", "</rss>"]
            Path(output).write_text("\n".join(lines), encoding="utf-8")
            return ToolResult(True, f"✓ RSS feed written to {output} ({len(items)} items)")
        except Exception as e:
            return ToolResult(False, f"✗ RSSFeed create_rss_feed failed: {e}")

    @staticmethod
    def aggregate_feeds(
        urls: list, limit_per_feed: int = 10, deduplicate: bool = True
    ) -> ToolResult:
        try:
            import feedparser

            all_items = []
            seen_links: set = set()
            for url in urls:
                try:
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:limit_per_feed]:
                        link = entry.get("link", "")
                        if deduplicate and link in seen_links:
                            continue
                        seen_links.add(link)
                        all_items.append({
                            "source":    feed.feed.get("title", url),
                            "title":     entry.get("title", ""),
                            "link":      link,
                            "published": entry.get("published", ""),
                            "summary":   entry.get("summary", "")[:300],
                        })
                except Exception:
                    pass
            return ToolResult(True, f"✓ Aggregated {len(all_items)} items from {len(urls)} feeds", all_items)
        except Exception as e:
            return ToolResult(False, f"✗ RSSFeed aggregate_feeds failed: {e}")

    @staticmethod
    def search_in_feed(url: str, query: str) -> ToolResult:
        try:
            import feedparser

            feed  = feedparser.parse(url)
            q = query.lower()
            matches = []
            for entry in feed.entries:
                text = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
                if q in text:
                    matches.append({
                        "title":     entry.get("title", ""),
                        "link":      entry.get("link", ""),
                        "published": entry.get("published", ""),
                    })
            return ToolResult(True, f"✓ {len(matches)} result(s) for '{query}'", matches)
        except Exception as e:
            return ToolResult(False, f"✗ RSSFeed search_in_feed failed: {e}")

    @staticmethod
    def export_feed_items(
        url: str, format: str = "json", output: str = "feed_export.json"
    ) -> ToolResult:
        try:
            import feedparser, json, csv
            from pathlib import Path

            feed  = feedparser.parse(url)
            items = [
                {
                    "title":     e.get("title", ""),
                    "link":      e.get("link", ""),
                    "published": e.get("published", ""),
                    "summary":   e.get("summary", ""),
                }
                for e in feed.entries
            ]
            if format.lower() == "csv":
                if not output.endswith(".csv"):
                    output = output.rsplit(".", 1)[0] + ".csv"
                with open(output, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=["title", "link", "published", "summary"])
                    writer.writeheader()
                    writer.writerows(items)
            else:
                Path(output).write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")

            return ToolResult(True, f"✓ {len(items)} items exported to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ RSSFeed export_feed_items failed: {e}")

    @staticmethod
    def subscribe_and_notify(
        url: str, notification_channel: str = "print"
    ) -> ToolResult:
        try:
            import feedparser, threading, time

            seen: set = set()

            def _notify(entry):
                title = entry.get("title", "")
                link  = entry.get("link", "")
                msg   = f"[RSS] {title} — {link}"
                if notification_channel == "print":
                    print(msg)
                elif notification_channel == "slack":
                    from agent_core import CredStore as CS
                    from slack_sdk import WebClient
                    token = CS.load("slack").get("bot_token", "")
                    if token:
                        WebClient(token=token).chat_postMessage(channel="#general", text=msg)

            def _watch():
                while True:
                    try:
                        feed = feedparser.parse(url)
                        for entry in feed.entries:
                            lnk = entry.get("link", "")
                            if lnk and lnk not in seen:
                                seen.add(lnk)
                                _notify(entry)
                    except Exception:
                        pass
                    time.sleep(300)

            threading.Thread(target=_watch, daemon=True).start()
            return ToolResult(True, f"✓ Subscribed to {url}, notifying via {notification_channel}")
        except Exception as e:
            return ToolResult(False, f"✗ RSSFeed subscribe_and_notify failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────#############################################################################################
# 7. WebhookTool
# ─────────────────────────────────────────────────────────────────────────────#############################################################################################

class WebhookTool:########################################################################################################################################################
    name = "webhook"
    description = (
        "Webhook server, signature verification, registration, testing, replay, "
        "proxy, and payload inspection."
    )

    _registered: dict = {}
    _received:   list = []

    @staticmethod
    def start_webhook_server(
        port: int = 5055,
        secret: str = "",
        callback=None,
    ) -> ToolResult:
        try:
            import threading, hashlib, hmac
            from flask import Flask, request, jsonify

            app = Flask(__name__)

            @app.route("/webhook", methods=["POST"])
            def _hook():
                payload   = request.get_data()
                signature = request.headers.get("X-Hub-Signature-256", "")
                if secret:
                    expected = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
                    if not hmac.compare_digest(expected, signature):
                        return jsonify({"error": "Invalid signature"}), 401
                data = request.get_json(silent=True) or payload.decode()
                WebhookTool._received.append(data)
                if callback:
                    threading.Thread(target=callback, args=(data,), daemon=True).start()
                return jsonify({"status": "received"}), 200

            t = threading.Thread(target=lambda: app.run(port=port, use_reloader=False), daemon=True)
            t.start()
            return ToolResult(True, f"✓ Webhook server started on port {port}")
        except Exception as e:
            return ToolResult(False, f"✗ Webhook start_webhook_server failed: {e}")

    @staticmethod
    def verify_signature(payload: bytes, signature: str, secret: str) -> ToolResult:
        try:
            import hmac, hashlib

            expected = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
            valid    = hmac.compare_digest(expected, signature)
            return ToolResult(valid, "✓ Signature valid" if valid else "✗ Signature mismatch")
        except Exception as e:
            return ToolResult(False, f"✗ Webhook verify_signature failed: {e}")

    @staticmethod
    def register_webhook(
        service: str, url: str, events: list, secret: str = ""
    ) -> ToolResult:
        try:
            import uuid

            webhook_id = str(uuid.uuid4())
            WebhookTool._registered[webhook_id] = {
                "service": service,
                "url":     url,
                "events":  events,
                "secret":  secret,
            }
            return ToolResult(True, f"✓ Webhook registered (ID: {webhook_id})", {"id": webhook_id})
        except Exception as e:
            return ToolResult(False, f"✗ Webhook register_webhook failed: {e}")

    @staticmethod
    def list_registered_webhooks(service: str = "") -> ToolResult:
        try:
            hooks = [
                {"id": k, **v}
                for k, v in WebhookTool._registered.items()
                if not service or v.get("service") == service
            ]
            return ToolResult(True, f"✓ {len(hooks)} registered webhook(s)", hooks)
        except Exception as e:
            return ToolResult(False, f"✗ Webhook list_registered_webhooks failed: {e}")

    @staticmethod
    def test_webhook(
        url: str, payload: dict, headers: dict = None
    ) -> ToolResult:
        try:
            import requests

            r = requests.post(url, json=payload, headers=headers or {}, timeout=15)
            return ToolResult(
                r.status_code < 300,
                f"✓ Webhook test response: {r.status_code}",
                {"status": r.status_code, "body": r.text[:500]},
            )
        except Exception as e:
            return ToolResult(False, f"✗ Webhook test_webhook failed: {e}")

    @staticmethod
    def replay_webhook(webhook_id: str) -> ToolResult:
        try:
            import requests

            hook = WebhookTool._registered.get(webhook_id)
            if not hook:
                return ToolResult(False, f"✗ Webhook ID {webhook_id} not found.")
            if not WebhookTool._received:
                return ToolResult(False, "✗ No received payloads to replay.")
            payload = WebhookTool._received[-1]
            r = requests.post(hook["url"], json=payload, timeout=15)
            return ToolResult(r.status_code < 300, f"✓ Replayed webhook to {hook['url']} → {r.status_code}")
        except Exception as e:
            return ToolResult(False, f"✗ Webhook replay_webhook failed: {e}")

    @staticmethod
    def create_webhook_proxy(forward_to: str, port: int = 5056) -> ToolResult:
        try:
            import threading, requests
            from flask import Flask, request, jsonify

            app = Flask(__name__)

            @app.route("/", methods=["POST", "GET"])
            def _proxy():
                data    = request.get_json(silent=True) or {}
                headers = dict(request.headers)
                r = requests.post(forward_to, json=data, headers=headers, timeout=15)
                return jsonify({"forwarded_status": r.status_code}), 200

            threading.Thread(target=lambda: app.run(port=port, use_reloader=False), daemon=True).start()
            return ToolResult(True, f"✓ Webhook proxy started on port {port}, forwarding to {forward_to}")
        except Exception as e:
            return ToolResult(False, f"✗ Webhook create_webhook_proxy failed: {e}")

    @staticmethod
    def inspect_webhook_payload(payload: dict) -> ToolResult:
        try:
            import json

            keys   = list(payload.keys()) if isinstance(payload, dict) else []
            pretty = json.dumps(payload, indent=2, default=str)
            return ToolResult(
                True,
                f"✓ Payload has {len(keys)} top-level keys: {keys}",
                {"keys": keys, "pretty": pretty},
            )
        except Exception as e:
            return ToolResult(False, f"✗ Webhook inspect_webhook_payload failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────#############################################################################################
# 8. CalendarTool
# ─────────────────────────────────────────────────────────────────────────────#############################################################################################

class CalendarTool:#########################################################################################################################################################
    name = "calendar"
    description = (
        "Google Calendar: list/create/update/delete events, quick-add, list/create calendars, "
        "find free slots, send invites, and sync/import iCal files."
    )

    @staticmethod
    def _service(cred_key: str = "google_calendar"):
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        creds_data = CredStore.load(cred_key)
        if not creds_data:
            raise ValueError("No Google Calendar credentials found.")
        creds = Credentials(
            token=creds_data.get("token"),
            refresh_token=creds_data.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=creds_data.get("client_id"),
            client_secret=creds_data.get("client_secret"),
        )
        return build("calendar", "v3", credentials=creds)

    @staticmethod
    def list_events(
        calendar_id: str = "primary",
        time_min: str = None,
        time_max: str = None,
        max_results: int = 20,
        cred_key: str = "google_calendar",
    ) -> ToolResult:
        try:
            from datetime import datetime, timezone

            svc = CalendarTool._service(cred_key)
            time_min = time_min or datetime.now(timezone.utc).isoformat()
            events_result = svc.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            events = events_result.get("items", [])
            return ToolResult(True, f"✓ {len(events)} events fetched", events)
        except Exception as e:
            return ToolResult(False, f"✗ Calendar list_events failed: {e}")

    @staticmethod
    def create_event(
        calendar_id: str = "primary",
        summary: str = "",
        start: str = "",
        end: str = "",
        description: str = "",
        location: str = "",
        attendees: list = None,
        reminders: list = None,
        cred_key: str = "google_calendar",
    ) -> ToolResult:
        try:
            svc = CalendarTool._service(cred_key)
            body = {
                "summary":     summary,
                "description": description,
                "location":    location,
                "start":       {"dateTime": start, "timeZone": "UTC"},
                "end":         {"dateTime": end,   "timeZone": "UTC"},
                "attendees":   [{"email": a} for a in (attendees or [])],
                "reminders":   {
                    "useDefault": False,
                    "overrides":  reminders or [{"method": "email", "minutes": 30}],
                },
            }
            event = svc.events().insert(calendarId=calendar_id, body=body, sendUpdates="all").execute()
            return ToolResult(True, f"✓ Event created: {event.get('htmlLink')}", event)
        except Exception as e:
            return ToolResult(False, f"✗ Calendar create_event failed: {e}")

    @staticmethod
    def update_event(
        calendar_id: str,
        event_id: str,
        data: dict,
        cred_key: str = "google_calendar",
    ) -> ToolResult:
        try:
            svc   = CalendarTool._service(cred_key)
            event = svc.events().get(calendarId=calendar_id, eventId=event_id).execute()
            event.update(data)
            updated = svc.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
            return ToolResult(True, f"✓ Event {event_id} updated", updated)
        except Exception as e:
            return ToolResult(False, f"✗ Calendar update_event failed: {e}")

    @staticmethod
    def delete_event(
        calendar_id: str, event_id: str, cred_key: str = "google_calendar"
    ) -> ToolResult:
        try:
            svc = CalendarTool._service(cred_key)
            svc.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            return ToolResult(True, f"✓ Event {event_id} deleted")
        except Exception as e:
            return ToolResult(False, f"✗ Calendar delete_event failed: {e}")

    @staticmethod
    def quick_add_event(
        calendar_id: str, text: str, cred_key: str = "google_calendar"
    ) -> ToolResult:
        try:
            svc   = CalendarTool._service(cred_key)
            event = svc.events().quickAdd(calendarId=calendar_id, text=text).execute()
            return ToolResult(True, f"✓ Quick event added: {event.get('htmlLink')}", event)
        except Exception as e:
            return ToolResult(False, f"✗ Calendar quick_add_event failed: {e}")

    @staticmethod
    def list_calendars(cred_key: str = "google_calendar") -> ToolResult:
        try:
            svc    = CalendarTool._service(cred_key)
            result = svc.calendarList().list().execute()
            items  = result.get("items", [])
            return ToolResult(True, f"✓ {len(items)} calendar(s) found", items)
        except Exception as e:
            return ToolResult(False, f"✗ Calendar list_calendars failed: {e}")

    @staticmethod
    def create_calendar(
        summary: str, timezone: str = "UTC", cred_key: str = "google_calendar"
    ) -> ToolResult:
        try:
            svc = CalendarTool._service(cred_key)
            cal = svc.calendars().insert(body={"summary": summary, "timeZone": timezone}).execute()
            return ToolResult(True, f"✓ Calendar created: {cal['id']}", cal)
        except Exception as e:
            return ToolResult(False, f"✗ Calendar create_calendar failed: {e}")

    @staticmethod
    def find_free_slots(
        calendar_id: str,
        duration_minutes: int = 30,
        date: str = None,
        working_hours: tuple = (9, 17),
        cred_key: str = "google_calendar",
    ) -> ToolResult:
        try:
            from datetime import datetime, timedelta, timezone

            target_date = datetime.fromisoformat(date) if date else datetime.now()
            day_start   = target_date.replace(hour=working_hours[0], minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
            day_end     = target_date.replace(hour=working_hours[1], minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

            svc = CalendarTool._service(cred_key)
            events_result = svc.events().list(
                calendarId=calendar_id,
                timeMin=day_start.isoformat(),
                timeMax=day_end.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            events = events_result.get("items", [])

            busy_slots = []
            for e in events:
                s = e["start"].get("dateTime", e["start"].get("date", ""))
                en = e["end"].get("dateTime", e["end"].get("date", ""))
                if s and en:
                    busy_slots.append((datetime.fromisoformat(s.replace("Z", "+00:00")),
                                       datetime.fromisoformat(en.replace("Z", "+00:00"))))

            free_slots = []
            cursor = day_start
            for busy_start, busy_end in sorted(busy_slots):
                if cursor + timedelta(minutes=duration_minutes) <= busy_start:
                    free_slots.append({"start": cursor.isoformat(), "end": busy_start.isoformat()})
                cursor = max(cursor, busy_end)
            if cursor + timedelta(minutes=duration_minutes) <= day_end:
                free_slots.append({"start": cursor.isoformat(), "end": day_end.isoformat()})

            return ToolResult(True, f"✓ {len(free_slots)} free slot(s) found", free_slots)
        except Exception as e:
            return ToolResult(False, f"✗ Calendar find_free_slots failed: {e}")

    @staticmethod
    def send_invite(
        summary: str,
        start: str,
        end: str,
        attendee_emails: list,
        location: str = "",
        description: str = "",
        cred_key: str = "google_calendar",
    ) -> ToolResult:
        return CalendarTool.create_event(
            calendar_id="primary",
            summary=summary,
            start=start,
            end=end,
            description=description,
            location=location,
            attendees=attendee_emails,
            cred_key=cred_key,
        )

    @staticmethod
    def sync_to_local(
        calendar_id: str, output_ical: str = "calendar.ics", cred_key: str = "google_calendar"
    ) -> ToolResult:
        try:
            from icalendar import Calendar, Event as ICalEvent
            from datetime import datetime, timezone
            from pathlib import Path

            svc = CalendarTool._service(cred_key)
            events_result = svc.events().list(
                calendarId=calendar_id,
                maxResults=200,
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            events = events_result.get("items", [])

            cal = Calendar()
            cal.add("prodid", "-//NPM Agent//NPMAI//EN")
            cal.add("version", "2.0")

            for e in events:
                ev = ICalEvent()
                ev.add("summary",     e.get("summary", ""))
                ev.add("description", e.get("description", ""))
                ev.add("location",    e.get("location", ""))
                s = e["start"].get("dateTime", e["start"].get("date", ""))
                en = e["end"].get("dateTime", e["end"].get("date", ""))
                if s:
                    ev.add("dtstart", datetime.fromisoformat(s.replace("Z", "+00:00")))
                if en:
                    ev.add("dtend",   datetime.fromisoformat(en.replace("Z", "+00:00")))
                cal.add_component(ev)

            Path(output_ical).write_bytes(cal.to_ical())
            return ToolResult(True, f"✓ {len(events)} events synced to {output_ical}")
        except Exception as e:
            return ToolResult(False, f"✗ Calendar sync_to_local failed: {e}")

    @staticmethod
    def import_ical(
        calendar_id: str, ical_path: str, cred_key: str = "google_calendar"
    ) -> ToolResult:
        try:
            from icalendar import Calendar
            from pathlib import Path

            svc   = CalendarTool._service(cred_key)
            data  = Calendar.from_ical(Path(ical_path).read_bytes())
            count = 0
            for component in data.walk():
                if component.name == "VEVENT":
                    start = component.get("dtstart")
                    end   = component.get("dtend")
                    body  = {
                        "summary":     str(component.get("summary", "")),
                        "description": str(component.get("description", "")),
                        "location":    str(component.get("location", "")),
                        "start":       {"dateTime": start.dt.isoformat() if start else ""},
                        "end":         {"dateTime": end.dt.isoformat()   if end   else ""},
                    }
                    svc.events().insert(calendarId=calendar_id, body=body).execute()
                    count += 1
            return ToolResult(True, f"✓ {count} events imported from {ical_path}")
        except Exception as e:
            return ToolResult(False, f"✗ Calendar import_ical failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────#############################################################################################
# 9. ChatOpsAutomationTool
# ─────────────────────────────────────────────────────────────────────────────#############################################################################################

class ChatOpsAutomationTool:################################################################################################################################################
    name = "chatops_automation"
    description = (
        "Cross-platform ChatOps: alerts, incidents, deployments, standups, approval workflows, "
        "announcements, and scheduled messages across Slack, Discord, Teams, and Telegram."
    )

    _workflows: dict = {}

    @staticmethod
    def _send_to_channel(channel_type: str, channel_id: str, message: str, cred_key: str = None) -> bool:
        try:
            if channel_type == "slack":
                from slack_sdk import WebClient
                token = CredStore.load(cred_key or "slack").get("bot_token", "")
                WebClient(token=token).chat_postMessage(channel=channel_id, text=message)
            elif channel_type == "discord":
                import requests
                webhook = CredStore.load(cred_key or "discord").get("webhook_url", channel_id)
                requests.post(webhook, json={"content": message}, timeout=10)
            elif channel_type == "teams":
                import requests
                requests.post(channel_id, json={"text": message}, timeout=10)
            elif channel_type == "telegram":
                import requests
                token = CredStore.load(cred_key or "telegram").get("bot_token", "")
                requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                              json={"chat_id": channel_id, "text": message}, timeout=10)
            return True
        except Exception:
            return False

    @staticmethod
    def route_alert(
        message: str,
        severity: str = "info",
        channels_config: list = None,
    ) -> ToolResult:
        try:
            if channels_config is None:
                channels_config = []
            severity_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(severity.lower(), "⚪")
            formatted = f"{severity_emoji} [{severity.upper()}] {message}"
            sent = 0
            for ch in channels_config:
                if ChatOpsAutomationTool._send_to_channel(ch.get("type", ""), ch.get("id", ""), formatted):
                    sent += 1
            return ToolResult(True, f"✓ Alert sent to {sent}/{len(channels_config)} channels")
        except Exception as e:
            return ToolResult(False, f"✗ ChatOps route_alert failed: {e}")

    @staticmethod
    def create_incident(
        title: str,
        description: str,
        severity: str = "high",
        channels: list = None,
    ) -> ToolResult:
        try:
            import uuid
            from datetime import datetime

            incident_id  = str(uuid.uuid4())[:8].upper()
            timestamp    = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            message      = (
                f"🚨 INCIDENT [{incident_id}]\n"
                f"Title: {title}\n"
                f"Severity: {severity.upper()}\n"
                f"Time: {timestamp}\n"
                f"Details: {description}"
            )
            ChatOpsAutomationTool._workflows[incident_id] = {
                "type": "incident", "title": title, "severity": severity, "time": timestamp
            }
            sent = 0
            for ch in (channels or []):
                if ChatOpsAutomationTool._send_to_channel(ch.get("type", ""), ch.get("id", ""), message):
                    sent += 1
            return ToolResult(True, f"✓ Incident {incident_id} created, notified {sent} channels", {"incident_id": incident_id})
        except Exception as e:
            return ToolResult(False, f"✗ ChatOps create_incident failed: {e}")

    @staticmethod
    def post_deployment_notification(
        service: str,
        version: str,
        environment: str,
        status: str,
        changelog: str = "",
        channels: list = None,
    ) -> ToolResult:
        try:
            emoji = "✅" if status.lower() == "success" else "❌"
            message = (
                f"{emoji} Deployment Update\n"
                f"Service: {service}  v{version}\n"
                f"Environment: {environment}\n"
                f"Status: {status.upper()}\n"
            )
            if changelog:
                message += f"Changes:\n{changelog}"
            sent = 0
            for ch in (channels or []):
                if ChatOpsAutomationTool._send_to_channel(ch.get("type", ""), ch.get("id", ""), message):
                    sent += 1
            return ToolResult(True, f"✓ Deployment notification sent to {sent} channels")
        except Exception as e:
            return ToolResult(False, f"✗ ChatOps post_deployment_notification failed: {e}")

    @staticmethod
    def send_daily_standup_reminder(
        team_channels: list,
        questions: list = None,
    ) -> ToolResult:
        try:
            if questions is None:
                questions = [
                    "1. What did you do yesterday?",
                    "2. What will you do today?",
                    "3. Any blockers?",
                ]
            message = "🌅 Daily Standup Time!\n\nPlease share your update:\n" + "\n".join(questions)
            sent = 0
            for ch in team_channels:
                if ChatOpsAutomationTool._send_to_channel(ch.get("type", ""), ch.get("id", ""), message):
                    sent += 1
            return ToolResult(True, f"✓ Standup reminder sent to {sent} channels")
        except Exception as e:
            return ToolResult(False, f"✗ ChatOps send_daily_standup_reminder failed: {e}")

    @staticmethod
    def collect_standup_responses(
        channel: dict, timeout: int = 300
    ) -> ToolResult:
        try:
            import time

            ch_type = channel.get("type", "slack")
            ch_id   = channel.get("id", "")
            if ch_type != "slack":
                return ToolResult(False, "✗ collect_standup_responses currently supports Slack only.")
            from slack_sdk import WebClient
            token   = CredStore.load("slack").get("bot_token", "")
            client  = WebClient(token=token)
            start   = time.time()
            responses = []
            while time.time() - start < timeout:
                history = client.conversations_history(channel=ch_id, limit=20)
                for msg in history.get("messages", []):
                    if "subtype" not in msg and msg.get("text"):
                        responses.append({"user": msg.get("user", ""), "text": msg.get("text", "")})
                time.sleep(30)
            return ToolResult(True, f"✓ Collected {len(responses)} standup response(s)", responses)
        except Exception as e:
            return ToolResult(False, f"✗ ChatOps collect_standup_responses failed: {e}")

    @staticmethod
    def create_approval_workflow(
        request_title: str,
        details: str,
        approvers: list,
        channels: list = None,
    ) -> ToolResult:
        try:
            import uuid

            wf_id   = str(uuid.uuid4())[:8].upper()
            message = (
                f"📋 Approval Required [{wf_id}]\n"
                f"Title: {request_title}\n"
                f"Details: {details}\n"
                f"Approvers: {', '.join(approvers)}\n"
                f"Reply with APPROVE {wf_id} or REJECT {wf_id}"
            )
            ChatOpsAutomationTool._workflows[wf_id] = {
                "type":     "approval",
                "title":    request_title,
                "approvers": approvers,
                "status":   "pending",
            }
            sent = 0
            for ch in (channels or []):
                if ChatOpsAutomationTool._send_to_channel(ch.get("type", ""), ch.get("id", ""), message):
                    sent += 1
            return ToolResult(True, f"✓ Approval workflow {wf_id} created, sent to {sent} channels", {"workflow_id": wf_id})
        except Exception as e:
            return ToolResult(False, f"✗ ChatOps create_approval_workflow failed: {e}")

    @staticmethod
    def check_approval_status(workflow_id: str) -> ToolResult:
        try:
            wf = ChatOpsAutomationTool._workflows.get(workflow_id)
            if not wf:
                return ToolResult(False, f"✗ Workflow {workflow_id} not found.")
            return ToolResult(True, f"✓ Workflow {workflow_id} status: {wf.get('status', 'unknown')}", wf)
        except Exception as e:
            return ToolResult(False, f"✗ ChatOps check_approval_status failed: {e}")

    @staticmethod
    def broadcast_announcement(
        message: str, channels_config: list = None
    ) -> ToolResult:
        try:
            formatted = f"📢 ANNOUNCEMENT\n\n{message}"
            sent = 0
            for ch in (channels_config or []):
                if ChatOpsAutomationTool._send_to_channel(ch.get("type", ""), ch.get("id", ""), formatted):
                    sent += 1
            return ToolResult(True, f"✓ Announcement broadcast to {sent} channels")
        except Exception as e:
            return ToolResult(False, f"✗ ChatOps broadcast_announcement failed: {e}")

    @staticmethod
    def schedule_message(
        channel_type: str,
        channel_id: str,
        message: str,
        send_at: str,
    ) -> ToolResult:
        try:
            import threading
            from datetime import datetime

            target = datetime.fromisoformat(send_at)
            now    = datetime.utcnow()
            delay  = (target - now).total_seconds()
            if delay < 0:
                return ToolResult(False, "✗ send_at is in the past.")

            def _send():
                import time
                time.sleep(delay)
                ChatOpsAutomationTool._send_to_channel(channel_type, channel_id, message)

            threading.Thread(target=_send, daemon=True).start()
            return ToolResult(True, f"✓ Message scheduled to {channel_type}:{channel_id} at {send_at}")
        except Exception as e:
            return ToolResult(False, f"✗ ChatOps schedule_message failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────#############################################################################################
# 10. SMTPAdvancedTool
# ─────────────────────────────────────────────────────────────────────────────##############################################################################################

class SMTPAdvancedTool:######################################################################################################################################################
    name = "smtp_advanced"
    description = (
        "Advanced SMTP/IMAP email operations: HTML sending, templates, inbox monitoring, "
        "search, attachment download, auto-reply, forwarding, and filter rules."
    )

    @staticmethod
    def send_html_email(
        to: str,
        subject: str,
        html: str,
        from_addr: str = None,
        password: str = None,
        smtp_host: str = "smtp.gmail.com",
        port: int = 587,
        attachments: list = None,
        cc: list = None,
        bcc: list = None,
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
            from pathlib import Path

            creds    = CredStore.load(cred_key)
            user     = from_addr or creds.get("email", "")
            pwd      = password  or creds.get("password", "")
            host     = smtp_host or creds.get("smtp_host", "smtp.gmail.com")
            send_port= port      or int(creds.get("smtp_port", 587))

            msg = MIMEMultipart("alternative")
            msg["From"]    = user
            msg["To"]      = to
            msg["Subject"] = subject
            if cc:
                msg["Cc"] = ", ".join(cc)
            if bcc:
                msg["Bcc"] = ", ".join(bcc)
            msg.attach(MIMEText(html, "html"))

            if attachments:
                for path in attachments:
                    with open(path, "rb") as f:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={Path(path).name}")
                    msg.attach(part)

            all_rcpts = [to] + (cc or []) + (bcc or [])
            with smtplib.SMTP(host, send_port) as s:
                s.starttls()
                s.login(user, pwd)
                s.sendmail(user, all_rcpts, msg.as_string())
            return ToolResult(True, f"✓ HTML email sent to {to}")
        except Exception as e:
            return ToolResult(False, f"✗ SMTP send_html_email failed: {e}")

    @staticmethod
    def send_template_email(
        to: str,
        template_path: str,
        variables: dict,
        from_addr: str = None,
        password: str = None,
        subject: str = "Message from NPM Agent",
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            from jinja2 import Template
            from pathlib import Path

            raw_template = Path(template_path).read_text(encoding="utf-8")
            rendered     = Template(raw_template).render(**variables)
            return SMTPAdvancedTool.send_html_email(
                to=to, subject=subject, html=rendered,
                from_addr=from_addr, password=password, cred_key=cred_key,
            )
        except Exception as e:
            return ToolResult(False, f"✗ SMTP send_template_email failed: {e}")

    @staticmethod
    def monitor_inbox(
        email: str = None,
        password: str = None,
        imap_host: str = "imap.gmail.com",
        callback=None,
        folder: str = "INBOX",
        interval: int = 60,
        filter_from: str = "",
        filter_subject: str = "",
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            import imaplib, email as email_lib, threading, time

            creds = CredStore.load(cred_key)
            user  = email    or creds.get("email", "")
            pwd   = password or creds.get("password", "")
            host  = imap_host or creds.get("imap_host", "imap.gmail.com")
            seen_ids: set = set()

            def _watch():
                while True:
                    try:
                        mail = imaplib.IMAP4_SSL(host)
                        mail.login(user, pwd)
                        mail.select(folder)
                        criteria = "UNSEEN"
                        if filter_from:
                            criteria = f'(FROM "{filter_from}")'
                        if filter_subject:
                            criteria = f'(SUBJECT "{filter_subject}")'
                        _, ids = mail.search(None, criteria)
                        for mid in ids[0].split():
                            if mid in seen_ids:
                                continue
                            seen_ids.add(mid)
                            _, data = mail.fetch(mid, "(RFC822)")
                            msg = email_lib.message_from_bytes(data[0][1])
                            if callback:
                                callback({"from": msg["From"], "subject": msg["Subject"], "date": msg["Date"]})
                        mail.logout()
                    except Exception:
                        pass
                    time.sleep(interval)

            threading.Thread(target=_watch, daemon=True).start()
            return ToolResult(True, f"✓ Monitoring inbox {user} every {interval}s")
        except Exception as e:
            return ToolResult(False, f"✗ SMTP monitor_inbox failed: {e}")

    @staticmethod
    def search_emails(
        email: str = None,
        password: str = None,
        imap_host: str = "imap.gmail.com",
        criteria: str = "ALL",
        folder: str = "INBOX",
        limit: int = 20,
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            import imaplib, email as email_lib

            creds = CredStore.load(cred_key)
            user  = email    or creds.get("email", "")
            pwd   = password or creds.get("password", "")
            host  = imap_host or creds.get("imap_host", "imap.gmail.com")

            mail = imaplib.IMAP4_SSL(host)
            mail.login(user, pwd)
            mail.select(folder)
            _, ids = mail.search(None, criteria)
            results = []
            for mid in ids[0].split()[-limit:]:
                _, data = mail.fetch(mid, "(RFC822)")
                msg = email_lib.message_from_bytes(data[0][1])
                results.append({
                    "id":      mid.decode(),
                    "from":    msg["From"],
                    "subject": msg["Subject"],
                    "date":    msg["Date"],
                })
            mail.logout()
            return ToolResult(True, f"✓ Found {len(results)} emails", results)
        except Exception as e:
            return ToolResult(False, f"✗ SMTP search_emails failed: {e}")

    @staticmethod
    def download_attachments(
        email: str = None,
        password: str = None,
        imap_host: str = "imap.gmail.com",
        output_folder: str = "attachments",
        filter_from: str = "",
        filter_subject: str = "",
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            import imaplib, email as email_lib
            from pathlib import Path

            creds = CredStore.load(cred_key)
            user  = email    or creds.get("email", "")
            pwd   = password or creds.get("password", "")
            host  = imap_host or creds.get("imap_host", "imap.gmail.com")
            out   = Path(output_folder)
            out.mkdir(parents=True, exist_ok=True)

            mail = imaplib.IMAP4_SSL(host)
            mail.login(user, pwd)
            mail.select("INBOX")

            criteria = "ALL"
            if filter_from:
                criteria = f'(FROM "{filter_from}")'
            elif filter_subject:
                criteria = f'(SUBJECT "{filter_subject}")'

            _, ids = mail.search(None, criteria)
            saved = 0
            for mid in ids[0].split():
                _, data = mail.fetch(mid, "(RFC822)")
                msg = email_lib.message_from_bytes(data[0][1])
                for part in msg.walk():
                    if part.get_content_maintype() == "multipart":
                        continue
                    if part.get("Content-Disposition") is None:
                        continue
                    filename = part.get_filename()
                    if filename:
                        filepath = out / filename
                        filepath.write_bytes(part.get_payload(decode=True))
                        saved += 1
            mail.logout()
            return ToolResult(True, f"✓ Downloaded {saved} attachment(s) to {output_folder}")
        except Exception as e:
            return ToolResult(False, f"✗ SMTP download_attachments failed: {e}")

    @staticmethod
    def auto_reply(
        email: str = None,
        password: str = None,
        imap_host: str = "imap.gmail.com",
        reply_template: str = "Thank you for your email. We will get back to you soon.",
        filter_subject: str = "",
        only_unread: bool = True,
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            import imaplib, email as email_lib, smtplib
            from email.mime.text import MIMEText

            creds = CredStore.load(cred_key)
            user  = email    or creds.get("email", "")
            pwd   = password or creds.get("password", "")
            ihost = imap_host or creds.get("imap_host", "imap.gmail.com")
            shost = creds.get("smtp_host", "smtp.gmail.com")
            sport = int(creds.get("smtp_port", 587))

            mail = imaplib.IMAP4_SSL(ihost)
            mail.login(user, pwd)
            mail.select("INBOX")
            criteria = "UNSEEN" if only_unread else "ALL"
            if filter_subject:
                criteria = f'(SUBJECT "{filter_subject}")'
            _, ids = mail.search(None, criteria)
            replied = 0
            for mid in ids[0].split():
                _, data = mail.fetch(mid, "(RFC822)")
                msg  = email_lib.message_from_bytes(data[0][1])
                from_addr = email_lib.utils.parseaddr(msg["From"])[1]
                if not from_addr:
                    continue
                reply = MIMEText(reply_template)
                reply["From"]    = user
                reply["To"]      = from_addr
                reply["Subject"] = f"Re: {msg.get('Subject', '')}"
                with smtplib.SMTP(shost, sport) as s:
                    s.starttls(); s.login(user, pwd)
                    s.sendmail(user, [from_addr], reply.as_string())
                replied += 1
            mail.logout()
            return ToolResult(True, f"✓ Auto-replied to {replied} email(s)")
        except Exception as e:
            return ToolResult(False, f"✗ SMTP auto_reply failed: {e}")

    @staticmethod
    def forward_emails(
        email: str = None,
        password: str = None,
        imap_host: str = "imap.gmail.com",
        forward_to: str = "",
        filter_subject: str = "",
        delete_after: bool = False,
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            import imaplib, email as email_lib, smtplib

            creds = CredStore.load(cred_key)
            user  = email    or creds.get("email", "")
            pwd   = password or creds.get("password", "")
            ihost = imap_host or creds.get("imap_host", "imap.gmail.com")
            shost = creds.get("smtp_host", "smtp.gmail.com")
            sport = int(creds.get("smtp_port", 587))

            mail = imaplib.IMAP4_SSL(ihost)
            mail.login(user, pwd)
            mail.select("INBOX")
            criteria = f'(SUBJECT "{filter_subject}")' if filter_subject else "ALL"
            _, ids = mail.search(None, criteria)
            forwarded = 0
            for mid in ids[0].split():
                _, data = mail.fetch(mid, "(RFC822)")
                raw_email = data[0][1]
                with smtplib.SMTP(shost, sport) as s:
                    s.starttls(); s.login(user, pwd)
                    s.sendmail(user, [forward_to], raw_email)
                if delete_after:
                    mail.store(mid, "+FLAGS", "\\Deleted")
                forwarded += 1
            if delete_after:
                mail.expunge()
            mail.logout()
            return ToolResult(True, f"✓ Forwarded {forwarded} email(s) to {forward_to}")
        except Exception as e:
            return ToolResult(False, f"✗ SMTP forward_emails failed: {e}")

    @staticmethod
    def mark_as_read(
        email: str = None,
        password: str = None,
        imap_host: str = "imap.gmail.com",
        criteria: str = "UNSEEN",
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            import imaplib

            creds = CredStore.load(cred_key)
            user  = email    or creds.get("email", "")
            pwd   = password or creds.get("password", "")
            host  = imap_host or creds.get("imap_host", "imap.gmail.com")

            mail = imaplib.IMAP4_SSL(host)
            mail.login(user, pwd)
            mail.select("INBOX")
            _, ids = mail.search(None, criteria)
            count = 0
            for mid in ids[0].split():
                mail.store(mid, "+FLAGS", "\\Seen")
                count += 1
            mail.logout()
            return ToolResult(True, f"✓ Marked {count} email(s) as read")
        except Exception as e:
            return ToolResult(False, f"✗ SMTP mark_as_read failed: {e}")

    @staticmethod
    def delete_emails(
        email: str = None,
        password: str = None,
        imap_host: str = "imap.gmail.com",
        criteria: str = "ALL",
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            import imaplib

            creds = CredStore.load(cred_key)
            user  = email    or creds.get("email", "")
            pwd   = password or creds.get("password", "")
            host  = imap_host or creds.get("imap_host", "imap.gmail.com")

            mail = imaplib.IMAP4_SSL(host)
            mail.login(user, pwd)
            mail.select("INBOX")
            _, ids = mail.search(None, criteria)
            count = 0
            for mid in ids[0].split():
                mail.store(mid, "+FLAGS", "\\Deleted")
                count += 1
            mail.expunge()
            mail.logout()
            return ToolResult(True, f"✓ Deleted {count} email(s)")
        except Exception as e:
            return ToolResult(False, f"✗ SMTP delete_emails failed: {e}")

    @staticmethod
    def create_filter_rule(
        email: str = None,
        password: str = None,
        imap_host: str = "imap.gmail.com",
        from_addr: str = "",
        action: str = "move",
        folder: str = "INBOX",
        cred_key: str = "smtp",
    ) -> ToolResult:
        try:
            import imaplib, email as email_lib

            creds = CredStore.load(cred_key)
            user  = email    or creds.get("email", "")
            pwd   = password or creds.get("password", "")
            host  = imap_host or creds.get("imap_host", "imap.gmail.com")

            mail = imaplib.IMAP4_SSL(host)
            mail.login(user, pwd)
            mail.select("INBOX")
            _, ids = mail.search(None, f'(FROM "{from_addr}")')
            count = 0
            for mid in ids[0].split():
                if action == "move":
                    mail.copy(mid, folder)
                    mail.store(mid, "+FLAGS", "\\Deleted")
                    count += 1
                elif action == "delete":
                    mail.store(mid, "+FLAGS", "\\Deleted")
                    count += 1
                elif action == "mark_read":
                    mail.store(mid, "+FLAGS", "\\Seen")
                    count += 1
            if action in ("move", "delete"):
                mail.expunge()
            mail.logout()
            return ToolResult(True, f"✓ Filter rule applied: {action} {count} email(s) from {from_addr}")
        except Exception as e:
            return ToolResult(False, f"✗ SMTP create_filter_rule failed: {e}")
