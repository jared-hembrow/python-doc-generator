# Python Documentation Generator

This is a command-line tool that helps you automatically generate HTML documentation from Python files. It extracts docstrings and organizes them into a user-friendly HTML format.

## Installation

**Prerequisites:**

- Python 3.x

**Installation Steps:**

1. Clone this repository:

   ```bash
   git clone https://github.com/jared-hembrow/python-doc-generator.git
   ```

2. Navigate to the project directory:

   ```bash
   cd python-doc-generator
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

There are two ways to use this tool:

**1. Interactive Mode:**

```bash
python cli.py -i
```

This mode will prompt you for the path to the directory containing your Python files and the desired output path for the generated HTML files.

**2. Command-Line Arguments:**

```bash
python cli.py -p <path_to_python_files> -o <output_path>
```

- `-p`: Path to the directory containing your Python files (required).
- `-o`: Path to the directory where you want to save the generated HTML files (optional, defaults to "output").

## Example

Let's say your Python files are located in a directory called `src` and you want to generate the HTML documentation in a directory called `docs`. You can use the following command:

```bash
python cli.py -p src -o docs
```

This will scan the `src` directory for Python files, extract their docstrings, and generate HTML documentation files in the `docs` directory.

## Features

- Extracts docstrings from Python files.
- Generates well-structured HTML documentation.
- Supports interactive mode for easy configuration.
- Command-line arguments for flexibility.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
