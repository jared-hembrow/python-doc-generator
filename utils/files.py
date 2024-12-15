from os import listdir
from os.path import isdir,basename,join
from importlib.util import spec_from_file_location, module_from_spec
from docstring_parser import parse
from utils.docs import FolderDoc, FileDoc

def get_all_files(path, recursive=True, file_type='.py'):
    files_and_folders = listdir(path)
    tree = list()
    
    for f in files_and_folders:
        file_path = f"{path.strip('/') if path.endswith('/') else path }/{f}"
        
        # Recursively extract files in subfolders
        if isdir(file_path) and recursive and not f.startswith("__"):
            tree.append(get_all_files(file_path))
        # Append correct file type to list
        elif f.endswith(file_type):
            tree.append(file_path)
    return tree    

def gather_files(path, recursive=True, file_type='.py'):
    """Find all files of a type

    Args:
        path (str): Path to where to begin search
        recursive (bool, optional): Continue into sub folders. Defaults to True.
        file_type (str, optional): File extension. Defaults to '.py'.

    Returns:
        FolderDoc: A tree of files
    """

    folder_doc = FolderDoc(path, basename(path))

    if not isdir(path):
        return folder_doc

    for f in listdir(path):
        file_path = join(path, f)

        if isdir(file_path) and recursive and not f.startswith("__"):
            folder_doc.add_folder(gather_files(file_path, recursive, file_type))
        elif f.endswith(file_type):
            folder_doc.add_file(FileDoc(file_path, f.strip(file_type), file_type.strip(".")))

    return folder_doc
        
# def gather_files(path, recursive=True, file_type='.py' ):
#     """Find all files of a type

#     Args:
#         path (str): Path to where to began search
#         recursive (bool, optional): Continue into sub folders. Defaults to True.
#         file_type (str, optional): File extension. Defaults to '.py'.

#     Returns:
#         dict: A tree of files
#     """
#     try:
#         # Get a list of strings of the files and folders
#         root_folder = path.split("/")[-1]
#         files_and_folders = listdir(path)
        
#         folder_doc = FolderDoc(path, root_folder)
        
        
        
        
#         # print(path)
#         # print("File Tree: ", file_tree)
#         # Loop through files and folders and find all files with the file_type extension
#         for f in files_and_folders:
#             # print("file:", f)
#             file_path = f"{path.strip('/') if path.endswith('/') else path }/{f}"
            
#             # Recursively extract files in subfolders
#             if isdir(file_path) and recursive and not f.startswith("__"):
#                 print("Is folder:" ,f )
#                 new_folder_doc = gather_files(file_path)
#                 print("parent folder doc:", folder_doc)
#                 print("new folder doc:", new_folder_doc)
#                 folder_doc.add_folder(new_folder_doc)
              
#             # Append correct file type to list
#             elif f.endswith(file_type):
#                 new_file_doc = FileDoc(file_path, f.strip(file_type), file_type.strip("."))
#                 folder_doc.add_file(new_file_doc)
#                 print("Adding file")
               
#     except (OSError, ValueError) as e:
#         print(e)
#     except Exception as e:
#         print(e)
    
#     return folder_doc    

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
                
                    