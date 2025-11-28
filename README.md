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

```bash
# Clone the repository
git clone https://github.com/4thNote0004/todo_cli.git
cd to-do-cli

# Install dependencies
poetry install


# Add tasks
poetry run todo add "Buy milk"
poetry run todo add "Send email"

# List tasks
poetry run todo list

# Update tasks
poetry run todo update 2 --title "Send email reminder" --done
poetry run todo update 1 --undone

# Delete tasks
poetry run todo delete 1

# Final list
poetry run todo list

# Run all tests to make sure everything works
poetry run pytest -v
