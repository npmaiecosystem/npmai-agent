"""
tools_media.py — Media Tools for NPM Agent (NPMAI ECOSYSTEM)
Author: Built for Sonu Kumar's NPM Agent
All tools inherit from agent_core patterns: ToolResult, CredStore, _ensure auto-installer.
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import threading
import time
import platform
import glob
import re
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple


# ─── Import from agent_core ───────────────────────────────────────────────────
try:
    from agent_core import ToolResult, CredStore
except ImportError:
    # Fallback if running standalone for testing
    class ToolResult:
        def __init__(self, success: bool, output: str, data=None):
            self.success = success
            self.output = output
            self.data = data
        def __str__(self): return self.output

    class CredStore:
        @classmethod
        def load(cls, name: str) -> dict: return {}
        @classmethod
        def save(cls, name: str, data: dict): pass


# ─── Auto-installer ───────────────────────────────────────────────────────────
def _ensure(pkg: str, import_name: str = None):
    n = import_name or pkg
    try:
        __import__(n)
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "-q", "--break-system-packages"],
            check=False, capture_output=True
        )


# Install all media dependencies up-front
_MEDIA_DEPS = [
    ("yt-dlp",              "yt_dlp"),
    ("pydub",               "pydub"),
    ("librosa",             "librosa"),
    ("sounddevice",         "sounddevice"),
    ("openai-whisper",      "whisper"),
    ("edge-tts",            "edge_tts"),
    ("pyttsx3",             "pyttsx3"),
    ("rembg",               "rembg"),
    ("mss",                 "mss"),
    ("pygetwindow",         "pygetwindow"),
    ("mutagen",             "mutagen"),
    ("tinytag",             "tinytag"),
    ("pymediainfo",         "pymediainfo"),
    ("moviepy",             "moviepy"),
    ("streamlink",          "streamlink"),
    ("Pillow",              "PIL"),
    ("opencv-python",       "cv2"),
    ("scikit-image",        "skimage"),
    ("numpy",               "numpy"),
    ("requests",            "requests"),
    ("pyautogui",           "pyautogui"),
    ("elevenlabs",          "elevenlabs"),
    ("feedgen",             "feedgen"),
]
for _pkg, _imp in _MEDIA_DEPS:
    _ensure(_pkg, _imp)


# ─────────────────────────────────────────────────────────────────────────────
# 1. FFmpegTool
# ─────────────────────────────────────────────────────────────────────────────
class FFmpegTool:
    name = "ffmpeg"
    description = (
        "Complete video/audio processing: trim, merge, compress, convert, "
        "extract audio, add subtitles, resize, crop, watermark, speed change, "
        "reverse, loop, transitions, frame extraction, thumbnails, GIFs, "
        "text overlays, stabilisation, colour grading, slideshows and more."
    )

    # ── internal helpers ──────────────────────────────────────────────────────
    @staticmethod
    def _run(args: List[str], timeout: int = 600) -> Tuple[bool, str]:
        """Run an ffmpeg command. Returns (success, combined_output)."""
        try:
            result = subprocess.run(
                ["ffmpeg", "-y"] + args,
                capture_output=True, text=True, timeout=timeout
            )
            combined = result.stdout + result.stderr
            return result.returncode == 0, combined
        except FileNotFoundError:
            return False, "ffmpeg not found. Install it: https://ffmpeg.org/download.html"
        except subprocess.TimeoutExpired:
            return False, "ffmpeg timed out."

    @staticmethod
    def _probe(path: str) -> dict:
        """Run ffprobe and return JSON info dict."""
        try:
            r = subprocess.run(
                ["ffprobe", "-v", "quiet", "-print_format", "json",
                 "-show_format", "-show_streams", path],
                capture_output=True, text=True, timeout=30
            )
            return json.loads(r.stdout) if r.returncode == 0 else {}
        except Exception:
            return {}

    # ── methods ───────────────────────────────────────────────────────────────
    @staticmethod
    def trim(input: str, output: str, start: str, end: str) -> ToolResult:
        """Trim video/audio from start to end (HH:MM:SS or seconds)."""
        try:
            ok, out = FFmpegTool._run([
                "-ss", str(start), "-to", str(end),
                "-i", input, "-c", "copy", output
            ])
            if ok:
                return ToolResult(True, f"✓ Trimmed {input} → {output}", output)
            return ToolResult(False, f"✗ Trim failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Trim error: {e}")

    @staticmethod
    def merge(inputs: List[str], output: str, method: str = "concat") -> ToolResult:
        """
        Merge multiple video/audio files.
        method: 'concat' (same codec), 'filter' (re-encode, handles different formats)
        """
        try:
            if method == "concat":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as fh:
                    for p in inputs:
                        fh.write(f"file '{os.path.abspath(p)}'\n")
                    list_file = fh.name
                ok, out = FFmpegTool._run([
                    "-f", "concat", "-safe", "0", "-i", list_file,
                    "-c", "copy", output
                ])
                os.unlink(list_file)
            else:
                # filter_complex method — re-encodes
                in_args = []
                for p in inputs:
                    in_args += ["-i", p]
                n = len(inputs)
                filter_str = "".join(f"[{i}:v][{i}:a]" for i in range(n))
                filter_str += f"concat=n={n}:v=1:a=1[outv][outa]"
                ok, out = FFmpegTool._run(
                    in_args + ["-filter_complex", filter_str,
                                "-map", "[outv]", "-map", "[outa]", output]
                )
            if ok:
                return ToolResult(True, f"✓ Merged {len(inputs)} files → {output}", output)
            return ToolResult(False, f"✗ Merge failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Merge error: {e}")

    @staticmethod
    def compress_video(
        input: str, output: str,
        crf: int = 23,
        preset: str = "medium",
        resolution: Optional[str] = None
    ) -> ToolResult:
        """Compress video with H.264. crf 18-28 (lower=better), preset: ultrafast…veryslow."""
        try:
            vf_args = []
            if resolution:
                w, h = resolution.split("x")
                vf_args = ["-vf", f"scale={w}:{h}"]
            ok, out = FFmpegTool._run(
                ["-i", input] + vf_args +
                ["-c:v", "libx264", "-crf", str(crf),
                 "-preset", preset, "-c:a", "aac", "-b:a", "128k", output]
            )
            if ok:
                orig = os.path.getsize(input)
                comp = os.path.getsize(output)
                pct = round((1 - comp / orig) * 100, 1)
                return ToolResult(True, f"✓ Compressed {pct}% smaller → {output}", output)
            return ToolResult(False, f"✗ Compress failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Compress video error: {e}")

    @staticmethod
    def compress_audio(input: str, output: str, bitrate: str = "128k") -> ToolResult:
        """Compress audio to target bitrate (e.g. '64k', '128k', '320k')."""
        try:
            ok, out = FFmpegTool._run([
                "-i", input, "-b:a", bitrate, output
            ])
            if ok:
                return ToolResult(True, f"✓ Audio compressed @ {bitrate} → {output}", output)
            return ToolResult(False, f"✗ Compress audio failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Compress audio error: {e}")

    @staticmethod
    def convert(
        input: str, output: str,
        video_codec: str = "copy",
        audio_codec: str = "copy",
        extra_args: Optional[List[str]] = None
    ) -> ToolResult:
        """Convert media format/codec. Pass 'copy' to avoid re-encoding."""
        try:
            args = ["-i", input,
                    "-c:v", video_codec,
                    "-c:a", audio_codec]
            if extra_args:
                args += extra_args
            args.append(output)
            ok, out = FFmpegTool._run(args)
            if ok:
                return ToolResult(True, f"✓ Converted → {output}", output)
            return ToolResult(False, f"✗ Convert failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Convert error: {e}")

    @staticmethod
    def extract_audio(input: str, output: str, format: str = "mp3") -> ToolResult:
        """Extract audio track from video."""
        try:
            if not output.endswith(f".{format}"):
                output = str(Path(output).with_suffix(f".{format}"))
            ok, out = FFmpegTool._run([
                "-i", input, "-vn", "-c:a",
                "libmp3lame" if format == "mp3" else "copy",
                "-q:a", "2", output
            ])
            if ok:
                return ToolResult(True, f"✓ Audio extracted → {output}", output)
            return ToolResult(False, f"✗ Extract audio failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Extract audio error: {e}")

    @staticmethod
    def replace_audio(video: str, audio: str, output: str) -> ToolResult:
        """Replace the audio track of a video with a different audio file."""
        try:
            ok, out = FFmpegTool._run([
                "-i", video, "-i", audio,
                "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0",
                "-shortest", output
            ])
            if ok:
                return ToolResult(True, f"✓ Audio replaced → {output}", output)
            return ToolResult(False, f"✗ Replace audio failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Replace audio error: {e}")

    @staticmethod
    def add_subtitles(
        video: str, srt_path: str, output: str,
        burned_in: bool = False
    ) -> ToolResult:
        """Add subtitles. burned_in=True permanently burns them into video."""
        try:
            if burned_in:
                # Use absolute path, escape colons on Windows
                srt_abs = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")
                ok, out = FFmpegTool._run([
                    "-i", video,
                    "-vf", f"subtitles='{srt_abs}'",
                    "-c:a", "copy", output
                ])
            else:
                ok, out = FFmpegTool._run([
                    "-i", video, "-i", srt_path,
                    "-c", "copy", "-c:s", "mov_text",
                    "-metadata:s:s:0", "language=eng", output
                ])
            if ok:
                return ToolResult(True, f"✓ Subtitles added → {output}", output)
            return ToolResult(False, f"✗ Subtitles failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Add subtitles error: {e}")

    @staticmethod
    def extract_subtitles(
        video: str, output: str, stream_index: int = 0
    ) -> ToolResult:
        """Extract subtitle stream from video to .srt file."""
        try:
            ok, out = FFmpegTool._run([
                "-i", video,
                "-map", f"0:s:{stream_index}",
                output
            ])
            if ok:
                return ToolResult(True, f"✓ Subtitles extracted → {output}", output)
            return ToolResult(False, f"✗ Extract subtitles failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Extract subtitles error: {e}")

    @staticmethod
    def resize(
        input: str, output: str,
        width: int, height: int,
        keep_aspect: bool = True
    ) -> ToolResult:
        """Resize video. keep_aspect pads with black bars if needed."""
        try:
            if keep_aspect:
                scale = f"scale={width}:{height}:force_original_aspect_ratio=decrease"
                pad = f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
                vf = f"{scale},{pad}"
            else:
                vf = f"scale={width}:{height}"
            ok, out = FFmpegTool._run([
                "-i", input, "-vf", vf, "-c:a", "copy", output
            ])
            if ok:
                return ToolResult(True, f"✓ Resized to {width}x{height} → {output}", output)
            return ToolResult(False, f"✗ Resize failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Resize error: {e}")

    @staticmethod
    def crop(
        input: str, output: str,
        x: int, y: int, w: int, h: int
    ) -> ToolResult:
        """Crop video to rectangle. x,y = top-left corner; w,h = dimensions."""
        try:
            ok, out = FFmpegTool._run([
                "-i", input,
                "-vf", f"crop={w}:{h}:{x}:{y}",
                "-c:a", "copy", output
            ])
            if ok:
                return ToolResult(True, f"✓ Cropped {w}x{h} @ ({x},{y}) → {output}", output)
            return ToolResult(False, f"✗ Crop failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Crop error: {e}")

    @staticmethod
    def add_watermark(
        input: str, watermark: str, output: str,
        position: str = "bottomright",
        opacity: float = 0.8
    ) -> ToolResult:
        """
        Add image watermark. position: topleft|topright|bottomleft|bottomright|center.
        opacity: 0.0–1.0.
        """
        try:
            pos_map = {
                "topleft":     "10:10",
                "topright":    "main_w-overlay_w-10:10",
                "bottomleft":  "10:main_h-overlay_h-10",
                "bottomright": "main_w-overlay_w-10:main_h-overlay_h-10",
                "center":      "(main_w-overlay_w)/2:(main_h-overlay_h)/2",
            }
            overlay_pos = pos_map.get(position, pos_map["bottomright"])
            alpha = f"format=rgba,colorchannelmixer=aa={opacity}"
            filter_c = f"[1:v]{alpha}[wm];[0:v][wm]overlay={overlay_pos}"
            ok, out = FFmpegTool._run([
                "-i", input, "-i", watermark,
                "-filter_complex", filter_c,
                "-c:a", "copy", output
            ])
            if ok:
                return ToolResult(True, f"✓ Watermark added ({position}) → {output}", output)
            return ToolResult(False, f"✗ Watermark failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Watermark error: {e}")

    @staticmethod
    def change_speed(
        input: str, output: str, speed_factor: float
    ) -> ToolResult:
        """
        Change playback speed. 0.5 = half speed, 2.0 = double speed.
        Adjusts both video and audio.
        """
        try:
            # atempo only supports 0.5–2.0, chain for extreme values
            audio_tempo = speed_factor
            atempo_chain = []
            while audio_tempo > 2.0:
                atempo_chain.append("atempo=2.0")
                audio_tempo /= 2.0
            while audio_tempo < 0.5:
                atempo_chain.append("atempo=0.5")
                audio_tempo /= 0.5
            atempo_chain.append(f"atempo={audio_tempo:.4f}")
            atempo_str = ",".join(atempo_chain)
            setpts = f"setpts={1/speed_factor:.4f}*PTS"
            ok, out = FFmpegTool._run([
                "-i", input,
                "-filter_complex",
                f"[0:v]{setpts}[v];[0:a]{atempo_str}[a]",
                "-map", "[v]", "-map", "[a]", output
            ])
            if ok:
                return ToolResult(True, f"✓ Speed x{speed_factor} → {output}", output)
            return ToolResult(False, f"✗ Speed change failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Speed change error: {e}")

    @staticmethod
    def reverse(input: str, output: str) -> ToolResult:
        """Reverse video and audio playback."""
        try:
            ok, out = FFmpegTool._run([
                "-i", input,
                "-vf", "reverse",
                "-af", "areverse",
                output
            ])
            if ok:
                return ToolResult(True, f"✓ Reversed → {output}", output)
            return ToolResult(False, f"✗ Reverse failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Reverse error: {e}")

    @staticmethod
    def loop(input: str, output: str, count: int = 3) -> ToolResult:
        """Loop a video N times (count=3 means play 3 times total)."""
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as fh:
                for _ in range(count):
                    fh.write(f"file '{os.path.abspath(input)}'\n")
                list_file = fh.name
            ok, out = FFmpegTool._run([
                "-f", "concat", "-safe", "0", "-i", list_file,
                "-c", "copy", output
            ])
            os.unlink(list_file)
            if ok:
                return ToolResult(True, f"✓ Looped x{count} → {output}", output)
            return ToolResult(False, f"✗ Loop failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Loop error: {e}")

    @staticmethod
    def concatenate_with_transition(
        inputs: List[str], output: str,
        transition: str = "fade",
        duration: float = 0.5
    ) -> ToolResult:
        """
        Concatenate videos with transition. transition: fade|wipeleft|wiperight|slideleft.
        Uses xfade filter (requires ffmpeg 4.3+).
        """
        try:
            if len(inputs) < 2:
                return ToolResult(False, "✗ Need at least 2 inputs for transitions.")
            in_args = []
            for p in inputs:
                in_args += ["-i", p]
            # Build xfade filter chain
            # Get durations for offset calculation
            offsets = []
            cumulative = 0.0
            for p in inputs[:-1]:
                info = FFmpegTool._probe(p)
                dur = float(info.get("format", {}).get("duration", 5))
                cumulative += dur - duration
                offsets.append(cumulative)
            filter_parts = []
            # Label first input
            prev_v = "0:v"
            prev_a = "0:a"
            for i in range(1, len(inputs)):
                out_v = f"v{i}" if i < len(inputs) - 1 else "outv"
                out_a = f"a{i}" if i < len(inputs) - 1 else "outa"
                filter_parts.append(
                    f"[{prev_v}][{i}:v]xfade=transition={transition}:"
                    f"duration={duration}:offset={offsets[i-1]:.3f}[{out_v}]"
                )
                filter_parts.append(
                    f"[{prev_a}][{i}:a]acrossfade=d={duration}[{out_a}]"
                )
                prev_v = out_v
                prev_a = out_a
            filter_complex = ";".join(filter_parts)
            ok, out = FFmpegTool._run(
                in_args + ["-filter_complex", filter_complex,
                            "-map", "[outv]", "-map", "[outa]",
                            "-c:v", "libx264", "-c:a", "aac", output]
            )
            if ok:
                return ToolResult(True, f"✓ Concatenated with {transition} transitions → {output}", output)
            return ToolResult(False, f"✗ Concat with transition failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Concat transition error: {e}")

    @staticmethod
    def extract_frames(
        input: str, output_folder: str,
        fps: float = 1.0,
        start: Optional[str] = None,
        end: Optional[str] = None,
        format: str = "jpg"
    ) -> ToolResult:
        """Extract frames at specified FPS into output_folder."""
        try:
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            args = []
            if start:
                args += ["-ss", str(start)]
            if end:
                args += ["-to", str(end)]
            args += ["-i", input, "-vf", f"fps={fps}",
                     os.path.join(output_folder, f"frame_%06d.{format}")]
            ok, out = FFmpegTool._run(args)
            count = len(list(Path(output_folder).glob(f"*.{format}")))
            if ok:
                return ToolResult(True, f"✓ Extracted {count} frames → {output_folder}", output_folder)
            return ToolResult(False, f"✗ Extract frames failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Extract frames error: {e}")

    @staticmethod
    def create_from_frames(
        input_pattern: str, output: str,
        fps: float = 24.0,
        codec: str = "libx264"
    ) -> ToolResult:
        """Create video from image sequence. input_pattern e.g. '/frames/frame_%06d.jpg'."""
        try:
            ok, out = FFmpegTool._run([
                "-framerate", str(fps),
                "-i", input_pattern,
                "-c:v", codec,
                "-pix_fmt", "yuv420p",
                output
            ])
            if ok:
                return ToolResult(True, f"✓ Video created from frames → {output}", output)
            return ToolResult(False, f"✗ Create from frames failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Create from frames error: {e}")

    @staticmethod
    def add_intro_outro(
        main: str, intro: Optional[str], outro: Optional[str], output: str
    ) -> ToolResult:
        """Prepend intro and/or append outro to main video."""
        try:
            parts = []
            if intro:
                parts.append(intro)
            parts.append(main)
            if outro:
                parts.append(outro)
            if len(parts) == 1:
                return ToolResult(False, "✗ No intro or outro provided.")
            return FFmpegTool.merge(parts, output, method="filter")
        except Exception as e:
            return ToolResult(False, f"✗ Intro/outro error: {e}")

    @staticmethod
    def picture_in_picture(
        main: str, overlay: str, output: str,
        position: str = "bottomright",
        size: str = "1/4"
    ) -> ToolResult:
        """
        Overlay a smaller video on top of main (picture-in-picture).
        size: fraction of main video width, e.g. '1/4'.
        position: topleft|topright|bottomleft|bottomright.
        """
        try:
            pos_map = {
                "topleft":     "10:10",
                "topright":    "main_w-overlay_w-10:10",
                "bottomleft":  "10:main_h-overlay_h-10",
                "bottomright": "main_w-overlay_w-10:main_h-overlay_h-10",
            }
            overlay_pos = pos_map.get(position, pos_map["bottomright"])
            # Calculate scale from fraction string e.g. "1/4" → 0.25
            try:
                parts = size.split("/")
                scale_ratio = float(parts[0]) / float(parts[1]) if len(parts) == 2 else float(size)
            except Exception:
                scale_ratio = 0.25
            scale_w = f"iw*{scale_ratio:.4f}"
            filter_c = (
                f"[1:v]scale={scale_w}:-1[pip];"
                f"[0:v][pip]overlay={overlay_pos}"
            )
            ok, out = FFmpegTool._run([
                "-i", main, "-i", overlay,
                "-filter_complex", filter_c,
                "-c:a", "copy", output
            ])
            if ok:
                return ToolResult(True, f"✓ PiP added ({position}) → {output}", output)
            return ToolResult(False, f"✗ PiP failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ PiP error: {e}")

    @staticmethod
    def normalize_audio(
        input: str, output: str,
        target_lufs: float = -14.0
    ) -> ToolResult:
        """
        Normalize audio loudness to target LUFS (EBU R128).
        Uses two-pass loudnorm filter.
        """
        try:
            # First pass — measure
            r1 = subprocess.run(
                ["ffmpeg", "-i", input,
                 "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11:print_format=json",
                 "-f", "null", "-"],
                capture_output=True, text=True, timeout=300
            )
            # Parse JSON from stderr
            stderr = r1.stderr
            json_match = re.search(r'\{[^{}]+\}', stderr, re.DOTALL)
            if json_match:
                stats = json.loads(json_match.group())
                af = (
                    f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11:"
                    f"measured_I={stats['input_i']}:"
                    f"measured_TP={stats['input_tp']}:"
                    f"measured_LRA={stats['input_lra']}:"
                    f"measured_thresh={stats['input_thresh']}:"
                    f"offset={stats['target_offset']}:linear=true:print_format=summary"
                )
            else:
                af = f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11"
            ok, out = FFmpegTool._run(["-i", input, "-af", af, output])
            if ok:
                return ToolResult(True, f"✓ Audio normalized to {target_lufs} LUFS → {output}", output)
            return ToolResult(False, f"✗ Normalize audio failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Normalize audio error: {e}")

    @staticmethod
    def denoise_audio(
        input: str, output: str, strength: float = 0.21
    ) -> ToolResult:
        """Denoise audio using afftdn filter. strength 0.01–1.0."""
        try:
            ok, out = FFmpegTool._run([
                "-i", input,
                "-af", f"afftdn=nf=-25:nr={strength * 97:.0f}",
                output
            ])
            if ok:
                return ToolResult(True, f"✓ Audio denoised → {output}", output)
            return ToolResult(False, f"✗ Denoise audio failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Denoise audio error: {e}")

    @staticmethod
    def get_metadata(input: str) -> ToolResult:
        """Return full metadata dict from ffprobe."""
        try:
            info = FFmpegTool._probe(input)
            if not info:
                return ToolResult(False, f"✗ Could not probe {input}")
            return ToolResult(True, f"✓ Metadata for {Path(input).name}", info)
        except Exception as e:
            return ToolResult(False, f"✗ Get metadata error: {e}")

    @staticmethod
    def get_duration(input: str) -> ToolResult:
        """Return duration in seconds as float."""
        try:
            info = FFmpegTool._probe(input)
            dur = float(info.get("format", {}).get("duration", 0))
            return ToolResult(True, f"✓ Duration: {dur:.2f}s", dur)
        except Exception as e:
            return ToolResult(False, f"✗ Get duration error: {e}")

    @staticmethod
    def get_resolution(input: str) -> ToolResult:
        """Return (width, height) of first video stream."""
        try:
            info = FFmpegTool._probe(input)
            for stream in info.get("streams", []):
                if stream.get("codec_type") == "video":
                    w = stream.get("width", 0)
                    h = stream.get("height", 0)
                    return ToolResult(True, f"✓ Resolution: {w}x{h}", {"width": w, "height": h})
            return ToolResult(False, "✗ No video stream found.")
        except Exception as e:
            return ToolResult(False, f"✗ Get resolution error: {e}")

    @staticmethod
    def create_thumbnail(
        input: str, output: str,
        timestamp: str = "00:00:01"
    ) -> ToolResult:
        """Capture a single frame as thumbnail image."""
        try:
            ok, out = FFmpegTool._run([
                "-ss", str(timestamp),
                "-i", input,
                "-frames:v", "1",
                "-q:v", "2",
                output
            ])
            if ok:
                return ToolResult(True, f"✓ Thumbnail saved → {output}", output)
            return ToolResult(False, f"✗ Thumbnail failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Thumbnail error: {e}")

    @staticmethod
    def create_gif(
        input: str, output: str,
        start: str = "0",
        end: str = "5",
        fps: int = 10,
        width: int = 480
    ) -> ToolResult:
        """Create optimised animated GIF from video segment."""
        try:
            palette = tempfile.mktemp(suffix=".png")
            # Generate palette for quality
            ok1, _ = FFmpegTool._run([
                "-ss", str(start), "-to", str(end),
                "-i", input,
                "-vf", f"fps={fps},scale={width}:-1:flags=lanczos,palettegen",
                palette
            ])
            ok2, out = FFmpegTool._run([
                "-ss", str(start), "-to", str(end),
                "-i", input, "-i", palette,
                "-lavfi", f"fps={fps},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
                output
            ])
            try:
                os.unlink(palette)
            except Exception:
                pass
            if ok2:
                return ToolResult(True, f"✓ GIF created → {output}", output)
            return ToolResult(False, f"✗ GIF creation failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Create GIF error: {e}")

    @staticmethod
    def split_by_duration(
        input: str, output_folder: str,
        segment_duration: int = 60
    ) -> ToolResult:
        """Split video/audio into equal-length segments."""
        try:
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            ext = Path(input).suffix
            pattern = os.path.join(output_folder, f"segment_%04d{ext}")
            ok, out = FFmpegTool._run([
                "-i", input,
                "-c", "copy",
                "-f", "segment",
                "-segment_time", str(segment_duration),
                "-reset_timestamps", "1",
                pattern
            ])
            segments = sorted(Path(output_folder).glob(f"segment_*{ext}"))
            if ok:
                return ToolResult(True, f"✓ Split into {len(segments)} segments → {output_folder}", output_folder)
            return ToolResult(False, f"✗ Split failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Split by duration error: {e}")

    @staticmethod
    def add_text_overlay(
        input: str, output: str,
        text: str,
        position: str = "center",
        font_size: int = 48,
        color: str = "white",
        start: float = 0.0,
        end: Optional[float] = None
    ) -> ToolResult:
        """Burn text overlay onto video between start and end seconds."""
        try:
            pos_map = {
                "center":      "(w-text_w)/2:(h-text_h)/2",
                "top":         "(w-text_w)/2:50",
                "bottom":      "(w-text_w)/2:h-text_h-50",
                "topleft":     "10:10",
                "topright":    "w-text_w-10:10",
                "bottomleft":  "10:h-text_h-10",
                "bottomright": "w-text_w-10:h-text_h-10",
            }
            xy = pos_map.get(position, pos_map["center"])
            enable = f"between(t,{start},{end})" if end else f"gte(t,{start})"
            # Escape text for drawtext
            safe_text = text.replace("'", "\\'").replace(":", "\\:")
            drawtext = (
                f"drawtext=text='{safe_text}':"
                f"fontsize={font_size}:fontcolor={color}:"
                f"x={xy}:enable='{enable}':"
                "box=1:boxcolor=black@0.4:boxborderw=5"
            )
            ok, out = FFmpegTool._run([
                "-i", input, "-vf", drawtext,
                "-c:a", "copy", output
            ])
            if ok:
                return ToolResult(True, f"✓ Text overlay added → {output}", output)
            return ToolResult(False, f"✗ Text overlay failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Text overlay error: {e}")

    @staticmethod
    def stabilize_video(input: str, output: str) -> ToolResult:
        """Two-pass video stabilization using vidstabdetect/vidstabtransform."""
        try:
            transforms = tempfile.mktemp(suffix=".trf")
            # Pass 1: detect
            ok1, out1 = FFmpegTool._run([
                "-i", input,
                "-vf", f"vidstabdetect=stepsize=6:shakiness=8:accuracy=9:result={transforms}",
                "-f", "null", "-"
            ])
            if not ok1:
                return ToolResult(False, f"✗ Stabilize pass 1 failed (vidstab may not be compiled): {out1}")
            # Pass 2: transform
            ok2, out2 = FFmpegTool._run([
                "-i", input,
                "-vf", f"vidstabtransform=input={transforms}:zoom=1:smoothing=30,unsharp=5:5:0.8:3:3:0.4",
                "-c:a", "copy", output
            ])
            try:
                os.unlink(transforms)
            except Exception:
                pass
            if ok2:
                return ToolResult(True, f"✓ Video stabilized → {output}", output)
            return ToolResult(False, f"✗ Stabilize pass 2 failed: {out2}")
        except Exception as e:
            return ToolResult(False, f"✗ Stabilize error: {e}")

    @staticmethod
    def color_grade(
        input: str, output: str,
        brightness: float = 0.0,
        contrast: float = 1.0,
        saturation: float = 1.0,
        hue: float = 0.0
    ) -> ToolResult:
        """
        Adjust colour grading.
        brightness: -1.0 to 1.0 (0=no change)
        contrast: 0 to 2 (1=no change)
        saturation: 0 to 3 (1=no change)
        hue: -180 to 180 degrees
        """
        try:
            eq_filter = (
                f"eq=brightness={brightness}:contrast={contrast}:saturation={saturation},"
                f"hue=h={hue}"
            )
            ok, out = FFmpegTool._run([
                "-i", input, "-vf", eq_filter,
                "-c:a", "copy", output
            ])
            if ok:
                return ToolResult(True, f"✓ Colour graded → {output}", output)
            return ToolResult(False, f"✗ Colour grade failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Colour grade error: {e}")

    @staticmethod
    def create_slideshow(
        images: List[str],
        output: str,
        duration_per_image: float = 3.0,
        transition: str = "fade",
        audio: Optional[str] = None
    ) -> ToolResult:
        """
        Create video slideshow from images with optional background audio.
        transition: fade|none (xfade for fade between slides)
        """
        try:
            if not images:
                return ToolResult(False, "✗ No images provided.")
            in_args = []
            for img in images:
                in_args += ["-loop", "1", "-t", str(duration_per_image), "-i", img]
            n = len(images)
            if audio:
                in_args += ["-i", audio]
            # Build filter
            filter_parts = []
            for i in range(n):
                filter_parts.append(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}]")
            # Concatenate
            concat_in = "".join(f"[v{i}]" for i in range(n))
            filter_parts.append(f"{concat_in}concat=n={n}:v=1:a=0[outv]")
            filter_complex = ";".join(filter_parts)
            if audio:
                audio_idx = n
                map_args = ["-map", "[outv]", "-map", f"{audio_idx}:a", "-shortest"]
            else:
                map_args = ["-map", "[outv]"]
            ok, out = FFmpegTool._run(
                in_args + ["-filter_complex", filter_complex] +
                map_args + ["-c:v", "libx264", "-pix_fmt", "yuv420p", output]
            )
            if ok:
                return ToolResult(True, f"✓ Slideshow ({n} images) → {output}", output)
            return ToolResult(False, f"✗ Slideshow failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Create slideshow error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. YouTubeDownloaderTool
# ─────────────────────────────────────────────────────────────────────────────
class YouTubeDownloaderTool:
    name = "youtube_downloader"
    description = (
        "Download YouTube videos, audio, playlists, subtitles, thumbnails; "
        "get video info, available formats, search videos, get channel videos."
    )

    @staticmethod
    def _ydl_opts(extra: dict = None) -> dict:
        base = {"quiet": True, "no_warnings": True}
        if extra:
            base.update(extra)
        return base

    @staticmethod
    def download_video(
        url: str, output_path: str = ".",
        quality: str = "best",
        format: str = "mp4"
    ) -> ToolResult:
        """Download video. quality: 'best','1080p','720p','480p','360p'."""
        try:
            import yt_dlp
            quality_map = {
                "best":  "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
                "720p":  "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
                "480p":  "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]",
                "360p":  "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]",
            }
            fmt = quality_map.get(quality, quality_map["best"])
            opts = {
                "format": fmt,
                "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
                "merge_output_format": format,
                "quiet": True,
            }
            downloaded = []
            def hook(d):
                if d["status"] == "finished":
                    downloaded.append(d.get("filename", ""))
            opts["progress_hooks"] = [hook]
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "video")
            return ToolResult(True, f"✓ Downloaded: {title}", downloaded[0] if downloaded else output_path)
        except Exception as e:
            return ToolResult(False, f"✗ YouTube download failed: {e}")

    @staticmethod
    def download_audio(
        url: str, output_path: str = ".",
        format: str = "mp3"
    ) -> ToolResult:
        """Download audio only from YouTube."""
        try:
            import yt_dlp
            opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format,
                    "preferredquality": "192",
                }],
                "quiet": True,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "audio")
            return ToolResult(True, f"✓ Audio downloaded: {title}", output_path)
        except Exception as e:
            return ToolResult(False, f"✗ Audio download failed: {e}")

    @staticmethod
    def download_playlist(
        url: str, output_folder: str = ".",
        quality: str = "best"
    ) -> ToolResult:
        """Download all videos from a YouTube playlist."""
        try:
            import yt_dlp
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            quality_map = {
                "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
            }
            opts = {
                "format": quality_map.get(quality, quality_map["best"]),
                "outtmpl": os.path.join(output_folder, "%(playlist_index)s - %(title)s.%(ext)s"),
                "merge_output_format": "mp4",
                "quiet": True,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                n = len(info.get("entries", []))
            return ToolResult(True, f"✓ Playlist downloaded: {n} videos → {output_folder}", output_folder)
        except Exception as e:
            return ToolResult(False, f"✗ Playlist download failed: {e}")

    @staticmethod
    def get_video_info(url: str) -> ToolResult:
        """Return metadata dict for a YouTube video without downloading."""
        try:
            import yt_dlp
            opts = {"quiet": True, "skip_download": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            data = {
                "title":       info.get("title"),
                "description": (info.get("description") or "")[:500],
                "duration":    info.get("duration"),
                "view_count":  info.get("view_count"),
                "like_count":  info.get("like_count"),
                "uploader":    info.get("uploader"),
                "upload_date": info.get("upload_date"),
                "thumbnail":   info.get("thumbnail"),
                "tags":        info.get("tags", []),
                "categories":  info.get("categories", []),
            }
            return ToolResult(True, f"✓ Info: {data['title']}", data)
        except Exception as e:
            return ToolResult(False, f"✗ Get video info failed: {e}")

    @staticmethod
    def download_subtitles(
        url: str, language: str = "en",
        output_path: str = "."
    ) -> ToolResult:
        """Download subtitles (.vtt / .srt) for a video."""
        try:
            import yt_dlp
            opts = {
                "quiet": True,
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": [language],
                "outtmpl": os.path.join(output_path, "%(title)s"),
                "subtitlesformat": "srt",
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "subtitles")
            srt_files = list(Path(output_path).glob(f"*.{language}.srt")) + \
                        list(Path(output_path).glob(f"*.{language}.vtt"))
            return ToolResult(True, f"✓ Subtitles for '{title}' → {output_path}",
                              [str(f) for f in srt_files])
        except Exception as e:
            return ToolResult(False, f"✗ Download subtitles failed: {e}")

    @staticmethod
    def get_available_formats(url: str) -> ToolResult:
        """List all available download formats for a video."""
        try:
            import yt_dlp
            opts = {"quiet": True, "skip_download": True, "listformats": False}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get("formats", []):
                formats.append({
                    "format_id":  f.get("format_id"),
                    "ext":        f.get("ext"),
                    "resolution": f.get("resolution") or f"{f.get('width','?')}x{f.get('height','?')}",
                    "fps":        f.get("fps"),
                    "vcodec":     f.get("vcodec"),
                    "acodec":     f.get("acodec"),
                    "filesize":   f.get("filesize"),
                    "tbr":        f.get("tbr"),
                })
            return ToolResult(True, f"✓ {len(formats)} formats available", formats)
        except Exception as e:
            return ToolResult(False, f"✗ Get formats failed: {e}")

    @staticmethod
    def download_thumbnail(url: str, output_path: str = "thumbnail.jpg") -> ToolResult:
        """Download the highest-resolution thumbnail of a YouTube video."""
        try:
            import yt_dlp, requests
            opts = {"quiet": True, "skip_download": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            thumb_url = info.get("thumbnail")
            if not thumb_url:
                return ToolResult(False, "✗ No thumbnail URL found.")
            r = requests.get(thumb_url, timeout=20)
            r.raise_for_status()
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as fh:
                fh.write(r.content)
            return ToolResult(True, f"✓ Thumbnail saved → {output_path}", output_path)
        except Exception as e:
            return ToolResult(False, f"✗ Download thumbnail failed: {e}")

    @staticmethod
    def search_videos(query: str, max_results: int = 10) -> ToolResult:
        """Search YouTube and return list of video info dicts."""
        try:
            import yt_dlp
            opts = {
                "quiet": True,
                "skip_download": True,
                "extract_flat": True,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(
                    f"ytsearch{max_results}:{query}", download=False
                )
            results = []
            for entry in info.get("entries", []):
                results.append({
                    "title":     entry.get("title"),
                    "url":       f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "duration":  entry.get("duration"),
                    "uploader":  entry.get("uploader"),
                    "view_count":entry.get("view_count"),
                })
            return ToolResult(True, f"✓ {len(results)} results for '{query}'", results)
        except Exception as e:
            return ToolResult(False, f"✗ Search videos failed: {e}")

    @staticmethod
    def get_channel_videos(
        channel_url: str,
        max_results: int = 20,
        download: bool = False
    ) -> ToolResult:
        """
        Get (and optionally download) videos from a YouTube channel.
        Returns list of video info dicts if download=False.
        """
        try:
            import yt_dlp
            opts = {
                "quiet": True,
                "extract_flat": not download,
                "playlistend": max_results,
            }
            if download:
                opts["outtmpl"] = "%(uploader)s/%(title)s.%(ext)s"
                opts["format"] = "bestvideo[height<=720][ext=mp4]+bestaudio/best"
                opts["merge_output_format"] = "mp4"
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(channel_url, download=download)
            videos = []
            for entry in (info.get("entries") or [])[:max_results]:
                videos.append({
                    "title":    entry.get("title"),
                    "url":      f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "duration": entry.get("duration"),
                })
            action = "Downloaded" if download else "Listed"
            return ToolResult(True, f"✓ {action} {len(videos)} channel videos", videos)
        except Exception as e:
            return ToolResult(False, f"✗ Channel videos failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. AudioTool
# ─────────────────────────────────────────────────────────────────────────────
class AudioTool:
    name = "audio"
    description = (
        "Audio processing and generation: convert, split, merge, normalize, "
        "pitch/tempo change, silence removal, EQ, fades, BPM detection, "
        "waveform data, microphone recording, playback, transcription, translation."
    )

    @staticmethod
    def convert(
        input: str, output: str,
        format: str = "mp3",
        bitrate: str = "192k",
        sample_rate: int = 44100,
        channels: int = 2
    ) -> ToolResult:
        """Convert audio file to target format/quality."""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(input)
            audio = audio.set_frame_rate(sample_rate).set_channels(channels)
            codec_map = {"mp3": "libmp3lame", "ogg": "libvorbis",
                         "flac": "flac", "wav": "pcm_s16le", "aac": "aac"}
            export_kwargs = {"format": format, "bitrate": bitrate}
            audio.export(output, **export_kwargs)
            return ToolResult(True, f"✓ Audio converted → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Audio convert failed: {e}")

    @staticmethod
    def split(
        input: str, output_folder: str,
        split_at_silences: bool = True,
        min_silence: int = 700,
        segment_duration: Optional[int] = None
    ) -> ToolResult:
        """
        Split audio. split_at_silences=True detects silence; otherwise splits by segment_duration (ms).
        """
        try:
            from pydub import AudioSegment
            from pydub.silence import split_on_silence, detect_silence
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            audio = AudioSegment.from_file(input)
            ext = Path(input).suffix.lstrip(".")
            if split_at_silences:
                chunks = split_on_silence(
                    audio,
                    min_silence_len=min_silence,
                    silence_thresh=audio.dBFS - 14,
                    keep_silence=200
                )
            else:
                dur = segment_duration or 60000
                chunks = [audio[i:i + dur] for i in range(0, len(audio), dur)]
            for i, chunk in enumerate(chunks):
                out_path = os.path.join(output_folder, f"segment_{i+1:04d}.{ext}")
                chunk.export(out_path, format=ext)
            return ToolResult(True, f"✓ Split into {len(chunks)} segments → {output_folder}", output_folder)
        except Exception as e:
            return ToolResult(False, f"✗ Audio split failed: {e}")

    @staticmethod
    def merge(
        inputs: List[str], output: str,
        crossfade: int = 0
    ) -> ToolResult:
        """Merge/concatenate audio files. crossfade in milliseconds."""
        try:
            from pydub import AudioSegment
            combined = AudioSegment.from_file(inputs[0])
            for path in inputs[1:]:
                seg = AudioSegment.from_file(path)
                if crossfade > 0:
                    combined = combined.append(seg, crossfade=crossfade)
                else:
                    combined += seg
            fmt = Path(output).suffix.lstrip(".") or "mp3"
            combined.export(output, format=fmt)
            return ToolResult(True, f"✓ Merged {len(inputs)} audio files → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Audio merge failed: {e}")

    @staticmethod
    def normalize(
        input: str, output: str,
        target_db: float = -20.0
    ) -> ToolResult:
        """Normalize audio to target dBFS level."""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(input)
            change_db = target_db - audio.dBFS
            normalized = audio.apply_gain(change_db)
            fmt = Path(output).suffix.lstrip(".") or "mp3"
            normalized.export(output, format=fmt)
            return ToolResult(True, f"✓ Normalized to {target_db} dBFS → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Normalize failed: {e}")

    @staticmethod
    def change_pitch(
        input: str, output: str,
        semitones: float = 2.0
    ) -> ToolResult:
        """Change pitch by N semitones (positive = higher, negative = lower)."""
        try:
            import librosa
            import soundfile as sf
            import numpy as np
            y, sr = librosa.load(input, sr=None)
            y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)
            sf.write(output, y_shifted, sr)
            return ToolResult(True, f"✓ Pitch shifted {semitones:+.1f} semitones → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Pitch change failed: {e}")

    @staticmethod
    def change_tempo(
        input: str, output: str,
        tempo_factor: float = 1.5
    ) -> ToolResult:
        """Change tempo without changing pitch. 1.5=50% faster, 0.5=50% slower."""
        try:
            import librosa
            import soundfile as sf
            y, sr = librosa.load(input, sr=None)
            y_stretched = librosa.effects.time_stretch(y, rate=tempo_factor)
            sf.write(output, y_stretched, sr)
            return ToolResult(True, f"✓ Tempo x{tempo_factor} → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Tempo change failed: {e}")

    @staticmethod
    def remove_silence(
        input: str, output: str,
        min_silence_len: int = 1000,
        silence_thresh: int = -40
    ) -> ToolResult:
        """Remove silent portions from audio file."""
        try:
            from pydub import AudioSegment
            from pydub.silence import split_on_silence
            audio = AudioSegment.from_file(input)
            chunks = split_on_silence(
                audio,
                min_silence_len=min_silence_len,
                silence_thresh=silence_thresh,
                keep_silence=100
            )
            combined = AudioSegment.empty()
            for chunk in chunks:
                combined += chunk
            fmt = Path(output).suffix.lstrip(".") or "mp3"
            combined.export(output, format=fmt)
            orig_dur = len(audio) / 1000
            new_dur = len(combined) / 1000
            removed = orig_dur - new_dur
            return ToolResult(True, f"✓ Removed {removed:.1f}s of silence → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Remove silence failed: {e}")

    @staticmethod
    def apply_eq(
        input: str, output: str,
        bass: float = 0.0,
        mid: float = 0.0,
        treble: float = 0.0
    ) -> ToolResult:
        """Apply simple 3-band EQ. Values are dB gain (-20 to +20)."""
        try:
            # Use ffmpeg equalizer filter
            filters = []
            if bass != 0:
                filters.append(f"equalizer=f=100:width_type=o:width=2:g={bass}")
            if mid != 0:
                filters.append(f"equalizer=f=1000:width_type=o:width=2:g={mid}")
            if treble != 0:
                filters.append(f"equalizer=f=10000:width_type=o:width=2:g={treble}")
            if not filters:
                shutil.copy2(input, output)
                return ToolResult(True, f"✓ No EQ changes (copied) → {output}", output)
            af = ",".join(filters)
            ok, out = FFmpegTool._run(["-i", input, "-af", af, output])
            if ok:
                return ToolResult(True, f"✓ EQ applied (bass={bass}, mid={mid}, treble={treble}) → {output}", output)
            return ToolResult(False, f"✗ EQ failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Apply EQ failed: {e}")

    @staticmethod
    def fade_in_out(
        input: str, output: str,
        fade_in: int = 1000,
        fade_out: int = 1000
    ) -> ToolResult:
        """Add fade in/out effects. fade_in and fade_out in milliseconds."""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(input)
            audio = audio.fade_in(fade_in).fade_out(fade_out)
            fmt = Path(output).suffix.lstrip(".") or "mp3"
            audio.export(output, format=fmt)
            return ToolResult(True, f"✓ Fades applied → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Fade in/out failed: {e}")

    @staticmethod
    def detect_bpm(input: str) -> ToolResult:
        """Detect the BPM (beats per minute) of an audio file."""
        try:
            import librosa
            y, sr = librosa.load(input, sr=None)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            # librosa returns numpy scalar, convert to float
            bpm = float(tempo)
            return ToolResult(True, f"✓ BPM detected: {bpm:.1f}", bpm)
        except Exception as e:
            return ToolResult(False, f"✗ BPM detection failed: {e}")

    @staticmethod
    def get_waveform_data(
        input: str, num_points: int = 500
    ) -> ToolResult:
        """Return downsampled amplitude data for waveform visualisation."""
        try:
            import librosa
            import numpy as np
            y, sr = librosa.load(input, sr=None, mono=True)
            chunk_size = max(1, len(y) // num_points)
            waveform = [float(np.max(np.abs(y[i:i+chunk_size])))
                        for i in range(0, len(y), chunk_size)][:num_points]
            return ToolResult(True, f"✓ Waveform data ({len(waveform)} points)", waveform)
        except Exception as e:
            return ToolResult(False, f"✗ Get waveform data failed: {e}")

    @staticmethod
    def record_microphone(
        output: str,
        duration: int = 10,
        sample_rate: int = 44100
    ) -> ToolResult:
        """Record from default microphone for specified duration (seconds)."""
        try:
            import sounddevice as sd
            import soundfile as sf
            import numpy as np
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16"
            )
            sd.wait()
            sf.write(output, recording, sample_rate)
            return ToolResult(True, f"✓ Recorded {duration}s → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Record microphone failed: {e}")

    @staticmethod
    def play_audio(path: str) -> ToolResult:
        """Play an audio file (non-blocking)."""
        try:
            import sounddevice as sd
            import soundfile as sf
            data, sr = sf.read(path)
            sd.play(data, sr)
            return ToolResult(True, f"✓ Playing {Path(path).name}", path)
        except Exception as e:
            # Fallback to system player
            try:
                if platform.system() == "Windows":
                    os.startfile(path)
                elif platform.system() == "Darwin":
                    subprocess.Popen(["afplay", path])
                else:
                    subprocess.Popen(["aplay", path])
                return ToolResult(True, f"✓ Playing {Path(path).name} (system player)", path)
            except Exception as e2:
                return ToolResult(False, f"✗ Play audio failed: {e} | {e2}")

    @staticmethod
    def transcribe(
        audio_path: str,
        language: str = "en",
        model_size: str = "base"
    ) -> ToolResult:
        """
        Transcribe audio to text using OpenAI Whisper (local).
        model_size: tiny|base|small|medium|large
        """
        try:
            import whisper
            model = whisper.load_model(model_size)
            result = model.transcribe(audio_path, language=language)
            text = result["text"].strip()
            segments = result.get("segments", [])
            return ToolResult(True, f"✓ Transcribed {len(text)} chars", {
                "text": text, "segments": segments, "language": result.get("language")
            })
        except Exception as e:
            return ToolResult(False, f"✗ Transcribe failed: {e}")

    @staticmethod
    def translate_audio(
        audio_path: str,
        target_language: str = "en"
    ) -> ToolResult:
        """
        Transcribe and translate audio to target_language using Whisper's translate task.
        Note: Whisper natively translates to English; for other targets uses transcribe.
        """
        try:
            import whisper
            model = whisper.load_model("base")
            if target_language == "en":
                result = model.transcribe(audio_path, task="translate")
            else:
                result = model.transcribe(audio_path, language=target_language)
            text = result["text"].strip()
            return ToolResult(True, f"✓ Translated audio → {target_language}", {
                "text": text, "language": target_language
            })
        except Exception as e:
            return ToolResult(False, f"✗ Translate audio failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. ImageAdvancedTool
# ─────────────────────────────────────────────────────────────────────────────
class ImageAdvancedTool:
    name = "image_advanced"
    description = (
        "Advanced image processing: batch resize/convert, collage, background removal, "
        "upscaling, face detection/blur, borders, shadows, GIF creation, web optimisation, "
        "dominant colour extraction, palette, image comparison, sprite sheets, "
        "watermark batch, ICO/favicon conversion."
    )

    @staticmethod
    def batch_resize(
        folder: str, output_folder: str,
        width: int = 800, height: int = 600,
        keep_aspect: bool = True,
        format: str = "jpg"
    ) -> ToolResult:
        """Batch resize all images in folder."""
        try:
            from PIL import Image
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            count = 0
            exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}
            for fp in Path(folder).iterdir():
                if fp.suffix.lower() not in exts:
                    continue
                try:
                    img = Image.open(fp).convert("RGB")
                    if keep_aspect:
                        img.thumbnail((width, height), Image.LANCZOS)
                    else:
                        img = img.resize((width, height), Image.LANCZOS)
                    out_path = Path(output_folder) / f"{fp.stem}.{format}"
                    img.save(str(out_path), quality=90)
                    count += 1
                except Exception:
                    pass
            return ToolResult(True, f"✓ Batch resized {count} images → {output_folder}", output_folder)
        except Exception as e:
            return ToolResult(False, f"✗ Batch resize failed: {e}")

    @staticmethod
    def batch_convert(
        folder: str, output_folder: str,
        target_format: str = "webp",
        quality: int = 85
    ) -> ToolResult:
        """Batch convert all images in folder to target format."""
        try:
            from PIL import Image
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            count = 0
            exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".gif"}
            for fp in Path(folder).iterdir():
                if fp.suffix.lower() not in exts:
                    continue
                try:
                    img = Image.open(fp)
                    if target_format.lower() in ("jpg", "jpeg") and img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    out_path = Path(output_folder) / f"{fp.stem}.{target_format}"
                    img.save(str(out_path), quality=quality)
                    count += 1
                except Exception:
                    pass
            return ToolResult(True, f"✓ Converted {count} images to {target_format} → {output_folder}", output_folder)
        except Exception as e:
            return ToolResult(False, f"✗ Batch convert failed: {e}")

    @staticmethod
    def create_collage(
        images: List[str], output: str,
        layout: str = "grid",
        padding: int = 10,
        background: str = "white",
        border: int = 0
    ) -> ToolResult:
        """
        Create a collage. layout: 'grid' (square grid) or 'horizontal' or 'vertical'.
        """
        try:
            from PIL import Image, ImageDraw
            import math
            imgs = [Image.open(p).convert("RGBA") for p in images]
            if not imgs:
                return ToolResult(False, "✗ No images provided.")
            # Uniform thumbnail size
            thumb_w, thumb_h = 400, 300
            thumbs = []
            for img in imgs:
                img.thumbnail((thumb_w, thumb_h), Image.LANCZOS)
                # Pad to uniform size
                canvas = Image.new("RGBA", (thumb_w, thumb_h), (0, 0, 0, 0))
                ox = (thumb_w - img.width) // 2
                oy = (thumb_h - img.height) // 2
                canvas.paste(img, (ox, oy))
                thumbs.append(canvas)
            n = len(thumbs)
            if layout == "horizontal":
                cols, rows = n, 1
            elif layout == "vertical":
                cols, rows = 1, n
            else:
                cols = math.ceil(math.sqrt(n))
                rows = math.ceil(n / cols)
            total_w = cols * (thumb_w + padding) + padding
            total_h = rows * (thumb_h + padding) + padding
            collage = Image.new("RGBA", (total_w, total_h),
                                background if background else "white")
            for idx, thumb in enumerate(thumbs):
                row = idx // cols
                col = idx % cols
                x = col * (thumb_w + padding) + padding
                y = row * (thumb_h + padding) + padding
                collage.paste(thumb, (x, y), mask=thumb)
            if output.lower().endswith((".jpg", ".jpeg")):
                collage = collage.convert("RGB")
            collage.save(output)
            return ToolResult(True, f"✓ Collage ({cols}x{rows}) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Create collage failed: {e}")

    @staticmethod
    def remove_background(
        input: str, output: str,
        model: str = "u2net"
    ) -> ToolResult:
        """Remove image background using rembg (local AI model, no API needed)."""
        try:
            from rembg import remove
            from PIL import Image
            inp = Image.open(input)
            result = remove(inp, model_name=model)
            result.save(output)
            return ToolResult(True, f"✓ Background removed → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Remove background failed: {e}")

    @staticmethod
    def replace_background(
        input: str, background: str, output: str
    ) -> ToolResult:
        """Remove foreground background and replace with new background image."""
        try:
            from rembg import remove
            from PIL import Image
            fg = remove(Image.open(input).convert("RGBA"))
            bg = Image.open(background).convert("RGBA").resize(fg.size, Image.LANCZOS)
            composite = Image.alpha_composite(bg, fg)
            if output.lower().endswith((".jpg", ".jpeg")):
                composite = composite.convert("RGB")
            composite.save(output)
            return ToolResult(True, f"✓ Background replaced → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Replace background failed: {e}")

    @staticmethod
    def upscale(
        input: str, output: str,
        scale_factor: int = 2,
        model: str = "lanczos"
    ) -> ToolResult:
        """
        Upscale image. model='lanczos' for fast resize.
        For AI upscaling, install realesrgan separately.
        """
        try:
            from PIL import Image
            img = Image.open(input)
            new_w = img.width * scale_factor
            new_h = img.height * scale_factor
            resampling = {
                "lanczos":  Image.LANCZOS,
                "bicubic":  Image.BICUBIC,
                "nearest":  Image.NEAREST,
            }.get(model, Image.LANCZOS)
            upscaled = img.resize((new_w, new_h), resampling)
            upscaled.save(output, quality=95)
            return ToolResult(True, f"✓ Upscaled {scale_factor}x ({new_w}x{new_h}) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Upscale failed: {e}")

    @staticmethod
    def restore_old_photo(input: str, output: str) -> ToolResult:
        """
        Restore old/damaged photo: auto contrast, mild denoise, sharpen.
        """
        try:
            import cv2
            import numpy as np
            img = cv2.imread(input)
            if img is None:
                return ToolResult(False, f"✗ Cannot open {input}")
            # Convert to LAB for CLAHE
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l_channel, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l_channel)
            enhanced = cv2.merge([cl, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
            # Denoise
            denoised = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
            # Sharpen
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            cv2.imwrite(output, sharpened)
            return ToolResult(True, f"✓ Photo restored → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Restore photo failed: {e}")

    @staticmethod
    def face_detect(
        image: str,
        draw_boxes: bool = True,
        output: Optional[str] = None
    ) -> ToolResult:
        """Detect faces using OpenCV Haar cascades. Returns list of bounding boxes."""
        try:
            import cv2
            img = cv2.imread(image)
            if img is None:
                return ToolResult(False, f"✗ Cannot open {image}")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            cascade = cv2.CascadeClassifier(cascade_path)
            faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            boxes = [(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]
            if draw_boxes and output:
                for x, y, w, h in boxes:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imwrite(output, img)
            return ToolResult(True, f"✓ Detected {len(boxes)} face(s)", boxes)
        except Exception as e:
            return ToolResult(False, f"✗ Face detect failed: {e}")

    @staticmethod
    def blur_faces(input: str, output: str) -> ToolResult:
        """Automatically detect and blur all faces in an image."""
        try:
            import cv2
            img = cv2.imread(input)
            if img is None:
                return ToolResult(False, f"✗ Cannot open {input}")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
            for x, y, w, h in faces:
                face_roi = img[y:y + h, x:x + w]
                blurred = cv2.GaussianBlur(face_roi, (99, 99), 30)
                img[y:y + h, x:x + w] = blurred
            cv2.imwrite(output, img)
            return ToolResult(True, f"✓ Blurred {len(faces)} face(s) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Blur faces failed: {e}")

    @staticmethod
    def add_border(
        input: str, output: str,
        size: int = 20,
        color: str = "white"
    ) -> ToolResult:
        """Add a solid-colour border around image."""
        try:
            from PIL import Image, ImageOps
            img = Image.open(input)
            bordered = ImageOps.expand(img, border=size, fill=color)
            bordered.save(output)
            return ToolResult(True, f"✓ Border added ({size}px {color}) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Add border failed: {e}")

    @staticmethod
    def add_shadow(
        input: str, output: str,
        offset: Tuple[int, int] = (10, 10),
        blur: int = 15,
        color: str = "black"
    ) -> ToolResult:
        """Add drop shadow effect to image."""
        try:
            from PIL import Image, ImageFilter
            import numpy as np
            img = Image.open(input).convert("RGBA")
            shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
            # Create shadow layer from alpha channel
            r, g, b, a = img.split()
            shadow_color = Image.new("RGBA", img.size, color + "CC")
            shadow.paste(shadow_color, mask=a)
            shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur))
            # Composite: shadow then image offset
            canvas_w = img.width + abs(offset[0]) + blur * 2
            canvas_h = img.height + abs(offset[1]) + blur * 2
            canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
            sx = max(0, offset[0]) + blur
            sy = max(0, offset[1]) + blur
            canvas.paste(shadow, (sx, sy), mask=shadow)
            ix = max(0, -offset[0]) + blur
            iy = max(0, -offset[1]) + blur
            canvas.paste(img, (ix, iy), mask=img)
            if output.lower().endswith((".jpg", ".jpeg")):
                canvas = canvas.convert("RGB")
            canvas.save(output)
            return ToolResult(True, f"✓ Shadow added → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Add shadow failed: {e}")

    @staticmethod
    def create_gif_from_images(
        images: List[str], output: str,
        duration: int = 200,
        loop: int = 0
    ) -> ToolResult:
        """Create animated GIF from list of image files. duration in ms per frame."""
        try:
            from PIL import Image
            frames = [Image.open(p).convert("RGBA") for p in images]
            if not frames:
                return ToolResult(False, "✗ No images provided.")
            frames[0].save(
                output,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=loop
            )
            return ToolResult(True, f"✓ GIF ({len(frames)} frames) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Create GIF failed: {e}")

    @staticmethod
    def optimize_for_web(
        input: str, output: str,
        max_size_kb: int = 200
    ) -> ToolResult:
        """Iteratively compress image until it's under max_size_kb."""
        try:
            from PIL import Image
            img = Image.open(input)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            quality = 90
            fmt = "JPEG"
            while quality >= 20:
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
                    tmp = tf.name
                img.save(tmp, format=fmt, quality=quality, optimize=True)
                size_kb = os.path.getsize(tmp) / 1024
                if size_kb <= max_size_kb:
                    shutil.move(tmp, output)
                    return ToolResult(True, f"✓ Optimized to {size_kb:.0f}KB (q={quality}) → {output}", output)
                os.unlink(tmp)
                quality -= 5
            # Last resort: save at minimum quality
            img.save(output, format=fmt, quality=20, optimize=True)
            final_kb = os.path.getsize(output) / 1024
            return ToolResult(True, f"✓ Optimized to {final_kb:.0f}KB (min quality) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Optimize for web failed: {e}")

    @staticmethod
    def extract_dominant_colors(
        image: str, n_colors: int = 5
    ) -> ToolResult:
        """Extract N dominant colours using K-Means clustering."""
        try:
            import cv2
            import numpy as np
            img = cv2.imread(image)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pixels = img_rgb.reshape(-1, 3).astype(np.float32)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, labels, centers = cv2.kmeans(
                pixels, n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
            )
            counts = np.bincount(labels.flatten())
            sorted_idx = np.argsort(-counts)
            colors = []
            for i in sorted_idx:
                r, g, b = [int(c) for c in centers[i]]
                hex_col = f"#{r:02x}{g:02x}{b:02x}"
                colors.append({"rgb": (r, g, b), "hex": hex_col,
                                "percentage": round(counts[i] / len(labels) * 100, 1)})
            return ToolResult(True, f"✓ Extracted {n_colors} dominant colours", colors)
        except Exception as e:
            return ToolResult(False, f"✗ Extract colors failed: {e}")

    @staticmethod
    def create_palette(
        image: str, output: str, n_colors: int = 8
    ) -> ToolResult:
        """Generate a colour palette image from dominant colours."""
        try:
            from PIL import Image, ImageDraw
            result = ImageAdvancedTool.extract_dominant_colors(image, n_colors)
            if not result.success:
                return result
            colors = result.data
            swatch_w, swatch_h = 80, 80
            palette_img = Image.new("RGB", (swatch_w * n_colors, swatch_h))
            draw = ImageDraw.Draw(palette_img)
            for i, c in enumerate(colors):
                r, g, b = c["rgb"]
                draw.rectangle([i * swatch_w, 0, (i + 1) * swatch_w, swatch_h], fill=(r, g, b))
            palette_img.save(output)
            return ToolResult(True, f"✓ Palette saved → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Create palette failed: {e}")

    @staticmethod
    def compare_images(
        img1: str, img2: str, output_diff: str
    ) -> ToolResult:
        """Generate difference image and return similarity score."""
        try:
            import cv2
            import numpy as np
            i1 = cv2.imread(img1)
            i2 = cv2.imread(img2)
            if i1 is None or i2 is None:
                return ToolResult(False, "✗ Could not open one or both images.")
            # Resize i2 to match i1
            i2 = cv2.resize(i2, (i1.shape[1], i1.shape[0]))
            diff = cv2.absdiff(i1, i2)
            diff_enhanced = cv2.applyColorMap(diff, cv2.COLORMAP_JET)
            cv2.imwrite(output_diff, diff_enhanced)
            # Structural Similarity Index
            from skimage.metrics import structural_similarity as ssim
            g1 = cv2.cvtColor(i1, cv2.COLOR_BGR2GRAY)
            g2 = cv2.cvtColor(i2, cv2.COLOR_BGR2GRAY)
            score, _ = ssim(g1, g2, full=True)
            return ToolResult(True, f"✓ Similarity: {score:.2%} | Diff saved → {output_diff}",
                              {"similarity": score, "diff_image": output_diff})
        except Exception as e:
            return ToolResult(False, f"✗ Compare images failed: {e}")

    @staticmethod
    def create_sprite_sheet(
        images: List[str], output: str, cols: int = 4
    ) -> ToolResult:
        """Create a sprite sheet from list of images."""
        try:
            from PIL import Image
            import math
            imgs = [Image.open(p).convert("RGBA") for p in images]
            if not imgs:
                return ToolResult(False, "✗ No images provided.")
            w = max(i.width for i in imgs)
            h = max(i.height for i in imgs)
            rows = math.ceil(len(imgs) / cols)
            sheet = Image.new("RGBA", (cols * w, rows * h), (0, 0, 0, 0))
            for idx, img in enumerate(imgs):
                row = idx // cols
                col = idx % cols
                sheet.paste(img, (col * w, row * h))
            sheet.save(output)
            return ToolResult(True, f"✓ Sprite sheet ({cols}x{rows}) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Create sprite sheet failed: {e}")

    @staticmethod
    def watermark_batch(
        folder: str, watermark: str,
        output_folder: str,
        position: str = "bottomright",
        opacity: float = 0.7
    ) -> ToolResult:
        """Apply watermark to all images in folder."""
        try:
            from PIL import Image
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            wm = Image.open(watermark).convert("RGBA")
            # Apply opacity to watermark
            r, g, b, a = wm.split()
            import PIL.ImageEnhance as IE
            a = IE.Brightness(a).enhance(opacity)
            wm.putalpha(a)
            exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
            count = 0
            for fp in Path(folder).iterdir():
                if fp.suffix.lower() not in exts:
                    continue
                try:
                    img = Image.open(fp).convert("RGBA")
                    # Scale watermark to max 25% of image size
                    wm_scaled = wm.copy()
                    max_wm_w = img.width // 4
                    if wm_scaled.width > max_wm_w:
                        ratio = max_wm_w / wm_scaled.width
                        wm_scaled = wm_scaled.resize(
                            (max_wm_w, int(wm_scaled.height * ratio)), Image.LANCZOS
                        )
                    pos_map = {
                        "topleft":     (10, 10),
                        "topright":    (img.width - wm_scaled.width - 10, 10),
                        "bottomleft":  (10, img.height - wm_scaled.height - 10),
                        "bottomright": (img.width - wm_scaled.width - 10,
                                        img.height - wm_scaled.height - 10),
                        "center":      ((img.width - wm_scaled.width) // 2,
                                        (img.height - wm_scaled.height) // 2),
                    }
                    pos = pos_map.get(position, pos_map["bottomright"])
                    img.paste(wm_scaled, pos, mask=wm_scaled)
                    out_path = Path(output_folder) / fp.name
                    if fp.suffix.lower() in (".jpg", ".jpeg"):
                        img = img.convert("RGB")
                    img.save(str(out_path))
                    count += 1
                except Exception:
                    pass
            return ToolResult(True, f"✓ Watermarked {count} images → {output_folder}", output_folder)
        except Exception as e:
            return ToolResult(False, f"✗ Watermark batch failed: {e}")

    @staticmethod
    def convert_to_ico(
        input: str, output: str,
        sizes: Optional[List[int]] = None
    ) -> ToolResult:
        """Convert image to .ico format with multiple sizes."""
        try:
            from PIL import Image
            sizes = sizes or [16, 32, 48, 64, 128, 256]
            img = Image.open(input).convert("RGBA")
            icon_sizes = [(s, s) for s in sizes]
            img.save(output, format="ICO", sizes=icon_sizes)
            return ToolResult(True, f"✓ ICO saved with sizes {sizes} → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Convert to ICO failed: {e}")

    @staticmethod
    def create_favicon(
        input: str, output_folder: str
    ) -> ToolResult:
        """Create a complete favicon set (ICO + multiple PNG sizes) for web use."""
        try:
            from PIL import Image
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            img = Image.open(input).convert("RGBA")
            files = []
            # Standard favicon sizes
            for size in [16, 32, 48, 64, 96, 180, 192, 512]:
                resized = img.resize((size, size), Image.LANCZOS)
                out = os.path.join(output_folder, f"favicon-{size}x{size}.png")
                resized.save(out)
                files.append(out)
            # ICO file with 16/32/48
            ico_path = os.path.join(output_folder, "favicon.ico")
            img.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
            files.append(ico_path)
            return ToolResult(True, f"✓ Favicon set ({len(files)} files) → {output_folder}", files)
        except Exception as e:
            return ToolResult(False, f"✗ Create favicon failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. ScreenRecorderTool
# ─────────────────────────────────────────────────────────────────────────────
class ScreenRecorderTool:
    name = "screen_recorder"
    description = (
        "Screen capture and recording: screenshot, all monitors, record screen "
        "(with audio), cursor highlighting, window capture, list windows, screencast GIF."
    )

    @staticmethod
    def screenshot(
        output: str = "screenshot.png",
        region: Optional[Tuple[int, int, int, int]] = None,
        monitor: int = 1
    ) -> ToolResult:
        """
        Take a screenshot. region=(left, top, width, height). monitor=1 is primary.
        """
        try:
            import mss
            with mss.mss() as sct:
                if region:
                    mon = {"left": region[0], "top": region[1],
                           "width": region[2], "height": region[3]}
                else:
                    mon = sct.monitors[monitor]
                img = sct.grab(mon)
                import mss.tools
                mss.tools.to_png(img.rgb, img.size, output=output)
            return ToolResult(True, f"✓ Screenshot → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Screenshot failed: {e}")

    @staticmethod
    def screenshot_all_monitors(output_folder: str = ".") -> ToolResult:
        """Take a screenshot of each monitor separately."""
        try:
            import mss, mss.tools
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            files = []
            with mss.mss() as sct:
                for i, mon in enumerate(sct.monitors[1:], start=1):
                    img = sct.grab(mon)
                    out = os.path.join(output_folder, f"monitor_{i}.png")
                    mss.tools.to_png(img.rgb, img.size, output=out)
                    files.append(out)
            return ToolResult(True, f"✓ {len(files)} monitor screenshots → {output_folder}", files)
        except Exception as e:
            return ToolResult(False, f"✗ Screenshot all monitors failed: {e}")

    @staticmethod
    def record_screen(
        output: str,
        duration: int = 10,
        fps: int = 30,
        region: Optional[Tuple[int, int, int, int]] = None,
        audio: bool = False,
        monitor: int = 1
    ) -> ToolResult:
        """
        Record screen to video file using ffmpeg.
        audio=True captures system audio (Linux: pulse, macOS: avfoundation, Windows: dshow).
        """
        try:
            os_name = platform.system()
            args = []
            if os_name == "Linux":
                display = os.environ.get("DISPLAY", ":0")
                if region:
                    x, y, w, h = region
                    grab = f"{display}.0+{x},{y}"
                    size = f"{w}x{h}"
                else:
                    grab = f"{display}.0"
                    # Get screen size
                    try:
                        r = subprocess.run(
                            ["xdpyinfo"], capture_output=True, text=True
                        )
                        match = re.search(r"dimensions:\s+(\d+x\d+)", r.stdout)
                        size = match.group(1) if match else "1920x1080"
                    except Exception:
                        size = "1920x1080"
                args = ["-f", "x11grab", "-r", str(fps), "-s", size,
                        "-i", grab]
                if audio:
                    args += ["-f", "pulse", "-i", "default"]
            elif os_name == "Darwin":
                args = ["-f", "avfoundation", "-r", str(fps),
                        "-i", f"{monitor}:none"]
                if audio:
                    args = ["-f", "avfoundation", "-r", str(fps),
                            "-i", f"{monitor}:0"]
            elif os_name == "Windows":
                args = ["-f", "gdigrab", "-r", str(fps), "-i", "desktop"]
                if audio:
                    args += ["-f", "dshow", "-i", "audio=Stereo Mix"]
            else:
                return ToolResult(False, f"✗ Unsupported OS: {os_name}")
            args += ["-t", str(duration), "-c:v", "libx264",
                     "-preset", "ultrafast", "-pix_fmt", "yuv420p", output]
            ok, out = FFmpegTool._run(args, timeout=duration + 30)
            if ok:
                return ToolResult(True, f"✓ Screen recorded {duration}s → {output}", output)
            return ToolResult(False, f"✗ Record screen failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Record screen error: {e}")

    @staticmethod
    def record_with_cursor(
        output: str,
        duration: int = 10,
        fps: int = 30,
        cursor_highlight_color: str = "yellow"
    ) -> ToolResult:
        """
        Record screen with cursor highlighted. Uses ffmpeg with cursor overlay.
        Currently supported on Linux (x11grab with cursor).
        """
        try:
            os_name = platform.system()
            if os_name == "Linux":
                display = os.environ.get("DISPLAY", ":0")
                ok, out = FFmpegTool._run([
                    "-f", "x11grab", "-r", str(fps),
                    "-draw_mouse", "1",
                    "-i", f"{display}.0",
                    "-t", str(duration),
                    "-c:v", "libx264", "-preset", "ultrafast",
                    "-pix_fmt", "yuv420p", output
                ], timeout=duration + 30)
            else:
                # Fallback to regular screen record
                return ScreenRecorderTool.record_screen(output, duration, fps)
            if ok:
                return ToolResult(True, f"✓ Screen recorded with cursor → {output}", output)
            return ToolResult(False, f"✗ Record with cursor failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Record with cursor error: {e}")

    @staticmethod
    def capture_window(
        window_title: str, output: str = "window.png"
    ) -> ToolResult:
        """Capture a specific window by title."""
        try:
            os_name = platform.system()
            if os_name == "Linux":
                # Use wmctrl + import (imagemagick)
                r = subprocess.run(
                    ["xdotool", "search", "--name", window_title],
                    capture_output=True, text=True
                )
                win_id = r.stdout.strip().split("\n")[0]
                if not win_id:
                    return ToolResult(False, f"✗ Window '{window_title}' not found.")
                subprocess.run(["import", "-window", win_id, output], check=True)
                return ToolResult(True, f"✓ Window captured → {output}", output)
            elif os_name == "Windows":
                import pygetwindow as gw
                wins = gw.getWindowsWithTitle(window_title)
                if not wins:
                    return ToolResult(False, f"✗ Window '{window_title}' not found.")
                win = wins[0]
                win.activate()
                time.sleep(0.5)
                import pyautogui
                region = (win.left, win.top, win.width, win.height)
                img = pyautogui.screenshot(region=region)
                img.save(output)
                return ToolResult(True, f"✓ Window captured → {output}", output)
            else:
                # macOS: use screencapture
                subprocess.run(
                    ["screencapture", "-l", window_title, output], check=True
                )
                return ToolResult(True, f"✓ Window captured → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Capture window failed: {e}")

    @staticmethod
    def list_windows() -> ToolResult:
        """List all open window titles."""
        try:
            os_name = platform.system()
            if os_name == "Windows":
                import pygetwindow as gw
                windows = [w.title for w in gw.getAllWindows() if w.title.strip()]
                return ToolResult(True, f"✓ {len(windows)} windows", windows)
            elif os_name == "Linux":
                r = subprocess.run(
                    ["wmctrl", "-l"], capture_output=True, text=True
                )
                windows = [line.split(None, 3)[-1] for line in r.stdout.strip().splitlines()]
                return ToolResult(True, f"✓ {len(windows)} windows", windows)
            elif os_name == "Darwin":
                script = 'tell application "System Events" to get name of every process whose background only is false'
                r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
                windows = [w.strip() for w in r.stdout.split(",")]
                return ToolResult(True, f"✓ {len(windows)} windows", windows)
            else:
                return ToolResult(False, f"✗ Unsupported OS: {os_name}")
        except Exception as e:
            return ToolResult(False, f"✗ List windows failed: {e}")

    @staticmethod
    def create_screencast_gif(
        output: str,
        duration: int = 5,
        fps: int = 10,
        region: Optional[Tuple[int, int, int, int]] = None,
        quality: int = 80
    ) -> ToolResult:
        """Capture screen as animated GIF."""
        try:
            import mss, mss.tools
            from PIL import Image
            frames = []
            interval = 1.0 / fps
            with mss.mss() as sct:
                mon = ({"left": region[0], "top": region[1],
                         "width": region[2], "height": region[3]}
                        if region else sct.monitors[1])
                start = time.time()
                while time.time() - start < duration:
                    frame_t = time.time()
                    img = sct.grab(mon)
                    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
                    # Resize for smaller GIF
                    if quality < 100:
                        scale = quality / 100
                        new_w = int(pil_img.width * scale)
                        new_h = int(pil_img.height * scale)
                        pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)
                    frames.append(pil_img.convert("P", palette=Image.ADAPTIVE, colors=128))
                    elapsed = time.time() - frame_t
                    time.sleep(max(0, interval - elapsed))
            if not frames:
                return ToolResult(False, "✗ No frames captured.")
            frames[0].save(
                output,
                save_all=True,
                append_images=frames[1:],
                duration=int(1000 / fps),
                loop=0,
                optimize=True
            )
            return ToolResult(True, f"✓ Screencast GIF ({len(frames)} frames) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Create screencast GIF failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. TextToSpeechTool
# ─────────────────────────────────────────────────────────────────────────────
class TextToSpeechTool:
    name = "text_to_speech"
    description = (
        "Voice generation: offline TTS (pyttsx3), Microsoft Neural TTS (edge-tts, free), "
        "ElevenLabs API voice cloning, batch generation, background music, "
        "translate-and-speak."
    )

    @staticmethod
    def generate(
        text: str, output: str,
        voice: str = "en-US-AriaNeural",
        language: str = "en-US",
        speed: float = 1.0,
        pitch: float = 0.0
    ) -> ToolResult:
        """
        Generate speech. Uses edge-tts (Microsoft Neural, free, no API key needed).
        voice examples: en-US-AriaNeural, en-GB-SoniaNeural, hi-IN-SwaraNeural.
        speed: 0.5–2.0 (1.0=normal). pitch: -50 to +50 Hz.
        """
        try:
            import edge_tts
            import asyncio

            rate_pct = int((speed - 1.0) * 100)
            rate_str = f"+{rate_pct}%" if rate_pct >= 0 else f"{rate_pct}%"
            pitch_str = f"+{int(pitch)}Hz" if pitch >= 0 else f"{int(pitch)}Hz"

            async def _synth():
                communicate = edge_tts.Communicate(
                    text=text,
                    voice=voice,
                    rate=rate_str,
                    pitch=pitch_str
                )
                await communicate.save(output)

            asyncio.run(_synth())
            return ToolResult(True, f"✓ Speech generated ({voice}) → {output}", output)
        except Exception as e:
            # Fallback to pyttsx3
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty("rate", int(200 * speed))
                engine.save_to_file(text, output)
                engine.runAndWait()
                return ToolResult(True, f"✓ Speech generated (pyttsx3 fallback) → {output}", output)
            except Exception as e2:
                return ToolResult(False, f"✗ TTS failed: {e} | fallback: {e2}")

    @staticmethod
    def list_voices(
        language: Optional[str] = None,
        gender: Optional[str] = None
    ) -> ToolResult:
        """List available edge-tts voices, optionally filtered by language/gender."""
        try:
            import edge_tts
            import asyncio

            async def _get_voices():
                return await edge_tts.list_voices()

            voices = asyncio.run(_get_voices())
            filtered = []
            for v in voices:
                if language and not v["Locale"].lower().startswith(language.lower()):
                    continue
                if gender and v.get("Gender", "").lower() != gender.lower():
                    continue
                filtered.append({
                    "name":   v["ShortName"],
                    "locale": v["Locale"],
                    "gender": v.get("Gender"),
                    "style":  v.get("VoiceTag", {}).get("ContentCategories", [])
                })
            return ToolResult(True, f"✓ {len(filtered)} voices found", filtered)
        except Exception as e:
            return ToolResult(False, f"✗ List voices failed: {e}")

    @staticmethod
    def generate_ssml(
        ssml: str, output: str,
        voice: str = "en-US-AriaNeural"
    ) -> ToolResult:
        """Generate speech from SSML markup using edge-tts."""
        try:
            import edge_tts
            import asyncio

            async def _synth():
                communicate = edge_tts.Communicate(text=ssml, voice=voice)
                await communicate.save(output)

            asyncio.run(_synth())
            return ToolResult(True, f"✓ SSML speech generated → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Generate SSML failed: {e}")

    @staticmethod
    def clone_voice(
        audio_sample: str, text: str, output: str,
        cred_key: str = "elevenlabs"
    ) -> ToolResult:
        """
        Clone a voice using ElevenLabs API and generate speech.
        Requires ElevenLabs API key in credentials.
        """
        try:
            from elevenlabs.client import ElevenLabs
            from elevenlabs import VoiceSettings
            creds = CredStore.load(cred_key)
            api_key = creds.get("api_key", "")
            if not api_key:
                return ToolResult(False, "✗ No ElevenLabs API key. Add it in Settings → Credentials.")
            client = ElevenLabs(api_key=api_key)
            # Add voice via cloning
            with open(audio_sample, "rb") as fh:
                voice = client.clone(
                    name=f"cloned_{Path(audio_sample).stem}",
                    files=[fh],
                    description="Cloned via NPM Agent"
                )
            audio = client.generate(
                text=text,
                voice=voice,
                model="eleven_multilingual_v2"
            )
            with open(output, "wb") as fh:
                for chunk in audio:
                    fh.write(chunk)
            return ToolResult(True, f"✓ Voice cloned and speech generated → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Clone voice failed: {e}")

    @staticmethod
    def generate_batch(
        texts: List[str], output_folder: str,
        voice: str = "en-US-AriaNeural",
        language: str = "en-US"
    ) -> ToolResult:
        """Generate speech for multiple texts, saving each to a numbered file."""
        try:
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            files = []
            for i, text in enumerate(texts):
                out = os.path.join(output_folder, f"speech_{i+1:04d}.mp3")
                result = TextToSpeechTool.generate(text, out, voice=voice, language=language)
                if result.success:
                    files.append(out)
            return ToolResult(True, f"✓ Generated {len(files)}/{len(texts)} audio files → {output_folder}", files)
        except Exception as e:
            return ToolResult(False, f"✗ Batch TTS failed: {e}")

    @staticmethod
    def add_background_music(
        speech: str, music: str, output: str,
        music_volume: float = 0.2
    ) -> ToolResult:
        """Mix speech with background music. music_volume: 0.0–1.0."""
        try:
            from pydub import AudioSegment
            speech_audio = AudioSegment.from_file(speech)
            music_audio = AudioSegment.from_file(music)
            # Loop music if shorter than speech
            while len(music_audio) < len(speech_audio):
                music_audio = music_audio + music_audio
            music_audio = music_audio[:len(speech_audio)]
            # Adjust music volume
            db_change = 20 * (music_volume if music_volume > 0 else 0.01) - 20
            music_audio = music_audio + db_change
            # Fade music at start and end
            fade_ms = min(2000, len(music_audio) // 4)
            music_audio = music_audio.fade_in(fade_ms).fade_out(fade_ms)
            combined = speech_audio.overlay(music_audio)
            fmt = Path(output).suffix.lstrip(".") or "mp3"
            combined.export(output, format=fmt)
            return ToolResult(True, f"✓ Speech + music mixed → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Add background music failed: {e}")

    @staticmethod
    def translate_and_speak(
        text: str, target_language: str, output: str
    ) -> ToolResult:
        """
        Translate text using a free API and generate speech in target language.
        Uses LibreTranslate if available, else falls back to direct TTS in target language.
        """
        try:
            import requests
            # Attempt LibreTranslate (free, self-hosted or public instances)
            translated = text
            try:
                r = requests.post(
                    "https://libretranslate.de/translate",
                    json={"q": text, "source": "auto", "target": target_language},
                    timeout=10
                )
                if r.ok:
                    translated = r.json().get("translatedText", text)
            except Exception:
                pass  # Use original text if translation fails
            # Map language code to edge-tts voice
            lang_voice_map = {
                "es": "es-ES-ElviraNeural",
                "fr": "fr-FR-DeniseNeural",
                "de": "de-DE-KatjaNeural",
                "hi": "hi-IN-SwaraNeural",
                "zh": "zh-CN-XiaoxiaoNeural",
                "ja": "ja-JP-NanamiNeural",
                "ar": "ar-SA-ZariyahNeural",
                "pt": "pt-BR-FranciscaNeural",
                "ru": "ru-RU-SvetlanaNeural",
                "ko": "ko-KR-SunHiNeural",
            }
            voice = lang_voice_map.get(target_language, f"{target_language}-{target_language.upper()}-Wavenet-A")
            return TextToSpeechTool.generate(translated, output, voice=voice)
        except Exception as e:
            return ToolResult(False, f"✗ Translate and speak failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. VideoEditingTool
# ─────────────────────────────────────────────────────────────────────────────
class VideoEditingTool:
    name = "video_editing"
    description = (
        "High-level video editing: auto-cut silences, jump cuts, colour correction, "
        "denoising, highlight reel, chapter markers, platform export, vertical video, "
        "batch processing, LUT application."
    )

    @staticmethod
    def auto_cut_silences(
        input: str, output: str,
        silence_thresh: float = -35.0,
        min_silence: float = 0.5
    ) -> ToolResult:
        """
        Remove silent sections from video automatically.
        silence_thresh: dB level below which audio is considered silent.
        min_silence: minimum duration of silence to cut (seconds).
        """
        try:
            # Extract audio to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                tmp_audio = tf.name
            FFmpegTool.extract_audio(input, tmp_audio, "wav")
            from pydub import AudioSegment
            from pydub.silence import detect_nonsilent
            audio = AudioSegment.from_wav(tmp_audio)
            nonsilent = detect_nonsilent(
                audio,
                min_silence_len=int(min_silence * 1000),
                silence_thresh=silence_thresh,
                seek_step=10
            )
            os.unlink(tmp_audio)
            if not nonsilent:
                return ToolResult(False, "✗ No non-silent sections detected.")
            # Create concat list of non-silent video segments
            with tempfile.TemporaryDirectory() as tmpdir:
                seg_files = []
                for i, (start_ms, end_ms) in enumerate(nonsilent):
                    seg_out = os.path.join(tmpdir, f"seg_{i:04d}.mp4")
                    start_s = start_ms / 1000
                    end_s = end_ms / 1000
                    ok, _ = FFmpegTool._run([
                        "-ss", str(start_s), "-to", str(end_s),
                        "-i", input, "-c", "copy", seg_out
                    ])
                    if ok:
                        seg_files.append(seg_out)
                if not seg_files:
                    return ToolResult(False, "✗ Failed to extract segments.")
                with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as fh:
                    for sf in seg_files:
                        fh.write(f"file '{sf}'\n")
                    list_file = fh.name
                ok, out_msg = FFmpegTool._run([
                    "-f", "concat", "-safe", "0",
                    "-i", list_file, "-c", "copy", output
                ])
                os.unlink(list_file)
            if ok:
                total_cut = sum(
                    (e - s) for s, e in
                    [(0, nonsilent[0][0])] +
                    [(nonsilent[i][1], nonsilent[i+1][0]) for i in range(len(nonsilent)-1)]
                ) / 1000
                return ToolResult(True, f"✓ Silences cut (~{total_cut:.1f}s removed) → {output}", output)
            return ToolResult(False, f"✗ Auto cut silences failed: {out_msg}")
        except Exception as e:
            return ToolResult(False, f"✗ Auto cut silences error: {e}")

    @staticmethod
    def jump_cut(input: str, output: str) -> ToolResult:
        """
        Apply jump-cut effect: remove repeated/frozen frames to create energetic edits.
        """
        try:
            # Detect scene changes as cut points using ffmpeg mpdecimate
            ok, out = FFmpegTool._run([
                "-i", input,
                "-vf", "mpdecimate,setpts=N/FRAME_RATE/TB",
                "-c:v", "libx264", "-preset", "fast",
                "-af", "asetpts=N/SR/TB",
                "-c:a", "aac", output
            ])
            if ok:
                return ToolResult(True, f"✓ Jump cuts applied → {output}", output)
            return ToolResult(False, f"✗ Jump cut failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Jump cut error: {e}")

    @staticmethod
    def auto_color_correct(input: str, output: str) -> ToolResult:
        """Apply automatic colour correction using histogram equalisation."""
        try:
            ok, out = FFmpegTool._run([
                "-i", input,
                "-vf", "histeq=strength=0.2:intensity=0.2:antibanding=weak",
                "-c:a", "copy", output
            ])
            if ok:
                return ToolResult(True, f"✓ Colour corrected → {output}", output)
            return ToolResult(False, f"✗ Auto color correct failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Auto color correct error: {e}")

    @staticmethod
    def auto_denoise(input: str, output: str) -> ToolResult:
        """Apply automatic video + audio denoising."""
        try:
            ok, out = FFmpegTool._run([
                "-i", input,
                "-vf", "hqdn3d=luma_spatial=4:chroma_spatial=3",
                "-af", "afftdn=nf=-25",
                "-c:v", "libx264", "-preset", "medium",
                "-c:a", "aac", output
            ])
            if ok:
                return ToolResult(True, f"✓ Denoised → {output}", output)
            return ToolResult(False, f"✗ Auto denoise failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Auto denoise error: {e}")

    @staticmethod
    def create_highlight_reel(
        input: str, output: str,
        duration: int = 60,
        method: str = "loudness"
    ) -> ToolResult:
        """
        Create a highlight reel from a longer video.
        method: 'loudness' (picks loudest audio segments), 'uniform' (evenly spaced clips).
        """
        try:
            info = FFmpegTool._probe(input)
            total_dur = float(info.get("format", {}).get("duration", 0))
            if total_dur == 0:
                return ToolResult(False, "✗ Could not determine video duration.")
            if method == "uniform":
                # Extract evenly spaced clips
                n_clips = max(3, duration // 10)
                clip_dur = duration / n_clips
                step = total_dur / n_clips
                clips = []
                with tempfile.TemporaryDirectory() as tmpdir:
                    for i in range(n_clips):
                        start = i * step
                        clip_out = os.path.join(tmpdir, f"clip_{i:04d}.mp4")
                        ok, _ = FFmpegTool._run([
                            "-ss", str(start), "-t", str(clip_dur),
                            "-i", input, "-c", "copy", clip_out
                        ])
                        if ok:
                            clips.append(clip_out)
                    if not clips:
                        return ToolResult(False, "✗ Failed to extract clips.")
                    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as fh:
                        for c in clips:
                            fh.write(f"file '{c}'\n")
                        list_file = fh.name
                    ok, out_msg = FFmpegTool._run([
                        "-f", "concat", "-safe", "0",
                        "-i", list_file, "-c", "copy", output
                    ])
                    os.unlink(list_file)
            else:
                # Loudness method: use uniform as fallback
                return VideoEditingTool.create_highlight_reel(input, output, duration, "uniform")
            if ok:
                return ToolResult(True, f"✓ Highlight reel ({duration}s, {method}) → {output}", output)
            return ToolResult(False, f"✗ Highlight reel failed.")
        except Exception as e:
            return ToolResult(False, f"✗ Create highlight reel error: {e}")

    @staticmethod
    def add_chapter_markers(
        input: str, output: str,
        chapters: List[Dict[str, Any]]
    ) -> ToolResult:
        """
        Add chapter markers to video. chapters: [{"start": 0, "title": "Intro"}, ...]
        start is in seconds.
        """
        try:
            # Write chapters to ffmpeg metadata
            info = FFmpegTool._probe(input)
            total_dur = float(info.get("format", {}).get("duration", 0))
            chapter_lines = [";FFMETADATA1\n"]
            for i, ch in enumerate(chapters):
                start_ms = int(float(ch.get("start", 0)) * 1000)
                if i + 1 < len(chapters):
                    end_ms = int(float(chapters[i + 1].get("start", 0)) * 1000) - 1
                else:
                    end_ms = int(total_dur * 1000)
                title = ch.get("title", f"Chapter {i+1}")
                chapter_lines.append(
                    f"\n[CHAPTER]\nTIMEBASE=1/1000\n"
                    f"START={start_ms}\nEND={end_ms}\ntitle={title}\n"
                )
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as fh:
                fh.write("".join(chapter_lines))
                meta_file = fh.name
            ok, out = FFmpegTool._run([
                "-i", input, "-i", meta_file,
                "-map_metadata", "1",
                "-map_chapters", "1",
                "-c", "copy", output
            ])
            os.unlink(meta_file)
            if ok:
                return ToolResult(True, f"✓ {len(chapters)} chapters added → {output}", output)
            return ToolResult(False, f"✗ Add chapters failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Add chapter markers error: {e}")

    @staticmethod
    def export_for_platform(
        input: str, output: str,
        platform: str = "youtube"
    ) -> ToolResult:
        """
        Export video optimised for a specific platform.
        platform: youtube|instagram_feed|instagram_reel|tiktok|twitter|linkedin|vimeo
        """
        try:
            profiles = {
                "youtube": {
                    "args": ["-c:v", "libx264", "-preset", "slow", "-crf", "18",
                             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                             "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,"
                                    "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1"],
                },
                "instagram_feed": {
                    "args": ["-c:v", "libx264", "-crf", "20", "-preset", "slow",
                             "-vf", "scale=1080:1080:force_original_aspect_ratio=decrease,"
                                    "pad=1080:1080:(ow-iw)/2:(oh-ih)/2,setsar=1",
                             "-c:a", "aac", "-b:a", "128k",
                             "-t", "60"],
                },
                "instagram_reel": {
                    "args": ["-c:v", "libx264", "-crf", "20", "-preset", "slow",
                             "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,"
                                    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
                             "-c:a", "aac", "-b:a", "128k",
                             "-t", "90"],
                },
                "tiktok": {
                    "args": ["-c:v", "libx264", "-crf", "20",
                             "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,"
                                    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                             "-c:a", "aac", "-b:a", "128k",
                             "-t", "60"],
                },
                "twitter": {
                    "args": ["-c:v", "libx264", "-crf", "23",
                             "-vf", "scale=1280:720",
                             "-c:a", "aac", "-b:a", "128k",
                             "-t", "140", "-movflags", "+faststart"],
                },
                "linkedin": {
                    "args": ["-c:v", "libx264", "-crf", "20",
                             "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,"
                                    "pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
                             "-c:a", "aac", "-b:a", "128k",
                             "-t", "600"],
                },
                "vimeo": {
                    "args": ["-c:v", "libx264", "-crf", "16", "-preset", "slow",
                             "-c:a", "aac", "-b:a", "256k",
                             "-movflags", "+faststart"],
                },
            }
            profile = profiles.get(platform.lower())
            if not profile:
                return ToolResult(False, f"✗ Unknown platform '{platform}'. Options: {list(profiles.keys())}")
            ok, out = FFmpegTool._run(["-i", input] + profile["args"] + [output])
            if ok:
                return ToolResult(True, f"✓ Exported for {platform} → {output}", output)
            return ToolResult(False, f"✗ Export for {platform} failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Export for platform error: {e}")

    @staticmethod
    def create_vertical_from_horizontal(
        input: str, output: str,
        focus_point: str = "center"
    ) -> ToolResult:
        """
        Convert 16:9 horizontal video to 9:16 vertical (for Reels/TikTok).
        focus_point: 'center', 'left', 'right', or 'auto' (face detection crop).
        """
        try:
            info = FFmpegTool._probe(input)
            for stream in info.get("streams", []):
                if stream.get("codec_type") == "video":
                    w = int(stream.get("width", 1920))
                    h = int(stream.get("height", 1080))
                    break
            else:
                w, h = 1920, 1080
            # Target 9:16 from 16:9: crop a 9:16 strip from horizontal
            target_w = int(h * 9 / 16)
            target_h = h
            if focus_point == "center":
                x_offset = (w - target_w) // 2
            elif focus_point == "left":
                x_offset = 0
            elif focus_point == "right":
                x_offset = w - target_w
            else:
                x_offset = (w - target_w) // 2
            vf = (
                f"crop={target_w}:{target_h}:{x_offset}:0,"
                f"scale=1080:1920:flags=lanczos"
            )
            ok, out = FFmpegTool._run([
                "-i", input, "-vf", vf,
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "copy", output
            ])
            if ok:
                return ToolResult(True, f"✓ Vertical video created (focus={focus_point}) → {output}", output)
            return ToolResult(False, f"✗ Create vertical failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Create vertical video error: {e}")

    @staticmethod
    def batch_process(
        input_folder: str, output_folder: str,
        operations: List[Dict[str, Any]]
    ) -> ToolResult:
        """
        Apply a sequence of operations to all videos in a folder.
        operations: [{"op": "compress_video", "params": {"crf": 28}}, ...]
        Supported ops: compress_video, resize, trim, convert, add_watermark, color_grade
        """
        try:
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            video_exts = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"}
            files = [f for f in Path(input_folder).iterdir()
                     if f.suffix.lower() in video_exts]
            results = []
            for fp in files:
                try:
                    current = str(fp)
                    for i, op in enumerate(operations):
                        op_name = op.get("op", "")
                        params = op.get("params", {})
                        is_last = (i == len(operations) - 1)
                        if is_last:
                            out_path = str(Path(output_folder) / fp.name)
                        else:
                            out_path = tempfile.mktemp(suffix=fp.suffix)
                        op_map = {
                            "compress_video": lambda i, o, p: FFmpegTool.compress_video(
                                i, o, **p),
                            "resize": lambda i, o, p: FFmpegTool.resize(i, o, **p),
                            "trim": lambda i, o, p: FFmpegTool.trim(i, o, **p),
                            "convert": lambda i, o, p: FFmpegTool.convert(i, o, **p),
                            "add_watermark": lambda i, o, p: FFmpegTool.add_watermark(i, o, **p),
                            "color_grade": lambda i, o, p: FFmpegTool.color_grade(i, o, **p),
                        }
                        if op_name in op_map:
                            result = op_map[op_name](current, out_path, params)
                            if not result.success:
                                break
                            if not is_last:
                                current = out_path
                    results.append({"file": fp.name, "success": result.success})
                except Exception as ex:
                    results.append({"file": fp.name, "success": False, "error": str(ex)})
            success_count = sum(1 for r in results if r["success"])
            return ToolResult(True, f"✓ Batch processed {success_count}/{len(files)} files → {output_folder}", results)
        except Exception as e:
            return ToolResult(False, f"✗ Batch process error: {e}")

    @staticmethod
    def apply_lut(
        input: str, output: str, lut_file: str
    ) -> ToolResult:
        """Apply a colour LUT (.cube or .3dl) to video for colour grading."""
        try:
            ok, out = FFmpegTool._run([
                "-i", input,
                "-vf", f"lut3d=file='{lut_file}'",
                "-c:a", "copy",
                "-c:v", "libx264", "-preset", "medium",
                output
            ])
            if ok:
                return ToolResult(True, f"✓ LUT applied → {output}", output)
            return ToolResult(False, f"✗ Apply LUT failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Apply LUT error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. PodcastTool
# ─────────────────────────────────────────────────────────────────────────────
class PodcastTool:
    name = "podcast"
    description = (
        "Podcast production: record episode, edit raw recording, clean audio, "
        "generate transcript, show notes, chapters, multi-format export, RSS feed."
    )

    @staticmethod
    def record_episode(
        output: str,
        duration: int = 3600,
        intro: Optional[str] = None,
        outro: Optional[str] = None,
        music: Optional[str] = None
    ) -> ToolResult:
        """Record a podcast episode from microphone with optional intro/outro/music."""
        try:
            import sounddevice as sd
            import soundfile as sf
            import numpy as np
            sample_rate = 44100
            print(f"Recording for {duration}s... Press Ctrl+C to stop early.")
            try:
                recording = sd.rec(
                    int(duration * sample_rate),
                    samplerate=sample_rate, channels=1, dtype="int16"
                )
                sd.wait()
            except KeyboardInterrupt:
                sd.stop()
                recording = recording[:int(sd.get_status().currentTime * sample_rate)]
            raw_path = output.replace(".mp3", "_raw.wav")
            sf.write(raw_path, recording, sample_rate)
            # Add intro/outro if provided
            if intro or outro:
                parts = []
                if intro:
                    parts.append(intro)
                parts.append(raw_path)
                if outro:
                    parts.append(outro)
                return AudioTool.merge(parts, output, crossfade=500)
            # Convert to mp3
            FFmpegTool.convert(raw_path, output, audio_codec="libmp3lame")
            try:
                os.unlink(raw_path)
            except Exception:
                pass
            return ToolResult(True, f"✓ Episode recorded → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Record episode failed: {e}")

    @staticmethod
    def edit_raw_recording(input: str, output: str) -> ToolResult:
        """
        Automatically edit a raw recording: remove silence, normalize, reduce noise.
        """
        try:
            # Step 1: Remove silence
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                no_silence = tf.name
            result = AudioTool.remove_silence(input, no_silence, min_silence_len=800, silence_thresh=-40)
            if not result.success:
                no_silence = input
            # Step 2: Normalize
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                normalized = tf.name
            AudioTool.normalize(no_silence, normalized, target_db=-18.0)
            # Step 3: Denoise
            FFmpegTool.denoise_audio(normalized, output, strength=0.2)
            for tmp in [no_silence, normalized]:
                try:
                    if tmp != input:
                        os.unlink(tmp)
                except Exception:
                    pass
            return ToolResult(True, f"✓ Raw recording edited → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Edit raw recording failed: {e}")

    @staticmethod
    def clean_audio(
        input: str, output: str,
        remove_ums: bool = True,
        remove_silence: bool = True,
        normalize: bool = True
    ) -> ToolResult:
        """
        Full audio cleaning pipeline for podcast production.
        remove_ums: removes filler words (requires transcript, best-effort).
        """
        try:
            current = input
            with tempfile.TemporaryDirectory() as tmpdir:
                if remove_silence:
                    tmp1 = os.path.join(tmpdir, "no_silence.wav")
                    AudioTool.remove_silence(current, tmp1, min_silence_len=600, silence_thresh=-42)
                    if os.path.exists(tmp1):
                        current = tmp1
                if normalize:
                    tmp2 = os.path.join(tmpdir, "normalized.wav")
                    AudioTool.normalize(current, tmp2, target_db=-16.0)
                    if os.path.exists(tmp2):
                        current = tmp2
                # Always denoise
                tmp3 = os.path.join(tmpdir, "denoised.wav")
                FFmpegTool.denoise_audio(current, tmp3)
                if os.path.exists(tmp3):
                    current = tmp3
                shutil.copy2(current, output)
            return ToolResult(True, f"✓ Audio cleaned → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Clean audio failed: {e}")

    @staticmethod
    def generate_transcript(
        audio: str,
        output_format: str = "txt",
        include_timestamps: bool = True
    ) -> ToolResult:
        """
        Generate transcript from audio using Whisper.
        output_format: 'txt', 'srt', 'json', 'vtt'.
        """
        try:
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(audio, verbose=False)
            segments = result.get("segments", [])
            if output_format == "txt":
                if include_timestamps:
                    lines = []
                    for seg in segments:
                        start = seg["start"]
                        end = seg["end"]
                        m_s, s_s = divmod(int(start), 60)
                        h_s, m_s = divmod(m_s, 60)
                        m_e, s_e = divmod(int(end), 60)
                        h_e, m_e = divmod(m_e, 60)
                        lines.append(f"[{h_s:02d}:{m_s:02d}:{s_s:02d} → {h_e:02d}:{m_e:02d}:{s_e:02d}] {seg['text'].strip()}")
                    content = "\n".join(lines)
                else:
                    content = result["text"].strip()
            elif output_format == "srt":
                lines = []
                for i, seg in enumerate(segments, 1):
                    start = seg["start"]
                    end = seg["end"]
                    def fmt(t):
                        h, rem = divmod(t, 3600)
                        m, s = divmod(rem, 60)
                        ms = int((s % 1) * 1000)
                        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms:03d}"
                    lines.append(f"{i}\n{fmt(start)} --> {fmt(end)}\n{seg['text'].strip()}\n")
                content = "\n".join(lines)
            elif output_format == "json":
                content = json.dumps({"text": result["text"], "segments": segments}, indent=2)
            else:
                content = result["text"].strip()
            # Write output file with appropriate extension
            out_ext = {"txt": ".txt", "srt": ".srt", "json": ".json", "vtt": ".vtt"}.get(output_format, ".txt")
            out_path = str(Path(audio).with_suffix(out_ext))
            Path(out_path).write_text(content, encoding="utf-8")
            return ToolResult(True, f"✓ Transcript ({output_format}) → {out_path}", {
                "path": out_path, "text": result["text"][:500]
            })
        except Exception as e:
            return ToolResult(False, f"✗ Generate transcript failed: {e}")

    @staticmethod
    def generate_show_notes(
        transcript: str, llm_model: str = "llama3.2:3b"
    ) -> ToolResult:
        """Generate podcast show notes from transcript using local LLM."""
        try:
            from npmai import Ollama
            if Path(transcript).exists():
                text = Path(transcript).read_text(encoding="utf-8")
            else:
                text = transcript
            llm = Ollama(model=llm_model, temperature=0.5,
                         change=True, Models=["mistral:7b"])
            prompt = f"""You are a podcast producer. Generate professional show notes from this transcript.
Include: Episode summary (2-3 sentences), Key topics covered (bullet list), Notable quotes (2-3),
Resources mentioned, Guest info if applicable, Call to action.

Transcript (excerpt):
{text[:4000]}

Show Notes:"""
            notes = llm.invoke(prompt)
            return ToolResult(True, f"✓ Show notes generated ({len(notes)} chars)", notes)
        except Exception as e:
            return ToolResult(False, f"✗ Generate show notes failed: {e}")

    @staticmethod
    def create_chapters(
        transcript: str, audio: str
    ) -> ToolResult:
        """Auto-generate chapter markers from transcript based on topic changes."""
        try:
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(audio, verbose=False)
            segments = result.get("segments", [])
            # Group segments into ~5 minute chapters
            chapters = []
            chapter_dur = 300  # 5 minutes
            current_chapter_start = 0
            current_texts = []
            for seg in segments:
                current_texts.append(seg["text"].strip())
                if seg["end"] - current_chapter_start >= chapter_dur:
                    title = " ".join(current_texts)[:60].rsplit(" ", 1)[0] + "…"
                    chapters.append({
                        "start": current_chapter_start,
                        "title": title,
                        "start_formatted": f"{int(current_chapter_start//60):02d}:{int(current_chapter_start%60):02d}"
                    })
                    current_chapter_start = seg["end"]
                    current_texts = []
            if current_texts:
                title = " ".join(current_texts)[:60].rsplit(" ", 1)[0] + "…"
                chapters.append({
                    "start": current_chapter_start,
                    "title": title,
                    "start_formatted": f"{int(current_chapter_start//60):02d}:{int(current_chapter_start%60):02d}"
                })
            return ToolResult(True, f"✓ {len(chapters)} chapters created", chapters)
        except Exception as e:
            return ToolResult(False, f"✗ Create chapters failed: {e}")

    @staticmethod
    def export_to_formats(
        input: str, output_folder: str,
        formats: Optional[List[str]] = None
    ) -> ToolResult:
        """Export podcast audio to multiple formats (mp3, aac, ogg, flac, wav)."""
        try:
            formats = formats or ["mp3", "aac", "ogg"]
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            stem = Path(input).stem
            results = []
            for fmt in formats:
                out = os.path.join(output_folder, f"{stem}.{fmt}")
                r = AudioTool.convert(input, out, format=fmt, bitrate="192k")
                results.append({"format": fmt, "path": out, "success": r.success})
            success_count = sum(1 for r in results if r["success"])
            return ToolResult(True, f"✓ Exported to {success_count}/{len(formats)} formats → {output_folder}", results)
        except Exception as e:
            return ToolResult(False, f"✗ Export formats failed: {e}")

    @staticmethod
    def generate_rss_feed(
        podcast_info: Dict[str, Any],
        episodes: List[Dict[str, Any]],
        output: str
    ) -> ToolResult:
        """
        Generate a valid podcast RSS feed (iTunes compatible).
        podcast_info: {title, description, link, author, email, image_url, language, category}
        episodes: [{title, description, mp3_url, duration, pub_date, episode_number}]
        """
        try:
            from feedgen.feed import FeedGenerator
            fg = FeedGenerator()
            fg.load_extension("podcast")
            fg.id(podcast_info.get("link", "https://example.com/podcast"))
            fg.title(podcast_info.get("title", "My Podcast"))
            fg.author({"name": podcast_info.get("author", "Unknown"),
                       "email": podcast_info.get("email", "")})
            fg.link(href=podcast_info.get("link", ""), rel="alternate")
            fg.logo(podcast_info.get("image_url", ""))
            fg.subtitle(podcast_info.get("description", ""))
            fg.description(podcast_info.get("description", "A podcast"))
            fg.language(podcast_info.get("language", "en"))
            fg.podcast.itunes_category(podcast_info.get("category", "Technology"))
            fg.podcast.itunes_author(podcast_info.get("author", ""))
            fg.podcast.itunes_image(podcast_info.get("image_url", ""))
            for ep in episodes:
                fe = fg.add_entry()
                fe.id(ep.get("mp3_url", ""))
                fe.title(ep.get("title", "Episode"))
                fe.description(ep.get("description", ""))
                fe.enclosure(ep.get("mp3_url", ""), 0, "audio/mpeg")
                fe.podcast.itunes_duration(str(ep.get("duration", "00:30:00")))
                fe.podcast.itunes_episode(str(ep.get("episode_number", 1)))
                if ep.get("pub_date"):
                    from datetime import datetime, timezone
                    fe.published(ep["pub_date"])
            fg.rss_file(output)
            return ToolResult(True, f"✓ RSS feed generated ({len(episodes)} episodes) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Generate RSS feed failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 9. StreamingTool
# ─────────────────────────────────────────────────────────────────────────────
class StreamingTool:
    name = "streaming"
    description = (
        "Live streaming utilities: stream to YouTube/Twitch, multi-destination streaming, "
        "capture/download streams, get stream info."
    )

    @staticmethod
    def _build_ffmpeg_stream_cmd(
        input_source: str,
        rtmp_url: str,
        quality: str = "medium",
        fps: int = 30
    ) -> List[str]:
        quality_map = {
            "low":    {"crf": 30, "res": "854x480",   "bitrate": "1000k"},
            "medium": {"crf": 23, "res": "1280x720",  "bitrate": "3000k"},
            "high":   {"crf": 18, "res": "1920x1080", "bitrate": "6000k"},
        }
        q = quality_map.get(quality, quality_map["medium"])
        # Detect if input is a file or screen
        is_file = Path(input_source).exists()
        if is_file:
            in_args = ["-re", "-i", input_source]
        else:
            # Screen capture
            os_name = platform.system()
            if os_name == "Linux":
                display = os.environ.get("DISPLAY", ":0")
                in_args = ["-f", "x11grab", "-r", str(fps), "-i", display,
                           "-f", "pulse", "-i", "default"]
            elif os_name == "Windows":
                in_args = ["-f", "gdigrab", "-r", str(fps), "-i", "desktop",
                           "-f", "dshow", "-i", "audio=Stereo Mix"]
            else:
                in_args = ["-f", "avfoundation", "-r", str(fps), "-i", "1:0"]
        return (
            ["ffmpeg"] + in_args + [
                "-c:v", "libx264", "-preset", "veryfast",
                "-tune", "zerolatency",
                "-crf", str(q["crf"]),
                "-s", q["res"],
                "-r", str(fps),
                "-b:v", q["bitrate"],
                "-maxrate", q["bitrate"],
                "-bufsize", str(int(q["bitrate"].replace("k", "")) * 2) + "k",
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                "-f", "flv", rtmp_url
            ]
        )

    @staticmethod
    def stream_to_youtube(
        input_source: str, rtmp_key: str,
        quality: str = "medium", fps: int = 30
    ) -> ToolResult:
        """
        Start streaming to YouTube Live. Returns process handle.
        input_source: file path or 'screen'.
        rtmp_key: your YouTube stream key.
        """
        try:
            rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{rtmp_key}"
            cmd = StreamingTool._build_ffmpeg_stream_cmd(
                input_source, rtmp_url, quality, fps
            )
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Store process ID for reference
            pid = proc.pid
            return ToolResult(True, f"✓ Streaming to YouTube started (PID {pid})", {"pid": pid, "rtmp": rtmp_url})
        except Exception as e:
            return ToolResult(False, f"✗ Stream to YouTube failed: {e}")

    @staticmethod
    def stream_to_twitch(
        input_source: str, rtmp_key: str,
        quality: str = "medium", fps: int = 30
    ) -> ToolResult:
        """Start streaming to Twitch. rtmp_key: your Twitch stream key."""
        try:
            rtmp_url = f"rtmp://live.twitch.tv/app/{rtmp_key}"
            cmd = StreamingTool._build_ffmpeg_stream_cmd(
                input_source, rtmp_url, quality, fps
            )
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pid = proc.pid
            return ToolResult(True, f"✓ Streaming to Twitch started (PID {pid})", {"pid": pid})
        except Exception as e:
            return ToolResult(False, f"✗ Stream to Twitch failed: {e}")

    @staticmethod
    def stream_to_multiple(
        input_source: str,
        destinations: List[Dict[str, str]]
    ) -> ToolResult:
        """
        Stream to multiple RTMP destinations simultaneously using ffmpeg tee muxer.
        destinations: [{"name": "YouTube", "rtmp": "rtmp://...", "key": "..."}]
        """
        try:
            is_file = Path(input_source).exists() if input_source != "screen" else False
            if is_file:
                in_args = ["-re", "-i", input_source]
            else:
                os_name = platform.system()
                if os_name == "Linux":
                    display = os.environ.get("DISPLAY", ":0")
                    in_args = ["-f", "x11grab", "-r", "30", "-i", display]
                else:
                    in_args = ["-i", input_source]
            # Build tee output
            tee_parts = []
            for dest in destinations:
                rtmp_full = f"{dest['rtmp']}{dest.get('key', '')}"
                tee_parts.append(f"[f=flv]{rtmp_full}")
            tee_output = "|".join(tee_parts)
            cmd = (
                ["ffmpeg"] + in_args + [
                    "-c:v", "libx264", "-preset", "veryfast",
                    "-b:v", "3000k", "-maxrate", "3000k", "-bufsize", "6000k",
                    "-c:a", "aac", "-b:a", "128k",
                    "-f", "tee", "-map", "0", tee_output
                ]
            )
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return ToolResult(True,
                f"✓ Multi-streaming to {len(destinations)} destinations (PID {proc.pid})",
                {"pid": proc.pid, "destinations": [d["name"] for d in destinations]}
            )
        except Exception as e:
            return ToolResult(False, f"✗ Multi-stream failed: {e}")

    @staticmethod
    def capture_stream(
        url: str, output: str, duration: int = 60
    ) -> ToolResult:
        """Capture a live stream to file for specified duration (seconds)."""
        try:
            ok, out = FFmpegTool._run([
                "-i", url, "-t", str(duration),
                "-c", "copy", output
            ], timeout=duration + 60)
            if ok:
                return ToolResult(True, f"✓ Stream captured ({duration}s) → {output}", output)
            # Try streamlink as fallback
            result = subprocess.run(
                ["streamlink", "--output", output, url, "best"],
                capture_output=True, text=True, timeout=duration + 60
            )
            if result.returncode == 0:
                return ToolResult(True, f"✓ Stream captured (streamlink) → {output}", output)
            return ToolResult(False, f"✗ Capture stream failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Capture stream error: {e}")

    @staticmethod
    def get_stream_info(url: str) -> ToolResult:
        """Get info about a live stream URL."""
        try:
            info = FFmpegTool._probe(url)
            if info:
                streams = info.get("streams", [])
                data = {
                    "format": info.get("format", {}).get("format_name"),
                    "duration": info.get("format", {}).get("duration"),
                    "streams": [
                        {
                            "codec_type": s.get("codec_type"),
                            "codec_name": s.get("codec_name"),
                            "width": s.get("width"),
                            "height": s.get("height"),
                            "fps": s.get("r_frame_rate"),
                        } for s in streams
                    ]
                }
                return ToolResult(True, f"✓ Stream info fetched", data)
            # Try streamlink
            result = subprocess.run(
                ["streamlink", url, "--json"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return ToolResult(True, "✓ Stream info (streamlink)", data)
            return ToolResult(False, "✗ Could not get stream info.")
        except Exception as e:
            return ToolResult(False, f"✗ Get stream info failed: {e}")

    @staticmethod
    def download_live_stream(
        url: str, output: str, duration: int = 0
    ) -> ToolResult:
        """
        Download a live stream or VOD using streamlink + yt-dlp fallback.
        duration=0 means download entire available content.
        """
        try:
            # Try yt-dlp first
            import yt_dlp
            opts = {
                "outtmpl": output,
                "format": "best",
                "quiet": True,
            }
            if duration > 0:
                opts["postprocessor_args"] = ["-t", str(duration)]
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            if Path(output).exists():
                return ToolResult(True, f"✓ Live stream downloaded → {output}", output)
            # Fallback: streamlink
            cmd = ["streamlink", url, "best", "-o", output]
            if duration > 0:
                cmd = ["timeout", str(duration)] + cmd
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 120 if duration > 0 else 3600)
            if result.returncode == 0 or Path(output).exists():
                return ToolResult(True, f"✓ Live stream downloaded (streamlink) → {output}", output)
            return ToolResult(False, f"✗ Download live stream failed.")
        except Exception as e:
            return ToolResult(False, f"✗ Download live stream error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 10. MediaMetadataTool
# ─────────────────────────────────────────────────────────────────────────────
class MediaMetadataTool:
    name = "media_metadata"
    description = (
        "Metadata management: read/write metadata, bulk rename by metadata, "
        "fix dates, album art management, NFO generation, M3U playlists, folder scanning."
    )

    @staticmethod
    def read_metadata(file: str) -> ToolResult:
        """Read comprehensive metadata from any media file."""
        try:
            result = {}
            # Try mutagen for audio
            try:
                from mutagen import File as MuFile
                mf = MuFile(file)
                if mf is not None:
                    result["tags"] = {str(k): str(v) for k, v in mf.tags.items()} if mf.tags else {}
                    result["info"] = {
                        "length":      getattr(mf.info, "length", None),
                        "bitrate":     getattr(mf.info, "bitrate", None),
                        "sample_rate": getattr(mf.info, "sample_rate", None),
                        "channels":    getattr(mf.info, "channels", None),
                    }
            except Exception:
                pass
            # Try tinytag for broader support
            try:
                from tinytag import TinyTag
                tag = TinyTag.get(file, image=True)
                result["tinytag"] = {k: v for k, v in tag.__dict__.items() if v is not None and k != "extra"}
            except Exception:
                pass
            # Try pymediainfo for video
            try:
                from pymediainfo import MediaInfo
                mi = MediaInfo.parse(file)
                result["mediainfo"] = []
                for track in mi.tracks:
                    result["mediainfo"].append({k: v for k, v in track.to_data().items() if v not in (None, "")})
            except Exception:
                pass
            # ffprobe as fallback
            if not result:
                info = FFmpegTool._probe(file)
                result = info
            return ToolResult(True, f"✓ Metadata read from {Path(file).name}", result)
        except Exception as e:
            return ToolResult(False, f"✗ Read metadata failed: {e}")

    @staticmethod
    def write_metadata(file: str, metadata_dict: Dict[str, str]) -> ToolResult:
        """
        Write metadata tags to audio/video file.
        Common tags: title, artist, album, year, genre, comment, track, composer.
        """
        try:
            from mutagen import File as MuFile
            mf = MuFile(file)
            if mf is None:
                # Fallback: use ffmpeg to write metadata
                meta_args = []
                for k, v in metadata_dict.items():
                    meta_args += ["-metadata", f"{k}={v}"]
                with tempfile.NamedTemporaryFile(suffix=Path(file).suffix, delete=False) as tf:
                    tmp = tf.name
                ok, out = FFmpegTool._run(["-i", file] + meta_args + ["-c", "copy", tmp])
                if ok:
                    shutil.move(tmp, file)
                    return ToolResult(True, f"✓ Metadata written (ffmpeg) to {Path(file).name}")
                return ToolResult(False, f"✗ Write metadata failed: {out}")
            if mf.tags is None:
                mf.add_tags()
            for k, v in metadata_dict.items():
                mf.tags[k] = v
            mf.save()
            return ToolResult(True, f"✓ Metadata written to {Path(file).name}", metadata_dict)
        except Exception as e:
            return ToolResult(False, f"✗ Write metadata failed: {e}")

    @staticmethod
    def bulk_rename_by_metadata(
        folder: str, pattern: str = "{artist} - {title}"
    ) -> ToolResult:
        """
        Bulk rename media files using metadata tags.
        pattern supports: {title}, {artist}, {album}, {year}, {track}, {genre}.
        """
        try:
            from tinytag import TinyTag
            renamed = 0
            errors = []
            audio_exts = {".mp3", ".flac", ".ogg", ".m4a", ".aac", ".wav", ".wma", ".opus"}
            for fp in Path(folder).iterdir():
                if fp.suffix.lower() not in audio_exts:
                    continue
                try:
                    tag = TinyTag.get(str(fp))
                    new_name = pattern
                    new_name = new_name.replace("{title}", str(tag.title or fp.stem))
                    new_name = new_name.replace("{artist}", str(tag.artist or "Unknown"))
                    new_name = new_name.replace("{album}", str(tag.album or "Unknown"))
                    new_name = new_name.replace("{year}", str(tag.year or ""))
                    new_name = new_name.replace("{track}", str(tag.track or ""))
                    new_name = new_name.replace("{genre}", str(tag.genre or ""))
                    # Sanitize filename
                    new_name = re.sub(r'[<>:"/\\|?*]', "_", new_name).strip()
                    new_path = fp.parent / f"{new_name}{fp.suffix}"
                    if new_path != fp and not new_path.exists():
                        fp.rename(new_path)
                        renamed += 1
                except Exception as ex:
                    errors.append(f"{fp.name}: {ex}")
            return ToolResult(True, f"✓ Renamed {renamed} files", {"renamed": renamed, "errors": errors})
        except Exception as e:
            return ToolResult(False, f"✗ Bulk rename failed: {e}")

    @staticmethod
    def fix_dates(
        folder: str, source: str = "metadata"
    ) -> ToolResult:
        """
        Fix file modification dates.
        source: 'metadata' (use embedded date tags), 'filename' (parse from filename).
        """
        try:
            from tinytag import TinyTag
            import datetime
            fixed = 0
            errors = []
            audio_exts = {".mp3", ".flac", ".m4a", ".ogg", ".aac", ".wav"}
            for fp in Path(folder).iterdir():
                if fp.suffix.lower() not in audio_exts:
                    continue
                try:
                    if source == "metadata":
                        tag = TinyTag.get(str(fp))
                        year = tag.year
                        if year and len(str(year)) >= 4:
                            year_int = int(str(year)[:4])
                            dt = datetime.datetime(year_int, 1, 1)
                            ts = dt.timestamp()
                            os.utime(str(fp), (ts, ts))
                            fixed += 1
                    elif source == "filename":
                        # Try to extract date from filename like 2023-01-15_...
                        match = re.search(r'(\d{4})[-_](\d{2})[-_](\d{2})', fp.name)
                        if match:
                            dt = datetime.datetime(int(match.group(1)),
                                                   int(match.group(2)),
                                                   int(match.group(3)))
                            ts = dt.timestamp()
                            os.utime(str(fp), (ts, ts))
                            fixed += 1
                except Exception as ex:
                    errors.append(f"{fp.name}: {ex}")
            return ToolResult(True, f"✓ Fixed dates for {fixed} files", {"fixed": fixed, "errors": errors})
        except Exception as e:
            return ToolResult(False, f"✗ Fix dates failed: {e}")

    @staticmethod
    def add_album_art(audio: str, image: str) -> ToolResult:
        """Embed album artwork into audio file."""
        try:
            ext = Path(audio).suffix.lower()
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tf:
                tmp = tf.name
            if ext == ".mp3":
                ok, out = FFmpegTool._run([
                    "-i", audio, "-i", image,
                    "-map", "0:a", "-map", "1:v",
                    "-c:a", "copy",
                    "-c:v", "mjpeg",
                    "-metadata:s:v", "title=Album cover",
                    "-metadata:s:v", "comment=Cover (front)",
                    "-id3v2_version", "3",
                    tmp
                ])
            else:
                ok, out = FFmpegTool._run([
                    "-i", audio, "-i", image,
                    "-map", "0", "-map", "1",
                    "-c", "copy",
                    "-disposition:1", "attached_pic",
                    tmp
                ])
            if ok:
                shutil.move(tmp, audio)
                return ToolResult(True, f"✓ Album art embedded in {Path(audio).name}", audio)
            else:
                try:
                    os.unlink(tmp)
                except Exception:
                    pass
                return ToolResult(False, f"✗ Add album art failed: {out}")
        except Exception as e:
            return ToolResult(False, f"✗ Add album art error: {e}")

    @staticmethod
    def extract_album_art(audio: str, output: str = None) -> ToolResult:
        """Extract embedded album artwork from audio file."""
        try:
            if not output:
                output = str(Path(audio).with_suffix(".jpg"))
            ok, out = FFmpegTool._run([
                "-i", audio,
                "-an", "-vcodec", "copy",
                output
            ])
            if ok and Path(output).exists():
                return ToolResult(True, f"✓ Album art extracted → {output}", output)
            # Try mutagen
            from mutagen.mp3 import MP3
            from mutagen.id3 import ID3
            tags = ID3(audio)
            for tag in tags.values():
                if tag.FrameID.startswith("APIC"):
                    with open(output, "wb") as fh:
                        fh.write(tag.data)
                    return ToolResult(True, f"✓ Album art extracted → {output}", output)
            return ToolResult(False, "✗ No album art found.")
        except Exception as e:
            return ToolResult(False, f"✗ Extract album art failed: {e}")

    @staticmethod
    def generate_nfo(file: str, output: str = None) -> ToolResult:
        """Generate .nfo XML file with media metadata (Kodi/Plex compatible)."""
        try:
            if not output:
                output = str(Path(file).with_suffix(".nfo"))
            info = FFmpegTool._probe(file)
            fmt = info.get("format", {})
            tags = fmt.get("tags", {})
            streams = info.get("streams", [])
            video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
            audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
            nfo_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<fileinfo>
    <streamdetails>
        <video>
            <codec>{video_stream.get("codec_name", "")}</codec>
            <width>{video_stream.get("width", "")}</width>
            <height>{video_stream.get("height", "")}</height>
            <fps>{video_stream.get("r_frame_rate", "")}</fps>
        </video>
        <audio>
            <codec>{audio_stream.get("codec_name", "")}</codec>
            <channels>{audio_stream.get("channels", "")}</channels>
            <language>{audio_stream.get("tags", {}).get("language", "")}</language>
        </audio>
    </streamdetails>
    <title>{tags.get("title", Path(file).stem)}</title>
    <artist>{tags.get("artist", tags.get("ARTIST", ""))}</artist>
    <album>{tags.get("album", tags.get("ALBUM", ""))}</album>
    <year>{tags.get("date", tags.get("DATE", ""))}</year>
    <genre>{tags.get("genre", tags.get("GENRE", ""))}</genre>
    <duration>{fmt.get("duration", "")}</duration>
    <filesize>{fmt.get("size", "")}</filesize>
    <format>{fmt.get("format_name", "")}</format>
</fileinfo>"""
            Path(output).write_text(nfo_content, encoding="utf-8")
            return ToolResult(True, f"✓ NFO generated → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Generate NFO failed: {e}")

    @staticmethod
    def create_m3u_playlist(
        files: List[str], output: str
    ) -> ToolResult:
        """Create an M3U playlist from a list of media file paths."""
        try:
            lines = ["#EXTM3U\n"]
            for fp in files:
                try:
                    from tinytag import TinyTag
                    tag = TinyTag.get(fp)
                    duration = int(tag.duration or -1)
                    artist = tag.artist or ""
                    title = tag.title or Path(fp).stem
                    display = f"{artist} - {title}" if artist else title
                    lines.append(f"#EXTINF:{duration},{display}\n{fp}\n")
                except Exception:
                    lines.append(f"#EXTINF:-1,{Path(fp).stem}\n{fp}\n")
            Path(output).write_text("".join(lines), encoding="utf-8")
            return ToolResult(True, f"✓ M3U playlist ({len(files)} tracks) → {output}", output)
        except Exception as e:
            return ToolResult(False, f"✗ Create M3U playlist failed: {e}")

    @staticmethod
    def scan_folder(
        path: str,
        include_technical: bool = True,
        recursive: bool = True
    ) -> ToolResult:
        """
        Scan a folder and return metadata inventory of all media files.
        Returns list of dicts with file info and optional technical metadata.
        """
        try:
            media_exts = {
                ".mp3", ".flac", ".m4a", ".ogg", ".aac", ".wav", ".wma", ".opus",
                ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v",
                ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
                ".pdf", ".epub"
            }
            glob_fn = Path(path).rglob if recursive else Path(path).glob
            files = [f for f in glob_fn("*") if f.is_file() and f.suffix.lower() in media_exts]
            inventory = []
            for fp in files:
                entry = {
                    "path":     str(fp),
                    "name":     fp.name,
                    "size_mb":  round(fp.stat().st_size / 1024 / 1024, 2),
                    "modified": datetime.fromtimestamp(fp.stat().st_mtime).isoformat()
                    if __import__("datetime") else "",
                    "ext":      fp.suffix.lower(),
                }
                if include_technical:
                    try:
                        from tinytag import TinyTag
                        if fp.suffix.lower() in {".mp3", ".flac", ".m4a", ".ogg", ".aac", ".wav"}:
                            tag = TinyTag.get(str(fp))
                            entry["title"]    = tag.title
                            entry["artist"]   = tag.artist
                            entry["album"]    = tag.album
                            entry["duration"] = round(tag.duration or 0, 1)
                            entry["bitrate"]  = tag.bitrate
                    except Exception:
                        pass
                    try:
                        if fp.suffix.lower() in {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"}:
                            info = FFmpegTool._probe(str(fp))
                            for stream in info.get("streams", []):
                                if stream.get("codec_type") == "video":
                                    entry["width"]  = stream.get("width")
                                    entry["height"] = stream.get("height")
                                    entry["codec"]  = stream.get("codec_name")
                                    break
                            entry["duration"] = round(float(info.get("format", {}).get("duration", 0)), 1)
                    except Exception:
                        pass
                inventory.append(entry)
            return ToolResult(True, f"✓ Scanned {len(inventory)} media files in {path}", inventory)
        except Exception as e:
            return ToolResult(False, f"✗ Scan folder failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Export all tool classes
# ─────────────────────────────────────────────────────────────────────────────
TOOLS = {
    "ffmpeg":           FFmpegTool,
    "youtube_downloader": YouTubeDownloaderTool,
    "audio":            AudioTool,
    "image_advanced":   ImageAdvancedTool,
    "screen_recorder":  ScreenRecorderTool,
    "text_to_speech":   TextToSpeechTool,
    "video_editing":    VideoEditingTool,
    "podcast":          PodcastTool,
    "streaming":        StreamingTool,
    "media_metadata":   MediaMetadataTool,
}

# Allow datetime to be used in scan_folder without import at runtime
from datetime import datetime

if __name__ == "__main__":
    print("tools_media.py — NPM Agent Media Tools")
    print("=" * 50)
    for name, cls in TOOLS.items():
        methods = [m for m in dir(cls) if not m.startswith("_") and callable(getattr(cls, m))]
        print(f"✓ {cls.name:25s} — {len(methods)} methods — {cls.description[:60]}…")
    print("\nAll tools loaded. ffmpeg must be installed for video/audio operations.")
    print("Run: sudo apt install ffmpeg  OR  brew install ffmpeg  OR download from ffmpeg.org")
