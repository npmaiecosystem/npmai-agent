"""
tools_system_hardware.py
NPM Agent — NPMAI ECOSYSTEM by Sonu Kumar
System & Hardware vertical: OS, Network, FileSystem, GUI Automation, Printers,
Clipboard, Hardware Monitor, Raspberry Pi, MQTT/IoT, Virtualization
"""

import sys, subprocess, platform

def _ensure(pkg: str, import_name: str = None):
    n = import_name or pkg
    try:
        __import__(n)
    except:
        try:
          subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"], check=False)
        except:
          print(f"Some packages is not installed properly in your environment due to some reasons these are the packages {n}")

for _p, _i in [
    ("psutil",            "psutil"),
    ("py-cpuinfo",        "cpuinfo"),
    ("GPUtil",            "GPUtil"),
    ("scapy",             "scapy"),
    ("paramiko",          "paramiko"),
    ("requests",          "requests"),
    ("watchdog",          "watchdog"),
    ("cryptography",      "cryptography"),
    ("pyautogui",         "pyautogui"),
    ("pygetwindow",       "pygetwindow"),
    ("keyboard",          "keyboard"),
    ("mouse",             "mouse"),
    ("pynput",            "pynput"),
    ("pyperclip",         "pyperclip"),
    ("Pillow",            "PIL"),
    ("paho-mqtt",         "paho"),
    ("python-whois",      "whois"),
]:
    if _p:
        _ensure(_p, _i)

_OS = platform.system()
if _OS == "Windows":
    _ensure("pywin32", "win32api")

from .core import ToolResult, CredStore


# ─────────────────────────────────────────────────────────────────────────────
# 1. SystemAdvancedTool
# ─────────────────────────────────────────────────────────────────────────────

class SystemAdvancedTool:
    name = "system_advanced"
    description = (
        "Deep OS operations cross-platform: system info, services, cron, firewall, startup, "
        "hosts file, DNS, programs, restore points, volume, battery, USB, drives."
    )
    use = ("""
Name of Tool:- SystemAdvancedTool

Purpose of Tool:- 
The SystemAdvancedTool provides a comprehensive cross-platform interface for performing deep Operating System operations. 
It supports robust hardware monitoring, detailed system resource reporting, service lifecycle orchestration (Windows, macOS, Linux), 
cron/scheduled task automation, host-file layout mutations, live DNS flushing, package/program inventory evaluations, uninstall sequences, 
Windows restore point baselines, software volume tracking, real-time peripheral diagnostic queries (battery, USB layouts), and disk 
lifecycle actions (ejection, multi-filesystem drive formatting).
This tool is designed for systemic automation, engineering infrastructure monitoring, and system-level agent configurations across 
Windows, macOS, and Linux kernels.

Methods:-
- get_full_system_info: Collects core operating system, environment, processing core configurations, memory capacity, and platform runtime context metrics.
- get_hardware_info: Collects diagnostic state frames mapping physical core utilities, partition tables, disk storage maps, interface network configurations, and systemic thermal/fan telemetry if fully initialized.
- manage_service: Modulates platform-native background system services (state updates like starting, stopping, reloading, restarting) via sub-layer system calls.
- list_services: Fetches an exhaustive string matrix representation of active and inactive background tasks running via standard system service layers.
- create_cron_job: Inserts system-scheduled crontab workflows or task-scheduler executions targeting persistent operational workflows.
- list_cron_jobs: Enumerates raw multi-line records tracking existing system scripts bound inside crontab schemas or scheduler configurations.
- remove_cron_job: Filters matching commands out of underlying automation crontabs or task-scheduler repositories to clear execution routines.
- manage_firewall: Alters local machine operational connectivity profiles to filter target TCP/UDP ports or process active configurations.
- create_startup_item: Configures system hooks within the registry matrix, plist launch domains, or target init configurations for boot executions.
- remove_startup_item: Disables and destroys configurations keeping target startup services initialized at early boot runtime environments.
- manage_hosts_file: Manipulates or extracts explicit local static domain-name target routes matching defined IP network configurations.
- flush_dns: Invalidates operating system local resolve caches to clear path bindings on dynamic network configurations.
- get_installed_programs: Indexes system software registries, application paths, or system package managers to build an exhaustive binary landscape.
- uninstall_program: Forces automated native application execution sequences to remove files and target binaries.
- create_restore_point: Instantiates a persistent system recovery index on Windows environments to safe-keep current OS files.
- list_restore_points: Queries the structural historical timeline listing existing Windows restore configurations and baseline indexes.
- set_system_volume: Updates physical master terminal system audio indicators by mapping a concrete percentage index context.
- get_battery_info: Reports systemic hardware cell metrics including structural depletion percentages, line power connection vectors, and remaining lifespan estimations.
- set_screen_brightness: Programs display hardware control lines to re-index the operational target balance parameters on laptop panels.
- list_usb_devices: Discovers structural multi-class USB processing trees and attached hardware interface devices currently reporting connections.
- eject_drive: Performs safely handled block-level unmount operations targeting local drives or removeable media layouts.
- format_drive: Overwrites layout headers and builds clean multi-flavor structural platforms targeting disk file containers.

How to use Tool Methods:-

1. get_full_system_info:
   - Purpose: Collects an overarching diagnostic frame aggregating OS platform identifiers, CPU designators, physical core indexes, RAM capacities, dynamic tracking margins, root storage availability layouts, and baseline boot epoch times.
   - Arguments: None.
   - Returns: ToolResult tracking successful completion status, validation strings, and a dictionary packing platform markers.
   - How to call: SystemAdvancedTool.get_full_system_info()

2. get_hardware_info:
   - Purpose: Samples underlying computing sub-components to deliver structured reports charting component-by-component hardware utilization rates and device state parameters.
   - Arguments:
     a) detail_level: str (default: "basic") - Selects analytical depths. Choosing "full" appends live thermal structural sensors and cooling fan rotational reporting data matrices where hardware access permissions permit.
   - Returns: ToolResult indicating diagnostic generation status, diagnostic logging strings, and a nested hardware configuration topology dictionary.
   - How to call: SystemAdvancedTool.get_hardware_info(detail_level="full")

3. manage_service:
   - Purpose: Programmatically dispatches command directives controlling platform background daemons, running through Windows "sc", macOS "launchctl", or Linux "systemctl" frameworks.
   - Arguments:
     a) name: str - The specific target identifier labeling the service structure under configuration.
     b) action: str - Command action to execute (e.g., "start", "stop", "restart", "reload").
     c) os_platform: str (default: None) - Manually target platform overrides. Leaves mapping automated based on detected system metrics when unassigned.
   - Returns: ToolResult outlining processing success parameters alongside captured process output logs.
   - How to call: SystemAdvancedTool.manage_service(name="nginx", action="restart", os_platform="Linux")

4. list_services:
   - Purpose: Queries standard system management tools to output a unified textual list mapping all registered service elements matching targeted parameter spaces.
   - Arguments:
     a) os_platform: str (default: None) - Directs selection variables targeting explicit OS environments. Falls back to local auto-detection if none provided.
     b) status_filter: str (default: "") - Token match string applied to filter matching output list elements during compilation stages.
   - Returns: ToolResult holding evaluation success markers and a multi-string sequence tracking individual lines of active components.
   - How to call: SystemAdvancedTool.list_services(os_platform="Windows", status_filter="running")

5. create_cron_job:
   - Purpose: Schedules an automated application execution rule set based on crontab parameters for Unix structures or daily Scheduled Tasks ("schtasks") environments for Windows setups.
   - Arguments:
     a) command: str - Raw programmatic script strings, application paths, or shell execution sequences targeted for persistent scheduling.
     b) schedule: str - Unix standard positional time instruction rulesets (e.g., "* * * * *") mapped down to simple hour/minute specifications when matching Windows environments.
     c) user: str (default: None) - Context parameter allocating target user table mappings on Linux configurations.
   - Returns: ToolResult capturing operational deployment success metrics alongside validation logs.
   - How to call: SystemAdvancedTool.create_cron_job(command="/usr/bin/backup.sh", schedule="0 2 * * *")

6. list_cron_jobs:
   - Purpose: Exposes automated execution timelines by dumping individual entries found across active scheduled user tasks or system crontab tables.
   - Arguments:
     a) user: str (default: None) - Filters results for a specific username when querying multi-user crontab registers.
   - Returns: ToolResult with completion flags accompanied by a string matrix sorting target operational lines.
   - How to call: SystemAdvancedTool.list_cron_jobs(user="root")

7. remove_cron_job:
   - Purpose: Scrubs scheduled scripts from automation registers by eliminating all table configuration records matching tracking criteria strings.
   - Arguments:
     a) command: str - Substring string target used to scan and remove items from scheduling system tables.
   - Returns: ToolResult tracking completion validation flags along with descriptive process results text.
   - How to call: SystemAdvancedTool.remove_cron_job(command="/usr/bin/backup.sh")

8. manage_firewall:
   - Purpose: Re-allocates ingress network packet filters across platform interface utilities like Windows Advanced Firewall netsh profiles, Apple pfctl configurations, or Linux ufw tools.
   - Arguments:
     a) action: str - Security action directive to enforce on the firewall stack (e.g., "allow", "deny", "status").
     b) port: int (default: None) - Numeric target network port marker targeted for explicit programmatic entry changes.
     c) protocol: str (default: "tcp") - Operational transport layer tracking scheme selector, typically supporting "tcp" or "udp" models.
     d) source_ip: str (default: "any") - Source network address constraints filtering packet traffic routes.
     e) os_platform: str (default: None) - Selects operational engine context maps. Automatically resolves from local platform signatures if left empty.
   - Returns: ToolResult formatting processing success conditions and reporting systemic responses.
   - How to call: SystemAdvancedTool.manage_firewall(action="allow", port=8080, protocol="tcp")

9. create_startup_item:
   - Purpose: Injects tracking links into the system to run targeted scripts automatically upon boot-up, using the Windows HKCU Run registry path, macOS LaunchAgents plist directories, or systemd target definitions.
   - Arguments:
     a) name: str - Target application descriptor tagging deployment configs.
     b) command: str - The specific target terminal execution command string triggered on boot events.
     c) os_platform: str (default: None) - System processing environment engine target switcher.
   - Returns: ToolResult displaying status parameters alongside execution logging frames.
   - How to call: SystemAdvancedTool.create_startup_item(name="MyAgent", command="/usr/local/bin/agent --start")

10. remove_startup_item:
    - Purpose: Removes application entries from system startup registers to prevent them from executing on next boot.
    - Arguments:
      a) name: str - Label identifier targeting files or key values slated for removal from startup configurations.
      b) os_platform: str (default: None) - System architectural processing framework selector switch override.
    - Returns: ToolResult detailing execution completion properties.
    - How to call: SystemAdvancedTool.remove_startup_item(name="MyAgent")

11. manage_hosts_file:
    - Purpose: Processes read, update, or clear mutations directly on system local networking resolution route tables.
    - Arguments:
      a) action: str - Explicit file operation direction target choice supporting parameters "add", "remove", or "list".
      b) ip: str (default: "") - Specific IP network destination routing node parameter string mapped during actions.
      c) hostname: str (default: "") - Target network naming label reference used during configuration modifications.
    - Returns: ToolResult packaging structural mapping evaluation flags alongside multi-line operational data blocks.
    - How to call: SystemAdvancedTool.manage_hosts_file(action="add", ip="127.0.0.1", hostname="local.test")

12. flush_dns:
    - Purpose: Purges operating system runtime domain resolution memory stores to force live cache updates over changing routing structures.
    - Arguments: None.
    - Returns: ToolResult outlining flush tracking confirmations and operation status values.
    - How to call: SystemAdvancedTool.flush_dns()

13. get_installed_programs:
    - Purpose: Indexes system locations such as Windows Uninstall paths, macOS Application structures, or Linux package registers (dpkg/rpm) to build a software tracking matrix.
    - Arguments:
      a) os_platform: str (default: None) - Architectural layout override switch targeting cross-system engines.
    - Returns: ToolResult providing success state metadata alongside an array sequence containing discovered application names.
    - How to call: SystemAdvancedTool.get_installed_programs(os_platform="Linux")

14. uninstall_program:
    - Purpose: Invokes native package removals or system application delete operations to erase tools from processing directories.
    - Arguments:
      a) name: str - Specific name key or program label pattern searched for during uninstall execution loops.
      b) os_platform: str (default: None) - Platform environment selector tracking operating conditions.
    - Returns: ToolResult declaring total tracking removal success indicators and application output logging.
    - How to call: SystemAdvancedTool.uninstall_program(name="badapp")

15. create_restore_point:
    - Purpose: Generates a system baseline state record via Windows PowerShell checkpoint utilities to protect operational states before running updates.
    - Arguments:
      a) description: str - Human-readable comment detailing why the restore point was generated.
    - Returns: ToolResult charting checkpoint production status or reporting validation blockages on non-supported OS targets.
    - How to call: SystemAdvancedTool.create_restore_point(description="Before Major Update")

16. list_restore_points:
    - Purpose: Returns historical indices containing dates and descriptions of previously compiled Windows restore operations.
    - Arguments: None.
    - Returns: ToolResult mapping data compilation states alongside list arrays outlining restore configuration rows.
    - How to call: SystemAdvancedTool.list_restore_points()

17. set_system_volume:
    - Purpose: Directly updates active terminal system audio processing attributes by enforcing concrete balance limits across standard platform engines.
    - Arguments:
      a) percent: int - Int parameter ranging between 0 and 100 pointing to the targeted sound pressure audio level.
    - Returns: ToolResult confirming new volume setting levels.
    - How to call: SystemAdvancedTool.set_system_volume(percent=75)

18. get_battery_info:
    - Purpose: Accesses system internal power infrastructure interfaces to track battery performance metrics.
    - Arguments: None.
    - Returns: ToolResult outputting runtime power status details including current remaining charge metrics, power brick connectivity states, and remaining runtime estimates.
    - How to call: SystemAdvancedTool.get_battery_info()

19. set_screen_brightness:
    - Purpose: Adjusts active visual monitor backlighting power levels via platform-native interface pathways.
    - Arguments:
      a) percent: int - Int target bounded from 0 to 100 mapping out the target screen visibility coefficient.
    - Returns: ToolResult documenting tracking change validations.
    - How to call: SystemAdvancedTool.set_screen_brightness(percent=80)

20. list_usb_devices:
    - Purpose: Triggers deep subsystem processing hardware walks to collect raw JSON metadata arrays or text representations enumerating visible USB devices.
    - Arguments: None.
    - Returns: ToolResult tracking parsing success parameters along with data records logging connected devices.
    - How to call: SystemAdvancedTool.list_usb_devices()

21. eject_drive:
    - Purpose: Unmounts specified target partitions or removeable hardware mount blocks cleanly to prevent data corruption.
    - Arguments:
      a) drive_path: str - Target filesystem mount route designation, storage label pattern, or platform volume reference (e.g., "E:", "/dev/sdb1").
    - Returns: ToolResult displaying execution validation logs and partition state reports.
    - How to call: SystemAdvancedTool.eject_drive(drive_path="E:")

22. format_drive:
    - Purpose: Erases structural sector properties and builds a fresh, clean filesystem framework across targeted storage blocks.
    - Arguments:
      a) drive_path: str - Targeted volume identifier or path reference pointing to the destination hardware block under configuration.
      b) filesystem: str (default: "ext4") - Filesystem format layout selection token (e.g., "ext4", "ntfs", "fat32", "exfat").
      c) label: str (default: "") - Appends a volume label name identifier to the formatted disk space.
    - Returns: ToolResult packing formatting block processing success indicators along with sub-layer terminal execution details.
    - How to call: SystemAdvancedTool.format_drive(drive_path="/dev/sdb1", filesystem="ext4", label="BackupDrive")
""")

    @staticmethod
    def get_full_system_info() -> ToolResult:
        try:
            import psutil, cpuinfo

            cpu   = cpuinfo.get_cpu_info()
            vmem  = psutil.virtual_memory()
            disk  = psutil.disk_usage("/")
            boot  = psutil.boot_time()
            from datetime import datetime
            info = {
                "os":            platform.platform(),
                "hostname":      platform.node(),
                "cpu_brand":     cpu.get("brand_raw", ""),
                "cpu_cores_phys": psutil.cpu_count(logical=False),
                "cpu_cores_log":  psutil.cpu_count(logical=True),
                "cpu_freq_mhz":  psutil.cpu_freq().current if psutil.cpu_freq() else 0,
                "ram_total_gb":  round(vmem.total / 1e9, 2),
                "ram_used_gb":   round(vmem.used  / 1e9, 2),
                "disk_total_gb": round(disk.total / 1e9, 2),
                "disk_free_gb":  round(disk.free  / 1e9, 2),
                "boot_time":     datetime.fromtimestamp(boot).isoformat(),
                "python":        platform.python_version(),
            }
            return ToolResult(True, "✓ Full system info fetched", info)
        except Exception as e:
            return ToolResult(False, f"✗ get_full_system_info failed: {e}")

    @staticmethod
    def get_hardware_info(detail_level: str = "basic") -> ToolResult:
        try:
            import psutil

            data: dict = {}
            # CPU
            data["cpu"] = {
                "logical_cores":  psutil.cpu_count(logical=True),
                "physical_cores": psutil.cpu_count(logical=False),
                "percent":        psutil.cpu_percent(interval=1, percpu=True),
                "freq":           psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
            }
            # Memory
            vm = psutil.virtual_memory()
            sw = psutil.swap_memory()
            data["memory"] = {"virtual": vm._asdict(), "swap": sw._asdict()}
            # Disks
            data["disks"] = [
                {"device": p.device, "mountpoint": p.mountpoint,
                 "fstype": p.fstype, "usage": psutil.disk_usage(p.mountpoint)._asdict()}
                for p in psutil.disk_partitions(all=False)
            ]
            # Network
            nics = psutil.net_if_addrs()
            data["network"] = {k: [a._asdict() for a in v] for k, v in nics.items()}
            if detail_level == "full":
                data["sensors"] = {}
                try:
                    temps = psutil.sensors_temperatures()
                    data["sensors"]["temperatures"] = {k: [t._asdict() for t in v] for k, v in (temps or {}).items()}
                    fans = psutil.sensors_fans()
                    data["sensors"]["fans"] = {k: [f._asdict() for f in v] for k, v in (fans or {}).items()}
                except Exception:
                    pass
            return ToolResult(True, "✓ Hardware info fetched", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_hardware_info failed: {e}")

    @staticmethod
    def manage_service(name: str, action: str, os_platform: str = None) -> ToolResult:
        try:
            os_platform = os_platform or platform.system()
            if os_platform == "Windows":
                r = subprocess.run(["sc", action, name], capture_output=True, text=True)
            elif os_platform == "Darwin":
                r = subprocess.run(["launchctl", action, name], capture_output=True, text=True)
            else:
                r = subprocess.run(["systemctl", action, name], capture_output=True, text=True)
            out = r.stdout + r.stderr
            return ToolResult(r.returncode == 0, f"✓ Service '{name}' {action}" if r.returncode == 0 else out.strip())
        except Exception as e:
            return ToolResult(False, f"✗ manage_service failed: {e}")

    @staticmethod
    def list_services(os_platform: str = None, status_filter: str = "") -> ToolResult:
        try:
            os_platform = os_platform or platform.system()
            if os_platform == "Windows":
                r = subprocess.run(["sc", "query", "type=", "all", "state=", "all"],
                                   capture_output=True, text=True)
            elif os_platform == "Darwin":
                r = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
            else:
                r = subprocess.run(["systemctl", "list-units", "--type=service", "--no-pager"],
                                   capture_output=True, text=True)
            lines = r.stdout.splitlines()
            if status_filter:
                lines = [l for l in lines if status_filter.lower() in l.lower()]
            return ToolResult(True, f"✓ {len(lines)} service lines found", lines)
        except Exception as e:
            return ToolResult(False, f"✗ list_services failed: {e}")

    @staticmethod
    def create_cron_job(command: str, schedule: str, user: str = None) -> ToolResult:
        try:
            if platform.system() == "Windows":
                parts  = schedule.split()
                minute = parts[0] if len(parts) > 0 else "0"
                hour   = parts[1] if len(parts) > 1 else "*"
                r = subprocess.run(
                    ["schtasks", "/create", "/tn", command[:20], "/tr", command,
                     "/sc", "DAILY", "/st", f"{hour.zfill(2)}:{minute.zfill(2)}", "/f"],
                    capture_output=True, text=True,
                )
                return ToolResult(r.returncode == 0, r.stdout + r.stderr)
            import tempfile, os
            r = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            existing = r.stdout if r.returncode == 0 else ""
            new_entry = f"{schedule} {command}\n"
            if new_entry.strip() in existing:
                return ToolResult(True, "✓ Cron job already exists")
            with tempfile.NamedTemporaryFile(mode="w", suffix=".cron", delete=False) as tmp:
                tmp.write(existing + new_entry)
                tmp_path = tmp.name
            r2 = subprocess.run(["crontab", tmp_path], capture_output=True, text=True)
            os.unlink(tmp_path)
            return ToolResult(r2.returncode == 0, f"✓ Cron job created: {schedule} {command}")
        except Exception as e:
            return ToolResult(False, f"✗ create_cron_job failed: {e}")

    @staticmethod
    def list_cron_jobs(user: str = None) -> ToolResult:
        try:
            if platform.system() == "Windows":
                r = subprocess.run(["schtasks", "/query", "/fo", "LIST"], capture_output=True, text=True)
                return ToolResult(True, "✓ Scheduled tasks fetched", r.stdout.splitlines())
            cmd = ["crontab", "-l"]
            if user:
                cmd = ["crontab", "-l", "-u", user]
            r = subprocess.run(cmd, capture_output=True, text=True)
            lines = [l for l in r.stdout.splitlines() if l.strip() and not l.startswith("#")]
            return ToolResult(True, f"✓ {len(lines)} cron job(s)", lines)
        except Exception as e:
            return ToolResult(False, f"✗ list_cron_jobs failed: {e}")

    @staticmethod
    def remove_cron_job(command: str) -> ToolResult:
        try:
            if platform.system() == "Windows":
                r = subprocess.run(["schtasks", "/delete", "/tn", command[:20], "/f"],
                                   capture_output=True, text=True)
                return ToolResult(r.returncode == 0, r.stdout + r.stderr)
            import tempfile, os
            r = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            lines = [l for l in r.stdout.splitlines() if command not in l]
            with tempfile.NamedTemporaryFile(mode="w", suffix=".cron", delete=False) as tmp:
                tmp.write("\n".join(lines) + "\n")
                tmp_path = tmp.name
            r2 = subprocess.run(["crontab", tmp_path], capture_output=True, text=True)
            os.unlink(tmp_path)
            return ToolResult(r2.returncode == 0, f"✓ Cron job removed: {command}")
        except Exception as e:
            return ToolResult(False, f"✗ remove_cron_job failed: {e}")

    @staticmethod
    def manage_firewall(
        action: str,
        port: int = None,
        protocol: str = "tcp",
        source_ip: str = "any",
        os_platform: str = None,
    ) -> ToolResult:
        try:
            os_platform = os_platform or platform.system()
            if os_platform == "Windows":
                if action == "allow" and port:
                    r = subprocess.run([
                        "netsh", "advfirewall", "firewall", "add", "rule",
                        f"name=NPMAgent_{port}", "dir=in", "action=allow",
                        f"protocol={protocol}", f"localport={port}",
                    ], capture_output=True, text=True)
                elif action == "deny" and port:
                    r = subprocess.run([
                        "netsh", "advfirewall", "firewall", "add", "rule",
                        f"name=NPMAgent_BLOCK_{port}", "dir=in", "action=block",
                        f"protocol={protocol}", f"localport={port}",
                    ], capture_output=True, text=True)
                elif action == "status":
                    r = subprocess.run(["netsh", "advfirewall", "show", "allprofiles"],
                                       capture_output=True, text=True)
                else:
                    return ToolResult(False, f"✗ Unknown firewall action: {action}")
            elif os_platform == "Darwin":
                if action in ("allow", "deny"):
                    r = subprocess.run(["pfctl", "-f", "/etc/pf.conf"], capture_output=True, text=True)
                else:
                    r = subprocess.run(["pfctl", "-s", "all"], capture_output=True, text=True)
            else:
                if action == "allow" and port:
                    r = subprocess.run(["ufw", "allow", f"{port}/{protocol}"], capture_output=True, text=True)
                elif action == "deny" and port:
                    r = subprocess.run(["ufw", "deny", f"{port}/{protocol}"], capture_output=True, text=True)
                elif action == "status":
                    r = subprocess.run(["ufw", "status", "verbose"], capture_output=True, text=True)
                else:
                    return ToolResult(False, f"✗ Unknown firewall action: {action}")
            return ToolResult(r.returncode == 0, r.stdout + r.stderr)
        except Exception as e:
            return ToolResult(False, f"✗ manage_firewall failed: {e}")

    @staticmethod
    def create_startup_item(name: str, command: str, os_platform: str = None) -> ToolResult:
        try:
            os_platform = os_platform or platform.system()
            if os_platform == "Windows":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Run",
                                     0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, name, 0, winreg.REG_SZ, command)
                winreg.CloseKey(key)
            elif os_platform == "Darwin":
                import plistlib
                from pathlib import Path
                plist = {
                    "Label": f"com.npmai.{name}",
                    "ProgramArguments": command.split(),
                    "RunAtLoad": True,
                }
                dest = Path.home() / "Library" / "LaunchAgents" / f"com.npmai.{name}.plist"
                dest.parent.mkdir(parents=True, exist_ok=True)
                with open(dest, "wb") as f:
                    plistlib.dump(plist, f)
                subprocess.run(["launchctl", "load", str(dest)], capture_output=True)
            else:
                from pathlib import Path
                service = f"""[Unit]
Description={name}
After=network.target

[Service]
ExecStart={command}
Restart=always

[Install]
WantedBy=multi-user.target
"""
                dest = Path(f"/etc/systemd/system/{name}.service")
                dest.write_text(service)
                subprocess.run(["systemctl", "enable", name], capture_output=True)
            return ToolResult(True, f"✓ Startup item '{name}' created")
        except Exception as e:
            return ToolResult(False, f"✗ create_startup_item failed: {e}")

    @staticmethod
    def remove_startup_item(name: str, os_platform: str = None) -> ToolResult:
        try:
            os_platform = os_platform or platform.system()
            if os_platform == "Windows":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Run",
                                     0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, name)
                winreg.CloseKey(key)
            elif os_platform == "Darwin":
                from pathlib import Path
                dest = Path.home() / "Library" / "LaunchAgents" / f"com.npmai.{name}.plist"
                subprocess.run(["launchctl", "unload", str(dest)], capture_output=True)
                dest.unlink(missing_ok=True)
            else:
                subprocess.run(["systemctl", "disable", name], capture_output=True)
                from pathlib import Path
                Path(f"/etc/systemd/system/{name}.service").unlink(missing_ok=True)
            return ToolResult(True, f"✓ Startup item '{name}' removed")
        except Exception as e:
            return ToolResult(False, f"✗ remove_startup_item failed: {e}")

    @staticmethod
    def manage_hosts_file(action: str, ip: str = "", hostname: str = "") -> ToolResult:
        try:
            import re
            from pathlib import Path
            hosts_path = Path("C:/Windows/System32/drivers/etc/hosts") if platform.system() == "Windows" \
                else Path("/etc/hosts")
            content = hosts_path.read_text()
            if action == "add":
                entry = f"\n{ip}\t{hostname}"
                if hostname in content:
                    return ToolResult(True, f"✓ Entry already exists for {hostname}")
                hosts_path.write_text(content + entry)
                return ToolResult(True, f"✓ Added {ip} → {hostname} to hosts file")
            elif action == "remove":
                new_content = re.sub(rf".*\s+{re.escape(hostname)}\s*\n?", "", content)
                hosts_path.write_text(new_content)
                return ToolResult(True, f"✓ Removed {hostname} from hosts file")
            elif action == "list":
                lines = [l for l in content.splitlines() if l.strip() and not l.startswith("#")]
                return ToolResult(True, f"✓ {len(lines)} hosts entries", lines)
            return ToolResult(False, f"✗ Unknown action: {action}")
        except Exception as e:
            return ToolResult(False, f"✗ manage_hosts_file failed: {e}")

    @staticmethod
    def flush_dns() -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                r = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True)
            elif os_name == "Darwin":
                r = subprocess.run(["dscacheutil", "-flushcache"], capture_output=True, text=True)
                subprocess.run(["killall", "-HUP", "mDNSResponder"], capture_output=True)
            else:
                r = subprocess.run(["systemd-resolve", "--flush-caches"], capture_output=True, text=True)
                if r.returncode != 0:
                    r = subprocess.run(["service", "dns-clean", "restart"], capture_output=True, text=True)
            return ToolResult(True, "✓ DNS cache flushed")
        except Exception as e:
            return ToolResult(False, f"✗ flush_dns failed: {e}")

    @staticmethod
    def get_installed_programs(os_platform: str = None) -> ToolResult:
        try:
            os_platform = os_platform or platform.system()
            programs = []
            if os_platform == "Windows":
                import winreg
                for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                    for path in [
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
                    ]:
                        try:
                            key = winreg.OpenKey(hive, path)
                            for i in range(winreg.QueryInfoKey(key)[0]):
                                try:
                                    subkey_name = winreg.EnumKey(key, i)
                                    subkey = winreg.OpenKey(key, subkey_name)
                                    name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                    programs.append(name)
                                except Exception:
                                    pass
                        except Exception:
                            pass
            elif os_platform == "Darwin":
                r = subprocess.run(["ls", "/Applications"], capture_output=True, text=True)
                programs = [l.replace(".app", "") for l in r.stdout.splitlines() if l.endswith(".app")]
            else:
                r = subprocess.run(["dpkg", "--get-selections"], capture_output=True, text=True)
                if r.returncode == 0:
                    programs = [l.split()[0] for l in r.stdout.splitlines() if "install" in l]
                else:
                    r2 = subprocess.run(["rpm", "-qa"], capture_output=True, text=True)
                    programs = r2.stdout.splitlines()
            return ToolResult(True, f"✓ {len(programs)} installed programs found", programs)
        except Exception as e:
            return ToolResult(False, f"✗ get_installed_programs failed: {e}")

    @staticmethod
    def uninstall_program(name: str, os_platform: str = None) -> ToolResult:
        try:
            os_platform = os_platform or platform.system()
            if os_platform == "Windows":
                r = subprocess.run(
                    ["wmic", "product", "where", f'name="{name}"', "call", "uninstall", "/nointeractive"],
                    capture_output=True, text=True,
                )
            elif os_platform == "Darwin":
                from pathlib import Path
                app_path = f"/Applications/{name}.app"
                r = subprocess.run(["rm", "-rf", app_path], capture_output=True, text=True)
            else:
                r = subprocess.run(["apt-get", "remove", "-y", name], capture_output=True, text=True)
                if r.returncode != 0:
                    r = subprocess.run(["yum", "remove", "-y", name], capture_output=True, text=True)
            return ToolResult(r.returncode == 0, f"✓ Uninstalled: {name}" if r.returncode == 0 else r.stderr)
        except Exception as e:
            return ToolResult(False, f"✗ uninstall_program failed: {e}")

    @staticmethod
    def create_restore_point(description: str) -> ToolResult:
        try:
            if platform.system() != "Windows":
                return ToolResult(False, "✗ Restore points are Windows-only.")
            r = subprocess.run(
                ["powershell", "-Command",
                 f'Checkpoint-Computer -Description "{description}" -RestorePointType MODIFY_SETTINGS'],
                capture_output=True, text=True,
            )
            return ToolResult(r.returncode == 0, f"✓ Restore point created: {description}")
        except Exception as e:
            return ToolResult(False, f"✗ create_restore_point failed: {e}")

    @staticmethod
    def list_restore_points() -> ToolResult:
        try:
            if platform.system() != "Windows":
                return ToolResult(False, "✗ Restore points are Windows-only.")
            r = subprocess.run(
                ["powershell", "-Command", "Get-ComputerRestorePoint | Select-Object Description,CreationTime"],
                capture_output=True, text=True,
            )
            return ToolResult(True, "✓ Restore points listed", r.stdout.splitlines())
        except Exception as e:
            return ToolResult(False, f"✗ list_restore_points failed: {e}")

    @staticmethod
    def set_system_volume(percent: int) -> ToolResult:
        try:
            percent = max(0, min(100, percent))
            os_name = platform.system()
            if os_name == "Windows":
                r = subprocess.run(
                    ["powershell", "-Command",
                     f"$obj = New-Object -ComObject WScript.Shell; $obj.SendKeys([char]174*{(100-percent)//2})"],
                    capture_output=True,
                )
            elif os_name == "Darwin":
                r = subprocess.run(["osascript", "-e", f"set volume output volume {percent}"],
                                   capture_output=True, text=True)
            else:
                r = subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{percent}%"],
                                   capture_output=True, text=True)
            return ToolResult(True, f"✓ Volume set to {percent}%")
        except Exception as e:
            return ToolResult(False, f"✗ set_system_volume failed: {e}")

    @staticmethod
    def get_battery_info() -> ToolResult:
        try:
            import psutil
            battery = psutil.sensors_battery()
            if not battery:
                return ToolResult(False, "✗ No battery detected.")
            return ToolResult(True, f"✓ Battery: {battery.percent:.1f}%", {
                "percent":    round(battery.percent, 1),
                "plugged_in": battery.power_plugged,
                "secs_left":  battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited",
            })
        except Exception as e:
            return ToolResult(False, f"✗ get_battery_info failed: {e}")

    @staticmethod
    def set_screen_brightness(percent: int) -> ToolResult:
        try:
            percent = max(0, min(100, percent))
            os_name = platform.system()
            if os_name == "Windows":
                r = subprocess.run(
                    ["powershell", "-Command",
                     f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{percent})"],
                    capture_output=True, text=True,
                )
            elif os_name == "Darwin":
                r = subprocess.run(["osascript", "-e", f"tell application \"System Events\" to set brightness to {percent/100}"],
                                   capture_output=True, text=True)
            else:
                r = subprocess.run(["xrandr", "--output", "eDP-1", "--brightness", str(percent / 100)],
                                   capture_output=True, text=True)
            return ToolResult(True, f"✓ Brightness set to {percent}%")
        except Exception as e:
            return ToolResult(False, f"✗ set_screen_brightness failed: {e}")

    @staticmethod
    def list_usb_devices() -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                r = subprocess.run(
                    ["powershell", "-Command",
                     "Get-PnpDevice -Class USB | Select-Object FriendlyName, Status | ConvertTo-Json"],
                    capture_output=True, text=True,
                )
                import json
                try:
                    data = json.loads(r.stdout)
                    return ToolResult(True, f"✓ {len(data) if isinstance(data,list) else 1} USB device(s)", data)
                except Exception:
                    return ToolResult(True, "✓ USB devices listed", r.stdout.splitlines())
            elif os_name == "Darwin":
                r = subprocess.run(["system_profiler", "SPUSBDataType"], capture_output=True, text=True)
            else:
                r = subprocess.run(["lsusb"], capture_output=True, text=True)
            return ToolResult(True, "✓ USB devices listed", r.stdout.splitlines())
        except Exception as e:
            return ToolResult(False, f"✗ list_usb_devices failed: {e}")

    @staticmethod
    def eject_drive(drive_path: str) -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                r = subprocess.run(
                    ["powershell", "-Command",
                     f"$vol = [System.IO.DriveInfo]'{drive_path}'; $shell = New-Object -ComObject Shell.Application; $shell.Namespace(17).ParseName('{drive_path}').InvokeVerb('Eject')"],
                    capture_output=True, text=True,
                )
            elif os_name == "Darwin":
                r = subprocess.run(["diskutil", "eject", drive_path], capture_output=True, text=True)
            else:
                r = subprocess.run(["eject", drive_path], capture_output=True, text=True)
            return ToolResult(True, f"✓ Drive ejected: {drive_path}")
        except Exception as e:
            return ToolResult(False, f"✗ eject_drive failed: {e}")

    @staticmethod
    def format_drive(drive_path: str, filesystem: str = "ext4", label: str = "") -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                label_arg = f"label={label}" if label else ""
                r = subprocess.run(
                    ["format", drive_path, f"/FS:{filesystem}", "/Q", "/Y"] +
                    ([f"/V:{label}"] if label else []),
                    capture_output=True, text=True, input="Y\n",
                )
            elif os_name == "Darwin":
                fs_map = {"ext4": "JHFS+", "fat32": "FAT32", "exfat": "ExFAT", "ntfs": "NTFS"}
                fs = fs_map.get(filesystem.lower(), "JHFS+")
                cmd = ["diskutil", "eraseDisk", fs, label or "DISK", drive_path]
                r = subprocess.run(cmd, capture_output=True, text=True)
            else:
                cmd = [f"mkfs.{filesystem}", drive_path] + (["-L", label] if label else [])
                r = subprocess.run(cmd, capture_output=True, text=True)
            return ToolResult(r.returncode == 0, r.stdout + r.stderr)
        except Exception as e:
            return ToolResult(False, f"✗ format_drive failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. NetworkAdvancedTool
# ─────────────────────────────────────────────────────────────────────────────

class NetworkAdvancedTool:
    name = "network_advanced"
    description = (
        "Network diagnostics and management: ping, traceroute, port scan, DNS, WHOIS, "
        "SSL, HTTP test, bandwidth, ARP, routing, uptime monitoring, SSH tunnels."
    )
    use = ("""
Name of Tool:- NetworkAdvancedTool

Purpose of Tool:- 
The NetworkAdvancedTool provides an advanced interface for executing core network diagnostics, probing host reachability, 
monitoring web health, mapping routing layouts, and handling secure encrypted communication forwarding mechanisms. It standardizes cross-platform 
diagnostics (ICMP ping, multi-hop packet routing paths) and low-level socket integrations (TCP port sweeps, specific port validation checks). 
Additionally, the tool automates public/private address reporting, DNS query tracking, reverse zone maps, deep domain WHOIS ownership indexes, 
SSL/TLS validation timelines, precise HTTP payload validations, live bandwidth throttling calculations, link-layer ARP caches, IP routing rulesets, 
and background multi-threaded uptime monitors alongside Paramiko-driven SSH tunneling channels.

Methods:-
- ping: Verifies physical remote host connectivity over low-overhead system ICMP requests.
- traceroute: Captures network path configurations by stepping through individual multi-hop gateways separating intermediate hardware channels.
- port_scan: Scans selected port lists to find exposed endpoints running on a target host.
- check_port_open: Fast-probes an explicit single transport address using native non-blocking TCP handshake sequences.
- dns_lookup: Interfaces with standard resolution tools to pull specific network record indicators mapping domain targets.
- reverse_dns: Back-resolves a numeric remote IP address layout into its registered textual pointer address name.
- whois_lookup: Extracts comprehensive registration metadata detailing domain records, hosting parameters, and administrative entities.
- get_local_ip: Checks the active interface routing configuration to identify the host machine's primary internal IP.
- get_public_ip: Queries an external secure API gateway to retrieve the machine's external-facing WAN IP address.
- get_network_interfaces: Enumerates system interfaces while indexing structural throughput indicators, operational states, and layer address pools.
- check_ssl_certificate: Handshakes with secure endpoints to inspect the root validity parameters of active x509 encryption keys.
- get_ssl_expiry: Computes standard certificate expiration parameters to safely predict remaining validation times.
- http_test: Dispatches customizable web request frames to measure performance timings and return payloads.
- bandwidth_test: Performs streaming operations over high-throughput content endpoints to calculate link speeds.
- capture_packets: Leverages Scapy mechanisms to monitor network interfaces and compile explicit raw payload capture records (.pcap).
- get_arp_table: Extracts network neighbor mappings linking Layer 2 physical hardware paths with active Layer 3 address structures.
- get_routing_table: Details current systemic destination routing rules and core interface gateways.
- set_dns_servers: Modifies primary static resolver endpoints within system scripts or configuration utilities.
- check_domain_health: Synthesizes multi-vector testing paths across DNS, HTTP status configurations, and encryption states to evaluate system availability.
- monitor_uptime: Spawns persistent analytical tracking threads designed to monitor target availability profiles using interval-bound probes.
- create_ssh_tunnel: Builds secure multi-threaded local-to-remote local port forwarding circuits across automated SSH pipelines.

How to use Tool Methods:-

1. ping:
   - Purpose: Measures the reachability and round-trip performance metrics of a specified remote node using ICMP echo chains.
   - Arguments:
     a) host: str - Target domain address or numeric IP sequence under verification.
     b) count: int (default: 4) - Number of sequential packet echo iterations dispatched during tests.
     c) timeout: int (default: 5) - Maximum lifespan parameters allocated to individual request drops.
   - Returns: ToolResult holding structural boolean connectivity status flags and a detailed execution block.
   - How to call: NetworkAdvancedTool.ping(host="8.8.8.8", count=4)

2. traceroute:
   - Purpose: Maps the explicit intermediate pathway taken by packets traveling across network routers to reach a destination.
   - Arguments:
     a) host: str - Destination destination routing endpoint node to investigate.
     b) max_hops: int (default: 30) - Safe terminal boundary checking ceiling limiting the path traversal loops.
     c) timeout: int (default: 5) - System response timeout threshold parameters.
   - Returns: ToolResult tracking routing path validation blocks and sequential hop-by-hop node matrices.
   - How to call: NetworkAdvancedTool.traceroute(host="example.com")

3. port_scan:
   - Purpose: Evaluates target system vulnerabilities or active services by attempting TCP connection routines across list vectors.
   - Arguments:
     a) host: str - System address targeted for service detection routines.
     b) ports: list (default: None) - Array of destination port digits to check. Falls back to scanning ports 1 to 1024 if unassigned.
     c) timeout: float (default: 1.0) - Handshake processing limit constraint applied per connection attempt.
     d) method: str (default: "connect") - Explicit operational state handling mechanism selection parameter.
   - Returns: ToolResult displaying scan status summaries alongside map dictionaries matching exposed ports with known protocols.
   - How to call: NetworkAdvancedTool.port_scan(host="192.168.1.1", ports=[22, 80, 443])

4. check_port_open:
   - Purpose: Performs a fast connection handshake check against a specific target port to see if it is actively accepting connections.
   - Arguments:
     a) host: str - The host network node under configuration audit.
     b) port: int - Exact port number targeted for connection verification.
     c) timeout: float (default: 3.0) - Time budget limits applied to socket connection states.
   - Returns: ToolResult storing open/closed validation states.
   - How to call: NetworkAdvancedTool.check_port_open(host="127.0.0.1", port=3306)

5. dns_lookup:
   - Purpose: Interrogates domain databases via system sub-layer structures to fetch requested zone records.
   - Arguments:
     a) domain: str - Textual destination identifier to look up.
     b) record_type: str (default: "A") - Explicit lookup target filter (e.g., "A", "AAAA", "MX", "TXT", "CNAME").
   - Returns: ToolResult containing processing flags alongside raw nslookup output records.
   - How to call: NetworkAdvancedTool.dns_lookup(domain="google.com", record_type="MX")

6. reverse_dns:
   - Purpose: Resolves an IP address back to its associated hostname via Pointer (PTR) record extraction routines.
   - Arguments:
     a) ip: str - Target IP routing location sequence under examination.
   - Returns: ToolResult tracking mapping updates and resolved text markers.
   - How to call: NetworkAdvancedTool.reverse_dns(ip="8.8.8.8")

7. whois_lookup:
   - Purpose: Queries domain WHOIS registries to extract structural assignment details, creation dates, and organization metadata.
   - Arguments:
     a) domain: str - Core domain name targeted for registry examination.
   - Returns: ToolResult packing validation flags alongside a dictionary filled with domain registration information.
   - How to call: NetworkAdvancedTool.whois_lookup(domain="github.com")

8. get_local_ip:
   - Purpose: Safely computes the machine's primary internal LAN routing address by opening an inactive socket channel toward external addresses.
   - Arguments: None.
   - Returns: ToolResult formatting operational flags and local network IP fields.
   - How to call: NetworkAdvancedTool.get_local_ip()

9. get_public_ip:
   - Purpose: Identifies the local environment's external WAN IP address as seen by the public internet.
   - Arguments: None.
   - Returns: ToolResult logging connectivity status along with external network IP metrics.
   - How to call: NetworkAdvancedTool.get_public_ip()

10. get_network_interfaces:
    - Purpose: Aggregates hardware interface lists to verify configuration statuses, packet speeds, and assigned address pools.
    - Arguments: None.
    - Returns: ToolResult mapping active adapter setups alongside structural network properties.
    - How to call: NetworkAdvancedTool.get_network_interfaces()

11. check_ssl_certificate:
    - Purpose: Validates peer certificate authentication layers during connection tests to detect potential trust failures.
    - Arguments:
      a) domain: str - Destination secure endpoint web address.
      b) port: int (default: 443) - Target security socket link identifier.
    - Returns: ToolResult describing certificate validation results and properties.
    - How to call: NetworkAdvancedTool.check_ssl_certificate(domain="cloudflare.com")

12. get_ssl_expiry:
    - Purpose: Analyzes x509 validation fields to compute the exact number of days remaining before an SSL/TLS certificate expires.
    - Arguments:
      a) domain: str - Web host target path intended for evaluation.
      b) port: int (default: 443) - The specific port number used to initiate the secure handshake.
    - Returns: ToolResult holding tracking metrics and expiration timelines.
    - How to call: NetworkAdvancedTool.get_ssl_expiry(domain="microsoft.com")

13. http_test:
    - Purpose: Dispatches custom HTTP request configurations to audit server endpoint availability, response headers, and performance latency.
    - Arguments:
      a) url: str - Absolute destination link schema targeted for verification.
      b) method: str (default: "GET") - HTTP transmission verb identifier (e.g., "GET", "POST", "PUT", "DELETE").
      c) headers: dict (default: None) - Key-value pair configurations mapping custom HTTP request headers.
      d) data: dict (default: None) - JSON-formatted payload structures appended to the request body.
      e) timeout: int (default: 15) - Maximum duration bounds allocated to response streaming windows.
      f) follow_redirects: bool (default: True) - Determines whether the client follows HTTP redirect chains.
      g) verify_ssl: bool (default: True) - Enables or disables enforcement of strict peer security checks.
    - Returns: ToolResult packing status codes, header configurations, and timing details.
    - How to call: NetworkAdvancedTool.http_test(url="https://httpbin.org/post", method="POST", data={"test": True})

14. bandwidth_test:
    - Purpose: Estimates connection performance limits by continuously downloading chunked streams over a fixed timeframe.
    - Arguments:
      a) server_url: str (default: high-capacity byte node) - Secure endpoint link supplying download test streams.
      b) duration: int (default: 5) - Target time duration bounds limiting speed tracking metrics loops.
    - Returns: ToolResult declaring evaluation metrics and average connection speeds in Mbps.
    - How to call: NetworkAdvancedTool.bandwidth_test(duration=3)

15. capture_packets:
    - Purpose: Sniffs low-level hardware or virtual interface frames, filtering capture data into formatted analysis records.
    - Arguments:
      a) interface: str (default: "eth0") - Specific interface adapter channel target assigned for packet capture.
      b) count: int (default: 10) - Target ceiling limiting packet counts captured during testing runs.
      c) filter: str (default: "") - Standard BPF packet filtering syntax queries (e.g., "tcp port 80").
      d) output_pcap: str (default: "capture.pcap") - Path location where captured file traces are saved.
    - Returns: ToolResult tracking saved output confirmation markers.
    - How to call: NetworkAdvancedTool.capture_packets(interface="wlan0", count=5, filter="icmp")

16. get_arp_table:
    - Purpose: Dumps the system Address Resolution Protocol table to check current IP-to-MAC address mappings.
    - Arguments: None.
    - Returns: ToolResult collecting network configuration arrays detailing known hardware address targets.
    - How to call: NetworkAdvancedTool.get_arp_table()

17. get_routing_table:
    - Purpose: Exposes internal packet path selections by extracting the operating system's active IP routing matrices.
    - Arguments: None.
    - Returns: ToolResult logging execution success metrics and raw system routing tracks.
    - How to call: NetworkAdvancedTool.get_routing_table()

18. set_dns_servers:
    - Purpose: Overwrites system resolver targets to re-route domain lookups through specific external name servers.
    - Arguments:
      a) servers: list - Array sequence mapping string formatting destination server IP records (e.g., ["8.8.8.8", "1.1.1.1"]).
      b) interface: str (default: "") - Targeted link adapter descriptor targeted for structural configuration.
    - Returns: ToolResult providing validation updates.
    - How to call: NetworkAdvancedTool.set_dns_servers(servers=["1.1.1.1", "1.0.0.1"])

19. check_domain_health:
    - Purpose: Aggregates multiple network testing utilities to build a unified profile evaluating domain availability and security posture.
    - Arguments:
      a) domain: str - Target name string intended for architectural health checks.
    - Returns: ToolResult packaging validation flags and sub-layer service evaluation parameters.
    - How to call: NetworkAdvancedTool.check_domain_health(domain="apple.com")

20. monitor_uptime:
    - Purpose: Spawns independent background monitoring tasks that check web server availability and trigger alerts if failure rates exceed thresholds.
    - Arguments:
      a) url: str - Destination link under analytical surveillance.
      b) interval: int (default: 60) - Testing delay cycles measured in seconds separating individual check sweeps.
      c) alert_threshold: int (default: 3) - Maximum allowable consecutive drops before triggering alert routines.
      d) callback: function (default: None) - Custom execution reference called when failure conditions are reached.
    - Returns: ToolResult validating successful initiation of the tracking background loop.
    - How to call: NetworkAdvancedTool.monitor_uptime(url="https://mywebsite.com", interval=30)

21. create_ssh_tunnel:
    - Purpose: Leverages paramiko SSH channels to forward local traffic securely across encrypted pipelines toward remote targets.
    - Arguments:
      a) local_port: int - Local connection target port listening for traffic on the host machine.
      b) remote_host: str - Final internal network destination address situated beyond the jump box.
      c) remote_port: int - Final system network application target port under configuration.
      d) ssh_host: str - Gateway intermediary server hosting active shell connections.
      e) ssh_user: str - Identity label used for secure shell server authentication.
      f) ssh_key: str (default: None) - Storage target file path referencing the user's private authentication key.
      g) cred_key: str (default: "ssh") - Index key mapping default verification metrics out of storage systems.
    - Returns: ToolResult mapping active circuit connection confirmations.
    - How to call: NetworkAdvancedTool.create_ssh_tunnel(local_port=8080, remote_host="10.0.0.5", remote_port=80, ssh_host="jump.mycompany.com", ssh_user="admin")
""")

    @staticmethod
    def ping(host: str, count: int = 4, timeout: int = 5) -> ToolResult:
        try:
            os_name = platform.system()
            flag    = "-n" if os_name == "Windows" else "-c"
            r = subprocess.run(["ping", flag, str(count), host], capture_output=True, text=True, timeout=timeout * count + 5)
            success = r.returncode == 0
            return ToolResult(success, r.stdout + r.stderr, {"reachable": success, "output": r.stdout})
        except Exception as e:
            return ToolResult(False, f"✗ ping failed: {e}")

    @staticmethod
    def traceroute(host: str, max_hops: int = 30, timeout: int = 5) -> ToolResult:
        try:
            cmd = ["tracert", host] if platform.system() == "Windows" else ["traceroute", "-m", str(max_hops), host]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return ToolResult(True, "✓ Traceroute complete", r.stdout.splitlines())
        except Exception as e:
            return ToolResult(False, f"✗ traceroute failed: {e}")

    @staticmethod
    def port_scan(
        host: str,
        ports: list = None,
        timeout: float = 1.0,
        method: str = "connect",
    ) -> ToolResult:
        try:
            import socket

            ports = ports or list(range(1, 1025))
            open_ports = []
            for port in ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(timeout)
                        result = s.connect_ex((host, port))
                        if result == 0:
                            try:
                                service = socket.getservbyport(port)
                            except Exception:
                                service = "unknown"
                            open_ports.append({"port": port, "service": service})
                except Exception:
                    pass
            return ToolResult(True, f"✓ {len(open_ports)} open port(s) on {host}", open_ports)
        except Exception as e:
            return ToolResult(False, f"✗ port_scan failed: {e}")

    @staticmethod
    def check_port_open(host: str, port: int, timeout: float = 3.0) -> ToolResult:
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((host, port))
            open_ = result == 0
            return ToolResult(open_, f"✓ Port {port} is {'open' if open_ else 'closed'} on {host}", {"open": open_})
        except Exception as e:
            return ToolResult(False, f"✗ check_port_open failed: {e}")

    @staticmethod
    def dns_lookup(domain: str, record_type: str = "A") -> ToolResult:
        try:
            r = subprocess.run(
                ["nslookup", "-type=" + record_type, domain],
                capture_output=True, text=True, timeout=15,
            )
            return ToolResult(True, f"✓ DNS lookup: {domain} ({record_type})", r.stdout.splitlines())
        except Exception as e:
            return ToolResult(False, f"✗ dns_lookup failed: {e}")

    @staticmethod
    def reverse_dns(ip: str) -> ToolResult:
        try:
            import socket
            hostname = socket.gethostbyaddr(ip)[0]
            return ToolResult(True, f"✓ Reverse DNS: {ip} → {hostname}", {"hostname": hostname})
        except Exception as e:
            return ToolResult(False, f"✗ reverse_dns failed: {e}")

    @staticmethod
    def whois_lookup(domain: str) -> ToolResult:
        try:
            import whois
            w = whois.whois(domain)
            return ToolResult(True, f"✓ WHOIS for {domain}", dict(w))
        except Exception as e:
            return ToolResult(False, f"✗ whois_lookup failed: {e}")

    @staticmethod
    def get_local_ip() -> ToolResult:
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ToolResult(True, f"✓ Local IP: {ip}", {"local_ip": ip})
        except Exception as e:
            return ToolResult(False, f"✗ get_local_ip failed: {e}")

    @staticmethod
    def get_public_ip() -> ToolResult:
        try:
            import requests
            ip = requests.get("https://api.ipify.org", timeout=10).text.strip()
            return ToolResult(True, f"✓ Public IP: {ip}", {"public_ip": ip})
        except Exception as e:
            return ToolResult(False, f"✗ get_public_ip failed: {e}")

    @staticmethod
    def get_network_interfaces() -> ToolResult:
        try:
            import psutil
            interfaces = {}
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            for name, addr_list in addrs.items():
                interfaces[name] = {
                    "addresses": [a._asdict() for a in addr_list],
                    "is_up":     stats[name].isup if name in stats else False,
                    "speed":     stats[name].speed if name in stats else 0,
                }
            return ToolResult(True, f"✓ {len(interfaces)} network interface(s)", interfaces)
        except Exception as e:
            return ToolResult(False, f"✗ get_network_interfaces failed: {e}")

    @staticmethod
    def check_ssl_certificate(domain: str, port: int = 443) -> ToolResult:
        try:
            import ssl, socket
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(10)
                s.connect((domain, port))
                cert = s.getpeercert()
            return ToolResult(True, f"✓ SSL certificate valid for {domain}", cert)
        except ssl.SSLCertVerificationError as e:
            return ToolResult(False, f"✗ SSL verification failed: {e}")
        except Exception as e:
            return ToolResult(False, f"✗ check_ssl_certificate failed: {e}")

    @staticmethod
    def get_ssl_expiry(domain: str, port: int = 443) -> ToolResult:
        try:
            import ssl, socket
            from datetime import datetime

            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(10)
                s.connect((domain, port))
                cert = s.getpeercert()
            expiry_str = cert["notAfter"]
            expiry     = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
            days_left  = (expiry - datetime.utcnow()).days
            return ToolResult(True, f"✓ SSL expires in {days_left} days ({expiry_str})", {"expiry": expiry_str, "days_left": days_left})
        except Exception as e:
            return ToolResult(False, f"✗ get_ssl_expiry failed: {e}")

    @staticmethod
    def http_test(
        url: str,
        method: str = "GET",
        headers: dict = None,
        data: dict = None,
        timeout: int = 15,
        follow_redirects: bool = True,
        verify_ssl: bool = True,
    ) -> ToolResult:
        try:
            import requests
            fn = getattr(requests, method.lower())
            r  = fn(url, headers=headers or {}, json=data, timeout=timeout,
                    allow_redirects=follow_redirects, verify=verify_ssl)
            return ToolResult(
                r.status_code < 400,
                f"✓ {method} {url} → {r.status_code} ({r.elapsed.total_seconds():.3f}s)",
                {
                    "status_code":  r.status_code,
                    "headers":      dict(r.headers),
                    "elapsed_ms":   round(r.elapsed.total_seconds() * 1000, 1),
                    "content_type": r.headers.get("Content-Type", ""),
                    "body_preview": r.text[:500],
                },
            )
        except Exception as e:
            return ToolResult(False, f"✗ http_test failed: {e}")

    @staticmethod
    def bandwidth_test(server_url: str = "https://httpbin.org/bytes/1048576", duration: int = 5) -> ToolResult:
        try:
            import requests, time

            download_bytes = 0
            start = time.time()
            while time.time() - start < duration:
                r = requests.get(server_url, timeout=10, stream=True)
                for chunk in r.iter_content(65536):
                    download_bytes += len(chunk)
                    if time.time() - start >= duration:
                        break
            elapsed = time.time() - start
            speed_mbps = round((download_bytes * 8) / (elapsed * 1e6), 2)
            return ToolResult(True, f"✓ Download speed: ~{speed_mbps} Mbps", {"speed_mbps": speed_mbps, "bytes": download_bytes})
        except Exception as e:
            return ToolResult(False, f"✗ bandwidth_test failed: {e}")

    @staticmethod
    def capture_packets(
        interface: str = "eth0",
        count: int = 10,
        filter: str = "",
        output_pcap: str = "capture.pcap",
    ) -> ToolResult:
        try:
            from scapy.all import sniff, wrpcap
            packets = sniff(iface=interface, count=count, filter=filter, timeout=30)
            wrpcap(output_pcap, packets)
            return ToolResult(True, f"✓ Captured {len(packets)} packets → {output_pcap}", {"count": len(packets)})
        except Exception as e:
            return ToolResult(False, f"✗ capture_packets failed: {e}")

    @staticmethod
    def get_arp_table() -> ToolResult:
        try:
            if platform.system() == "Windows":
                r = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            else:
                r = subprocess.run(["arp", "-n"], capture_output=True, text=True)
            return ToolResult(True, "✓ ARP table fetched", r.stdout.splitlines())
        except Exception as e:
            return ToolResult(False, f"✗ get_arp_table failed: {e}")

    @staticmethod
    def get_routing_table() -> ToolResult:
        try:
            if platform.system() == "Windows":
                r = subprocess.run(["route", "print"], capture_output=True, text=True)
            else:
                r = subprocess.run(["netstat", "-rn"], capture_output=True, text=True)
            return ToolResult(True, "✓ Routing table fetched", r.stdout.splitlines())
        except Exception as e:
            return ToolResult(False, f"✗ get_routing_table failed: {e}")

    @staticmethod
    def set_dns_servers(servers: list, interface: str = "") -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                iface = interface or "Ethernet"
                for i, server in enumerate(servers):
                    index = "primary" if i == 0 else "secondary"
                    subprocess.run(
                        ["netsh", "interface", "ipv4", "set", "dns",
                         f"name={iface}", "static" if i == 0 else "add", server],
                        capture_output=True,
                    )
            elif os_name == "Darwin":
                for server in servers:
                    subprocess.run(
                        ["networksetup", "-setdnsservers", interface or "Wi-Fi", server],
                        capture_output=True,
                    )
            else:
                from pathlib import Path
                content = "\n".join(f"nameserver {s}" for s in servers) + "\n"
                Path("/etc/resolv.conf").write_text(content)
            return ToolResult(True, f"✓ DNS servers set: {', '.join(servers)}")
        except Exception as e:
            return ToolResult(False, f"✗ set_dns_servers failed: {e}")

    @staticmethod
    def check_domain_health(domain: str) -> ToolResult:
        try:
            import requests, ssl, socket

            results: dict = {}
            # HTTP reachability
            try:
                r = requests.get(f"https://{domain}", timeout=10, verify=True)
                results["http_status"]   = r.status_code
                results["https_reachable"] = True
            except Exception as ex:
                results["https_reachable"] = False
                results["http_error"]      = str(ex)
            # SSL
            try:
                from datetime import datetime
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                    s.settimeout(5); s.connect((domain, 443))
                    cert = s.getpeercert()
                expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                results["ssl_valid"]    = True
                results["ssl_days_left"] = (expiry - datetime.utcnow()).days
            except Exception as ex:
                results["ssl_valid"] = False; results["ssl_error"] = str(ex)
            # DNS
            try:
                socket.gethostbyname(domain)
                results["dns_resolves"] = True
            except Exception:
                results["dns_resolves"] = False
            return ToolResult(True, f"✓ Domain health check for {domain}", results)
        except Exception as e:
            return ToolResult(False, f"✗ check_domain_health failed: {e}")

    @staticmethod
    def monitor_uptime(
        url: str,
        interval: int = 60,
        alert_threshold: int = 3,
        callback=None,
    ) -> ToolResult:
        try:
            import threading, requests, time

            failures = [0]

            def _watch():
                while True:
                    try:
                        r = requests.get(url, timeout=10)
                        if r.status_code >= 400:
                            failures[0] += 1
                        else:
                            failures[0] = 0
                    except Exception:
                        failures[0] += 1
                    if failures[0] >= alert_threshold and callback:
                        callback({"url": url, "failures": failures[0]})
                    time.sleep(interval)

            threading.Thread(target=_watch, daemon=True).start()
            return ToolResult(True, f"✓ Monitoring uptime for {url} every {interval}s")
        except Exception as e:
            return ToolResult(False, f"✗ monitor_uptime failed: {e}")

    @staticmethod
    def create_ssh_tunnel(
        local_port: int,
        remote_host: str,
        remote_port: int,
        ssh_host: str,
        ssh_user: str,
        ssh_key: str = None,
        cred_key: str = "ssh",
    ) -> ToolResult:
        try:
            import threading
            import paramiko

            creds   = CredStore.load(cred_key)
            key_path = ssh_key or creds.get("key_path", None)
            password = creds.get("password", None)

            transport = paramiko.Transport((ssh_host, 22))
            if key_path:
                pkey = paramiko.RSAKey.from_private_key_file(key_path)
                transport.connect(username=ssh_user, pkey=pkey)
            else:
                transport.connect(username=ssh_user, password=password)

            import socket

            def _accept():
                server = socket.socket()
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(("127.0.0.1", local_port))
                server.listen(5)
                while True:
                    client, _ = server.accept()
                    chan = transport.open_channel("direct-tcpip",
                                                  (remote_host, remote_port),
                                                  ("127.0.0.1", local_port))
                    def bridge(src, dst):
                        while True:
                            data = src.recv(1024)
                            if not data: break
                            dst.sendall(data)
                    threading.Thread(target=bridge, args=(client, chan), daemon=True).start()
                    threading.Thread(target=bridge, args=(chan, client), daemon=True).start()

            threading.Thread(target=_accept, daemon=True).start()
            return ToolResult(True, f"✓ SSH tunnel: localhost:{local_port} → {remote_host}:{remote_port} via {ssh_host}")
        except Exception as e:
            return ToolResult(False, f"✗ create_ssh_tunnel failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. FileSystemAdvancedTool
# ─────────────────────────────────────────────────────────────────────────────

class FileSystemAdvancedTool:
    name = "filesystem_advanced"
    description = (
        "Advanced file operations: folder watch/sync, duplicate detection/removal, "
        "encryption, secure delete, split/join, compression, malware scan, permissions."
    )
    use = ("""
Name of Tool:- FileSystemAdvancedTool

Purpose of Tool:- 
The FileSystemAdvancedTool provides an advanced and secure interface for complex filesystem management, structural audits, data sanitation, 
and integrity enforcement. It wraps system-level and library-driven operations into a clean API covering directory event monitoring, automated 
one-way or bidirectional directory synchronization, cryptographically sound deduplication via hashes, authenticated encryption primitives (AES-GCM), 
unrecoverable file shredding, chunked file splitting/joining, custom malware pattern filtering, recursive Unix access control modification (chmod/chown), 
virtual SFTP volume mounting, and massive manifest creation using verifiable checksum fingerprints.

Methods:-
- watch_folder: Sets up a background monitoring event loop to capture structural modifications under specified directory trees.
- sync_folders: Performs multi-tier file replication or bidirectional path mirrors across distinct system directory paths.
- find_duplicates: Sweeps selected directory locations to spot and pool redundant data objects based on hash uniqueness keys.
- remove_duplicates: Automatically purges duplicate files found inside target structures based on relative indexing order selections.
- encrypt_file: Derives high-entropy security keys via Scrypt to secure target payloads with robust AES-GCM envelope protections.
- decrypt_file: Extracts salt and nonce parameters from encrypted blobs to fully reconstruct original unencrypted plaintext contents.
- secure_delete: Obliterates local file records by executing continuous cryptographically random byte overwrite runs before block unlinking.
- split_file: Slices large targeted objects into sequentially numbered byte fragments for easy transport.
- join_files: Combines split part components back into a single operational structural data assembly.
- compress_folder: Archives complex structured folder nodes into portable, custom-leveled compressed archives like .zip or .tar.gz format packages.
- scan_for_malware: Runs quick regex matches across local file contents to uncover suspicious strings, shell scripts, or unsafe system commands.
- find_large_files: Filters file elements by file size boundaries to create sorted breakdowns of massive space-consuming files.
- change_permissions_recursive: Performs recursive bitwise access control mode alterations across targeted folder structures.
- change_owner_recursive: Modifies systemic ownership boundaries by calling platform processes recursively on targeted assets.
- mount_remote_folder: Validates structural connectivity and directory availability metrics against external SFTP nodes over Paramiko transport links.
- verify_checksum: Recomputes absolute hex digests on files to confirm payload alignment with expected hash profiles.
- generate_checksum_file: Dispatches validation routines down directory paths to generate comprehensive signature catalogs for mass file verification.

How to use Tool Methods:-

1. watch_folder:
   - Purpose: Tracks real-time folder mutations (creations, deletions, updates) by spawning a background Watchdog monitoring worker thread.
   - Arguments:
     a) path: str - Base folder target path under monitoring surveillance.
     b) callback: function - Callable execution target triggered upon catching systemic filesystem event types.
     c) patterns: list (default: None) - Filter matching formats used to flag specific file extensions.
     d) recursive: bool (default: True) - Controls whether the engine monitors all nested subdirectories.
     e) ignore_patterns: list (default: None) - File format patterns excluded from monitoring sweeps.
   - Returns: ToolResult holding background observer validation confirmations.
   - How to call: FileSystemAdvancedTool.watch_folder(path="/var/www", callback=print, patterns=["*.py"])

2. sync_folders:
   - Purpose: Replicates data assets between directory nodes with handling options for extra files, mirrors, and dry runs.
   - Arguments:
     a) source: str - Root source folder address feeding file states.
     b) destination: str - Destination tracking workspace targeted for alignment.
     c) bidirectional: bool (default: False) - Enables concurrent reverse updates back into the source path.
     d) delete_extra: bool (default: False) - Purges elements within the destination folder that do not exist at the source.
     e) dry_run: bool (default: False) - Simulates operations to log target changes without writing any changes to disk.
   - Returns: ToolResult packing final synced transaction statistics.
   - How to call: FileSystemAdvancedTool.sync_folders(source="./src", destination="./backup", delete_extra=True)

3. find_duplicates:
   - Purpose: Builds unique hash maps across files to precisely group and expose completely identical data blobs.
   - Arguments:
     a) paths: list - Target search folder addresses to look through.
     b) method: str (default: "md5") - Selection parameter specifying the crypto hashing routine (e.g., "md5", "sha256").
     c) output: str (default: None) - Optional target output path to dump the duplicate mappings as a JSON file.
   - Returns: ToolResult detailing duplicate group counts alongside data matrices matching hashes to file path locations.
   - How to call: FileSystemAdvancedTool.find_duplicates(paths=["/data/docs"], method="sha256")

4. remove_duplicates:
   - Purpose: Cleans up storage locations by safely deleting identical files uncovered during folder sweeps.
   - Arguments:
     a) paths: list - Target target system paths targeted for duplicate removal loops.
     b) keep: str (default: "first") - Selects which unique variant index to preserve ("first" or "last").
     c) method: str (default: "md5") - Crypto algorithm choice used to confirm identity match states.
   - Returns: ToolResult summarizing total file units removed from disk.
   - How to call: FileSystemAdvancedTool.remove_duplicates(paths=["/home/user/downloads"], keep="first")

5. encrypt_file:
   - Purpose: Uses strong Scrypt key derivation and AES-GCM authenticated encryption to convert raw files into protected data blobs.
   - Arguments:
     a) input: str - Plaintext file source target slated for protection.
     b) output: str - Destination tracking path where the encrypted file will be saved.
     c) password: str - Base passphrase text string feeding the key derivation functions.
     b) algorithm: str (default: "AES") - Underlying security symmetric encryption type framework.
   - Returns: ToolResult tracking successfully processed secure output states.
   - How to call: FileSystemAdvancedTool.encrypt_file(input="secret.txt", output="secret.enc", password="SuperSecurePassword123")

6. decrypt_file:
   - Purpose: Validates envelope headers and decrypts AES-GCM data payloads back into true plaintext.
   - Arguments:
     a) input: str - Target path pointing to the valid encrypted file source.
     b) output: str - Target system destination path where decrypted contents will be written.
     c) password: str - Passphrase matching the exact key derivation settings used to encrypt the file.
   - Returns: ToolResult indicating confirmation of safe payload decryption.
   - How to call: FileSystemAdvancedTool.decrypt_file(input="secret.enc", output="restored.txt", password="SuperSecurePassword123")

7. secure_delete:
   - Purpose: Shreds data sectors using continuous random byte write buffers to stop file recovery before unlinking records from the OS.
   - Arguments:
     a) path: str - Target target file item marked for permanent secure destruction.
     b) passes: int (default: 3) - The number of random byte overwrite cycles applied across target blocks.
   - Returns: ToolResult charting deletion confirmations.
   - How to call: FileSystemAdvancedTool.secure_delete(path="sensitive_data.csv", passes=5)

8. split_file:
   - Purpose: Slices large structural objects into smaller byte chunks to fit transport size limits.
   - Arguments:
     a) path: str - Main file asset scheduled for division.
     b) chunk_size: int (default: 10485760) - Target byte volume parameter limiting maximum individual chunk splits (defaults to 10 MB).
     c) output_folder: str (default: None) - Output path destination designated to store the generated partial split fragments.
   - Returns: ToolResult detailing piece metrics and tracking output destinations.
   - How to call: FileSystemAdvancedTool.split_file(path="archive.tar", chunk_size=5242880)

9. join_files:
   - Purpose: Assembles sequenced partial files back into a single unified binary file structure.
   - Arguments:
     a) parts_folder: str - Source folder containing the split data chunks.
     b) output: str - Reconstructed path location mapping where the combined file will be saved.
     c) extension: str (default: ".part") - Tracking suffix selector used to identify and sort split parts.
   - Returns: ToolResult providing reconstruction progress statuses.
   - How to call: FileSystemAdvancedTool.join_files(parts_folder="./archive_parts", output="restored_archive.tar")

10. compress_folder:
    - Purpose: Bundles entire nested folder tree structures into space-saving compressed archives using custom algorithms.
    - Arguments:
      a) path: str - Target folder directory root slated for archiving.
      b) output: str (default: None) - Desired output archive path name (autocompletes file extensions if blank).
      c) algorithm: str (default: "zip") - Compression scheme selector flag (options include "zip" or "tar.gz").
      d) level: int (default: 6) - Numeric scale balancing compression time against final output file size (scale from 1 to 9).
    - Returns: ToolResult logging the saved output location of the archive.
    - How to call: FileSystemAdvancedTool.compress_folder(path="./projects", algorithm="tar.gz", level=9)

11. scan_for_malware:
    - Purpose: Checks file bodies against high-risk regex string signatures to spot potential web shells, injection paths, or backdoors.
    - Arguments:
      a) path: str - Target file path or root folder location selected for pattern filtering scans.
      b) patterns: list (default: None) - Optional array tracking custom suspicious evaluation strings.
    - Returns: ToolResult charting structural match positions and total high-risk flags identified.
    - How to call: FileSystemAdvancedTool.scan_for_malware(path="/var/www/html")

12. find_large_files:
    - Purpose: Crawls file systems to find and catalog space-heavy files that exceed specified size limits.
    - Arguments:
      a) path: str - Root location where the size tracking sweep begins.
      b) min_size_mb: float (default: 100) - Minimum file size ceiling filter value in Megabytes.
      c) recursive: bool (default: True) - Dictates whether the tool crawls down nested folders.
    - Returns: ToolResult packing sorted details mapping large file nodes to their respective sizes.
    - How to call: FileSystemAdvancedTool.find_large_files(path="/var/log", min_size_mb=50.0)

13. change_permissions_recursive:
    - Purpose: Changes system file access codes recursively across entire directory trees using Unix octal permissions mode formatting.
    - Arguments:
      a) path: str - Root folder location targeted for permissions changes.
      b) mode: int (default: 0o755) - Bitwise permissions mask value passed using standard octal representations.
    - Returns: ToolResult counting total items adjusted across system tracks.
    - How to call: FileSystemAdvancedTool.change_permissions_recursive(path="./scripts", mode=0o744)

14. change_owner_recursive:
    - Purpose: Changes user and group ownership boundaries recursively across target items using platform tools.
    - Arguments:
      a) path: str - System file location marked for ownership updates.
      b) user: str - Account user name mapping the new target owner.
      c) group: str (default: None) - Intended platform group name string to attach alongside user parameters.
    - Returns: ToolResult capturing operational return logs from sub-process tasks.
    - How to call: FileSystemAdvancedTool.change_owner_recursive(path="/var/www", user="www-data", group="www-data")

15. mount_remote_folder:
    - Purpose: Opens a secure transport connection to check and read from folders on remote SFTP hosts.
    - Arguments:
      a) host: str - Intermediary system hostname network target.
      b) remote_path: str - Folder layout path residing on the target remote server environment.
      c) local_path: str - Local folder path used as a placeholder target during validation tests.
      d) credentials: dict (default: None) - Custom authentication login configurations.
      e) cred_key: str (default: "ssh") - Index key mapping default verification parameters from credential databases.
    - Returns: ToolResult packing lists tracking files present inside the remote folder target.
    - How to call: FileSystemAdvancedTool.mount_remote_folder(host="sftp.partner.com", remote_path="/uploads", local_path="./remote_preview")

16. verify_checksum:
    - Purpose: Compares the computed runtime hash value of a target file directly against an expected hash string to verify file integrity.
    - Arguments:
      a) file: str - Target file path targeted for tracking calculations.
      b) expected: str - Pre-computed verification hash string used to confirm authenticity.
      c) algorithm: str (default: "sha256") - Selection parameter defining the algorithm used (e.g., "md5", "sha1", "sha256").
    - Returns: ToolResult storing verification matches along with actual string tracking markers.
    - How to call: FileSystemAdvancedTool.verify_checksum(file="ubuntu.iso", expected="a3c2...ef45")

17. generate_checksum_file:
    - Purpose: Crawls directories to map files and write their corresponding cryptographic signatures out into unified manifest index files.
    - Arguments:
      a) folder: str - Base folder directory path selected for verification checks.
      b) algorithm: str (default: "sha256") - Underlying hash algorithm scheme used to generate individual checksums.
      c) output: str (default: "checksums.txt") - Destination file tracking path where the generated manifest text will be saved.
    - Returns: ToolResult tracking output confirmations and listing total file counts cataloged.
    - How to call: FileSystemAdvancedTool.generate_checksum_file(folder="./release_pkg", algorithm="sha256")
""")

    @staticmethod
    def watch_folder(
        path: str,
        callback,
        patterns: list = None,
        recursive: bool = True,
        ignore_patterns: list = None,
    ) -> ToolResult:
        try:
            import threading
            from watchdog.observers import Observer
            from watchdog.events import PatternMatchingEventHandler

            handler = PatternMatchingEventHandler(
                patterns=patterns or ["*"],
                ignore_patterns=ignore_patterns or [],
                ignore_directories=False,
                case_sensitive=True,
            )
            handler.on_any_event = lambda event: callback(event)
            observer = Observer()
            observer.schedule(handler, path, recursive=recursive)
            observer.start()
            return ToolResult(True, f"✓ Watching folder: {path}")
        except Exception as e:
            return ToolResult(False, f"✗ watch_folder failed: {e}")

    @staticmethod
    def sync_folders(
        source: str,
        destination: str,
        bidirectional: bool = False,
        delete_extra: bool = False,
        dry_run: bool = False,
    ) -> ToolResult:
        try:
            import shutil, filecmp
            from pathlib import Path

            def _sync(src: Path, dst: Path) -> int:
                dst.mkdir(parents=True, exist_ok=True)
                count = 0
                for item in src.iterdir():
                    d = dst / item.name
                    if item.is_dir():
                        count += _sync(item, d)
                    else:
                        if not d.exists() or item.stat().st_mtime > d.stat().st_mtime:
                            if not dry_run:
                                shutil.copy2(str(item), str(d))
                            count += 1
                if delete_extra:
                    for item in dst.iterdir():
                        if not (src / item.name).exists():
                            if not dry_run:
                                if item.is_dir(): shutil.rmtree(str(item))
                                else: item.unlink()
                return count

            src_p = Path(source)
            dst_p = Path(destination)
            count = _sync(src_p, dst_p)
            if bidirectional:
                count += _sync(dst_p, src_p)
            mode = "(dry run) " if dry_run else ""
            return ToolResult(True, f"✓ {mode}Synced {count} file(s)")
        except Exception as e:
            return ToolResult(False, f"✗ sync_folders failed: {e}")

    @staticmethod
    def find_duplicates(
        paths: list, method: str = "md5", output: str = None
    ) -> ToolResult:
        try:
            import hashlib, json
            from pathlib import Path
            from collections import defaultdict

            def file_hash(filepath: str) -> str:
                h = hashlib.new(method)
                with open(filepath, "rb") as f:
                    for chunk in iter(lambda: f.read(65536), b""):
                        h.update(chunk)
                return h.hexdigest()

            hashes: dict = defaultdict(list)
            for path in paths:
                p = Path(path)
                for f in (p.rglob("*") if p.is_dir() else [p]):
                    if f.is_file():
                        try:
                            hashes[file_hash(str(f))].append(str(f))
                        except Exception:
                            pass

            duplicates = {h: files for h, files in hashes.items() if len(files) > 1}
            if output:
                Path(output).write_text(json.dumps(duplicates, indent=2))
            return ToolResult(True, f"✓ Found {len(duplicates)} duplicate group(s)", duplicates)
        except Exception as e:
            return ToolResult(False, f"✗ find_duplicates failed: {e}")

    @staticmethod
    def remove_duplicates(
        paths: list, keep: str = "first", method: str = "md5"
    ) -> ToolResult:
        try:
            result = FileSystemAdvancedTool.find_duplicates(paths, method)
            if not result.success:
                return result
            removed = 0
            for hash_val, files in (result.data or {}).items():
                to_remove = files[1:] if keep == "first" else files[:-1]
                for f in to_remove:
                    from pathlib import Path
                    Path(f).unlink()
                    removed += 1
            return ToolResult(True, f"✓ Removed {removed} duplicate file(s)")
        except Exception as e:
            return ToolResult(False, f"✗ remove_duplicates failed: {e}")

    @staticmethod
    def encrypt_file(
        input: str,
        output: str,
        password: str,
        algorithm: str = "AES",
    ) -> ToolResult:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
            from pathlib import Path
            import os

            salt = os.urandom(16)
            kdf  = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
            key  = kdf.derive(password.encode())
            nonce = os.urandom(12)
            aesgcm = AESGCM(key)
            plaintext  = Path(input).read_bytes()
            ciphertext = aesgcm.encrypt(nonce, plaintext, None)
            Path(output).write_bytes(salt + nonce + ciphertext)
            return ToolResult(True, f"✓ File encrypted: {output}")
        except Exception as e:
            return ToolResult(False, f"✗ encrypt_file failed: {e}")

    @staticmethod
    def decrypt_file(input: str, output: str, password: str) -> ToolResult:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
            from pathlib import Path

            data  = Path(input).read_bytes()
            salt  = data[:16]
            nonce = data[16:28]
            ct    = data[28:]
            kdf   = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
            key   = kdf.derive(password.encode())
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(nonce, ct, None)
            Path(output).write_bytes(plaintext)
            return ToolResult(True, f"✓ File decrypted: {output}")
        except Exception as e:
            return ToolResult(False, f"✗ decrypt_file failed: {e}")

    @staticmethod
    def secure_delete(path: str, passes: int = 3) -> ToolResult:
        try:
            import os
            from pathlib import Path

            p = Path(path)
            if not p.exists():
                return ToolResult(False, f"✗ File not found: {path}")
            size = p.stat().st_size
            with open(path, "r+b") as f:
                for _ in range(passes):
                    f.seek(0)
                    f.write(os.urandom(size))
                    f.flush()
            p.unlink()
            return ToolResult(True, f"✓ Securely deleted: {path} ({passes} passes)")
        except Exception as e:
            return ToolResult(False, f"✗ secure_delete failed: {e}")

    @staticmethod
    def split_file(path: str, chunk_size: int = 10485760, output_folder: str = None) -> ToolResult:
        try:
            from pathlib import Path

            src  = Path(path)
            dest = Path(output_folder) if output_folder else src.parent / (src.stem + "_parts")
            dest.mkdir(parents=True, exist_ok=True)
            count = 0
            with open(path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    part_path = dest / f"{src.name}.part{count:04d}"
                    part_path.write_bytes(chunk)
                    count += 1
            return ToolResult(True, f"✓ Split into {count} parts in {dest}")
        except Exception as e:
            return ToolResult(False, f"✗ split_file failed: {e}")

    @staticmethod
    def join_files(parts_folder: str, output: str, extension: str = ".part") -> ToolResult:
        try:
            from pathlib import Path

            parts = sorted(Path(parts_folder).glob(f"*{extension}*"))
            if not parts:
                return ToolResult(False, f"✗ No parts found in {parts_folder}")
            with open(output, "wb") as out_f:
                for part in parts:
                    out_f.write(part.read_bytes())
            return ToolResult(True, f"✓ Joined {len(parts)} parts → {output}")
        except Exception as e:
            return ToolResult(False, f"✗ join_files failed: {e}")

    @staticmethod
    def compress_folder(
        path: str, output: str = None, algorithm: str = "zip", level: int = 6
    ) -> ToolResult:
        try:
            import shutil, zipfile, tarfile
            from pathlib import Path

            src  = Path(path)
            dest = output or str(src) + (".zip" if algorithm == "zip" else ".tar.gz")
            if algorithm == "zip":
                with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=level) as zf:
                    for f in src.rglob("*"):
                        if f.is_file():
                            zf.write(f, f.relative_to(src.parent))
            else:
                mode = "w:gz" if algorithm in ("gz", "gzip", "tar.gz") else "w:bz2"
                with tarfile.open(dest, mode) as tf:
                    tf.add(path, arcname=src.name)
            return ToolResult(True, f"✓ Compressed to {dest}")
        except Exception as e:
            return ToolResult(False, f"✗ compress_folder failed: {e}")

    @staticmethod
    def scan_for_malware(path: str, patterns: list = None) -> ToolResult:
        try:
            from pathlib import Path
            import re

            suspicious_patterns = patterns or [
                r"eval\(base64_decode", r"exec\(base64",
                r"<\?php.*system\(",   r"cmd\.exe /c",
                r"powershell -enc",    r"wget.*http.*\|.*bash",
                r"curl.*\|.*sh",       r"rm -rf /",
                r"nc -e /bin/sh",
            ]
            found = []
            p = Path(path)
            files = list(p.rglob("*")) if p.is_dir() else [p]
            for f in files:
                if not f.is_file():
                    continue
                try:
                    content = f.read_text(errors="replace")
                    for pattern in suspicious_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            found.append({"file": str(f), "pattern": pattern})
                except Exception:
                    pass
            return ToolResult(True, f"✓ Scan complete: {len(found)} suspicious match(es)", found)
        except Exception as e:
            return ToolResult(False, f"✗ scan_for_malware failed: {e}")

    @staticmethod
    def find_large_files(
        path: str, min_size_mb: float = 100, recursive: bool = True
    ) -> ToolResult:
        try:
            from pathlib import Path

            threshold = int(min_size_mb * 1024 * 1024)
            p      = Path(path)
            search = p.rglob("*") if recursive else p.glob("*")
            large  = [
                {"path": str(f), "size_mb": round(f.stat().st_size / 1e6, 2)}
                for f in search
                if f.is_file() and f.stat().st_size >= threshold
            ]
            large.sort(key=lambda x: x["size_mb"], reverse=True)
            return ToolResult(True, f"✓ {len(large)} file(s) >= {min_size_mb} MB", large)
        except Exception as e:
            return ToolResult(False, f"✗ find_large_files failed: {e}")

    @staticmethod
    def change_permissions_recursive(path: str, mode: int = 0o755) -> ToolResult:
        try:
            import os
            from pathlib import Path

            count = 0
            for f in Path(path).rglob("*"):
                os.chmod(str(f), mode)
                count += 1
            return ToolResult(True, f"✓ Changed permissions on {count} item(s) to {oct(mode)}")
        except Exception as e:
            return ToolResult(False, f"✗ change_permissions_recursive failed: {e}")

    @staticmethod
    def change_owner_recursive(path: str, user: str, group: str = None) -> ToolResult:
        try:
            import shutil
            r = subprocess.run(
                ["chown", "-R", f"{user}:{group}" if group else user, path],
                capture_output=True, text=True,
            )
            return ToolResult(r.returncode == 0, r.stdout + r.stderr or f"✓ Owner changed to {user}")
        except Exception as e:
            return ToolResult(False, f"✗ change_owner_recursive failed: {e}")

    @staticmethod
    def mount_remote_folder(
        host: str, remote_path: str, local_path: str, credentials: dict = None, cred_key: str = "ssh"
    ) -> ToolResult:
        try:
            import paramiko, os
            from pathlib import Path

            Path(local_path).mkdir(parents=True, exist_ok=True)
            creds    = credentials or CredStore.load(cred_key)
            transport = paramiko.Transport((host, 22))
            transport.connect(username=creds.get("user", ""), password=creds.get("password", ""))
            sftp = paramiko.SFTPClient.from_transport(transport)
            files = sftp.listdir(remote_path)
            sftp.close(); transport.close()
            return ToolResult(True, f"✓ Remote folder accessible: {host}:{remote_path} ({len(files)} items)", files)
        except Exception as e:
            return ToolResult(False, f"✗ mount_remote_folder failed: {e}")

    @staticmethod
    def verify_checksum(file: str, expected: str, algorithm: str = "sha256") -> ToolResult:
        try:
            import hashlib
            h = hashlib.new(algorithm)
            with open(file, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            actual  = h.hexdigest()
            matched = actual.lower() == expected.lower()
            return ToolResult(matched, f"✓ Checksum {'matches' if matched else 'MISMATCH'}: {actual}", {"actual": actual, "expected": expected, "match": matched})
        except Exception as e:
            return ToolResult(False, f"✗ verify_checksum failed: {e}")

    @staticmethod
    def generate_checksum_file(
        folder: str, algorithm: str = "sha256", output: str = "checksums.txt"
    ) -> ToolResult:
        try:
            import hashlib
            from pathlib import Path

            lines = []
            for f in sorted(Path(folder).rglob("*")):
                if not f.is_file():
                    continue
                h = hashlib.new(algorithm)
                with open(f, "rb") as fh:
                    for chunk in iter(lambda: fh.read(65536), b""):
                        h.update(chunk)
                lines.append(f"{h.hexdigest()}  {f.relative_to(folder)}")
            Path(output).write_text("\n".join(lines))
            return ToolResult(True, f"✓ Checksums written for {len(lines)} files → {output}")
        except Exception as e:
            return ToolResult(False, f"✗ generate_checksum_file failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. ProcessAutomationTool
# ─────────────────────────────────────────────────────────────────────────────

class ProcessAutomationTool:
    name = "process_automation"
    description = (
        "Windows/Mac GUI automation: window management, mouse/keyboard control, "
        "screen image finding, application control, macro record/play."
    )
    use = ("""
Name of Tool:- ProcessAutomationTool

Purpose of Tool:- 
The ProcessAutomationTool provides a versatile interface for cross-platform cross-application Graphical User Interface (GUI) 
automation, application lifestyle control, and macro interaction capture. It utilizes lower-level library drivers to find, 
manipulate, resize, and prioritize desktop windows, dispatch targeted mouse button actions, text strings, keyboard strokes, 
and drag-and-drop sequences. It also features spatial image matching routines to anchor executions visually on desktop elements, 
manages execution run cycles via process identification frameworks, and records or executes structured peripheral event histories (macros).

Methods:-
- find_window: Queries active operating system layout nodes to locate window states matching titles or process elements.
- focus_window: Brings a designated target window front and center into operational foreground focus.
- minimize_window: Visually collapses the targeted active GUI application window.
- maximize_window: Restores or maximizes targeted system interface panels to fit the full screen area.
- click_at: Fires precise hardware-level mouse click events at explicit Cartesian pixel coordinates on the active screen workspace.
- type_text: Emulates user keyboard inputs by transmitting explicit text characters into active input boxes at specific timing intervals.
- press_key: Simulates explicit single keystrokes or complex compound hotkey modifier variations.
- drag_and_drop: Automatically handles drag-and-drop pathways by tracking mouse paths from a start point to an end point.
- scroll: Triggers vertical mouse wheel increments at explicit anchor coordinates.
- take_screenshot_region: Snippets localized pixel blocks out of the live display surface layout and writes them into image records.
- find_image_on_screen: Runs spatial template matching passes to locate visual elements matching target asset snapshots.
- click_image: Coordinates automatic visual targeting routines to spot an image element and center a mouse click right on it.
- wait_for_image: Sets up a polling validation loop that waits for a specific visual state asset to show up on screen.
- run_application: Dispatches native background shell creation executions to run third-party software bundles.
- close_application: Runs system-level process terminations using process IDs or text name lookups to force-close applications.
- get_active_window: Pulls positioning telemetry details directly from whichever window currently holds active system focus.
- get_all_windows: Extracts information from all valid workspace application titles open in the operating system architecture.
- send_hotkey: Interprets localized string formats to execute multi-key combinations quickly.
- record_macro: Intercepts and logs mouse coordinates and keyboard strokes to record automated macro sequences.
- play_macro: Replays recorded macro logs to reconstruct original peripheral movements and clicks at chosen speeds.

How to use Tool Methods:-

1. find_window:
   - Purpose: Searches through active system windows using text matching strings to find specific application layouts.
   - Arguments:
     a) title: str (default: "") - Target text string value to search for inside window titles.
     b) process_name: str (default: "") - Filter parameter string targeting process names.
   - Returns: ToolResult holding lists filled with window layout data dictionaries.
   - How to call: ProcessAutomationTool.find_window(title="Notepad")

2. focus_window:
   - Purpose: Highlights and focuses a chosen application window to prepare it for user input.
   - Arguments:
     a) title: str - Exact or partial title string of the window you want to focus.
   - Returns: ToolResult tracking focus completion states.
   - How to call: ProcessAutomationTool.focus_window(title="Calculator")

3. minimize_window:
   - Purpose: Minimizes chosen desktop interface layouts down into the system taskbar.
   - Arguments:
     a) title: str - Target title matching strings of the layout window to collapse.
   - Returns: ToolResult providing verification update logs.
   - How to call: ProcessAutomationTool.minimize_window(title="Terminal")

4. maximize_window:
   - Purpose: Expands the dimensions of a targeted window to fill the entire monitor workspace.
   - Arguments:
     a) title: str - The window title tracking criteria of the app being targeted.
   - Returns: ToolResult validating layout alterations.
   - How to call: ProcessAutomationTool.maximize_window(title="Browser")

5. click_at:
   - Purpose: Sends native click actions to any coordinate on the screen.
   - Arguments:
     a) x: int - Target horizontal pixel coordinate position.
     b) y: int - Target vertical pixel coordinate position.
     c) button: str (default: "left") - Button identifier mapping ("left", "right", "middle").
     d) clicks: int (default: 1) - Frequency count representing how many clicks to execute.
   - Returns: ToolResult confirming structural interaction metrics.
   - How to call: ProcessAutomationTool.click_at(x=500, y=400, button="right", clicks=1)

6. type_text:
   - Purpose: Automates text entry by simulating quick keyboard strokes with adjustable gaps between characters.
   - Arguments:
     a) text: str - Payloads containing the text block sequence slated for transmission.
     b) interval: float (default: 0.05) - Delays measured in seconds inserted between character executions.
   - Returns: ToolResult capturing character metrics processed.
   - How to call: ProcessAutomationTool.type_text(text="Hello, World!", interval=0.1)

7. press_key:
   - Purpose: Automates single key strikes or button shortcuts with attached modifier keys like Shift or Control.
   - Arguments:
     a) key: str - Target key value targeted for execution (e.g., "enter", "f5").
     b) modifiers: list (default: None) - Array tracking wrapping key states (e.g., ["ctrl", "alt"]).
   - Returns: ToolResult tracking execution state confirmations.
   - How to call: ProcessAutomationTool.press_key(key="s", modifiers=["ctrl"])

8. drag_and_drop:
   - Purpose: Moves the cursor to a start position, holds the left click down, and drags over to an end coordinate.
   - Arguments:
     a) from_x: int - Original coordinate position horizontal axis location.
     b) from_y: int - Original coordinate position vertical axis location.
     c) to_x: int - Terminal point coordinate destination horizontal location.
     d) to_y: int - Terminal point coordinate destination vertical location.
     d) duration: float (default: 0.5) - Time span in seconds allocated for cursor movement.
   - Returns: ToolResult registering successful translation states.
   - How to call: ProcessAutomationTool.drag_and_drop(from_x=100, from_y=100, to_x=600, to_y=600)

9. scroll:
   - Purpose: Moves the cursor to selected screen positions and executes vertical wheel scrolling movements.
   - Arguments:
     a) x: int - Target coordinate alignment horizontal anchor location.
     b) y: int - Target coordinate alignment vertical anchor location.
     c) clicks: int (default: 3) - Volume strength configuration denoting rotational scroll adjustments.
     d) direction: str (default: "down") - Text flag assigning rotational directional orientation ("up" or "down").
   - Returns: ToolResult outlining transactional execution summaries.
   - How to call: ProcessAutomationTool.scroll(x=300, y=300, clicks=10, direction="up")

10. take_screenshot_region:
    - Purpose: Captures a specific portion of the display bounding box and outputs the slice as a static image file.
    - Arguments:
      a) x: int - Top-left bounding box starting horizontal coordinate.
      b) y: int - Top-left bounding box starting vertical coordinate.
      c) width: int - Bounding box dimension width across the horizontal plane.
      d) height: int - Bounding box dimension height down the vertical plane.
      e) output: str (default: "region.png") - Storage asset path tracking where the PNG file will save.
    - Returns: ToolResult confirming file generation details on disk.
    - How to call: ProcessAutomationTool.take_screenshot_region(x=0, y=0, width=1920, height=1080, output="desktop.png")

11. find_image_on_screen:
    - Purpose: Crawls the display screen interface layout looking for match instances that replicate target image patches.
    - Arguments:
      a) image_path: str - Reference image patch asset path targeted for pattern comparison.
      b) confidence: float (default: 0.8) - Pixel matching tolerance factor required to trigger matching states (scale from 0.0 to 1.0).
    - Returns: ToolResult identifying coordinate centers and framing boundary rectangles if found.
    - How to call: ProcessAutomationTool.find_image_on_screen(image_path="submit_btn.png", confidence=0.9)

12. click_image:
    - Purpose: Combines computer vision matching with hardware interaction by locating a graphic on screen and clicking its center point.
    - Arguments:
      a) image_path: str - Local reference asset image file used for structural template searches.
      b) confidence: float (default: 0.8) - Matching metric thresholds required to validate true matches.
      c) button: str (default: "left") - Target mouse button chosen for execution once target location is verified.
    - Returns: ToolResult showing targeted positioning data coordinates.
    - How to call: ProcessAutomationTool.click_image(image_path="login_icon.png", button="left")

13. wait_for_image:
    - Purpose: Blocks active execution runs until a target visual element shows up on screen or a timeout limit is reached.
    - Arguments:
      a) image_path: str - Asset pattern file checked across the display workspace during polling loops.
      b) timeout: int (default: 30) - Maximum time allowed in seconds before throwing failure errors.
      c) confidence: float (default: 0.8) - Precision threshold used to identify valid image matches.
    - Returns: ToolResult storing center position coordinates once items appear.
    - How to call: ProcessAutomationTool.wait_for_image(image_path="dashboard_load.png", timeout=15)

14. run_application:
    - Purpose: Spawns application binaries in the background using optional configuration parameters.
    - Arguments:
      a) path_or_name: str - Execution system name or full file path string mapping the app target.
      b) args: list (default: None) - Appended operational flags passed alongside initialization calls.
      c) wait: bool (default: False) - Dictates whether execution halts until the application exits.
    - Returns: ToolResult packing launch confirmations or detailed terminal runtime capture metrics.
    - How to call: ProcessAutomationTool.run_application(path_or_name="notepad.exe", args=["notes.txt"])

15. close_application:
    - Purpose: Shuts down active background processes by matching against their process identifier numbers or name strings.
    - Arguments:
      a) name_or_pid: Union[int, str] - Target criteria used to search out processes (e.g., "chrome.exe" or 4312).
    - Returns: ToolResult listing total terminated process instances.
    - How to call: ProcessAutomationTool.close_application(name_or_pid="excel")

16. get_active_window:
    - Purpose: Retrieves positional coordinates and title tracking data from whichever window currently holds active desktop focus.
    - Arguments: None
    - Returns: ToolResult tracking titles alongside positional geometry specifications.
    - How to call: ProcessAutomationTool.get_active_window()

17. get_all_windows:
    - Purpose: Collects a comprehensive list of all active windows with valid titles open across the operating system environment.
    - Arguments: None
    - Returns: ToolResult containing arrays populated with spatial positioning dictionaries.
    - How to call: ProcessAutomationTool.get_all_windows()

18. send_hotkey:
    - Purpose: Parses simple string syntax expressions to send complex keyboard shortcuts to the system.
    - Arguments:
      a) hotkey_string: str - Combination text format linking shortcut strings with plus operators (e.g., "ctrl+alt+delete").
    - Returns: ToolResult verifying validation deliveries.
    - How to call: ProcessAutomationTool.send_hotkey(hotkey_string="ctrl+shift+esc")

19. record_macro:
    - Purpose: Listens to mouse and keyboard events to capture user actions and save them into structured macro files.
    - Arguments:
      a) output_file: str - Local JSON target file tracking where the recorded event array will save.
      b) duration: int (default: 10) - The time limit in seconds that the tool records system peripheral inputs.
    - Returns: ToolResult summarizing total data events captured.
    - How to call: ProcessAutomationTool.record_macro(output_file="macro1.json", duration=5)

20. play_macro:
    - Purpose: Reads structured macro files to replay recorded cursor pathways and inputs at adjustable speeds.
    - Arguments:
      a) macro_file: str - Local JSON macro file tracking historical automation operations.
      b) speed: float (default: 1.0) - Playback speed multiplier (e.g., 2.0 doubles the speed, 0.5 slows it down by half).
    - Returns: ToolResult mapping validation results and providing execution statistics.
    - How to call: ProcessAutomationTool.play_macro(macro_file="macro1.json", speed=1.5)
""")

    @staticmethod
    def find_window(title: str = "", process_name: str = "") -> ToolResult:
        try:
            import pygetwindow as gw
            windows = gw.getAllWindows()
            results = []
            for w in windows:
                title_match   = title.lower() in w.title.lower() if title else True
                if title_match:
                    results.append({"title": w.title, "left": w.left, "top": w.top, "width": w.width, "height": w.height})
            return ToolResult(bool(results), f"✓ Found {len(results)} window(s)", results)
        except Exception as e:
            return ToolResult(False, f"✗ find_window failed: {e}")

    @staticmethod
    def focus_window(title: str) -> ToolResult:
        try:
            import pygetwindow as gw
            wins = gw.getWindowsWithTitle(title)
            if not wins:
                return ToolResult(False, f"✗ Window not found: {title}")
            wins[0].activate()
            return ToolResult(True, f"✓ Focused window: {title}")
        except Exception as e:
            return ToolResult(False, f"✗ focus_window failed: {e}")

    @staticmethod
    def minimize_window(title: str) -> ToolResult:
        try:
            import pygetwindow as gw
            wins = gw.getWindowsWithTitle(title)
            if not wins:
                return ToolResult(False, f"✗ Window not found: {title}")
            wins[0].minimize()
            return ToolResult(True, f"✓ Minimized: {title}")
        except Exception as e:
            return ToolResult(False, f"✗ minimize_window failed: {e}")

    @staticmethod
    def maximize_window(title: str) -> ToolResult:
        try:
            import pygetwindow as gw
            wins = gw.getWindowsWithTitle(title)
            if not wins:
                return ToolResult(False, f"✗ Window not found: {title}")
            wins[0].maximize()
            return ToolResult(True, f"✓ Maximized: {title}")
        except Exception as e:
            return ToolResult(False, f"✗ maximize_window failed: {e}")

    @staticmethod
    def click_at(
        x: int, y: int, button: str = "left", clicks: int = 1
    ) -> ToolResult:
        try:
            import pyautogui
            pyautogui.click(x, y, button=button, clicks=clicks)
            return ToolResult(True, f"✓ Clicked at ({x}, {y}) with {button} button × {clicks}")
        except Exception as e:
            return ToolResult(False, f"✗ click_at failed: {e}")

    @staticmethod
    def type_text(text: str, interval: float = 0.05) -> ToolResult:
        try:
            import pyautogui
            pyautogui.typewrite(text, interval=interval)
            return ToolResult(True, f"✓ Typed {len(text)} characters")
        except Exception as e:
            return ToolResult(False, f"✗ type_text failed: {e}")

    @staticmethod
    def press_key(key: str, modifiers: list = None) -> ToolResult:
        try:
            import pyautogui
            if modifiers:
                pyautogui.hotkey(*modifiers, key)
            else:
                pyautogui.press(key)
            return ToolResult(True, f"✓ Pressed key: {key}")
        except Exception as e:
            return ToolResult(False, f"✗ press_key failed: {e}")

    @staticmethod
    def drag_and_drop(
        from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.5
    ) -> ToolResult:
        try:
            import pyautogui
            pyautogui.moveTo(from_x, from_y)
            pyautogui.dragTo(to_x, to_y, duration=duration, button="left")
            return ToolResult(True, f"✓ Dragged from ({from_x},{from_y}) to ({to_x},{to_y})")
        except Exception as e:
            return ToolResult(False, f"✗ drag_and_drop failed: {e}")

    @staticmethod
    def scroll(x: int, y: int, clicks: int = 3, direction: str = "down") -> ToolResult:
        try:
            import pyautogui
            pyautogui.moveTo(x, y)
            amount = -clicks if direction == "down" else clicks
            pyautogui.scroll(amount)
            return ToolResult(True, f"✓ Scrolled {direction} {abs(clicks)} clicks at ({x},{y})")
        except Exception as e:
            return ToolResult(False, f"✗ scroll failed: {e}")

    @staticmethod
    def take_screenshot_region(
        x: int, y: int, width: int, height: int, output: str = "region.png"
    ) -> ToolResult:
        try:
            import pyautogui
            img = pyautogui.screenshot(region=(x, y, width, height))
            img.save(output)
            return ToolResult(True, f"✓ Screenshot region saved: {output}")
        except Exception as e:
            return ToolResult(False, f"✗ take_screenshot_region failed: {e}")

    @staticmethod
    def find_image_on_screen(image_path: str, confidence: float = 0.8) -> ToolResult:
        try:
            import pyautogui
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                return ToolResult(True, f"✓ Image found at ({center.x}, {center.y})", {"x": center.x, "y": center.y, "region": location})
            return ToolResult(False, f"✗ Image not found on screen: {image_path}")
        except Exception as e:
            return ToolResult(False, f"✗ find_image_on_screen failed: {e}")

    @staticmethod
    def click_image(
        image_path: str, confidence: float = 0.8, button: str = "left"
    ) -> ToolResult:
        try:
            import pyautogui
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if not location:
                return ToolResult(False, f"✗ Image not found: {image_path}")
            pyautogui.click(location, button=button)
            return ToolResult(True, f"✓ Clicked image at ({location.x}, {location.y})")
        except Exception as e:
            return ToolResult(False, f"✗ click_image failed: {e}")

    @staticmethod
    def wait_for_image(
        image_path: str, timeout: int = 30, confidence: float = 0.8
    ) -> ToolResult:
        try:
            import pyautogui, time
            start = time.time()
            while time.time() - start < timeout:
                try:
                    loc = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
                    if loc:
                        return ToolResult(True, f"✓ Image appeared at ({loc.x}, {loc.y})", {"x": loc.x, "y": loc.y})
                except Exception:
                    pass
                time.sleep(0.5)
            return ToolResult(False, f"✗ Image not found within {timeout}s: {image_path}")
        except Exception as e:
            return ToolResult(False, f"✗ wait_for_image failed: {e}")

    @staticmethod
    def run_application(
        path_or_name: str, args: list = None, wait: bool = False
    ) -> ToolResult:
        try:
            cmd = [path_or_name] + (args or [])
            if wait:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                return ToolResult(r.returncode == 0, r.stdout + r.stderr)
            subprocess.Popen(cmd)
            return ToolResult(True, f"✓ Launched: {path_or_name}")
        except Exception as e:
            return ToolResult(False, f"✗ run_application failed: {e}")

    @staticmethod
    def close_application(name_or_pid) -> ToolResult:
        try:
            import psutil
            killed = 0
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    if str(name_or_pid).isdigit():
                        if proc.pid == int(name_or_pid):
                            proc.kill(); killed += 1
                    else:
                        if name_or_pid.lower() in proc.name().lower():
                            proc.kill(); killed += 1
                except Exception:
                    pass
            return ToolResult(killed > 0, f"✓ Closed {killed} process(es) matching '{name_or_pid}'")
        except Exception as e:
            return ToolResult(False, f"✗ close_application failed: {e}")

    @staticmethod
    def get_active_window() -> ToolResult:
        try:
            import pygetwindow as gw
            w = gw.getActiveWindow()
            if not w:
                return ToolResult(False, "✗ No active window detected.")
            return ToolResult(True, f"✓ Active window: {w.title}", {"title": w.title, "left": w.left, "top": w.top})
        except Exception as e:
            return ToolResult(False, f"✗ get_active_window failed: {e}")

    @staticmethod
    def get_all_windows() -> ToolResult:
        try:
            import pygetwindow as gw
            windows = [{"title": w.title, "left": w.left, "top": w.top, "width": w.width, "height": w.height}
                       for w in gw.getAllWindows() if w.title]
            return ToolResult(True, f"✓ {len(windows)} windows found", windows)
        except Exception as e:
            return ToolResult(False, f"✗ get_all_windows failed: {e}")

    @staticmethod
    def send_hotkey(hotkey_string: str) -> ToolResult:
        try:
            import pyautogui
            keys = hotkey_string.replace("+", " ").split()
            pyautogui.hotkey(*keys)
            return ToolResult(True, f"✓ Hotkey sent: {hotkey_string}")
        except Exception as e:
            return ToolResult(False, f"✗ send_hotkey failed: {e}")

    @staticmethod
    def record_macro(output_file: str, duration: int = 10) -> ToolResult:
        try:
            import time, json
            from pynput import mouse, keyboard

            events = []
            stop_time = [time.time() + duration]

            def on_click(x, y, button, pressed):
                if time.time() > stop_time[0]:
                    return False
                events.append({"type": "click", "x": x, "y": y, "button": str(button), "pressed": pressed, "time": time.time()})

            def on_press(key):
                if time.time() > stop_time[0]:
                    return False
                try:
                    events.append({"type": "keypress", "key": key.char, "time": time.time()})
                except AttributeError:
                    events.append({"type": "keypress", "key": str(key), "time": time.time()})

            from pynput.mouse import Listener as ML
            from pynput.keyboard import Listener as KL

            with ML(on_click=on_click), KL(on_press=on_press):
                time.sleep(duration)

            import json
            from pathlib import Path
            Path(output_file).write_text(json.dumps(events, indent=2))
            return ToolResult(True, f"✓ Macro recorded: {len(events)} events → {output_file}")
        except Exception as e:
            return ToolResult(False, f"✗ record_macro failed: {e}")

    @staticmethod
    def play_macro(macro_file: str, speed: float = 1.0) -> ToolResult:
        try:
            import json, time, pyautogui
            from pathlib import Path

            events = json.loads(Path(macro_file).read_text())
            for i, event in enumerate(events):
                if i > 0:
                    delay = (event["time"] - events[i - 1]["time"]) / speed
                    time.sleep(max(0, delay))
                if event["type"] == "click" and event["pressed"]:
                    pyautogui.click(event["x"], event["y"])
                elif event["type"] == "keypress":
                    pyautogui.press(event.get("key", ""))
            return ToolResult(True, f"✓ Macro played: {len(events)} events at {speed}× speed")
        except Exception as e:
            return ToolResult(False, f"✗ play_macro failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. PrinterTool
# ─────────────────────────────────────────────────────────────────────────────

class PrinterTool:
    name = "printer"
    description = (
        "Print management: list printers, print files/PDFs/images, manage print queue, "
        "cancel jobs, get printer status, install printers, export to PDF."
    )
    use = ("""
Name of Tool:- PrinterTool

Purpose of Tool:- 
The PrinterTool provides a robust cross-platform interface for local and network print subsystem management, 
document spooling, queue parsing, device provisioning, and file-to-PDF conversion pipelines. It bridges systemic differences 
by abstraction layers over the Windows Print Spooler APIs (`win32print`, `win32api`) and POSIX Common Unix Printing Systems 
(CUPS command utilities like `lp`, `lpstat`, `lpq`, `cancel`, and `lpadmin`). This allows applications to uniformly programmatically 
discover devices, audit real-time diagnostic status metrics, enqueue file variations (raw text, structured PDFs, binary images), 
purge stalled spool jobs, provision fresh drivers, or render headless documents into fixed-layout PDF variants.

Methods:-
- list_printers: Queries the active platform sub-layer to discover all locally or networks attached printable hardware destinations.
- get_default_printer: Evaluates fallback routing states to output the hardware device currently designated as the primary target.
- set_default_printer: Overrides global system preferences to lock down a target printing node for headless dispatch queues.
- print_file: Routes raw text or structured document objects through the system printing stack using optional parameters.
- print_pdf: dispatches precise multipage PDF streams into target spoolers while respecting pagination limits and layout constraints.
- print_image: Transmits graphic binaries (PNG, JPEG, etc.) directly into local imaging targets, supporting aspect scaling configurations.
- get_print_queue: Audits hardware device backlogs to parse, snapshot, and structure data blocks representing waiting jobs.
- cancel_job: Issues immediate abort commands down targeted system rails to pull stalled data streams from device queues.
- get_printer_status: Connects directly with device configurations to parse current operational states and active workloads.
- install_printer: Deploys virtual or physical endpoint print pathways into device trees using hardware address ports and drivers.
- export_to_pdf: Leverages headless sub-processes (Word COM blocks, cupsfilters, or LibreOffice engines) to render layout assets into PDFs.

How to use Tool Methods:-

1. list_printers:
   - Purpose: Crawls system registry pathways or local daemon services to discover all operational printer layouts.
   - Arguments: None
   - Returns: ToolResult holding lists filled with discovered printer string name targets.
   - How to call: PrinterTool.list_printers()

2. get_default_printer:
   - Purpose: Checks system environment defaults to identify which printer acts as the automatic target when none is specified.
   - Arguments: None
   - Returns: ToolResult containing data matrices detailing the default printer name.
   - How to call: PrinterTool.get_default_printer()

3. set_default_printer:
   - Purpose: Changes system-wide preferences to assign a chosen printer as the automatic primary target.
   - Arguments:
     a) name: str - Target printer identifier name string slated for focus allocation.
   - Returns: ToolResult tracking routing completion states.
   - How to call: PrinterTool.set_default_printer(name="Office_Laser_Jet")

4. print_file:
   - Purpose: Dispatches native text or documents to chosen hardware destinations with optional formatting controls.
   - Arguments:
     a) file_path: str - Target document or text file asset path slated for hardware translation.
     b) printer: str (default: None) - Name of the device target (falls back to system default if empty).
     c) copies: int (default: 1) - Quantitative volume metric specifying total printouts to produce.
     d) orientation: str (default: "portrait") - Layout design routing parameter selection ("portrait" or "landscape").
     e) paper_size: str (default: "A4") - Target size constraint formatting (e.g., "A4", "Letter").
     f) duplex: bool (default: False) - Enables double-sided printing modes on supporting hardware.
   - Returns: ToolResult validating spool transmission confirmations.
   - How to call: PrinterTool.print_file(file_path="invoice.txt", printer="DeskJet_110", copies=2)

5. print_pdf:
   - Purpose: Processes PDF files through system print stacks with specialized page selection and fit parameters.
   - Arguments:
     a) pdf_path: str - Local target PDF file path scheduled for physical printing.
     b) printer: str (default: None) - System identifier mapping the targeted printer destination.
     c) pages: str (default: None) - Explicit layout range boundaries targeted for rendering (e.g., "1-3, 5").
     d) copies: int (default: 1) - Frequency count representing how many duplicates to print.
     b) fit_to_page: bool (default: True) - Automatically resizes document bounds to match media dimensions.
   - Returns: ToolResult tracking successful job submission events.
   - How to call: PrinterTool.print_pdf(pdf_path="report.pdf", pages="1, 3-5", fit_to_page=True)

6. print_image:
   - Purpose: Passes raw binary graphic files directly to printing layout arrays.
   - Arguments:
     a) image_path: str - Path directing the engine to the target graphics file asset (e.g., "photo.jpg").
     b) printer: str (default: None) - Hardware address label mapping the target print station.
     c) copies: int (default: 1) - Total number of physical print executions requested.
     d) fit: bool (default: True) - Forces image boundaries to conform smoothly to printable area footprints.
   - Returns: ToolResult indicating confirmation of safe transaction handoffs.
   - How to call: PrinterTool.print_image(image_path="schematic.png", printer="Plotter_01", fit=True)

7. get_print_queue:
   - Purpose: Inspects active hardware print buffers to pull a detailed log of all queued or stuck print jobs.
   - Arguments:
     a) printer: str (default: None) - Target printer name string chosen for verification checks (defaults to primary if blank).
   - Returns: ToolResult packing lists tracking queued task structures, IDs, and ownership properties.
   - How to call: PrinterTool.get_print_queue(printer="Office_Laser_Jet")

8. cancel_job:
   - Purpose: Purges stalled, corrupted, or unwanted print tasks using explicit task tracking codes.
   - Arguments:
     a) job_id: str - Explicit operational task sequence number targeted for deletion.
     b) printer: str (default: None) - Host printer device label where the job is currently queued.
   - Returns: ToolResult confirming queue eviction results.
   - How to call: PrinterTool.cancel_job(job_id="104", printer="Office_Laser_Jet")

9. get_printer_status:
   - Purpose: Connects with active peripheral devices to report status details and current task load metrics.
   - Arguments:
     a) printer: str - The specific target printer name string selected for diagnostic screening.
   - Returns: ToolResult detailing systemic status codes alongside current task backlogs.
   - How to call: PrinterTool.get_printer_status(printer="HP_PageWide")

10. install_printer:
    - Purpose: Registers a new printer connection with the operating system using selected communication ports and drivers.
    - Arguments:
      a) name: str - Appointed friendly tracking label assigned to define the new printer.
      b) driver: str (default: "") - Specific system architecture driver string model registration.
      c) port: str (default: "USB001") - Virtual or physical connector channel map matching the hardware link (e.g., "LPT1", "192.168.1.50").
    - Returns: ToolResult providing hardware initialization status profiles.
    - How to call: PrinterTool.install_printer(name="Label_Printer", driver="Zebra Generic", port="USB002")

11. export_to_pdf:
    - Purpose: Triggers background document conversion pipelines to transform files like .docx or .txt into standardized PDF format packages.
    - Arguments:
      a) file_path: str - Target source file path chosen for fixed-layout PDF rebuilding.
      b) output: str (default: None) - Explicit destination save path (autocompletes a matching name with a .pdf extension if blank).
    - Returns: ToolResult logging the saved output location of the generated PDF file.
    - How to call: PrinterTool.export_to_pdf(file_path="draft.docx", output="final_release.pdf")
""")

    @staticmethod
    def list_printers() -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                import win32print
                printers = [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
            elif os_name == "Darwin":
                r = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                printers = [l.split()[1] for l in r.stdout.splitlines() if l.startswith("printer")]
            else:
                r = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                printers = [l.split()[1] for l in r.stdout.splitlines() if l.startswith("printer")]
            return ToolResult(True, f"✓ {len(printers)} printer(s) found", printers)
        except Exception as e:
            return ToolResult(False, f"✗ list_printers failed: {e}")

    @staticmethod
    def get_default_printer() -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                import win32print
                printer = win32print.GetDefaultPrinter()
            else:
                r = subprocess.run(["lpstat", "-d"], capture_output=True, text=True)
                printer = r.stdout.strip().split(":")[-1].strip()
            return ToolResult(True, f"✓ Default printer: {printer}", {"printer": printer})
        except Exception as e:
            return ToolResult(False, f"✗ get_default_printer failed: {e}")

    @staticmethod
    def set_default_printer(name: str) -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                import win32print
                win32print.SetDefaultPrinter(name)
            else:
                subprocess.run(["lpoptions", "-d", name], capture_output=True)
            return ToolResult(True, f"✓ Default printer set to: {name}")
        except Exception as e:
            return ToolResult(False, f"✗ set_default_printer failed: {e}")

    @staticmethod
    def print_file(
        file_path: str,
        printer: str = None,
        copies: int = 1,
        orientation: str = "portrait",
        paper_size: str = "A4",
        duplex: bool = False,
    ) -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                import win32print, win32api
                printer_name = printer or win32print.GetDefaultPrinter()
                win32api.ShellExecute(0, "print", file_path, f'/d:"{printer_name}"', ".", 0)
            else:
                cmd = ["lp"]
                if printer:  cmd += ["-d", printer]
                if copies > 1: cmd += ["-n", str(copies)]
                cmd.append(file_path)
                subprocess.run(cmd, capture_output=True)
            return ToolResult(True, f"✓ Print job sent: {file_path}")
        except Exception as e:
            return ToolResult(False, f"✗ print_file failed: {e}")

    @staticmethod
    def print_pdf(
        pdf_path: str,
        printer: str = None,
        pages: str = None,
        copies: int = 1,
        fit_to_page: bool = True,
    ) -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                import win32print, win32api
                printer_name = printer or win32print.GetDefaultPrinter()
                win32api.ShellExecute(0, "print", pdf_path, f'/d:"{printer_name}"', ".", 0)
            else:
                cmd = ["lp"]
                if printer:  cmd += ["-d", printer]
                if copies > 1: cmd += ["-n", str(copies)]
                if pages:    cmd += ["-P", pages]
                if fit_to_page: cmd += ["-o", "fit-to-page"]
                cmd.append(pdf_path)
                subprocess.run(cmd, capture_output=True)
            return ToolResult(True, f"✓ PDF print job sent: {pdf_path}")
        except Exception as e:
            return ToolResult(False, f"✗ print_pdf failed: {e}")

    @staticmethod
    def print_image(
        image_path: str, printer: str = None, copies: int = 1, fit: bool = True
    ) -> ToolResult:
        try:
            cmd = ["lp"]
            if printer:  cmd += ["-d", printer]
            if copies > 1: cmd += ["-n", str(copies)]
            if fit:      cmd += ["-o", "fit-to-page"]
            cmd.append(image_path)
            r = subprocess.run(cmd, capture_output=True, text=True)
            return ToolResult(r.returncode == 0, f"✓ Image print job sent: {image_path}")
        except Exception as e:
            return ToolResult(False, f"✗ print_image failed: {e}")

    @staticmethod
    def get_print_queue(printer: str = None) -> ToolResult:
        try:
            if platform.system() == "Windows":
                import win32print
                pname = printer or win32print.GetDefaultPrinter()
                hPrinter = win32print.OpenPrinter(pname)
                jobs = win32print.EnumJobs(hPrinter, 0, -1, 1)
                win32print.ClosePrinter(hPrinter)
                return ToolResult(True, f"✓ {len(jobs)} job(s) in queue", jobs)
            else:
                cmd = ["lpq"] + (["-P", printer] if printer else [])
                r   = subprocess.run(cmd, capture_output=True, text=True)
                return ToolResult(True, "✓ Print queue fetched", r.stdout.splitlines())
        except Exception as e:
            return ToolResult(False, f"✗ get_print_queue failed: {e}")

    @staticmethod
    def cancel_job(job_id: str, printer: str = None) -> ToolResult:
        try:
            if platform.system() == "Windows":
                import win32print
                pname = printer or win32print.GetDefaultPrinter()
                hPrinter = win32print.OpenPrinter(pname)
                win32print.SetJob(hPrinter, int(job_id), 0, None, win32print.JOB_CONTROL_DELETE)
                win32print.ClosePrinter(hPrinter)
            else:
                r = subprocess.run(["cancel", job_id] + (["-P", printer] if printer else []),
                                   capture_output=True, text=True)
            return ToolResult(True, f"✓ Job {job_id} cancelled")
        except Exception as e:
            return ToolResult(False, f"✗ cancel_job failed: {e}")

    @staticmethod
    def get_printer_status(printer: str) -> ToolResult:
        try:
            if platform.system() == "Windows":
                import win32print
                h = win32print.OpenPrinter(printer)
                info = win32print.GetPrinter(h, 2)
                win32print.ClosePrinter(h)
                return ToolResult(True, f"✓ Printer status fetched", {"status": info["Status"], "jobs": info["cJobs"]})
            else:
                r = subprocess.run(["lpstat", "-p", printer], capture_output=True, text=True)
                return ToolResult(True, "✓ Printer status fetched", r.stdout.strip())
        except Exception as e:
            return ToolResult(False, f"✗ get_printer_status failed: {e}")

    @staticmethod
    def install_printer(name: str, driver: str = "", port: str = "USB001") -> ToolResult:
        try:
            if platform.system() == "Windows":
                r = subprocess.run(
                    ["rundll32", "printui.dll,PrintUIEntry", "/if", "/b", name, "/r", port, "/m", driver],
                    capture_output=True, text=True,
                )
                return ToolResult(r.returncode == 0, r.stdout + r.stderr)
            else:
                r = subprocess.run(["lpadmin", "-p", name, "-E", "-v", port] + (["-m", driver] if driver else []),
                                   capture_output=True, text=True)
                return ToolResult(r.returncode == 0, f"✓ Printer '{name}' installed")
        except Exception as e:
            return ToolResult(False, f"✗ install_printer failed: {e}")

    @staticmethod
    def export_to_pdf(file_path: str, output: str = None) -> ToolResult:
        try:
            from pathlib import Path
            dest = output or str(Path(file_path).with_suffix(".pdf"))
            os_name = platform.system()
            if os_name == "Windows":
                r = subprocess.run(
                    ["powershell", "-Command",
                     f'$word = New-Object -ComObject Word.Application; $doc = $word.Documents.Open("{file_path}"); $doc.ExportAsFixedFormat("{dest}", 17); $word.Quit()'],
                    capture_output=True, text=True,
                )
            elif os_name == "Darwin":
                r = subprocess.run(["cupsfilter", file_path, "-o", dest], capture_output=True, text=True)
            else:
                r = subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", file_path, "--outdir", str(Path(dest).parent)],
                                   capture_output=True, text=True)
            return ToolResult(True, f"✓ Exported to PDF: {dest}")
        except Exception as e:
            return ToolResult(False, f"✗ export_to_pdf failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. ClipboardAdvancedTool
# ─────────────────────────────────────────────────────────────────────────────

class ClipboardAdvancedTool:
    name = "clipboard_advanced"
    description = (
        "Advanced clipboard: text, image, files, HTML, history, monitoring, "
        "formatted tables, rich text, and clipboard transforms."
    )
    use = ("""
Name of Tool:- ClipboardAdvancedTool

Purpose of Tool:- 
The ClipboardAdvancedTool offers a cross-platform programmatic interface for manipulating, monitoring, and converting 
operating system clipboard data. Beyond managing standard plain text transfers via `pyperclip`, it handles multimedia payloads 
(extracting and injecting images across Windows, macOS, and Linux formats), parses system-level file-drop streams, and reads raw 
HTML clipboard segments. Additionally, the tool provides real-time active clipboard monitoring via background threads, tracks 
transaction histories, formats tabular arrays into spreadsheet-compatible tab-separated values, and performs structural text string 
transformations (such as line deduplication, regex stripping, and structural statistical mapping) directly within the clipboard buffer.

Methods:-
- get_text: Extracts the current plain text string payload sitting in the system clipboard buffer.
- set_text: Commits a designated text string directly into the primary system clipboard and logs it to local history.
- get_image: Pulls rasterized graphic objects out of the current clipboard and commits the snapshot data to disk as a file.
- set_image: Registers a local graphic asset directly into the system clipboard via operating system-specific binary streams.
- get_files: Evaluates Windows drop-file storage arrays to recover absolute file paths currently staged for copy/paste actions.
- set_files: Concatenates an array of absolute file pathways into a newline-delimited text block and writes it to the clipboard.
- get_html: Reads raw structural HTML data blocks from the active system clipboard data exchange channels.
- set_html: Places raw HTML code text arrays onto the standard plain-text clipboard buffer interface.
- monitor: Spawns an asynchronous tracking daemon thread to actively log changes to the system clipboard plain text data.
- get_history: Returns a localized, chronological collection of text elements modified or intercepted by the tool framework.
- clear_history: Completely flushes the localized internal memory tracking collection array.
- copy_formatted_table: Transforms matrix tables or dictionaries into tab-separated spreadsheets and copies the string layout.
- copy_rich_text: Places strings onto the system clipboard buffer to serve as targets for generic formatting transfers.
- paste_as_plain_text: Uses regular expressions to clean HTML or markup tags from clipboard content and saves the text back.
- transform_clipboard: Executes text mutations (e.g., casing, sorting, analytics) on the text payload inside the clipboard.

How to use Tool Methods:-

1. get_text:
   - Purpose: Grabs whatever plain text string is currently held inside the shared system clipboard space.
   - Arguments: None
   - Returns: ToolResult holding the complete extracted text data.
   - How to call: ClipboardAdvancedTool.get_text()

2. set_text:
   - Purpose: Copies a new plain text string into the system clipboard and appends it to the session history array.
   - Arguments:
     a) text: str - The specific text string payload to be copied into active clipboard memory.
   - Returns: ToolResult reflecting successful text injection metrics.
   - How to call: ClipboardAdvancedTool.set_text(text="Staged configuration data string.")

3. get_image:
   - Purpose: Captures image binaries residing on the clipboard and saves the matrix output to a local image file.
   - Arguments:
     a) output: str (default: "clipboard_image.png") - The file path location where the PNG image will be saved.
   - Returns: ToolResult showing destination file paths upon validation.
   - How to call: ClipboardAdvancedTool.get_image(output="assets/extracted_blueprint.png")

4. set_image:
   - Purpose: Lowers local graphic assets directly into OS clipboard interfaces (`CF_DIB`, `osascript`, or `xclip`).
   - Arguments:
     a) path: str - Target local image asset file path slated for injection into clipboard memory.
   - Returns: ToolResult indicating completion of platform-specific binary writing workflows.
   - How to call: ClipboardAdvancedTool.set_image(path="branding/logo.png")

5. get_files:
   - Purpose: Decodes file object paths currently marked for transfer in the active Windows copy buffer.
   - Arguments: None
   - Returns: ToolResult enclosing lists of verified target absolute file paths (Supported on Windows).
   - How to call: ClipboardAdvancedTool.get_files()

6. set_files:
   - Purpose: Links collections of file paths together into a unified text block and writes it to the clipboard.
   - Arguments:
     a) paths: list - An array containing target system file paths meant for string copy procedures.
   - Returns: ToolResult validating array compilation parameters.
   - How to call: ClipboardAdvancedTool.set_files(paths=["/var/log/sys.log", "/var/log/auth.log"])

7. get_html:
   - Purpose: Accesses rich structural HTML source blocks straight out of active system transfer registers.
   - Arguments: None
   - Returns: ToolResult embedding raw markup string payload results (Supported on Windows).
   - How to call: ClipboardAdvancedTool.get_html()

8. set_html:
   - Purpose: Passes target HTML strings out onto standard text targets as plain code scripts.
   - Arguments:
     a) html: str - The raw code or markup source blocks targeted for plain text copy execution.
   - Returns: ToolResult tracking buffer operational status alerts.
   - How to call: ClipboardAdvancedTool.set_html(html="<div><p>Formatted Export</p></div>")

9. monitor:
   - Purpose: Spawns a polling daemon thread that monitors the clipboard and fires a callback whenever changes are found.
   - Arguments:
     a) callback: function - An executable function tracking parameters triggered on found string alterations.
     b) interval: float (default: 1.0) - The pause span in seconds executed between active clipboard state queries.
   - Returns: ToolResult tracking successful initialization profiles.
   - How to call: ClipboardAdvancedTool.monitor(callback=print, interval=0.5)

10. get_history:
    - Purpose: Extracts a subset array tracking structural clipboard logs collected during active tool operation.
    - Arguments:
      a) limit: int (default: 20) - Max array slice limit boundary count tracking requested historical logs.
    - Returns: ToolResult containing arrays populated with transaction record dictionaries.
    - How to call: ClipboardAdvancedTool.get_history(limit=5)

11. clear_history:
    - Purpose: Empties out historical cache records saved inside memory tracking arrays during active runtime operations.
    - Arguments: None
    - Returns: ToolResult confirming data array erasure transformations.
    - How to call: ClipboardAdvancedTool.clear_history()

12. copy_formatted_table:
    - Purpose: Formats multi-dimensional matrix entries or dictionaries into tab-delimited text blocks for spreadsheet apps.
    - Arguments:
      a) data: list - Multi-dimensional array tracking database rows targeted for string serialization.
      b) headers: list (default: None) - String array tracking column descriptors added to row layouts.
    - Returns: ToolResult summarizing dimension properties processed.
    - How to call: ClipboardAdvancedTool.copy_formatted_table(data=[[1, "Alice"], [2, "Bob"]], headers=["ID", "Name"])

13. copy_rich_text:
    - Purpose: Simulates plain data copy protocols across clipboard targets using standard string variables.
    - Arguments:
      a) text: str - The text payload slated for basic system clip registration.
      b) formatting: dict (default: None) - Placeholder mapping parameters reserved for expanded style profiles.
    - Returns: ToolResult detailing simple data transmission sizes.
    - How to call: ClipboardAdvancedTool.copy_rich_text(text="Target payload information text.")

14. paste_as_plain_text:
    - Purpose: Extracts clipboard content, strips out markup tags using regex, and copies the clean plain text back.
    - Arguments: None
    - Returns: ToolResult enclosing structural plain text strings devoid of code fragments.
    - How to call: ClipboardAdvancedTool.paste_as_plain_text()

15. transform_clipboard:
    - Purpose: Performs immediate structural text string modifications directly on the current clipboard payload.
    - Arguments:
      a) operation: str - Type of change requested. Options include:
         * "upper": Forces all alphabet letters into matching uppercase structures.
         * "lower": Shrinks strings down entirely to generic lowercase configurations.
         * "title": Shifts word capitalization alignments to match title rules.
         * "strip": Trims leading or trailing whitespace chunks.
         * "reverse": Reverses the direction of the string characters.
         * "word_count": Computes the total number of individual words found.
         * "char_count": Counts the total number of characters in the string.
         * "lines": Returns the total line count metric.
         * "dedup_lines": Deletes repeating lines while keeping the original order.
    - Returns: ToolResult capturing operational tracking results or analytical counters.
    - How to call: ClipboardAdvancedTool.transform_clipboard(operation="dedup_lines")
""")

    _history: list = []

    @staticmethod
    def get_text() -> ToolResult:
        try:
            import pyperclip
            text = pyperclip.paste()
            return ToolResult(True, f"✓ Clipboard text: {len(text)} chars", text)
        except Exception as e:
            return ToolResult(False, f"✗ get_text failed: {e}")

    @staticmethod
    def set_text(text: str) -> ToolResult:
        try:
            import pyperclip
            pyperclip.copy(text)
            ClipboardAdvancedTool._history.append({"type": "text", "content": text[:200]})
            return ToolResult(True, f"✓ Text copied to clipboard ({len(text)} chars)")
        except Exception as e:
            return ToolResult(False, f"✗ set_text failed: {e}")

    @staticmethod
    def get_image(output: str = "clipboard_image.png") -> ToolResult:
        try:
            from PIL import ImageGrab
            img = ImageGrab.grabclipboard()
            if img is None:
                return ToolResult(False, "✗ No image in clipboard.")
            img.save(output)
            return ToolResult(True, f"✓ Clipboard image saved: {output}", {"path": output})
        except Exception as e:
            return ToolResult(False, f"✗ get_image failed: {e}")

    @staticmethod
    def set_image(path: str) -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                import win32clipboard
                from PIL import Image
                import io
                img = Image.open(path).convert("RGB")
                buf = io.BytesIO()
                img.save(buf, format="BMP")
                data = buf.getvalue()[14:]
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
            elif os_name == "Darwin":
                r = subprocess.run(["osascript", "-e",
                                    f'set the clipboard to (read (POSIX file "{path}") as JPEG picture)'],
                                   capture_output=True, text=True)
            else:
                r = subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", "-i", path],
                                   capture_output=True, text=True)
            return ToolResult(True, f"✓ Image copied to clipboard: {path}")
        except Exception as e:
            return ToolResult(False, f"✗ set_image failed: {e}")

    @staticmethod
    def get_files() -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                import win32clipboard
                win32clipboard.OpenClipboard()
                try:
                    files = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
                finally:
                    win32clipboard.CloseClipboard()
                return ToolResult(True, f"✓ {len(files)} file(s) in clipboard", list(files))
            return ToolResult(False, "✗ get_files only supported on Windows currently.")
        except Exception as e:
            return ToolResult(False, f"✗ get_files failed: {e}")

    @staticmethod
    def set_files(paths: list) -> ToolResult:
        try:
            import pyperclip
            pyperclip.copy("\n".join(paths))
            return ToolResult(True, f"✓ {len(paths)} file path(s) copied to clipboard")
        except Exception as e:
            return ToolResult(False, f"✗ set_files failed: {e}")

    @staticmethod
    def get_html() -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                import win32clipboard
                HTML_FORMAT = win32clipboard.RegisterClipboardFormat("HTML Format")
                win32clipboard.OpenClipboard()
                try:
                    html = win32clipboard.GetClipboardData(HTML_FORMAT).decode("utf-8", errors="replace")
                finally:
                    win32clipboard.CloseClipboard()
                return ToolResult(True, "✓ HTML clipboard content fetched", html)
            return ToolResult(False, "✗ get_html only supported on Windows currently.")
        except Exception as e:
            return ToolResult(False, f"✗ get_html failed: {e}")

    @staticmethod
    def set_html(html: str) -> ToolResult:
        try:
            import pyperclip
            pyperclip.copy(html)
            return ToolResult(True, "✓ HTML copied to clipboard (as plain text)")
        except Exception as e:
            return ToolResult(False, f"✗ set_html failed: {e}")

    @staticmethod
    def monitor(callback, interval: float = 1.0) -> ToolResult:
        try:
            import threading, pyperclip

            last = [pyperclip.paste()]

            def _watch():
                while True:
                    import time
                    time.sleep(interval)
                    current = pyperclip.paste()
                    if current != last[0]:
                        last[0] = current
                        ClipboardAdvancedTool._history.append({"type": "text", "content": current[:200]})
                        if callback:
                            callback(current)

            threading.Thread(target=_watch, daemon=True).start()
            return ToolResult(True, f"✓ Clipboard monitor started (interval={interval}s)")
        except Exception as e:
            return ToolResult(False, f"✗ monitor failed: {e}")

    @staticmethod
    def get_history(limit: int = 20) -> ToolResult:
        try:
            hist = ClipboardAdvancedTool._history[-limit:]
            return ToolResult(True, f"✓ {len(hist)} clipboard history item(s)", hist)
        except Exception as e:
            return ToolResult(False, f"✗ get_history failed: {e}")

    @staticmethod
    def clear_history() -> ToolResult:
        try:
            ClipboardAdvancedTool._history.clear()
            return ToolResult(True, "✓ Clipboard history cleared")
        except Exception as e:
            return ToolResult(False, f"✗ clear_history failed: {e}")

    @staticmethod
    def copy_formatted_table(data: list, headers: list = None) -> ToolResult:
        try:
            import pyperclip
            if headers:
                rows = ["\t".join(str(h) for h in headers)]
            else:
                rows = []
            for row in data:
                if isinstance(row, dict):
                    rows.append("\t".join(str(v) for v in row.values()))
                else:
                    rows.append("\t".join(str(v) for v in row))
            text = "\n".join(rows)
            pyperclip.copy(text)
            return ToolResult(True, f"✓ Table copied ({len(data)} rows, {len(rows[0].split(chr(9)))} cols)")
        except Exception as e:
            return ToolResult(False, f"✗ copy_formatted_table failed: {e}")

    @staticmethod
    def copy_rich_text(text: str, formatting: dict = None) -> ToolResult:
        try:
            import pyperclip
            pyperclip.copy(text)
            return ToolResult(True, f"✓ Rich text copied ({len(text)} chars)")
        except Exception as e:
            return ToolResult(False, f"✗ copy_rich_text failed: {e}")

    @staticmethod
    def paste_as_plain_text() -> ToolResult:
        try:
            import pyperclip, re
            text = pyperclip.paste()
            plain = re.sub(r"<[^>]+>", "", text)
            pyperclip.copy(plain)
            return ToolResult(True, f"✓ Pasted as plain text ({len(plain)} chars)", plain)
        except Exception as e:
            return ToolResult(False, f"✗ paste_as_plain_text failed: {e}")

    @staticmethod
    def transform_clipboard(operation: str) -> ToolResult:
        try:
            import pyperclip
            text = pyperclip.paste()
            ops = {
                "upper":      text.upper(),
                "lower":      text.lower(),
                "title":      text.title(),
                "strip":      text.strip(),
                "reverse":    text[::-1],
                "word_count": str(len(text.split())),
                "char_count": str(len(text)),
                "lines":      str(len(text.splitlines())),
                "dedup_lines": "\n".join(dict.fromkeys(text.splitlines())),
            }
            if operation not in ops:
                return ToolResult(False, f"✗ Unknown operation: {operation}. Available: {list(ops.keys())}")
            result = ops[operation]
            if operation not in ("word_count", "char_count", "lines"):
                pyperclip.copy(result)
            return ToolResult(True, f"✓ Clipboard transformed: {operation}", result)
        except Exception as e:
            return ToolResult(False, f"✗ transform_clipboard failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. HardwareMonitorTool
# ─────────────────────────────────────────────────────────────────────────────

class HardwareMonitorTool:
    name = "hardware_monitor"
    description = (
        "Deep hardware monitoring: CPU/GPU/disk temperatures, fans, voltages, power, "
        "memory slots, SMART data, benchmarks, event log, threshold monitoring."
    )
    use = ("""
Name of Tool:- HardwareMonitorTool

Purpose of Tool:- 
The HardwareMonitorTool provides a comprehensive, cross-platform interface for auditing system hardware sensors,
measuring component performance, and monitoring real-time system stability thresholds. By bridging python libraries (`psutil`, `GPUtil`) 
with low-level operating system diagnostic binaries (`smartctl`, `dmidecode`, `lm-sensors`, PowerShell WMI interfaces, and `journalctl`), 
it abstracts telemetry parsing across varying architectures. The tool empowers applications to query thermal metrics (CPU, GPU, and storage arrays), 
track mechanical fan tachometers, extract input voltages or power states, map physical memory slot allocations, run targeted internal component 
benchmarks (processing, memory bandwidth, and disk I/O), filter system error event logs, and configure asynchronous threshold alert loops.

Methods:-
- get_cpu_temperature: Parses thermal sensors to collect individual processor or core temperatures.
- get_gpu_temperature: Communicates with graphics interfaces to aggregate telemetry on GPU load, thermals, and memory allocations.
- get_disk_temperature: Extracts physical non-volatile storage temperature readings via direct hardware sensors or SMART utilities.
- get_fan_speeds: Queries cooling fan subsystems to measure rotational speeds in RPM.
- get_voltages: Interfaces with motherboard hardware controllers to evaluate active component voltage feeds.
- get_power_consumption: Pulls diagnostic metrics relative to battery charge profiles and active watt consumption properties.
- get_memory_slots: Inspects physical memory configurations to generate detailed profiles of installed RAM sticks and empty slots.
- get_storage_devices_smart: Calls low-level disk diagnostic subsystems to pull full S.M.A.R.T. self-monitoring data grids.
- benchmark_cpu: Runs localized arithmetic loops over a timed interval to gauge mathematical compute rates.
- benchmark_memory: Executes direct bytearray reads and writes to measure active RAM throughput performance.
- benchmark_disk: Generates and reads temporary garbage data chunks to gauge storage drive read/write bandwidth velocities.
- get_system_events_log: Examines operating system log aggregators to pull back recent system crashes or critical device failures.
- monitor_thresholds: Initializes an asynchronous tracking thread that alerts a callback routine if resource limits are exceeded.

How to use Tool Methods:-

1. get_cpu_temperature:
   - Purpose: Discovers and reports current operational temperature statistics across available central processor cores.
   - Arguments: None
   - Returns: ToolResult enclosing data matrices populated with dictionary thermal profiles.
   - How to call: HardwareMonitorTool.get_cpu_temperature()

2. get_gpu_temperature:
   - Purpose: Connects with graphics adapters to inventory processing load, active temps, and memory constraints.
   - Arguments: None
   - Returns: ToolResult tracking lists populated with discrete graphic processing unit information sets.
   - How to call: HardwareMonitorTool.get_gpu_temperature()

3. get_disk_temperature:
   - Purpose: Probes active NVMe or SATA controllers to evaluate physical storage medium thermals.
   - Arguments: None
   - Returns: ToolResult holding extracted drive array temperatures.
   - How to call: HardwareMonitorTool.get_disk_temperature()

4. get_fan_speeds:
   - Purpose: Checks hardware monitoring arrays to extract cooling fan activity metrics.
   - Arguments: None
   - Returns: ToolResult encapsulating tachometer speed maps (measured in RPM).
   - How to call: HardwareMonitorTool.get_fan_speeds()

5. get_voltages:
   - Purpose: Returns motherboard voltage lines to track power distribution health.
   - Arguments: None
   - Returns: ToolResult housing string lists of mapped voltage readings (Supported on Linux).
   - How to call: HardwareMonitorTool.get_voltages()

6. get_power_consumption:
   - Purpose: Aggregates battery life remaining alongside systemic physical wattage draws.
   - Arguments: None
   - Returns: ToolResult packing a dictionary containing localized power line parameters.
   - How to call: HardwareMonitorTool.get_power_consumption()

7. get_memory_slots:
   - Purpose: Queries system hardware databases to outline the speed, size, and manufacturing info of installed RAM.
   - Arguments: None
   - Returns: ToolResult exposing structural JSON or array list items breaking down active storage lanes.
   - How to call: HardwareMonitorTool.get_memory_slots()

8. get_storage_devices_smart:
   - Purpose: Extracts historical reliability indices and self-test failure reports from physical hard disks.
   - Arguments:
     a) drive: str (default: "/dev/sda") - Target physical storage node string tracking requested diagnostic scopes.
   - Returns: ToolResult enclosing structural string line feedback grids from the smartctl subsystem.
   - How to call: HardwareMonitorTool.get_storage_devices_smart(drive="/dev/nvme0n1")

9. benchmark_cpu:
   - Purpose: Quantifies mathematical execution capabilities by counting raw square-root loops completed per second.
   - Arguments:
     a) duration: int (default: 5) - Target execution monitoring ceiling window specified in seconds.
   - Returns: ToolResult charting measured computational execution loops per second (in millions).
   - How to call: HardwareMonitorTool.benchmark_cpu(duration=3)

10. benchmark_memory:
    - Purpose: Profiles memory communication limits by tracking sequential data allocations.
    - Arguments: None
    - Returns: ToolResult tracking throughput metrics written out in megabytes per second (MB/s).
    - How to call: HardwareMonitorTool.benchmark_memory()

11. benchmark_disk:
    - Purpose: Performs sequential raw read/write processes against designated directories to verify I/O bounds.
    - Arguments:
      a) path: str (default: "/tmp") - Target folder path designated to host temporary benchmarking operations.
    - Returns: ToolResult tracking disk bandwidth velocity limits.
    - How to call: HardwareMonitorTool.benchmark_disk(path="./test_vault")

12. get_system_events_log:
    - Purpose: Inspects core OS event frameworks to find structural hardware faults or driver initialization failures.
    - Arguments:
      a) level: str (default: "ERROR") - Severity target criterion classification filters (e.g., "CRITICAL", "ERROR").
      b) count: int (default: 50) - Maximum historical event line items returned during structural filtering.
      c) source: str (default: "") - Specific driver system hardware component tracking filter tag string.
      d) hours_back: int (default: 24) - Time tracking window boundaries applied on Linux journal logs.
    - Returns: ToolResult encapsulating aggregated system fault alerts.
    - How to call: HardwareMonitorTool.get_system_events_log(level="WARNING", count=10)

13. monitor_thresholds:
    - Purpose: Sets up a continuous background tracking thread to monitor utilization bounds across core resources.
    - Arguments:
      a) thresholds: dict - Mapping configuration dictionary indicating alert ceilings (e.g., `{"cpu_percent": 85.0}`).
      b) interval: int (default: 30) - Sleep delay time sequence parameters executed between validation checks.
      c) alert_callback: function (default: None) - Trigger routine fired when a resource breaches specified limits.
    - Returns: ToolResult tracking registration setup operations.
    - How to call: HardwareMonitorTool.monitor_thresholds(thresholds={"cpu_percent": 90, "memory_percent": 95}, interval=10, alert_callback=print)
""")

    @staticmethod
    def get_cpu_temperature() -> ToolResult:
        try:
            import psutil
            temps = psutil.sensors_temperatures()
            if not temps:
                return ToolResult(False, "✗ Temperature sensors not available.")
            cpu_keys = [k for k in temps if "cpu" in k.lower() or "core" in k.lower() or "k10" in k.lower()]
            data = {}
            for k in (cpu_keys or list(temps.keys())[:2]):
                data[k] = [t._asdict() for t in temps[k]]
            return ToolResult(True, "✓ CPU temperatures fetched", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_cpu_temperature failed: {e}")

    @staticmethod
    def get_gpu_temperature() -> ToolResult:
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if not gpus:
                return ToolResult(False, "✗ No GPU detected by GPUtil.")
            data = [{"id": g.id, "name": g.name, "temperature": g.temperature, "load": g.load, "memory_used": g.memoryUsed} for g in gpus]
            return ToolResult(True, f"✓ {len(data)} GPU(s) found", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_gpu_temperature failed: {e}")

    @staticmethod
    def get_disk_temperature() -> ToolResult:
        try:
            import psutil
            temps = psutil.sensors_temperatures() or {}
            disk_keys = [k for k in temps if "nvme" in k.lower() or "disk" in k.lower() or "ssd" in k.lower()]
            if disk_keys:
                data = {k: [t._asdict() for t in temps[k]] for k in disk_keys}
                return ToolResult(True, "✓ Disk temperatures fetched", data)
            r = subprocess.run(["smartctl", "-A", "/dev/sda"], capture_output=True, text=True)
            lines = [l for l in r.stdout.splitlines() if "Temperature" in l]
            return ToolResult(bool(lines), "✓ Disk temperatures (SMART)" if lines else "✗ No disk temp data", lines)
        except Exception as e:
            return ToolResult(False, f"✗ get_disk_temperature failed: {e}")

    @staticmethod
    def get_fan_speeds() -> ToolResult:
        try:
            import psutil
            fans = psutil.sensors_fans() or {}
            if not fans:
                return ToolResult(False, "✗ Fan sensors not available on this system.")
            data = {k: [f._asdict() for f in v] for k, v in fans.items()}
            return ToolResult(True, "✓ Fan speeds fetched", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_fan_speeds failed: {e}")

    @staticmethod
    def get_voltages() -> ToolResult:
        try:
            r = subprocess.run(["sensors"], capture_output=True, text=True)
            voltage_lines = [l for l in r.stdout.splitlines() if "V" in l and ("+" in l or "-" in l)]
            return ToolResult(bool(voltage_lines), "✓ Voltages read", voltage_lines)
        except Exception as e:
            return ToolResult(False, f"✗ get_voltages failed: {e}")

    @staticmethod
    def get_power_consumption() -> ToolResult:
        try:
            import psutil
            battery = psutil.sensors_battery()
            data: dict = {}
            if battery:
                data["battery_percent"] = battery.percent
                data["plugged_in"]      = battery.power_plugged
            r = subprocess.run(["sensors"], capture_output=True, text=True)
            power_lines = [l for l in r.stdout.splitlines() if "Watt" in l or "watt" in l or "power" in l.lower()]
            data["power_lines"] = power_lines
            return ToolResult(True, "✓ Power consumption data fetched", data)
        except Exception as e:
            return ToolResult(False, f"✗ get_power_consumption failed: {e}")

    @staticmethod
    def get_memory_slots() -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                r = subprocess.run(
                    ["powershell", "-Command",
                     "Get-WmiObject Win32_PhysicalMemory | Select-Object DeviceLocator,Capacity,Speed,Manufacturer | ConvertTo-Json"],
                    capture_output=True, text=True,
                )
                import json
                try:
                    data = json.loads(r.stdout)
                    return ToolResult(True, "✓ Memory slots fetched", data)
                except Exception:
                    return ToolResult(True, "✓ Memory info", r.stdout.splitlines())
            else:
                r = subprocess.run(["dmidecode", "-t", "17"], capture_output=True, text=True)
                slots = [l.strip() for l in r.stdout.splitlines() if any(k in l for k in ["Size", "Speed", "Manufacturer", "Locator"])]
                return ToolResult(True, "✓ Memory slots fetched", slots)
        except Exception as e:
            return ToolResult(False, f"✗ get_memory_slots failed: {e}")

    @staticmethod
    def get_storage_devices_smart(drive: str = "/dev/sda") -> ToolResult:
        try:
            r = subprocess.run(["smartctl", "-a", drive], capture_output=True, text=True)
            if r.returncode not in (0, 4):
                return ToolResult(False, f"✗ SMART failed: {r.stderr}")
            lines = r.stdout.splitlines()
            return ToolResult(True, f"✓ SMART data for {drive}", lines)
        except Exception as e:
            return ToolResult(False, f"✗ get_storage_devices_smart failed: {e}")

    @staticmethod
    def benchmark_cpu(duration: int = 5) -> ToolResult:
        try:
            import time, math

            ops = 0
            start = time.time()
            while time.time() - start < duration:
                for i in range(10000):
                    math.sqrt(i * 3.14159)
                ops += 10000
            elapsed = time.time() - start
            rate = round(ops / elapsed / 1e6, 2)
            return ToolResult(True, f"✓ CPU benchmark: {rate}M ops/sec over {duration}s", {"ops_per_sec_m": rate})
        except Exception as e:
            return ToolResult(False, f"✗ benchmark_cpu failed: {e}")

    @staticmethod
    def benchmark_memory() -> ToolResult:
        try:
            import time

            size    = 100 * 1024 * 1024
            data    = bytearray(size)
            start   = time.time()
            for i in range(0, size, 4096):
                data[i] = (i % 256)
            write_time = time.time() - start
            start = time.time()
            _ = sum(data[i] for i in range(0, size, 4096))
            read_time = time.time() - start
            write_mbps = round((size / 1e6) / write_time, 1)
            read_mbps  = round((size / 1e6) / read_time, 1)
            return ToolResult(True, f"✓ Memory: write {write_mbps} MB/s, read {read_mbps} MB/s", {"write_mbps": write_mbps, "read_mbps": read_mbps})
        except Exception as e:
            return ToolResult(False, f"✗ benchmark_memory failed: {e}")

    @staticmethod
    def benchmark_disk(path: str = "/tmp") -> ToolResult:
        try:
            import time, os
            from pathlib import Path

            test_file = Path(path) / "npm_disk_bench.tmp"
            data = os.urandom(50 * 1024 * 1024)

            start = time.time()
            test_file.write_bytes(data)
            write_time = time.time() - start

            start = time.time()
            _ = test_file.read_bytes()
            read_time = time.time() - start

            test_file.unlink(missing_ok=True)
            write_mbps = round(50 / write_time, 1)
            read_mbps  = round(50 / read_time,  1)
            return ToolResult(True, f"✓ Disk: write {write_mbps} MB/s, read {read_mbps} MB/s", {"write_mbps": write_mbps, "read_mbps": read_mbps})
        except Exception as e:
            return ToolResult(False, f"✗ benchmark_disk failed: {e}")

    @staticmethod
    def get_system_events_log(
        level: str = "ERROR", count: int = 50, source: str = "", hours_back: int = 24
    ) -> ToolResult:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                r = subprocess.run(
                    ["powershell", "-Command",
                     f'Get-EventLog -LogName System -Newest {count} -EntryType {level} | Select-Object TimeGenerated,Source,Message | ConvertTo-Json'],
                    capture_output=True, text=True,
                )
                import json
                try:
                    return ToolResult(True, "✓ Event log fetched", json.loads(r.stdout))
                except Exception:
                    return ToolResult(True, "✓ Event log fetched", r.stdout.splitlines())
            else:
                r = subprocess.run(
                    ["journalctl", f"-p", level.lower(), f"--since={hours_back} hours ago", f"-n", str(count), "--no-pager"],
                    capture_output=True, text=True,
                )
                return ToolResult(True, f"✓ {len(r.stdout.splitlines())} log lines", r.stdout.splitlines())
        except Exception as e:
            return ToolResult(False, f"✗ get_system_events_log failed: {e}")

    @staticmethod
    def monitor_thresholds(
        thresholds: dict,
        interval: int = 30,
        alert_callback=None,
    ) -> ToolResult:
        try:
            import threading, psutil, time

            def _watch():
                while True:
                    alerts = []
                    cpu = psutil.cpu_percent(interval=1)
                    if "cpu_percent" in thresholds and cpu > thresholds["cpu_percent"]:
                        alerts.append({"metric": "cpu_percent", "value": cpu, "threshold": thresholds["cpu_percent"]})
                    vm = psutil.virtual_memory()
                    if "memory_percent" in thresholds and vm.percent > thresholds["memory_percent"]:
                        alerts.append({"metric": "memory_percent", "value": vm.percent, "threshold": thresholds["memory_percent"]})
                    for part in psutil.disk_partitions():
                        try:
                            usage = psutil.disk_usage(part.mountpoint)
                            if "disk_percent" in thresholds and usage.percent > thresholds["disk_percent"]:
                                alerts.append({"metric": "disk_percent", "mountpoint": part.mountpoint, "value": usage.percent})
                        except Exception:
                            pass
                    if alerts and alert_callback:
                        alert_callback(alerts)
                    time.sleep(interval)

            threading.Thread(target=_watch, daemon=True).start()
            return ToolResult(True, f"✓ Hardware threshold monitoring started (interval={interval}s)", thresholds)
        except Exception as e:
            return ToolResult(False, f"✗ monitor_thresholds failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. RaspberryPiTool
# ─────────────────────────────────────────────────────────────────────────────

class RaspberryPiTool:
    name = "raspberry_pi"
    description = (
        "Full RPi GPIO and hardware: pin setup/read/write, PWM, I2C, SPI, "
        "sensors, servo, stepper, ultrasonic, LCD, buttons, camera."
    )
    use = ("""
Name of Tool:- HardwareMonitorTool

Purpose of Tool:- 
The HardwareMonitorTool provides a comprehensive, cross-platform interface for auditing system hardware sensors,
measuring component performance, and monitoring real-time system stability thresholds. By bridging python libraries (`psutil`, `GPUtil`) 
with low-level operating system diagnostic binaries (`smartctl`, `dmidecode`, `lm-sensors`, PowerShell WMI interfaces, and `journalctl`), 
it abstracts telemetry parsing across varying architectures. The tool empowers applications to query thermal metrics (CPU, GPU, and storage arrays), 
track mechanical fan tachometers, extract input voltages or power states, map physical memory slot allocations, run targeted internal component 
benchmarks (processing, memory bandwidth, and disk I/O), filter system error event logs, and configure asynchronous threshold alert loops.

Methods:-
- get_cpu_temperature: Parses thermal sensors to collect individual processor or core temperatures.
- get_gpu_temperature: Communicates with graphics interfaces to aggregate telemetry on GPU load, thermals, and memory allocations.
- get_disk_temperature: Extracts physical non-volatile storage temperature readings via direct hardware sensors or SMART utilities.
- get_fan_speeds: Queries cooling fan subsystems to measure rotational speeds in RPM.
- get_voltages: Interfaces with motherboard hardware controllers to evaluate active component voltage feeds.
- get_power_consumption: Pulls diagnostic metrics relative to battery charge profiles and active watt consumption properties.
- get_memory_slots: Inspects physical memory configurations to generate detailed profiles of installed RAM sticks and empty slots.
- get_storage_devices_smart: Calls low-level disk diagnostic subsystems to pull full S.M.A.R.T. self-monitoring data grids.
- benchmark_cpu: Runs localized arithmetic loops over a timed interval to gauge mathematical compute rates.
- benchmark_memory: Executes direct bytearray reads and writes to measure active RAM throughput performance.
- benchmark_disk: Generates and reads temporary garbage data chunks to gauge storage drive read/write bandwidth velocities.
- get_system_events_log: Examines operating system log aggregators to pull back recent system crashes or critical device failures.
- monitor_thresholds: Initializes an asynchronous tracking thread that alerts a callback routine if resource limits are exceeded.

How to use Tool Methods:-

1. get_cpu_temperature:
   - Purpose: Discovers and reports current operational temperature statistics across available central processor cores.
   - Arguments: None
   - Returns: ToolResult enclosing data matrices populated with dictionary thermal profiles.
   - How to call: HardwareMonitorTool.get_cpu_temperature()

2. get_gpu_temperature:
   - Purpose: Connects with graphics adapters to inventory processing load, active temps, and memory constraints.
   - Arguments: None
   - Returns: ToolResult tracking lists populated with discrete graphic processing unit information sets.
   - How to call: HardwareMonitorTool.get_gpu_temperature()

3. get_disk_temperature:
   - Purpose: Probes active NVMe or SATA controllers to evaluate physical storage medium thermals.
   - Arguments: None
   - Returns: ToolResult holding extracted drive array temperatures.
   - How to call: HardwareMonitorTool.get_disk_temperature()

4. get_fan_speeds:
   - Purpose: Checks hardware monitoring arrays to extract cooling fan activity metrics.
   - Arguments: None
   - Returns: ToolResult encapsulating tachometer speed maps (measured in RPM).
   - How to call: HardwareMonitorTool.get_fan_speeds()

5. get_voltages:
   - Purpose: Returns motherboard voltage lines to track power distribution health.
   - Arguments: None
   - Returns: ToolResult housing string lists of mapped voltage readings (Supported on Linux).
   - How to call: HardwareMonitorTool.get_voltages()

6. get_power_consumption:
   - Purpose: Aggregates battery life remaining alongside systemic physical wattage draws.
   - Arguments: None
   - Returns: ToolResult packing a dictionary containing localized power line parameters.
   - How to call: HardwareMonitorTool.get_power_consumption()

7. get_memory_slots:
   - Purpose: Queries system hardware databases to outline the speed, size, and manufacturing info of installed RAM.
   - Arguments: None
   - Returns: ToolResult exposing structural JSON or array list items breaking down active storage lanes.
   - How to call: HardwareMonitorTool.get_memory_slots()

8. get_storage_devices_smart:
   - Purpose: Extracts historical reliability indices and self-test failure reports from physical hard disks.
   - Arguments:
     a) drive: str (default: "/dev/sda") - Target physical storage node string tracking requested diagnostic scopes.
   - Returns: ToolResult enclosing structural string line feedback grids from the smartctl subsystem.
   - How to call: HardwareMonitorTool.get_storage_devices_smart(drive="/dev/nvme0n1")

9. benchmark_cpu:
   - Purpose: Quantifies mathematical execution capabilities by counting raw square-root loops completed per second.
   - Arguments:
     a) duration: int (default: 5) - Target execution monitoring ceiling window specified in seconds.
   - Returns: ToolResult charting measured computational execution loops per second (in millions).
   - How to call: HardwareMonitorTool.benchmark_cpu(duration=3)

10. benchmark_memory:
    - Purpose: Profiles memory communication limits by tracking sequential data allocations.
    - Arguments: None
    - Returns: ToolResult tracking throughput metrics written out in megabytes per second (MB/s).
    - How to call: HardwareMonitorTool.benchmark_memory()

11. benchmark_disk:
    - Purpose: Performs sequential raw read/write processes against designated directories to verify I/O bounds.
    - Arguments:
      a) path: str (default: "/tmp") - Target folder path designated to host temporary benchmarking operations.
    - Returns: ToolResult tracking disk bandwidth velocity limits.
    - How to call: HardwareMonitorTool.benchmark_disk(path="./test_vault")

12. get_system_events_log:
    - Purpose: Inspects core OS event frameworks to find structural hardware faults or driver initialization failures.
    - Arguments:
      a) level: str (default: "ERROR") - Severity target criterion classification filters (e.g., "CRITICAL", "ERROR").
      b) count: int (default: 50) - Maximum historical event line items returned during structural filtering.
      c) source: str (default: "") - Specific driver system hardware component tracking filter tag string.
      d) hours_back: int (default: 24) - Time tracking window boundaries applied on Linux journal logs.
    - Returns: ToolResult encapsulating aggregated system fault alerts.
    - How to call: HardwareMonitorTool.get_system_events_log(level="WARNING", count=10)

13. monitor_thresholds:
    - Purpose: Sets up a continuous background tracking thread to monitor utilization bounds across core resources.
    - Arguments:
      a) thresholds: dict - Mapping configuration dictionary indicating alert ceilings (e.g., `{"cpu_percent": 85.0}`).
      b) interval: int (default: 30) - Sleep delay time sequence parameters executed between validation checks.
      c) alert_callback: function (default: None) - Trigger routine fired when a resource breaches specified limits.
    - Returns: ToolResult tracking registration setup operations.
    - How to call: HardwareMonitorTool.monitor_thresholds(thresholds={"cpu_percent": 90, "memory_percent": 95}, interval=10, alert_callback=print)
""")

    _pwm_channels: dict = {}

    @staticmethod
    def _gpio():
        try:
            import RPi.GPIO as GPIO
            return GPIO
        except ImportError:
            raise ImportError("RPi.GPIO not available. This tool requires a Raspberry Pi.")

    @staticmethod
    def setup_pin(pin: int, mode: str = "OUT", pull_up_down: str = "OFF") -> ToolResult:
        try:
            GPIO = RaspberryPiTool._gpio()
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            direction = GPIO.OUT if mode.upper() == "OUT" else GPIO.IN
            pud_map   = {"UP": GPIO.PUD_UP, "DOWN": GPIO.PUD_DOWN, "OFF": GPIO.PUD_OFF}
            pud       = pud_map.get(pull_up_down.upper(), GPIO.PUD_OFF)
            GPIO.setup(pin, direction, pull_up_down=pud)
            return ToolResult(True, f"✓ Pin {pin} set as {mode}")
        except Exception as e:
            return ToolResult(False, f"✗ setup_pin failed: {e}")

    @staticmethod
    def read_pin(pin: int) -> ToolResult:
        try:
            GPIO = RaspberryPiTool._gpio()
            value = GPIO.input(pin)
            return ToolResult(True, f"✓ Pin {pin} = {value}", {"pin": pin, "value": value})
        except Exception as e:
            return ToolResult(False, f"✗ read_pin failed: {e}")

    @staticmethod
    def write_pin(pin: int, value: int) -> ToolResult:
        try:
            GPIO = RaspberryPiTool._gpio()
            GPIO.output(pin, value)
            return ToolResult(True, f"✓ Pin {pin} set to {value}")
        except Exception as e:
            return ToolResult(False, f"✗ write_pin failed: {e}")

    @staticmethod
    def setup_pwm(pin: int, frequency: float = 50.0) -> ToolResult:
        try:
            GPIO = RaspberryPiTool._gpio()
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, frequency)
            pwm.start(0)
            RaspberryPiTool._pwm_channels[pin] = pwm
            return ToolResult(True, f"✓ PWM started on pin {pin} at {frequency} Hz")
        except Exception as e:
            return ToolResult(False, f"✗ setup_pwm failed: {e}")

    @staticmethod
    def set_pwm_duty(pin: int, duty_cycle: float) -> ToolResult:
        try:
            pwm = RaspberryPiTool._pwm_channels.get(pin)
            if not pwm:
                return ToolResult(False, f"✗ PWM not set up on pin {pin}. Call setup_pwm first.")
            pwm.ChangeDutyCycle(max(0, min(100, duty_cycle)))
            return ToolResult(True, f"✓ PWM duty cycle on pin {pin} set to {duty_cycle}%")
        except Exception as e:
            return ToolResult(False, f"✗ set_pwm_duty failed: {e}")

    @staticmethod
    def read_i2c(device_address: int, register: int, length: int = 1) -> ToolResult:
        try:
            import smbus2
            bus  = smbus2.SMBus(1)
            data = bus.read_i2c_block_data(device_address, register, length)
            bus.close()
            return ToolResult(True, f"✓ I2C read from 0x{device_address:02X} reg 0x{register:02X}", data)
        except Exception as e:
            return ToolResult(False, f"✗ read_i2c failed: {e}")

    @staticmethod
    def write_i2c(device_address: int, register: int, data: list) -> ToolResult:
        try:
            import smbus2
            bus = smbus2.SMBus(1)
            bus.write_i2c_block_data(device_address, register, data)
            bus.close()
            return ToolResult(True, f"✓ I2C write to 0x{device_address:02X} reg 0x{register:02X}: {data}")
        except Exception as e:
            return ToolResult(False, f"✗ write_i2c failed: {e}")

    @staticmethod
    def read_spi(device: int = 0, speed: int = 500000, mode: int = 0, length: int = 4) -> ToolResult:
        try:
            import spidev
            spi = spidev.SpiDev()
            spi.open(0, device)
            spi.max_speed_hz = speed
            spi.mode = mode
            data = spi.readbytes(length)
            spi.close()
            return ToolResult(True, f"✓ SPI read: {data}", data)
        except Exception as e:
            return ToolResult(False, f"✗ read_spi failed: {e}")

    @staticmethod
    def write_spi(device: int = 0, speed: int = 500000, mode: int = 0, data: list = None) -> ToolResult:
        try:
            import spidev
            spi = spidev.SpiDev()
            spi.open(0, device)
            spi.max_speed_hz = speed
            spi.mode = mode
            spi.xfer2(data or [0x00])
            spi.close()
            return ToolResult(True, f"✓ SPI write: {data}")
        except Exception as e:
            return ToolResult(False, f"✗ write_spi failed: {e}")

    @staticmethod
    def read_temperature_sensor(sensor_id: str = "28-", protocol: str = "1wire") -> ToolResult:
        try:
            if protocol == "1wire":
                from pathlib import Path
                base = Path("/sys/bus/w1/devices")
                sensors = list(base.glob(f"{sensor_id}*"))
                if not sensors:
                    return ToolResult(False, f"✗ No 1-wire sensor found matching '{sensor_id}'")
                raw = (sensors[0] / "w1_slave").read_text()
                temp_line = [l for l in raw.splitlines() if "t=" in l]
                if not temp_line:
                    return ToolResult(False, "✗ Could not parse temperature.")
                temp_c = int(temp_line[0].split("t=")[1]) / 1000.0
                return ToolResult(True, f"✓ Temperature: {temp_c}°C", {"celsius": temp_c, "fahrenheit": round(temp_c * 9/5 + 32, 1)})
            return ToolResult(False, f"✗ Protocol not supported: {protocol}")
        except Exception as e:
            return ToolResult(False, f"✗ read_temperature_sensor failed: {e}")

    @staticmethod
    def control_servo(pin: int, angle: float) -> ToolResult:
        try:
            if pin not in RaspberryPiTool._pwm_channels:
                RaspberryPiTool.setup_pwm(pin, 50)
            duty = 2.5 + (angle / 180.0) * 10.0
            RaspberryPiTool._pwm_channels[pin].ChangeDutyCycle(duty)
            return ToolResult(True, f"✓ Servo on pin {pin} moved to {angle}°")
        except Exception as e:
            return ToolResult(False, f"✗ control_servo failed: {e}")

    @staticmethod
    def control_stepper(
        pins: list, steps: int, direction: int = 1, speed: float = 0.001
    ) -> ToolResult:
        try:
            import time
            GPIO = RaspberryPiTool._gpio()
            GPIO.setmode(GPIO.BCM)
            for p in pins:
                GPIO.setup(p, GPIO.OUT)
            seq = [
                [1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0],
                [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0],
                [0, 0, 1, 1], [0, 0, 0, 1],
            ]
            for _ in range(steps):
                for step in (seq if direction == 1 else seq[::-1]):
                    for i, p in enumerate(pins):
                        GPIO.output(p, step[i % len(step)])
                    time.sleep(speed)
            return ToolResult(True, f"✓ Stepper moved {steps} steps {'CW' if direction == 1 else 'CCW'}")
        except Exception as e:
            return ToolResult(False, f"✗ control_stepper failed: {e}")

    @staticmethod
    def read_hcsr04_distance(trig: int, echo: int) -> ToolResult:
        try:
            import time
            GPIO = RaspberryPiTool._gpio()
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(trig, GPIO.OUT)
            GPIO.setup(echo, GPIO.IN)
            GPIO.output(trig, False)
            time.sleep(0.2)
            GPIO.output(trig, True)
            time.sleep(0.00001)
            GPIO.output(trig, False)
            timeout = time.time() + 1
            pulse_start = time.time()
            while GPIO.input(echo) == 0:
                pulse_start = time.time()
                if time.time() > timeout: break
            pulse_end = time.time()
            while GPIO.input(echo) == 1:
                pulse_end = time.time()
                if time.time() > timeout: break
            distance_cm = round((pulse_end - pulse_start) * 17150, 2)
            return ToolResult(True, f"✓ Distance: {distance_cm} cm", {"cm": distance_cm, "inches": round(distance_cm / 2.54, 2)})
        except Exception as e:
            return ToolResult(False, f"✗ read_hcsr04_distance failed: {e}")

    @staticmethod
    def display_on_lcd(i2c_address: int, text: str, row: int = 0) -> ToolResult:
        try:
            import smbus2, time
            bus = smbus2.SMBus(1)

            def _write_byte(data):
                bus.write_byte(i2c_address, data)
                time.sleep(0.0001)

            def _write_cmd(cmd):
                _write_byte(cmd & 0xF0 | 0x04)
                _write_byte(cmd & 0xF0)
                _write_byte((cmd << 4) & 0xF0 | 0x04)
                _write_byte((cmd << 4) & 0xF0)

            def _write_char(char):
                _write_byte(ord(char) & 0xF0 | 0x05)
                _write_byte(ord(char) & 0xF0 | 0x01)
                _write_byte((ord(char) << 4) & 0xF0 | 0x05)
                _write_byte((ord(char) << 4) & 0xF0 | 0x01)

            row_offsets = [0x00, 0x40]
            _write_cmd(0x80 | (row_offsets[row % len(row_offsets)]))
            for char in text[:16]:
                _write_char(char)
            bus.close()
            return ToolResult(True, f"✓ LCD row {row}: '{text[:16]}'")
        except Exception as e:
            return ToolResult(False, f"✗ display_on_lcd failed: {e}")

    @staticmethod
    def read_button(pin: int, debounce: float = 0.05) -> ToolResult:
        try:
            import time
            GPIO = RaspberryPiTool._gpio()
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            pressed = GPIO.input(pin) == GPIO.LOW
            if pressed:
                time.sleep(debounce)
                pressed = GPIO.input(pin) == GPIO.LOW
            return ToolResult(True, f"✓ Button on pin {pin}: {'PRESSED' if pressed else 'RELEASED'}", {"pressed": pressed})
        except Exception as e:
            return ToolResult(False, f"✗ read_button failed: {e}")

    @staticmethod
    def capture_camera(
        output: str = "photo.jpg", width: int = 1920, height: int = 1080, duration: int = 0
    ) -> ToolResult:
        try:
            if duration > 0:
                r = subprocess.run(["raspivid", "-o", output, "-t", str(duration * 1000),
                                    "-w", str(width), "-h", str(height)], capture_output=True)
            else:
                r = subprocess.run(["libcamera-still", "-o", output, "--width", str(width), "--height", str(height)],
                                   capture_output=True)
            return ToolResult(r.returncode == 0, f"✓ Camera capture saved: {output}")
        except Exception as e:
            return ToolResult(False, f"✗ capture_camera failed: {e}")

    @staticmethod
    def stream_camera(port: int = 8080) -> ToolResult:
        try:
            proc = subprocess.Popen(
                ["libcamera-vid", "-t", "0", "--inline", "--listen", "-o", f"tcp://0.0.0.0:{port}"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            return ToolResult(True, f"✓ Camera streaming on port {port} (PID: {proc.pid})", {"pid": proc.pid})
        except Exception as e:
            return ToolResult(False, f"✗ stream_camera failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 9. MQTTIoTTool
# ─────────────────────────────────────────────────────────────────────────────

class MQTTIoTTool:
    name = "mqtt_iot"
    description = (
        "IoT communication via MQTT: connect, publish/subscribe, JSON payloads, "
        "sensor data, device commands, Home Assistant, automations, log replay."
    )
    use = ("""
Name of Tool:- MQTTIoTTool

Purpose of Tool:- 
The MQTTIoTTool provides a centralized abstraction layer for orchestrating Internet of Things (IoT) hardware over the MQTT 
(Message Queuing Telemetry Transport) protocol. By wrapping the `paho-mqtt` ecosystem alongside underlying REST adapters, this tool 
simplifies machine-to-machine telemetry streams. It allows developers to register long-lived network client connections, issue real-time 
sensor publications, manage state tracking pipelines, establish persistent event-driven message loops, map dynamic raw JSON values to 
external brokers, listen on specific message threads with timeouts, write structured diagnostic telemetry scripts, send custom device 
commands, route integration commands to Home Assistant smart home engines, build automated conditional response flows, and capture or 
replay hardware log events.

Methods:-
- connect: Establishes a long-running client thread to a targeted central MQTT broker with secure credential mappings.
- publish: Dispatches a raw text string payload out to a designated topic network vector channel.
- subscribe: Registers a listener on designated message streams and sets an optional callback routine to parse incoming packets.
- publish_json: Converts structured Python data configurations into serialized strings before publishing them over a topic vector.
- listen_once: Monopolizes a single routing path until a packet matches the topic or a timeout ceiling triggers.
- publish_sensor_data: Structures real-time environment metrics with device IDs and timestamps into standard telemetry schemas.
- send_command: Issues control instructions or JSON parameter blocks directly down target execution channels.
- get_device_state: Publishes a query request to a device topic, then waits to intercept its structural status payload.
- control_home_assistant_entity: Targets Home Assistant platform domains via REST API backends to toggle smart appliances or automations.
- create_automation: Links a conditional sub-routine that publishes a specific response when a target keyword is read on a monitored topic.
- monitor_topics: Starts a background logger that appends incoming bus events to a local JSON Lines (JSONL) storage file.
- replay_messages: Reads captured telemetry history logs and sequentially republishes them to reconstruct specific system scenarios.

How to use Tool Methods:-

1. connect:
   - Purpose: Establishes an active network session with a local or cloud-hosted MQTT broker server.
   - Arguments:
     a) broker: str - The network hostname or IP address pointing to the active message broker node.
     b) port: int (default: 1883) - The target TCP network port used to route data traffic.
     c) username: str (default: None) - Authentication user identifier token (overrides CredStore settings).
     d) password: str (default: None) - Verification passkey token tied to the user profile string.
     e) client_id: str (default: "npm_agent") - The unique client identifier string registered on the broker.
     f) tls: bool (default: False) - Configures SSL/TLS cryptographic connection parameters when set to True.
     g) cred_key: str (default: "mqtt") - Storage lookup key used to pull credentials from an internal vault.
   - Returns: ToolResult tracking successful connection parameters.
   - How to call: MQTTIoTTool.connect(broker="192.168.1.50", port=1883, client_id="living_room_agent")

2. publish:
   - Purpose: Publishes text messages across specified network channels to alert listening nodes.
   - Arguments:
     a) topic: str - The hierarchical message routing channel path string (e.g., "home/living_room/temp").
     b) payload: str - The core raw text message body being transmitted to subscribers.
     c) qos: int (default: 0) - Quality of Service delivery guarantee metric flags (0, 1, or 2).
     d) retain: bool (default: False) - Instructs the broker to save this message as the valid reference for future subscribers.
     e) client_id: str (default: "npm_agent") - The identifier matching the specific active connection instance to use.
   - Returns: ToolResult verifying successful socket delivery.
   - How to call: MQTTIoTTool.publish(topic="home/garden/valve", payload="ON", qos=1, retain=True)

3. subscribe:
   - Purpose: Instructs the broker to route real-time message streams from chosen paths into the client message loop.
   - Arguments:
     a) topics: list - An array of routing filter path strings (supports wildcards like `+` or `#`).
     b) callback: function (default: None) - The processing routine triggered when a new message is intercepted.
     c) qos: int (default: 0) - The requested maximum Quality of Service protocol delivery constraint flag.
     d) client_id: str (default: "npm_agent") - Target client tracker registry identifier mapping.
   - Returns: ToolResult logging subscription validation tokens.
   - How to call: MQTTIoTTool.subscribe(topics=["home/kitchen/#", "home/status"], callback=print)

4. publish_json:
   - Purpose: Serializes dictionary data into a clean JSON string format before publishing it to the broker.
   - Arguments:
     a) topic: str - Hierarchical destination communication channel pathway string.
     b) data: dict - Structural key-value configuration payload data slated for serialization.
     c) qos: int (default: 0) - Transmission quality profile reliability level indicator.
     d) client_id: str (default: "npm_agent") - Active connection client map index string.
   - Returns: ToolResult tracking communication status metrics.
   - How to call: MQTTIoTTool.publish_json(topic="home/hvac/config", data={"target_temp": 22.5, "mode": "cool"})

5. listen_once:
   - Purpose: Blocks or monitors a target channel path to intercept a single incoming message payload before a timeout clears.
   - Arguments:
     a) topic: str - The specific structural data topic string tracked during listening cycles.
     b) timeout: int (default: 10) - Maximum window threshold in seconds allocated to wait for incoming bytes.
     c) client_id: str (default: "npm_agent") - Specific active broker connector instance target key.
   - Returns: ToolResult containing dictionary logs detailing the intercepted message topic and payload.
   - How to call: MQTTIoTTool.listen_once(topic="home/garage/door/feedback", timeout=5)

6. publish_sensor_data:
   - Purpose: Packages numerical telemetry readings into a standard ISO timestamped format for tracking dashboards.
   - Arguments:
     a) topic: str - Telemetry ingestion pathway target string.
     b) sensor_type: str - Classification token defining the physical metric (e.g., "humidity", "lux").
     b) value: float - Numerical engineering unit value reflecting physical environment sensor telemetry.
     c) unit: str - Suffix mapping indicating unit frameworks (e.g., "%", "lx", "C").
     d) device_id: str - Hardware MAC or custom identifier tracking the physical transmitter.
     e) client_id: str (default: "npm_agent") - Connection routing tag key map identifier.
   - Returns: ToolResult verifying transmission status logs.
   - How to call: MQTTIoTTool.publish_sensor_data(topic="sensors/weather", sensor_type="temperature", value=24.7, unit="C", device_id="esp32_north")

7. send_command:
   - Purpose: Forces downstream hardware systems to execute instructions by appending parameters to command sub-channels.
   - Arguments:
     a) device_topic: str - Core root directory location referencing target physical hardware arrays.
     b) command: str - Target operation label string directing actions (e.g., "reboot", "toggle_lock").
     c) params: dict (default: None) - Configuration properties containing variable instruction bounds.
     d) client_id: str (default: "npm_agent") - Client target locator tracking network routing options.
   - Returns: ToolResult logging transaction confirmations.
   - How to call: MQTTIoTTool.send_command(device_topic="devices/blinds", command="set_position", params={"open_percent": 45})

8. get_device_state:
   - Purpose: Triggers a state update request on a remote device, then catches and returns its quick status response.
   - Arguments:
     a) device_topic: str - Root identifier topic pathway corresponding to the targeted remote hardware device.
     b) timeout: int (default: 5) - Processing wait window limit in seconds allocated to hook returned results.
     c) client_id: str (default: "npm_agent") - Specific communication interface key registration map tag.
   - Returns: ToolResult tracking the returned status message values.
   - How to call: MQTTIoTTool.get_device_state(device_topic="devices/power_meter", timeout=3)

9. control_home_assistant_entity:
   - Purpose: Bypasses direct broker topics to interact with standard smart home systems using native API bearer tokens.
   - Arguments:
     a) entity_id: str - Unique target home assistant entity lookup string identifier (e.g., "light.backyard_flood").
     b) action: str - Operation tracking identifier routing request methods (e.g., "turn_on", "toggle").
     c) attributes: dict (default: None) - Variable parameter maps matching target setup demands (e.g., brightness levels).
     d) cred_key: str (default: "home_assistant") - Core configuration key matching stored platform addresses and secrets.
   - Returns: ToolResult enclosing structural tracking data returned by target systems.
   - How to call: MQTTIoTTool.control_home_assistant_entity(entity_id="climate.main_floor", action="set_temperature", attributes={"temperature": 21})

10. create_automation:
    - Purpose: Sets up a simple on-device automation that checks incoming traffic and triggers a secondary message response when matched.
    - Arguments:
      a) trigger_topic: str - Monitored interface stream route channel targeted for verification checks.
      b) trigger_value: str - Target keyword or parameter flag scanned within the message string payload.
      c) action_topic: str - Destination response channel routed to receive automated outbound notifications.
      d) action_payload: str - Core text block dispatched down the secondary lane when criteria are successfully met.
      e) client_id: str (default: "npm_agent") - Local network route mapping index tracker.
    - Returns: ToolResult confirming operational subscription handler registrations.
    - How to call: MQTTIoTTool.create_automation(trigger_topic="home/leak_sensor", trigger_value="leak_detected", action_topic="home/main_valve", action_payload="CLOSE")

11. monitor_topics:
    - Purpose: Logs background bus traffic for a set duration, writing the telemetry data out to structured log files.
    - Arguments:
      a) topics: list - Array tracking requested target path patterns slated for log parsing.
      b) log_file: str (default: "mqtt_log.jsonl") - File path location designated to receive log entries.
      c) duration: int (default: 60) - Logging window timeframe constraints specified in seconds.
      d) client_id: str (default: "npm_agent") - Core infrastructure network reference connection link index.
    - Returns: ToolResult indicating the background logging thread has initialized.
    - How to call: MQTTIoTTool.monitor_topics(topics=["tele/#"], log_file="debug_dump.jsonl", duration=120)

12. replay_messages:
    - Purpose: Reads captured system log lines and publishes them step-by-step to test system configurations or replay events.
    - Arguments:
      a) log_file: str - Target data log file reference tracking source playback strings.
      b) broker: str - Network host domain address hosting diagnostic routing target runs.
      c) port: int (default: 1883) - Connection configuration routing access door interface numbers.
      d) client_id: str (default: "replayer") - Isolated identity profile tracking player operation frameworks.
    - Returns: ToolResult confirming the total number of replayed message payloads processed.
    - How to call: MQTTIoTTool.replay_messages(log_file="debug_dump.jsonl", broker="localhost")
""")

    _clients: dict = {}
    _messages: list = []

    @staticmethod
    def connect(
        broker: str,
        port: int = 1883,
        username: str = None,
        password: str = None,
        client_id: str = "npm_agent",
        tls: bool = False,
        cred_key: str = "mqtt",
    ) -> ToolResult:
        try:
            import paho.mqtt.client as mqtt

            creds = CredStore.load(cred_key)
            user  = username or creds.get("username", "")
            pwd   = password or creds.get("password", "")

            client = mqtt.Client(client_id=client_id)
            if user:
                client.username_pw_set(user, pwd)
            if tls:
                client.tls_set()

            client.connect(broker, port, keepalive=60)
            client.loop_start()
            MQTTIoTTool._clients[client_id] = client
            return ToolResult(True, f"✓ MQTT connected to {broker}:{port} as '{client_id}'", {"client_id": client_id})
        except Exception as e:
            return ToolResult(False, f"✗ MQTT connect failed: {e}")

    @staticmethod
    def publish(
        topic: str,
        payload: str,
        qos: int = 0,
        retain: bool = False,
        client_id: str = "npm_agent",
    ) -> ToolResult:
        try:
            client = MQTTIoTTool._clients.get(client_id)
            if not client:
                return ToolResult(False, f"✗ No MQTT client '{client_id}'. Call connect() first.")
            result = client.publish(topic, payload, qos=qos, retain=retain)
            return ToolResult(result.rc == 0, f"✓ Published to '{topic}': {str(payload)[:80]}")
        except Exception as e:
            return ToolResult(False, f"✗ MQTT publish failed: {e}")

    @staticmethod
    def subscribe(
        topics: list,
        callback=None,
        qos: int = 0,
        client_id: str = "npm_agent",
    ) -> ToolResult:
        try:
            client = MQTTIoTTool._clients.get(client_id)
            if not client:
                return ToolResult(False, f"✗ No MQTT client '{client_id}'. Call connect() first.")

            def _on_message(cl, userdata, msg):
                entry = {"topic": msg.topic, "payload": msg.payload.decode("utf-8", errors="replace"), "qos": msg.qos}
                MQTTIoTTool._messages.append(entry)
                if callback:
                    callback(entry)

            client.on_message = _on_message
            for topic in topics:
                client.subscribe(topic, qos)
            return ToolResult(True, f"✓ Subscribed to {topics}")
        except Exception as e:
            return ToolResult(False, f"✗ MQTT subscribe failed: {e}")

    @staticmethod
    def publish_json(
        topic: str, data: dict, qos: int = 0, client_id: str = "npm_agent"
    ) -> ToolResult:
        try:
            import json
            return MQTTIoTTool.publish(topic, json.dumps(data), qos=qos, client_id=client_id)
        except Exception as e:
            return ToolResult(False, f"✗ MQTT publish_json failed: {e}")

    @staticmethod
    def listen_once(
        topic: str, timeout: int = 10, client_id: str = "npm_agent"
    ) -> ToolResult:
        try:
            import paho.mqtt.subscribe as subscribe

            client_info = MQTTIoTTool._clients.get(client_id)
            if not client_info:
                return ToolResult(False, f"✗ No MQTT client '{client_id}'.")
            received = [None]
            original_msg_handler = client_info._on_message

            def _once(cl, userdata, msg):
                received[0] = {"topic": msg.topic, "payload": msg.payload.decode("utf-8", errors="replace")}

            client_info.message_callback_add(topic, _once)
            import time
            start = time.time()
            while received[0] is None and time.time() - start < timeout:
                time.sleep(0.1)
            client_info.message_callback_remove(topic)
            if received[0]:
                return ToolResult(True, f"✓ Received on '{topic}'", received[0])
            return ToolResult(False, f"✗ No message received on '{topic}' within {timeout}s")
        except Exception as e:
            return ToolResult(False, f"✗ MQTT listen_once failed: {e}")

    @staticmethod
    def publish_sensor_data(
        topic: str,
        sensor_type: str,
        value: float,
        unit: str,
        device_id: str,
        client_id: str = "npm_agent",
    ) -> ToolResult:
        try:
            from datetime import datetime
            import json

            payload = {
                "device_id":   device_id,
                "sensor_type": sensor_type,
                "value":       value,
                "unit":        unit,
                "timestamp":   datetime.utcnow().isoformat() + "Z",
            }
            return MQTTIoTTool.publish(topic, json.dumps(payload), client_id=client_id)
        except Exception as e:
            return ToolResult(False, f"✗ MQTT publish_sensor_data failed: {e}")

    @staticmethod
    def send_command(
        device_topic: str,
        command: str,
        params: dict = None,
        client_id: str = "npm_agent",
    ) -> ToolResult:
        try:
            import json
            payload = {"command": command, "params": params or {}}
            return MQTTIoTTool.publish(f"{device_topic}/command", json.dumps(payload), client_id=client_id)
        except Exception as e:
            return ToolResult(False, f"✗ MQTT send_command failed: {e}")

    @staticmethod
    def get_device_state(
        device_topic: str, timeout: int = 5, client_id: str = "npm_agent"
    ) -> ToolResult:
        try:
            MQTTIoTTool.publish(f"{device_topic}/get", "state", client_id=client_id)
            return MQTTIoTTool.listen_once(f"{device_topic}/state", timeout=timeout, client_id=client_id)
        except Exception as e:
            return ToolResult(False, f"✗ MQTT get_device_state failed: {e}")

    @staticmethod
    def control_home_assistant_entity(
        entity_id: str,
        action: str,
        attributes: dict = None,
        cred_key: str = "home_assistant",
    ) -> ToolResult:
        try:
            import requests
            creds   = CredStore.load(cred_key)
            base_url = creds.get("base_url", "http://homeassistant.local:8123")
            token    = creds.get("token", "")
            headers  = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            domain   = entity_id.split(".")[0]
            payload  = {"entity_id": entity_id, **(attributes or {})}
            r = requests.post(f"{base_url}/api/services/{domain}/{action}", headers=headers, json=payload, timeout=10)
            return ToolResult(r.status_code < 300, f"✓ HA entity '{entity_id}' action '{action}' sent", r.json() if r.content else {})
        except Exception as e:
            return ToolResult(False, f"✗ MQTT control_home_assistant_entity failed: {e}")

    @staticmethod
    def create_automation(
        trigger_topic: str,
        trigger_value: str,
        action_topic: str,
        action_payload: str,
        client_id: str = "npm_agent",
    ) -> ToolResult:
        try:
            def _on_trigger(msg):
                payload = msg.get("payload", "")
                if trigger_value in payload:
                    MQTTIoTTool.publish(action_topic, action_payload, client_id=client_id)

            MQTTIoTTool.subscribe([trigger_topic], callback=_on_trigger, client_id=client_id)
            return ToolResult(True, f"✓ Automation created: '{trigger_topic}' → '{action_topic}'")
        except Exception as e:
            return ToolResult(False, f"✗ MQTT create_automation failed: {e}")

    @staticmethod
    def monitor_topics(
        topics: list, log_file: str = "mqtt_log.jsonl", duration: int = 60, client_id: str = "npm_agent"
    ) -> ToolResult:
        try:
            import threading, time, json
            from pathlib import Path

            stop_event = threading.Event()

            def _log(msg):
                with open(log_file, "a") as f:
                    f.write(json.dumps(msg) + "\n")

            MQTTIoTTool.subscribe(topics, callback=_log, client_id=client_id)

            def _stop():
                time.sleep(duration)
                stop_event.set()

            threading.Thread(target=_stop, daemon=True).start()
            return ToolResult(True, f"✓ Monitoring {topics} for {duration}s → {log_file}")
        except Exception as e:
            return ToolResult(False, f"✗ MQTT monitor_topics failed: {e}")

    @staticmethod
    def replay_messages(
        log_file: str,
        broker: str,
        port: int = 1883,
        client_id: str = "replayer",
    ) -> ToolResult:
        try:
            import json, time
            from pathlib import Path

            lines = Path(log_file).read_text().splitlines()
            if not lines:
                return ToolResult(False, "✗ Log file is empty.")
            connect_result = MQTTIoTTool.connect(broker, port, client_id=client_id)
            if not connect_result.success:
                return connect_result
            count = 0
            for line in lines:
                try:
                    msg = json.loads(line)
                    MQTTIoTTool.publish(msg["topic"], msg["payload"], client_id=client_id)
                    count += 1
                    time.sleep(0.05)
                except Exception:
                    pass
            return ToolResult(True, f"✓ Replayed {count} messages from {log_file}")
        except Exception as e:
            return ToolResult(False, f"✗ MQTT replay_messages failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 10. VirtualizationTool
# ─────────────────────────────────────────────────────────────────────────────

class VirtualizationTool:
    name = "virtualization"
    description = (
        "VM management: list, start/stop/restart/suspend/resume VMs, snapshots, "
        "info, resources, clone, export, run commands in VM, copy files to VM. "
        "Supports VirtualBox, libvirt/KVM, and VMware."
    )
    use = ("""
Name of Tool:- VirtualizationTool

Purpose of Tool:- 
The VirtualizationTool provides a generalized programmatic interface to automate and orchestrate Virtual Machines (VMs) 
across multiple hypervisors including Oracle VirtualBox, libvirt/KVM, and VMware. By executing lower-level binary wrapper commands 
(`VBoxManage`, `vmrun`, `virt-install`, `virt-clone`, `virsh`) and leveraging target platform bindings (`libvirt`), it allows developers 
to perform automated infrastructure tasks. These include querying running VM inventories, provisioning new guest operating systems with custom hardware resource limits, adjusting hardware envelopes on the fly, toggling system execution life-cycles, manipulating state restoration points (snapshots), copying operational assets directly into internal guest storage spaces, or issuing headless runtime instructions remotely over automated local test environments.

Methods:-
- list_vms: Scans the target hypervisor ecosystem to pull back an inventory list of existing virtual machine configurations.
- start_vm: Signals the hypervisor to initialize and run a target guest virtual machine (by default in a headless context).
- stop_vm: Instructs a target guest virtual machine to execute a safe ACPI shutdown cycle or forces an immediate power-off.
- restart_vm: Sequentially runs a shutdown command followed by an initialization routine to perform a full system reboot loop.
- suspend_vm: Pauses active processor states and saves guest system memory to a local persistent disk state file.
- resume_vm: Wakes up a suspended guest machine by reloading its cached RAM memory mapping back into active execution cycles.
- create_snapshot: Takes a baseline recovery capture point of a virtual machine's current state disk blocks and runtime metadata.
- restore_snapshot: Reverts a guest virtual machine's current operational volume back to a previously defined recovery snapshot point.
- delete_snapshot: Permanently purges an explicit snapshot capture chain entry to consolidate modified disk blocks.
- list_snapshots: Inspects a designated virtual machine configuration to return all associated state snapshots.
- get_vm_info: Extracts low-level properties including network addresses, CPU count, RAM sizes, and runtime attributes.
- set_vm_resources: Modifies hardware resource limits such as CPU core allocations and system memory ceilings.
- clone_vm: Creates an exact standalone copy of a source virtual machine configuration onto a new target registration block.
- export_vm: Bundles a virtual machine's logical volume configurations and disks into universally portable schemas like OVA metadata files.
- run_in_vm: Invokes guest execution layers to execute system bash commands directly inside an active virtual guest instance.
- copy_to_vm: Transfers folders or separate local file units into a designated directory tree deep inside the target virtual machine.
- create_vm: Assembles hardware properties to build a brand new bare virtual machine with assigned storage controllers and installation media.

How to use Tool Methods:-

1. list_vms:
   - Purpose: Retrieves all virtual machines registered on a specific hypervisor engine.
   - Arguments:
     a) hypervisor: str (default: "virtualbox") - The target virtualization framework name string ("virtualbox", "libvirt", or "vmware").
   - Returns: ToolResult containing an array of available virtual machine names or tracking state blocks.
   - How to call: VirtualizationTool.list_vms(hypervisor="libvirt")

2. start_vm:
   - Purpose: Powers up a configured guest virtual machine instance.
   - Arguments:
     a) name: str - The specific target registration name identifier of the virtual machine.
     b) hypervisor: str (default: "virtualbox") - Hypervisor ecosystem engine selector choice.
   - Returns: ToolResult logging the boot initialization success state.
   - How to call: VirtualizationTool.start_vm(name="ubuntu-server-22", hypervisor="virtualbox")

3. stop_vm:
   - Purpose: Safely halts guest operations or immediately drops machine power connections.
   - Arguments:
     a) name: str - Target identifier label mapping the guest machine instance.
     b) hypervisor: str (default: "virtualbox") - Target virtualization module driver key.
     c) force: bool (default: False) - Forces immediate power-off when True, bypassing standard operating system shutdown procedures.
   - Returns: ToolResult verifying execution termination.
   - How to call: VirtualizationTool.stop_vm(name="debian-test", hypervisor="vmware", force=True)

4. restart_vm:
   - Purpose: Cycles a machine through a power shutdown phase before bringing it back up.
   - Arguments:
     a) name: str - Identification name string value referencing the targeted virtual node.
     b) hypervisor: str (default: "virtualbox") - Operational platform engine target key.
   - Returns: ToolResult validating the boot re-initialization pipeline.
   - How to call: VirtualizationTool.restart_vm(name="web-app-node", hypervisor="virtualbox")

5. suspend_vm:
   - Purpose: Freezes a guest virtual machine's active state and saves its memory to disk.
   - Arguments:
     a) name: str - Unique virtual target identity token name string.
     b) hypervisor: str (default: "virtualbox") - Hypervisor framework interface engine selector.
   - Returns: ToolResult tracking machine operational state transitions.
   - How to call: VirtualizationTool.suspend_vm(name="win11-sandbox", hypervisor="libvirt")

6. resume_vm:
   - Purpose: Returns a frozen or suspended virtual machine back to an active running state.
   - Arguments:
     a) name: str - Identification registration tag mapping the target guest machine.
     b) hypervisor: str (default: "virtualbox") - Infrastructure framework platform engine key string.
   - Returns: ToolResult detailing execution state confirmations.
   - How to call: VirtualizationTool.resume_vm(name="win11-sandbox", hypervisor="libvirt")

7. create_snapshot:
   - Purpose: Saves a specific recovery checkpoint state for a chosen virtual machine.
   - Arguments:
     a) name: str - The virtual machine name identifier to capture.
     b) snapshot_name: str - A user-defined string label for tracking this snapshot entry.
     c) hypervisor: str (default: "virtualbox") - Core architectural platform engine provider flag.
   - Returns: ToolResult detailing snapshot processing success metrics.
   - How to call: VirtualizationTool.create_snapshot(name="kali-linux", snapshot_name="pre-exploit-clean", hypervisor="virtualbox")

8. restore_snapshot:
   - Purpose: Reverts a virtual machine back to a specified snapshot state, discarding any changes made since it was taken.
   - Arguments:
     a) name: str - Core targeted guest hardware registration identity name string.
     b) snapshot_name: str - Tracking title label pointing to the target restoration index.
     c) hypervisor: str (default: "virtualbox") - Infrastructure platform controller layout tag.
   - Returns: ToolResult tracking volume adjustment results.
   - How to call: VirtualizationTool.restore_snapshot(name="kali-linux", snapshot_name="pre-exploit-clean", hypervisor="virtualbox")

9. delete_snapshot:
   - Purpose: Deletes a snapshot checkpoint from a virtual machine's history chain to clean up disk space.
   - Arguments:
     a) name: str - Targeted virtual system tracking configuration label string.
     b) snapshot_name: str - Explicit tracking tag identifying the snapshot to delete.
     c) hypervisor: str (default: "virtualbox") - Virtualization core execution profile indicator.
   - Returns: ToolResult logging chain deletion confirmations.
   - How to call: VirtualizationTool.delete_snapshot(name="ubuntu-server-22", snapshot_name="old-patch-state", hypervisor="vmware")

10. list_snapshots:
    - Purpose: Lists all historical snapshots recorded for a specific virtual machine.
    - Arguments:
      a) name: str - The specific target virtual engine node label identity string.
      b) hypervisor: str (default: "virtualbox") - Operational layout management engine reference.
    - Returns: ToolResult holding structural lists tracking active snapshot history records.
    - How to call: VirtualizationTool.list_snapshots(name="database-replica", hypervisor="libvirt")

11. get_vm_info:
    - Purpose: Collects details about a virtual machine's hardware settings, state, and network properties.
    - Arguments:
      a) name: str - Reference identity name mapping target system parameters.
      b) hypervisor: str (default: "virtualbox") - Underlying hypervisor configuration target key string.
    - Returns: ToolResult containing an information dictionary detailing memory sizes, CPU cores, and IP configurations.
    - How to call: VirtualizationTool.get_vm_info(name="gateway-router", hypervisor="virtualbox")

12. set_vm_resources:
    - Purpose: Dynamically reconfigures a virtual machine's allocated CPU cores and RAM size.
    - Arguments:
      a) name: str - Selected infrastructure target machine tracking identifier.
      b) cpus: int (default: None) - Total processing core limits allocated to run within guest environments.
      c) memory_mb: int (default: None) - Capacity allocation limits defined in Megabytes mapping active RAM boundaries.
      d) hypervisor: str (default: "virtualbox") - Platform software interface control switch.
    - Returns: ToolResult confirming structural property adjustments.
    - How to call: VirtualizationTool.set_vm_resources(name="compile-box", cpus=8, memory_mb=16384, hypervisor="virtualbox")

13. clone_vm:
    - Purpose: Creates a duplicate copy of an existing virtual machine to quickly spin up new nodes.
    - Arguments:
      a) source: str - Original baseline machine registration master identification string.
      b) destination: str - Desired allocation tracking identity string for the new clone.
      c) hypervisor: str (default: "virtualbox") - Target virtualization framework runtime platform selector.
    - Returns: ToolResult documenting creation validations.
    - How to call: VirtualizationTool.clone_vm(source="ubuntu-base-template", destination="web-node-01", hypervisor="libvirt")

14. export_vm:
    - Purpose: Compiles a virtual machine and its virtual disk drives into a single portable distribution file.
    - Arguments:
      a) name: str - Virtual registration source identity tracking label.
      b) output_path: str - File system location path destination string where the export will be saved.
      c) format: str (default: "ova") - Extensible storage archive format layout structure selector.
      d) hypervisor: str (default: "virtualbox") - Execution platform context provider.
    - Returns: ToolResult validating export pipeline completions.
    - How to call: VirtualizationTool.export_vm(name="stage-db", output_path="/backups/stage-db.ova", hypervisor="virtualbox")

15. run_in_vm:
    - Purpose: Executes bash scripts or system commands directly inside an active guest operating system.
    - Arguments:
      a) name: str - Target host machine identity label reference string.
      b) command: str - Raw command string payload targeted for guest execution.
      c) hypervisor: str (default: "virtualbox") - Framework execution wrapper driver platform selector.
    - Returns: ToolResult containing standard output data or error strings returned by the guest system.
    - How to call: VirtualizationTool.run_in_vm(name="centos-worker", command="systemctl restart nginx", hypervisor="virtualbox")

16. copy_to_vm:
    - Purpose: Copies files or folders from the host system directly into a running virtual machine's file system.
    - Arguments:
      a) name: str - Destination machine profile indexing tag name string.
      b) local_path: str - Source asset file path location string residing on the host side.
      c) vm_path: str - Bounded absolute directory target location destination string inside the guest system.
      d) hypervisor: str (default: "virtualbox") - Framework application driver switch layer tracker.
    - Returns: ToolResult checking task confirmation codes.
    - How to call: VirtualizationTool.copy_to_vm(name="centos-worker", local_path="./app.conf", vm_path="/etc/app.conf", hypervisor="virtualbox")

17. create_vm:
    - Purpose: Automates building a brand new virtual machine from scratch, setting up its virtual disk, RAM, and boot ISO.
    - Arguments:
      a) name: str - Unique label identifier string indicating the target virtual engine registration node name.
      b) os: str (default: "Ubuntu_64") - Guest OS template classification profile tag.
      c) cpus: int (default: 2) - Core count capacity tracking limits.
      d) memory: int (default: 2048) - Volatile RAM memory block limits mapped in Megabytes.
      d) disk_size: int (default: 20000) - Disk drive capacity limit values assigned in Megabytes.
      e) iso_path: str (default: "") - File path location referencing an operating system installation ISO image file.
      f) hypervisor: str (default: "virtualbox") - Core hypervisor execution interface management driver string.
    - Returns: ToolResult logging full assembly and verification metrics.
    - How to call: VirtualizationTool.create_vm(name="arch-dev", os="ArchLinux_64", cpus=4, memory=4096, iso_path="/iso/arch.iso")
""")

    @staticmethod
    def _vbox(cmd: list) -> tuple:
        r = subprocess.run(["VBoxManage"] + cmd, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    @staticmethod
    def _libvirt_conn(uri: str = "qemu:///system"):
        import libvirt
        conn = libvirt.open(uri)
        if not conn:
            raise RuntimeError("Failed to open libvirt connection.")
        return conn

    @staticmethod
    def list_vms(hypervisor: str = "virtualbox") -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["list", "vms"])
                vms = [line.split('"')[1] for line in out.splitlines() if '"' in line]
                return ToolResult(rc == 0, f"✓ {len(vms)} VirtualBox VM(s)", vms)
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                domains = conn.listAllDomains()
                vms = [{"name": d.name(), "state": d.isActive()} for d in domains]
                conn.close()
                return ToolResult(True, f"✓ {len(vms)} libvirt VM(s)", vms)
            elif hypervisor == "vmware":
                r = subprocess.run(["vmrun", "list"], capture_output=True, text=True)
                return ToolResult(True, "✓ VMware VMs listed", r.stdout.splitlines())
            return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
        except Exception as e:
            return ToolResult(False, f"✗ list_vms failed: {e}")

    @staticmethod
    def start_vm(name: str, hypervisor: str = "virtualbox") -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["startvm", name, "--type", "headless"])
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                rc   = dom.create()
                out  = f"libvirt start returned {rc}"
                conn.close()
            elif hypervisor == "vmware":
                r  = subprocess.run(["vmrun", "start", name, "nogui"], capture_output=True, text=True)
                rc, out = r.returncode, r.stdout + r.stderr
            else:
                return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
            return ToolResult(rc == 0, f"✓ Started VM: {name}" if rc == 0 else out.strip())
        except Exception as e:
            return ToolResult(False, f"✗ start_vm failed: {e}")

    @staticmethod
    def stop_vm(name: str, hypervisor: str = "virtualbox", force: bool = False) -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                action = "poweroff" if force else "acpipowerbutton"
                rc, out = VirtualizationTool._vbox(["controlvm", name, action])
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                rc   = dom.destroy() if force else dom.shutdown()
                out  = ""
                conn.close()
            elif hypervisor == "vmware":
                mode = "hard" if force else "soft"
                r  = subprocess.run(["vmrun", "stop", name, mode], capture_output=True, text=True)
                rc, out = r.returncode, r.stdout + r.stderr
            else:
                return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
            return ToolResult(rc == 0, f"✓ Stopped VM: {name}")
        except Exception as e:
            return ToolResult(False, f"✗ stop_vm failed: {e}")

    @staticmethod
    def restart_vm(name: str, hypervisor: str = "virtualbox") -> ToolResult:
        try:
            VirtualizationTool.stop_vm(name, hypervisor)
            import time; time.sleep(3)
            return VirtualizationTool.start_vm(name, hypervisor)
        except Exception as e:
            return ToolResult(False, f"✗ restart_vm failed: {e}")

    @staticmethod
    def suspend_vm(name: str, hypervisor: str = "virtualbox") -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["controlvm", name, "savestate"])
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                dom.managedSave()
                conn.close(); rc = 0; out = ""
            elif hypervisor == "vmware":
                r  = subprocess.run(["vmrun", "suspend", name], capture_output=True, text=True)
                rc, out = r.returncode, r.stdout
            else:
                return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
            return ToolResult(rc == 0, f"✓ Suspended VM: {name}")
        except Exception as e:
            return ToolResult(False, f"✗ suspend_vm failed: {e}")

    @staticmethod
    def resume_vm(name: str, hypervisor: str = "virtualbox") -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["startvm", name, "--type", "headless"])
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                dom.create()
                conn.close(); rc = 0; out = ""
            elif hypervisor == "vmware":
                r  = subprocess.run(["vmrun", "start", name], capture_output=True, text=True)
                rc, out = r.returncode, r.stdout
            else:
                return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
            return ToolResult(rc == 0, f"✓ Resumed VM: {name}")
        except Exception as e:
            return ToolResult(False, f"✗ resume_vm failed: {e}")

    @staticmethod
    def create_snapshot(
        name: str, snapshot_name: str, hypervisor: str = "virtualbox"
    ) -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["snapshot", name, "take", snapshot_name])
            elif hypervisor == "libvirt":
                import xml.etree.ElementTree as ET
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                snap_xml = f"<domainsnapshot><name>{snapshot_name}</name></domainsnapshot>"
                dom.snapshotCreateXML(snap_xml, 0)
                conn.close(); rc = 0; out = ""
            elif hypervisor == "vmware":
                r  = subprocess.run(["vmrun", "snapshot", name, snapshot_name], capture_output=True, text=True)
                rc, out = r.returncode, r.stdout
            else:
                return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
            return ToolResult(rc == 0, f"✓ Snapshot '{snapshot_name}' created for VM '{name}'")
        except Exception as e:
            return ToolResult(False, f"✗ create_snapshot failed: {e}")

    @staticmethod
    def restore_snapshot(
        name: str, snapshot_name: str, hypervisor: str = "virtualbox"
    ) -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["snapshot", name, "restore", snapshot_name])
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                snap = dom.snapshotLookupByName(snapshot_name, 0)
                dom.revertToSnapshot(snap, 0)
                conn.close(); rc = 0; out = ""
            elif hypervisor == "vmware":
                r  = subprocess.run(["vmrun", "revertToSnapshot", name, snapshot_name], capture_output=True, text=True)
                rc, out = r.returncode, r.stdout
            else:
                return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
            return ToolResult(rc == 0, f"✓ Restored snapshot '{snapshot_name}' for VM '{name}'")
        except Exception as e:
            return ToolResult(False, f"✗ restore_snapshot failed: {e}")

    @staticmethod
    def delete_snapshot(
        name: str, snapshot_name: str, hypervisor: str = "virtualbox"
    ) -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["snapshot", name, "delete", snapshot_name])
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                snap = dom.snapshotLookupByName(snapshot_name, 0)
                snap.delete(0)
                conn.close(); rc = 0; out = ""
            elif hypervisor == "vmware":
                r  = subprocess.run(["vmrun", "deleteSnapshot", name, snapshot_name], capture_output=True, text=True)
                rc, out = r.returncode, r.stdout
            else:
                return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
            return ToolResult(rc == 0, f"✓ Snapshot '{snapshot_name}' deleted")
        except Exception as e:
            return ToolResult(False, f"✗ delete_snapshot failed: {e}")

    @staticmethod
    def list_snapshots(name: str, hypervisor: str = "virtualbox") -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["snapshot", name, "list"])
                return ToolResult(rc == 0, f"✓ Snapshots for '{name}'", out.splitlines())
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                snaps = [s.getName() for s in dom.listAllSnapshots()]
                conn.close()
                return ToolResult(True, f"✓ {len(snaps)} snapshot(s)", snaps)
            elif hypervisor == "vmware":
                r  = subprocess.run(["vmrun", "listSnapshots", name], capture_output=True, text=True)
                return ToolResult(True, "✓ Snapshots listed", r.stdout.splitlines())
            return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
        except Exception as e:
            return ToolResult(False, f"✗ list_snapshots failed: {e}")

    @staticmethod
    def get_vm_info(name: str, hypervisor: str = "virtualbox") -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["showvminfo", name, "--machinereadable"])
                info = dict(line.split("=", 1) for line in out.splitlines() if "=" in line)
                return ToolResult(rc == 0, f"✓ VM info: {name}", info)
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                info = {"name": dom.name(), "state": dom.isActive(), "max_memory": dom.maxMemory(), "vcpus": dom.maxVcpus()}
                conn.close()
                return ToolResult(True, f"✓ VM info: {name}", info)
            elif hypervisor == "vmware":
                r  = subprocess.run(["vmrun", "getGuestIPAddress", name], capture_output=True, text=True)
                return ToolResult(True, "✓ VM info", {"ip": r.stdout.strip()})
            return ToolResult(False, f"✗ Unknown hypervisor: {hypervisor}")
        except Exception as e:
            return ToolResult(False, f"✗ get_vm_info failed: {e}")

    @staticmethod
    def set_vm_resources(
        name: str, cpus: int = None, memory_mb: int = None, hypervisor: str = "virtualbox"
    ) -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                if cpus:
                    VirtualizationTool._vbox(["modifyvm", name, "--cpus", str(cpus)])
                if memory_mb:
                    VirtualizationTool._vbox(["modifyvm", name, "--memory", str(memory_mb)])
            elif hypervisor == "libvirt":
                conn = VirtualizationTool._libvirt_conn()
                dom  = conn.lookupByName(name)
                if memory_mb:
                    dom.setMaxMemory(memory_mb * 1024)
                    dom.setMemory(memory_mb * 1024)
                if cpus:
                    dom.setVcpus(cpus)
                conn.close()
            elif hypervisor == "vmware":
                if cpus:
                    subprocess.run(["vmrun", "writeVariable", name, "runtimeConfig", "numvcpus", str(cpus)], capture_output=True)
            return ToolResult(True, f"✓ VM resources updated: {name} (CPU={cpus}, RAM={memory_mb}MB)")
        except Exception as e:
            return ToolResult(False, f"✗ set_vm_resources failed: {e}")

    @staticmethod
    def clone_vm(
        source: str, destination: str, hypervisor: str = "virtualbox"
    ) -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["clonevm", source, "--name", destination, "--register"])
            elif hypervisor == "libvirt":
                r  = subprocess.run(["virt-clone", "--original", source, "--name", destination, "--auto-clone"], capture_output=True, text=True)
                rc, out = r.returncode, r.stdout + r.stderr
            else:
                return ToolResult(False, f"✗ clone_vm not supported for {hypervisor}")
            return ToolResult(rc == 0, f"✓ Cloned '{source}' → '{destination}'")
        except Exception as e:
            return ToolResult(False, f"✗ clone_vm failed: {e}")

    @staticmethod
    def export_vm(
        name: str,
        output_path: str,
        format: str = "ova",
        hypervisor: str = "virtualbox",
    ) -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox(["export", name, "--output", output_path])
            elif hypervisor == "libvirt":
                r  = subprocess.run(
                    ["virsh", "dumpxml", name], capture_output=True, text=True
                )
                from pathlib import Path
                Path(output_path).write_text(r.stdout)
                rc, out = r.returncode, output_path
            else:
                return ToolResult(False, f"✗ export_vm not supported for {hypervisor}")
            return ToolResult(rc == 0, f"✓ VM '{name}' exported to {output_path}")
        except Exception as e:
            return ToolResult(False, f"✗ export_vm failed: {e}")

    @staticmethod
    def run_in_vm(name: str, command: str, hypervisor: str = "virtualbox") -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox([
                    "guestcontrol", name, "run",
                    "--exe", "/bin/bash", "--", "bash", "-c", command,
                ])
            elif hypervisor == "vmware":
                creds  = CredStore.load("vmware")
                r  = subprocess.run(
                    ["vmrun", "-gu", creds.get("user", ""), "-gp", creds.get("password", ""),
                     "runProgramInGuest", name, "/bin/bash", "-c", command],
                    capture_output=True, text=True,
                )
                rc, out = r.returncode, r.stdout + r.stderr
            else:
                return ToolResult(False, f"✗ run_in_vm not supported for {hypervisor}")
            return ToolResult(rc == 0, f"✓ Command ran in VM '{name}'", out.strip())
        except Exception as e:
            return ToolResult(False, f"✗ run_in_vm failed: {e}")

    @staticmethod
    def copy_to_vm(
        name: str, local_path: str, vm_path: str, hypervisor: str = "virtualbox"
    ) -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                rc, out = VirtualizationTool._vbox([
                    "guestcontrol", name, "copyto", local_path, vm_path, "--recursive",
                ])
            elif hypervisor == "vmware":
                creds  = CredStore.load("vmware")
                r  = subprocess.run(
                    ["vmrun", "-gu", creds.get("user", ""), "-gp", creds.get("password", ""),
                     "copyFileFromHostToGuest", name, local_path, vm_path],
                    capture_output=True, text=True,
                )
                rc, out = r.returncode, r.stdout + r.stderr
            else:
                return ToolResult(False, f"✗ copy_to_vm not supported for {hypervisor}")
            return ToolResult(rc == 0, f"✓ Copied '{local_path}' to VM '{name}':{vm_path}")
        except Exception as e:
            return ToolResult(False, f"✗ copy_to_vm failed: {e}")

    @staticmethod
    def create_vm(
        name: str,
        os: str = "Ubuntu_64",
        cpus: int = 2,
        memory: int = 2048,
        disk_size: int = 20000,
        iso_path: str = "",
        hypervisor: str = "virtualbox",
    ) -> ToolResult:
        try:
            if hypervisor == "virtualbox":
                for cmd in [
                    ["createvm", "--name", name, "--ostype", os, "--register"],
                    ["modifyvm", name, "--memory", str(memory), "--cpus", str(cpus), "--nic1", "nat"],
                    ["createhd", "--filename", f"{name}.vdi", "--size", str(disk_size)],
                    ["storagectl", name, "--name", "SATA", "--add", "sata"],
                    ["storageattach", name, "--storagectl", "SATA", "--port", "0", "--type", "hdd", "--medium", f"{name}.vdi"],
                ]:
                    rc, out = VirtualizationTool._vbox(cmd)
                    if rc != 0:
                        return ToolResult(False, f"✗ VBox create_vm step failed: {out}")
                if iso_path:
                    VirtualizationTool._vbox([
                        "storageattach", name, "--storagectl", "SATA",
                        "--port", "1", "--type", "dvddrive", "--medium", iso_path,
                    ])
            elif hypervisor == "libvirt":
                r  = subprocess.run([
                    "virt-install", "--name", name, "--memory", str(memory),
                    "--vcpus", str(cpus), "--disk", f"size={disk_size // 1024}",
                    "--os-type", "linux", "--os-variant", os.lower(),
                    "--noautoconsole",
                ] + (["--cdrom", iso_path] if iso_path else ["--import"]),
                    capture_output=True, text=True,
                )
                return ToolResult(r.returncode == 0, r.stdout + r.stderr)
            else:
                return ToolResult(False, f"✗ create_vm not supported for {hypervisor}")
            return ToolResult(True, f"✓ VM '{name}' created ({os}, {cpus} CPUs, {memory}MB RAM, {disk_size}MB disk)")
        except Exception as e:
            return ToolResult(False, f"✗ create_vm failed: {e}")
