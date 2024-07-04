# Overview

This repository is the base repository used for developing applications with FastAPI. Simply use `git clone` and run `make init; make run-dev` to set up the development environment.


## Prerequisites

- Make
- Docker
- Docker Compose
- pre-commit

pre-commit can be installed by running the following commands.

```bash
make install-requirements
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
```

## Memo

The special char ⨱ is used to denote that the maximum recursion level was reached (in this example it was set to 3). I need a better way for doing that, as the returned sentences must be parsable by the rule they were created for.
