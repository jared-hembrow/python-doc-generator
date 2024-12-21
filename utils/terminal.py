class TerminalPrint:
    """
    This class provides methods for printing colored text to the terminal
    and displaying information related to the file tree and docstrings.

    Attributes:
        COLORS (dict): A dictionary containing color codes for terminal output.
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

        color = self.COLORS[color] if color in self.COLORS else self.COLORS["white"]
        print(f"{color}{text}\033[0m")

    def print_folder_branch(self, branch, level=1):
        """
        Prints information about a folder in the file tree.

        Args:
            branch (dict): A dictionary representing a folder in the file tree.
            level (int, optional): The indentation level for the output.
                                Defaults to 1.

        Returns:
            None
        """

        self.print(
            f"{"".join(["\t" for i in range(0, level)])}∟ {branch['name']} -- Items: {len(branch["items"])} -- Folders: {len(branch['folders']) if "folders" in branch else "0"}",
            color="magenta",
        )
        if "items" in branch:
            for item in branch["items"]:
                self.print_file_detail(item, level=level + 1)
        if "folders" in branch:
            for folder in branch["folders"]:
                self.print_folder_branch(folder, level=level + 1)

    def print_doc_item(self, doc_item, level=1):
        """
        Prints information about a docstring item (function or class).

        Args:
            doc_item (dict): A dictionary representing a docstring item.
            level (int, optional): The indentation level for the output.
                                Defaults to 1.

        Returns:
            None
        """

        self.print(
            f"{"".join(["\t" for i in range(0, level)])}∟ {doc_item['name']} -- {"Class" if doc_item['sub_doc_strings'] is not None else "Function"}",
            color="yellow" if doc_item["sub_doc_strings"] is not None else "blue",
        )
        if doc_item["sub_doc_strings"] is not None:
            for sub_item in doc_item["sub_doc_strings"]["doc_strings"]:
                self.print_doc_item(sub_item, level=level + 1)

    def print_file_detail(self, file_detail, level=1):
        """
        Prints information about a file in the file tree.

        Args:
            file_detail (dict): A dictionary representing a file in the file tree.
            level (int, optional): The indentation level for the output.
                                Defaults to 1.

        Returns:
            None
        """

        self.print(
            f"{"".join([
            "\t" for i in range(0, level)
            ])}∟ {file_detail['name']} -- Doc Strings: {len(file_detail['doc_strings']) if 'doc_strings' in file_detail and file_detail['doc_strings'] is not None else ''} ",
            color="cyan",
        )
        if (
            file_detail["doc_strings"] is not None
            and "doc_strings" in file_detail["doc_strings"]
        ):
            for doc_string in file_detail["doc_strings"]["doc_strings"]:
                self.print_doc_item(doc_string, level=level + 1)

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

        self.print(
            "###############################\nWelcome to docstring parsing\n###############################",
            color="green",
        )
