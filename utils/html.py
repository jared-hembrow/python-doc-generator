from os.path import isdir
from os import mkdir

class HtmlBody:
    def __init__(self, item_tree):
        self.item_tree = item_tree
    
    def write_html_file(self, path):
        if not isdir(path):
            mkdir(path)
        with open(f"{path}/index.html", "w") as file:
            file.write(self.html)
    
    def build_html(self):
        self.html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Documentation</title>
  </head>
  <body>
  {''.join([item.build_component() for item in self.item_tree])}
  </body>
</html>
"""

class DocNode:
    def build_component(self):
        return f"""<details>
        <summary>{self.name}</summary>
        <p>
        {''.join([item.build_component() for item in self.items])}
        </p>
        </details>"""

class Doc():
    def __init__(self, name, docstring):
        self.name= name
        self.docstring = docstring
    def build_component(self):
        return f"""<details>
        <summary>{self.name}</summary>
        <p>
        {self.docstring.description}
        </p>
        </details>"""
        
class FileDoc(DocNode):
    def __init__(self,  name, items=[]):
    
        self.name = name
        self.items = items

    def add_docstring(self, docstring):
        self.items.append(docstring)


class FolderDoc(DocNode):
    def __init__(self, name, items=[]):
        self.name = name
        self.items = items
        
    def add_module(self, module):
        self.items.append(module)
    


class ModuleDoc:
    def __init__(self, module_name, func_list):
        self.module_name = module_name
        self.func_list = func_list
    
    def add_func(self, func):
        self.func_list.append(func)
    
    def build_component(self):
         return f"""<details>
        <summary>{self.module_name}</summary>
        <p>
        {''.join([func.build_component() for func in self.func_list])}
        </p>
        </details>"""

class FuncDoc:
    
    def __init__(self,func_name, doc_string):
        self.func_name = func_name
        self.doc_string = doc_string
        
    def build_html(self):
        return self.build_component(self.func_name, self.doc_string.description)
        
    
    def build_component(self):
        return f"""<div>
        <h1>{self.func_name}</h1>
        <p>{self.doc_string.description}</p>
        </div>"""
    