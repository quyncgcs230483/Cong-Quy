import csv
import random
from pathlib import Path

import pytest

from video_library import CsvVideoRepository, Video, VideoLibrary


@pytest.fixture
def library(tmp_path: Path) -> VideoLibrary:
    return VideoLibrary(CsvVideoRepository(tmp_path / "videos.csv"))


def test_video_validates_required_fields_and_rating() -> None:
    with pytest.raises(ValueError, match="required"):
        Video("01", "", "Director", 3)
    with pytest.raises(ValueError, match="between 1 and 5"):
        Video("01", "Film", "Director", 6)


def test_video_formats_complete_summary() -> None:
    video = Video("01", "Film", "Director", 3, 2)
    assert video.stars == "★★★☆☆"
    assert video.summary == "01: Film — Director ★★★☆☆ (2 plays)"


def test_add_assigns_stable_ids_and_persists(library: VideoLibrary) -> None:
    first = library.add("First", "Director A", 4)
    second = library.add("Second", "Director B", 5)
    reloaded = VideoLibrary(library.repository)

    assert (first.video_id, second.video_id) == ("01", "02")
    assert [video.name for video in reloaded.list_videos()] == ["First", "Second"]


def test_deleted_ids_are_not_reused(library: VideoLibrary) -> None:
    library.add("First", "Director", 3)
    library.add("Second", "Director", 3)
    library.delete("01")
    assert library.add("Third", "Director", 3).video_id == "03"


def test_update_rating_validates_and_persists(library: VideoLibrary) -> None:
    video = library.add("Film", "Director", 2)
    library.update_rating(video.video_id, 5)
    assert VideoLibrary(library.repository).get(video.video_id).rating == 5
    with pytest.raises(ValueError):
        library.update_rating(video.video_id, 0)


def test_play_is_transactional_for_missing_video(library: VideoLibrary) -> None:
    video = library.add("Film", "Director", 3)
    with pytest.raises(KeyError):
        library.play([video.video_id, "99"])
    assert video.play_count == 0


def test_play_increments_every_playlist_occurrence(library: VideoLibrary) -> None:
    video = library.add("Film", "Director", 3)
    library.play([video.video_id, video.video_id])
    assert video.play_count == 2
    assert VideoLibrary(library.repository).get(video.video_id).play_count == 2


def test_random_video_is_deterministic_with_injected_generator(library: VideoLibrary) -> None:
    library.add("First", "Director", 3)
    library.add("Second", "Director", 3)
    assert library.random_video(random.Random(1)).video_id == "01"


def test_empty_random_library_raises(library: VideoLibrary) -> None:
    with pytest.raises(LookupError, match="empty"):
        library.random_video()


def test_repository_rejects_duplicate_ids(tmp_path: Path) -> None:
    path = tmp_path / "videos.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(CsvVideoRepository.fieldnames)
        writer.writerow(["01", "First", "Director", 3, 0])
        writer.writerow(["01", "Duplicate", "Director", 3, 0])
    with pytest.raises(ValueError, match="Duplicate"):
        CsvVideoRepository(path).load()
