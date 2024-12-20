FOLDER = {
    "type": "folder",
    "path": "./utils",
    "name": "utils",
    "items": [
        {
            "type": "file",
            "file_type": ".py",
            "path": "./utils/terminal.py",
            "file_name": "terminal.py",
            "name": "terminal",
            "doc_strings": {
                "name": "module.name",
                "doc_strings": [
                    {
                        "name": "TerminalPrint",
                        "sub_doc_strings": {
                            "name": "TerminalPrint",
                            "doc_strings": [
                                {
                                    "name": "print",
                                    "sub_doc_strings": None,
                                    "doc_strings": {
                                        "meta": [
                                            {
                                                "args": ["param", "text (str)"],
                                                "description": "Text that will be printed to terminal",
                                                "arg_name": "text",
                                                "type_name": "str",
                                                "is_optional": False,
                                                "default": None,
                                            },
                                            {
                                                "args": [
                                                    "param",
                                                    "color (str, optional)",
                                                ],
                                                "description": 'color of the text. Defaults to "white".',
                                                "arg_name": "color",
                                                "type_name": "str",
                                                "is_optional": True,
                                                "default": '"white"',
                                            },
                                        ],
                                        "short_description": "Print text to the terminal with the option to choose what color the text will be displayed in",
                                        "blank_after_short_description": True,
                                        "blank_after_long_description": False,
                                        "style": {"name": "GOOGLE", "value": 2},
                                    },
                                }
                            ],
                        },
                        "doc_strings": None,
                    }
                ],
            },
        },
        {
            "type": "file",
            "file_type": ".py",
            "path": "./utils/html.py",
            "file_name": "html.py",
            "name": "html",
            "doc_strings": None,
        },
        {
            "type": "file",
            "file_type": ".py",
            "path": "./utils/__init__.py",
            "file_name": "__init__.py",
            "name": "__init__",
            "doc_strings": None,
        },
        {
            "type": "file",
            "file_type": ".py",
            "path": "./utils/docs.py",
            "file_name": "docs.py",
            "name": "docs",
            "doc_strings": {
                "name": "module.name",
                "doc_strings": [
                    {
                        "name": "FileTree",
                        "sub_doc_strings": {
                            "name": "FileTree",
                            "doc_strings": [
                                {
                                    "name": "import_module_from_file",
                                    "sub_doc_strings": None,
                                    "doc_strings": {
                                        "meta": [
                                            {
                                                "args": ["param", "file_path (str)"],
                                                "description": "path to file",
                                                "arg_name": "file_path",
                                                "type_name": "str",
                                                "is_optional": False,
                                                "default": None,
                                            },
                                            {
                                                "args": ["returns", "module"],
                                                "description": "python file as module",
                                                "type_name": "module",
                                                "is_generator": False,
                                                "return_name": None,
                                            },
                                        ],
                                        "short_description": "Dynamically import python module from a file path",
                                        "blank_after_short_description": True,
                                        "blank_after_long_description": False,
                                        "style": {"name": "GOOGLE", "value": 2},
                                    },
                                },
                                {
                                    "name": "extract_function_docstrings",
                                    "sub_doc_strings": None,
                                    "doc_strings": {
                                        "meta": [
                                            {
                                                "args": ["param", "module (module)"],
                                                "description": "python module to extract docstring",
                                                "arg_name": "module",
                                                "type_name": "module",
                                                "is_optional": False,
                                                "default": None,
                                            },
                                            {
                                                "args": ["returns", "Docstring"],
                                                "description": "List of docstring objects",
                                                "type_name": "Docstring",
                                                "is_generator": False,
                                                "return_name": None,
                                            },
                                        ],
                                        "short_description": "_summary_",
                                        "blank_after_short_description": True,
                                        "blank_after_long_description": False,
                                        "style": {"name": "GOOGLE", "value": 2},
                                    },
                                },
                            ],
                        },
                        "doc_strings": None,
                    }
                ],
            },
        },
        {
            "type": "file",
            "file_type": ".py",
            "path": "./utils/cli.py",
            "file_name": "cli.py",
            "name": "cli",
            "doc_strings": {
                "name": "module.name",
                "doc_strings": [
                    {
                        "name": "Cli",
                        "sub_doc_strings": {
                            "name": "Cli",
                            "doc_strings": [
                                {
                                    "name": "run",
                                    "sub_doc_strings": None,
                                    "doc_strings": {
                                        "meta": [],
                                        "short_description": "Run The main CLI program",
                                        "long_description": "Stage 1 - Get parameters from flags or through interactive mode\nStage 2 - Get Files and doc strings\nstage 3 - Output HTML & CSS files",
                                        "blank_after_short_description": False,
                                        "blank_after_long_description": False,
                                        "style": {"name": "REST", "value": 1},
                                    },
                                }
                            ],
                        },
                        "doc_strings": {
                            "meta": [],
                            "short_description": "_summary_",
                            "blank_after_short_description": False,
                            "blank_after_long_description": False,
                            "style": {"name": "REST", "value": 1},
                        },
                    }
                ],
            },
        },
    ],
    "folders": [
        {
            "type": "folder",
            "path": "./utils/fft",
            "name": "fft",
            "items": [
                {
                    "type": "file",
                    "file_type": ".py",
                    "path": "./utils/fft/giga.py",
                    "file_name": "giga.py",
                    "name": "giga",
                    "doc_strings": {
                        "name": "module.name",
                        "doc_strings": [
                            {
                                "name": "giga",
                                "sub_doc_strings": None,
                                "doc_strings": {
                                    "meta": [
                                        {
                                            "args": ["param", "name (_type_)"],
                                            "description": "_description_",
                                            "arg_name": "name",
                                            "type_name": "_type_",
                                            "is_optional": False,
                                            "default": None,
                                        },
                                        {
                                            "args": ["returns", "_type_"],
                                            "description": "_description_",
                                            "type_name": "_type_",
                                            "is_generator": False,
                                            "return_name": None,
                                        },
                                    ],
                                    "short_description": "_summary_",
                                    "blank_after_short_description": True,
                                    "blank_after_long_description": False,
                                    "style": {"name": "GOOGLE", "value": 2},
                                },
                            }
                        ],
                    },
                },
                {
                    "type": "file",
                    "file_type": ".py",
                    "path": "./utils/fft/__init__.py",
                    "file_name": "__init__.py",
                    "name": "__init__",
                    "doc_strings": None,
                },
            ],
        }
    ],
}
