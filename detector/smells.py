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

    def detect_large_classes(self, tree, max_methods=10):
        '''
        Detect classes in the AST that contain too many methods.

        :param tree: ast.AST
            The Abstract Syntax Tree (AST) of the Python code to analyze.
        :param max_methods: int, optional (default=10)
            The maximum number of methods a class can have before being considered too large.
        :return: dict
            A dictionary mapping class names (str) to their method counts (int) for classes exceeding max_methods.
        '''
        large_classes = {}

        # Traverse all nodes in the AST tree
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_count = 0

                # Check each element in the class body
                for method in node.body:
                    if isinstance(method, ast.FunctionDef):
                        method_count += 1

                # If method count exceeds or equals threshold, record it
                if method_count > max_methods:
                    large_classes[node.name] = method_count

        return large_classes

    def detect_long_parameter_list(self, tree, max_params=5):
        '''
        Detects functions that have too many parameters.

        :param tree: ast.AST
            The Abstract Syntax Tree (AST) of the Python code to analyze.
        :param max_params: int, optional (default=5)
            The maximum number of parameters a function can have before being considered too complex.
        :return: dict
            A dictionary mapping function names (str) to the number of parameters (int) for functions exceeding max_params.
        '''
        long_param_functions = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                parameter_names = []  # List to hold parameter names

                for argument in node.args.args:
                    parameter_names.append(argument.arg)

                # Exclude 'self' if it's a method inside a class
                if parameter_names and parameter_names[0] == 'self':
                    parameter_names = parameter_names[1:]

                parameter_count = len(parameter_names)

                if parameter_count > max_params:
                    long_param_functions[node.name] = parameter_count

        return long_param_functions


