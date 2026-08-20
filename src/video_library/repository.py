"""CSV repository with atomic persistence."""

import csv
import os
import tempfile
from collections.abc import Iterable
from pathlib import Path

from .models import Video


class CsvVideoRepository:
    fieldnames = ("video_id", "name", "director", "rating", "play_count")

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> dict[str, Video]:
        if not self.path.exists():
            return {}
        videos: dict[str, Video] = {}
        with self.path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                video = Video(
                    video_id=row["video_id"],
                    name=row["name"],
                    director=row["director"],
                    rating=int(row["rating"]),
                    play_count=int(row["play_count"]),
                )
                if video.video_id in videos:
                    raise ValueError(f"Duplicate video ID: {video.video_id}")
                videos[video.video_id] = video
        return videos

    def save(self, videos: Iterable[Video]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(dir=self.path.parent, text=True)
        try:
            with os.fdopen(descriptor, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=self.fieldnames)
                writer.writeheader()
                for video in videos:
                    writer.writerow(
                        {
                            "video_id": video.video_id,
                            "name": video.name,
                            "director": video.director,
                            "rating": video.rating,
                            "play_count": video.play_count,
                        }
                    )
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, self.path)
        except BaseException:
            Path(temporary_name).unlink(missing_ok=True)
            raise
