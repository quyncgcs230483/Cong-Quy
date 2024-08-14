import tkinter as tk                          # Import the tkinter module for creating the GUI
import tkinter.scrolledtext as tkst            # Import ScrolledText from tkinter for text areas with scrollbars

import video_library as lib                    # Import a custom module for handling video library functions
import font_manager as fonts                   # Import a custom module for managing font configurations

# Function to set the text in a given text area widget
def set_text(text_area, content):
    text_area.delete("1.0", tk.END)            # Clear any existing text in the text area
    text_area.insert(1.0, content)             # Insert new content into the text area starting from the beginning
# Class that defines the CheckVideos GUI window and its functionalities
class CheckVideos():
    def __init__(self, window):
        # Set the window size and title
        window.geometry("750x350")
        window.title("Check Videos")
        list_videos_btn = tk.Button(window, text="List All Videos", command=self.list_videos_clicked) # Create and position a button to list all videos
        list_videos_btn.grid(row=0, column=0, padx=10, pady=10)      
        enter_lbl = tk.Label(window, text="Enter Video Number") # Create and position a label for entering video number
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)
        self.input_txt = tk.Entry(window, width=3)# Create and position an entry widget for inputting the video number
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)
        check_video_btn = tk.Button(window, text="Check Video", command=self.check_video_clicked) # Create and position a button to check the details of a specific video
        check_video_btn.grid(row=0, column=3, padx=10, pady=10)
        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")# Create and position a scrolled text widget to display a list of videos
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)
        self.video_txt = tk.Text(window, width=24, height=4, wrap="none") # Create and position a text widget to display details of a specific video
        self.video_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))# Create and position a label for status updates
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)
        self.list_videos_clicked()# Automatically list all videos when the window is initialized
    def check_video_clicked(self):# Function to handle the "Check Video" button click event
        key = self.input_txt.get()             # Get the video number entered by the user
        name = lib.get_name(key)               # Get the video name using the video number
        if name is not None:
            director = lib.get_director(key)   # Get the video director
            rating = lib.get_rating(key)       # Get the video rating
            play_count = lib.get_play_count(key) # Get the video play count
            video_details = f"{name}\n{director}\nrating: {rating}\nplays: {play_count}"
            set_text(self.video_txt, video_details) # Display video details in the text widget
        else:
            set_text(self.video_txt, f"Video {key} not found") # Display an error if video not found
        self.status_lbl.configure(text="Check Video button was clicked!") # Update the status label
    def list_videos_clicked(self): # Function to handle the "List All Videos" button click event
        video_list = lib.list_all()            # Get the list of all videos from the library
        set_text(self.list_txt, video_list)    # Display the list in the scrolled text widget
        self.status_lbl.configure(text="List Videos button was clicked!") # Update the status label

# Main function to run the application
if __name__ == "__main__":                    # Ensure this block runs only when this file is executed directly
    window = tk.Tk()                          # Create the main window object
    fonts.configure()                         # Configure the fonts using the font_manager module
    CheckVideos(window)                       # Instantiate the CheckVideos class to open the GUI
    window.mainloop()                         # Start the Tkinter main loop to keep the window open
