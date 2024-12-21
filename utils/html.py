from os.path import isdir
from os import mkdir


class Html:
    """
    This class handles the generation of HTML documentation for the codebase.

    Attributes:
        style (str): The inline CSS style content to be included in the HTML.

    Methods:
        check_dir(self, path: str) -> tuple[bool, Exception | None]:
            Checks if the directory exists and creates it if necessary.
            Returns a tuple indicating success (bool) and any exceptions (None or Exception).

        write_html_file(self, path: str) -> Exception | None:
            Writes the generated HTML content to a file at the specified path.
            Returns any exceptions encountered during the process (None or Exception).

        build_html(self, tree: dict) -> str:
            Builds the complete HTML content from the parsed file tree structure.

        build_folder(self, folder: dict) -> str:
            Recursively builds the HTML representation for a folder within the tree.

        build_file(self, file: dict) -> str:
            Builds the HTML representation for a single file with its docstrings.

        build_item(self, item: dict) -> str:
            Builds the HTML representation for a docstring item (function, class, etc.).

        build_sub_item(self, sub_item: dict) -> str:
            Recursively builds the HTML representation for sub-items within a docstring.

        build_meta_items(self, items: list) -> str:
            Processes docstring meta information (parameters, returns) into HTML.

        build_list_item(self, item: dict) -> str:
            Builds the HTML representation for a single parameter or return value.
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

    def check_dir(self, path):
        """
        Checks if the directory exists and creates it if necessary.

        Args:
          path (str): The path to the directory to check.

        Returns:
          A tuple containing a boolean indicating success and an exception object if
          an error occurred, or None if successful.
        """
        try:
            if not isdir(path):
                mkdir(path)
            return True, None
        except Exception as e:
            return False, e

    def write_html_file(self, path):
        """
        Writes the generated HTML content to a file at the specified path.

        Args:
          path (str): The path to the output file (index.html).

        Returns:
          An exception object if an error occurred during the writing process,
          or None if successful.
        """
        check_path, err = self.check_dir(path)
        if check_path is False:
            return err
        try:
            with open(f"{path}/index.html", "w") as file:
                file.write(self.html)
        except Exception as e:
            return err
        return None

    def build_html(self, tree):
        """
        Builds the complete HTML content from the parsed file tree structure.

        Args:
          tree (dict): The parsed file tree structure representing the codebase.

        Returns:
          str: The complete HTML content as a string.
        """
        self.html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Documentation</title>
  </head>
  {self.style}
  <body>
  <section class="container">
  {self.build_folder(tree)}
  </section>
  </body>
</html>
"""

    def build_folder(self, folder):
        """
        Recursively builds the HTML representation for a folder within the tree.

        Args:
          folder (dict): A dictionary representing a folder within the file tree.

        Returns:
          str: The HTML representation of the folder and its contents.
        """
        return f"""<details>
        <summary>{folder['name'] if "name" in folder else ""}</summary>
        <section>
        {''.join([self.build_file(item) for item in folder['items']] if "items" in folder else "")}
        </section>
        </details>
        {''.join([self.build_folder(folder_item) for folder_item in folder['folders']]) if "folders" in folder else ""}
        """

    def build_file(self, file):
        """
        Builds the HTML representation for a single file with its docstrings.

        Args:
          file (dict): A dictionary representing a file with its docstring information.

        Returns:
          str: The HTML representation of the file and its docstrings.
        """

        if file["doc_strings"] is None:
            return ""
        start_tag = "<details>"
        title = f"<summary>{file['name']}</summary>"
        content = f"<p>{''.join([self.build_item(item) for item in file['doc_strings']['doc_strings']])}</p>"
        end_tag = "</details>"
        return start_tag + title + content + end_tag

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
        if item["doc_strings"]:
            if "long_description" in item["doc_strings"]:
                long_description = f"<p>{item['doc_strings']['long_description']}</p>"
            if "short_description" in item["doc_strings"]:
                short_description = f"<p>{item['doc_strings']['short_description']}</p>"
        return short_description, long_description

    def build_item(self, item):
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
        meta_items = self.build_meta_items(
            item["doc_strings"]["meta"] if item["doc_strings"] else ""
        )
        sub_items = (
            self.build_sub_item(item["sub_doc_strings"])
            if item["sub_doc_strings"]
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

    def build_sub_item(self, sub_item):
        """
        Recursively builds the HTML representation for sub-items within a docstring.

        Args:
          sub_item (dict): A dictionary representing a sub-item within a docstring.

        Returns:
          str: The HTML representation of the sub-item and its potential sub-items.
        """

        sub_list = []
        for item in sub_item["doc_strings"]:
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

        params = [item for item in items if item["args"][0] == "param"]
        returns = [item for item in items if item["args"][0] == "returns"]
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
