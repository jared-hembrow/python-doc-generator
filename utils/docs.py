from os import listdir
from os.path import isdir, basename, join
from docstring_parser import parse
from importlib.util import spec_from_file_location, module_from_spec


class FileTree:

    def __init__(self, root_path, file_type=".py"):
        self.root_path = root_path
        self.file_type = file_type
        self.docstring_index = []
        self.root_folder = self.search_folder(self.root_path, self.file_type)

    def search_folder(self, path, file_type):
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
        """Dynamically import python module from a file path

        Args:
            file_path (str): path to file

        Returns:
            module: python file as module
        """

        spec = spec_from_file_location("module.name", file_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def extract_function_docstrings(self, module):
        """_summary_

        Args:
            module (module): python module to extract docstring

        Returns:
            Docstring: List of docstring objects
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
        return self.extract_function_docstrings(self.import_module_from_file(path))
