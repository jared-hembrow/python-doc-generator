from os import listdir
from os.path import isdir, basename, join
from docstring_parser import parse
from importlib.util import spec_from_file_location, module_from_spec


class FileTree:
    """
    This class represents a file tree structure for a codebase.

    Attributes:
        root_path (str): The path to the root directory of the file tree.
        file_type (str, optional): The file extension to search for (defaults to ".py").
        docstring_index (list): A list to keep track of processed function names.
        root_folder (dict): A dictionary representing the root folder of the tree.
    """

    def __init__(self, root_path, file_type=".py"):
        """
        Initializes a FileTree object.

        Args:
            root_path (str): The path to the root directory of the file tree.
            file_type (str, optional): The file extension to search for (defaults to ".py").
        """

        self.root_path = root_path
        self.file_type = file_type
        self.docstring_index = []
        self.root_folder = self.search_folder(self.root_path, self.file_type)

    def search_folder(self, path, file_type):
        """
        Recursively builds a dictionary representation of a folder and its contents.

        Args:
            path (str): The path to the folder.
            file_type (str): The file extension to search for.

        Returns:
            dict: A dictionary representing the folder structure, including subfolders,
            files, and their docstrings (if any).
        """

        folder = {"type": "folder", "path": path, "name": basename(path), "items": []}

        for f in listdir(path):
            file_path = join(path, f)

            if isdir(file_path) and not f.startswith("__"):
                folder["folders"] = []
                folder["folders"].append(self.search_folder(file_path, file_type))

            elif f.endswith(file_type):
                folder["items"].append(
                    {
                        "type": "file",
                        "file_type": file_type,
                        "path": file_path,
                        "file_name": f,
                        "name": f.strip(file_type),
                        "doc_strings": self.get_docstring(file_path),
                    }
                )

        return folder

    def import_module_from_file(self, file_path):
        """
        Dynamically imports a Python module from a file path.

        Args:
            file_path (str): The path to the Python file.

        Returns:
            module: The imported Python module.
        """

        spec = spec_from_file_location("module.name", file_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def extract_function_docstrings(self, module):
        """
        Extracts docstrings from functions and sub-functions within a module.

        Args:
            module (module): The Python module to extract docstrings from.

        Returns:
            dict (or None): A dictionary containing the module name and a list of
            extracted docstring information, or None if no docstrings are found.
        """

        doc_strings = []
        for name, obj in module.__dict__.items():
            if callable(obj) and obj.__module__.startswith("module.name"):
                doc = {
                    "name": name,
                    "sub_doc_strings": self.extract_function_docstrings(obj),
                    "doc_strings": None,
                }

                docstring = obj.__doc__
                if docstring:
                    if name not in self.docstring_index:
                        doc["doc_strings"] = self.parse_doc_string(parse(docstring))

                if doc["sub_doc_strings"] is not None or doc["doc_strings"] is not None:
                    doc_strings.append(doc)
                    self.docstring_index.append(name)

        if doc_strings is None or len(doc_strings) < 1:
            return None
        return {"name": module.__name__, "doc_strings": doc_strings}

    def parse_doc_string(self, docstring):
        """
        Parses an AST representation of a docstring into a dictionary.

        Args:
            docstring (ast.AST): The AST representation of the docstring.

        Returns:
            dict: A dictionary containing the extracted information from the docstring,
            including potential metadata (if present).
        """

        converted = {"meta": []}
        for name, obj in docstring.__dict__.items():
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

    def get_docstring(self, path):
        """
        Extracts docstrings from a Python file at the specified path.

        Args:
            path (str): The path to the Python file.

        Returns:
            dict (or None): A dictionary containing the module name and a list of
            extracted docstring information, or None if the file cannot be imported
            or no docstrings are found.
        """

        return self.extract_function_docstrings(self.import_module_from_file(path))
