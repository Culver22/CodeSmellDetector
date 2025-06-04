import ast

class SmellDetector:
    def __init__(self, tree, config=None):
        self.tree = tree
        # Allows for config like thresholds e.g max_lines or max_params
        self.config = config or {}

    def detect_long_functions(self, tree, max_lines=50):
        '''
        Detect functions in the AST that exceed a specified number of lines.

        NOTE: The function counts blank lines within a function

        :param tree: ast.AST
            The Abstract Syntax Tree (AST) of the Python code to analyze.
        :param max_lines: int, optional (default=50)
            The maximum number of lines a function can have before being considered too long.
        :return: dict
            A dictionary mapping function names (str) to their line counts (int) for functions longer than max_lines.
        '''
        long_functions = {}  # Dictionary to store functions that are too long

        # Traverse all nodes in the AST tree
        for node in ast.walk(tree):
            # Check if node is a function
            if isinstance(node, ast.FunctionDef):
                start_line = node.lineno  # Line where the function starts
                line_numbers = []  # List to hold all line numbers of statements inside the function

                # Traverse all nodes within the function node to find line numbers
                for n in ast.walk(node):
                    if hasattr(n, 'lineno'):  # Only consider nodes that have a line number
                        line_numbers.append(n.lineno)

                # Determine the last line number of the function
                if line_numbers:
                    end_line = max(line_numbers)
                else:
                    end_line = start_line  # If no line numbers found, function length is 1 line

                line_count = end_line - start_line + 1  # Total lines spanned by the function

                # Check if function is longer than allowed maximum
                if line_count > max_lines:
                    long_functions[node.name] = line_count  # Record function name and its length

        return long_functions
