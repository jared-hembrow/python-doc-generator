"""
This module provides classes for printing colored text to the terminal and 
displaying information related to the file tree and docstrings.

Includes the following classes:

    - Print: 
        - Provides methods for getting color escape codes and printing 
          colored text to the terminal.

    - PrintInfoToTerminal:
        - Inherits from Print and provides methods for displaying 
          information about the file tree and docstrings, including:
            - Printing directory branches.
            - Printing file details.
            - Printing docstring items (functions, classes, methods).
            - Printing configuration settings.
            - Printing an introduction message.
"""


class Print:
    """
    A class for printing colored text to the terminal.

    Provides methods for:
        - Getting color escape codes.
        - Printing text with a specified color.

    Attributes:
        COLORS (dict): A dictionary of color escape codes.
        RESET (str): An escape code to reset the terminal color.
    """

    COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }
    RESET = "\033[0m"

    def get_color(self, color):
        """
        Gets the color escape code for the specified color.

        Args:
            color (str): The desired color.

        Returns:
            str: The color escape code. If the specified color is invalid,
                 returns the white color escape code.
        """
        return self.COLORS[color] if color in self.COLORS else self.COLORS["white"]

    def print(self, text, color="white"):
        """
        Prints text to the terminal with the specified color.

        Args:
            text (str): The text to be printed.
            color (str, optional): The color of the text.
                                Defaults to "white".

        Returns:
            None
        """

        print(f"{self.get_color(color)}{text}{self.RESET}")


class PrintInfoToTerminal(Print):
    """
    This class provides methods for printing colored text to the terminal
    and displaying information related to the file tree and docstrings.

    Attributes:
        COLORS (dict): A dictionary containing color codes for terminal output.
    """

    def print_directory_branch(self, branch, level=1):
        """
        Prints information about a folder in the file tree.

        Args:
            branch (dict): A dictionary representing a folder in the file tree.
            level (int, optional): The indentation level for the output.
                                Defaults to 1.

        Returns:
            None
        """
        directory_name = branch["name"]
        files_count = f" -- Files: {len(branch["files"])}" if "files" in branch else ""
        directories_count = (
            f" -- Folders: {len(branch["directories"]) }"
            if "directories" in branch
            else ""
        )
        tabs = ["\t" for i in range(0, level)]

        self.print(
            f"{"".join(tabs)}∟ {directory_name}{files_count}{directories_count}",
            color="magenta",
        )
        if "files" in branch:
            for item in branch["files"]:
                self.print_file_detail(item, level=level + 1)
        if "directories" in branch:
            for directory in branch["directories"]:
                self.print_directory_branch(directory, level=level + 1)

    def print_file_detail(self, file, level=1):
        """
        Prints information about a file in the file tree.

        Args:
            file_detail (dict): A dictionary representing a file in the file tree.
            level (int, optional): The indentation level for the output.
                                Defaults to 1.

        Returns:
            None
        """
        file_name = file["name"]
        content_count = (
            f" -- Functions: {len(file["content"]["functions"])}"
            if "content" in file
            else ""
        )

        self.print(
            f"{"".join([
            "\t" for i in range(0, level)
            ])}∟ {file_name}{content_count}",
            color="cyan",
        )
        if "content" in file:
            if "functions" in file["content"]:
                for func in file["content"]["functions"]:
                    self.print_doc_item(func, level=level + 1)
            if "classes" in file["content"]:
                for class_item in file["content"]["classes"]:
                    self.print_class_item(class_item, level=level + 1)

    def print_doc_item(self, doc_item, doc_type="Function", level=1):
        """
        Prints information about a docstring item (function or class).

        Args:
            doc_item (dict): A dictionary representing a docstring item.
            level (int, optional): The indentation level for the output.
                                Defaults to 1.

        Returns:
            None
        """

        colors = {"Cla'ss": "blue", "Function": "yellow", "Method": "magenta"}
        doc_name = doc_item["name"]

        text_color = colors[doc_type] if doc_type in colors else "white"

        self.print(
            f"{"".join(["\t" for i in range(0, level)])}∟ {doc_type}: {doc_name}",
            color=text_color,
        )

    def print_class_item(self, class_item, level=1):
        """
        Prints information about a class and its methods.

        Args:
            self: The instance of the class calling this method.
            class_item: A dictionary representing the class, containing keys like
                    "name", "docstring", and a list of "methods".
            level: The current indentation level for printing (default: 1).
        """

        self.print_doc_item(class_item, doc_type="Class", level=level)
        for method in class_item["methods"]:
            self.print_doc_item(method, doc_type="Method", level=level + 1)

    def print_config(self, config):
        """
        Prints the configuration settings for the program.

        Args:
            config (dict): A dictionary containing the configuration settings.

        Returns:
            None
        """

        for key, item in config.items():
            self.print(f"{key}: {item}", color="blue")

    def print_introduction(self):
        """
        Prints a welcome message to the terminal.

        Returns:
            None
        """

        welcome_message = "Welcome to docstring parsing"
        hashes = "".join(["#" for i in welcome_message])
        self.print(f"{hashes}\n{welcome_message}\n{hashes}", color="green")
