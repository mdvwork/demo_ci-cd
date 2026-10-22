"""Подготовка статического сайта к выпуску без сторонних зависимостей."""
import json
import os
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
destination = root / "dist"
if destination.exists():
    shutil.rmtree(destination)
shutil.copytree(root / "site", destination)
commit = os.environ.get("GITHUB_SHA", "local")
(destination / "release.json").write_text(
    json.dumps({"source_commit": commit}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(f"Build ready: dist; source_commit={commit}")
