from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = APP_DIR / "data"
YAMLS_DIR = DATA_DIR / "yamls"
SCRIPTS_DIR = DATA_DIR / "scripts"
IMAGES_DIR = DATA_DIR / "images"
SESSIONS_DIR = DATA_DIR / "sessions"


def ensure_dirs():
    for d in (DATA_DIR, YAMLS_DIR, SCRIPTS_DIR, IMAGES_DIR, SESSIONS_DIR):
        d.mkdir(parents=True, exist_ok=True)