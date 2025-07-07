import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

from parser.parser import parse_code
from smells.smells import SmellDetector

class CodeSmellApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Smell Detector")
        self.root.geometry("700x500")

        self.setup_ui()