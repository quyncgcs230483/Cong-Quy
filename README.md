# Video Library — Python Coursework

Small desktop application for maintaining a video collection and playlist. Scope stays intentionally focused while code demonstrates clean separation between domain validation, business operations, durable storage, and Tkinter UI.

## Features

- Add, inspect, rate, delete, and persist videos
- Build playlists manually or with deterministic random selection
- Track play counts, including repeated playlist entries
- Store data in human-readable CSV using atomic file replacement
- Validate ratings, required metadata, duplicate identifiers, and missing records
- Run as installed command or Python module

## Architecture

```text
models.py       validated Video dataclass
repository.py   UTF-8 CSV loading and atomic writes
service.py      CRUD, rating, playlist, and play-count rules
gui.py          Tkinter adapter with no persistence logic
tests/          isolated service/repository tests using temporary files
```

## Run

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
cp data/videos.csv video_library.csv
video-library
```

Set `VIDEO_LIBRARY_PATH` to choose another CSV file.

## Verify

```bash
ruff format --check .
ruff check .
mypy
pytest
```

GitHub Actions runs same formatter, lint, strict type, and test gates on every push and pull request.
