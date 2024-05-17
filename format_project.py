#!/usr/bin/env python3

import os
import sys
import pyperclip
import fnmatch
import argparse
import logging

def read_gitignore(directory):
    """Read the .gitignore file and return a list of patterns to exclude, including .git directory by default."""
    gitignore_path = os.path.join(directory, '.gitignore')
    patterns = ['.git/', 'venv/', 'ENV/', 'env/', 'env.bak/', 'venv.bak/', '.gitignore']  # Always exclude common virtual environment directories
    
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as file:
            lines = file.readlines()
        
        patterns += [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    
    return patterns

def should_exclude(path, patterns, root, is_dir):
    """Check if a path should be excluded based on the given patterns."""
    relative_path = os.path.relpath(path, root)
    for pattern in patterns:
        # Check if the pattern is for a directory
        if is_dir and pattern.endswith('/') and fnmatch.fnmatch(relative_path + '/', pattern):
            logging.debug(f"Excluding directory {relative_path} (matched pattern: {pattern})")
            return True
        # Check if the pattern is for a file
        if not is_dir and fnmatch.fnmatch(relative_path, pattern):
            logging.debug(f"Excluding file {relative_path} (matched pattern: {pattern})")
            return True
        # Check if pattern matches any part of the path
        for part in relative_path.split(os.sep):
            if fnmatch.fnmatch(part, pattern):
                logging.debug(f"Excluding {relative_path} (matched part: {part})")
                return True
    return False

def format_project(directory, include_extensions=None, additional_excludes=None, verbose=False):
    """Format the project directory into a structured string."""
    gitignore_patterns = read_gitignore(directory)
    if additional_excludes:
        gitignore_patterns.extend(additional_excludes)
    logging.info(f".gitignore patterns: {gitignore_patterns}")
    project_structure = []
    excluded_files = 0
    processed_files = 0
    
    for root, dirs, files in os.walk(directory):
        # Modify the dirs list in-place to exclude directories
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), gitignore_patterns, directory, True)]
        for file in files:
            file_path = os.path.join(root, file)
            if should_exclude(file_path, gitignore_patterns, directory, False):
                excluded_files += 1
                continue
            if include_extensions and not file_path.endswith(tuple(include_extensions)):
                excluded_files += 1
                continue
            try:
                with open(file_path, 'r') as f:
                    file_contents = f.read()
            except Exception as e:
                logging.debug(f"Error reading {file_path}: {e}")
                continue
            relative_path = os.path.relpath(file_path, directory)
            formatted_file = f"=== File: {relative_path} ===\n{file_contents}\n"
            project_structure.append(formatted_file)
            processed_files += 1
    
    return "\n".join(project_structure), processed_files, excluded_files

def main():
    parser = argparse.ArgumentParser(description="Format a project directory into a structured string.")
    parser.add_argument("directory", help="Path to the project directory")
    parser.add_argument("-c", "--clipboard", action="store_true", help="Copy the formatted project structure to the clipboard")
    parser.add_argument("-o", "--output-file", help="Output file to write the formatted project structure")
    parser.add_argument("-i", "--include", help="Comma-separated list of file extensions to include")
    parser.add_argument("-e", "--exclude", help="Comma-separated list of additional files or directories to exclude")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("--log-file", help="Path to the log file")
    args = parser.parse_args()

    if args.log_file:
        logging.basicConfig(filename=args.log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    elif args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        sys.exit(1)
    
    include_extensions = args.include.split(',') if args.include else None
    additional_excludes = args.exclude.split(',') if args.exclude else None
    formatted_project, processed_files, excluded_files = format_project(args.directory, include_extensions, additional_excludes, args.verbose)

    if args.clipboard:
        pyperclip.copy(formatted_project)
        print("Formatted project structure has been copied to the clipboard.")
    elif args.output_file:
        try:
            with open(args.output_file, 'w') as f:
                f.write(formatted_project)
            print(f"Formatted project structure has been written to {args.output_file}.")
        except Exception as e:
            print(f"Error writing to {args.output_file}: {e}")
    else:
        print(formatted_project)
    
    # Print the summary report
    print("\nSummary Report:")
    print(f"Total files processed: {processed_files}")
    print(f"Total files excluded: {excluded_files}")
    print(f"Total files in project: {processed_files + excluded_files}")

if __name__ == "__main__":
    main()
