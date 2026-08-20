"""Tkinter adapter for video library services."""

import os
import tkinter as tk
from collections.abc import Callable
from pathlib import Path
from tkinter import messagebox, ttk
from typing import cast

from .repository import CsvVideoRepository
from .service import VideoLibrary


class VideoLibraryApp(tk.Tk):
    def __init__(self, library: VideoLibrary) -> None:
        super().__init__()
        self.library = library
        self.playlist: list[str] = []
        self.title("Video Library")
        self.geometry("920x560")
        self.minsize(760, 480)
        self._build()
        self.refresh()

    def _build(self) -> None:
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        ttk.Label(self, text="Video Library", font=("Helvetica", 24, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=18, pady=(18, 8)
        )

        library_frame = ttk.LabelFrame(self, text="Collection", padding=12)
        library_frame.grid(row=1, column=0, sticky="nsew", padx=(18, 8), pady=8)
        library_frame.columnconfigure(0, weight=1)
        library_frame.rowconfigure(0, weight=1)
        self.video_list = tk.Listbox(library_frame, font=("Helvetica", 12))
        self.video_list.grid(row=0, column=0, columnspan=3, sticky="nsew")
        ttk.Button(library_frame, text="Add to playlist", command=self.add_selected).grid(
            row=1, column=0, sticky="ew", pady=(10, 0)
        )
        ttk.Button(library_frame, text="Delete", command=self.delete_selected).grid(
            row=1, column=1, sticky="ew", padx=8, pady=(10, 0)
        )
        ttk.Button(library_frame, text="Random", command=self.add_random).grid(
            row=1, column=2, sticky="ew", pady=(10, 0)
        )

        editor = ttk.LabelFrame(self, text="Add or update", padding=12)
        editor.grid(row=1, column=1, sticky="nsew", padx=(8, 18), pady=8)
        self.video_id = tk.StringVar()
        self.name = tk.StringVar()
        self.director = tk.StringVar()
        self.rating = tk.StringVar(value="3")
        for row, (label, variable) in enumerate(
            (
                ("Video ID", self.video_id),
                ("Name", self.name),
                ("Director", self.director),
                ("Rating 1–5", self.rating),
            )
        ):
            ttk.Label(editor, text=label).grid(row=row * 2, column=0, sticky="w")
            ttk.Entry(editor, textvariable=variable).grid(
                row=row * 2 + 1, column=0, sticky="ew", pady=(0, 8)
            )
        editor.columnconfigure(0, weight=1)
        ttk.Button(editor, text="Add video", command=self.add_video).grid(
            row=8, column=0, sticky="ew"
        )
        ttk.Button(editor, text="Update rating", command=self.update_rating).grid(
            row=9, column=0, sticky="ew", pady=(8, 0)
        )

        playlist_frame = ttk.LabelFrame(self, text="Playlist", padding=12)
        playlist_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=18, pady=(8, 18))
        playlist_frame.columnconfigure(0, weight=1)
        self.playlist_text = ttk.Label(playlist_frame, text="Playlist is empty")
        self.playlist_text.grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Button(playlist_frame, text="Play playlist", command=self.play_playlist).grid(
            row=1, column=0, sticky="ew", pady=(8, 0)
        )
        ttk.Button(playlist_frame, text="Clear", command=self.clear_playlist).grid(
            row=1, column=1, padx=8, pady=(8, 0)
        )
        self.status = ttk.Label(playlist_frame, text="Ready")
        self.status.grid(row=1, column=2, sticky="e", pady=(8, 0))

    def refresh(self) -> None:
        self.video_list.delete(0, tk.END)
        for video in self.library.list_videos():
            self.video_list.insert(tk.END, video.summary)

    def selected_id(self) -> str:
        selection = cast(
            tuple[int, ...],
            self.video_list.curselection(),  # type: ignore[no-untyped-call]
        )
        if not selection:
            raise ValueError("Select a video first")
        return self.library.list_videos()[selection[0]].video_id

    def add_video(self) -> None:
        self._act(
            lambda: self.library.add(self.name.get(), self.director.get(), int(self.rating.get()))
        )

    def update_rating(self) -> None:
        self._act(lambda: self.library.update_rating(self.video_id.get(), int(self.rating.get())))

    def delete_selected(self) -> None:
        self._act(lambda: self.library.delete(self.selected_id()))

    def add_selected(self) -> None:
        self._add_to_playlist(self.selected_id())

    def add_random(self) -> None:
        self._add_to_playlist(self.library.random_video().video_id)

    def _add_to_playlist(self, video_id: str) -> None:
        self.playlist.append(video_id)
        self._show_playlist()
        self.status.configure(text=f"Added {video_id}")

    def play_playlist(self) -> None:
        self._act(lambda: self.library.play(self.playlist), "Play counts updated")

    def clear_playlist(self) -> None:
        self.playlist.clear()
        self._show_playlist()

    def _show_playlist(self) -> None:
        names = [self.library.get(video_id).name for video_id in self.playlist]
        self.playlist_text.configure(text=" → ".join(names) or "Playlist is empty")

    def _act(self, operation: Callable[[], object], success: str = "Saved") -> None:
        try:
            operation()
            self.refresh()
            self.status.configure(text=success)
        except (KeyError, LookupError, TypeError, ValueError) as error:
            messagebox.showerror("Video Library", str(error))


def main() -> None:
    path = Path(os.environ.get("VIDEO_LIBRARY_PATH", "video_library.csv"))
    VideoLibraryApp(VideoLibrary(CsvVideoRepository(path))).mainloop()


if __name__ == "__main__":
    main()
