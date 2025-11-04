import sys, os, platform

# Print Python version
print(sys.version)

# Print Python version using platform module
print(platform.python_version())
print(sys.executable)

# Print if running in a virtual environment
print("venv:", getattr(sys, "real_prefix", None) or (sys.prefix != getattr(sys, "base_prefix", sys.prefix))) 
print("VIRTUAL_ENV:", os.environ.get("VIRTUAL_ENV"))