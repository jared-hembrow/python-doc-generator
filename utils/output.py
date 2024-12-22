from .terminal import Print
import json


class FileOpts:

    def write_file(self, path, text):
        try:
            with open(f"{path}", "w", encoding="utf-8") as file:
                file.write(text)
        except FileNotFoundError as e:
            return f"FileNotFoundError: Could not open file at {path}: {e}"
        except PermissionError as e:
            return f"PermissionError: Insufficient permissions to write to {path}: {e}"
        except IOError as e:
            return f"IOError: An I/O error occurred while writing to {path}: {e}"
        except Exception as e:
            return f"An unexpected error occurred while writing to {path}: {e}"
        return None


class Json(Print):

    def build_json(self, data):
        try:
            json_string = json.dumps(data, indent=4)
            return json_string
        except TypeError as e:
            self.print(
                f"TypeError: {e}. Data may contain unsupported types for JSON serialization.",
                color="red",
            )
            return None
        except ValueError as e:
            self.print(
                f"ValueError: {e}. Data may contain invalid values for JSON serialization.",
                color="red",
            )
            return None
        except Exception as e:
            self.print(
                f"An unexpected error occurred during JSON serialization: {e}",
                color="red",
            )
            return None


class Html:
    """
    This class handles the generation of HTML documentation for the codebase.

    Attributes:
        style (str): The inline CSS style content to be included in the HTML.

    Methods:

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


class Markdown:
    """
    This class handles the generation of Markdown documentation for the codebase.

    Methods:

        build_markdown(self, tree: dict) -> str:
            Builds the complete Markdown content from the parsed file tree structure.

        build_directory(self, directory: dict, base: bool (optional)) -> str:
            Recursively builds the Markdown representation for a directory within the tree.

        build_file(self, file: dict) -> str:
            Builds the Markdown representation for a single file with its docstrings.

        build_item(self, item: dict, item_type: str (optional, default: "Function")) -> str:
            Builds the Markdown representation for a docstring item (function, class, etc.).

        build_description(self, item: dict) -> str:
            Extracts the short and long descriptions from a docstring item.

        build_sub_items(self, sub_items: dict) -> str:
            Recursively builds the Markdown representation for sub-items within a docstring.

        build_meta_items(self, items: list) -> str:
            Processes docstring meta information (parameters, returns) into Markdown.

        build_list_item(self, item: dict) -> str:
            Builds the Markdown representation for a single parameter or return value.
    """

    def build_markdown(self, tree):
        """
        Builds the complete Markdown content from the parsed file tree structure.

        Args:
          tree (dict): The parsed file tree structure representing the codebase.

        Returns:
          str: The complete Markdown content as a string.
        """

        return self.build_directory(tree, base=True)

    def build_directory(self, directory, base=False):
        """
        Recursively builds the Markdown representation for a directory within the tree.

        Args:
          directory (dict): A dictionary representing a folder within the file tree.

        Returns:
          str: The Markdown representation of the folder and its contents.
        """
        directory_name = directory["name"] if "name" in directory else ""
        files_content = "\n".join(
            [self.build_file(file) for file in directory["files"]]
            if "files" in directory
            else ""
        )
        folder_content = (
            "\n".join(
                [
                    self.build_directory(directory_item)
                    for directory_item in directory["directories"]
                ]
            )
            if "directories" in directory
            else ""
        )

        if base:
            return f"# {directory_name}\n\n{files_content}\n\n{folder_content}"

        return f"## {directory_name}\n\n{files_content}\n\n{folder_content}"

    def build_file(self, file):
        """
        Builds the Markdown representation for a single file with its docstrings.

        Args:
          file (dict): A dictionary representing a file with its docstring information.

        Returns:
          str: The Markdown representation of the file and its docstrings.
        """
        title = f"**{file['name']}**\n"
        classes_content = (
            "\n".join(
                [
                    self.build_item(item, item_type="Class")
                    for item in file["content"]["classes"]
                ]
            )
            if len(file["content"]["classes"]) > 0
            else ""
        )
        functions_content = (
            "\n".join([self.build_item(item) for item in file["content"]["functions"]])
            if len(file["content"]["functions"]) > 0
            else ""
        )

        return f"{title}\n{classes_content}\n{functions_content}\n"

    def build_item(self, item, item_type="Function"):
        """
        Builds the Markdown representation for a docstring item (function, class, etc.).

        Args:
          item (dict): A dictionary representing a docstring item.

        Returns:
          str: The Markdown representation of the docstring item.
        """

        title = f"## {item_type}: {item['name']}\n\n"
        short_description, long_description = self.build_description(item)
        meta_items = self.build_meta_items(item["doc_string"]["meta"])
        sub_items = (
            self.build_sub_items(item["methods"])
            if item_type == "Class" and "methods" in item
            else ""
        )

        return (
            f"{title}{short_description}\n{long_description}\n{meta_items}{sub_items}\n"
        )

    def build_description(self, item):
        """
        Extracts the short and long descriptions from a docstring item.

        Args:
            item (dict): A dictionary representing a docstring item
                        (e.g., function, class).

        Returns:
            tuple: A tuple containing the short description and long description
                  as Markdown strings.
                  If no short or long description is found, empty strings
                  are returned.
        """
        short_description = ""
        long_description = ""
        if item["doc_string"]:
            if "long_description" in item["doc_string"]:
                long_description = f"{item['doc_string']['long_description']}"
            if "short_description" in item["doc_string"]:
                short_description = f"{item['doc_string']['short_description']}"
        return short_description, long_description

    def build_sub_items(self, sub_items):
        """
        Recursively builds the Markdown representation for sub-items within a docstring.

        Args:
          sub_item (dict): A dictionary representing a sub-item within a docstring.

        Returns:
          str: The Markdown representation of the sub-item and its potential sub-items.
        """

        sub_list = []
        for item in sub_items:
            sub_list.append(self.build_item(item))
        return "\n".join(sub_list)

    def build_meta_items(self, items):
        """
        Processes docstring meta information (parameters, returns) into Markdown.

        Args:
          items (list): A list of dictionaries containing docstring meta information.

        Returns:
          str: The Markdown representation of the parameters and return values sections.
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
        params_tag = (
            f"#### Parameters:\n"
            + "\n".join([self.build_list_item(item) for item in params])
            if len(params) > 0
            else ""
        )
        returns_tag = (
            f"#### Returns:\n"
            + "\n".join([self.build_list_item(item) for item in returns])
            if len(returns) > 0
            else ""
        )
        return f"{params_tag}\n{returns_tag}\n"

    def build_list_item(self, item):
        """
        Builds the Markdown representation for a single parameter or return value.

        Args:
          item (dict): A dictionary representing a single parameter or return value.

        Returns:
          str: The Markdown representation of the parameter or return value list item.
        """

        return f"- `{item['arg_name'] if 'arg_name' in item else ''} ({item['type_name']})`: {item['description']}"


class Builder(FileOpts):

    def __init__(self):
        self.content = None
        self.html = Html()
        self.markdown = Markdown()
        self.json = Json()

    def build(self, tree, output_type):
        if output_type == "html":
            self.content = self.html.build_html(tree)
        if output_type == "markdown":
            self.content = self.markdown.build_markdown(tree)
        if output_type == "json":
            self.content = self.json.build_json(tree)

        return self.content

    def output_content(self, output_path):

        return self.write_file(output_path, self.content)
