import os
import subprocess
from pathlib import Path

import typer

app = typer.Typer()

def ensure_env(name: str, default: str):

    if name not in os.environ:
        os.environ[name] = default

def ensure_env_file(path: Path, values: dict[str, str]):

    existing = {}

    if path.exists():

        for line in path.read_text().splitlines():

            if "=" in line:
                key, value = line.split("=", 1)
                existing[key] = value

    updated = False

    for key, value in values.items():

        if key not in existing:
            existing[key] = value
            updated = True

    if updated or not path.exists():
        content = "\n".join(
            f"{k}={v}"
            for k, v in existing.items()
        )

        path.write_text(content)

def setup_environment():
    # Backend
    ensure_env("APP_HOST", "0.0.0.0")
    ensure_env("APP_PORT", "8000")
    ensure_env("APP_LOGGING_DEBUG", "true")

    # Frontend
    ensure_env_file(
        Path("client/.env"),
        {
            "VITE_S3_BROWSER_URL": "http://127.0.0.1:8000"
        }
    )

    # Database
    ensure_env(
        "DB_STORAGE_PATH",
        "./storage"
    )


@app.command()
def run(dev: bool = True):
    setup_environment()

    host = os.environ["APP_HOST"]
    port = os.environ["APP_PORT"]

    if dev:
        subprocess.Popen(
            f"uv run uvicorn browser.run:app --reload --host {host} --port {port}",
            cwd="server/src",
            shell=True
        )

        frontend_env = os.environ.copy()

        frontend_env["VITE_API_URL"] = (
            f"http://{os.environ['APP_HOST']}:{os.environ['APP_PORT']}"
        )

        subprocess.run(
            "npm run dev",
            cwd="client",
            shell=True,
            env=frontend_env
        )
@app.command()
def hello(name: str):
    print(f"Hello {name}")

if __name__ == "__main__":
    app()