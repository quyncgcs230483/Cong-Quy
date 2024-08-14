import tkinter as tk
import tkinter.scrolledtext as tkst
import video_library as lib
import font_manager as fonts

# Define a class named UpdateVideos
class UpdateVideos:
    def __init__(self, window):
        window.geometry("750x350")# Set the size of the window to 750x350 pixels
        window.title("Update Videos")# Set the title of the window to "Update Videos"
        update_rating_btn = tk.Button(window, text="Update Rating", command=self.update_rating_clicked) # Create a button to update the rating, with a callback method
        update_rating_btn.grid(row=0, column=0, padx=10, pady=10) # Place the button in the grid layout at row 0, column 0 with padding
        enter_lbl = tk.Label(window, text="Enter Video Number")# Create a label prompting the user to enter a video number
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)# Place the label in the grid layout at row 0, column 1 with padding
        self.video_number_txt = tk.Entry(window, width=3)# Create an entry widget for entering the video number
        self.video_number_txt.grid(row=0, column=2, padx=10, pady=10)# Place the entry widget in the grid layout at row 0, column 2 with padding
        rating_lbl = tk.Label(window, text="Enter New Rating")# Create a label prompting the user to enter a new rating
        rating_lbl.grid(row=0, column=3, padx=10, pady=10)# Place the label in the grid layout at row 0, column 3 with padding
        self.rating_txt = tk.Entry(window, width=3)# Create an entry widget for entering the new rating
        self.rating_txt.grid(row=0, column=4, padx=10, pady=10)# Place the entry widget in the grid layout at row 0, column 4 with padding
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))# Create a label to display status messages
        self.status_lbl.grid(row=1, column=0, columnspan=5,
                             sticky="W", padx=10, pady=10)# Place the status label in the grid layout at row 1, spanning 5 columns
        self.details_txt = tk.Text(window, width=48, height=12, wrap="none")# Create a Text widget to display video details       
        self.details_txt.grid(row=2, column=0, columnspan=5,
                              sticky="W", padx=10, pady=10)# Place the Text widget in the grid layout at row 2, column 0, spanning 5 columns

    # Define the callback method for updating the rating
    def update_rating_clicked(self):
        # Get the video number from the input field
        key = self.video_number_txt.get()
        try:            
            new_rating = int(self.rating_txt.get())# Convert the new rating to an integer            
            name = lib.get_name(key)# Retrieve the video name from the library using the entered key
            if name is not None:               
                lib.set_rating(key, new_rating)# Update the rating of the video in the library               
                play_count = lib.get_play_count(key)# Retrieve the play count of the video               
                details = f"{name}\nNew rating: {new_rating}\nPlay count: {play_count}"# Create a string with the updated video details
                self.details_txt.delete("1.0", tk.END)# Update the details_txt Text widget with the new details
                self.details_txt.insert("1.0", details)
                self.status_lbl.configure(text=f"Video {key} rating updated")# Update the status label to indicate success
            else:
                self.status_lbl.configure(text=f"Video {key} not found")# Update the status label if the video is not found
        except ValueError:
            self.status_lbl.configure(text="Please enter a valid rating")# Update the status label if the entered rating is not valid


# Main program execution
if __name__ == "__main__":
    # Create a Tkinter window
    window = tk.Tk()
    # Configure the fonts (assuming this is a predefined function)
    fonts.configure()
    # Create an instance of the UpdateVideos class
    UpdateVideos(window)
    # Start the Tkinter main event loop
    window.mainloop()