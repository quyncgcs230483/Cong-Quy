import pytest
from video_library import LibraryItem

def test_initialization_of_library_item():
    item = LibraryItem("Sample Film", "Sample Director", 3)
    assert item.name == "Sample Film"
    assert item.director == "Sample Director"
    assert item.rating == 3
    assert item.play_count == 0

def test_library_item_information():
    item = LibraryItem("Sample Film", "Sample Director", 4)
    assert item.info() == "Sample Film - Sample Director ****"

def test_star_representation():
    item = LibraryItem("Sample Film", "Sample Director", 2)
    assert item.stars() == "**"

def test_play_count_increment():
    item = LibraryItem("Sample Film", "Sample Director", 2)
    assert item.play_count == 0
    item.play_count += 1
    assert item.play_count == 1