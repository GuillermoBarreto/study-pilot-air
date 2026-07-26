"""Desktop entry point for the packaged Study Pilot Air application."""

import threading
import webbrowser

import uvicorn


HOST = "127.0.0.1"
PORT = 8765


def open_dashboard() -> None:
    webbrowser.open(f"http://{HOST}:{PORT}")


def main() -> None:
    threading.Timer(0.75, open_dashboard).start()
    uvicorn.run("app.main:app", host=HOST, port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
