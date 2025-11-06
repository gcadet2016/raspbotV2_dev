
import cv2
import sys, os, platform

from appLib import env_detect as e

# ----- Print environment information -----
print("Environment:", e.get_runtime_env())
print("Is environment WSL:", e.is_wsl())
print("Is environment Raspberry Pi:", e.is_raspberry_pi())
print()

# ----- Print Python version -----
print("Python version:", sys.version)

# Print Python version using platform module
print("Platform Python version:", platform.python_version())
print("Python executable:", sys.executable)

# Print if running in a virtual environment
print("venv:", getattr(sys, "real_prefix", None) or (sys.prefix != getattr(sys, "base_prefix", sys.prefix))) 
print("VIRTUAL_ENV:", os.environ.get("VIRTUAL_ENV"))
print()

# ----- Print OpenCV version -----
print("OpenCV version:", cv2.__version__)

# ----- Print Picamera2 version if available -----
if e.is_raspberry_pi():
    try:
        from picamera2 import Picamera2
        print("Picamera2 version: " + Picamera2.__version__)
    except ImportError:
        print("WARNING: Picamera2 is not installed in this Raspberry Pi environment.")

# ----- Next test here -----