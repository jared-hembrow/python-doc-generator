"""
This module provides classes for generating various types of documentation 
from a given codebase structure.

Classes:

    Json: 
        Handles JSON serialization of data.

    Html:
        Generates HTML documentation with a basic style.

    Markdown:
        Generates Markdown documentation.

    Builder:
        Orchestrates the building process for different output formats 
        (HTML, Markdown, JSON).
"""

import json
from .terminal import Print
from .file_tools import FileTools


class Json(Print):
    """
    A class responsible for serializing data into JSON format.

    Inherits from the `Print` class (assumed to provide printing functionalities).

    Args:
        Print: Base class for printing messages with color.
    """

    def build_json(self, data):
        """
        Serializes the given data into a JSON string.

        Args:
            data: The data to be serialized.

        Returns:
            The JSON string representation of the data if successful,
            otherwise None.

        Raises:
            TypeError: If the data contains unsupported types for JSON serialization.
            ValueError: If the data contains invalid values for JSON serialization.
            Exception: For any other unexpected errors during serialization.
        """

        try:
            json_string = json.dumps(data, indent=4)
            return json_string
        except TypeError as error:
            self.print(
                f"TypeError: {error}. Data may contain unsupported types for JSON serialization.",
                color="red",
            )
            return None
        except ValueError as error:
            self.print(
                f"ValueError: {error}. Data may contain invalid values for JSON serialization.",
                color="red",
            )
            return None
        except Exception as error:
            self.print(
                f"An unexpected error occurred during JSON serialization: {error}",
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
        file_list = (
            [self.build_file(file) for file in directory["files"]]
            if "files" in directory
            else ""
        )
        files_content = f"<section>{''.join(file_list)}</section>"
        folder_list = (
            [
                self.build_directory(directory_item)
                for directory_item in directory["directories"]
            ]
            if "directories" in directory
            else []
        )
        folder_content = f"{''.join(folder_list) }"

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
        class_list = [
            self.build_item(item, item_type="Class")
            for item in file["content"]["classes"]
        ]
        classes_content = (
            f"<div>{''.join(class_list)}</div>"
            if len(file["content"]["classes"]) > 0
            else ""
        )
        function_list = [self.build_item(item) for item in file["content"]["functions"]]
        functions_content = (
            f"<div>{''.join(function_list)}</div>"
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
        param_list = [self.build_list_item(item) for item in params]
        return_list = [self.build_list_item(item) for item in returns]
        params_tag = (
            f" {'<h4>Params</h4>' if len(params) > 0 else ''}{"".join(param_list)}"
        )
        returns_tag = (
            f"{'<h4>Returns</h4>' if len(returns) > 0 else ''}{"".join(return_list)}"
        )
        return params_tag + returns_tag

    def build_list_item(self, item):
        """
        Builds the HTML representation for a single parameter or return value.

        Args:
          item (dict): A dictionary representing a single parameter or return value.

        Returns:
          str: The HTML representation of the parameter or return value list item.
        """
        arg_name = item["arg_name"] if "arg_name" in item else ""
        type_name = item["type_name"]
        description = item["description"]
        return f'<li class="doc-string-list-item">{arg_name} ({type_name}){description}</li>'


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
            "#### Parameters:\n"
            + "\n".join([self.build_list_item(item) for item in params])
            if len(params) > 0
            else ""
        )
        returns_tag = (
            "#### Returns:\n"
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

        arg_name = item["arg_name"] if "arg_name" in item else ""
        return f"- `{arg_name} ({item['type_name']})`: {item['description']}"


class Builder:
    """
    A class responsible for building output content based on different formats.

    This class utilizes helper classes (Html, Markdown, Json) to generate
    content in the specified format.

    """

    def __init__(self):
        """
        Initializes the Builder instance.

        Sets up initial attributes:
            - `self.content`: Stores the generated content.
            - `self.html`: An instance of the Html class.
            - `self.markdown`: An instance of the Markdown class.
            - `self.json`: An instance of the Json class.
        """

        self.content = None
        self.html = Html()
        self.markdown = Markdown()
        self.json = Json()

    def build(self, tree, output_type):
        """
        Builds the output content based on the specified output type.

        Args:
            tree: The input data structure (likely a tree-like representation).
            output_type: The desired output format ("html", "markdown", or "json").

        Returns:
            The generated content string.
        """

        if output_type == "html":
            self.content = self.html.build_html(tree)
        if output_type == "markdown":
            self.content = self.markdown.build_markdown(tree)
        if output_type == "json":
            self.content = self.json.build_json(tree)

        return self.content

    def output_content(self, output_path):
        """
        Writes the generated content to the specified output path.

        Utilizes the `write_file` method inherited from the `FileOpts` base class.

        Args:
            output_path: The path to the output file.

        Returns:
            The result of the `write_file` operation (likely a boolean indicating success).
        """

        return FileTools.write_file(output_path, self.content)
