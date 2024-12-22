class Terminal:
    """
    This class provides methods for printing colored text to the terminal
    and displaying information related to the file tree and docstrings.

    Attributes:
        COLORS (dict): A dictionary containing color codes for terminal output.
    """

    @staticmethod
    def print(text, color="white"):
        """
        Prints text to the terminal with the specified color.

        Args:
            text (str): The text to be printed.
            color (str, optional): The color of the text.
                                Defaults to "white".

        Returns:
            None
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
        color = COLORS[color] if color in COLORS else COLORS["white"]
        print(f"{color}{text}\033[0m")

    @staticmethod
    def print_directory_branch(branch, level=1):
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
            f" -- Folders: {len(branch['directories']) }"
            if "directories" in branch
            else ""
        )
        Terminal.print(
            f"{"".join(["\t" for i in range(0, level)])}∟ {directory_name}{files_count}{directories_count}",
            color="magenta",
        )
        if "files" in branch:
            for item in branch["files"]:
                Terminal.print_file_detail(item, level=level + 1)
        if "directories" in branch:
            for directory in branch["directories"]:
                Terminal.print_directory_branch(directory, level=level + 1)

    @staticmethod
    def print_file_detail(file, level=1):
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
            f" -- Functions: {len(file['content']['functions'])}"
            if "content" in file
            else ""
        )

        Terminal.print(
            f"{"".join([
            "\t" for i in range(0, level)
            ])}∟ {file_name}{content_count}",
            color="cyan",
        )
        if "content" in file:
            if "functions" in file["content"]:
                for func in file["content"]["functions"]:
                    Terminal.print_doc_item(func, level=level + 1)
            if "classes" in file["content"]:
                for cl in file["content"]["classes"]:
                    Terminal.print_class_item(cl, level=level + 1)

    @staticmethod
    def print_doc_item(doc_item, doc_type="Function", level=1):
        """
        Prints information about a docstring item (function or class).

        Args:
            doc_item (dict): A dictionary representing a docstring item.
            level (int, optional): The indentation level for the output.
                                Defaults to 1.

        Returns:
            None
        """
        colors = {"Class": "blue", "Function": "yellow", "Method": "magenta"}
        doc_name = doc_item["name"]

        text_color = colors[doc_type] if doc_type in colors else "white"

        Terminal.print(
            f"{"".join(["\t" for i in range(0, level)])}∟ {doc_type}: {doc_name}",
            color=text_color,
        )

    @staticmethod
    def print_class_item(class_item, level=1):
        Terminal.print_doc_item(class_item, doc_type="Class", level=level)
        for method in class_item["methods"]:
            Terminal.print_doc_item(method, doc_type="Method", level=level + 1)

    @staticmethod
    def print_config(config):
        """
        Prints the configuration settings for the program.

        Args:
            config (dict): A dictionary containing the configuration settings.

        Returns:
            None
        """

        for key, item in config.items():
            Terminal.print(f"{key}: {item}", color="blue")

    @staticmethod
    def print_introduction():
        """
        Prints a welcome message to the terminal.

        Returns:
            None
        """

        Terminal.print(
            "###############################\nWelcome to docstring parsing\n###############################",
            color="green",
        )
