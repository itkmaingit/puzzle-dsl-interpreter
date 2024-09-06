# Overview

This repository defines the grammar rules for puzzle rules relevant to the study of automatic puzzle rule creation. Developers can set up their development environment according to this document.

## Prerequisites

- [Task](https://taskfile.dev/)
- [pre-commit](https://pre-commit.com/)
- Docker
- Docker Compose


`Task` can be installed by running the following commands.

```bash
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
```

`pre-commit` can be installed by running the following commands.

```bash
pip install pre-commit
```

## Installation

Execute the following command. This application employs pre-commit, so if it is not installed, please execute `pip install pre-commit`.

First, install all necessary modules.

```bash
task init
```

Next, launch the container by `docker compose`. You can run either command. Basically, `make run-dev` is fine.

```bash
task run # without image build
task run-with-build # with image build
task run-from-scratch # with image build without build cache
```

## Development

Development of this application is assumed to be done inside a container. If you have run `task init`, you should have a Docker extension. Click the Docker icon from the side panel, right-click `<your-container-name>` and run `Attach Visual Studio Code`.

Once inside the container, be sure to execute the following commands. The following command is required every time you run `task down`.

```bash
task init
```

To start the application, execute the following command

```bash
task generate # generate puzzle rule.
task generate -- /path/to/output.pzl # generate puzzle and output file.
task analyze -- /path/to/analyze.pzl # analyze puzzle rule.
task example-analyze # analyze existing puzzle rules.
```

## Stop

If something goes wrong or you want to restart the container, execute the following command.

```bash
task down
```

## Test

The tests are performed automatically during git push, but they can also be run in the container with the following commands.

```bash
task test
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
│   │   ├── generator
│   │   │   ├── PuzzleDSLRandomGenerator.py
│   │   │   ├── definitions
│   │   │   │   ├── constants.py
│   │   │   │   ├── errors.py
│   │   │   │   ├── rules.py
│   │   │   │   └── token.py
│   │   │   ├── helpers
│   │   │   │   ├── operators.py
│   │   │   │   └── token.py
│   │   │   ├── stores
│   │   │   │   ├── context.py
│   │   │   │   ├── store.py
│   │   │   │   └── variables.py
│   │   │   └── utils
│   │   │       └── logger.py
│   │   ├── definitions # Syntax Rules. DON'T EDIT.
│   │   │   ├── PuzzleDSLParser.json
│   │   │   ├── PuzzleDSLParser.g4
│   │   │   └── PuzzleDSLLexer.g4
│   │   ├── poc # Feel free to write your own code for verification.
│   │   │   └── test.py
│   │   └── main.py # entrypoint
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

## Caution

When running `task generate`, you may often encounter the error `RecursionError: maximum recursion depth exceeded`. This is an inherently difficult problem to solve. There is currently no way to prevent int + int + int... Currently no way has been found to prevent the `int + int + int...' error. We dynamically change the weights of the values, but by the time this works well, we are often in a deep recursive state. It might be possible to adjust the initial state weights better, but I don't know the appropriate weights. Please make suggestions in the PR.
*** Translated with www.DeepL.com/Translator (free version) ***
