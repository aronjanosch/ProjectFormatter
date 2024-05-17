# ProjectFormatter
ProjectFormatter is a command-line tool that formats a project directory into a structured string, with options to include specific file types, exclude files and directories based on `.gitignore` patterns, and additional exclusions specified from the command line. It also supports copying the output to the clipboard.

## Features

- Formats the directory structure of a project.
- Excludes files and directories based on `.gitignore` patterns.
- Optionally includes only specific file types.
- Allows additional files or directories to be excluded via command-line arguments.
- Outputs the formatted structure to the console, a file, or the clipboard.
- Provides a summary report of processed and excluded files.
- Verbose mode for detailed output during processing.

## Installation

### Prerequisites

- Python 3.x
- `pyperclip` library (install using `pip install pyperclip`)

### Installation Steps

1. Clone the repository:

```sh
git clone https://github.com/yourusername/ProjectFormatter.git
cd ProjectFormatter
```

2. Make the script executable and move it to a directory in your PATH:

```sh
chmod +x format_project.py
mv format_project.py /usr/local/bin/format_project
```

## Usage

```sh
format_project <path_to_project> [options]
```

### Options

- `-c`, `--clipboard`: Copy the formatted project structure to the clipboard.
- `-o <file>`, `--output-file <file>`: Write the formatted project structure to the specified output file.
- `-i <extensions>`, `--include <extensions>`: Comma-separated list of file extensions to include.
- `-e <patterns>`, `--exclude <patterns>`: Comma-separated list of additional files or directories to exclude.
- `-v`, `--verbose`: Enable verbose mode.
- `--log-file <file>`: Path to the log file.

### Examples

Format a project and print to the console:

```sh
format_project /path/to/your/project
```

Format a project and copy to the clipboard:

```sh
format_project /path/to/your/project -c
```

Format a project and include only specific file types:

```sh
format_project /path/to/your/project -i .py,.txt
```

Format a project and exclude specific files:

```sh
format_project /path/to/your/project -e LICENSE,README.md
```

Format a project, copy to the clipboard, and enable verbose mode:

```sh
format_project /path/to/your/project -c -v
```

Format a project and log verbose output to a file:

```sh
format_project /path/to/your/project --log-file debug.log
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
"""