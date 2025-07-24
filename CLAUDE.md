# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Text Processing CLI Application ("mypt/demo")

A Python 3.12+ text processing CLI application demonstrating TDD best practices, structured logging, and modern Python development patterns.

## Tech Stack

**Python 3.12+** | uv | Ruff | mypy | pytest + Hypothesis | pre-commit | GitHub Actions

## Project Structure (default – update as needed)

```
project-root/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── dependabot.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── template/
│   ├── src/
│   │   └── template_package/    # A complete example of a model package
│   │       ├── __init__.py      # Example of package exports
│   │       ├── py.typed         # Marker file for type information
│   │       ├── types.py         # Best practices for type definitions
│   │       ├── core/
│   │       │   └── example.py   # Example of class/function implementation
│   │       └── utils/
│   │           ├── helpers.py   # Example implementation of utility functions
│   │           ├── logging_config.py # Example logging configuration
│   │           └── profiling.py # Example implementation for performance profiling
│   └── tests/                   # Fully implemented test code examples
│       ├── unit/                # Unit tests
│       ├── property/            # Property-based tests
│       ├── integration/         # Integration tests
│       └── conftest.py          # pytest fixtures
├── src/                         # Development directory for the actual project
│       └── project_name/
│           └── (Place project-specific packages here)
├── tests/                       # Testing directory for the actual project
│   ├── unit/
│   ├── property/
│   ├── integration/
│   └── conftest.py
├── docs/                        # Documentation
├── scripts/
├── pyproject.toml
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
└── CLAUDE.md
```

## Mandatory Requirements for Implementation

1. **Incremental and staged development** (Protocol → Test → Implementation → Optimization)  
2. **Automated quality checks** (format, lint, typecheck, test)  
3. **Ensuring observability** (logging & profiling)

### 0. Development Environment

- **Package management**: Use `uv` for unified environment management. Always prefix Python commands with `uv run`.  
- **Adding dependencies**: Use `uv add` (for regular packages) / `uv add --dev` (for development packages)  
- **GitHub operations**: Use `make pr` / `make issue` or the `gh` command  
- **Quality assurance**: Pre-commit hooks are configured. Run `make check-all` for comprehensive checks  
- **Development support**: Helpful development commands are aggregated in the Makefile. Use `make help` to list them

### 1. Implementation Flow: TDD-Based Incremental Development

Development with Claude Code follows a test-driven development (TDD) approach inspired by t-wada.  
Repeat the following cycle to implement features safely in small steps:

**Red** (Write a failing test)  
**Green** (Make it pass with a minimal implementation)  
**Refactor** (Clean up and generalize the implementation and tests)

#### Implementation Steps

1. Define protocols (interface design)  
2. Implement tests (unit tests and property-based tests)  
3. Create a temporary implementation  
4. Add logging and error messages  
5. Generalize the implementation (ensure tests pass)  
6. Optimize through profiling

### 2. Quality Checks for Implementation (Run Continuously)

Perform the following quality checks in this order, and submit commits or pull requests only after passing all of them:

```bash
make format     # Auto-formatting (using ruff)
make lint       # Linting for code style compliance
make typecheck  # Type consistency check (mypy strict)
make test       # Run unit, integration, and property-based tests
```

> To run all checks at once: `make check-all`

### 3. Logging (Applied to All Code)

### Mandatory Requirements

1. At the top of each module: define a `logger`  
2. At the start & end of each function: output logs  
3. On errors: specify `exc_info=True`  
4. Log levels: DEBUG | INFO | WARNING | ERROR

Best Practices: @template/src/template_package/utils/logging_config.py & @template/src/template_package/core/example.py

### Configuration
```python
setup_logging(level="INFO")
# Or 
export LOG_LEVEL=INFO
```

### Test Configuration
```bash
# Control test-time log level via environment variable
export TEST_LOG_LEVEL=INFO  # Default is DEBUG
```

```python
# Change log level for individual tests
def test_custom_log_level(set_test_log_level):
    set_test_log_level("WARNING")
    # Run the test
```

### 4. Performance Profiling (Limited to Necessary Areas)

Perform profiling for functions with long execution times, batch processing, I/O operations, recursive functions, etc.

```python
from template_package.utils.profiling import profile, timeit, Timer

@profile  # Detailed profiling
@timeit   # Measure execution time
def func():
    ...

with Timer("operation"):  # Measure a specific code block
    ...
```

Best Practices：@template/src/template_package/utils/profiling.py

### 5. Testing Strategy (Based on TDD Principles)

* Tests should focus on **verifying behavior**, and be written based on specifications.  
* Don’t aim for high coverage alone — write tests for each meaningful behavior.

### Principles

- Proceed in small steps  
- Generalize using triangulation  
- Start with uncertain or risky parts  
- Continuously update the test list

#### Example of Triangulation

```python
# 1. Temporary implementation: return 5
assert add(2, 3) == 5

# 2. Generalize: return a + b
assert add(10, 20) == 30

# 3. Confirm edge cases
assert add(-1, -2) == -3
```

#### Test Types

1. **Unit**: Basic functionality tests `template/tests/unit/`  
2. **Property-Based**: Auto-generated with Hypothesis `template/tests/property/`  
3. **Integration**: Interaction/combined tests `template/tests/integration/`

#### Notes

- 1 test : 1 behavior  
- Commit after Red → Green  
- Use Japanese test names where appropriate  
- Refactor when you see duplication, readability issues, or SOLID violations

#### Test Naming Convention

`test_[normal_case|error_case|edge_case]_condition_expectedResult()`

### 6. Evidence-Based Development

**Prohibited words**: best, optimal, faster, always, never, perfect  
**Recommended words**: measured, documented, approximately, typically

**Required Evidence Types**:

- **Performance**: "measured Xms" | "reduces X%"  
- **Quality**: "coverage X%" | "complexity Y"  
- **Security**: "scan detected X"  
- **Reliability**: "uptime X%" | "error rate Y%"

### 7. Efficiency Techniques

#### Communication Notation
```yaml
→ : "Process flow"       # analyze → fix → test  
| : "Options/Separator"  # option1 | option2  
& : "Parallel/Combined"  # task1 & task2  
::: : "Definition"       # variable ::: value  
» : "Sequence"           # step1 » step2  
@ : "Reference/Location" # @file:line
```

#### Execution Patterns

- **Parallel**: No dependencies, no conflicts, order doesn't matter → multiple file loading | independent tests | parallel builds  
- **Batch**: Same operation type, shared resources → bulk formatting | import fixes | batch tests  
- **Sequential**: Has dependencies, state changes, transactions → DB migrations | staged refactoring | dependency installation

#### Error Recovery

- **Retry**: Up to 3 times with exponential backoff  
- **Fallback**: Prioritize speed → reliability  
- **State Restoration**: checkpoint » rollback | recover from clean state » resume | re-run only failed steps

#### Providing Constructive Feedback

**Triggers for Feedback**:

- Detecting inefficient approaches  
- Identifying security risks  
- Recognizing over-engineering  
- Spotting inappropriate practices

**Approach**:

- Direct expression > indirect phrasing  
- Evidence-based alternatives > mere criticism  
- Examples: "More efficient method: X" | "Security risk: SQL injection"

## Using the `template/` Directory

Always refer to it before implementation:

- **Classes/Functions**: @template/src/template_package/core/example.py (type hints, docstrings, error handling)  
- **Type Definitions**: @template/src/template_package/types.py  
- **Utilities**: @template/src/template_package/utils/helpers.py  
- **Tests**: @template/tests/{unit|property|integration}/  
- **Fixtures**: @template/tests/conftest.py  
- **Logging**: @template/src/template_package/utils/logging_config.py  

During implementation:  
Check similar examples in `template/` → Follow their patterns → Adjust for your project

Note: Changes or deletions in `template/` are prohibited

## Frequently Used Commands
```bash
# Initial Setup
make setup              # Install dependencies + configure pre-commit hooks

# Basics
make help               # Show list of available commands  
make check-all          # Run all checks  
make clean              # Remove caches

# Quality Checks
make format             # Code formatting  
make lint               # Linting  
make typecheck          # Type checking  
make test               # Run tests  
make test-cov           # Run tests with coverage report

# GitHub Operations
make pr TITLE="x" BODY="y" [LABEL="z"]     # Create a pull request  
make issue TITLE="x" BODY="y"              # Create an issue  
# Note: BODY can be a file path (e.g., BODY="/tmp/pr_body.md")  
# Note: Nonexistent labels will be created automatically

# Dependencies
uv add package_name               # Add regular package  
uv add --dev package_name         # Add development package  
make sync                         # Sync all dependencies  
uv lock --upgrade                 # Upgrade dependencies
```

## Git Guidelines

**Branches**: feature/ | fix/ | refactor/ | docs/ | test/  
**Labels**: enhancement | bug | refactor | documentation | test

## Coding Conventions

Packages and tests should follow the structure under `template/`.  
Core logic must always be placed under `src/project_name`.

### Python Coding Style

- Type hints: Must use Python 3.12+ style (mypy strict + PEP 695)  
- Docstrings: NumPy style  
- Naming conventions:  
  - Classes: PascalCase  
  - Functions: snake_case  
  - Constants: UPPER_SNAKE  
  - Private members: _prefix  
- Best practices: See @template/src/template_package/types.py

### Error Messages

1. **Be specific**: "Invalid input" → "Expected positive integer, got {count}"  
2. **Include context**: "Failed to process {source_file}: {e}"  
3. **Suggest a solution**: "Not found. Create by: python -m {__package__}.init"

### Anchor Comments

```python
# AIDEV-NOTE: Explanation  
# AIDEV-TODO: Task  
# AIDEV-QUESTION: Question  
```

## Update Triggers

- When specifications, dependencies, structure, or conventions change  
- Same question asked more than twice → Add to FAQ  
- Same error pattern occurs more than twice → Add to Troubleshooting

## Troubleshooting / FAQ

Update as needed

## Custom Guides

Can be added under `docs/`.  
When added, a summary **must** be documented in CLAUDE.md.