#################################################################################################
'''
NOTE:- Here we use a Library called CairoSVG because we are developing a python package framework
and we do not know on what machine this package will be installed therefore we are not able to add
the extra dependencies of CairoSVG and we do not want to make process too complex therefore we are
trying to find a dynamic solution to install that extra dependency for CairoSVG so please cooperate
here.

Updated by AdenOrg at 9:00 IST by VJ.
'''                                                                                            
#################################################################################################

"""
tools_creative.py — Creative Tools for NPM Agent (NPMAI ECOSYSTEM)
Author: Generated for Sonu Kumar / NPMAI ECOSYSTEM
Tools: FigmaTool, BlenderTool, SVGTool, CanvaTool, FontTool,
       ColorTool, IconTool, DiagramTool, PrintTool, ThreeDTool
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import colorsys
import math
import re
from pathlib import Path
from typing import Optional, List, Dict, Any

from core import ToolResult, CredStore, _ensure

# ── auto-install dependencies ────────────────────────────────────────────────
for _pkg, _imp in [
    ("requests",       "requests"),
    ("svgwrite",       "svgwrite"),
    ("cairosvg",       "cairosvg"),
    ("Pillow",         "PIL"),
    ("fonttools",      "fonttools"),
    ("colormath",      "colormath"),
    ("reportlab",      "reportlab"),
    ("weasyprint",     "weasyprint"),
    ("trimesh",        "trimesh"),
    ("networkx",       "networkx"),
    ("matplotlib",     "matplotlib"),
    ("numpy",          "numpy"),
]:
    _ensure(_pkg, _imp)

# ─────────────────────────────────────────────────────────────────────────────
# 1. FigmaTool
# ─────────────────────────────────────────────────────────────────────────────

class FigmaTool:
    name = "figma"
    description = (
        "Complete Figma API integration: read files, export assets, manage "
        "comments, webhooks, components, styles, versions and team projects."
    )
    use = (
           """Name of Tool:- FigmaTool

Purpose of Tool:- 
The FigmaTool provides a comprehensive integration with the Figma REST API, allowing programmatic access to design files, projects, prototypes, and workspace components. It enables automated design-to-code pipelines by extracting layout JSON data, rendering and downloading visual assets directly from layers, managing contextual canvas comments, tracking file version histories, and listing team space projects. It also supports automated design system auditing by listing global styles or shared components, and enables real-time event tracking by configuring live platform webhooks.

Methods:-
- get_file: Retrieves the full JSON data tree representing a specific Figma file's layers, vector properties, and hierarchy.
- get_node: Extracts design node metadata or specific subset elements isolated from a parent file tree.
- list_files: Fetches a structured inventory of all design sheets and canvases stored under an explicit project repository.
- export_asset: Renders a selected element node onto an isolated image asset file down to a local disk path.
- export_all_assets: Walks through the root document boundaries to batch download up to 50 top-level canvases or framing structures simultaneously.
- get_components: Gathers all unique reusable design blocks and interaction components published inside a specific file.
- get_styles: Catalogs shared presentation specifications like typography settings, color fills, and effect layer maps inside a file.
- get_comments: Pulls user discussion records, feedback feeds, and resolved annotations attached to canvas coordinates.
- post_comment: Appends feedback strings onto explicit X/Y canvas coordinate positions or directly anchors them onto specific node elements.
- create_webhook: Mounts an active programmatic event push notification handler that fires updates on activities like file updates or comments.
- list_projects: Returns all directory containers and workspace modules created within a target team folder space.
- get_team_components: Inventories globally published component libraries shared across a broader multi-project organizational tier.
- get_versions: Generates an analytical changelog tracking chronological commit milestones and save states for a document.

How to use Tool Methods:-

1. get_file:
   - Purpose: Acquires complete design structure specifications to dynamically analyze elements or map layouts.
   - Arguments:
     a) file_key: str - Unique alphanumeric string identifier found in a Figma file's share URL.
     b) cred_key: str (default: "figma") - Security identifier referencing the storage profile vault key.
   - Returns: ToolResult holding the full layer tree dictionary object.
   - How to call: FigmaTool.get_file(file_key="abcd1234EFGH5678")

2. get_node:
   - Purpose: Strips out complex root layers to read structural data from a single specific canvas sub-component.
   - Arguments:
     a) file_key: str - Unique alphanumeric string tracking the target file.
     b) node_id: str - Explicit ID path of the target vector or layer element (e.g., "0:1").
     c) cred_key: str (default: "figma") - Key mapping targeting authorization profiles.
   - Returns: ToolResult mapping data for the targeted canvas layout slice.
   - How to call: FigmaTool.get_node(file_key="abcd1234EFGH5678", node_id="12:204")

3. list_files:
   - Purpose: Collects an updated inventory checklist of all design sheets housed inside an explicit team project bucket.
   - Arguments:
     a) project_id: str - Alphanumeric project category bucket key.
     b) cred_key: str (default: "figma") - Reference credential pointer.
   - Returns: ToolResult packaging details of matching canvas files.
   - How to call: FigmaTool.list_files(project_id="987654321")

4. export_asset:
   - Purpose: Extracts UI layouts, icon groups, or graphic patterns into ready-to-use vector or rasterized local files.
   - Arguments:
     a) file_key: str - File locator reference code.
     b) node_id: str - Explicit element location tag target.
     c) format: str (default: "PNG") - Desired rendering output layout option ("PNG", "JPG", "SVG", "PDF").
     d) scale: float (default: 2.0) - Sizing multiplier factor managing resolution scaling.
     d) output_path: str (default: "figma_asset.png") - Storage path on the local system.
     e) cred_key: str (default: "figma") - Core token account storage access profile.
   - Returns: ToolResult confirming binary file generation and disk output locations.
   - How to call: FigmaTool.export_asset(file_key="abcd1234", node_id="4:12", format="SVG", output_path="assets/logo.svg")

5. export_all_assets:
   - Purpose: Speeds up deployment updates by harvesting batch asset collections directly out of top-level document layouts.
   - Arguments:
     a) file_key: str - File location pointer mapping code.
     b) output_folder: str - Target folder destination folder where assets will save.
     c) format: str (default: "PNG") - Render type identifier syntax string.
     d) cred_key: str (default: "figma") - Authentication mapping configuration value.
   - Returns: ToolResult documenting downing loops statistics and file tallies.
   - How to call: FigmaTool.export_all_assets(file_key="abcd1234", output_folder="./ui_export", format="JPG")

6. get_components:
   - Purpose: Extracts structural component logs to evaluate asset definitions or trace component patterns.
   - Arguments:
     a) file_key: str - Source workspace token string.
     b) cred_key: str (default: "figma") - Key context credential indicator.
   - Returns: ToolResult detailing registered template component records.
   - How to call: FigmaTool.get_components(file_key="abcd1234")

7. get_styles:
   - Purpose: Validates implementation constraints by analyzing color maps and typographic rules.
   - Arguments:
     a) file_key: str - Reference target file document identifier.
     b) cred_key: str (default: "figma") - Token workspace index tracking details.
   - Returns: ToolResult collecting published layout style definitions.
   - How to call: FigmaTool.get_styles(file_key="abcd1234")

8. get_comments:
   - Purpose: Gathers designer remarks and feedback feeds into localized tracking tasks automatically.
   - Arguments:
     a) file_key: str - Target project file index string.
     b) cred_key: str (default: "figma") - Storage key profile pointer.
   - Returns: ToolResult collecting timeline lists of feedback statements.
   - How to call: FigmaTool.get_comments(file_key="abcd1234")

9. post_comment:
   - Purpose: Leaves precise notes directly on canvas coordinates or links feedback to specific frame components.
   - Arguments:
     a) file_key: str - Design workspace path locator.
     b) message: str - Plain text note body content.
     c) x: float (default: 0) - Canvas horizontal coordinate placement marker.
     d) y: float (default: 0) - Canvas vertical coordinate placement marker.
     e) node_id: Optional[str] (default: None) - Element layout tracking index target anchor point.
     f) cred_key: str (default: "figma") - Secure credential verification lookup tag.
   - Returns: ToolResult confirming server note processing parameters.
   - How to call: FigmaTool.post_comment(file_key="abcd1234", message="Fix alignment here", node_id="100:15")

10. create_webhook:
    - Purpose: Binds automated systems to immediate webhook signals when changes or updates occur in design spaces.
    - Arguments:
      a) event_type: str - Event trigger name string (e.g., "FILE_UPDATE", "FILE_COMMENT").
      b) endpoint: str - Destination HTTP pipeline network path that will process the incoming payload.
      c) passcode: str - Custom verification secret verifying transmission reliability.
      d) team_id: str - Target team identifier controlling the context window.
      e) cred_key: str (default: "figma") - Internal configuration file lookup key index.
    - Returns: ToolResult outlining registration details along status maps.
    - How to call: FigmaTool.create_webhook(event_type="FILE_UPDATE", endpoint="https://api.mybot.dev/figma-hooks", passcode="secret_pass", team_id="5544332211")

11. list_projects:
    - Purpose: Resolves higher-level workspace groupings across managed organizational tiers.
    - Arguments:
      a) team_id: str - Target team alphanumeric identification marker.
      b) cred_key: str (default: "figma") - Storage indexing mapping configuration token.
    - Returns: ToolResult outlining the team's project folders.
    - How to call: FigmaTool.list_projects(team_id="5544332211")

12. get_team_components:
    - Purpose: Audits design library component definitions shared across global corporate workspaces.
    - Arguments:
      a) team_id: str - Core team container tracking index mapping value.
      b) cred_key: str (default: "figma") - Account lookups parameters token configuration identifier.
    - Returns: ToolResult packaging shared cross-project component dictionaries.
    - How to call: FigmaTool.get_team_components(team_id="5544332211")

13. get_versions:
    - Purpose: Tracks structural file evolution timelines or isolates milestone versions for rollback comparisons.
    - Arguments:
      a) file_key: str - Managed workspace sheet code locator.
      b) cred_key: str (default: "figma") - Default verification access lookup key context.
    - Returns: ToolResult aggregating structural timestamp changes and metadata mappings.
    - How to call: FigmaTool.get_versions(file_key="abcd1234")
    """)

    _BASE = "https://api.figma.com/v1"

    @staticmethod
    def _headers(cred_key: str = "figma") -> dict:
        token = CredStore.load(cred_key).get("token", "")
        if not token:
            raise ValueError("No Figma token. Add it in Settings → Credentials (key: 'figma', field: 'token').")
        return {"X-Figma-Token": token}

    @staticmethod
    def _get(path: str, cred_key: str = "figma") -> dict:
        import requests
        r = requests.get(
            f"{FigmaTool._BASE}{path}",
            headers=FigmaTool._headers(cred_key),
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    @staticmethod
    def _post(path: str, payload: dict, cred_key: str = "figma") -> dict:
        import requests
        r = requests.post(
            f"{FigmaTool._BASE}{path}",
            headers={**FigmaTool._headers(cred_key), "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    # ── file ──────────────────────────────────────────────────────────────────
    @staticmethod
    def get_file(file_key: str, cred_key: str = "figma") -> ToolResult:
        try:
            data = FigmaTool._get(f"/files/{file_key}", cred_key)
            return ToolResult(True, f"✓ Fetched file: {data.get('name', file_key)}", data)
        except Exception as e:
            return ToolResult(False, f"✗ Figma get_file failed: {e}")

    @staticmethod
    def get_node(file_key: str, node_id: str, cred_key: str = "figma") -> ToolResult:
        try:
            data = FigmaTool._get(f"/files/{file_key}/nodes?ids={node_id}", cred_key)
            return ToolResult(True, f"✓ Fetched node {node_id}", data)
        except Exception as e:
            return ToolResult(False, f"✗ Figma get_node failed: {e}")

    @staticmethod
    def list_files(project_id: str, cred_key: str = "figma") -> ToolResult:
        try:
            data = FigmaTool._get(f"/projects/{project_id}/files", cred_key)
            files = data.get("files", [])
            return ToolResult(True, f"✓ {len(files)} files in project", files)
        except Exception as e:
            return ToolResult(False, f"✗ Figma list_files failed: {e}")

    @staticmethod
    def export_asset(
        file_key: str,
        node_id: str,
        format: str = "PNG",
        scale: float = 2.0,
        output_path: str = "figma_asset.png",
        cred_key: str = "figma",
    ) -> ToolResult:
        try:
            import requests
            data = FigmaTool._get(
                f"/images/{file_key}?ids={node_id}&format={format.upper()}&scale={scale}",
                cred_key,
            )
            images = data.get("images", {})
            url = images.get(node_id)
            if not url:
                return ToolResult(False, "✗ No image URL returned by Figma.")
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_bytes(r.content)
            return ToolResult(True, f"✓ Exported asset to {output_path}")
        except Exception as e:
            return ToolResult(False, f"✗ Figma export_asset failed: {e}")

    @staticmethod
    def export_all_assets(
        file_key: str,
        output_folder: str,
        format: str = "PNG",
        cred_key: str = "figma",
    ) -> ToolResult:
        try:
            import requests
            # Get all top-level frames/components
            file_data = FigmaTool._get(f"/files/{file_key}", cred_key)
            pages = file_data.get("document", {}).get("children", [])
            node_ids = []
            for page in pages:
                for child in page.get("children", []):
                    node_ids.append(child["id"])
            if not node_ids:
                return ToolResult(False, "✗ No exportable nodes found.")
            ids_str = ",".join(node_ids[:50])  # Figma limit
            img_data = FigmaTool._get(
                f"/images/{file_key}?ids={ids_str}&format={format.upper()}&scale=2",
                cred_key,
            )
            images = img_data.get("images", {})
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            count = 0
            for nid, url in images.items():
                if not url:
                    continue
                r = requests.get(url, timeout=60)
                r.raise_for_status()
                safe_name = nid.replace(":", "_").replace(";", "_")
                out = Path(output_folder) / f"{safe_name}.{format.lower()}"
                out.write_bytes(r.content)
                count += 1
            return ToolResult(True, f"✓ Exported {count} assets to {output_folder}")
        except Exception as e:
            return ToolResult(False, f"✗ Figma export_all_assets failed: {e}")

    @staticmethod
    def get_components(file_key: str, cred_key: str = "figma") -> ToolResult:
        try:
            data = FigmaTool._get(f"/files/{file_key}/components", cred_key)
            comps = data.get("meta", {}).get("components", [])
            return ToolResult(True, f"✓ {len(comps)} components", comps)
        except Exception as e:
            return ToolResult(False, f"✗ Figma get_components failed: {e}")

    @staticmethod
    def get_styles(file_key: str, cred_key: str = "figma") -> ToolResult:
        try:
            data = FigmaTool._get(f"/files/{file_key}/styles", cred_key)
            styles = data.get("meta", {}).get("styles", [])
            return ToolResult(True, f"✓ {len(styles)} styles", styles)
        except Exception as e:
            return ToolResult(False, f"✗ Figma get_styles failed: {e}")

    @staticmethod
    def get_comments(file_key: str, cred_key: str = "figma") -> ToolResult:
        try:
            data = FigmaTool._get(f"/files/{file_key}/comments", cred_key)
            comments = data.get("comments", [])
            return ToolResult(True, f"✓ {len(comments)} comments", comments)
        except Exception as e:
            return ToolResult(False, f"✗ Figma get_comments failed: {e}")

    @staticmethod
    def post_comment(
        file_key: str,
        message: str,
        x: float = 0,
        y: float = 0,
        node_id: Optional[str] = None,
        cred_key: str = "figma",
    ) -> ToolResult:
        try:
            payload: dict = {"message": message, "client_meta": {"x": x, "y": y}}
            if node_id:
                payload["client_meta"]["node_id"] = node_id
            data = FigmaTool._post(f"/files/{file_key}/comments", payload, cred_key)
            return ToolResult(True, f"✓ Comment posted (id={data.get('id')})", data)
        except Exception as e:
            return ToolResult(False, f"✗ Figma post_comment failed: {e}")

    @staticmethod
    def create_webhook(
        event_type: str,
        endpoint: str,
        passcode: str,
        team_id: str,
        cred_key: str = "figma",
    ) -> ToolResult:
        try:
            payload = {
                "event_type": event_type,
                "team_id": team_id,
                "endpoint": endpoint,
                "passcode": passcode,
            }
            data = FigmaTool._post("/webhooks/v2", payload, cred_key)
            return ToolResult(True, f"✓ Webhook created (id={data.get('id')})", data)
        except Exception as e:
            return ToolResult(False, f"✗ Figma create_webhook failed: {e}")

    @staticmethod
    def list_projects(team_id: str, cred_key: str = "figma") -> ToolResult:
        try:
            data = FigmaTool._get(f"/teams/{team_id}/projects", cred_key)
            projects = data.get("projects", [])
            return ToolResult(True, f"✓ {len(projects)} projects", projects)
        except Exception as e:
            return ToolResult(False, f"✗ Figma list_projects failed: {e}")

    @staticmethod
    def get_team_components(team_id: str, cred_key: str = "figma") -> ToolResult:
        try:
            data = FigmaTool._get(f"/teams/{team_id}/components", cred_key)
            comps = data.get("meta", {}).get("components", [])
            return ToolResult(True, f"✓ {len(comps)} team components", comps)
        except Exception as e:
            return ToolResult(False, f"✗ Figma get_team_components failed: {e}")

    @staticmethod
    def get_versions(file_key: str, cred_key: str = "figma") -> ToolResult:
        try:
            data = FigmaTool._get(f"/files/{file_key}/versions", cred_key)
            versions = data.get("versions", [])
            return ToolResult(True, f"✓ {len(versions)} versions", versions)
        except Exception as e:
            return ToolResult(False, f"✗ Figma get_versions failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. BlenderTool
# ─────────────────────────────────────────────────────────────────────────────

class BlenderTool:
    name = "blender"
    description = (
        "Blender 3D automation via subprocess: render images/animations, "
        "import/export OBJ/FBX/glTF, apply materials, batch render, turntable video."
    )
    use = (
           """
Name of Tool:- BlenderTool,

Purpose of Tool:- 
The BlenderTool enables powerful automation of Blender 3D software through headless subprocess execution. 
It supports rendering still images and animations, importing/exporting common 3D formats (OBJ, FBX, glTF), applying materials, batch rendering multiple files, format conversion, and creating professional turntable videos. 
It dynamically locates the Blender executable and uses temporary Python scripts passed to Blender's `--python` flag in background mode. 
This tool is essential for 3D asset pipelines, automated visualization, batch processing, product render farms, and agentic 3D content generation workflows.

Methods:-
- _blender_exe: Internal helper to locate the Blender executable.
- _run_blender: Internal helper to execute Blender with a temporary Python script.
- render_image: Renders a single frame from a .blend file as an image.
- render_animation: Renders a full animation sequence from a .blend file.
- import_obj: Imports an OBJ file into a new or existing .blend file.
- import_fbx: Imports an FBX file into a .blend file.
- export_obj: Exports objects from a .blend file to OBJ format.
- export_fbx: Exports objects from a .blend file to FBX format.
- export_gltf: Exports objects from a .blend file to glTF/GLB format.
- convert_format: Converts between supported 3D file formats.
- apply_material: Applies a Principled BSDF material to a named object.
- batch_render: Renders multiple .blend files in batch.
- create_turntable_video: Creates a 360-degree turntable animation video of an object.

How to use Tool Methods:-

1. _blender_exe (Internal Helper):
   - Purpose: Automatically detects the Blender executable on different operating systems and installation paths.
   - Note: Internal method. Raises FileNotFoundError if Blender is not installed or not in PATH.

2. _run_blender (Internal Helper):
   - Purpose: Runs Blender in background mode with a dynamically generated Python script.
   - Arguments:
     a) blend_file: str or None - Path to .blend file (None for empty scene).
     b) script: str - Python code to execute inside Blender.
     c) extra_args: list (optional) - Additional command-line arguments.
   - Note: Internal method used by all public operations.

3. render_image:
   - Purpose: Renders a single frame from a Blender scene to an image file.
   - Arguments:
     a) blend_file: str - Path to .blend file.
     b) output: str (default: "render.png") - Output image path.
     c) frame: int (default: 1) - Frame number to render.
     d) resolution: tuple (default: (1920, 1080)) - (width, height).
     e) samples: int (default: 128) - Cycles render samples.
     f) engine: str (default: "CYCLES") - "CYCLES" or "BLENDER_EEVEE".
   - How to call: BlenderTool.render_image(blend_file="scene.blend", output="output.png", resolution=(3840, 2160))

4. render_animation:
   - Purpose: Renders a full animation sequence as a series of PNG frames.
   - Arguments:
     a) blend_file: str
     b) output_folder: str - Folder to save frame_####.png files.
     c) start: int (default: 1)
     d) end: int (default: 250)
     e) fps: int (default: 24)
     f) resolution: tuple (default: (1920, 1080))
   - How to call: BlenderTool.render_animation(blend_file="anim.blend", output_folder="frames", start=1, end=120)

5. import_obj:
   - Purpose: Imports an OBJ file into Blender and saves as .blend.
   - Arguments:
     a) blend_file: str or None - Existing .blend (None = new file).
     b) obj_path: str - Path to OBJ file.
     c) output_blend: str - Path to save resulting .blend file.
   - How to call: BlenderTool.import_obj(blend_file=None, obj_path="model.obj", output_blend="imported.blend")

6. import_fbx:
   - Purpose: Imports an FBX file (similar to import_obj).
   - Arguments: blend_file, fbx_path, output_blend.
   - How to call: BlenderTool.import_fbx(blend_file=None, fbx_path="model.fbx", output_blend="imported.blend")

7. export_obj:
   - Purpose: Exports selected or all objects from a .blend file to OBJ.
   - Arguments:
     a) blend_file: str
     b) output_obj: str
     c) objects: list (optional) - Specific object names to export.
   - How to call: BlenderTool.export_obj(blend_file="scene.blend", output_obj="export.obj")

8. export_fbx / export_gltf:
   - Similar to export_obj but for FBX and glTF/GLB formats.
   - How to call: BlenderTool.export_gltf(blend_file="scene.blend", output="model.glb", format="GLB")

9. convert_format:
   - Purpose: Converts between supported 3D formats (OBJ, FBX, STL, glTF/GLB) using Blender as a converter.
   - Arguments:
     a) input: str - Input file path.
     b) output: str - Output file path.
     c) format: str - Target format ("obj", "fbx", "stl", "glb", "gltf").
   - How to call: BlenderTool.convert_format(input="model.obj", output="model.glb", format="glb")

10. apply_material:
    - Purpose: Applies a Principled BSDF material with specified properties to a named object.
    - Arguments:
      a) blend_file: str
      b) object_name: str
      c) material_props: dict - Keys like "base_color", "metallic", "roughness".
      d) output_blend: str
    - How to call: BlenderTool.apply_material(blend_file="scene.blend", object_name="Cube", material_props={"base_color": [1.0, 0.0, 0.0, 1.0], "metallic": 0.8}, output_blend="updated.blend")

11. batch_render:
    - Purpose: Renders multiple .blend files with consistent settings.
    - Arguments:
      a) blend_files: list - List of .blend paths.
      b) output_folder: str
      c) settings: dict (optional) - Render engine, samples, resolution, etc.
    - How to call: BlenderTool.batch_render(blend_files=["file1.blend", "file2.blend"], output_folder="renders/")

12. create_turntable_video:
    - Purpose: Creates a professional 360-degree turntable animation video of a specific object.
    - Arguments:
      a) blend_file: str
      b) object_name: str - Object to rotate around.
      c) output: str - Output video path (e.g., "turntable.mp4").
      d) frames: int (default: 72) - Number of frames for full rotation.
      e) resolution: tuple (default: (1920, 1080))
    - How to call: BlenderTool.create_turntable_video(blend_file="model.blend", object_name="Product", output="turntable.mp4", frames=120)
""")

    @staticmethod
    def _blender_exe() -> str:
        for candidate in ["blender", "/usr/bin/blender", "/Applications/Blender.app/Contents/MacOS/Blender",
                          r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"]:
            if shutil.which(candidate):
                return candidate
        raise FileNotFoundError(
            "Blender executable not found. Install Blender and ensure it is on PATH."
        )

    @staticmethod
    def _run_blender(blend_file: Optional[str], script: str, extra_args: List[str] = None) -> subprocess.CompletedProcess:
        exe = BlenderTool._blender_exe()
        tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8")
        tmp.write(script)
        tmp.close()
        cmd = [exe, "--background"]
        if blend_file:
            cmd.append(blend_file)
        cmd += ["--python", tmp.name]
        if extra_args:
            cmd += extra_args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return result
        finally:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass

    @staticmethod
    def render_image(
        blend_file: str,
        output: str = "render.png",
        frame: int = 1,
        resolution: tuple = (1920, 1080),
        samples: int = 128,
        engine: str = "CYCLES",
    ) -> ToolResult:
        try:
            script = f"""
import bpy
bpy.context.scene.render.engine = '{engine}'
bpy.context.scene.render.resolution_x = {resolution[0]}
bpy.context.scene.render.resolution_y = {resolution[1]}
bpy.context.scene.render.filepath = r'{output}'
bpy.context.scene.frame_set({frame})
if '{engine}' == 'CYCLES':
    bpy.context.scene.cycles.samples = {samples}
bpy.ops.render.render(write_still=True)
print("RENDER_DONE")
"""
            r = BlenderTool._run_blender(blend_file, script)
            if "RENDER_DONE" in r.stdout:
                return ToolResult(True, f"✓ Rendered frame {frame} to {output}")
            return ToolResult(False, f"✗ Render failed: {r.stderr[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool render_image failed: {e}")

    @staticmethod
    def render_animation(
        blend_file: str,
        output_folder: str,
        start: int = 1,
        end: int = 250,
        fps: int = 24,
        resolution: tuple = (1920, 1080),
    ) -> ToolResult:
        try:
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            out_pattern = str(Path(output_folder) / "frame_####.png")
            script = f"""
import bpy
bpy.context.scene.render.filepath = r'{out_pattern}'
bpy.context.scene.render.resolution_x = {resolution[0]}
bpy.context.scene.render.resolution_y = {resolution[1]}
bpy.context.scene.render.fps = {fps}
bpy.context.scene.frame_start = {start}
bpy.context.scene.frame_end = {end}
bpy.ops.render.render(animation=True)
print("ANIM_DONE")
"""
            r = BlenderTool._run_blender(blend_file, script)
            if "ANIM_DONE" in r.stdout:
                return ToolResult(True, f"✓ Animation rendered ({start}-{end}) to {output_folder}")
            return ToolResult(False, f"✗ Animation render failed: {r.stderr[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool render_animation failed: {e}")

    @staticmethod
    def import_obj(
        blend_file: Optional[str],
        obj_path: str,
        output_blend: str,
    ) -> ToolResult:
        try:
            script = f"""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.obj(filepath=r'{obj_path}')
bpy.ops.wm.save_as_mainfile(filepath=r'{output_blend}')
print("IMPORT_OBJ_DONE")
"""
            r = BlenderTool._run_blender(blend_file, script)
            if "IMPORT_OBJ_DONE" in r.stdout:
                return ToolResult(True, f"✓ OBJ imported and saved to {output_blend}")
            return ToolResult(False, f"✗ OBJ import failed: {r.stderr[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool import_obj failed: {e}")

    @staticmethod
    def import_fbx(
        blend_file: Optional[str],
        fbx_path: str,
        output_blend: str,
    ) -> ToolResult:
        try:
            script = f"""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=r'{fbx_path}')
bpy.ops.wm.save_as_mainfile(filepath=r'{output_blend}')
print("IMPORT_FBX_DONE")
"""
            r = BlenderTool._run_blender(blend_file, script)
            if "IMPORT_FBX_DONE" in r.stdout:
                return ToolResult(True, f"✓ FBX imported to {output_blend}")
            return ToolResult(False, f"✗ FBX import failed: {r.stderr[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool import_fbx failed: {e}")

    @staticmethod
    def export_obj(
        blend_file: str,
        output_obj: str,
        objects: Optional[List[str]] = None,
    ) -> ToolResult:
        try:
            select_code = ""
            if objects:
                obj_list = json.dumps(objects)
                select_code = f"""
for obj in bpy.data.objects:
    obj.select_set(obj.name in {obj_list})
"""
            script = f"""
import bpy
{select_code}
bpy.ops.export_scene.obj(filepath=r'{output_obj}', use_selection={bool(objects)})
print("EXPORT_OBJ_DONE")
"""
            r = BlenderTool._run_blender(blend_file, script)
            if "EXPORT_OBJ_DONE" in r.stdout:
                return ToolResult(True, f"✓ Exported OBJ to {output_obj}")
            return ToolResult(False, f"✗ OBJ export failed: {r.stderr[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool export_obj failed: {e}")

    @staticmethod
    def export_fbx(
        blend_file: str,
        output_fbx: str,
        objects: Optional[List[str]] = None,
    ) -> ToolResult:
        try:
            select_code = ""
            if objects:
                obj_list = json.dumps(objects)
                select_code = f"""
for obj in bpy.data.objects:
    obj.select_set(obj.name in {obj_list})
"""
            script = f"""
import bpy
{select_code}
bpy.ops.export_scene.fbx(filepath=r'{output_fbx}', use_selection={bool(objects)})
print("EXPORT_FBX_DONE")
"""
            r = BlenderTool._run_blender(blend_file, script)
            if "EXPORT_FBX_DONE" in r.stdout:
                return ToolResult(True, f"✓ Exported FBX to {output_fbx}")
            return ToolResult(False, f"✗ FBX export failed: {r.stderr[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool export_fbx failed: {e}")

    @staticmethod
    def export_gltf(
        blend_file: str,
        output: str,
        objects: Optional[List[str]] = None,
        format: str = "GLB",
    ) -> ToolResult:
        try:
            select_code = ""
            if objects:
                obj_list = json.dumps(objects)
                select_code = f"""
for obj in bpy.data.objects:
    obj.select_set(obj.name in {obj_list})
"""
            script = f"""
import bpy
{select_code}
bpy.ops.export_scene.gltf(
    filepath=r'{output}',
    export_format='{format.upper()}',
    use_selection={bool(objects)}
)
print("EXPORT_GLTF_DONE")
"""
            r = BlenderTool._run_blender(blend_file, script)
            if "EXPORT_GLTF_DONE" in r.stdout:
                return ToolResult(True, f"✓ Exported glTF ({format}) to {output}")
            return ToolResult(False, f"✗ glTF export failed: {r.stderr[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool export_gltf failed: {e}")

    @staticmethod
    def convert_format(
        input: str,
        output: str,
        format: str,
    ) -> ToolResult:
        try:
            ext = Path(input).suffix.lower()
            import_ops = {
                ".obj": "bpy.ops.import_scene.obj(filepath=r'" + input + "')",
                ".fbx": "bpy.ops.import_scene.fbx(filepath=r'" + input + "')",
                ".stl": "bpy.ops.import_mesh.stl(filepath=r'" + input + "')",
                ".glb": "bpy.ops.import_scene.gltf(filepath=r'" + input + "')",
                ".gltf": "bpy.ops.import_scene.gltf(filepath=r'" + input + "')",
            }
            export_ops = {
                "obj":  f"bpy.ops.export_scene.obj(filepath=r'{output}')",
                "fbx":  f"bpy.ops.export_scene.fbx(filepath=r'{output}')",
                "stl":  f"bpy.ops.export_mesh.stl(filepath=r'{output}')",
                "glb":  f"bpy.ops.export_scene.gltf(filepath=r'{output}', export_format='GLB')",
                "gltf": f"bpy.ops.export_scene.gltf(filepath=r'{output}', export_format='GLTF_SEPARATE')",
            }
            imp = import_ops.get(ext)
            exp = export_ops.get(format.lower())
            if not imp:
                return ToolResult(False, f"✗ Unsupported input format: {ext}")
            if not exp:
                return ToolResult(False, f"✗ Unsupported output format: {format}")
            script = f"""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
{imp}
{exp}
print("CONVERT_DONE")
"""
            r = BlenderTool._run_blender(None, script)
            if "CONVERT_DONE" in r.stdout:
                return ToolResult(True, f"✓ Converted {input} → {output}")
            return ToolResult(False, f"✗ Conversion failed: {r.stderr[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool convert_format failed: {e}")

    @staticmethod
    def apply_material(
        blend_file: str,
        object_name: str,
        material_props: dict,
        output_blend: str,
    ) -> ToolResult:
        try:
            base_color = material_props.get("base_color", [0.8, 0.8, 0.8, 1.0])
            metallic    = material_props.get("metallic", 0.0)
            roughness   = material_props.get("roughness", 0.5)
            script = f"""
import bpy
obj = bpy.data.objects.get('{object_name}')
if obj is None:
    raise ValueError("Object '{object_name}' not found")
mat = bpy.data.materials.new(name="NPMAgentMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = {base_color}
    bsdf.inputs['Metallic'].default_value   = {metallic}
    bsdf.inputs['Roughness'].default_value  = {roughness}
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)
bpy.ops.wm.save_as_mainfile(filepath=r'{output_blend}')
print("MATERIAL_DONE")
"""
            r = BlenderTool._run_blender(blend_file, script)
            if "MATERIAL_DONE" in r.stdout:
                return ToolResult(True, f"✓ Material applied to '{object_name}', saved to {output_blend}")
            return ToolResult(False, f"✗ apply_material failed: {r.stderr[-500:]}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool apply_material failed: {e}")

    @staticmethod
    def batch_render(
        blend_files: List[str],
        output_folder: str,
        settings: Optional[dict] = None,
    ) -> ToolResult:
        try:
            settings = settings or {}
            engine     = settings.get("engine", "CYCLES")
            samples    = settings.get("samples", 64)
            resolution = settings.get("resolution", (1920, 1080))
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            results = []
            for bf in blend_files:
                out = str(Path(output_folder) / (Path(bf).stem + "_render.png"))
                res = BlenderTool.render_image(bf, out,
                                               resolution=resolution,
                                               samples=samples,
                                               engine=engine)
                results.append({"file": bf, "success": res.success, "msg": res.output})
            done = sum(1 for r in results if r["success"])
            return ToolResult(True, f"✓ Batch rendered {done}/{len(blend_files)} files", results)
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool batch_render failed: {e}")

    @staticmethod
    def create_turntable_video(
        blend_file: str,
        object_name: str,
        output: str,
        frames: int = 72,
        resolution: tuple = (1920, 1080),
    ) -> ToolResult:
        try:
            tmp_frames = tempfile.mkdtemp()
            script = f"""
import bpy, math
scene = bpy.context.scene
scene.render.resolution_x = {resolution[0]}
scene.render.resolution_y = {resolution[1]}
scene.frame_start = 1
scene.frame_end   = {frames}
obj = bpy.data.objects.get('{object_name}')
if obj is None:
    raise ValueError("Object not found: {object_name}")
# Create a rotation keyframe approach using an empty parent
bpy.ops.object.empty_add(type='PLAIN_AXES', location=obj.location)
pivot = bpy.context.active_object
pivot.name = "_TurnPivot"
orig_parent = obj.parent
obj.parent = pivot
for frame in range(1, {frames}+1):
    scene.frame_set(frame)
    angle = (frame / {frames}) * 2 * math.pi
    pivot.rotation_euler[2] = angle
    pivot.keyframe_insert(data_path='rotation_euler', index=2)
scene.render.filepath = r'{tmp_frames}/frame_####.png'
bpy.ops.render.render(animation=True)
print("TURNTABLE_FRAMES_DONE")
"""
            r = BlenderTool._run_blender(blend_file, script)
            if "TURNTABLE_FRAMES_DONE" not in r.stdout:
                return ToolResult(False, f"✗ Turntable frames failed: {r.stderr[-500:]}")
            # Compile frames to video using ffmpeg
            ffmpeg = shutil.which("ffmpeg")
            if not ffmpeg:
                return ToolResult(True, f"✓ Turntable frames in {tmp_frames} (ffmpeg not found — skipped video encoding)")
            ffcmd = [
                ffmpeg, "-y",
                "-framerate", "24",
                "-i", str(Path(tmp_frames) / "frame_%04d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                output,
            ]
            subprocess.run(ffcmd, check=True, capture_output=True, timeout=300)
            shutil.rmtree(tmp_frames, ignore_errors=True)
            return ToolResult(True, f"✓ Turntable video saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ BlenderTool create_turntable_video failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. SVGTool
# ─────────────────────────────────────────────────────────────────────────────

class SVGTool:
    name = "svg"
    description = (
        "SVG generation, manipulation, animation, conversion (PNG/PDF), "
        "optimization, icon sets, bitmap tracing, and merging."
    )
    use = (
           """
Name of Tool:- SVGTool,

Purpose of Tool:- 
The SVGTool provides a comprehensive suite for creating, manipulating, optimizing, converting, and animating Scalable Vector Graphics (SVG). 
It supports programmatic SVG generation, element addition, format conversion (PNG/PDF), optimization, bitmap tracing, icon generation, animation via SMIL, batch processing, and merging multiple SVGs. 
It uses libraries like svgwrite, cairosvg, and potrace (when available) for high-quality vector operations. 
This tool is ideal for dynamic icon generation, data visualization, diagram automation, asset pipelines, and agentic graphic design workflows.

Methods:-
- create_svg: Creates a new SVG file from a list of element definitions.
- add_element: Adds a new graphical element to an existing SVG file.
- convert_to_png: Converts an SVG to a raster PNG image.
- convert_to_pdf: Converts an SVG to PDF.
- optimize: Optimizes SVG by removing metadata and minifying whitespace.
- animate: Adds SMIL animation to a specific element in an SVG.
- batch_convert: Batch converts multiple SVG files to PNG or PDF.
- create_icon_set: Generates a set of simple placeholder icons.
- trace_bitmap: Traces a bitmap image to vector SVG using potrace.
- merge_svgs: Merges multiple SVGs into a single SVG (horizontal or vertical layout).

How to use Tool Methods:-

1. create_svg:
   - Purpose: Generates a new SVG file from a structured list of elements (rect, circle, text, path, etc.).
   - Arguments:
     a) width: int - Canvas width in pixels.
     b) height: int - Canvas height in pixels.
     c) elements: List[dict] - List of element dictionaries with "type" and attributes.
     d) output: str (default: "output.svg") - Output file path.
   - How to call: 
     SVGTool.create_svg(
         width=800, height=600,
         elements=[{"type": "rect", "x": 10, "y": 10, "width": 100, "height": 100, "fill": "red"}],
         output="diagram.svg"
     )

2. add_element:
   - Purpose: Appends a new SVG element to an existing SVG file using XML manipulation.
   - Arguments:
     a) svg_file: str - Path to existing SVG.
     b) element_type: str - SVG element type (rect, circle, text, path, etc.).
     c) attrs: dict - Attributes for the element (x, y, width, fill, etc.).
     d) output: str - Path for the modified SVG.
   - How to call: SVGTool.add_element(svg_file="base.svg", element_type="circle", attrs={"cx": 100, "cy": 100, "r": 50, "fill": "blue"}, output="updated.svg")

3. convert_to_png:
   - Purpose: Renders an SVG to a high-quality PNG raster image.
   - Arguments:
     a) svg: str - Path or URL to SVG file.
     b) output: str (default: "output.png")
     c) width: int (optional) - Output width.
     d) height: int (optional) - Output height.
     e) dpi: int (default: 96)
   - How to call: SVGTool.convert_to_png(svg="design.svg", output="design.png", width=1200)

4. convert_to_pdf:
   - Purpose: Converts SVG to vector PDF.
   - Arguments: svg, output (default: "output.pdf")
   - How to call: SVGTool.convert_to_pdf(svg="design.svg", output="design.pdf")

5. optimize:
   - Purpose: Cleans and minifies an SVG file for smaller file size and better performance.
   - Arguments:
     a) svg: str - Input SVG path.
     b) output: str - Output path.
     c) remove_metadata: bool (default: True)
     d) minify: bool (default: True)
   - How to call: SVGTool.optimize(svg="large.svg", output="optimized.svg")

6. animate:
   - Purpose: Adds SMIL-based animation to a specific element by ID.
   - Arguments:
     a) svg: str - Input SVG path.
     b) element_id: str - ID of the element to animate.
     c) property: str - Attribute to animate (e.g., "x", "opacity", "transform").
     d) from_val: str - Starting value.
     e) to_val: str - Ending value.
     f) duration: float (default: 1.0) - Duration in seconds.
     g) output: str - Output path.
   - How to call: SVGTool.animate(svg="icon.svg", element_id="circle1", property="cx", from_val="50", to_val="200", duration=2.0)

7. batch_convert:
   - Purpose: Converts all SVGs in a folder to PNG or PDF.
   - Arguments:
     a) folder: str - Input folder containing SVGs.
     b) output_folder: str - Destination folder.
     c) target_format: str (default: "png") - "png" or "pdf".
   - How to call: SVGTool.batch_convert(folder="icons/", output_folder="pngs/", target_format="png")

8. create_icon_set:
   - Purpose: Generates a set of simple placeholder SVG icons with text labels.
   - Arguments:
     a) names: List[str] - List of icon names.
     b) style: str (default: "outline") - "outline" or filled.
     c) output_folder: str (default: "icons")
   - How to call: SVGTool.create_icon_set(names=["home", "user", "settings"], style="outline")

9. trace_bitmap:
   - Purpose: Converts a bitmap image to vector SVG using potrace (requires potrace installed).
   - Arguments:
     a) image: str - Input image path.
     b) output: str - Output SVG path.
     c) color: str (default: "black")
     d) threshold: int (default: 128) - Binarization threshold.
   - How to call: SVGTool.trace_bitmap(image="logo.png", output="logo_vector.svg")

10. merge_svgs:
    - Purpose: Combines multiple SVGs into a single SVG file (horizontal or vertical layout).
    - Arguments:
      a) svgs: List[str] - List of input SVG paths.
      b) output: str - Output path.
      c) layout: str (default: "horizontal") - "horizontal" or "vertical".
      d) spacing: int (default: 10) - Spacing between SVGs in pixels.
    - How to call: SVGTool.merge_svgs(svgs=["icon1.svg", "icon2.svg"], output="combined.svg", layout="horizontal")
""")

    @staticmethod
    def create_svg(
        width: int,
        height: int,
        elements: List[dict],
        output: str = "output.svg",
    ) -> ToolResult:
        try:
            import svgwrite
            dwg = svgwrite.Drawing(output, size=(width, height))
            for el in elements:
                etype = el.get("type", "rect")
                attrs = {k: v for k, v in el.items() if k != "type"}
                if etype == "rect":
                    dwg.add(dwg.rect(**attrs))
                elif etype == "circle":
                    dwg.add(dwg.circle(**attrs))
                elif etype == "ellipse":
                    dwg.add(dwg.ellipse(**attrs))
                elif etype == "line":
                    dwg.add(dwg.line(**attrs))
                elif etype == "text":
                    text_val = attrs.pop("text", "")
                    dwg.add(dwg.text(text_val, **attrs))
                elif etype == "path":
                    dwg.add(dwg.path(**attrs))
                elif etype == "polyline":
                    dwg.add(dwg.polyline(**attrs))
                elif etype == "polygon":
                    dwg.add(dwg.polygon(**attrs))
            dwg.save()
            return ToolResult(True, f"✓ SVG created at {output}")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool create_svg failed: {e}")

    @staticmethod
    def add_element(
        svg_file: str,
        element_type: str,
        attrs: dict,
        output: str,
    ) -> ToolResult:
        try:
            from xml.etree import ElementTree as ET
            ET.register_namespace("", "http://www.w3.org/2000/svg")
            tree = ET.parse(svg_file)
            root = tree.getroot()
            ns = "http://www.w3.org/2000/svg"
            el = ET.SubElement(root, f"{{{ns}}}{element_type}")
            for k, v in attrs.items():
                el.set(k, str(v))
            tree.write(output, xml_declaration=True, encoding="utf-8")
            return ToolResult(True, f"✓ Element '{element_type}' added, saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool add_element failed: {e}")

    @staticmethod
    def convert_to_png(
        svg: str,
        output: str = "output.png",
        width: Optional[int] = None,
        height: Optional[int] = None,
        dpi: int = 96,
    ) -> ToolResult:
        try:
            import cairosvg
            kwargs: dict = {"url": svg, "write_to": output, "dpi": dpi}
            if width:
                kwargs["output_width"] = width
            if height:
                kwargs["output_height"] = height
            cairosvg.svg2png(**kwargs)
            return ToolResult(True, f"✓ SVG converted to PNG at {output}")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool convert_to_png failed: {e}")

    @staticmethod
    def convert_to_pdf(
        svg: str,
        output: str = "output.pdf",
    ) -> ToolResult:
        try:
            import cairosvg
            cairosvg.svg2pdf(url=svg, write_to=output)
            return ToolResult(True, f"✓ SVG converted to PDF at {output}")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool convert_to_pdf failed: {e}")

    @staticmethod
    def optimize(
        svg: str,
        output: str,
        remove_metadata: bool = True,
        minify: bool = True,
    ) -> ToolResult:
        try:
            from xml.etree import ElementTree as ET
            content = Path(svg).read_text(encoding="utf-8")
            # Remove metadata tags
            if remove_metadata:
                content = re.sub(r'<metadata[^>]*>.*?</metadata>', '', content, flags=re.DOTALL)
                content = re.sub(r'<\?xml[^>]*\?>', '', content)
            if minify:
                content = re.sub(r'\s+', ' ', content)
                content = re.sub(r'>\s+<', '><', content)
                content = content.strip()
            Path(output).write_text(content, encoding="utf-8")
            orig_size = Path(svg).stat().st_size
            new_size  = Path(output).stat().st_size
            saved_pct = round((1 - new_size / orig_size) * 100, 1) if orig_size else 0
            return ToolResult(True, f"✓ SVG optimized → {output} ({saved_pct}% smaller)")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool optimize failed: {e}")

    @staticmethod
    def animate(
        svg: str,
        element_id: str,
        property: str,
        from_val: str,
        to_val: str,
        duration: float = 1.0,
        output: str = "animated.svg",
    ) -> ToolResult:
        try:
            from xml.etree import ElementTree as ET
            ET.register_namespace("", "http://www.w3.org/2000/svg")
            tree = ET.parse(svg)
            root = tree.getroot()
            ns = "http://www.w3.org/2000/svg"

            def find_by_id(node, target_id):
                if node.get("id") == target_id:
                    return node
                for child in node:
                    result = find_by_id(child, target_id)
                    if result is not None:
                        return result
                return None

            target = find_by_id(root, element_id)
            if target is None:
                return ToolResult(False, f"✗ Element with id='{element_id}' not found.")
            anim = ET.SubElement(target, f"{{{ns}}}animate")
            anim.set("attributeName", property)
            anim.set("from", str(from_val))
            anim.set("to", str(to_val))
            anim.set("dur", f"{duration}s")
            anim.set("repeatCount", "indefinite")
            tree.write(output, xml_declaration=True, encoding="utf-8")
            return ToolResult(True, f"✓ Animation added to '{element_id}', saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool animate failed: {e}")

    @staticmethod
    def batch_convert(
        folder: str,
        output_folder: str,
        target_format: str = "png",
    ) -> ToolResult:
        try:
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            count = 0
            for svg_path in Path(folder).glob("*.svg"):
                out = Path(output_folder) / svg_path.with_suffix(f".{target_format.lower()}").name
                if target_format.lower() == "png":
                    SVGTool.convert_to_png(str(svg_path), str(out))
                elif target_format.lower() == "pdf":
                    SVGTool.convert_to_pdf(str(svg_path), str(out))
                count += 1
            return ToolResult(True, f"✓ Converted {count} SVGs to {target_format} in {output_folder}")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool batch_convert failed: {e}")

    @staticmethod
    def create_icon_set(
        names: List[str],
        style: str = "outline",
        output_folder: str = "icons",
    ) -> ToolResult:
        try:
            import svgwrite
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            stroke_color = "#333333" if style == "outline" else "#333333"
            fill_color   = "none" if style == "outline" else "#333333"
            count = 0
            for name in names:
                dwg = svgwrite.Drawing(str(Path(output_folder) / f"{name}.svg"), size=(24, 24))
                # Generic placeholder shape — a rounded square
                dwg.add(dwg.rect(
                    insert=(2, 2), size=(20, 20), rx=3, ry=3,
                    stroke=stroke_color, fill=fill_color, stroke_width=2,
                ))
                # Add first letter as text
                dwg.add(dwg.text(
                    name[0].upper(),
                    insert=(8, 16), font_size=12,
                    fill=stroke_color, font_family="sans-serif",
                ))
                dwg.save()
                count += 1
            return ToolResult(True, f"✓ Created {count} icons in {output_folder}")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool create_icon_set failed: {e}")

    @staticmethod
    def trace_bitmap(
        image: str,
        output: str,
        color: str = "black",
        threshold: int = 128,
    ) -> ToolResult:
        try:
            potrace = shutil.which("potrace")
            mkbitmap = shutil.which("mkbitmap")
            if not potrace:
                return ToolResult(False, "✗ potrace not found. Install potrace (apt/brew/choco).")
            from PIL import Image
            img = Image.open(image).convert("L")
            img = img.point(lambda x: 0 if x < threshold else 255, "1")
            bmp_tmp = tempfile.NamedTemporaryFile(suffix=".bmp", delete=False)
            img.save(bmp_tmp.name)
            bmp_tmp.close()
            subprocess.run(
                [potrace, bmp_tmp.name, "-s", "-o", output],
                check=True, capture_output=True, timeout=60,
            )
            os.unlink(bmp_tmp.name)
            return ToolResult(True, f"✓ Bitmap traced to SVG at {output}")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool trace_bitmap failed: {e}")

    @staticmethod
    def merge_svgs(
        svgs: List[str],
        output: str,
        layout: str = "horizontal",
        spacing: int = 10,
    ) -> ToolResult:
        try:
            from xml.etree import ElementTree as ET
            import svgwrite

            widths, heights = [], []
            contents = []
            for s in svgs:
                tree = ET.parse(s)
                root = tree.getroot()
                vb = root.get("viewBox", "")
                w = int(root.get("width", 100))
                h = int(root.get("height", 100))
                if vb:
                    parts = vb.strip().split()
                    if len(parts) == 4:
                        w, h = int(float(parts[2])), int(float(parts[3]))
                widths.append(w)
                heights.append(h)
                contents.append((root, w, h))

            if layout == "horizontal":
                total_w = sum(widths) + spacing * (len(svgs) - 1)
                total_h = max(heights)
            else:
                total_w = max(widths)
                total_h = sum(heights) + spacing * (len(svgs) - 1)

            dwg = svgwrite.Drawing(output, size=(total_w, total_h))
            x_offset, y_offset = 0, 0
            for root, w, h in contents:
                ns = "http://www.w3.org/2000/svg"
                ET.register_namespace("", ns)
                inner = ET.tostring(root, encoding="unicode")
                grp = dwg.add(dwg.g(transform=f"translate({x_offset},{y_offset})"))
                # Embed as raw SVG string inside a foreignObject isn't ideal;
                # use image embed approach via data URI instead
                import cairosvg, base64
                tmp = tempfile.NamedTemporaryFile(suffix=".svg", delete=False, mode="w")
                tmp.write(inner)
                tmp.close()
                png_bytes = cairosvg.svg2png(url=tmp.name)
                os.unlink(tmp.name)
                b64 = base64.b64encode(png_bytes).decode()
                grp.add(dwg.image(
                    href=f"data:image/png;base64,{b64}",
                    insert=(0, 0), size=(w, h),
                ))
                if layout == "horizontal":
                    x_offset += w + spacing
                else:
                    y_offset += h + spacing
            dwg.save()
            return ToolResult(True, f"✓ Merged {len(svgs)} SVGs into {output}")
        except Exception as e:
            return ToolResult(False, f"✗ SVGTool merge_svgs failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. CanvaTool
# ─────────────────────────────────────────────────────────────────────────────

class CanvaTool:
    name = "canva"
    description = (
        "Canva Connect API integration: list/create/export designs, "
        "brand kits, assets and template-based design creation."
    )
    use = (
           """
Name of Tool:- CanvaTool,

Purpose of Tool:- 
The CanvaTool provides integration with the Canva Connect REST API for automated design creation, management, and export. 
It supports listing and retrieving designs, creating new custom-sized designs, exporting designs to high-quality formats (PDF, PNG, etc.), managing brand kits, listing/uploading assets, and generating designs from templates using autofill. 
All operations use authenticated API calls with an access token stored in CredStore. 
This tool is perfect for dynamic graphic generation, marketing asset automation, template-based content creation, brand-consistent design workflows, and agentic visual content production.

Methods:-
- _headers: Internal helper to generate authentication headers.
- _get: Internal helper for GET requests to Canva API.
- _post: Internal helper for POST requests.
- list_designs: Lists all designs in the authenticated account.
- get_design: Retrieves detailed information about a specific design.
- create_design: Creates a new blank custom-sized design.
- export_design: Exports a design to PDF/PNG/etc. with background job polling.
- list_brand_kits: Lists available brand kits.
- get_brand_kit: Retrieves details of a specific brand kit.
- list_assets: Lists assets by type (images, etc.).
- upload_asset: Uploads a local file as a Canva asset.
- create_from_template: Creates a design from a template using autofill replacements and exports it.

How to use Tool Methods:-

1. _headers (Internal Authentication Helper):
   - Purpose: Constructs Bearer token headers for Canva API requests.
   - Arguments: cred_key: str (default: "canva")
   - Credential requirement: CredStore must contain {'access_token': 'your-canva-access-token'}.
   - Note: Internal method used by all API calls.

2. list_designs:
   - Purpose: Retrieves a list of all designs in the account.
   - Arguments: cred_key: str (default: "canva")
   - Returns: List of design objects with IDs, titles, etc.
   - How to call: CanvaTool.list_designs()

3. get_design:
   - Purpose: Fetches complete details of a specific design by ID.
   - Arguments:
     a) design_id: str - Canva design identifier.
     b) cred_key: str (default: "canva").
   - How to call: CanvaTool.get_design(design_id="DAE123456789")

4. create_design:
   - Purpose: Creates a new blank design with custom dimensions and title.
   - Arguments:
     a) name: str - Title of the new design.
     b) width: int (default: 800)
     c) height: int (default: 600)
     d) unit: str (default: "px") - "px", "mm", etc.
     e) cred_key: str (default: "canva").
   - Returns: Design creation response containing the new design ID.
   - How to call: CanvaTool.create_design(name="Social Media Post", width=1080, height=1080)

5. export_design:
   - Purpose: Starts an export job for a design and polls until completion, then downloads the file.
   - Arguments:
     a) design_id: str - ID of the design to export.
     b) output_path: str (default: "design_export.pdf") - Local path to save the exported file.
     c) format: str (default: "pdf") - Supported formats like "pdf", "png", etc.
     d) quality: str (default: "regular")
     e) cred_key: str (default: "canva").
   - How to call: CanvaTool.export_design(design_id="DAE123456789", output_path="final_poster.pdf", format="pdf")

6. list_brand_kits:
   - Purpose: Lists all brand kits available to the user.
   - Arguments: cred_key: str (default: "canva")
   - How to call: CanvaTool.list_brand_kits()

7. get_brand_kit:
   - Purpose: Retrieves detailed information about a specific brand kit.
   - Arguments:
     a) brand_kit_id: str
     b) cred_key: str (default: "canva").
   - How to call: CanvaTool.get_brand_kit(brand_kit_id="BK...")

8. list_assets:
   - Purpose: Lists assets (images, videos, elements, etc.) by type.
   - Arguments:
     a) asset_type: str (default: "image")
     b) cred_key: str (default: "canva").
   - How to call: CanvaTool.list_assets(asset_type="image")

9. upload_asset:
   - Purpose: Uploads a local file (image, video, etc.) to Canva as a reusable asset.
   - Arguments:
     a) file_path: str - Local path to the file.
     b) name: str - Display name for the asset.
     c) cred_key: str (default: "canva").
   - How to call: CanvaTool.upload_asset(file_path="logo.png", name="Company Logo")

10. create_from_template:
    - Purpose: Creates a new design from an existing Canva template using autofill data and exports the result.
    - Arguments:
      a) template_id: str - Canva template ID.
      b) replacements: dict - Dictionary of text replacements for autofill.
      c) output: str - Path to save the exported design.
      d) cred_key: str (default: "canva").
    - How to call: 
      CanvaTool.create_from_template(
          template_id="T-abc123",
          replacements={"title": "Q2 Report", "date": "June 2026"},
          output="generated_report.pdf"
      )
""")

    _BASE = "https://api.canva.com/rest/v1"

    @staticmethod
    def _headers(cred_key: str = "canva") -> dict:
        token = CredStore.load(cred_key).get("access_token", "")
        if not token:
            raise ValueError("No Canva access_token. Add in Settings → Credentials (key: 'canva').")
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    @staticmethod
    def _get(path: str, cred_key: str = "canva") -> dict:
        import requests
        r = requests.get(
            f"{CanvaTool._BASE}{path}",
            headers=CanvaTool._headers(cred_key),
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    @staticmethod
    def _post(path: str, payload: dict, cred_key: str = "canva") -> dict:
        import requests
        r = requests.post(
            f"{CanvaTool._BASE}{path}",
            headers=CanvaTool._headers(cred_key),
            json=payload,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    @staticmethod
    def list_designs(cred_key: str = "canva") -> ToolResult:
        try:
            data = CanvaTool._get("/designs", cred_key)
            designs = data.get("items", [])
            return ToolResult(True, f"✓ {len(designs)} designs", designs)
        except Exception as e:
            return ToolResult(False, f"✗ CanvaTool list_designs failed: {e}")

    @staticmethod
    def get_design(design_id: str, cred_key: str = "canva") -> ToolResult:
        try:
            data = CanvaTool._get(f"/designs/{design_id}", cred_key)
            return ToolResult(True, f"✓ Design fetched: {design_id}", data)
        except Exception as e:
            return ToolResult(False, f"✗ CanvaTool get_design failed: {e}")

    @staticmethod
    def create_design(
        name: str,
        width: int = 800,
        height: int = 600,
        unit: str = "px",
        cred_key: str = "canva",
    ) -> ToolResult:
        try:
            payload = {
                "design_type": {"type": "custom", "width": width, "height": height, "unit": unit},
                "title": name,
            }
            data = CanvaTool._post("/designs", payload, cred_key)
            return ToolResult(True, f"✓ Design created: {data.get('design', {}).get('id', '')}", data)
        except Exception as e:
            return ToolResult(False, f"✗ CanvaTool create_design failed: {e}")

    @staticmethod
    def export_design(
        design_id: str,
        output_path: str = "design_export.pdf",
        format: str = "pdf",
        quality: str = "regular",
        cred_key: str = "canva",
    ) -> ToolResult:
        try:
            import requests, time
            payload = {"design_id": design_id, "format": format.upper(), "quality": quality}
            job_data = CanvaTool._post("/exports", payload, cred_key)
            job_id   = job_data.get("job", {}).get("id", "")
            # Poll for completion
            for _ in range(30):
                status = CanvaTool._get(f"/exports/{job_id}", cred_key)
                job = status.get("job", {})
                if job.get("status") == "success":
                    url = job.get("urls", [None])[0]
                    if url:
                        r = requests.get(url, timeout=120)
                        r.raise_for_status()
                        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                        Path(output_path).write_bytes(r.content)
                        return ToolResult(True, f"✓ Design exported to {output_path}")
                    return ToolResult(False, "✗ Export succeeded but no URL returned.")
                elif job.get("status") == "failed":
                    return ToolResult(False, f"✗ Export job failed: {job}")
                time.sleep(2)
            return ToolResult(False, "✗ Export timed out after 60s.")
        except Exception as e:
            return ToolResult(False, f"✗ CanvaTool export_design failed: {e}")

    @staticmethod
    def list_brand_kits(cred_key: str = "canva") -> ToolResult:
        try:
            data = CanvaTool._get("/brand-kits", cred_key)
            kits = data.get("items", [])
            return ToolResult(True, f"✓ {len(kits)} brand kits", kits)
        except Exception as e:
            return ToolResult(False, f"✗ CanvaTool list_brand_kits failed: {e}")

    @staticmethod
    def get_brand_kit(brand_kit_id: str, cred_key: str = "canva") -> ToolResult:
        try:
            data = CanvaTool._get(f"/brand-kits/{brand_kit_id}", cred_key)
            return ToolResult(True, f"✓ Brand kit fetched: {brand_kit_id}", data)
        except Exception as e:
            return ToolResult(False, f"✗ CanvaTool get_brand_kit failed: {e}")

    @staticmethod
    def list_assets(asset_type: str = "image", cred_key: str = "canva") -> ToolResult:
        try:
            data = CanvaTool._get(f"/assets?type={asset_type}", cred_key)
            assets = data.get("items", [])
            return ToolResult(True, f"✓ {len(assets)} assets of type '{asset_type}'", assets)
        except Exception as e:
            return ToolResult(False, f"✗ CanvaTool list_assets failed: {e}")

    @staticmethod
    def upload_asset(
        file_path: str,
        name: str,
        cred_key: str = "canva",
    ) -> ToolResult:
        try:
            import requests
            headers = CanvaTool._headers(cred_key)
            headers.pop("Content-Type", None)
            with open(file_path, "rb") as fh:
                r = requests.post(
                    f"{CanvaTool._BASE}/assets",
                    headers=headers,
                    files={"asset_file": (name, fh)},
                    data={"name_base64": name.encode().hex()},
                    timeout=120,
                )
            r.raise_for_status()
            return ToolResult(True, f"✓ Asset '{name}' uploaded", r.json())
        except Exception as e:
            return ToolResult(False, f"✗ CanvaTool upload_asset failed: {e}")

    @staticmethod
    def create_from_template(
        template_id: str,
        replacements: dict,
        output: str,
        cred_key: str = "canva",
    ) -> ToolResult:
        try:
            # Autofill API
            payload = {
                "brand_template_id": template_id,
                "title": replacements.get("title", "NPM Agent Design"),
                "data": [
                    {"type": "text", "name": k, "text": v}
                    for k, v in replacements.items()
                    if k != "title"
                ],
            }
            job_data = CanvaTool._post("/autofills", payload, cred_key)
            job_id   = job_data.get("job", {}).get("id", "")
            import time
            for _ in range(20):
                status = CanvaTool._get(f"/autofills/{job_id}", cred_key)
                job = status.get("job", {})
                if job.get("status") == "success":
                    design_id = job.get("result", {}).get("design", {}).get("id", "")
                    # Export the design
                    return CanvaTool.export_design(design_id, output, cred_key=cred_key)
                elif job.get("status") == "failed":
                    return ToolResult(False, f"✗ Autofill job failed: {job}")
                time.sleep(2)
            return ToolResult(False, "✗ Autofill timed out.")
        except Exception as e:
            return ToolResult(False, f"✗ CanvaTool create_from_template failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. FontTool
# ─────────────────────────────────────────────────────────────────────────────

class FontTool:
    name = "font"
    description = (
        "Font management: list system fonts, install/remove, render text images, "
        "animated text frames, font previews, conversion, subsetting and pairing."
    )
    use = (
           """Name of Tool:- FontTool

Purpose of Tool:- 
The FontTool provides an all-in-one system typography management and processing pipeline. It interacts directly with standard operating system directories to audit, configure, install, or drop structural TrueType (.ttf) and OpenType (.otf) font assets. It also acts as a programmatic graphics rendering engine to produce alpha-channeled text titles, multi-frame kinetic layout animations, and multi-size font specimen previews. For web performance, it supports font file structural conversion and dynamic context subsetting to compress files for target letter pools, alongside matching lookup engines to pair complementary typographic structures.

Methods:-
- list_system_fonts: Scans operating system directories to catalog all active typography font assets.
- install_font: Downloads web font assets or copies local files to configure them securely in system fonts registries.
- remove_font: Identifies and removes specific font files out of operating system asset paths.
- render_text_image: Compiles a custom styled text block into an aligned rasterized PNG image file.
- create_text_animation_frames: Generates sequential graphic frame arrays applying transition effects like fades, slides, or zooms.
- generate_font_preview: Compiles a localized multi-point type scaling sample page for layout auditing.
- convert_font: Transcodes desktop font resources into compressed web formatting architectures like WOFF or WOFF2.
- subset_font: Strips unneeded glyph blocks out of a font file to output an optimized payload containing only selected character strings.
- get_font_info: Extracts core design metadata tags including authorship copyrights, version strings, and designer profiles.
- pair_fonts_suggestion: Evaluates a chosen font style to recommend design-appropriate, matching font combinations.

How to use Tool Methods:-

1. list_system_fonts:
   - Purpose: Discovers typography files currently installed and ready on the host environment.
   - Arguments: None.
   - Returns: ToolResult listing unique font family name strings.
   - How to call: FontTool.list_system_fonts()

2. install_font:
   - Purpose: Automates onboarding web styles or external files across multi-platform storage paths.
   - Arguments:
     a) font_path_or_url: str - Local disk directory reference or online download web path tracking a valid font file.
   - Returns: ToolResult registering destination installation status markers.
   - How to call: FontTool.install_font(font_path_or_url="https://fonts.gstatic.com/s/lobster/v30/neolw9o9l02v_bkaOux9.ttf")

3. remove_font:
   - Purpose: Deletes target custom typography assets to clean up corporate systems or refresh file versions.
   - Arguments:
     a) font_name: str - Partial or complete file name string used to match and target specific fonts.
   - Returns: ToolResult mapping individual paths removed by the purge process.
   - How to call: FontTool.remove_font(font_name="Lobster")

4. render_text_image:
   - Purpose: Generates styled headlines, watermark templates, or layout badges for downstream design pipelines.
   - Arguments:
     a) text: str - Core text characters to render into a graphic.
     b) font: str (default: "Arial") - Target typographic system family name.
     c) size: int (default: 48) - Structural size height point constraint.
     d) color: str (default: "#000000") - Hex color code controlling text layout fill.
     e) background: str (default: "#FFFFFF") - Background fill value mapping.
     f) output: str (default: "text.png") - Local path where the image will save.
     g) width: int (default: 800) - Canvas horizontal resolution bounding parameter.
     h) height: int (default: 200) - Canvas vertical space allotment marker.
     i) align: str (default: "center") - Layout alignment anchor position constraint ("center", "left", "right").
   - Returns: ToolResult verifying canvas conversion accuracy.
   - How to call: FontTool.render_text_image(text="PROMOTION", font="Impact", size=60, color="#FF0000", output="ads/banner.png")

5. create_text_animation_frames:
   - Purpose: Generates visual image loops and video layers using custom text transitions.
   - Arguments:
     a) text: str - Core wording pattern targeting sequence renders.
     b) font: str (default: "Arial") - Target text design group.
     c) size: int (default: 48) - Point scale configuration constraint mapping.
     d) animation: str (default: "fade") - Selected kinetic motion trajectory logic ("fade", "slide_in", "zoom").
     e) output_folder: str (default: "text_frames") - Local folder path to save sequential PNG files.
     f) fps: int (default: 24) - Frame calculation volume metric mapping tracking.
     g) duration: float (default: 1.0) - Time block boundary span tracking length constraints in seconds.
   - Returns: ToolResult tracking full frame output logs metrics data maps.
   - How to call: FontTool.create_text_animation_frames(text="Loading...", animation="zoom", output_folder="frames/loader", duration=2.0)

6. generate_font_preview:
   - Purpose: Creates type specimen charts to visually audit styling options before selection.
   - Arguments:
     a) font_name: str - Selected system family path reference indicator.
     b) output: str (default: "font_preview.png") - Storage asset output indicator.
     c) text: str (default: "The quick brown fox...") - Custom test phrase layer template string.
     d) sizes: Optional[List[int]] (default: None) - Array of sizing milestones used to scale preview text lines.
   - Returns: ToolResult certifying graphic file creation parameters.
   - How to call: FontTool.generate_font_preview(font_name="Helvetica", sizes=[10, 14, 20, 32])

7. convert_font:
   - Purpose: Standardizes and compresses graphic layouts for optimal loading across modern web architectures.
   - Arguments:
     a) input: str - Path location reference tracking source TrueType/OpenType files.
     b) output_format: str - Transcoding compression format target identifier ("woff", "woff2").
   - Returns: ToolResult logging processed path conversions.
   - How to call: FontTool.convert_font(input="fonts/custom.ttf", output_format="woff2")

8. subset_font:
   - Purpose: Minimizes application bundle sizes by stripping out unused character glyph blocks.
   - Arguments:
     a) font: str - File location pointer tracking input resources.
     b) characters: str - Exact set of character strings to keep in the final file structure.
     c) output: str - Destination storage path mapping for the optimized file.
   - Returns: ToolResult indicating file optimization status.
   - How to call: FontTool.subset_font(font="global.ttf", characters="0123456789$-.", output="minified_digits.ttf")

9. get_font_info:
   - Purpose: Audits legal compliance and version constraints by inspecting font file header tables.
   - Arguments:
     a) font_path: str - Local destination tracker pointing at core type assets.
   - Returns: ToolResult holding an explanatory dictionary of font header records.
   - How to call: FontTool.get_font_info(font_path="fonts/OpenSans-Regular.ttf")

10. pair_fonts_suggestion:
    - Purpose: Speeds up interface layout designs by matching headings with complementary body font choices.
    - Arguments:
      a) font_name: str - Reference style point key from which pairings determine.
    - Returns: ToolResult providing pairing suggestion arrays.
    - How to call: FontTool.pair_fonts_suggestion(font_name="Montserrat")
    """)

    @staticmethod
    def list_system_fonts() -> ToolResult:
        try:
            import matplotlib.font_manager as fm
            fonts = sorted({Path(f).stem for f in fm.findSystemFonts()})
            return ToolResult(True, f"✓ {len(fonts)} system fonts found", fonts)
        except Exception as e:
            return ToolResult(False, f"✗ FontTool list_system_fonts failed: {e}")

    @staticmethod
    def install_font(font_path_or_url: str) -> ToolResult:
        try:
            import platform, requests
            src = font_path_or_url
            if src.startswith("http"):
                r = requests.get(src, timeout=60)
                r.raise_for_status()
                tmp = tempfile.NamedTemporaryFile(
                    suffix=Path(src.split("?")[0]).suffix or ".ttf",
                    delete=False,
                )
                tmp.write(r.content)
                tmp.close()
                src = tmp.name
            os_name = platform.system()
            if os_name == "Windows":
                font_dir = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
            elif os_name == "Darwin":
                font_dir = Path.home() / "Library" / "Fonts"
            else:
                font_dir = Path.home() / ".local" / "share" / "fonts"
            font_dir.mkdir(parents=True, exist_ok=True)
            dest = font_dir / Path(src).name
            shutil.copy2(src, dest)
            # Refresh font cache on Linux
            if os_name == "Linux":
                subprocess.run(["fc-cache", "-f"], capture_output=True)
            return ToolResult(True, f"✓ Font installed to {dest}")
        except Exception as e:
            return ToolResult(False, f"✗ FontTool install_font failed: {e}")

    @staticmethod
    def remove_font(font_name: str) -> ToolResult:
        try:
            import platform, matplotlib.font_manager as fm
            font_files = [
                f for f in fm.findSystemFonts()
                if font_name.lower() in Path(f).stem.lower()
            ]
            if not font_files:
                return ToolResult(False, f"✗ No font matching '{font_name}' found.")
            removed = []
            for ff in font_files:
                try:
                    os.remove(ff)
                    removed.append(ff)
                except PermissionError:
                    pass
            if platform.system() == "Linux":
                subprocess.run(["fc-cache", "-f"], capture_output=True)
            return ToolResult(True, f"✓ Removed {len(removed)} font file(s)", removed)
        except Exception as e:
            return ToolResult(False, f"✗ FontTool remove_font failed: {e}")

    @staticmethod
    def _load_font(font: str, size: int):
        from PIL import ImageFont
        try:
            return ImageFont.truetype(font, size)
        except Exception:
            import matplotlib.font_manager as fm
            matches = fm.findfont(fm.FontProperties(family=font))
            if matches:
                return ImageFont.truetype(matches, size)
            return ImageFont.load_default()

    @staticmethod
    def render_text_image(
        text: str,
        font: str = "Arial",
        size: int = 48,
        color: str = "#000000",
        background: str = "#FFFFFF",
        output: str = "text.png",
        width: int = 800,
        height: int = 200,
        align: str = "center",
    ) -> ToolResult:
        try:
            from PIL import Image, ImageDraw
            img  = Image.new("RGBA", (width, height), background)
            draw = ImageDraw.Draw(img)
            fnt  = FontTool._load_font(font, size)
            # Calculate text position
            bbox = draw.textbbox((0, 0), text, font=fnt)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if align == "center":
                x = (width - tw) // 2
            elif align == "right":
                x = width - tw - 10
            else:
                x = 10
            y = (height - th) // 2
            draw.text((x, y), text, font=fnt, fill=color)
            img.save(output)
            return ToolResult(True, f"✓ Text image saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ FontTool render_text_image failed: {e}")

    @staticmethod
    def create_text_animation_frames(
        text: str,
        font: str = "Arial",
        size: int = 48,
        animation: str = "fade",
        output_folder: str = "text_frames",
        fps: int = 24,
        duration: float = 1.0,
    ) -> ToolResult:
        try:
            from PIL import Image, ImageDraw
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            total_frames = int(fps * duration)
            fnt = FontTool._load_font(font, size)
            img_w, img_h = 800, 200
            for i in range(total_frames):
                img  = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 255))
                draw = ImageDraw.Draw(img)
                bbox = draw.textbbox((0, 0), text, font=fnt)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                x, y   = (img_w - tw) // 2, (img_h - th) // 2
                progress = i / max(total_frames - 1, 1)
                if animation == "fade":
                    alpha = int(255 * progress)
                    draw.text((x, y), text, font=fnt, fill=(0, 0, 0, alpha))
                elif animation == "slide_in":
                    offset = int(img_w - img_w * progress)
                    draw.text((x - offset, y), text, font=fnt, fill=(0, 0, 0, 255))
                elif animation == "zoom":
                    z_size = max(8, int(size * progress))
                    z_fnt  = FontTool._load_font(font, z_size)
                    bb2 = draw.textbbox((0, 0), text, font=z_fnt)
                    tw2, th2 = bb2[2] - bb2[0], bb2[3] - bb2[1]
                    draw.text(((img_w - tw2) // 2, (img_h - th2) // 2), text, font=z_fnt, fill=(0, 0, 0))
                else:
                    draw.text((x, y), text, font=fnt, fill=(0, 0, 0, 255))
                img.save(Path(output_folder) / f"frame_{i:04d}.png")
            return ToolResult(True, f"✓ {total_frames} animation frames saved to {output_folder}")
        except Exception as e:
            return ToolResult(False, f"✗ FontTool create_text_animation_frames failed: {e}")

    @staticmethod
    def generate_font_preview(
        font_name: str,
        output: str = "font_preview.png",
        text: str = "The quick brown fox jumps over the lazy dog",
        sizes: Optional[List[int]] = None,
    ) -> ToolResult:
        try:
            from PIL import Image, ImageDraw
            sizes = sizes or [12, 18, 24, 36, 48]
            line_h = max(sizes) + 10
            img_h  = line_h * len(sizes) + 20
            img    = Image.new("RGB", (900, img_h), "white")
            draw   = ImageDraw.Draw(img)
            y = 10
            for sz in sizes:
                fnt = FontTool._load_font(font_name, sz)
                draw.text((10, y), f"{sz}pt: {text}", font=fnt, fill="black")
                y += sz + 10
            img.save(output)
            return ToolResult(True, f"✓ Font preview saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ FontTool generate_font_preview failed: {e}")

    @staticmethod
    def convert_font(
        input: str,
        output_format: str,
    ) -> ToolResult:
        try:
            from fonttools.ttLib import TTFont
            out_path = Path(input).with_suffix(f".{output_format.lower()}")
            font = TTFont(input)
            font.flavor = None  # reset for woff/woff2
            if output_format.lower() == "woff":
                font.flavor = "woff"
            elif output_format.lower() == "woff2":
                font.flavor = "woff2"
            font.save(str(out_path))
            return ToolResult(True, f"✓ Font converted to {out_path}")
        except Exception as e:
            return ToolResult(False, f"✗ FontTool convert_font failed: {e}")

    @staticmethod
    def subset_font(
        font: str,
        characters: str,
        output: str,
    ) -> ToolResult:
        try:
            _ensure("fonttools", "fonttools")
            unicodes = ",".join(str(ord(c)) for c in set(characters))
            result = subprocess.run(
                [
                    sys.executable, "-m", "fonttools", "subset",
                    font, f"--unicodes={unicodes}", f"--output-file={output}",
                ],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode == 0:
                return ToolResult(True, f"✓ Font subset saved to {output}")
            return ToolResult(False, f"✗ subset_font failed: {result.stderr}")
        except Exception as e:
            return ToolResult(False, f"✗ FontTool subset_font failed: {e}")

    @staticmethod
    def get_font_info(font_path: str) -> ToolResult:
        try:
            from fonttools.ttLib import TTFont
            font = TTFont(font_path)
            name_table = font["name"]
            info = {}
            for record in name_table.names:
                try:
                    val = record.toUnicode()
                    info[record.nameID] = val
                except Exception:
                    pass
            friendly = {
                1: "Family",
                2: "Style",
                3: "Unique ID",
                4: "Full Name",
                5: "Version",
                6: "PostScript Name",
                8: "Manufacturer",
                9: "Designer",
                11: "URL Vendor",
                12: "URL Designer",
            }
            result = {friendly.get(k, str(k)): v for k, v in info.items()}
            return ToolResult(True, f"✓ Font info for {font_path}", result)
        except Exception as e:
            return ToolResult(False, f"✗ FontTool get_font_info failed: {e}")

    @staticmethod
    def pair_fonts_suggestion(font_name: str) -> ToolResult:
        try:
            import requests
            # Query Google Fonts API for pairings (heuristic)
            GOOGLE_FONTS_PAIRINGS: dict = {
                "roboto":       ["Lato", "Open Sans", "Merriweather", "Raleway"],
                "open sans":    ["Roboto", "Lato", "Playfair Display", "Montserrat"],
                "lato":         ["Merriweather", "Roboto", "Raleway", "Source Sans Pro"],
                "montserrat":   ["Source Sans Pro", "Open Sans", "Lato", "Cardo"],
                "playfair display": ["Source Sans Pro", "Raleway", "Lato", "Open Sans"],
            }
            key = font_name.lower()
            pairs = PAIRINGS = None
            for k, v in GOOGLE_FONTS_PAIRINGS.items():
                if k in key or key in k:
                    PAIRINGS = v
                    break
            if not PAIRINGS:
                PAIRINGS = ["Open Sans", "Lato", "Roboto", "Merriweather"]
            return ToolResult(
                True,
                f"✓ Suggested pairings for '{font_name}'",
                {"font": font_name, "pair_with": PAIRINGS},
            )
        except Exception as e:
            return ToolResult(False, f"✗ FontTool pair_fonts_suggestion failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. ColorTool
# ─────────────────────────────────────────────────────────────────────────────

class ColorTool:
    name = "color"
    description = (
        "Color science: palette generation, image palette extraction, color space "
        "conversion, contrast checking, gradients, color wheels, brand palettes."
    )
    use = (
           """
Name of Tool:- ColorTool,

Purpose of Tool:- 
The ColorTool is a comprehensive color science and design utility for palette generation, color space conversions, contrast analysis, gradient creation, image color extraction, brand palette suggestions, color wheel generation, and palette export in multiple formats. 
It leverages Python standard libraries (colorsys), PIL for image processing, and supports hex, RGB, HSL, HSV, and CMYK color spaces. 
This tool is essential for UI/UX design automation, data visualization, brand identity systems, accessibility checking, generative art, and agentic creative design workflows.

Methods:-
- _hex_to_rgb: Internal helper to convert hex color to RGB tuple.
- _rgb_to_hex: Internal helper to convert RGB values to hex string.
- generate_palette: Generates harmonious color palettes (complementary, triadic, analogous, etc.).
- extract_palette_from_image: Extracts dominant colors from an image using quantization.
- convert_color: Converts a color between different color spaces (hex, rgb, hsl, hsv, cmyk).
- find_complementary: Calculates the complementary color of a given hex color.
- create_gradient: Generates a smooth gradient image between multiple colors.
- check_contrast_ratio: Calculates WCAG contrast ratio and accessibility compliance.
- suggest_accessible_combination: Automatically suggests accessible color combinations.
- create_color_wheel: Generates a full HSV color wheel image.
- generate_brand_palette: Creates a professional brand palette with primary, accents, and neutrals.
- export_palette: Exports a color palette to JSON, CSS, SCSS, or Adobe ASE format.
- analyze_image_colors: Performs comprehensive color analysis on an image (average, dominant, brightness, etc.).

How to use Tool Methods:-

1. generate_palette:
   - Purpose: Generates a harmonious color palette based on a base color and color theory rules.
   - Arguments:
     a) base_color: str - Hex color (e.g., "#FF0000").
     b) harmony: str (default: "complementary") - "complementary", "triadic", "analogous", "split-complementary", "tetradic", or "monochromatic".
     c) n_colors: int (default: 5) - Number of colors in the palette.
   - Returns: List of hex colors.
   - How to call: ColorTool.generate_palette(base_color="#3498db", harmony="triadic", n_colors=6)

2. extract_palette_from_image:
   - Purpose: Extracts the most dominant colors from an image using PIL quantization.
   - Arguments:
     a) image: str - Path to image file.
     b) n_colors: int (default: 5) - Number of colors to extract.
   - Returns: List of hex colors.
   - How to call: ColorTool.extract_palette_from_image(image="photo.jpg", n_colors=8)

3. convert_color:
   - Purpose: Converts a color between supported color spaces.
   - Arguments:
     a) value: str - Color value in source space (e.g., "#FF0000", "rgb(255,0,0)", "hsl(0,100%,50%)").
     b) from_space: str - "hex", "rgb", "hsl", "hsv".
     c) to_space: str - "hex", "rgb", "hsl", "hsv", "cmyk".
   - Returns: Converted color string.
   - How to call: ColorTool.convert_color(value="#FF0000", from_space="hex", to_space="hsl")

4. find_complementary:
   - Purpose: Returns the complementary (opposite on color wheel) color.
   - Arguments: hex_color: str
   - Returns: Complementary hex color and details.
   - How to call: ColorTool.find_complementary(hex_color="#00FF00")

5. create_gradient:
   - Purpose: Creates a smooth linear gradient image between multiple colors.
   - Arguments:
     a) colors: List[str] - List of hex colors.
     b) steps: int (default: 10) - Not directly used in interpolation (segment-based).
     c) direction: str (default: "horizontal") - "horizontal" or "vertical".
     d) output_image: str (default: "gradient.png")
     e) width, height: int - Image dimensions.
   - How to call: ColorTool.create_gradient(colors=["#FF0000", "#00FF00", "#0000FF"], direction="horizontal", output_image="rainbow.png")

6. check_contrast_ratio:
   - Purpose: Calculates contrast ratio between two colors and checks WCAG AA/AAA compliance.
   - Arguments:
     a) color1: str - Hex color (background usually).
     b) color2: str - Hex color (foreground/text).
   - Returns: Ratio and accessibility flags.
   - How to call: ColorTool.check_contrast_ratio(color1="#FFFFFF", color2="#000000")

7. suggest_accessible_combination:
   - Purpose: Automatically adjusts a foreground color to meet WCAG AA contrast requirements.
   - Arguments:
     a) background: str - Background hex color.
     b) foreground: str - Initial foreground hex color.
   - Returns: Adjusted accessible color pair.
   - How to call: ColorTool.suggest_accessible_combination(background="#1E3A8A", foreground="#FFFFFF")

8. create_color_wheel:
   - Purpose: Generates a full HSV color wheel as a PNG image.
   - Arguments:
     a) output: str (default: "color_wheel.png")
     b) size: int (default: 400) - Diameter in pixels.
   - How to call: ColorTool.create_color_wheel(output="wheel.png", size=800)

9. generate_brand_palette:
   - Purpose: Creates a complete brand palette with primary, accent, and neutral colors.
   - Arguments:
     a) primary: str - Primary brand hex color.
     b) n_accent: int (default: 3)
     c) n_neutral: int (default: 4)
   - Returns: Structured palette dictionary.
   - How to call: ColorTool.generate_brand_palette(primary="#3B82F6", n_accent=4)

10. export_palette:
    - Purpose: Exports a list of colors to JSON, CSS variables, SCSS variables, or Adobe ASE swatch file.
    - Arguments:
      a) colors: List[str] - List of hex colors.
      b) format: str (default: "json") - "json", "css", "scss", "ase".
      c) output: str - Base filename (extension added automatically).
    - How to call: ColorTool.export_palette(colors=["#FF0000", "#00FF00"], format="css", output="brand")

11. analyze_image_colors:
    - Purpose: Performs statistical color analysis on an image (average color, dominant colors, brightness, saturation, hue).
    - Arguments: image: str - Path to image file.
    - Returns: Detailed color analysis dictionary.
    - How to call: ColorTool.analyze_image_colors(image="photo.jpg")
""")

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def _rgb_to_hex(r: int, g: int, b: int) -> str:
        return f"#{r:02X}{g:02X}{b:02X}"

    @staticmethod
    def generate_palette(
        base_color: str,
        harmony: str = "complementary",
        n_colors: int = 5,
    ) -> ToolResult:
        try:
            r, g, b = ColorTool._hex_to_rgb(base_color)
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            palette = []
            if harmony == "complementary":
                angles = [0, 0.5] + [(i / (n_colors - 2)) * 0.5 for i in range(n_colors - 2)]
            elif harmony == "triadic":
                angles = [0, 1/3, 2/3] + [(i / max(n_colors - 3, 1)) for i in range(n_colors - 3)]
            elif harmony == "analogous":
                angles = [(i / (n_colors - 1)) * 0.25 - 0.125 for i in range(n_colors)]
            elif harmony == "split-complementary":
                angles = [0, 5/12, 7/12] + [(i / max(n_colors - 3, 1)) for i in range(n_colors - 3)]
            elif harmony == "tetradic":
                angles = [0, 0.25, 0.5, 0.75] + [(i / max(n_colors - 4, 1)) for i in range(n_colors - 4)]
            else:
                angles = [(i / (n_colors - 1)) for i in range(n_colors)]
            for angle in angles[:n_colors]:
                nh = (h + angle) % 1.0
                nr, ng, nb = colorsys.hsv_to_rgb(nh, s, v)
                palette.append(ColorTool._rgb_to_hex(int(nr * 255), int(ng * 255), int(nb * 255)))
            return ToolResult(True, f"✓ Generated {len(palette)} {harmony} colors", palette)
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool generate_palette failed: {e}")

    @staticmethod
    def extract_palette_from_image(
        image: str,
        n_colors: int = 5,
    ) -> ToolResult:
        try:
            from PIL import Image
            img = Image.open(image).convert("RGB").resize((150, 150))
            pixels = list(img.getdata())
            # Simple k-means-lite: quantize
            img_q = img.quantize(colors=n_colors)
            palette_raw = img_q.getpalette()
            colors = []
            for i in range(n_colors):
                r, g, b = palette_raw[i*3], palette_raw[i*3+1], palette_raw[i*3+2]
                colors.append(ColorTool._rgb_to_hex(r, g, b))
            return ToolResult(True, f"✓ Extracted {n_colors} colors from image", colors)
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool extract_palette_from_image failed: {e}")

    @staticmethod
    def convert_color(
        value: str,
        from_space: str,
        to_space: str,
    ) -> ToolResult:
        try:
            from_space = from_space.lower()
            to_space   = to_space.lower()
            # Normalize to RGB first
            if from_space == "hex":
                r, g, b = ColorTool._hex_to_rgb(value)
                rf, gf, bf = r / 255, g / 255, b / 255
            elif from_space == "rgb":
                parts = [float(x.strip()) for x in value.strip("rgb()").split(",")]
                rf, gf, bf = parts[0] / 255, parts[1] / 255, parts[2] / 255
            elif from_space == "hsl":
                parts = [float(x.strip().strip("%")) for x in value.strip("hsl()").split(",")]
                rf, gf, bf = colorsys.hls_to_rgb(parts[0] / 360, parts[2] / 100, parts[1] / 100)
            elif from_space == "hsv":
                parts = [float(x.strip().strip("%")) for x in value.strip("hsv()").split(",")]
                rf, gf, bf = colorsys.hsv_to_rgb(parts[0] / 360, parts[1] / 100, parts[2] / 100)
            else:
                return ToolResult(False, f"✗ Unsupported from_space: {from_space}")
            # Convert to target
            if to_space == "hex":
                result = ColorTool._rgb_to_hex(int(rf * 255), int(gf * 255), int(bf * 255))
            elif to_space == "rgb":
                result = f"rgb({int(rf*255)}, {int(gf*255)}, {int(bf*255)})"
            elif to_space == "hsl":
                h, l, s = colorsys.rgb_to_hls(rf, gf, bf)
                result = f"hsl({round(h*360)}, {round(s*100)}%, {round(l*100)}%)"
            elif to_space == "hsv":
                h, s, v = colorsys.rgb_to_hsv(rf, gf, bf)
                result = f"hsv({round(h*360)}, {round(s*100)}%, {round(v*100)}%)"
            elif to_space == "cmyk":
                if max(rf, gf, bf) == 0:
                    result = "cmyk(0%, 0%, 0%, 100%)"
                else:
                    k = 1 - max(rf, gf, bf)
                    c = (1 - rf - k) / (1 - k)
                    m = (1 - gf - k) / (1 - k)
                    y = (1 - bf - k) / (1 - k)
                    result = f"cmyk({round(c*100)}%, {round(m*100)}%, {round(y*100)}%, {round(k*100)}%)"
            else:
                return ToolResult(False, f"✗ Unsupported to_space: {to_space}")
            return ToolResult(True, f"✓ {value} ({from_space}) → {result} ({to_space})", result)
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool convert_color failed: {e}")

    @staticmethod
    def find_complementary(hex_color: str) -> ToolResult:
        try:
            r, g, b = ColorTool._hex_to_rgb(hex_color)
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            ch = (h + 0.5) % 1.0
            cr, cg, cb = colorsys.hsv_to_rgb(ch, s, v)
            comp = ColorTool._rgb_to_hex(int(cr * 255), int(cg * 255), int(cb * 255))
            return ToolResult(True, f"✓ Complementary of {hex_color} = {comp}",
                              {"original": hex_color, "complementary": comp})
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool find_complementary failed: {e}")

    @staticmethod
    def create_gradient(
        colors: List[str],
        steps: int = 10,
        direction: str = "horizontal",
        output_image: str = "gradient.png",
        width: int = 800,
        height: int = 100,
    ) -> ToolResult:
        try:
            from PIL import Image
            img = Image.new("RGB", (width, height))
            px  = img.load()
            if len(colors) < 2:
                return ToolResult(False, "✗ Need at least 2 colors for gradient.")
            # Convert stops to RGB
            stops = [ColorTool._hex_to_rgb(c) for c in colors]

            def interp(a, b, t):
                return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

            if direction == "horizontal":
                total = width
                for x in range(total):
                    t = x / (total - 1)
                    seg_f = t * (len(stops) - 1)
                    seg_i = min(int(seg_f), len(stops) - 2)
                    local_t = seg_f - seg_i
                    color = interp(stops[seg_i], stops[seg_i + 1], local_t)
                    for y in range(height):
                        px[x, y] = color
            else:
                total = height
                for y in range(total):
                    t = y / (total - 1)
                    seg_f = t * (len(stops) - 1)
                    seg_i = min(int(seg_f), len(stops) - 2)
                    local_t = seg_f - seg_i
                    color = interp(stops[seg_i], stops[seg_i + 1], local_t)
                    for x in range(width):
                        px[x, y] = color
            img.save(output_image)
            return ToolResult(True, f"✓ Gradient saved to {output_image}")
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool create_gradient failed: {e}")

    @staticmethod
    def check_contrast_ratio(color1: str, color2: str) -> ToolResult:
        try:
            def relative_luminance(hex_c):
                r, g, b = [x / 255 for x in ColorTool._hex_to_rgb(hex_c)]
                def linearize(c):
                    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
                return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)
            l1 = relative_luminance(color1)
            l2 = relative_luminance(color2)
            lighter, darker = max(l1, l2), min(l1, l2)
            ratio = (lighter + 0.05) / (darker + 0.05)
            wcag_aa  = ratio >= 4.5
            wcag_aaa = ratio >= 7.0
            return ToolResult(
                True,
                f"✓ Contrast ratio {ratio:.2f}:1  |  WCAG AA: {'✓' if wcag_aa else '✗'}  AAA: {'✓' if wcag_aaa else '✗'}",
                {"ratio": round(ratio, 2), "WCAG_AA": wcag_aa, "WCAG_AAA": wcag_aaa},
            )
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool check_contrast_ratio failed: {e}")

    @staticmethod
    def suggest_accessible_combination(
        background: str,
        foreground: str,
    ) -> ToolResult:
        try:
            result = ColorTool.check_contrast_ratio(background, foreground)
            if not result.success:
                return result
            ratio = result.data["ratio"]
            if ratio >= 4.5:
                return ToolResult(True,
                    f"✓ {background}/{foreground} passes WCAG AA (ratio {ratio:.2f})",
                    {"background": background, "foreground": foreground, "ratio": ratio, "accessible": True})
            # Darken or lighten foreground until compliant
            r, g, b = ColorTool._hex_to_rgb(foreground)
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            for step in range(20):
                v_try = max(0, v - step * 0.05)
                nr, ng, nb = colorsys.hsv_to_rgb(h, s, v_try)
                new_fg = ColorTool._rgb_to_hex(int(nr * 255), int(ng * 255), int(nb * 255))
                r2 = ColorTool.check_contrast_ratio(background, new_fg)
                if r2.data and r2.data["ratio"] >= 4.5:
                    return ToolResult(True,
                        f"✓ Adjusted foreground {new_fg} passes WCAG AA",
                        {"background": background, "foreground": new_fg, "ratio": r2.data["ratio"], "accessible": True})
            return ToolResult(False, "✗ Could not find an accessible combination automatically.")
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool suggest_accessible_combination failed: {e}")

    @staticmethod
    def create_color_wheel(
        output: str = "color_wheel.png",
        size: int = 400,
    ) -> ToolResult:
        try:
            from PIL import Image
            img = Image.new("RGB", (size, size), "white")
            cx, cy = size // 2, size // 2
            radius = size // 2 - 10
            px = img.load()
            for y in range(size):
                for x in range(size):
                    dx, dy = x - cx, y - cy
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist <= radius:
                        hue = (math.atan2(dy, dx) / (2 * math.pi)) % 1.0
                        sat = dist / radius
                        r, g, b = colorsys.hsv_to_rgb(hue, sat, 1.0)
                        px[x, y] = (int(r * 255), int(g * 255), int(b * 255))
            img.save(output)
            return ToolResult(True, f"✓ Color wheel saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool create_color_wheel failed: {e}")

    @staticmethod
    def generate_brand_palette(
        primary: str,
        n_accent: int = 3,
        n_neutral: int = 4,
    ) -> ToolResult:
        try:
            r, g, b = ColorTool._hex_to_rgb(primary)
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            accents = []
            for i in range(n_accent):
                ah = (h + (i + 1) / (n_accent + 1)) % 1.0
                ar, ag, ab = colorsys.hsv_to_rgb(ah, s, v)
                accents.append(ColorTool._rgb_to_hex(int(ar * 255), int(ag * 255), int(ab * 255)))
            neutrals = []
            for i in range(n_neutral):
                nv = 0.9 - (i * 0.7 / (n_neutral - 1))
                nr, ng, nb = colorsys.hsv_to_rgb(h, 0.05, nv)
                neutrals.append(ColorTool._rgb_to_hex(int(nr * 255), int(ng * 255), int(nb * 255)))
            palette = {"primary": primary, "accents": accents, "neutrals": neutrals}
            return ToolResult(True, f"✓ Brand palette generated", palette)
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool generate_brand_palette failed: {e}")

    @staticmethod
    def export_palette(
        colors: List[str],
        format: str = "json",
        output: str = "palette",
    ) -> ToolResult:
        try:
            format = format.lower()
            if format == "json":
                out_path = output if output.endswith(".json") else output + ".json"
                Path(out_path).write_text(json.dumps({"colors": colors}, indent=2))
            elif format == "css":
                out_path = output if output.endswith(".css") else output + ".css"
                lines = [":root {"]
                for i, c in enumerate(colors):
                    lines.append(f"  --color-{i+1}: {c};")
                lines.append("}")
                Path(out_path).write_text("\n".join(lines))
            elif format == "scss":
                out_path = output if output.endswith(".scss") else output + ".scss"
                lines = [f"$color-{i+1}: {c};" for i, c in enumerate(colors)]
                Path(out_path).write_text("\n".join(lines))
            elif format == "ase":
                # Adobe Swatch Exchange — simple binary format
                out_path = output if output.endswith(".ase") else output + ".ase"
                import struct
                header = b"ASEF\x00\x01\x00\x00"
                blocks = b""
                for c in colors:
                    r, g, b = [x / 255 for x in ColorTool._hex_to_rgb(c)]
                    name = c.encode("utf-16-be") + b"\x00\x00"
                    color_data = b"RGB " + struct.pack(">fff", r, g, b) + b"\x00\x00"
                    block_len = 2 + len(name) + len(color_data)
                    blocks += b"\x00\x01" + struct.pack(">I", block_len) + name + color_data
                num_blocks = struct.pack(">I", len(colors))
                Path(out_path).write_bytes(header + num_blocks + blocks)
            else:
                return ToolResult(False, f"✗ Unsupported palette format: {format}")
            return ToolResult(True, f"✓ Palette exported to {out_path}")
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool export_palette failed: {e}")

    @staticmethod
    def analyze_image_colors(image: str) -> ToolResult:
        try:
            from PIL import Image
            img = Image.open(image).convert("RGB").resize((200, 200))
            pixels = list(img.getdata())
            # Color statistics
            total = len(pixels)
            avg_r = sum(p[0] for p in pixels) // total
            avg_g = sum(p[1] for p in pixels) // total
            avg_b = sum(p[2] for p in pixels) // total
            avg_hex = ColorTool._rgb_to_hex(avg_r, avg_g, avg_b)
            # Dominant colors via quantize
            img_q = img.quantize(colors=8)
            pal = img_q.getpalette()
            dominant = [ColorTool._rgb_to_hex(pal[i*3], pal[i*3+1], pal[i*3+2]) for i in range(8)]
            h, s, v = colorsys.rgb_to_hsv(avg_r / 255, avg_g / 255, avg_b / 255)
            result = {
                "average_color": avg_hex,
                "dominant_colors": dominant,
                "brightness": round(v * 100, 1),
                "saturation": round(s * 100, 1),
                "hue_degrees": round(h * 360, 1),
            }
            return ToolResult(True, f"✓ Image color analysis complete", result)
        except Exception as e:
            return ToolResult(False, f"✗ ColorTool analyze_image_colors failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. IconTool
# ─────────────────────────────────────────────────────────────────────────────

class IconTool:
    name = "icon"
    description = (
        "Icon generation and management: generate icons from text/emoji, "
        "create app icon sets, resize, convert ICO, favicons, badges."
    )
    use = (
           """Name of Tool:- IconTool

Purpose of Tool:- 
The IconTool provides a robust utility suite for generating, optimizing, formatting, and restructuring digital iconography across major mobile, desktop, and web frameworks. It handles graphic modifications by rendering characters or emoji vectors onto structured shape canvases, generating platform-compliant multi-resolution asset matrices (iOS, Android, macOS, Windows), and exporting bundled favicon asset directories complete with progressive web application standard manifests. Additionally, it contains image processing operations for converting imagery to multi-layered ICO architectures, automated batch transcoding workflows, and localized graphic augmentation matrices to layer operational dynamic alert badges.

Methods:-
- generate_icon: Compiles an emoji character or plain-text string directly into a flat, rounded, or circular graphic emblem asset.
- create_app_icon_set: Downsamples a primary master asset layout into comprehensive multi-resolution dimensions for specific platforms.
- resize_icon: Scales an input image element into an explicit list of target resolution parameters.
- convert_ico: Combines source design files into a multi-layer Windows architecture ICO graphic.
- create_favicon_package: Generates an optimized deployment package containing legacy favicons, high-resolution web layers, mobile home touch layouts, and matching web manifest maps.
- batch_convert_icons: Transcodes entire folders of graphic files simultaneously into a targeted design format.
- add_badge: Layers a colorful graphic alert notification or numerical notification circle overlay directly onto canvas layout profiles.

How to use Tool Methods:-

1. generate_icon:
   - Purpose: Builds fast interface profile elements, generic placeholder elements, or vector style avatars using simple text tokens or emojis.
   - Arguments:
     a) text_or_emoji: str - Characters or emoji strings to center on the canvas layout.
     b) style: str (default: "flat") - Core boundary trimming shape style profile ("flat", "rounded", "circle").
     c) size: int (default: 512) - Pixel size resolution boundary.
     d) background: str (default: "#4F46E5") - Hex canvas fill color setting.
     e) foreground: str (default: "#FFFFFF") - Text glyph color hex parameter.
     f) output: str (default: "icon.png") - Path location map where the graphic will save.
   - Returns: ToolResult tracking successful canvas creation profiles.
   - How to call: IconTool.generate_icon(text_or_emoji="🚀", style="circle", background="#22C55E", output="icons/launch.png")

2. create_app_icon_set:
   - Purpose: Speeds up development pipelines by creating all required platform dimension variations automatically.
   - Arguments:
     a) source_image: str - High-resolution source master image path location reference.
     b) output_folder: str - Folder destination directory path.
     c) platform: str (default: "ios") - Specific ecosystem layout targets ("ios", "android", "web", "macos", "windows").
   - Returns: ToolResult logging the generated target file paths.
   - How to call: IconTool.create_app_icon_set(source_image="masters/logo.png", output_folder="build/assets", platform="android")

3. resize_icon:
   - Purpose: Resizes custom graphics down to specific layout requirements quickly.
   - Arguments:
     a) input: str - Input target file workspace resource location mapping.
     b) sizes: List[int] - Array of sizing dimension integers to process.
     c) output_folder: str - Target local saving directory endpoint.
     d) format: str (default: "PNG") - Export file format option type syntax.
   - Returns: ToolResult confirming the saved layout path array list.
   - How to call: IconTool.resize_icon(input="app.png", sizes=[64, 128], output_folder="dist/icons")

4. convert_ico:
   - Purpose: Bundles multiple layout resolution paths into a single unified container file for system deployment profiles.
   - Arguments:
     a) input: str - Primary graphic master layout reference string pointer.
     b) output: str - Target save path ending with `.ico`.
     c) sizes: Optional[List[int]] (default: None) - Dimensional parameters matrix mapping options stack.
   - Returns: ToolResult confirming execution parameters.
   - How to call: IconTool.convert_ico(input="logo.png", output="favicon.ico", sizes=[16, 32, 48])

5. create_favicon_package:
   - Purpose: Prepares a website's complete bookmark and application shortcut package in one step.
   - Arguments:
     a) source: str - High resolution root design graphic layer file reference pointer.
     b) output_folder: str - Destination tracking target workspace folder location.
   - Returns: ToolResult verifying configuration map generations and file outputs.
   - How to call: IconTool.create_favicon_package(source="branding/icon.png", output_folder="public/")

6. batch_convert_icons:
   - Purpose: Normalizes format properties across asset files uniformly.
   - Arguments:
     a) folder: str - Target workspace directory tracking incoming resource targets.
     b) output_folder: str - Export path directory target container destination.
     c) format: str (default: "ico") - Output translation architecture name format mapping.
   - Returns: ToolResult displaying operational volume conversion statistics.
   - How to call: IconTool.batch_convert_icons(folder="src/png_assets", output_folder="src/ico_assets", format="ico")

7. add_badge:
   - Purpose: Updates application icons with notification indicator counters or warning labels.
   - Arguments:
     a) icon: str - Baseline application graphic source layer directory tracker.
     b) badge_text: str - Notice data or tally strings to layer over the icon.
     c) badge_color: str (default: "#E53E3E") - Hex code color tracking badge circle fill logic.
     d) position: str (default: "top-right") - Anchor location string choice ("top-right", "top-left", "bottom-right", "bottom-left").
     e) output: str (default: "icon_badge.png") - Storage path location mapping tracker identifier.
   - Returns: ToolResult detailing visual compilation status parameters.
   - How to call: IconTool.add_badge(icon="app.png", badge_text="9+", position="top-right", output="notifications/alert_icon.png")
   """)

    @staticmethod
    def generate_icon(
        text_or_emoji: str,
        style: str = "flat",
        size: int = 512,
        background: str = "#4F46E5",
        foreground: str = "#FFFFFF",
        output: str = "icon.png",
    ) -> ToolResult:
        try:
            from PIL import Image, ImageDraw, ImageFont
            img  = Image.new("RGBA", (size, size), background)
            draw = ImageDraw.Draw(img)
            if style == "rounded":
                mask = Image.new("L", (size, size), 0)
                mask_draw = ImageDraw.Draw(mask)
                radius = size // 4
                mask_draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
                base = Image.new("RGBA", (size, size), background)
                base.putalpha(mask)
                img = base
                draw = ImageDraw.Draw(img)
            elif style == "circle":
                mask = Image.new("L", (size, size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([0, 0, size - 1, size - 1], fill=255)
                base = Image.new("RGBA", (size, size), background)
                base.putalpha(mask)
                img = base
                draw = ImageDraw.Draw(img)
            font_size = int(size * 0.5)
            fnt = FontTool._load_font("DejaVuSans", font_size)
            bbox = draw.textbbox((0, 0), text_or_emoji, font=fnt)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(
                ((size - tw) // 2, (size - th) // 2),
                text_or_emoji, font=fnt, fill=foreground,
            )
            img.save(output)
            return ToolResult(True, f"✓ Icon saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ IconTool generate_icon failed: {e}")

    @staticmethod
    def create_app_icon_set(
        source_image: str,
        output_folder: str,
        platform: str = "ios",
    ) -> ToolResult:
        try:
            from PIL import Image
            img = Image.open(source_image).convert("RGBA")
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            SIZES: Dict[str, List[int]] = {
                "ios": [20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180, 1024],
                "android": [36, 48, 72, 96, 144, 192, 512],
                "web": [16, 32, 48, 64, 128, 256, 512],
                "macos": [16, 32, 64, 128, 256, 512, 1024],
                "windows": [16, 24, 32, 48, 64, 128, 256],
            }
            sizes = SIZES.get(platform.lower(), [16, 32, 64, 128, 256, 512])
            saved = []
            for s in sizes:
                resized = img.resize((s, s), Image.LANCZOS)
                out = Path(output_folder) / f"icon_{s}x{s}.png"
                resized.save(out)
                saved.append(str(out))
            return ToolResult(True, f"✓ {len(saved)} icons created for {platform}", saved)
        except Exception as e:
            return ToolResult(False, f"✗ IconTool create_app_icon_set failed: {e}")

    @staticmethod
    def resize_icon(
        input: str,
        sizes: List[int],
        output_folder: str,
        format: str = "PNG",
    ) -> ToolResult:
        try:
            from PIL import Image
            img = Image.open(input).convert("RGBA")
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            saved = []
            for s in sizes:
                resized = img.resize((s, s), Image.LANCZOS)
                out = Path(output_folder) / f"{Path(input).stem}_{s}.{format.lower()}"
                resized.save(out, format.upper())
                saved.append(str(out))
            return ToolResult(True, f"✓ {len(saved)} icons saved to {output_folder}", saved)
        except Exception as e:
            return ToolResult(False, f"✗ IconTool resize_icon failed: {e}")

    @staticmethod
    def convert_ico(
        input: str,
        output: str,
        sizes: Optional[List[int]] = None,
    ) -> ToolResult:
        try:
            from PIL import Image
            img = Image.open(input).convert("RGBA")
            sizes = sizes or [16, 32, 48, 64, 128, 256]
            imgs = [img.resize((s, s), Image.LANCZOS) for s in sizes]
            imgs[0].save(output, format="ICO", sizes=[(s, s) for s in sizes], append_images=imgs[1:])
            return ToolResult(True, f"✓ ICO saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ IconTool convert_ico failed: {e}")

    @staticmethod
    def create_favicon_package(
        source: str,
        output_folder: str,
    ) -> ToolResult:
        try:
            from PIL import Image
            img = Image.open(source).convert("RGBA")
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            # favicon.ico
            IconTool.convert_ico(source, str(Path(output_folder) / "favicon.ico"))
            # PNG sizes
            for size in [16, 32, 48, 96, 192, 512]:
                resized = img.resize((size, size), Image.LANCZOS)
                resized.save(Path(output_folder) / f"favicon-{size}x{size}.png")
            # Apple touch icon
            apple = img.resize((180, 180), Image.LANCZOS)
            apple.save(Path(output_folder) / "apple-touch-icon.png")
            # Web manifest entry
            manifest = {
                "icons": [
                    {"src": f"/favicon-{s}x{s}.png", "sizes": f"{s}x{s}", "type": "image/png"}
                    for s in [192, 512]
                ]
            }
            (Path(output_folder) / "site.webmanifest").write_text(json.dumps(manifest, indent=2))
            return ToolResult(True, f"✓ Favicon package saved to {output_folder}")
        except Exception as e:
            return ToolResult(False, f"✗ IconTool create_favicon_package failed: {e}")

    @staticmethod
    def batch_convert_icons(
        folder: str,
        output_folder: str,
        format: str = "ico",
    ) -> ToolResult:
        try:
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            count = 0
            for f in Path(folder).iterdir():
                if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".bmp", ".webp"):
                    out = Path(output_folder) / f.with_suffix(f".{format.lower()}").name
                    if format.lower() == "ico":
                        IconTool.convert_ico(str(f), str(out))
                    else:
                        from PIL import Image
                        Image.open(f).save(out, format.upper())
                    count += 1
            return ToolResult(True, f"✓ Converted {count} icons to {format} in {output_folder}")
        except Exception as e:
            return ToolResult(False, f"✗ IconTool batch_convert_icons failed: {e}")

    @staticmethod
    def add_badge(
        icon: str,
        badge_text: str,
        badge_color: str = "#E53E3E",
        position: str = "top-right",
        output: str = "icon_badge.png",
    ) -> ToolResult:
        try:
            from PIL import Image, ImageDraw, ImageFont
            img  = Image.open(icon).convert("RGBA")
            w, h = img.size
            draw = ImageDraw.Draw(img)
            badge_r = max(int(w * 0.15), 12)
            offset  = badge_r // 3
            positions_map = {
                "top-right":    (w - badge_r - offset, offset),
                "top-left":     (offset, offset),
                "bottom-right": (w - badge_r - offset, h - badge_r - offset),
                "bottom-left":  (offset, h - badge_r - offset),
            }
            cx, cy = positions_map.get(position, positions_map["top-right"])
            draw.ellipse([cx - badge_r, cy - badge_r, cx + badge_r, cy + badge_r], fill=badge_color)
            fnt  = FontTool._load_font("DejaVuSans", badge_r)
            bbox = draw.textbbox((0, 0), badge_text, font=fnt)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((cx - tw // 2, cy - th // 2), badge_text, font=fnt, fill="white")
            img.save(output)
            return ToolResult(True, f"✓ Badge added, saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ IconTool add_badge failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. DiagramTool
# ─────────────────────────────────────────────────────────────────────────────

class DiagramTool:
    name = "diagram"
    description = (
        "Automated diagram generation: flowcharts, ER diagrams, sequence diagrams, "
        "class diagrams, network diagrams, Gantt charts, mind maps, org charts, "
        "Mermaid and PlantUML rendering."
    )
    use = (
           """
Name of Tool:- DiagramTool,

Purpose of Tool:- 
The DiagramTool enables automated generation of various professional diagrams using matplotlib, networkx, and external tools (Mermaid CLI and PlantUML). 
It supports flowcharts, ER diagrams, sequence diagrams, class diagrams, network diagrams, Gantt charts, mind maps, organization charts, and rendering of Mermaid and PlantUML code. 
This tool is ideal for documentation automation, system architecture visualization, project planning, data modeling, and agentic diagram generation for reports, presentations, and technical documentation.

Methods:-
- create_flowchart: Generates a flowchart from a list of steps with different node types.
- create_er_diagram: Creates an Entity-Relationship diagram from table definitions.
- create_sequence_diagram: Generates a sequence diagram showing interactions between actors.
- create_class_diagram: Creates a UML class diagram with attributes and methods.
- create_network_diagram: Draws a network topology diagram using graph layout.
- create_gantt: Generates a Gantt chart for project scheduling.
- create_mindmap: Creates a hierarchical mind map.
- create_org_chart: Generates an organization chart from a hierarchy.
- render_mermaid: Renders Mermaid diagram code to an image (requires Mermaid CLI).
- render_plantuml: Renders PlantUML diagram code to an image (requires PlantUML/Java).

How to use Tool Methods:-

1. create_flowchart:
   - Purpose: Creates a vertical or horizontal flowchart with process, decision, start, and end nodes.
   - Arguments:
     a) steps: List[dict] - List of steps with "type" ("process", "decision", "start", "end") and "label".
     b) output: str (default: "flowchart.png")
     c) style: str (default: "default")
     d) direction: str (default: "TB") - Currently fixed to vertical in implementation.
   - How to call: 
     DiagramTool.create_flowchart(
         steps=[
             {"type": "start", "label": "Start"},
             {"type": "process", "label": "Process Data"},
             {"type": "decision", "label": "Valid?"},
             {"type": "end", "label": "End"}
         ],
         output="workflow.png"
     )

2. create_er_diagram:
   - Purpose: Visualizes database schema with tables and fields.
   - Arguments:
     a) tables: List[dict] - Each dict has "name" and "fields" (list of strings or dicts with "name" and "type").
     b) output: str (default: "er_diagram.png")
   - How to call: DiagramTool.create_er_diagram(tables=[{"name": "users", "fields": ["id", "name", "email"]}], output="schema.png")

3. create_sequence_diagram:
   - Purpose: Creates UML sequence diagrams showing message flow between participants.
   - Arguments:
     a) actors: List[str] - List of participant names.
     b) messages: List[dict] - Each dict has "from", "to", and "label".
     c) output: str (default: "sequence.png")
   - How to call: DiagramTool.create_sequence_diagram(actors=["User", "API", "DB"], messages=[{"from": "User", "to": "API", "label": "Request"}])

4. create_class_diagram:
   - Purpose: Generates UML class diagrams with class name, attributes, and methods.
   - Arguments:
     a) classes: List[dict] - Each dict has "name", "attributes" (list), "methods" (list).
     b) output: str (default: "class_diagram.png")
   - How to call: DiagramTool.create_class_diagram(classes=[{"name": "User", "attributes": ["id", "name"], "methods": ["login()"]}])

5. create_network_diagram:
   - Purpose: Draws network topology using graph layout.
   - Arguments:
     a) nodes: List[dict] - Each dict has "id", optional "label", "color".
     b) connections: List[dict] - Each dict has "from", "to", optional "label".
     c) output: str (default: "network.png")
   - How to call: DiagramTool.create_network_diagram(nodes=[{"id": "Server"}], connections=[{"from": "Client", "to": "Server"}])

6. create_gantt:
   - Purpose: Creates a Gantt chart for project tasks with start and end times.
   - Arguments:
     a) tasks: List[dict] - Each dict has "name", "start", "end".
     b) output: str (default: "gantt.png")
   - How to call: DiagramTool.create_gantt(tasks=[{"name": "Task 1", "start": 0, "end": 5}])

7. create_mindmap:
   - Purpose: Generates a radial mind map from a hierarchical structure.
   - Arguments:
     a) root: str - Central topic.
     b) children: dict - Nested dictionary of subtopics.
     c) output: str (default: "mindmap.png")
   - How to call: DiagramTool.create_mindmap(root="Project", children={"Phase 1": ["Task A", "Task B"]})

8. create_org_chart:
   - Purpose: Creates a hierarchical organization chart.
   - Arguments:
     a) hierarchy: dict - Nested structure with "name", "title", "children".
     b) output: str (default: "org_chart.png")
   - How to call: DiagramTool.create_org_chart(hierarchy={"name": "CEO", "children": [{"name": "CTO", ...}]})

9. render_mermaid:
   - Purpose: Renders Mermaid.js diagram code to an image.
   - Arguments:
     a) mermaid_code: str - Valid Mermaid syntax.
     b) output: str (default: "diagram.png")
     c) format: str (default: "png")
   - How to call: DiagramTool.render_mermaid(mermaid_code="flowchart TD\nA-->B", output="flow.png")

10. render_plantuml:
    - Purpose: Renders PlantUML diagram code to an image.
    - Arguments:
      a) puml_code: str - Valid PlantUML syntax.
      b) output: str (default: "diagram.png")
      c) format: str (default: "png")
    - How to call: DiagramTool.render_plantuml(puml_code="@startuml\nAlice -> Bob: Hello\n@enduml")
""")

    @staticmethod
    def create_flowchart(
        steps: List[dict],
        output: str = "flowchart.png",
        style: str = "default",
        direction: str = "TB",
    ) -> ToolResult:
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            fig, ax = plt.subplots(figsize=(10, len(steps) * 1.5 + 2))
            ax.set_xlim(0, 10); ax.set_ylim(0, len(steps) * 2 + 1)
            ax.axis("off")
            colors = {"process": "#4F46E5", "decision": "#F59E0B",
                      "start": "#10B981", "end": "#EF4444", "default": "#6B7280"}
            for i, step in enumerate(steps):
                y = len(steps) * 2 - i * 2
                stype = step.get("type", "process")
                color = colors.get(stype, colors["default"])
                label = step.get("label", f"Step {i+1}")
                if stype == "decision":
                    diamond = mpatches.FancyBboxPatch(
                        (2.5, y - 0.4), 5, 0.8,
                        boxstyle="round,pad=0.1", facecolor=color, edgecolor="black", alpha=0.8,
                    )
                    ax.add_patch(diamond)
                    ax.text(5, y, f"◆ {label}", ha="center", va="center", fontsize=9, color="white", weight="bold")
                else:
                    box = mpatches.FancyBboxPatch(
                        (2.5, y - 0.35), 5, 0.7,
                        boxstyle="round,pad=0.1", facecolor=color, edgecolor="black", alpha=0.8,
                    )
                    ax.add_patch(box)
                    ax.text(5, y, label, ha="center", va="center", fontsize=9, color="white", weight="bold")
                if i < len(steps) - 1:
                    ax.annotate("", xy=(5, y - 2 + 0.35), xytext=(5, y - 0.35),
                                arrowprops=dict(arrowstyle="->", color="black"))
            plt.tight_layout()
            plt.savefig(output, dpi=150, bbox_inches="tight")
            plt.close()
            return ToolResult(True, f"✓ Flowchart saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool create_flowchart failed: {e}")

    @staticmethod
    def create_er_diagram(
        tables: List[dict],
        output: str = "er_diagram.png",
    ) -> ToolResult:
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            n = len(tables)
            cols = min(3, n)
            rows = math.ceil(n / cols)
            fig, ax = plt.subplots(figsize=(cols * 5, rows * 4))
            ax.set_xlim(0, cols * 5); ax.set_ylim(0, rows * 4)
            ax.axis("off")
            for idx, table in enumerate(tables):
                col = idx % cols; row = idx // cols
                x, y = col * 5 + 0.3, (rows - row - 1) * 4 + 0.3
                tname = table.get("name", f"Table{idx+1}")
                fields = table.get("fields", [])
                ax.add_patch(mpatches.FancyBboxPatch(
                    (x, y), 4.4, min(len(fields) + 1, 8) * 0.4 + 0.4,
                    boxstyle="square,pad=0", facecolor="#EEF2FF", edgecolor="#4F46E5", linewidth=2,
                ))
                ax.add_patch(mpatches.FancyBboxPatch(
                    (x, y + min(len(fields), 7) * 0.4 + 0.4),
                    4.4, 0.4, boxstyle="square,pad=0",
                    facecolor="#4F46E5", edgecolor="#4F46E5",
                ))
                ax.text(x + 2.2, y + min(len(fields), 7) * 0.4 + 0.6,
                        tname, ha="center", va="center", color="white", weight="bold", fontsize=9)
                for fi, field in enumerate(fields[:7]):
                    fname = field if isinstance(field, str) else field.get("name", f"field_{fi}")
                    ftype = "" if isinstance(field, str) else field.get("type", "")
                    ax.text(x + 0.2, y + (6 - fi) * 0.4 + 0.2,
                            f"  {fname}  {ftype}", va="center", fontsize=7, color="#1F2937")
            plt.savefig(output, dpi=150, bbox_inches="tight")
            plt.close()
            return ToolResult(True, f"✓ ER diagram saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool create_er_diagram failed: {e}")

    @staticmethod
    def create_sequence_diagram(
        actors: List[str],
        messages: List[dict],
        output: str = "sequence.png",
    ) -> ToolResult:
        try:
            import matplotlib.pyplot as plt
            n_actors = len(actors)
            n_msgs   = len(messages)
            fig_w = max(6, n_actors * 2.5)
            fig_h = max(4, n_msgs * 0.8 + 2)
            fig, ax = plt.subplots(figsize=(fig_w, fig_h))
            ax.set_xlim(-0.5, n_actors - 0.5)
            ax.set_ylim(0, n_msgs + 1)
            ax.axis("off")
            # Draw actor lifelines
            x_positions = {a: i for i, a in enumerate(actors)}
            for i, actor in enumerate(actors):
                ax.text(i, n_msgs + 0.7, actor, ha="center", va="center", fontsize=10,
                        weight="bold",
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="#EEF2FF", edgecolor="#4F46E5"))
                ax.plot([i, i], [0.2, n_msgs + 0.4], color="#9CA3AF", linestyle="--", linewidth=1)
            # Draw messages
            for mi, msg in enumerate(messages):
                y = n_msgs - mi
                frm = x_positions.get(msg.get("from", actors[0]), 0)
                to  = x_positions.get(msg.get("to", actors[-1]), len(actors) - 1)
                label = msg.get("label", "")
                ax.annotate(
                    "", xy=(to, y), xytext=(frm, y),
                    arrowprops=dict(arrowstyle="->", color="#4F46E5", lw=1.5),
                )
                mid_x = (frm + to) / 2
                ax.text(mid_x, y + 0.15, label, ha="center", va="bottom", fontsize=8, color="#1F2937")
            plt.tight_layout()
            plt.savefig(output, dpi=150, bbox_inches="tight")
            plt.close()
            return ToolResult(True, f"✓ Sequence diagram saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool create_sequence_diagram failed: {e}")

    @staticmethod
    def create_class_diagram(
        classes: List[dict],
        output: str = "class_diagram.png",
    ) -> ToolResult:
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            n = len(classes)
            cols = min(3, n)
            rows = math.ceil(n / cols)
            fig, ax = plt.subplots(figsize=(cols * 5, rows * 4 + 1))
            ax.set_xlim(0, cols * 5); ax.set_ylim(0, rows * 4 + 1)
            ax.axis("off")
            for idx, cls in enumerate(classes):
                col = idx % cols; row = idx // cols
                x = col * 5 + 0.3
                y = (rows - row - 1) * 4 + 0.3
                name = cls.get("name", f"Class{idx}")
                attrs = cls.get("attributes", [])
                methods = cls.get("methods", [])
                total_h = (len(attrs) + len(methods) + 2) * 0.35 + 0.4
                ax.add_patch(mpatches.FancyBboxPatch(
                    (x, y), 4.4, total_h, boxstyle="square,pad=0",
                    facecolor="#F8FAFC", edgecolor="#334155", linewidth=1.5,
                ))
                # Class name header
                ax.add_patch(mpatches.FancyBboxPatch(
                    (x, y + total_h - 0.4), 4.4, 0.4,
                    boxstyle="square,pad=0", facecolor="#334155", edgecolor="#334155",
                ))
                ax.text(x + 2.2, y + total_h - 0.2, name, ha="center", va="center",
                        color="white", weight="bold", fontsize=9)
                yy = y + total_h - 0.7
                for attr in attrs:
                    ax.text(x + 0.2, yy, f"  {attr}", va="center", fontsize=7, color="#1E293B")
                    yy -= 0.35
                ax.plot([x, x + 4.4], [yy + 0.15, yy + 0.15], color="#CBD5E1", linewidth=0.8)
                for meth in methods:
                    ax.text(x + 0.2, yy, f"  {meth}()", va="center", fontsize=7,
                            color="#1E293B", style="italic")
                    yy -= 0.35
            plt.savefig(output, dpi=150, bbox_inches="tight")
            plt.close()
            return ToolResult(True, f"✓ Class diagram saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool create_class_diagram failed: {e}")

    @staticmethod
    def create_network_diagram(
        nodes: List[dict],
        connections: List[dict],
        output: str = "network.png",
    ) -> ToolResult:
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            G = nx.Graph()
            for node in nodes:
                G.add_node(node["id"], label=node.get("label", node["id"]),
                           color=node.get("color", "#4F46E5"))
            for conn in connections:
                G.add_edge(conn["from"], conn["to"], label=conn.get("label", ""))
            fig, ax = plt.subplots(figsize=(12, 8))
            pos = nx.spring_layout(G, seed=42)
            colors = [G.nodes[n].get("color", "#4F46E5") for n in G.nodes]
            labels = {n: G.nodes[n].get("label", n) for n in G.nodes}
            nx.draw(G, pos, ax=ax, labels=labels, node_color=colors,
                    node_size=1500, font_size=9, font_color="white",
                    font_weight="bold", edge_color="#9CA3AF", arrows=True)
            edge_labels = nx.get_edge_attributes(G, "label")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=ax)
            plt.savefig(output, dpi=150, bbox_inches="tight")
            plt.close()
            return ToolResult(True, f"✓ Network diagram saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool create_network_diagram failed: {e}")

    @staticmethod
    def create_gantt(
        tasks: List[dict],
        output: str = "gantt.png",
    ) -> ToolResult:
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            fig, ax = plt.subplots(figsize=(14, max(4, len(tasks) * 0.6 + 2)))
            colors = ["#4F46E5", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"]
            max_end = max(t.get("end", t.get("start", 0) + 1) for t in tasks)
            for i, task in enumerate(tasks):
                start = task.get("start", 0)
                end   = task.get("end", start + 1)
                name  = task.get("name", f"Task {i+1}")
                color = colors[i % len(colors)]
                ax.barh(i, end - start, left=start, height=0.6,
                        color=color, alpha=0.85, edgecolor="white")
                ax.text(start + (end - start) / 2, i, name,
                        ha="center", va="center", fontsize=8, color="white", weight="bold")
            ax.set_yticks(range(len(tasks)))
            ax.set_yticklabels([t.get("name", f"Task {i+1}") for i, t in enumerate(tasks)])
            ax.set_xlabel("Time Units")
            ax.set_title("Gantt Chart", fontsize=14, weight="bold")
            ax.set_xlim(0, max_end + 1)
            ax.grid(axis="x", alpha=0.3)
            plt.tight_layout()
            plt.savefig(output, dpi=150, bbox_inches="tight")
            plt.close()
            return ToolResult(True, f"✓ Gantt chart saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool create_gantt failed: {e}")

    @staticmethod
    def create_mindmap(
        root: str,
        children: dict,
        output: str = "mindmap.png",
    ) -> ToolResult:
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            G = nx.Graph()
            G.add_node(root)
            positions = {root: (0, 0)}
            all_nodes = [root]

            def add_children(parent, kids, depth=1, angle_start=0, angle_span=2 * math.pi):
                if isinstance(kids, dict):
                    items = list(kids.items())
                else:
                    items = [(k, {}) for k in kids]
                n = len(items)
                for i, (child, grandkids) in enumerate(items):
                    angle = angle_start + (i + 0.5) * angle_span / n
                    r = depth * 2.5
                    x = r * math.cos(angle)
                    y = r * math.sin(angle)
                    G.add_node(child)
                    G.add_edge(parent, child)
                    positions[child] = (x, y)
                    all_nodes.append(child)
                    if grandkids:
                        add_children(child, grandkids, depth + 1,
                                     angle - angle_span / n / 2, angle_span / n)

            add_children(root, children)
            fig, ax = plt.subplots(figsize=(14, 10))
            node_colors = ["#4F46E5" if n == root else "#A78BFA" for n in G.nodes]
            nx.draw(G, positions, ax=ax, labels={n: n for n in G.nodes},
                    node_color=node_colors, node_size=1200,
                    font_size=8, font_color="white", font_weight="bold",
                    edge_color="#C4B5FD")
            ax.set_title(f"Mind Map: {root}", fontsize=14, weight="bold")
            plt.savefig(output, dpi=150, bbox_inches="tight")
            plt.close()
            return ToolResult(True, f"✓ Mind map saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool create_mindmap failed: {e}")

    @staticmethod
    def create_org_chart(
        hierarchy: dict,
        output: str = "org_chart.png",
    ) -> ToolResult:
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            G = nx.DiGraph()

            def build(node, parent=None):
                name = node.get("name", "?")
                G.add_node(name, title=node.get("title", ""))
                if parent:
                    G.add_edge(parent, name)
                for child in node.get("children", []):
                    build(child, name)

            build(hierarchy)
            pos = nx.drawing.nx_agraph.graphviz_layout(G, prog="dot") \
                if shutil.which("dot") else nx.spring_layout(G, seed=1)
            fig, ax = plt.subplots(figsize=(14, 8))
            nx.draw(G, pos, ax=ax,
                    labels={n: n for n in G.nodes},
                    node_color="#4F46E5", node_size=2000,
                    font_size=8, font_color="white", font_weight="bold",
                    edge_color="#9CA3AF", arrows=True)
            plt.savefig(output, dpi=150, bbox_inches="tight")
            plt.close()
            return ToolResult(True, f"✓ Org chart saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool create_org_chart failed: {e}")

    @staticmethod
    def render_mermaid(
        mermaid_code: str,
        output: str = "diagram.png",
        format: str = "png",
    ) -> ToolResult:
        try:
            mmdc = shutil.which("mmdc") or shutil.which("mermaid")
            if not mmdc:
                # Try npx
                if not shutil.which("npx"):
                    return ToolResult(False, "✗ mermaid-js (mmdc) not found. Install: npm install -g @mermaid-js/mermaid-cli")
                mmdc_cmd = ["npx", "-y", "@mermaid-js/mermaid-cli", "mmdc"]
            else:
                mmdc_cmd = [mmdc]
            tmp = tempfile.NamedTemporaryFile(suffix=".mmd", delete=False, mode="w", encoding="utf-8")
            tmp.write(mermaid_code)
            tmp.close()
            result = subprocess.run(
                mmdc_cmd + ["-i", tmp.name, "-o", output],
                capture_output=True, text=True, timeout=60,
            )
            os.unlink(tmp.name)
            if result.returncode == 0:
                return ToolResult(True, f"✓ Mermaid diagram rendered to {output}")
            return ToolResult(False, f"✗ Mermaid render failed: {result.stderr}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool render_mermaid failed: {e}")

    @staticmethod
    def render_plantuml(
        puml_code: str,
        output: str = "diagram.png",
        format: str = "png",
    ) -> ToolResult:
        try:
            puml_jar = shutil.which("plantuml")
            if not puml_jar:
                # Try java -jar plantuml.jar
                jar_path = Path.home() / ".npmai_agent" / "plantuml.jar"
                if not jar_path.exists():
                    import requests
                    r = requests.get(
                        "https://github.com/plantuml/plantuml/releases/download/v1.2024.3/plantuml-1.2024.3.jar",
                        stream=True, timeout=120,
                    )
                    r.raise_for_status()
                    jar_path.parent.mkdir(exist_ok=True)
                    jar_path.write_bytes(r.content)
                java = shutil.which("java")
                if not java:
                    return ToolResult(False, "✗ Java not found. Install Java to use PlantUML.")
                cmd_prefix = [java, "-jar", str(jar_path)]
            else:
                cmd_prefix = [puml_jar]
            tmp = tempfile.NamedTemporaryFile(suffix=".puml", delete=False, mode="w", encoding="utf-8")
            tmp.write(puml_code)
            tmp.close()
            result = subprocess.run(
                cmd_prefix + [f"-t{format}", "-pipe"],
                input=puml_code, capture_output=True, timeout=60,
            )
            os.unlink(tmp.name)
            if result.returncode == 0 and result.stdout:
                Path(output).write_bytes(result.stdout)
                return ToolResult(True, f"✓ PlantUML diagram rendered to {output}")
            return ToolResult(False, f"✗ PlantUML render failed: {result.stderr.decode()}")
        except Exception as e:
            return ToolResult(False, f"✗ DiagramTool render_plantuml failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 9. PrintTool
# ─────────────────────────────────────────────────────────────────────────────

class PrintTool:
    name = "print"
    description = (
        "Print-ready document generation: business cards, flyers, posters, "
        "brochures, certificates, label sheets, letterheads, and bleed marks."
    )
    use = (
           """ Name of Tool:- PrintTool

Purpose of Tool:- 
The PrintTool is a dedicated programmatic document design and prepress engine built to compile print-ready branding materials and localized templates. It constructs highly formatted, vector-based PDF structures conforming to standard commercial media dimensions (such as A3, A4, and Letter shapes) and strict geometric layouts. The suite features automated background painting, geometric accent dividers, content wrapper string splitting, multi-panel brochure folds, and matrix addressing alignments. Crucially for physical workflows, it also provides an automated prepress registration utility that alters native document bounding containers to merge localized bleed bounds and precision corner target lines for standard press cutting systems.

Methods:-
- create_business_card: Compiles identity records, branding vectors, and details into custom 3.5" x 2" landscape PDF cards.
- create_flyer: Packages visual image columns and structural copy paragraphs together into promotional media.
- create_poster: Generates high-impact, wide-format marketing or informational placards using structured background motifs.
- create_brochure: Implements geometric division paths and folding indicator marks to space multi-column panels dynamically.
- create_certificate: Produces official merit sheets overlaid with complex double-bordered tracking loops and authorization lines.
- create_label_sheet: Distributes cell coordinates down a grid sheet to output uniform commercial mailing indicators.
- create_letterhead: Locks institutional contact configurations, tagline headers, and branding logos into official documentation blocks.
- add_bleed_marks: Expands media canvas layers to superimpose registration and margin corner lines for printer cropping.

How to use Tool Methods:-

1. create_business_card:
   - Purpose: Generates high-density corporate layout identifiers ready for commercial paper stocks.
   - Arguments:
     a) name: str - Target person identity token line.
     b) title: str - Professional title or corporate department string.
     c) email: str - Contact address parameter.
     d) phone: str - Communication contact string value.
     e) website: str (default: "") - Online portal destination map link.
     f) logo: Optional[str] (default: None) - File reference pointing to a custom badge or image layer.
     g) output: str (default: "business_card.pdf") - Local target storage destination tracker.
     h) size: tuple (default: (3.5, 2)) - Physical canvas dimensional parameters in inches.
   - Returns: ToolResult tracking asset file completion metrics.
   - How to call: PrintTool.create_business_card(name="Alex Smith", title="Art Director", email="alex@studio.com", phone="555-0192", logo="assets/logo.png")

2. create_flyer:
   - Purpose: Constructs hand-out distributions or bulletin notices quickly and efficiently.
   - Arguments:
     a) title: str - Prominent structural title banner message.
     b) content: str - Detailed descriptions or info text blocks.
     c) images: Optional[List[str]] (default: None) - Array of local asset image references to scale underneath the heading banner.
     d) output: str (default: "flyer.pdf") - Target local saving path string identifier.
     e) size: str (default: "A4") - Hardcopy manufacturing size standard ("A4", "LETTER").
     f) orientation: str (default: "portrait") - Structural canvas layout direction ("portrait", "landscape").
   - Returns: ToolResult certifying graphic calculation outcomes.
   - How to call: PrintTool.create_flyer(title="Summer Festival", content="Join us for music and food!", images=["fest.png"], size="Letter")

3. create_poster:
   - Purpose: Formats large event signage, showcase diagrams, or wall notices.
   - Arguments:
     a) title: str - Center headline message text string.
     b) subtitle: str - Supporting contextual text string value.
     c) content: str - Body tracking instructions or paragraphs.
     d) background: str (default: "#1E3A5F") - Hex code styling background fill.
     e) output: str (default: "poster.pdf") - Export storage marker location tracker.
     b) size: str (default: "A3") - Dimensional surface standard string ("A3", "A4").
   - Returns: ToolResult indicating visual document validation markers.
   - How to call: PrintTool.create_poster(title="TECH CON 2026", subtitle="The Future is Now", content="Keynotes, labs, and panels.", background="#111827")

4. create_brochure:
   - Purpose: Maps complex promotional folds and product menus out neatly onto a single document sheet.
   - Arguments:
     a) sections: List[dict] - Structural data nodes holding `title` and `content` properties for individual panels.
     b) output: str (default: "brochure.pdf") - Local file system string tracking endpoint targets.
     c) folds: int (default: 2) - Number of mechanical fold segments (e.g., 2 folds creates a 3-panel trifold brochure).
   - Returns: ToolResult confirming vector rendering integrity.
   - How to call: PrintTool.create_brochure(sections=[{"title": "About", "content": "We do tech."}, {"title": "Services", "content": "Cloud computing."}], folds=2)

5. create_certificate:
   - Purpose: Automates corporate recognition plaques, course completions, or award tracking programs.
   - Arguments:
     a) template: str - Primary award headline text.
     b) data: dict - Node containing key details such as `recipient`, `achievement`, `date`, and `issuer`.
     c) output: str (default: "certificate.pdf") - Local output path target string.
   - Returns: ToolResult verifying layout composition metrics.
   - How to call: PrintTool.create_certificate(template="Diploma of Excellence", data={"recipient": "Jane Doe", "achievement": "First Place", "date": "2026-06-16", "issuer": "Academy"})

6. create_label_sheet:
   - Purpose: Automates structural print grids matching standard adhesive sheet templates like Avery.
   - Arguments:
     a) labels_data: List[dict] - Array of identity details tracking dictionary values (`name`, `line1`, `line2`, `line3`).
     b) template: str (default: "avery_5160") - Predefined standard alignment parameters map identity key ("avery_5160", "avery_5163").
     c) output: str (default: "labels.pdf") - File destination path tracker reference mapping.
     d) paper_size: str (default: "LETTER") - Target substrate size choice tracking standard media profiles ("LETTER", "A4").
   - Returns: ToolResult tracking address compilation tally details.
   - How to call: PrintTool.create_label_sheet(labels_data=[{"name": "Warehouse", "line1": "123 Ind. Way"}], template="avery_5163")

7. create_letterhead:
   - Purpose: Prepares standard corporate communication sheets with official institutional branding.
   - Arguments:
     a) logo: Optional[str] - Path reference tracking company visual branding graphics.
     b) company_info: dict - Dictionary holding fields such as `name`, `tagline`, `address`, `phone`, `email`, and `website`.
     c) output: str (default: "letterhead.pdf") - Vector file workspace tracking target destination.
   - Returns: ToolResult tracking visual document generation markers.
   - How to call: PrintTool.create_letterhead(logo="brand/logo.png", company_info={"name": "Nexus Corp", "tagline": "Connecting People"})

8. add_bleed_marks:
   - Purpose: Modifies standard PDF containers to insert margin boundaries and cutting guides for production houses.
   - Arguments:
     a) input: str - Location pointer tracking the source input PDF document.
     b) output: str - Target local saving path string tracking expanded margins outputs.
     c) bleed_size: float (default: 3.0) - Structural border width offset tracking parameters measured in millimeters.
   - Returns: ToolResult logging processed prepress updates.
   - How to call: PrintTool.add_bleed_marks(input="drafts/flyer.pdf", output="production/flyer_w_bleed.pdf", bleed_size=4.0)
   """)

    @staticmethod
    def create_business_card(
        name: str,
        title: str,
        email: str,
        phone: str,
        website: str = "",
        logo: Optional[str] = None,
        output: str = "business_card.pdf",
        size: tuple = (3.5, 2),
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import inch
            from reportlab.pdfgen import canvas as rl_canvas
            from reportlab.lib import colors
            w, h = size[0] * inch, size[1] * inch
            c = rl_canvas.Canvas(output, pagesize=(w, h))
            # Background
            c.setFillColor(colors.HexColor("#1E3A5F"))
            c.rect(0, 0, w, h, fill=True, stroke=False)
            # Accent bar
            c.setFillColor(colors.HexColor("#4F46E5"))
            c.rect(0, h * 0.6, w, 3, fill=True, stroke=False)
            # Logo
            if logo and Path(logo).exists():
                c.drawImage(logo, 10, h - 40, width=30, height=30, preserveAspectRatio=True, mask="auto")
            # Name
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(12, h * 0.65, name)
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.HexColor("#A5B4FC"))
            c.drawString(12, h * 0.55, title)
            # Contact
            c.setFillColor(colors.white)
            c.setFont("Helvetica", 8)
            line_y = h * 0.42
            for item in [email, phone, website]:
                if item:
                    c.drawString(12, line_y, item)
                    line_y -= 12
            c.save()
            return ToolResult(True, f"✓ Business card saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ PrintTool create_business_card failed: {e}")

    @staticmethod
    def create_flyer(
        title: str,
        content: str,
        images: Optional[List[str]] = None,
        output: str = "flyer.pdf",
        size: str = "A4",
        orientation: str = "portrait",
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait
            from reportlab.pdfgen import canvas as rl_canvas
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            size_map = {"A4": A4, "LETTER": LETTER}
            ps = size_map.get(size.upper(), A4)
            if orientation.lower() == "landscape":
                ps = landscape(ps)
            w, h = ps
            c = rl_canvas.Canvas(output, pagesize=ps)
            # Header
            c.setFillColor(colors.HexColor("#4F46E5"))
            c.rect(0, h - 80, w, 80, fill=True, stroke=False)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(w / 2, h - 50, title)
            # Images
            img_y = h - 120
            if images:
                img_w = (w - 40) / min(len(images), 3)
                for i, img_path in enumerate(images[:3]):
                    if Path(img_path).exists():
                        c.drawImage(img_path, 20 + i * img_w, img_y - 150,
                                    width=img_w - 10, height=140, preserveAspectRatio=True)
                img_y -= 160
            # Content
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 11)
            from reportlab.lib.utils import simpleSplit
            lines = simpleSplit(content, "Helvetica", 11, w - 40)
            y = img_y - 20
            for line in lines:
                if y < 40:
                    break
                c.drawString(20, y, line)
                y -= 16
            c.save()
            return ToolResult(True, f"✓ Flyer saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ PrintTool create_flyer failed: {e}")

    @staticmethod
    def create_poster(
        title: str,
        subtitle: str,
        content: str,
        background: str = "#1E3A5F",
        output: str = "poster.pdf",
        size: str = "A3",
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import A3, A4
            from reportlab.pdfgen import canvas as rl_canvas
            from reportlab.lib import colors
            from reportlab.lib.utils import simpleSplit
            ps = A3 if size.upper() == "A3" else A4
            w, h = ps
            c = rl_canvas.Canvas(output, pagesize=ps)
            # Background
            c.setFillColor(colors.HexColor(background))
            c.rect(0, 0, w, h, fill=True, stroke=False)
            # Decorative circles
            c.setFillColor(colors.HexColor("#4F46E530"))
            c.circle(w * 0.85, h * 0.85, 150, fill=True, stroke=False)
            c.circle(w * 0.1, h * 0.15, 100, fill=True, stroke=False)
            # Title
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 48)
            c.drawCentredString(w / 2, h * 0.72, title)
            # Subtitle
            c.setFont("Helvetica", 24)
            c.setFillColor(colors.HexColor("#A5B4FC"))
            c.drawCentredString(w / 2, h * 0.64, subtitle)
            # Divider
            c.setStrokeColor(colors.HexColor("#4F46E5"))
            c.setLineWidth(3)
            c.line(w * 0.2, h * 0.61, w * 0.8, h * 0.61)
            # Content
            c.setFillColor(colors.white)
            c.setFont("Helvetica", 14)
            lines = simpleSplit(content, "Helvetica", 14, w - 100)
            y = h * 0.55
            for line in lines[:20]:
                c.drawCentredString(w / 2, y, line)
                y -= 20
            c.save()
            return ToolResult(True, f"✓ Poster saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ PrintTool create_poster failed: {e}")

    @staticmethod
    def create_brochure(
        sections: List[dict],
        output: str = "brochure.pdf",
        folds: int = 2,
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.pdfgen import canvas as rl_canvas
            from reportlab.lib import colors
            from reportlab.lib.utils import simpleSplit
            ps = landscape(A4)
            w, h = ps
            c = rl_canvas.Canvas(output, pagesize=ps)
            panel_w = w / (folds + 1)
            panel_colors = ["#4F46E5", "#7C3AED", "#2563EB", "#059669"]
            for i, section in enumerate(sections[:folds + 1]):
                x = i * panel_w
                # Panel background (alternating)
                if i % 2 == 0:
                    c.setFillColor(colors.white)
                else:
                    c.setFillColor(colors.HexColor("#F8FAFC"))
                c.rect(x, 0, panel_w, h, fill=True, stroke=False)
                # Header bar
                hcolor = panel_colors[i % len(panel_colors)]
                c.setFillColor(colors.HexColor(hcolor))
                c.rect(x, h - 70, panel_w, 70, fill=True, stroke=False)
                # Title
                c.setFillColor(colors.white)
                c.setFont("Helvetica-Bold", 14)
                c.drawCentredString(x + panel_w / 2, h - 40, section.get("title", f"Panel {i+1}"))
                # Content
                c.setFillColor(colors.HexColor("#1F2937"))
                c.setFont("Helvetica", 9)
                body = section.get("content", "")
                lines = simpleSplit(body, "Helvetica", 9, panel_w - 20)
                y = h - 90
                for line in lines[:30]:
                    if y < 30:
                        break
                    c.drawString(x + 10, y, line)
                    y -= 13
                # Fold marks
                if i > 0:
                    c.setStrokeColor(colors.HexColor("#E5E7EB"))
                    c.setDash(3, 3)
                    c.line(x, 0, x, h)
                    c.setDash()
            c.save()
            return ToolResult(True, f"✓ Brochure saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ PrintTool create_brochure failed: {e}")

    @staticmethod
    def create_certificate(
        template: str,
        data: dict,
        output: str = "certificate.pdf",
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.pdfgen import canvas as rl_canvas
            from reportlab.lib import colors
            ps = landscape(A4)
            w, h = ps
            c = rl_canvas.Canvas(output, pagesize=ps)
            # Background
            c.setFillColor(colors.white)
            c.rect(0, 0, w, h, fill=True, stroke=False)
            # Border
            c.setStrokeColor(colors.HexColor("#4F46E5"))
            c.setLineWidth(8)
            c.rect(20, 20, w - 40, h - 40, fill=False, stroke=True)
            c.setLineWidth(2)
            c.rect(30, 30, w - 60, h - 60, fill=False, stroke=True)
            # Title
            c.setFillColor(colors.HexColor("#4F46E5"))
            c.setFont("Helvetica-Bold", 36)
            c.drawCentredString(w / 2, h - 100, template or "Certificate of Achievement")
            # Recipient
            c.setFillColor(colors.HexColor("#1F2937"))
            c.setFont("Helvetica", 16)
            c.drawCentredString(w / 2, h * 0.55, "This certifies that")
            c.setFont("Helvetica-Bold", 28)
            c.setFillColor(colors.HexColor("#4F46E5"))
            c.drawCentredString(w / 2, h * 0.46, data.get("recipient", ""))
            # Achievement
            c.setFillColor(colors.HexColor("#1F2937"))
            c.setFont("Helvetica", 14)
            c.drawCentredString(w / 2, h * 0.38, data.get("achievement", ""))
            # Date / Issuer
            c.setFont("Helvetica", 11)
            c.drawString(80, 80, f"Date: {data.get('date', '')}")
            c.drawString(80, 60, f"Issued by: {data.get('issuer', '')}")
            # Signature line
            c.setStrokeColor(colors.HexColor("#9CA3AF"))
            c.line(w - 250, 80, w - 60, 80)
            c.setFont("Helvetica", 9)
            c.drawCentredString(w - 155, 68, "Authorized Signature")
            c.save()
            return ToolResult(True, f"✓ Certificate saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ PrintTool create_certificate failed: {e}")

    @staticmethod
    def create_label_sheet(
        labels_data: List[dict],
        template: str = "avery_5160",
        output: str = "labels.pdf",
        paper_size: str = "LETTER",
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import LETTER, A4
            from reportlab.lib.units import inch
            from reportlab.pdfgen import canvas as rl_canvas
            from reportlab.lib import colors
            from reportlab.lib.utils import simpleSplit
            TEMPLATES = {
                "avery_5160": {"cols": 3, "rows": 10, "label_w": 2.625 * inch, "label_h": 1.0 * inch,
                               "margin_x": 0.1875 * inch, "margin_y": 0.5 * inch},
                "avery_5163": {"cols": 2, "rows": 5, "label_w": 4.0 * inch, "label_h": 2.0 * inch,
                               "margin_x": 0.15 * inch, "margin_y": 0.5 * inch},
            }
            tmpl = TEMPLATES.get(template, TEMPLATES["avery_5160"])
            ps   = LETTER if paper_size.upper() == "LETTER" else A4
            w, h = ps
            c = rl_canvas.Canvas(output, pagesize=ps)
            label_idx = 0
            page_started = True
            for row in range(tmpl["rows"]):
                for col in range(tmpl["cols"]):
                    if label_idx >= len(labels_data):
                        break
                    lx = tmpl["margin_x"] + col * tmpl["label_w"]
                    ly = h - tmpl["margin_y"] - (row + 1) * tmpl["label_h"]
                    label = labels_data[label_idx]
                    # Draw label border (faint)
                    c.setStrokeColor(colors.HexColor("#E5E7EB"))
                    c.setLineWidth(0.5)
                    c.rect(lx, ly, tmpl["label_w"] - 4, tmpl["label_h"] - 4)
                    # Content
                    c.setFillColor(colors.black)
                    text_lines = []
                    for k in ["name", "line1", "line2", "line3"]:
                        if k in label:
                            text_lines.append(label[k])
                    c.setFont("Helvetica-Bold" if text_lines else "Helvetica", 9)
                    ty = ly + tmpl["label_h"] - 20
                    for i, line in enumerate(text_lines[:4]):
                        c.setFont("Helvetica-Bold" if i == 0 else "Helvetica", 9)
                        c.drawString(lx + 6, ty, line)
                        ty -= 13
                    label_idx += 1
            c.save()
            return ToolResult(True, f"✓ Label sheet saved to {output} ({len(labels_data)} labels)")
        except Exception as e:
            return ToolResult(False, f"✗ PrintTool create_label_sheet failed: {e}")

    @staticmethod
    def create_letterhead(
        logo: Optional[str],
        company_info: dict,
        output: str = "letterhead.pdf",
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas as rl_canvas
            from reportlab.lib import colors
            w, h = A4
            c = rl_canvas.Canvas(output, pagesize=A4)
            # Header bar
            c.setFillColor(colors.HexColor("#1E3A5F"))
            c.rect(0, h - 90, w, 90, fill=True, stroke=False)
            # Logo
            if logo and Path(logo).exists():
                c.drawImage(logo, 20, h - 80, width=60, height=60,
                            preserveAspectRatio=True, mask="auto")
            # Company name
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(100, h - 40, company_info.get("name", "Company Name"))
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.HexColor("#A5B4FC"))
            c.drawString(100, h - 56, company_info.get("tagline", ""))
            # Contact bar
            c.setFillColor(colors.HexColor("#4F46E5"))
            c.rect(0, h - 110, w, 20, fill=True, stroke=False)
            c.setFillColor(colors.white)
            c.setFont("Helvetica", 8)
            contact_str = "  |  ".join(filter(None, [
                company_info.get("address", ""),
                company_info.get("phone", ""),
                company_info.get("email", ""),
                company_info.get("website", ""),
            ]))
            c.drawCentredString(w / 2, h - 105, contact_str)
            # Footer
            c.setFillColor(colors.HexColor("#1E3A5F"))
            c.rect(0, 0, w, 40, fill=True, stroke=False)
            c.setFillColor(colors.white)
            c.setFont("Helvetica", 8)
            c.drawCentredString(w / 2, 15, contact_str)
            c.save()
            return ToolResult(True, f"✓ Letterhead saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ PrintTool create_letterhead failed: {e}")

    @staticmethod
    def add_bleed_marks(
        input: str,
        output: str,
        bleed_size: float = 3.0,
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import mm
            from pypdf import PdfReader, PdfWriter
            from reportlab.pdfgen import canvas as rl_canvas
            from reportlab.lib import colors
            import io
            reader = PdfReader(input)
            writer = PdfWriter()
            bleed_pt = bleed_size * mm
            for page in reader.pages:
                orig_w = float(page.mediabox.width)
                orig_h = float(page.mediabox.height)
                new_w  = orig_w + 2 * bleed_pt
                new_h  = orig_h + 2 * bleed_pt
                # Create overlay with crop marks
                packet = io.BytesIO()
                c = rl_canvas.Canvas(packet, pagesize=(new_w, new_h))
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.5)
                mark_len = 10
                # Top-left
                c.line(0, new_h - bleed_pt, mark_len, new_h - bleed_pt)
                c.line(bleed_pt, new_h, bleed_pt, new_h - mark_len)
                # Top-right
                c.line(new_w - mark_len, new_h - bleed_pt, new_w, new_h - bleed_pt)
                c.line(new_w - bleed_pt, new_h, new_w - bleed_pt, new_h - mark_len)
                # Bottom-left
                c.line(0, bleed_pt, mark_len, bleed_pt)
                c.line(bleed_pt, 0, bleed_pt, mark_len)
                # Bottom-right
                c.line(new_w - mark_len, bleed_pt, new_w, bleed_pt)
                c.line(new_w - bleed_pt, 0, new_w - bleed_pt, mark_len)
                c.save()
                packet.seek(0)
                from pypdf import PdfReader as PDFReader2
                overlay_page = PDFReader2(packet).pages[0]
                overlay_page.merge_page(page)
                writer.add_page(overlay_page)
            with open(output, "wb") as out_f:
                writer.write(out_f)
            return ToolResult(True, f"✓ Bleed marks added to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ PrintTool add_bleed_marks failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 10. ThreeDTool
# ─────────────────────────────────────────────────────────────────────────────

class ThreeDTool:
    name = "3d"
    description = (
        "3D model utilities without Blender: view, inspect, convert formats, "
        "optimize mesh, center, scale, merge models, generate thumbnails."
    )
    use = (
           """
Name of Tool:- ThreeDTool,

Purpose of Tool:- 
The ThreeDTool provides a lightweight, Blender-independent interface for working with 3D models using the trimesh library (with optional pyrender for advanced rendering). 
It supports loading/inspecting models, format conversion, mesh optimization (decimation), centering and scaling, merging multiple models, and generating high-quality thumbnails. 
This tool is ideal for 3D asset pipelines, model validation, batch processing, thumbnail generation, and agentic 3D content management without requiring a full 3D modeling suite.

Methods:-
- _load_mesh: Internal helper to load a 3D model using trimesh.
- view_model: Opens an interactive 3D viewer window for the model.
- get_model_info: Returns detailed geometric and topological information about a model.
- convert_model: Converts a 3D model between supported formats (OBJ, FBX, GLB, STL, etc.).
- optimize_mesh: Reduces the complexity of a mesh (face count) while preserving shape.
- center_model: Translates the model so its centroid is at the origin.
- scale_model: Uniformly scales the model by a given factor.
- merge_models: Combines multiple 3D models into a single mesh.
- generate_thumbnail: Renders a static 2D thumbnail image of the 3D model (uses pyrender when available, falls back to trimesh).

How to use Tool Methods:-

1. _load_mesh (Internal Helper):
   - Purpose: Loads a 3D model file into a trimesh object.
   - Arguments: file: str - Path to the 3D model file.
   - Note: Internal method used by most operations. Supports OBJ, FBX, GLB, STL, PLY, and many others.

2. view_model:
   - Purpose: Opens an interactive 3D viewer window to visually inspect the model.
   - Arguments: file: str - Path to the 3D model.
   - How to call: ThreeDTool.view_model(file="model.obj")

3. get_model_info:
   - Purpose: Returns comprehensive metadata about the 3D model including vertex/face count, volume, surface area, bounds, etc.
   - Arguments: file: str - Path to the 3D model.
   - Returns: Dictionary with geometric statistics.
   - How to call: ThreeDTool.get_model_info(file="model.glb")

4. convert_model:
   - Purpose: Converts a 3D model from one format to another.
   - Arguments:
     a) input: str - Input model file path.
     b) output: str - Desired output file path (extension determines format).
     c) target_format: str - Explicit target format (e.g., "obj", "glb").
   - How to call: ThreeDTool.convert_model(input="model.fbx", output="model.glb", target_format="glb")

5. optimize_mesh:
   - Purpose: Reduces polygon count (decimation) to optimize the model for performance while preserving shape.
   - Arguments:
     a) input: str - Input model path.
     b) output: str - Output optimized model path.
     c) target_faces: int (default: 10000) - Desired maximum number of faces.
   - How to call: ThreeDTool.optimize_mesh(input="highpoly.obj", output="optimized.obj", target_faces=5000)

6. center_model:
   - Purpose: Centers the model at the origin (0,0,0) by translating its centroid.
   - Arguments:
     a) input: str
     b) output: str
   - How to call: ThreeDTool.center_model(input="model.obj", output="centered.obj")

7. scale_model:
   - Purpose: Applies uniform scaling to the entire model.
   - Arguments:
     a) input: str
     b) output: str
     c) scale: float - Scaling factor (e.g., 0.5 for half size, 2.0 for double).
   - How to call: ThreeDTool.scale_model(input="model.obj", output="scaled.obj", scale=0.1)

8. merge_models:
   - Purpose: Combines multiple 3D models into a single mesh file.
   - Arguments:
     a) inputs: List[str] - List of input model file paths.
     b) output: str - Output merged model path.
   - How to call: ThreeDTool.merge_models(inputs=["part1.obj", "part2.obj"], output="combined.glb")

9. generate_thumbnail:
   - Purpose: Renders a static 2D thumbnail image of the 3D model from a nice angle.
   - Arguments:
     a) model_file: str - Path to the 3D model.
     b) output: str (default: "thumbnail.png")
     c) width, height: int (default: 512) - Thumbnail resolution.
     d) background_color: tuple (default: (255, 255, 255)) - RGB background.
   - How to call: ThreeDTool.generate_thumbnail(model_file="product.glb", output="thumb.png", width=1024, height=1024)
""")

    @staticmethod
    def _load_mesh(file: str):
        import trimesh
        mesh = trimesh.load(file, force="mesh")
        return mesh

    @staticmethod
    def view_model(file: str) -> ToolResult:
        try:
            import trimesh
            mesh = ThreeDTool._load_mesh(file)
            trimesh.viewer.windowed(mesh)
            return ToolResult(True, f"✓ Viewing model {file}")
        except Exception as e:
            return ToolResult(False, f"✗ ThreeDTool view_model failed: {e}")

    @staticmethod
    def get_model_info(file: str) -> ToolResult:
        try:
            import trimesh
            mesh = ThreeDTool._load_mesh(file)
            info = {
                "file": file,
                "vertices": len(mesh.vertices),
                "faces": len(mesh.faces),
                "is_watertight": bool(mesh.is_watertight),
                "volume": round(float(mesh.volume), 4) if mesh.is_watertight else None,
                "surface_area": round(float(mesh.area), 4),
                "bounds_min": mesh.bounds[0].tolist(),
                "bounds_max": mesh.bounds[1].tolist(),
                "extents": mesh.extents.tolist(),
                "center_mass": mesh.center_mass.tolist(),
            }
            return ToolResult(True, f"✓ Model info: {len(mesh.vertices)} verts, {len(mesh.faces)} faces", info)
        except Exception as e:
            return ToolResult(False, f"✗ ThreeDTool get_model_info failed: {e}")

    @staticmethod
    def convert_model(
        input: str,
        output: str,
        target_format: str,
    ) -> ToolResult:
        try:
            import trimesh
            mesh = trimesh.load(input)
            output_path = output if output.endswith(f".{target_format.lower()}") \
                else str(Path(output).with_suffix(f".{target_format.lower()}"))
            mesh.export(output_path)
            return ToolResult(True, f"✓ Model converted to {output_path}")
        except Exception as e:
            return ToolResult(False, f"✗ ThreeDTool convert_model failed: {e}")

    @staticmethod
    def optimize_mesh(
        input: str,
        output: str,
        target_faces: int = 10000,
    ) -> ToolResult:
        try:
            import trimesh
            mesh = trimesh.load(input, force="mesh")
            orig_faces = len(mesh.faces)
            if orig_faces <= target_faces:
                mesh.export(output)
                return ToolResult(True, f"✓ Mesh already has {orig_faces} faces (≤{target_faces}), copied to {output}")
            # Use open3d for decimation if available, else trimesh simplification
            try:
                import open3d as o3d
                o3d_mesh = o3d.io.read_triangle_mesh(input)
                simplified = o3d_mesh.simplify_quadric_decimation(target_faces)
                o3d.io.write_triangle_mesh(output, simplified)
                new_faces = len(simplified.triangles)
            except ImportError:
                # Fallback: trimesh doesn't have built-in decimation easily,
                # use vertex clustering
                mesh_simple = mesh.simplify_quadratic_decimation(target_faces)
                mesh_simple.export(output)
                new_faces = len(mesh_simple.faces)
            return ToolResult(True, f"✓ Mesh optimized: {orig_faces} → {new_faces} faces, saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ ThreeDTool optimize_mesh failed: {e}")

    @staticmethod
    def center_model(
        input: str,
        output: str,
    ) -> ToolResult:
        try:
            import trimesh
            mesh = trimesh.load(input, force="mesh")
            mesh.apply_translation(-mesh.centroid)
            mesh.export(output)
            return ToolResult(True, f"✓ Model centered at origin, saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ ThreeDTool center_model failed: {e}")

    @staticmethod
    def scale_model(
        input: str,
        output: str,
        scale: float,
    ) -> ToolResult:
        try:
            import trimesh
            mesh = trimesh.load(input, force="mesh")
            mesh.apply_scale(scale)
            mesh.export(output)
            return ToolResult(True, f"✓ Model scaled by {scale}x, saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ ThreeDTool scale_model failed: {e}")

    @staticmethod
    def merge_models(
        inputs: List[str],
        output: str,
    ) -> ToolResult:
        try:
            import trimesh
            meshes = [trimesh.load(f, force="mesh") for f in inputs]
            merged = trimesh.util.concatenate(meshes)
            merged.export(output)
            return ToolResult(True, f"✓ {len(inputs)} models merged, saved to {output}")
        except Exception as e:
            return ToolResult(False, f"✗ ThreeDTool merge_models failed: {e}")

    @staticmethod
    def generate_thumbnail(
        model_file: str,
        output: str = "thumbnail.png",
        width: int = 512,
        height: int = 512,
        background_color: tuple = (255, 255, 255),
    ) -> ToolResult:
        try:
            import trimesh
            mesh = trimesh.load(model_file, force="mesh")
            # Try pyrender first
            try:
                import pyrender
                import numpy as np
                scene   = pyrender.Scene(bg_color=[*[c / 255 for c in background_color], 1.0])
                tri_mesh = pyrender.Mesh.from_trimesh(mesh)
                scene.add(tri_mesh)
                # Auto camera
                centroid = mesh.centroid
                extent   = max(mesh.extents)
                camera_pose = np.array([
                    [1.0, 0.0, 0.0, centroid[0]],
                    [0.0, 1.0, 0.0, centroid[1]],
                    [0.0, 0.0, 1.0, centroid[2] + extent * 2],
                    [0.0, 0.0, 0.0, 1.0],
                ])
                camera = pyrender.PerspectiveCamera(yfov=math.radians(45))
                scene.add(camera, pose=camera_pose)
                light  = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=5.0)
                scene.add(light, pose=camera_pose)
                r = pyrender.OffscreenRenderer(width, height)
                color, _ = r.render(scene)
                r.delete()
                from PIL import Image
                Image.fromarray(color).save(output)
                return ToolResult(True, f"✓ Thumbnail saved to {output}")
            except ImportError:
                pass
            # Fallback: use trimesh built-in
            img_data = mesh.scene().save_image(resolution=(width, height))
            if img_data:
                with open(output, "wb") as f:
                    f.write(img_data)
                return ToolResult(True, f"✓ Thumbnail saved to {output}")
            return ToolResult(False, "✗ Could not render thumbnail (install pyrender for best results).")
        except Exception as e:
            return ToolResult(False, f"✗ ThreeDTool generate_thumbnail failed: {e}")
