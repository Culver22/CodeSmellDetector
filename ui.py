import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from file_parser import parse_code
from smells import SmellDetector


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
            title="Select Python File",  # Title of the dialog window
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]  # Options to show .py files or all files
        )
        if file_path:
            self.file_entry.delete(0, tk.END)  # Clear the existing text
            self.file_entry.insert(0, file_path)  # Insert new file path

    def run_detection(self):
        '''
        This method handles the detection of code smells from a selected Python file.
        It uses the SmellDetector class to check for:
            - Long functions
            - Large classes
            - Too many parameters
            - Deep nesting

        It then prints a structured report in the output_box (Tkinter Text widget).
        If an invalid file is selected, or an error occurs during analysis,
        an error message is shown instead.
        '''

        file_path = self.file_entry.get()  # Get the selected file path from the input field

        # Ensure the selected file is a .py file
        if not file_path.endswith(".py"):
            messagebox.showerror("Invalid File", "Please select a valid Python (.py) file.")
            return

        try:
            # Parse the file into an AST
            tree = parse_code(file_path)

            # Create an instance of SmellDetector with the AST
            detector = SmellDetector(tree)

            # Run all smell detection methods and store results
            smells = {
                'long_functions': detector.detect_long_functions(tree),
                'large_classes': detector.detect_large_classes(tree),
                'too_many_parameters': detector.detect_long_parameter_list(tree),
                'deep_nesting': detector.detect_deep_nesting(tree),
            }

            # Clear any previous output from the Text box
            self.output_box.delete("1.0", tk.END)

            # Start the formatted output report
            self.output_box.insert(tk.END, "=" * 10 + " CODE SMELL REPORT " + "=" * 10 + "\n\n")

            # Loop through each smell type and print the findings
            for smell_name, results in smells.items():
                # Format smell title
                self.output_box.insert(tk.END, f"[SMELL] {smell_name.replace('_', ' ').title()}:\n")

                # Handle case when no smells were found
                if not results:
                    self.output_box.insert(tk.END, "  No issues found.\n\n")
                    continue

                # Print results with formatting based on smell type
                for name, value in results.items():
                    if smell_name == 'long_functions':
                        self.output_box.insert(tk.END, f"  - {name}: {value} lines\n")
                    elif smell_name == 'large_classes':
                        self.output_box.insert(tk.END, f"  - {name}: {value} methods\n")
                    elif smell_name == 'too_many_parameters':
                        self.output_box.insert(tk.END, f"  - {name}: {value} parameters\n")
                    elif smell_name == 'deep_nesting':
                        self.output_box.insert(tk.END, f"  - {name}: nesting depth {value}\n")
                    else:
                        self.output_box.insert(tk.END, f"  - {name}: {value}\n")

                # Add spacing after each smell type
                self.output_box.insert(tk.END, "\n")

        except Exception as e:
            # Show error message box if analysis fails
            messagebox.showerror("Error", f"Failed to analyze file:\n{str(e)}")

