import ast

class SmellDetector:
    def __init__(self, tree, config=None):
        self.tree = tree
        # Allows for config like thresholds e.g max_lines or max_params
        self.config = config or {}


