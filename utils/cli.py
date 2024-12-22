"""
CLI Class
"""

import argparse
from os.path import isdir, abspath
from os import mkdir
from utils.output import Builder
from utils.terminal import PrintInfoToTerminal
from utils.file_tools import FileTools


class Cli(PrintInfoToTerminal):
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
    output_type = "html"
    file_tree = {}

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
        parser.add_argument("-ot", "--outputtype", help="Output type", default="html")
        self.args = parser.parse_args()

        # Builder
        self.builder = Builder()

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
                self.print("This is an invalid path, please try again", color="red")

        # Get user input for output
        output_path = input("Please enter an output path: ")

        # Get users prefered output type
        output_type = "html"
        while True:
            out_types = {
                "1": "html",
                "2": "markdown",
                "3": "json",
                "html": "html",
                "markdown": "markdown",
                "json": "json",
            }
            get_output_type = input("Please select output type: ")
            if get_output_type in out_types:
                output_type = out_types[get_output_type]
                break
            self.print("Invalid option, please try again", color="red")

        # Assign user input as properties
        self.root_path = input_path
        self.output_path = output_path
        self.output_type = output_type

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
            self.print("Entering Interactive Mode", color="yellow")
            self.run_interactive_mode()
        else:
            if self.args.path is not None:
                self.root_path = self.args.path

            if self.args.out is not None:
                self.output_path = self.args.out
            if self.args.outputtype is not None:
                self.output_type = self.args.outputtype

        # Display Introduction Message
        self.print_introduction()

        # Display Objects configuration
        self.print_config(
            {
                "Input Path": self.root_path,
                "Output Path": self.output_path,
                "Output Type": self.output_type,
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

    def check_output_directory(self, path):
        """Check if the output directory is valid and if not create it

        Args:
            path (str): path of the output directory

        Returns:
            bool: result of the functions success
        """
        # Check output folder
        try:
            if not isdir(path):
                mkdir(path)
        except FileNotFoundError:
            self.print(
                f"FileNotFoundError: The parent directory for '{path}' does not exist."
            )
            return False
        except PermissionError:
            self.print(
                f"PermissionError: You do not have permission to create the directory '{path}'."
            )
            return False
        except OSError as error:
            self.print(
                f"OSError: An error occurred while creating the directory '{path}': {error}"
            )
            return False
        except Exception as error:
            self.print(
                f"An unexpected error occurred while creating the directory '{path}': {error}"
            )
            return False
        return True

    def build_output_stage(self):
        """
        Generates the content and write to output.

        Builds the content using the `builder` object and
        writes it to the specified output file.

        Args:
            None

        Returns:
            None
        """

        # STAGE 3:
        file_path = abspath(f"{self.output_path}")
        file_name = ""

        # Check output folder
        check_out_dir = self.check_output_directory(file_path)
        if not check_out_dir:
            self.print("Error with output directory!", color="red")
            return

        self.print(f"Output: {self.output_type} to '{file_path}'", color="green")

        # Build the content
        content = self.builder.build(self.file_tree, self.output_type)
        if content is None:
            self.print("Unable to Build Content", color="red")
            return

        if self.output_type == "html":
            file_name = "index.html"
        if self.output_type == "markdown":
            file_name = "doc.md"
        if self.output_type == "json":
            file_name = "doc.json"

        # Output the content
        result = self.builder.output_content(f"{file_path}/{file_name}")
        if result is not None:
            self.print(result, color="red")
        else:
            self.print("Output complete", color="green")

    def run(self):
        """Run The main CLI program
        Stage 1 - Get parameters from flags or through interactive mode
        Stage 2 - Get Files and doc strings
        stage 3 - Output HTML & CSS files
        """
        # try:
        #  STAGE 1:
        self.config_stage()

        # STAGE 2:
        self.files_and_doc_strings_stage()
        self.print_directory_branch(self.file_tree, level=0)

        # STAGE 3:
        self.build_output_stage()

        # except Exception as error:
        #     self.print(f"Main Error: {error}", color="red")
