# Overview

This repository defines the grammar rules for puzzle rules relevant to the study of automatic puzzle rule creation. Developers can set up their development environment according to this document.

## Prerequisites

- Make
- Docker
- Docker Compose
- pre-commit

pre-commit can be installed by running the following commands.

```bash
pip install pre-commit
```

## Installation

Execute the following command. This application employs pre-commit, so if it is not installed, please execute `pip install pre-commit`.

First, install all necessary modules.

```bash
make init
```

Next, launch the container by `docker compose`. You can run either command. Basically, `make run-dev` is fine.

```bash
make run-dev # without image build
make run-dev-with-build # with image build
```

## Development

Development of this application is assumed to be done inside a container. If you have run `make init`, you should have a Docker extension. Click the Docker icon from the side panel, right-click `<your-container-name>` and run `Attach Visual Studio Code`.

Once inside the container, be sure to execute the following commands. The following command is required every time you run `make down`.

```bash
make init
```

To start the application, execute the following command

```bash
make run
```

## Stop

If something goes wrong or you want to restart the container, execute the following command.

```bash
make down
```

## Test

The tests are performed automatically during git push, but they can also be run in the container with the following commands.

```bash
make test
make all-test # If you have updated your grammar rules, run this command to see if there are any errors.
```

## Directory Structure

```plaintext
.
├── .github
├── .pre-commit-config.yaml
├── Dockerfile # for production (still not implement)
├── .gitignore # DON'T EDIT
├── Makefile
├── mypy.ini # DON'T EDIT
├── docker-compose.dev.yml # DON'T EDIT
├── pytest.ini # DON'T EDIT
├── ruff.toml # DON'T EDIT
├── works -------------------------- Directory for storing application code
│   ├── poetry.lock # DON'T EDIT
│   ├── Makefile
│   ├── .editorconfig # DON'T EDIT
│   ├── puzzle_dsl_interpreter ----- interpreter codes.
│   │   ├── __init__.py # DON'T EDIT
│   │   ├── interpreter ------------ interpreter codes.
│   │   │   ├── PuzzleDSLInterpreter.py ---- interpreter implemention (In practice, implementation is almost entirely left to the Visitor.)
│   │   │   ├── CustomPuzzleDSLParserVisitor.py --- De facto interpreter. (Error evaluation by Visitor pattern)
│   │   │   ├── definitions
│   │   │   │   └── token.py --- token calss definition.
│   │   │   └── errors.py --- error definition.
│   │   ├── main.py # entrypoint
│   │   ├── poc # Feel free to write your own code for verification.
│   │   │   └── test.py
│   │   └── definitions # Syntax Rules. DON'T EDIT.
│   │       ├── PuzzleDSLParser.json
│   │       ├── PuzzleDSLParser.g4
│   │       └── PuzzleDSLLexer.g4
│   ├── scripts
│   │   ├── output_escape_sequence.py ---- Code for converting special characters to escape sequences.
│   │   ├── convert_head_spaces_to_tabs.py ---- conversion code to \t from space
│   │   ├── convert_tabs_to_spaces.sh ---- conversion code to space from \t
│   │   └── all_test.sh ---- Code to test against *.pzl under `rules` directory
│   ├── setup.sh # DON'T EDIT
│   ├── rules # sample puzzle rules. DON'T EDIT. Adding pzl files is ok.
│   ├── pyproject.toml
│   └── .gitignore
├── .vscode
│   ├── settings.json # DON'T EDIT
│   └── launch.json
├── Dockerfile.dev
└── Readme.md
```

## Memo

The special char ⨱ is used to denote that the maximum recursion level was reached (in this example it was set to 3). I need a better way for doing that, as the returned sentences must be parsable by the rule they were created for.
