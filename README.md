# To-Do CLI App

A simple Python CLI application to manage your tasks efficiently from the terminal.

## Features
- Add, list, update, and delete tasks
- Store tasks in a JSON file
- Mark tasks as done or undone
- Fully tested using pytest
- Easy-to-use CLI interface

## Requirements
- Python 3.14
- Poetry for dependency management

## Installation

git clone https://github.com/4thNote0004/todo_cli.git
cd to-do-cli
poetry install

## Usage

# Run the CLI
poetry run todo add "Buy milk"
poetry run todo list
poetry run todo update 1 --title "Buy bread" --done
poetry run todo delete 1

## Testing

# Run all tests
poetry run pytest -v

## License
MIT License

