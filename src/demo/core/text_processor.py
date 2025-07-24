import re

from ..utils.logging_config import get_logger
from ..utils.profiling import profile

logger = get_logger(__name__)


class SimpleTextProcessor:
    """Simple text processing utility for demonstrating TDD best practices."""

    def __init__(self, text: str) -> None:
        """Initialize processor with raw text.

        Args:
            text: Raw input text to process
        """
        self.text = text
        logger.info("SimpleTextProcessor initialized", text_length=len(text))

    def preprocess(self) -> str:
        """Preprocess text by stripping whitespace and converting tabs to spaces.

        Returns:
            Preprocessed text
        """
        try:
            # Strip leading/trailing whitespace
            result = self.text.strip()

            # Convert tabs to single spaces
            result = re.sub(r"\t+", " ", result)

            logger.info(
                "Text preprocessed",
                original_length=len(self.text),
                processed_length=len(result),
            )

            return result

        except Exception as e:
            logger.exception("Error during text preprocessing", error=str(e))
            raise

    def tokenize(self) -> list[str]:
        """Tokenize preprocessed text by splitting on whitespace.

        Returns:
            List of tokens (words)
        """
        try:
            # First preprocess the text
            preprocessed = self.preprocess()

            # Handle empty string case
            if not preprocessed:
                logger.info("Tokenized empty text", token_count=0)
                return []

            # Split on one or more whitespace characters
            tokens = re.split(r"\s+", preprocessed)

            logger.info(
                "Text tokenized",
                token_count=len(tokens),
                sample_tokens=tokens[:3] if len(tokens) > 0 else [],
            )

            return tokens

        except Exception as e:
            logger.exception("Error during tokenization", error=str(e))
            raise

    @profile
    def count_words(self) -> int:
        """Count the number of words in the text.

        Returns:
            Number of words (tokens) in the text
        """
        try:
            tokens = self.tokenize()
            count = len(tokens)

            logger.info(
                "Word count completed", word_count=count, input_length=len(self.text)
            )

            return count

        except Exception as e:
            logger.exception("Error during word counting", error=str(e))
            raise

    def word_frequency(self, word: str) -> int:
        """Count the frequency of a specific word in the text.

        Args:
            word: The word to count (case-sensitive)

        Returns:
            Number of times the word appears in the text

        Raises:
            TypeError: If word is not a string
        """
        try:
            if not isinstance(word, str):
                raise TypeError(f"Expected str, got {type(word).__name__}")

            tokens = self.tokenize()
            frequency = tokens.count(word)

            logger.info(
                "Word frequency calculated",
                word=word,
                frequency=frequency,
                total_tokens=len(tokens),
            )

            return frequency

        except Exception as e:
            logger.exception(
                "Error during word frequency calculation", error=str(e), word=word
            )
            raise
