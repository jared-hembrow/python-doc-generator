import argparse


class Cli():
    def __init__(self): 
        # Parse args given
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--path", help="Path", default=".")
        self.args = parser.parse_args()

        
        
        
    def print_text(self,text, color='white'):
        colors ={ 
                "reset": "\033[0m",
                "bold": "\033[1m",
                "underline": "\033[4m",
                "black": "\033[30m",
                "red": "\033[31m",
                "green": "\033[32m",
                "yellow": "\033[33m",
                "blue": "\033[34m",
                "magenta": "\033[35m",
                "cyan": "\033[36m",
                "white": "\033[37m",
            }
        print(f"{colors[color]}{text}{colors['reset']}")
    
    
    
    
    def run(self):
        # Print welcome message
        self.print_text(\
            "###############################\nWelcome to docstring parsing\n###############################",
            color="green")
        self.print_text("Hello", color="red")