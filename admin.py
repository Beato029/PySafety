import os
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )

def install():
    app_name = "PySafety"
    program_files = os.environ.get("ProgramFiles")

    percorso = os.path.join(program_files, app_name)
    os.makedirs(percorso, exist_ok=True)

    print(f"✅ Cartella creata in: {percorso}")

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
        sys.exit()

    # SOLO qui sei admin
    install()