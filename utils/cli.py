import argparse
from utils.terminal import TerminalPrint
from utils.html import Html
from utils.docs import FileTree

# from docstring_parser.common import Docstring
# import json
from os.path import isdir


class Cli:
    """
    This class represents the Command-Line Interface (CLI) for the documentation
    generator. It handles user input, configures the program, extracts
    documentation from files, and generates the final HTML output.

    Attributes:
        root_path (str): The root directory to scan for Python files.
        output_path (str): The directory where the generated HTML will be saved.
        file_tree (dict): A dictionary representing the file structure.
        file_type (str): The extension of files to be processed (e.g., ".py").

    Methods:
        __init__(self): Initializes the CLI, parses command-line arguments,
                       and creates instances of TerminalPrint and Html classes.
        run_interactive_mode(self): Prompts the user for input in interactive mode.
        config_stage(self): Configures the program based on command-line
                           arguments or user input.
        files_and_doc_strings_stage(self):
                           Extracts files and their docstrings from the file tree.
        build_output_stage(self): Generates the HTML output files.
        run(self): Executes the main program workflow.
    """

    # Properties
    root_path = "./utils"
    output_path = "output"
    file_tree = {}
    file_type = ".py"

    def __init__(self):
        """
        Initializes the CLI object.

        Parses command-line arguments using `argparse`.
        Creates instances of `TerminalPrint` and `Html` for
        terminal output and HTML generation respectively.

        Args:
            None

        Returns:
            None
        """

        # Parse args given in initial command
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            help="Interactive Mode",
            default=False,
        )
        parser.add_argument("-p", "--path", help="Path")
        parser.add_argument("-o", "--out", help="Output path", default="output")
        self.args = parser.parse_args()

        # Property for object that will handle printing to terminal
        self.print = TerminalPrint()

        # Property for the object that will handle the creation of html
        self.html = Html()

    def run_interactive_mode(self):
        """
        Prompts the user for input in interactive mode.

        Gets user input for the root directory and output path.
        Validates the input path and assigns the values to
        `self.root_path` and `self.output_path`.

        Args:
            None

        Returns:
            None
        """

        # Get user input for the root folder to document
        input_path = None
        # Loop till user enters a valid path
        while input_path is None:
            user_input = input("Please enter the path you wish to Document: ")
            if isdir(user_input):
                input_path = user_input
            else:
                self.print.print(
                    "This is an invalid path, please try again", color="red"
                )

        # Get user input for output
        output_path = input("Please enter an output path: ")

        # Assign user input as properties
        self.root_path = input_path
        self.output_path = output_path

    def config_stage(self):
        """
        Configures the CLI object.

        Checks for interactive mode and prompts the user for input if necessary.
        Displays the introduction message and configuration details.

        Args:
            None

        Returns:
            None
        """

        #  STAGE 1:
        # Configure Object
        if self.args.interactive:
            self.print.print("Entering Interactive Mode", color="yellow")
            self.run_interactive_mode()
        else:
            if self.args.path is not None:
                self.root_path = self.args.path

            if self.args.out is not None:
                self.output_path = self.args.out

        # Display Introduction Message
        self.print.print_introduction()

        # Display Objects configuration
        self.print.print_config(
            {
                "Input Path": self.root_path,
                "Output Path": self.output_path,
            }
        )

    def files_and_doc_strings_stage(self):
        """
        Extracts files and their docstrings.

        Creates a `FileTree` object to traverse the file system
        and extract information about files and their docstrings.
        Displays the file tree to the user.

        Args:
            None

        Returns:
            None
        """

        # STAGE 2:
        # Get File tree
        self.file_tree = FileTree(self.root_path)

        # Display File Tree
        self.print.print_folder_branch(self.file_tree.root_folder, level=0)

    def build_output_stage(self):
        """
        Generates the HTML output.

        Builds the HTML content using the `Html` object and
        writes it to the specified output file.

        Args:
            None

        Returns:
            None
        """

        # STAGE 3:
        self.html.build_html(self.file_tree.root_folder)

        write = self.html.write_html_file(self.output_path)
        if write is not None:
            self.print.print(write, color="red")

    def run(self):
        """Run The main CLI program
        Stage 1 - Get parameters from flags or through interactive mode
        Stage 2 - Get Files and doc strings
        stage 3 - Output HTML & CSS files
        """

        #  STAGE 1:
        self.config_stage()

        # STAGE 2:
        self.files_and_doc_strings_stage()

        # STAGE 3:
        self.build_output_stage()
