import sys, site, subprocess

print("Python:", sys.version)
print("Executable:", sys.executable)
print("Base Prefix (venv root):", sys.base_prefix)
print("Site-packages:", site.getsitepackages())

# check pip inside this venv
subprocess.run([sys.executable, "-m", "pip", "--version"])
