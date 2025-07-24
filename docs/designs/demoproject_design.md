# 📝 Demo Project — API & Test Specification

This document defines the **public API** for the demo project and the **test specifications** that guarantee the functional and non-functional requirements stated earlier.

---

## 1. Public API Design

### 1.1 `demo.core.text_processor.SimpleTextProcessor`

* **Constructor**

  * Signature: `SimpleTextProcessor(text: str)`
  * Description: Store raw text. No heavy work.

* **`preprocess`**

  * Signature: `-> str`
  * Description:

    * Strip leading/trailing whitespace
    * Convert tabs to single space
    * Returns preprocessed string

* **`tokenize`**

  * Signature: `-> list[str]`
  * Description:

    * Split on one or more ASCII whitespace characters using `re.split(r"\s+")` after `preprocess()`

* **`count_words`**

  * Signature: `-> int`
  * Description:

    * Return the number of resulting tokens

* **`word_frequency`**

  * Signature: `word: str -> int`
  * Description:

    * Case-sensitive count of `word` in token list
    * Returns `0` if absent

* **Logging**

  * Uses `structlog.get_logger(__name__)`
  * `.info()` on successful `preprocess` and `count_words`
  * `.exception()` on unexpected errors

* **Profiling**

  * `@profile` decorator (noop in prod) on `count_words`

---

### 1.2 Command-Line Interface (`demo.cli`)

* **Command: `count`**

  * Example: `python -m demo count "Hello world"`
  * Behaviour: Prints `2` (word count)

* **Command: `freq`**

  * Example: `python -m demo freq "world" -t "hello world world"`
  * Behaviour: Prints `2`

* **Flags**

  * `-t/--text` (string)
  * `--file` (path, exclusive with `--text`)

* **Implementation**

  * Uses `argparse` sub-commands mapping to `SimpleTextProcessor` calls

---

### 1.3 Package Exports (`demo/__init__.py`)

```python
from .core.text_processor import SimpleTextProcessor

__all__ = ["SimpleTextProcessor"]
```

---

## 2. Test Specification

### 2.1 Unit Tests (`tests/unit/test_text_processor.py`)

* **UT-1: Trim & tab collapse**

  * Input: `SimpleTextProcessor("\tHello \n")`→`preprocess()`
  * Expected: `"Hello"`

* **UT-2: Tokenization basic**

  * Input: Text `"a  b\tc"`
  * Expected: `["a", "b", "c"]`

* **UT-3: Word count**

  * Input: `"a a b"`
  * Expected: `count_words()` → `3`

* **UT-4: Frequency present**

  * Input: `"spam spam eggs"` & `word_frequency("spam")`
  * Expected: `2`

* **UT-5: Frequency absent**

  * Input: Same text, `word_frequency("ham")`
  * Expected: `0`

* **UT-6: Empty string edge**

  * Input: `""`
  * Expected: `count_words()` → `0`, empty token list

---

### 2.2 CLI Tests (`tests/unit/test_cli.py`)

* **Scenario: `count` basic**

  * Command: `python -m demo count "a b"`
  * Exit Code: `0`
  * STDOUT: `2`

* **Scenario: `freq` basic**

  * Command: `python -m demo freq "b" -t "a b b"`
  * Exit Code: `0`
  * STDOUT: `2`

---

### 2.3 Property-Based Tests (`tests/property/test_text_processor_prop.py`)

* **Property: Token concat invariant**

  * Hypothesis Strategy: `st.text()` (any unicode)
  * Assertion: `len(proc.tokenize()) == proc.count_words()`

* **Property: Sum of frequencies = count**

  * Hypothesis Strategy: Same string
  * Assertion: `sum(Counter(tokens).values()) == count_words()`

* **Property: Idempotent preprocess**

  * Hypothesis Strategy: Any text
  * Assertion: `proc.preprocess() == SimpleTextProcessor(proc.preprocess()).preprocess()`

---

### 2.4 Coverage Target

* Global statement coverage ≥ **90%**

  * Command: `pytest --cov=demo --cov-fail-under=90`

---

### 2.5 Negative / Error Paths

* `word_frequency(None)` → `TypeError`
* CLI invoked with both `--text` and `--file` → exit 1 + help message

---

## 3. CI / Pre-commit Integration

### 3.1 pre-commit

* `ruff format --check`
* `ruff check`
* `mypy --strict`
* `pytest -q`

### 3.2 GitHub Actions `ci.yml`

* 同上のステップ
* 追加で `pytest --cov` 実行

---