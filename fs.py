import os
import importlib.util
from docstring_parser import parse

class Files:
    def __init__(self, root_path='./'):
        self.root_path = root_path
    

    def parse_docstring(self,docstring):
        return parse(docstring)
    
    def import_module_from_file(self,file_path):
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def extract_function_docstrings(self, module):
        for name, obj in module.__dict__.items():
            if callable(obj):
                docstring = obj.__doc__
                if docstring:
                    dd = self.parse_docstring(docstring)
                    print("dd",dd)
                    print("dd",dir(dd))
                    print("blank_after_long_description",dd.blank_after_long_description)
                    print("blank_after_short_description",dd.blank_after_short_description)
                    print("deprecation",dd.deprecation)
                    print("description",dd.description)
                    print("examples",dd.examples)
                    print("long_description",dd.long_description)
                    print("many_returns",dd.many_returns)
                    print("meta",dd.meta)
                    print("#############################################")
                    print("params",dd.params)
                    for p in dd.params:
                        print(f"{p.arg_name} {p.type_name}: {p.description}")
                    print("#############################################")
                    print("raises",dd.raises)
                    print("returns",dd.returns)
                    print("short_description",dd.short_description)
                    print("style",dd.style)
                        
                    print(f"Function: {name}\nDocstring:\n{docstring}\n")
                    
    def gather_files(self, path):
        files_and_folders = os.listdir(path)
        files_list = list()
        
        for f in files_and_folders:
            file_path = f"{path.strip('/') if path.endswith('/') else path }/{f}"
            if (os.path.isdir(file_path)):
                print(f"Folder: {f}" )
                files_list += self.gather_files(file_path)
            elif f.endswith('.py'):
                files_list.append(file_path)
        return files_list    
    
    def run(self):
        self.files = self.gather_files(self.root_path)
        for f in self.files:
            print(f)
            mod = self.import_module_from_file(f)
            self.extract_function_docstrings(mod)
