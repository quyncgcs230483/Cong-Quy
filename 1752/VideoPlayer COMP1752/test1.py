import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk
import csv
import webbrowser

# VideoLibrary class definition
class VideoLibrary:
    def __init__(self):
        self.library = {}
        self.load_from_csv()

    def add_video(self, name, director, rating):
        video_id = str(len(self.library) + 1)
        self.library[video_id] = {'name': name, 'director': director, 'rating': rating, 'play_count': 0}
        self.save_to_csv()
        return video_id

    def get_name(self, video_id):
        return self.library.get(video_id, {}).get('name')

    def get_director(self, video_id):
        return self.library.get(video_id, {}).get('director')

    def get_rating(self, video_id):
        return self.library.get(video_id, {}).get('rating')

    def get_play_count(self, video_id):
        return self.library.get(video_id, {}).get('play_count')

    def set_rating(self, video_id, new_rating):
        if video_id in self.library:
            self.library[video_id]['rating'] = new_rating
            self.save_to_csv()

    def increment_play_count(self, video_id):
        if video_id in self.library:
            self.library[video_id]['play_count'] += 1
            self.save_to_csv()

    def delete_video(self, video_id):
        if video_id in self.library:
            del self.library[video_id]
            self.save_to_csv()

    def list_all(self):
        return "\n".join([f"ID: {key}, Name: {val['name']}, Director: {val['director']}, Rating: {val['rating']}, Plays: {val['play_count']}"
                          for key, val in self.library.items()])

    def save_to_csv(self):
        with open('video_library.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Director', 'Rating', 'Play Count'])
            for key, val in self.library.items():
                writer.writerow([key, val['name'], val['director'], val['rating'], val['play_count']])

    def load_from_csv(self):
        try:
            with open('video_library.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                self.library = {}
                for row in reader:
                    video_id, name, director, rating, play_count = row
                    self.library[video_id] = {
                        'name': name,
                        'director': director,
                        'rating': int(rating),
                        'play_count': int(play_count)
                    }
        except FileNotFoundError:
            self.library = {}

lib = VideoLibrary()  # Create an instance of VideoLibrary

# Function to set the text in a given text area widget
def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)

# CheckVideos class
class CheckVideos(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=10, pady=10)
        list_videos_btn = tk.Button(self, text="List All Videos", command=self.list_videos_clicked)
        list_videos_btn.grid(row=0, column=0, padx=10, pady=10)
        enter_lbl = tk.Label(self, text="Enter Video Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)
        self.input_txt = tk.Entry(self, width=3)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)
        check_video_btn = tk.Button(self, text="Check Video", command=self.check_video_clicked)
        check_video_btn.grid(row=0, column=3, padx=10, pady=10)
        delete_video_btn = tk.Button(self, text="Delete Video", command=self.delete_video_clicked)
        delete_video_btn.grid(row=0, column=4, padx=10, pady=10)
        play_video_btn = tk.Button(self, text="Play Video", command=self.play_video_clicked)
        play_video_btn.grid(row=0, column=5, padx=10, pady=10)
        
        self.list_box = tk.Listbox(self, width=48, height=12)
        self.list_box.grid(row=1, column=0, columnspan=4, sticky="W", padx=10, pady=10)
        
        self.video_txt = tk.Text(self, width=24, height=4, wrap="none")
        self.video_txt.grid(row=1, column=4, columnspan=2, sticky="NW", padx=10, pady=10)
        
        self.status_lbl = tk.Label(self, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=6, sticky="W", padx=10, pady=10)
        
        self.list_videos_clicked()

    def check_video_clicked(self):
        key = self.input_txt.get()
        name = lib.get_name(key)
        if name is not None:
            director = lib.get_director(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            video_details = f"{name}\n{director}\nRating: {rating}\nPlays: {play_count}"
            set_text(self.video_txt, video_details)
            self.status_lbl.configure(text="Video details displayed", fg="green")
        else:
            set_text(self.video_txt, f"Video {key} not found")
            self.status_lbl.configure(text="Video not found", fg="red")

    def list_videos_clicked(self):
        video_list = lib.list_all().split('\n')
        self.list_box.delete(0, tk.END)
        for video in video_list:
            self.list_box.insert(tk.END, video)
        self.status_lbl.configure(text="All videos listed", fg="green")

    def delete_video_clicked(self):
        key = self.input_txt.get()
        name = lib.get_name(key)
        if name is not None:
            lib.delete_video(key)
            self.list_videos_clicked()  # Refresh the video list
            self.status_lbl.configure(text=f"Video {key} deleted", fg="green")
        else:
            self.status_lbl.configure(text="Video not found", fg="red")

    def play_video_clicked(self):
        key = self.input_txt.get()
        name = lib.get_name(key)
        if name is not None:
            search_query = f"https://www.youtube.com/results?search_query={name.replace(' ', '+')}"
            webbrowser.open(search_query)
            self.status_lbl.configure(text=f"Playing {name} on YouTube", fg="green")
        else:
            self.status_lbl.configure(text="Video not found", fg="red")

# UpdateVideos class
class UpdateVideos(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=10, pady=10)
        enter_lbl = tk.Label(self, text="Enter Video Number")
        enter_lbl.grid(row=0, column=0, padx=10, pady=10)
        self.input_txt = tk.Entry(self, width=3)
        self.input_txt.grid(row=0, column=1, padx=10, pady=10)
        check_video_btn = tk.Button(self, text="Check Video", command=self.check_video_clicked)
        check_video_btn.grid(row=0, column=2, padx=10, pady=10)
        rating_lbl = tk.Label(self, text="Set New Rating")
        rating_lbl.grid(row=1, column=0, padx=10, pady=10)
        self.rating_txt = tk.Entry(self, width=3)
        self.rating_txt.grid(row=1, column=1, padx=10, pady=10)
        set_rating_btn = tk.Button(self, text="Set Rating", command=self.set_rating_clicked)
        set_rating_btn.grid(row=1, column=2, padx=10, pady=10)
        self.video_txt = tk.Text(self, width=24, height=4, wrap="none")
        self.video_txt.grid(row=2, column=0, columnspan=3, sticky="NW", padx=10, pady=10)
        self.status_lbl = tk.Label(self, text="", font=("Helvetica", 10), fg="green")
        self.status_lbl.grid(row=3, column=0, columnspan=3, sticky="W", padx=10, pady=10)

    def check_video_clicked(self):
        key = self.input_txt.get()
        name = lib.get_name(key)
        if name is not None:
            director = lib.get_director(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            video_details = f"{name}\n{director}\nRating: {rating}\nPlays: {play_count}"
            set_text(self.video_txt, video_details)
            self.status_lbl.configure(text="Video details displayed")
        else:
            set_text(self.video_txt, f"Video {key} not found")
            self.status_lbl.configure(text="Video not found")

    def set_rating_clicked(self):
        key = self.input_txt.get()
        new_rating = self.rating_txt.get()
        if new_rating.isdigit():
            new_rating = int(new_rating)
            if 1 <= new_rating <= 10:
                lib.set_rating(key, new_rating)
                self.status_lbl.configure(text="Rating updated", fg="green")
            else:
                self.status_lbl.configure(text="Rating must be between 1 and 10", fg="red")
        else:
            self.status_lbl.configure(text="Invalid rating", fg="red")

# CreateVideo class
class CreateVideo(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=10, pady=10)
        name_lbl = tk.Label(self, text="Video Name")
        name_lbl.grid(row=0, column=0, padx=10, pady=10)
        self.name_txt = tk.Entry(self, width=30)
        self.name_txt.grid(row=0, column=1, padx=10, pady=10)
        director_lbl = tk.Label(self, text="Director")
        director_lbl.grid(row=1, column=0, padx=10, pady=10)
        self.director_txt = tk.Entry(self, width=30)
        self.director_txt.grid(row=1, column=1, padx=10, pady=10)
        rating_lbl = tk.Label(self, text="Rating (1-10)")
        rating_lbl.grid(row=2, column=0, padx=10, pady=10)
        self.rating_txt = tk.Entry(self, width=3)
        self.rating_txt.grid(row=2, column=1, padx=10, pady=10)
        create_btn = tk.Button(self, text="Add Video", command=self.add_video_clicked)
        create_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.status_lbl = tk.Label(self, text="", font=("Helvetica", 10), fg="green")
        self.status_lbl.grid(row=4, column=0, columnspan=2, sticky="W", padx=10, pady=10)

    def add_video_clicked(self):
        name = self.name_txt.get()
        director = self.director_txt.get()
        rating = self.rating_txt.get()
        if name and director and rating.isdigit():
            rating = int(rating)
            if 1 <= rating <= 10:
                video_id = lib.add_video(name, director, rating)
                self.status_lbl.configure(text=f"Video added with ID {video_id}")
            else:
                self.status_lbl.configure(text="Rating must be between 1 and 10", fg="red")
        else:
            self.status_lbl.configure(text="Please fill out all fields", fg="red")

# Main application setup
class VideoLibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Library Management System")
        self.geometry("800x600")

        # Create tabs
        self.tab_control = ttk.Notebook(self)
        self.check_videos_tab = CheckVideos(self.tab_control)
        self.update_videos_tab = UpdateVideos(self.tab_control)
        self.create_video_tab = CreateVideo(self.tab_control)

        self.tab_control.add(self.check_videos_tab, text="Check Videos")
        self.tab_control.add(self.update_videos_tab, text="Update Videos")
        self.tab_control.add(self.create_video_tab, text="Create Video")

        self.tab_control.pack(expand=1, fill="both")

if __name__ == "__main__":
    app = VideoLibraryApp()
    app.mainloop()