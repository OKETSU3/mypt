# ✅ Demo Project Requirements (for Claude Code Python Template)

This document defines the requirements for the **Demo Project** bundled with the Claude Code Python Template.  
The project demonstrates best practices while implementing minimal functionality.

---

## 1. Purpose

- Provide a "working example" that users can run immediately after cloning or downloading the template.
- Demonstrate usage of TDD, type hints, logging, profiling, and CI workflows through actual code.
- Reduce the learning curve and prevent confusion right after template adoption.

---

## 2. Functional Requirements

### 2.1 Core Feature: `SimpleTextProcessor`

- **FR-1: Text Preprocessing**
  - Strip leading/trailing whitespace
  - Replace tabs with a single ASCII space

- **FR-2: Tokenization**
  - Tokenize input by splitting on whitespace (equivalent to `split()`)

- **FR-3: Word Count**
  - Return the number of words in the input string

- **FR-4: Word Frequency**
  - Provide a method `word_frequency(word)` that returns the occurrence count of a given word

### 2.2 CLI Interface

- **FR-5: Subcommand `count`**
  - Command: `python -m demo count "text here"`
  - Behavior: Outputs the word count

- **FR-6: Subcommand `freq`**
  - Command: `python -m demo freq "word" -t "text here"`
  - Behavior: Outputs the frequency of the specified word

---

## 3. Non-Functional Requirements

- **NFR-1: Quality**
  - Use `ruff format`, `ruff check`, and `mypy --strict`
  - Ensure 100% type coverage

- **NFR-2: Testing**
  - Unit tests for normal and error cases
  - Property-based tests using Hypothesis with random text
  - Code coverage must be ≥ 90%

- **NFR-3: Logging**
  - Log input size and result at INFO level
  - Log exceptions with full trace using `exc_info=True`

- **NFR-4: Profiling**
  - Use `@profile` decorator to measure `count_words()`

- **NFR-5: CLI UX**
  - Show help output per subcommand with `--help`

- **NFR-6: CI/CD**
  - GitHub Actions workflow (`ci.yml`) must run format → lint → type check → test

---

## 4. Source Layout

```
src/
└── demo/                  # ← Renamed to match project_name
    ├── __init__.py
    ├── core/
    │   └── text_processor.py
    ├── cli.py             # Entry point: python -m demo
    └── utils/
        └── logging_config.py
tests/
└── unit/
    └── test_text_processor.py
└── property/
    └── test_text_processor_prop.py
```

---

## 5. Development Flow

1. **Red**: Write failing unit test → run with `pytest -k`
2. **Green**: Implement minimal code to pass the test
3. **Refactor**: Add type hints, logs, rename as needed
4. **Property Test**: Verify generalizability
5. **Profiling & Optimization**: As needed

---

## 6. Out of Scope

- No database or network I/O
- No external API calls
- No GUI or web framework usage

---