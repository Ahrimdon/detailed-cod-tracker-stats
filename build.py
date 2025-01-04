import os
import shutil
import subprocess
import PyInstaller.__main__

# Constants for your project
SCRIPT = "get_cod_stats.py"
ICON = "assets/icon.ico"
NAME = "get_cod_stats"
DIST_PATH = "bin"

# Path to the 'frequencies.json' file within the charset_normalizer package
charset_normalizer_data = os.path.join('deps', 'frequencies.json')

# Activate the virtual environment
venv_activation_script = os.path.join(os.getcwd(), 'venv', 'Scripts', 'activate')
subprocess.call(venv_activation_script, shell=True)

# Run PyInstaller
PyInstaller.__main__.run([
    SCRIPT,
    '--name', NAME,
    '--noconfirm',
    '--onefile',
    '--console',
    '--icon', ICON,
    '--distpath', DIST_PATH,
    '--add-data', f"{charset_normalizer_data};charset_normalizer/assets"
])

# Clean up the build directory and spec file
shutil.rmtree('build', ignore_errors=True)
os.remove('get_cod_stats.spec')

# Optional: Pause at the end (like the 'pause' in batch script)
input("Press Enter to continue...")
