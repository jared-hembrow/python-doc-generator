from os import listdir
from os.path import isdir

def gather_files(path, recursive=True, file_type='.py' ):
    """Find all files of a type

    Args:
        path (str): Path to where to began search
        recursive (bool, optional): Continue into sub folders. Defaults to True.
        file_type (str, optional): File extension. Defaults to '.py'.

    Returns:
        list: A list of file paths
    """
    try:
        # Get a list of strings of the files and folders
        files_and_folders = listdir(path)
        files_list = list()
        
        # Loop through files and folders and find all files with the file_type extension
        for f in files_and_folders:
            file_path = f"{path.strip('/') if path.endswith('/') else path }/{f}"
            
            # Recursively extract files in subfolders
            if isdir(file_path) and recursive:
                files_list += gather_files(file_path)
            # Append correct file type to list
            elif f.endswith(file_type):
                files_list.append(file_path)
    except (OSError, ValueError) as e:
        print(e)
    except Exception as e:
        print(e)
    
    return files_list    