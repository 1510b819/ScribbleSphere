import os
import customtkinter as ctk
from tkinter import filedialog

class ScribbleSphere(ctk.CTk):
    def startApp(self):
        self.title("Scribble Sphere")  # Set window title
        self.geometry("1080x800")  # Set geometry to 1080x800
        ctk.set_appearance_mode("dark")  # Set the appearance mode to dark

        # Configure the grid layout
        self.grid_columnconfigure(0, weight=3)  # Notes frame column (larger)
        self.grid_columnconfigure(1, weight=1)  # Button frame column (right side)
        self.grid_rowconfigure(0, weight=1)  # Make the row expand

        self.Main()

    def Main(self):
        # Notes Frame (no custom styling)
        self.notes_frame = ctk.CTkFrame(self)
        self.notes_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.notes_frame.grid_rowconfigure(0, weight=0)
        self.notes_frame.grid_rowconfigure(1, weight=1)
        self.notes_frame.grid_columnconfigure(0, weight=1)

        # Title Label inside notes_frame (default styling)
        self.title_label = ctk.CTkLabel(self.notes_frame, text="Scribble")
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        # Textbox for notes with default style
        self.notes = ctk.CTkTextbox(master=self.notes_frame, wrap="word", scrollbar_button_hover_color="lightblue",)
        self.notes.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")

        # Button Frame (default styling)
        self.create_frame = ctk.CTkFrame(self)
        self.create_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nse")

        # Button to create new scribble (default style)
        self.create = ctk.CTkButton(self.create_frame, text="+ Create New Scribble", command=self.new_scribble)
        self.create.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Button to save the current scribble (default style)
        self.save_button = ctk.CTkButton(self.create_frame, text="Save Scribble", command=self.save_scribble)
        self.save_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Button to load an existing scribble (default style)
        self.load_button = ctk.CTkButton(self.create_frame, text="Load Scribble", command=self.load_scribble)
        self.load_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Frame for .txt file buttons (default style)
        self.file_frame = ctk.CTkFrame(self.create_frame)
        self.file_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Load and display .txt file buttons
        self.load_file_buttons()

    def new_scribble(self):
        """Clear the textbox to start a new note."""
        self.notes.delete("1.0", ctk.END)
        self.title_label.configure(text="Scribble")  # Reset title to default

    def save_scribble(self):
        """Save the content of the textbox to a file."""
        content = self.notes.get("1.0", ctk.END).strip()
        if not content:
            print("No content to save!")
            return
        
        # Open file dialog to choose where to save the note in ./Scribble directory
        if not os.path.exists('./Scribble'):
            os.makedirs('./Scribble')
        
        file_path = filedialog.asksaveasfilename(initialdir="./Scribble", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            print("Note saved to:", file_path)

        # After saving, refresh the file buttons to show the new file
        self.load_file_buttons()

        # Set the title to the name of the saved file
        self.title_label.configure(text=os.path.basename(file_path))

    def load_scribble(self):
        """Load content from a file into the textbox."""
        file_path = filedialog.askopenfilename(initialdir="./Scribble", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.notes.delete("1.0", ctk.END)  # Clear current content
            self.notes.insert("1.0", content)  # Insert loaded content
            print("Note loaded from:", file_path)

            # Set the title to the name of the loaded file
            self.title_label.configure(text=os.path.basename(file_path))

    def load_file_buttons(self):
        """Load and display all .txt files in the Scribble directory as buttons."""
        for widget in self.file_frame.winfo_children():
            widget.destroy()  # Clear the previous file buttons

        if not os.path.exists('./Scribble'):
            os.makedirs('./Scribble')

        # Get all .txt files in the './Scribble' directory
        files = [f for f in os.listdir('./Scribble') if f.endswith('.txt')]

        # Create a button for each file (default styling)
        for idx, file_name in enumerate(files):
            file_button = ctk.CTkButton(self.file_frame, text=file_name, 
                                        command=lambda file_name=file_name: self.load_file_content(file_name))
            file_button.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")

    def load_file_content(self, file_name):
        """Load the content of a specific file into the textbox."""
        file_path = os.path.join('./Scribble', file_name)
        with open(file_path, "r") as file:
            content = file.read()
        self.notes.delete("1.0", ctk.END)  # Clear current content
        self.notes.insert("1.0", content)  # Insert loaded content
        print(f"Loaded content from {file_name}")

        # Set the title to the name of the loaded file
        self.title_label.configure(text=file_name)

    def __init__(self):
        super().__init__()
        self.startApp()

# Run the application
app = ScribbleSphere()
app.mainloop()
