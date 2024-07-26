.PHONY: init
init:
		@pre-commit install
		@code --install-extension charliermarsh.ruff > /dev/null 2>&1
		@code --install-extension ms-python.mypy-type-checker > /dev/null 2>&1
		@code --install-extension ms-python.python > /dev/null 2>&1
		@code --install-extension ms-azuretools.vscode-docker > /dev/null 2>&1

.PHONY: run-dev
run-dev:
		docker-compose -f docker-compose.dev.yml up -d

.PHONY: run-dev-with-build
run-dev-with-build:
		docker-compose -f docker-compose.dev.yml up -d --build

.PHONY: down
down:
		docker-compose -f docker-compose.dev.yml down --remove-orphans
