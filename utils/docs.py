from os import listdir
from os.path import isdir,basename,join
from docstring_parser import parse
from importlib.util import spec_from_file_location, module_from_spec

class FileTree():
    
    def __init__(self, root_path, file_type=".py"):
        self.root_path = root_path
        self.file_type = file_type
        self.docstring_index = []
        self.root_folder = self.search_folder(self.root_path, self.file_type)
    
    def search_folder(self, path, file_type):
        folder = {
            "type": "folder",
            "path": path,
            "name": basename(path),
            "items": []
        }
        
        for f in listdir(path):
            file_path = join(path, f)

            if isdir(file_path) and not f.startswith("__"):
                folder['folders'] = []
                folder['folders'].append(self.search_folder(file_path, file_type))
               
            elif f.endswith(file_type):
                folder['items'].append(
                    {
                        "type": "file",
                        "file_type": file_type,
                        "path": file_path,
                        "file_name":f,
                        "name": f.strip(file_type),
                        "doc_string": self.get_docstring(file_path)
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

    def extract_function_docstrings(self,module):
        """_summary_

        Args:
            module (module): python module to extract docstring

        Returns:
            Docstring: List of docstring objects
        """
        doc_string_tree = dict()
        
        doc_strings = []
        for name, obj in module.__dict__.items():
            if callable(obj) and obj.__module__.startswith("module.name"):
                print("###############################\n")
                print("Callable")
                doc = {
                    "name": name,
                    "sub_doc_strings": self.extract_function_docstrings(obj),
                    "doc_string": None
                    
                }
            
                
                # print("\n###############################")
                # print(f"{name}: {obj}")
                # print("Dir:",  dir(obj), "\n")
                # print("Module:", obj.__module__, len(obj.__module__), len("module.name"))
                # print("Name:", obj.__name__)
                # print(obj.__repr__, "\n\n")
                
                
                print("###############################\n")
                docstring = obj.__doc__
                if docstring:
                    print(f"Function: {name} Appending")
                    if name not in self.docstring_index:
                        doc["doc_string"] = self.parse_doc_string(parse(docstring))
               
                if doc['sub_doc_strings']is not None or doc['doc_string'] is not None:
                    doc_strings.append(doc)
                    self.docstring_index.append(name)
                        
        if doc_strings is None or len(doc_strings) < 1:
            return None
        return {
            "name": module.__name__,
            "doc_strings": doc_strings}
    
    def parse_doc_string(self, docstring):
        print(dir(docstring))
        converted = {
            "meta": []
        }
        for name, obj in docstring.__dict__.items():
            print(name, obj, obj is not None)
            if name is "style" and obj is not None:
                converted['style'] = {
                    "name": obj.name,
                    "value": obj.value
                }
                print(dir(obj))
                continue
            if name is "meta":
                for meta in obj:
                    print("-----------------------------------")
                    print(meta)
                    meta_item = {}
                    for meta_name, meta_object in meta.__dict__.items():
                        meta_item[meta_name] = meta_object
                        print(meta_name, meta_object, type(meta_object))
                    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                    converted['meta'].append(meta_item)
                continue
            if obj is not None:
                converted[name] = obj
            print("converted", converted)
        return converted
    
    def get_docstring(self,path):
        return self.extract_function_docstrings(self.import_module_from_file(path))
    

class FolderDoc():
    
    def __init__(self,path, name,  files = [], folders = []):
        self.path = path
        self.name = name
        self.files = files
        self.folders = folders
        
    def add_file(self, file):
        self.files.append(file)
        
    def add_folder(self, folder):
        print("\n",self.folders, folder)
        if folder not in self.folders:
            self.folders.append(folder)
    
class FileDoc():
    
    def __init__(self, path, name, file_type, docs=[]):
        self.path = path
        self.name = name
        self.file_type = file_type
        self.docs = docs
    