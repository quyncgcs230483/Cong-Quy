import csv

# Initialize your library dictionary (this should be loaded from the CSV initially)
library = {}

# Function to load the video library from a CSV file
def load_library_from_csv(file_path):
    global library
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            library[row['key']] = {
                'name': row['name'],
                'director': row['director'],
                'rating': int(row['rating']),
                'play_count': int(row['play_count'])
            }

# Function to save a video to the CSV file
def save_video_to_csv(file_path, key, name, director, rating):
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([key, name, director, rating, 0])  # play_count starts at 0

# Add a video to the library and save it to the CSV
def add_video(name, director, rating, csv_file='video_library.csv'):
    new_key = str(len(library) + 1)
    library[new_key] = {"name": name, "director": director, "rating": rating, "play_count": 0}
    save_video_to_csv(csv_file, new_key, name, director, rating)
    return new_key

# Function to list all videos (for reference in your script)
def list_all():
    return "\n".join([f"{key}: {video['name']} by {video['director']}" for key, video in library.items()])

# Other utility functions (get_name, get_director, etc.) remain the same...

from library_item import LibraryItem


library = {}
library["01"] = LibraryItem("Tom and Jerry", "Fred Quimby", 4)
library["02"] = LibraryItem("Breakfast at Tiffany's", "Blake Edwards", 5)
library["03"] = LibraryItem("Casablanca", "Michael Curtiz", 2)
library["04"] = LibraryItem("The Sound of Music", "Robert Wise", 1)
library["05"] = LibraryItem("Gone with the Wind", "Victor Fleming", 3)

def add_video(name, director, rating):
    new_key = str(len(library) + 1)
    library[new_key] = {"name": name, "director": director, "rating": rating, "play_count": 0}
    return new_key

def list_all():
    output = ""
    for key in library:
        item = library[key]
        output += f"{key} {item.info()}\n"
    return output


def get_name(key):
    try:
        item = library[key]
        return item.name
    except KeyError:
        return None


def get_director(key):
    try:
        item = library[key]
        return item.director
    except KeyError:
        return None


def get_rating(key):
    try:
        item = library[key]
        return item.rating
    except KeyError:
        return -1

def set_rating(key, rating):
    try:
        item = library[key]
        item.rating = rating
    except KeyError:
        return


def get_play_count(key):
    try:
        item = library[key]
        return item.play_count
    except KeyError:
        return -1

def increment_play_count(key):
    try:
        item = library[key]
        item.play_count += 1
    except KeyError:
        return



