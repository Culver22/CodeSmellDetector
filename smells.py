import ast


class SmellDetector:
    def __init__(self, tree, config=None):
        self.tree = tree
        self.source_code = []
        # Allows for config like thresholds e.g max_lines or max_params
        self.config = config or {}

    def detect_long_functions(self, tree, max_lines=30):
        """
        Detect functions in the AST that exceed a specified number of lines,
        ignoring blank lines and docstrings for more accurate line counts.

        :param tree: ast.AST
            The Abstract Syntax Tree (AST) of the Python code to analyze.
        :param max_lines: int, optional (default=30)
            The maximum number of lines a function can have before being considered too long.
        :return: dict
            A dictionary mapping function names (str) to their adjusted line counts (int)
            for functions longer than max_lines.
        """
        long_functions = {}  # Dictionary to store functions that are too long

        # Split the full source code into lines to access by line number
        source_lines = self.source_code

        # Traverse all nodes in the AST tree
        for node in ast.walk(tree):
            # Check if node is a function definition
            if isinstance(node, ast.FunctionDef):
                # Get the docstring for the function, if any
                docstring = ast.get_docstring(node)

                # Starting line number of the function definition
                start_line = node.lineno

                # Determine the last line number of the function by finding
                # the max lineno in all child nodes, fallback to start_line
                end_line = max(getattr(n, 'lineno', start_line) for n in ast.walk(node))

                # Calculate the length of the docstring in lines, if present
                if docstring:
                    docstring_lines = len(docstring.splitlines())
                    # Adjust start line to exclude docstring lines (and the quotes line)
                    adjusted_start = start_line + docstring_lines + 1
                    # Calculate function length excluding the docstring lines
                    length = end_line - adjusted_start + 1
                else:
                    # If no docstring, length is simply last - first line + 1
                    length = end_line - start_line + 1

                # Check if function length exceeds the allowed maximum
                if length > max_lines:
                    # Record function name and its adjusted length
                    long_functions[node.name] = length

        return long_functions

    def detect_large_classes(self, tree, max_methods=10):
        """
        Detect classes in the AST that contain too many methods.

        :param tree: ast.AST
            The Abstract Syntax Tree (AST) of the Python code to analyze.
        :param max_methods: int, optional (default=10)
            The maximum number of methods a class can have before being considered too large.
        :return: dict
            A dictionary mapping class names (str) to their method counts (int) for classes exceeding max_methods.
        """
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
        """
        Detects functions that have too many parameters.

        :param tree: ast.AST
            The Abstract Syntax Tree (AST) of the Python code to analyze.
        :param max_params: int, optional (default=5)
            The maximum number of parameters a function can have before being considered too complex.
        :return: dict
            A dictionary mapping function names (str) to the number of parameters (int) for functions exceeding
            max_params.
        """
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

    def detect_deep_nesting(self, node=None, current_depth=0, max_depth=3):
        """
        Detect functions with deep levels of nested control structures.

        :param node: ast.AST
            Current node in the AST traversal (defaults to root tree if None).
        :param current_depth: int
            Current level of nesting (used internally in recursion).
        :param max_depth: int
            Max allowed depth before being flagged.
        :return: dict
            Function names mapped to their max nesting depth if they exceed threshold.
        """
        # If no node passed, use the root tree
        if node is None:
            node = self.tree

        control_nodes = (
            ast.If,
            ast.For,
            ast.While,
            ast.With,
            ast.Try,
        )

        results = {}

        for child in ast.iter_child_nodes(node):
            # If it's a function definition, track the deepest nesting inside it
            if isinstance(child, ast.FunctionDef):
                max_found = self._calculate_max_nesting(child)
                if max_found > max_depth:
                    results[child.name] = max_found

            # Continue searching inside the module or class
            else:
                results.update(self.detect_deep_nesting(child, max_depth=max_depth))

        return results

    def _calculate_max_nesting(self, node, depth=0):
        """
        Recursively calculates the maximum depth of nested control structures.

        :param node: ast.AST
        The AST node to inspect.
        :param depth: int
        The current depth of control structure nesting.
        :return: int
        The deepest level of nesting found under this node.
        """

        control_nodes = (
            ast.If,
            ast.For,
            ast.While,
            ast.With,
            ast.Try,
        )

        max_depth = depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, control_nodes):
                # Increase depth if it's a control node
                child_depth = self._calculate_max_nesting(child, depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                # Recurse without increasing depth
                child_depth = self._calculate_max_nesting(child, depth)
                max_depth = max(max_depth, child_depth)

        return max_depth
