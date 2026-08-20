"""Video library business operations."""

import random
from collections.abc import Sequence

from .models import Video
from .repository import CsvVideoRepository


class VideoLibrary:
    def __init__(self, repository: CsvVideoRepository) -> None:
        self.repository = repository
        self._videos = repository.load()

    def list_videos(self) -> tuple[Video, ...]:
        return tuple(sorted(self._videos.values(), key=lambda video: video.video_id))

    def get(self, video_id: str) -> Video:
        try:
            return self._videos[video_id.strip()]
        except KeyError as error:
            raise KeyError(f"Video {video_id!r} not found") from error

    def add(self, name: str, director: str, rating: int) -> Video:
        numeric_ids = [int(key) for key in self._videos if key.isdigit()]
        video_id = f"{max(numeric_ids, default=0) + 1:02d}"
        video = Video(video_id, name, director, rating)
        self._videos[video_id] = video
        self._persist()
        return video

    def update_rating(self, video_id: str, rating: int) -> Video:
        video = self.get(video_id)
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        video.rating = rating
        self._persist()
        return video

    def delete(self, video_id: str) -> Video:
        video = self.get(video_id)
        del self._videos[video.video_id]
        self._persist()
        return video

    def play(self, video_ids: Sequence[str]) -> tuple[Video, ...]:
        videos = tuple(self.get(video_id) for video_id in video_ids)
        for video in videos:
            video.play_count += 1
        self._persist()
        return videos

    def random_video(self, generator: random.Random | None = None) -> Video:
        if not self._videos:
            raise LookupError("Video library is empty")
        return (generator or random).choice(list(self._videos.values()))

    def _persist(self) -> None:
        self.repository.save(self.list_videos())
