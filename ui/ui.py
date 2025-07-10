import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import parser
import smells
import report


class CodeSmellApp:
    """
    Class which creates the GUI environment for detecting code smells in python files - using Tkinter
    """

    def __init__(self, root):
        """
        Initialises the CodeSmellApp GUI
        :param root: Tkinter root window
        """
        self.root = root
        self.root.title("Code Smell Detector")
        self.root.geometry("1000x750")

        # Setting up UI

        # Label to describe entry
        tk.Label(root, text="Select a Python file:").pack(pady=10)

        # Entry to display selected file path
        self.file_entry = tk.Entry(root, width=60)
        self.file_entry.pack(padx=10)

        # Button to browse for file
        tk.Button(root, text="Browse", command=self.browse_file).pack(pady=5)

        # Button to run detection
        tk.Button(root, text="Run Smell Detection", command=self.run_detection).pack(pady=10)

        # The Output area to display code smell results
        self.output_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=25, width=80)
        self.output_box.pack(padx=10, pady=10)

    def browse_file(self):
        """
        Opens File explorer for selecting a python file and updates the entry box.
        browse_file is called in the constructor when the "Browse button" is selected

        """
        file_path = filedialog.askopenfilename(
            title="Select Python File", # Title of the dialog window
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")] # Options to show .py files or all files
        )
        if file_path:
            self.file_entry.delete(0, tk.END)  # Clear the existing text
            self.file_entry.insert(0,file_path)  # Insert new file path


    def run_detection(self):


