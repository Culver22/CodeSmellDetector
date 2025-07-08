import ast
from pathlib import Path


def parse_code(source_or_path):
    """
    Parse Python code from a file path or directly from a string.
    :param source_or_path: (str or Path) - Either a path to a Python file or Python code as a string.
    :return: Parsed AST (Abstract Syntax Tree)
    """
    try:
        # Check if input is a path to a file
        if isinstance(source_or_path, (str, Path)) and Path(source_or_path).is_file():
            with open(source_or_path, 'r', encoding='utf-8') as file:
                # 'utf-8' allows for source_or_path to be parsed on any OS/System (Encoder is specified)
                source = file.read()
        else:
            # Treat input as code string
            source = source_or_path

        return ast.parse(source)
    except FileNotFoundError:
        raise ValueError(f'File not found: {source_or_path}')
    except SyntaxError as e:
        raise ValueError(f'Syntax error in code: {e}')


def get_functions(tree):
    """

    :param tree: from the parse_code function
    :return: List of all functions in the python code
    """
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node)
    return functions


def get_classes(tree):
    """

    :param tree: from the parse_code function
    :return: List of all classes in the python code
    """
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node)
    return classes
