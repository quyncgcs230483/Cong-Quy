"""Validated video domain model."""

from dataclasses import dataclass


@dataclass(slots=True)
class Video:
    video_id: str
    name: str
    director: str
    rating: int
    play_count: int = 0

    def __post_init__(self) -> None:
        self.video_id = self.video_id.strip()
        self.name = self.name.strip()
        self.director = self.director.strip()
        if not self.video_id or not self.name or not self.director:
            raise ValueError("Video ID, name, and director are required")
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        if self.play_count < 0:
            raise ValueError("Play count cannot be negative")

    @property
    def stars(self) -> str:
        return "★" * self.rating + "☆" * (5 - self.rating)

    @property
    def summary(self) -> str:
        return (
            f"{self.video_id}: {self.name} — {self.director} {self.stars} ({self.play_count} plays)"
        )
