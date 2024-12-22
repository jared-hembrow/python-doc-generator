from os.path import isdir
from os import mkdir


class Html:
    """
    This class handles the generation of HTML documentation for the codebase.

    Attributes:
        style (str): The inline CSS style content to be included in the HTML.

    Methods:
        write_html_file(self, path: str, html: str) -> Exception | None:
            Writes the generated HTML content to a file at the specified path.
            Returns any exceptions encountered during the process (None or Exception).

        build_html(self, tree: dict) -> str:
            Builds the complete HTML content from the parsed file tree structure.

        build_directory(self, directory: dict, base: bool (optional)) -> str:
            Recursively builds the HTML representation for a directory within the tree.

        build_file(self, file: dict) -> str:
            Builds the HTML representation for a single file with its docstrings.

        build_item(self, item: dict, item_type: str (optional, default: "Function") -> str:
            Builds the HTML representation for a docstring item (function, class, etc.).

        build_sub_item(self, sub_items: dict) -> str:
            Recursively builds the HTML representation for sub-items within a docstring.

        build_meta_items(self, items: list) -> str:
            Processes docstring meta information (parameters, returns) into HTML.

        build_list_item(self, item: dict) -> str:
            Builds the HTML representation for a single parameter or return value.
    """

    @staticmethod
    def write_html_file(path, html):
        """
        Writes the generated HTML content to a file at the specified path.

        Args:
          path (str): The path to the output file (index.html).
          html (str): The html to write to the output file (index.html).

        Returns:
          An exception object if an error occurred during the writing process,
          or None if successful.
        """

        try:
            if not isdir(path):
                mkdir(path)

        except Exception as e:
            return e
        try:
            with open(f"{path}/index.html", "w") as file:
                file.write(html)
        except Exception as e:
            return e
        return None

    def build_html(self, tree):
        """
        Builds the complete HTML content from the parsed file tree structure.

        Args:
          tree (dict): The parsed file tree structure representing the codebase.

        Returns:
          str: The complete HTML content as a string.
        """
        style = """
    <style>
  body {
    font-family: sans-serif;
    margin: 0;
  }
  
  .container {
    margin: 20px;
  }
  
  h3 {
    font-style: oblique; 
  }
    
  details {
    margin: 1rem 0;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 1rem;
    background-color: #f8f8f8; /* Light gray background */
  }
  
  summary {
    cursor: pointer;
    font-weight: bold;
  }
  
  section {
    margin-left: 1rem;
  }
  
  .item {
    margin: 0.5rem 0;
    border: 1px solid #eee;
    border-radius: 3px;
    padding: 0.5rem;
    background-color: #f0f0f0; /* Lighter gray background */
  }
  
  .item h3 {
    margin-bottom: 0.25rem;
  }
  
  .doc-string-list-item {
    margin-left: 1rem;
    list-style-type: disc;
  }
  
</style>
    """

        html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Documentation</title>
  </head>
  {style}
  <body>
  
  {self.build_directory(tree, base=True)}
  
  </body>
</html>
"""
        return html

    def build_directory(self, directory, base=False):
        """
        Recursively builds the HTML representation for a folder within the tree.

        Args:
          folder (dict): A dictionary representing a folder within the file tree.

        Returns:
          str: The HTML representation of the folder and its contents.
        """
        directory_name = directory["name"] if "name" in directory else ""
        files_content = f"<section>{''.join([self.build_file(file) for file in directory['files']] if "files" in directory else "")}</section>"
        folder_content = f"{''.join([self.build_directory(directory_item) for directory_item in directory['directories']]) if "directories" in directory else ""}"

        if base:
            return f"""<section class="container">
        <h1>{directory_name}</h1>        
        {files_content}        
        {folder_content}
        </section>
        """

        return f"""<details>
        <summary>{directory_name}</summary>
        
        {files_content}
        
        </details>
        {folder_content}
        """

    def build_file(self, file):
        """
        Builds the HTML representation for a single file with its docstrings.

        Args:
          file (dict): A dictionary representing a file with its docstring information.

        Returns:
          str: The HTML representation of the file and its docstrings.
        """
        start_tag = "<details>"
        title = f"<summary>{file['name']}</summary>"
        classes_content = (
            f"<div>{''.join([self.build_item(item, item_type="Class") for item in file['content']['classes']])}</div>"
            if len(file["content"]["classes"]) > 0
            else ""
        )
        functions_content = (
            f"<div>{''.join([self.build_item(item) for item in file['content']['functions']])}</div>"
            if len(file["content"]["functions"]) > 0
            else ""
        )

        end_tag = "</details>"
        return start_tag + title + classes_content + functions_content + end_tag

    def build_item(self, item, item_type="Function"):
        """
        Builds the HTML representation for a docstring item (function, class, etc.).

        Args:
          item (dict): A dictionary representing a docstring item.

        Returns:
          str: The HTML representation of the docstring item.
        """

        start_tag = '<article class="item">'
        title = f"<h3>{item['name']}</h3>"
        short_description, long_description = self.build_description(item)
        meta_items = self.build_meta_items(item["doc_string"]["meta"])
        sub_items = (
            self.build_sub_items(item["methods"])
            if item_type == "Class" and "methods" in item
            else ""
        )
        end_tag = "</article>"
        return (
            start_tag
            + title
            + short_description
            + long_description
            + meta_items
            + sub_items
            + end_tag
        )

    def build_description(self, item):
        """
        Extracts the short and long descriptions from a docstring item.

        Args:
            item (dict): A dictionary representing a docstring item
                        (e.g., function, class).

        Returns:
            tuple: A tuple containing the short description and long description
                  as HTML strings.
                  If no short or long description is found, empty strings
                  are returned.
        """
        short_description = ""
        long_description = ""
        if item["doc_string"]:
            if "long_description" in item["doc_string"]:
                long_description = f"<p>{item['doc_string']['long_description']}</p>"
            if "short_description" in item["doc_string"]:
                short_description = f"<p>{item['doc_string']['short_description']}</p>"
        return short_description, long_description

    def build_sub_items(self, sub_items):
        """
        Recursively builds the HTML representation for sub-items within a docstring.

        Args:
          sub_item (dict): A dictionary representing a sub-item within a docstring.

        Returns:
          str: The HTML representation of the sub-item and its potential sub-items.
        """

        sub_list = []
        for item in sub_items:
            sub_list.append(self.build_item(item))
        return "".join(sub_list)

    def build_meta_items(self, items):
        """
        Processes docstring meta information (parameters, returns) into HTML.

        Args:
          items (list): A list of dictionaries containing docstring meta information.

        Returns:
          str: The HTML representation of the parameters and return values sections.
        """
        params = [
            item
            for item in items
            if len(item["args"]) > 0 and item["args"][0] == "param"
        ]
        returns = [
            item
            for item in items
            if len(item["args"]) > 0 and item["args"][0] == "returns"
        ]
        params_tag = f" {'<h4>Params</h4>' if len(params) > 0 else ''}{''.join([self.build_list_item(item) for item in params])}"
        returns_tag = f"{'<h4>Returns</h4>' if len(returns) > 0 else ''}{''.join([self.build_list_item(item) for item in returns])}"
        return params_tag + returns_tag

    def build_list_item(self, item):
        """
        Builds the HTML representation for a single parameter or return value.

        Args:
          item (dict): A dictionary representing a single parameter or return value.

        Returns:
          str: The HTML representation of the parameter or return value list item.
        """

        return f'<li class="doc-string-list-item">{item['arg_name'] if "arg_name" in item else ''} ({item['type_name']}){item['description']}</li>'
