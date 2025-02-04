# Architecture Service

This project is a practical exercise for Node.js, demonstrating how to manage contacts using a file-based service. It includes functionalities to list, add, delete, and watch contacts.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Options](#options)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd architecture-service
    ```

2. Install the dependencies:
    ```sh
    npm install
    ```

## Usage

Run the application using the following command:
```
node contacts.js <command> [options]
```
Replace `<command>` with the desired command and `[options]` with the command options.

Refer to the [Commands](#commands) section for a list of available commands or run the following command to display the help message:
```sh
node contacts.js --help
```

## Commands
* `list`: Lists all contacts.
* `add <firstName> <lastName>`: Adds a new contact.
* `delete <id>`: Deletes a contact.
* `watch`: Watches for changes in the contacts file.

## Options
* `--help`: Displays the help message.
* `--version`: Displays the application version.
* `-C, --color`: Enables color output.
* `-D, --debug`: Enables debug mode.
