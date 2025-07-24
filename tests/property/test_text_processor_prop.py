from collections import Counter

from hypothesis import given
from hypothesis import strategies as st

from demo import SimpleTextProcessor


class TestSimpleTextProcessorProperties:
    """Property-based tests for SimpleTextProcessor using Hypothesis."""

    @given(st.text())
    def test_token_count_equals_tokenize_length(self, text: str) -> None:
        """Property: len(tokenize()) == count_words() for any input."""
        processor = SimpleTextProcessor(text)
        tokens = processor.tokenize()
        count = processor.count_words()

        assert len(tokens) == count

    @given(st.text())
    def test_sum_of_frequencies_equals_count(self, text: str) -> None:
        """Property: sum of all word frequencies equals total word count."""
        processor = SimpleTextProcessor(text)
        tokens = processor.tokenize()
        count = processor.count_words()

        # Calculate sum of frequencies for all unique tokens
        if tokens:
            unique_tokens = set(tokens)
            frequency_sum = sum(
                processor.word_frequency(token) for token in unique_tokens
            )
            assert frequency_sum == count
        else:
            assert count == 0

    @given(st.text())
    def test_preprocess_is_idempotent(self, text: str) -> None:
        """Property: preprocessing is idempotent (applying twice gives same result)."""
        processor = SimpleTextProcessor(text)
        first_preprocess = processor.preprocess()

        # Create new processor with already preprocessed text
        processor2 = SimpleTextProcessor(first_preprocess)
        second_preprocess = processor2.preprocess()

        assert first_preprocess == second_preprocess

    @given(st.text(), st.text(min_size=1))
    def test_word_frequency_matches_manual_count(self, text: str, word: str) -> None:
        """Property: word_frequency matches manual count using Counter."""
        processor = SimpleTextProcessor(text)
        tokens = processor.tokenize()

        # Manual count using Counter
        counter = Counter(tokens)
        expected_frequency = counter[word]

        # Our implementation
        actual_frequency = processor.word_frequency(word)

        assert actual_frequency == expected_frequency

    @given(st.text())
    def test_empty_word_frequency_is_zero(self, text: str) -> None:
        """Property: frequency of empty string is always zero."""
        processor = SimpleTextProcessor(text)
        frequency = processor.word_frequency("")
        assert frequency == 0

    @given(st.text().filter(lambda x: x.strip()))  # Non-empty after stripping
    def test_nonempty_text_has_positive_count(self, text: str) -> None:
        """Property: non-empty text (after preprocessing) has positive word count."""
        processor = SimpleTextProcessor(text)
        preprocessed = processor.preprocess()

        if preprocessed:  # If still non-empty after preprocessing
            count = processor.count_words()
            assert count > 0
