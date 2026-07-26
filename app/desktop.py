"""Desktop entry point for the packaged Study Pilot Air application."""

import os
import sys
import threading
import time
from urllib.request import urlopen
import webbrowser

# A windowless PyInstaller app has no stdout/stderr. Uvicorn configures logging
# during startup, so provide harmless streams before importing it.
if getattr(sys, "frozen", False):
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")

import uvicorn
from app.main import app


HOST = "127.0.0.1"
PORT = 8765


def open_dashboard_when_ready() -> None:
    """Open the browser only after the bundled local server can answer."""
    url = f"http://{HOST}:{PORT}/health"
    for _ in range(120):
        try:
            with urlopen(url, timeout=1):
                webbrowser.open(f"http://{HOST}:{PORT}")
                return
        except OSError:
            time.sleep(0.5)


def main() -> None:
    threading.Thread(target=open_dashboard_when_ready, daemon=True).start()
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
