import pytest

from demo import SimpleTextProcessor


class TestSimpleTextProcessor:
    """Unit tests for SimpleTextProcessor following TDD principles."""

    def test_preprocess_trims_whitespace_and_converts_tabs(self) -> None:
        """UT-1: Trim & tab collapse - strips whitespace and converts tabs to spaces."""
        processor = SimpleTextProcessor("\tHello \n")
        result = processor.preprocess()
        assert result == "Hello"

    def test_preprocess_converts_multiple_tabs_to_single_space(self) -> None:
        """Additional test for tab handling."""
        processor = SimpleTextProcessor("Hello\t\tworld")
        result = processor.preprocess()
        assert result == "Hello world"

    def test_tokenize_splits_on_whitespace(self) -> None:
        """UT-2: Tokenization basic - splits text on whitespace."""
        processor = SimpleTextProcessor("a  b\tc")
        result = processor.tokenize()
        assert result == ["a", "b", "c"]

    def test_tokenize_handles_empty_string(self) -> None:
        """Edge case: tokenizing empty string should return empty list."""
        processor = SimpleTextProcessor("")
        result = processor.tokenize()
        assert result == []

    def test_count_words_returns_token_count(self) -> None:
        """UT-3: Word count - returns number of tokens."""
        processor = SimpleTextProcessor("a a b")
        result = processor.count_words()
        assert result == 3

    def test_count_words_empty_string_returns_zero(self) -> None:
        """UT-6: Empty string edge case - count_words should return 0."""
        processor = SimpleTextProcessor("")
        result = processor.count_words()
        assert result == 0

    def test_word_frequency_returns_count_for_present_word(self) -> None:
        """UT-4: Frequency present - returns count of word in text."""
        processor = SimpleTextProcessor("spam spam eggs")
        result = processor.word_frequency("spam")
        assert result == 2

    def test_word_frequency_returns_zero_for_absent_word(self) -> None:
        """UT-5: Frequency absent - returns 0 for word not in text."""
        processor = SimpleTextProcessor("spam spam eggs")
        result = processor.word_frequency("ham")
        assert result == 0

    def test_word_frequency_is_case_sensitive(self) -> None:
        """Additional test: word frequency should be case-sensitive."""
        processor = SimpleTextProcessor("Hello hello HELLO")
        assert processor.word_frequency("hello") == 1
        assert processor.word_frequency("Hello") == 1
        assert processor.word_frequency("HELLO") == 1

    def test_word_frequency_raises_type_error_for_non_string(self) -> None:
        """Error case: word_frequency should raise TypeError for non-string input."""
        processor = SimpleTextProcessor("hello world")
        with pytest.raises(TypeError, match="Expected str, got NoneType"):
            processor.word_frequency(None)  # type: ignore[arg-type]
