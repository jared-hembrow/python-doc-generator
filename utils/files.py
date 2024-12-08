from os import listdir
from os.path import isdir
from importlib.util import spec_from_file_location, module_from_spec
from docstring_parser import parse

def gather_files(path, recursive=True, file_type='.py' ):
    """Find all files of a type

    Args:
        path (str): Path to where to began search
        recursive (bool, optional): Continue into sub folders. Defaults to True.
        file_type (str, optional): File extension. Defaults to '.py'.

    Returns:
        dict: A tree of files
    """
    try:
        # Get a list of strings of the files and folders
        root_folder = path.split("/")[-1]
        files_and_folders = listdir(path)
        files_list = list()
        file_tree = dict()
        file_tree[root_folder] = {}
        print(path)
        print("File Tree: ", file_tree)
        # Loop through files and folders and find all files with the file_type extension
        for f in files_and_folders:
            print("file:", f)
            file_path = f"{path.strip('/') if path.endswith('/') else path }/{f}"
            
            # Recursively extract files in subfolders
            if isdir(file_path) and recursive and not f.startswith("__"):
                print("Is folder:" ,f )
                file_tree[root_folder][f] = gather_files(file_path)
            # Append correct file type to list
            elif f.endswith(file_type) :
                file_tree[root_folder][f] = {
                    "path": file_path,
                    "name": f.replace(file_type, ""),
                    "file_type": file_type,
                    "docs": []
                }
                files_list.append(file_path)
    except (OSError, ValueError) as e:
        print(e)
    except Exception as e:
        print(e)
    
    return file_tree    

def group_files_by_folder(files_list):
   
    for f in files_list:
        
        print("f", f)

def import_module_from_file(file_path):
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

def extract_function_docstrings(module):
    """_summary_

    Args:
        module (module): python module to extract docstring

    Returns:
        Docstring: List of docstring objects
    """
    doc_string_tree = dict()
    
    docstrings = []
    for name, obj in module.__dict__.items():
        if callable(obj) and obj.__module__.startswith("module.name"):
            docstrings.append({
                    "name": name,
                    "docs": extract_function_docstrings(obj)
                    })
            print("\n###############################")
            print(f"{name}: {obj}")
            print("Dir:",  dir(obj), "\n")
            print("Module:", obj.__module__, len(obj.__module__), len("module.name"))
            print("Name:", obj.__name__)
            print(obj.__repr__, "\n\n")
            
            
            print("###############################\n")
            docstring = obj.__doc__
            if docstring:
                print(f"Function: {name} Appending")
                docstrings.append( {
                    "name": name,
                    "docstring": parse(docstring)})
    return {
        "name": module.__name__,
        "doc_strings": docstrings}
                
                    