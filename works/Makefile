
.PHONY: init
init:
		@code --install-extension charliermarsh.ruff > /dev/null 2>&1
		@code --install-extension ms-python.mypy-type-checker > /dev/null 2>&1
		@code --install-extension ms-python.python > /dev/null 2>&1
		@code --install-extension ms-python.vscode-pylance > /dev/null 2>&1
		@code --install-extension mike-lischke.vscode-antlr4 > /dev/null 2>&1
		@poetry config virtualenvs.in-project true
		@poetry install --no-root

# make run INPUT=<input-file-name>
# relative path from `works`
.PHONY: run
run:
		@bash scripts/convert_tabs_to_spaces.sh
		poetry run python puzzle_dsl_interpreter/main.py $(INPUT)

.PHONY: test
test:
		@poetry run pytest
