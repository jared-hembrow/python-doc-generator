import argparse
from utils.terminal import TerminalPrint
from utils.html import Html
from utils.docs import FileTree

# from docstring_parser.common import Docstring
# import json
from os.path import isdir


class Cli:
    """_summary_"""

    root_path = "./utils"
    output_path = "output"
    file_tree = {}
    file_type = ".py"

    def __init__(self):
        # Parse args given
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
        self.print = TerminalPrint()

    def run_interactive_mode(self):

        # Get user input for the root folder to document
        input_path = None
        # Loop till user enters a valid path
        while input_path is None:
            user_input = input("Please enter the path you wish to Document: ")
            if isdir(user_input):
                input_path = user_input
            else:
                print("This is an invalid path, please try again")

        # Get user input for output
        output_path = input("Please enter an output path: ")

        # Assign user input as properties
        self.root_path = input_path
        self.output_path = output_path

    def run(self):
        """Run The main CLI program
        Stage 1 - Get parameters from flags or through interactive mode
        Stage 2 - Get Files and doc strings
        stage 3 - Output HTML & CSS files
        """

        #  STAGE 1:
        # Configure Object
        if self.args.interactive:
            print("Is Interactive")
            self.run_interactive_mode()

        # Display Introduction Message
        self.print.print_introduction()

        # Display Objects configuration
        self.print.print_config(
            {
                "Input Path": self.root_path,
                "Output Path": self.output_path,
            }
        )

        # STAGE 2:
        # Get File tree
        self.file_tree = FileTree(self.root_path)

        # Display File Tree
        self.print.print_folder_branch(self.file_tree.root_folder, level=0)

        # with open('tree.json', 'w') as jj:
        #     json.dump(self.file_tree.root_folder, jj, indent=4)

        # STAGE 3:
        html_builder = Html()
        html_builder.build_html(self.file_tree.root_folder)
        html_builder.write_html_file(self.output_path)
        # html_body = HtmlBody(tree_list)
        # html_body.build_html()
        # html_body.write_html_file(self.output_path)
