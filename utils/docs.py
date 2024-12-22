import ast
from os import listdir
from os.path import isdir, basename, abspath
from docstring_parser import parse


class FileTools:
    """
    This class provides static methods for working with files and directories,
    including building file/directory structures and parsing docstrings.
    """

    @staticmethod
    def build_file(file_path):
        """
        Builds a dictionary representation of a Python file.

        Args:
            file_path (str): The path to the Python file.

        Returns:
            dict: A dictionary containing information about the file, including:
                - name (str): The name of the file without the ".py" extension.
                - type (str): "file".
                - path (str): The absolute path to the file.
                - content (dict): The content of the file, including functions and classes.
        """

        absolute_path = abspath(file_path)
        return {
            "name": basename(absolute_path).strip(".py"),
            "type": "file",
            "path": absolute_path,
            "content": FileTools.build_file_content(absolute_path),
        }

    @staticmethod
    def parse_doc_string(doc_string):
        """
        Parses a docstring using the `docstring_parser` library and converts it
        into a dictionary representation.

        Args:
            doc_string (str): The docstring to be parsed.

        Returns:
            dict: A dictionary containing the parsed docstring information.
        """

        doc = parse(doc_string)
        converted = {"meta": []}
        for name, obj in doc.__dict__.items():
            if name == "style" and obj is not None:
                converted["style"] = {"name": obj.name, "value": obj.value}
                continue
            if name == "meta":
                for meta in obj:

                    meta_item = {}
                    for meta_name, meta_object in meta.__dict__.items():
                        meta_item[meta_name] = meta_object

                    converted["meta"].append(meta_item)
                continue
            if obj is not None:
                converted[name] = obj
        return converted

    @staticmethod
    def build_doc_string(node):
        """
        Extracts function or class name and docstring information from an AST node.

        Args:
            node (ast.AST): An AST node representing a function or class definition.

        Returns:
            dict (or None): A dictionary containing information about the function/class
                             and its docstring (if present), or None if no docstring is found.

        Raises:
            TypeError: If the provided node is not an ast.FunctionDef or ast.ClassDef.
        """

        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            func_name = node.name
            docstring = ast.get_docstring(node)
            if docstring:
                return {
                    "name": func_name,
                    "doc_string": FileTools.parse_doc_string(docstring),
                }
        return None

    @staticmethod
    def build_file_content(file_path):
        """
        Analyzes a Python file and extracts information about its functions, classes,
        and their docstrings.

        Args:
            file_path (str): The path to the Python file.

        Returns:
            dict: A dictionary containing information about the file's content, including:
                - functions (list): A list of dictionaries representing functions,
                                    each containing name and parsed docstring (if available).
                - classes (list): A list of dictionaries representing classes,
                                   each containing name, parsed docstring (if available),
                                   and a list of methods with their docstrings.
        """

        functions = list()
        classes = list()
        with open(file_path, "r") as file:
            try:
                tree = ast.parse(file.read())
            except SyntaxError:
                print(f"Syntax error in {file_path}")
                return list()

            for node in ast.walk(tree):
                # print("NODE:", node, isinstance(node, ast.FunctionDef))
                if isinstance(node, ast.ClassDef):
                    class_doc = FileTools.build_doc_string(node)
                    if class_doc:
                        class_doc["methods"] = list()
                        for method in node.body:
                            doc = FileTools.build_doc_string(method)
                            if doc:
                                class_doc["methods"].append(doc)
                        classes.append(class_doc)

                else:
                    doc = FileTools.build_doc_string(node)
                    if doc:
                        functions.append(doc)

        return {"functions": functions, "classes": classes}

    @staticmethod
    def build_directory(directory_path):
        absolute_path = abspath(directory_path)
        return {
            "name": basename(absolute_path),
            "type": "directory",
            "path": absolute_path,
            "items": listdir(absolute_path),
        }

    @staticmethod
    def build_directories(base_path):
        """
        Recursively builds a hierarchical representation of the directory structure
        starting from the given base path.

        Args:
            base_path (str): The absolute or relative path to the base directory.

        Returns:
            dict: A dictionary representing the directory structure, containing:
                - name (str): The name of the directory.
                - type (str): "directory".
                - path (str): The absolute path to the directory.
                - directories (list): A list of dictionaries, each representing a
                                    subdirectory within this directory.
                - files (list): A list of dictionaries, each representing a Python
                                file within this directory.

        This function iterates through the contents of the given directory.
        For each item:
            - If it's a directory (and not a hidden directory or a special system directory):
                - Recursively calls `build_directories` to build the subdirectory structure.
                - Adds the subdirectory to the "directories" list if it contains
                subdirectories or Python files.
            - If it's a Python file:
                - Builds a file dictionary using `FileTools.build_file`.
                - Adds the file dictionary to the "files" list if it contains
                functions or classes.

        Finally, removes the "items" key from the directory dictionary
        as it's no longer needed.
        """
        absolute_path = abspath(base_path)
        directory = FileTools.build_directory(absolute_path)

        for item in directory["items"]:
            item_path = f"{absolute_path}/{item}"
            if (
                isdir(item_path)
                and not item.startswith("__")
                and not item.startswith(".")
            ):
                if "directories" not in directory:
                    directory["directories"] = list()
                new_directory = FileTools.build_directories(item_path)
                add = False
                if (
                    "directories" in new_directory
                    and len(new_directory["directories"]) > 0
                ):
                    add = True
                if "files" in new_directory and len(new_directory["files"]) > 0:
                    add = True

                if add:
                    directory["directories"].append(new_directory)
            else:
                if item.endswith(".py"):
                    if "files" not in directory:
                        directory["files"] = list()
                    new_file = FileTools.build_file(item_path)
                    if (
                        len(new_file["content"]["functions"]) > 0
                        or len(new_file["content"]["classes"]) > 0
                    ):
                        directory["files"].append(new_file)
        del directory["items"]
        return directory
