# SETUP_SPEC.md

## Overview

This specification defines the requirements for a setup script used to initialize a Python development environment.  
The script is intended to be generated using Claude Code CLI.

## Target Environment

- OS: macOS or Linux (including WSL)
- Shell: bash or sh
- Python version specified via `.python-version`
- Package manager: `uv`

---

## Script Specification

### 1. DevTools Installation Check

The script must check that the following Dev tools are installed.  
It should only report missing tools with guidance — it must **not install** them automatically.

| Tool              | Check Command         |
|-------------------|------------------------|
| Claude Code CLI   | `claude --version`     |
| Gemini CLI        | `gemini --version`     |
| GitHub CLI        | `gh --version`         |
| uv                | `uv --version`         |

If a command is not found, display a warning like:

```sh
echo "❌ Claude CLI not found. Please install it using: npm install -g @anthropic-ai/claude-code"
```

---

### 2. Python Version Pinning

Ensure the Python version defined in `.python-version` is available.  
Use `uv venv` to create a virtual environment using that version.  
There is no need to export environment variables for the venv path.

---

### 3. Dependency Installation

Use `uv sync` to install dependencies as specified in `pyproject.toml`.  
This includes both production and development dependencies.  
Dependencies are declared under `[dependency-groups]`.

---

### 4. pre-commit Setup

Run the following commands to install Git hooks:

```sh
pre-commit install
pre-commit autoupdate
```

Note: Do **not** install `pre-commit` here — it is assumed to be installed via `uv sync`.

---

### 5. Git Initialization

Run:

```sh
git init
```

Optionally, perform an initial commit if `.gitignore` and other base files are already in place.

---

## Expected Output Log

```
✅ Claude CLI installed: v1.0.0
✅ Gemini CLI installed
✅ GitHub CLI installed
✅ uv installed: 0.1.16
✅ Python version: 3.12.1
✅ Virtualenv created
✅ Dependencies installed via uv sync
✅ pre-commit hooks installed
✅ Git repo initialized
```

---

## Notes

- CLI installation must not be performed — only check and warn
- `.pre-commit-config.yaml` is assumed to already exist
- `requirements.txt` is not used
- The script should be **non-interactive** and **idempotent**, so it can run safely in CI

---

# 📦 Setup Script Enhancement: Project Name Update

This document defines the requirements for enhancing the `setup.sh` script to support automatic project name replacement using a Python script.

---

## 🧭 Purpose

To ensure that when initializing a Python project from a template, all references to the default project name (`project_name`) are replaced with a user-relevant name, derived from the directory name.

---

## ✅ Functional Requirements

### 1. Project Name Update Script Invocation

- The setup script must call an external Python script named `update_project_name.py`.
- This script is responsible for replacing all references to the default name (`project_name`) with a new name throughout the project files and directories.

### 2. Default Project Name Resolution

- If no name is provided explicitly, the new project name should default to the current working directory name.
- The name must be normalized by:
  - Converting all letters to lowercase
  - Replacing hyphens (`-`) with underscores (`_`)
- The normalized name should be stored in a constant shell variable:

```sh
DEFAULT_PROJECT_NAME=$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr '-' '_')
```

### 3. Shell Function Structure

- The project name update logic must be encapsulated in a separate function, e.g., `update_project_name()`.
- This function should:
  - Log the operation result (success or error)
  - Execute the Python script as follows:

```sh
python update_project_name.py "$DEFAULT_PROJECT_NAME"
```

- All major setup steps, including this one, must be orchestrated by a central `main()` function for clear and maintainable control flow.

---

## 🔧 Non-Functional Requirements

- The name update step should **not interrupt** the setup flow if it fails, but must log an error clearly.
- The implementation must use **standard shell utilities** and maintain POSIX compatibility.
- This step should be executed **before or after** Python environment setup depending on logical order of the workflow.
- The name update is expected to be **run once per project** (no need for re-runnability or rollback).

---

## 📌 Example Usage in setup.sh

```sh
update_project_name() {
    DEFAULT_PROJECT_NAME=$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr '-' '_')
    echo "🔄 Updating project name to $DEFAULT_PROJECT_NAME..."

    python update_project_name.py "$DEFAULT_PROJECT_NAME"
}
```

Then call this in your `main()` function:

```sh
main() {
    check_dev_tools
    update_project_name
    setup_python_env
    install_dependencies
    setup_pre_commit
    init_git_repo
}
```

---