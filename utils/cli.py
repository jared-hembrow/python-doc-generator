import argparse
from utils.files import gather_files, import_module_from_file, extract_function_docstrings,group_files_by_folder
from utils.html import FuncDoc,HtmlBody,ModuleDoc,FolderDoc,FileDoc, Doc
from docstring_parser.common import Docstring
class Cli():
    """_summary_
    """
    
    root_path = "./utils"
    output_path = "output"
    file_tree = {}
    file_type = '.py'
    
    def __init__(self): 
        # Parse args given
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--path", help="Path")
        parser.add_argument("-o", "--out", help="Output path",default="output")
        self.args = parser.parse_args()
        

        
        
        
    def print_text(self,text, color='white'):
        """_summary_

        Args:
            text (_type_): _description_
            color (str, optional): _description_. Defaults to 'white'.
        """
        colors ={ 
                "reset": "\033[0m",
                "bold": "\033[1m",
                "underline": "\033[4m",
                "black": "\033[30m",
                "red": "\033[31m",
                "green": "\033[32m",
                "yellow": "\033[33m",
                "blue": "\033[34m",
                "magenta": "\033[35m",
                "cyan": "\033[36m",
                "white": "\033[37m",
            }
        print(f"{colors[color]}{text}{colors['reset']}")
    
    def find_all_files(self):
        self.file_tree = gather_files(self.root_path)

    
    def get_all_modules(self, file_tree):
        for f in file_tree:
            if f.endswith(self.file_type):
                module = import_module_from_file(file_tree[f]['path'])
                docs = extract_function_docstrings(module)
                file_tree[f]['docs'] = docs
                print("DOCS:", docs)
            else:
                print(file_tree[f])
                
                self.get_all_modules(file_tree[f])
    
    def create_folder_docs(self,tree_name, tree):
        
        for file in tree:
            print("\tFILE:", file, tree[file].keys(),"\n")
            # mod_list = self.create_module_docs(tree[file]['name'], tree[file]['docs']['doc_strings'])
            # mod = ModuleDoc(tree[file]['name'], mod_list)
            # return mod_list
            return []
            # for func in tree[file]['docs']:
            #     print("FUNC:",func, tree[file]['docs'][func],"\n")
    def create_file_doc(self, file_dict):
        print("FILE_DICT", file_dict.keys())
        file = FileDoc(file_dict['name'])
        doc_list = file_dict['docs']['doc_strings'] if 'docs' in file_dict else file_dict['doc_strings']
        for doc_obj in doc_list:
            print("DOC OBJ:", doc_obj)
            if "docstring" in doc_obj and isinstance(doc_obj['docstring'], Docstring):
                file.add_docstring(Doc(doc_obj['name'], doc_obj['docstring']))
            if "doc_strings" in doc_obj and len(doc_obj['doc_strings']['doc_strings']) > 0:
                file.add_docstring(self.create_file_doc(doc_obj))
            # print("\tFILE:", file, tree[file].keys(),"\n")
            # mod_list = self.create_module_docs(tree[file]['name'], tree[file]['docs']['doc_strings'])
            # mod = ModuleDoc(tree[file]['name'], mod_list)
            # return mod_list
        return file
    
    def create_module_docs(self, module_name, tree):
        print("File:", tree)
        file = ModuleDoc(module_name, [])
        file_list = list()
        for doc_string in tree:
            if isinstance(doc_string, str):
                continue
            print("\t\t\tDoc:", doc_string)
            if "docstring" in doc_string:
                if isinstance(doc_string['docstring'], Docstring):
                    print("name:", doc_string)
                    file.add_func(FuncDoc(doc_string['name'],doc_string['docstring']))
            else:
                print("ERROR", doc_string)
                file_list += self.create_module_docs(doc_string['name'], doc_string['doc_strings'])
                # self.create_tree()
        file_list.append(file)
        return file_list
    
    def create_func_docs(self, tree):
        pass
    
    def create_tree(self, tree):
        tree_list = list()
        for item in tree:
            print("FOLDER: ", item,tree[item].keys(), "\n")
            folder = FolderDoc(item)
            for file in tree[item]:
                the_tree = self.create_file_doc(tree[item][file])
                folder.add_module(the_tree)
            tree_list.append(folder)
            # for f in tree[item]:
            #     folder.add_module(file)
            #     # print("Doc strings: ", print(tree[item][f]['docs']['doc_strings']))    
        return tree_list
    
    
    def run(self):
        # Print welcome message
        self.print_text(\
            "###############################\nWelcome to docstring parsing\n###############################",
            color="green")
        self.print_text(f"Args: {self.args}", color="red")
        self.find_all_files()
        self.get_all_modules(self.file_tree)
        print("Finished tree", self.file_tree)
        print("\n\n")
        tree_list = self.create_tree(self.file_tree)
        print("FINAL:", tree_list)
        for folder in tree_list:
            print("FINAL FOLDER:", folder, folder.name)
            for item in folder.items:
                print("\t", item, item.items)
                for it in item.items:
                    print("\t\t", it, it.name)
                    print("\t\t\t", it.docstring)
        html_body = HtmlBody(tree_list)
        html_body.build_html()
        html_body.write_html_file(self.output_path)