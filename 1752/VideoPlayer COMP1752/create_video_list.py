import tkinter as tk
import tkinter.scrolledtext as tkst
import random
import video_library as lib
import font_manager as fonts

class CreateVideoList():
    def __init__(self, window):
        self.playlist = []
        window.geometry("1000x350")
        window.title("Create Video List")
        add_video_btn = tk.Button(window, text="Add Video to Playlist", command=self.add_video_clicked)
        add_video_btn.grid(row=0, column=2, padx=10, pady=10)
        add_random_video_btn = tk.Button(window, text="Add Random Video", command=self.add_random_video_clicked)
        add_random_video_btn.grid(row=0, column=3, padx=10, pady=10)
        play_videos_btn = tk.Button(window, text="Play Playlist", command=self.play_playlist_clicked)
        play_videos_btn.grid(row=0, column=4, padx=10, pady=10)
        reset_playlist_btn = tk.Button(window, text="Reset Playlist", command=self.reset_playlist_clicked)
        reset_playlist_btn.grid(row=0, column=5, padx=10, pady=10)
        enter_lbl = tk.Label(window, text="Enter Video Number")
        enter_lbl.grid(row=0, column=0, padx=10, pady=10)
        self.input_txt = tk.Entry(window, width=3)
        self.input_txt.grid(row=0, column=1, padx=10, pady=10)
        self.playlist_txt = tkst.ScrolledText(window, width=58, height=12, wrap="none")
        self.playlist_txt.grid(row=1, column=0, columnspan=6, sticky="W", padx=10, pady=10)
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=6, sticky="W", padx=10, pady=10)

    def add_video_clicked(self):
        key = self.input_txt.get()
        name = lib.get_name(key)
        if name is not None:
            self.playlist.append(key)
            self.update_playlist_display()
            self.status_lbl.configure(text=f"Video {key} added to playlist")
        else:
            self.status_lbl.configure(text=f"Video {key} not found")
    def add_random_video_clicked(self):
        keys = list(lib.library.keys())
        random_key = random.choice(keys)
        self.playlist.append(random_key)
        self.update_playlist_display()
        self.status_lbl.configure(text=f"Random video {random_key} added to playlist")
    def play_playlist_clicked(self):
        for key in self.playlist:
            lib.increment_play_count(key)
        self.status_lbl.configure(text="Playlist played. Play counts updated.")
    def reset_playlist_clicked(self):
        self.playlist = []
        self.update_playlist_display()
        self.status_lbl.configure(text="Playlist reset.")
    def update_playlist_display(self):
        content = "\n".join([lib.get_name(key) for key in self.playlist])
        self.playlist_txt.delete("1.0", tk.END)
        self.playlist_txt.insert("1.0", content)

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    CreateVideoList(window)
    window.mainloop()