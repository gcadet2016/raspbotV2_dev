"""
Environment detection helpers for Raspberry Pi vs WSL and general OS.

Usage:
    from tools.env_detect import is_raspberry_pi, is_wsl, get_runtime_env
    if is_raspberry_pi():
        ... # Pi-specific code
    elif is_wsl():
        ... # WSL-specific code

This avoids relying on optional packages (e.g., RPi.GPIO) and uses
kernel/device-tree hints that are robust across Pi models and WSL versions.
"""

from __future__ import annotations

import os
import platform
from pathlib import Path


def _read_text(path: str) -> str:
    try:
        return Path(path).read_text(errors="ignore")
    except Exception:
        return ""


def is_wsl() -> bool:
    """Return True if running under Windows Subsystem for Linux (WSL)."""
    # Environment variables set by WSL
    if os.environ.get("WSL_DISTRO_NAME") or os.environ.get("WSL_INTEROP"):
        return True

    # Kernel strings containing 'microsoft' or 'wsl'
    osrelease = _read_text("/proc/sys/kernel/osrelease")
    version = _read_text("/proc/version")
    data = f"{osrelease} {version}".lower()
    return ("microsoft" in data) or ("wsl" in data)


def is_raspberry_pi() -> bool:
    """Return True if running on a Raspberry Pi device.

    Checks the device-tree model first (most reliable), then /proc/cpuinfo,
    and finally uses architecture + hostname as a weak hint.
    """
    # Device-tree model path varies across kernels
    for p in ("/proc/device-tree/model", 
              "/sys/firmware/devicetree/base/model"):
        model = _read_text(p).strip().lower()
        if "raspberry pi" in model:
            return True

    # Fallback: look for 'Raspberry Pi' in cpuinfo
    cpuinfo = _read_text("/proc/cpuinfo").lower()
    if "raspberry pi" in cpuinfo:
        return True

    # Very weak hints (avoid false positives): ARM + hostname containing 'rasp'
    machine = platform.machine().lower()
    if machine in ("armv6l", "armv7l", "aarch64"):
        try:
            node = platform.uname().node.lower()
        except Exception:
            node = ""
        if "rasp" in node:
            return True

    return False


def is_linux() -> bool:
    return platform.system().lower() == "linux" and not is_wsl()


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def is_macos() -> bool:
    return platform.system().lower() == "darwin"


def get_runtime_env() -> str:
    """Return a short label for the runtime environment.

    Possible values: 'raspberry_pi', 'wsl', 'linux', 'macos', 'windows', or a
    fallback of platform.system().lower().
    """
    if is_raspberry_pi():
        return "raspberry_pi"
    if is_wsl():
        return "wsl"
    if is_linux():
        return "linux"
    if is_macos():
        return "macos"
    if is_windows():
        return "windows"
    return platform.system().lower()


if __name__ == "__main__":
    print("env:", get_runtime_env())
    print("is_raspberry_pi:", is_raspberry_pi())
    print("is_wsl:", is_wsl())
    print("system:", platform.system())
    print("machine:", platform.machine())
