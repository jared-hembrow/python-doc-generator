import argparse
from utils.terminal import Terminal
from utils.html import Html
from utils.docs import FileTools

from os.path import isdir


class Cli:
    """
    This class represents the Command-Line Interface (CLI) for the documentation
    generator. It handles user input, configures the program, extracts
    documentation from files, and generates the final HTML output.

    Attributes:
        root_path (str): The root directory to scan for Python files.
        output_path (str): The directory where the generated HTML will be saved.

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
    root_path = "./"
    output_path = "output"
    # file_tree = {}

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
        Terminal.print_introduction()

        # Display Objects configuration
        Terminal.print_config(
            {
                "Input Path": self.root_path,
                "Output Path": self.output_path,
            }
        )

    def files_and_doc_strings_stage(self):
        """
        Extracts files and their docstrings.

        Creates a `FileTree` to traverse the file system
        and extract information about files and their docstrings.
        Args:
            None

        Returns:
            None
        """

        # STAGE 2:
        self.file_tree = FileTools.build_directories(self.root_path)

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
        html = Html()
        output_html = html.build_html(self.file_tree)

        write = html.write_html_file(self.output_path, output_html)
        if write is not None:
            Terminal.print(write, color="red")

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
        Terminal.print_directory_branch(self.file_tree, level=0)

        # STAGE 3:
        self.build_output_stage()
