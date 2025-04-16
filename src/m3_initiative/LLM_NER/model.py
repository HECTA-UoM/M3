import json
import os
import re
from typing import Dict, List, Optional, Tuple

from ollama import Client, Options

from .data_structure import Entity, NERResponse
from .prompt_manager import PromptManager


class OllamaNER:
    """
    Named Entity Recognition using Ollama models.

    This class sends text to an Ollama endpoint, receives JSON-based entity predictions,
    and converts those predictions into Label Studio's annotation format.
    It now uses a word list provided as a dictionary mapping each word index to a triple:
      {
         word_index: (word_text, start_char_index, end_char_index),
         ...
      }
    This additional context should help the model make more accurate index predictions.
    """

    def __init__(self, host: str):
        super().__init__()
        # Initialize Ollama client
        self.client = Client(host=host)

        # Create a singleton instance
        prompt_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "prompts_json"
        )
        self.prompts = PromptManager(prompt_dir=prompt_dir)  # type: ignore
        self.default_prompt = self.prompts.get_prompt("default")

    def _split_into_words(self, text: str) -> Dict[int, Tuple[str, int, int]]:
        """
        Split text into words and track their character positions.

        Returns:
            A dictionary where each key is a word index and the value is a tuple:
              (word_text, start_char_index, end_char_index)
        """
        words = {}
        pattern = r"\b[A-Za-z0-9]+(?:[-./'][A-Za-z0-9]+)*\b"
        for idx, match in enumerate(re.finditer(pattern, text)):
            words[idx] = (match.group(), match.start(), match.end())
        return words

    @staticmethod
    def construct_from_tokens(
        tokens: List[str],
    ) -> Tuple[str, Dict[int, Tuple[str, int, int]]]:
        """
        Construct a string from tokens and create a mapping of word indices to character positions.
        """
        char_index = 0
        words_list = {}
        text = ""
        for ix, token in enumerate(tokens):
            words_list[ix] = (token, char_index, char_index + len(token))
            char_index += len(token) + 1
            text += f"{token} "
        text = text.strip()
        return (text, words_list)

    def adjust_indices(
        self,
        original_text: str,
        predicted_text: str,
        fallback_start: int,
        fallback_end: int,
    ) -> Tuple[int, int]:
        """
        Adjust the predicted character indices to align with the LLM-predicted text.

        This function searches for the predicted_text within original_text and, if found,
        returns the occurrence whose start index is closest to fallback_start.
        If the predicted text is not found, it returns the fallback indices.

        Args:
            original_text (str): The full original text.
            predicted_text (str): The entity text predicted by the LLM.
            fallback_start (int): The original start index (from word indices or LLM prediction).
            fallback_end (int): The original end index.

        Returns:
            A tuple (new_start, new_end) that aligns with the predicted text.
        """
        # Normalize the predicted text for matching (strip whitespace)
        norm_predicted = predicted_text.strip()
        if not norm_predicted:
            return fallback_start, fallback_end

        # Find all occurrences of predicted_text in the original text
        matches = list(re.finditer(re.escape(norm_predicted), original_text))
        if not matches:
            # If no exact match is found, fallback to the original indices.
            return fallback_start, fallback_end

        # Select the occurrence whose start is closest to the fallback_start.
        best_match = min(matches, key=lambda m: abs(m.start() - fallback_start))
        return best_match.start(), best_match.end()

    def _validate_entity(
        self, text: str, entity: Entity, words: Dict[int, Tuple[str, int, int]]
    ) -> Optional[Dict]:
        """
        Convert an NER entity (with word indices and optionally character indices)
        to Label Studio's format with character-level offsets.

        If the entity contains char_start and char_end, they are used directly.
        Otherwise, they are derived from the word indices using the provided words dictionary.

        Args:
            text (str): The original text.
            entity (Entity): The predicted entity.
            words (Dict[int, Tuple[str, int, int]]): Dictionary mapping word indices to triples.

        Returns:
            A dictionary in Label Studio format or None if validation fails.
        """
        try:
            # Validate word indices first
            if (
                entity.word_start < 0
                or entity.word_end not in words
                or entity.word_start > entity.word_end
            ):
                return None

            # Derive character positions from the words dictionary
            char_start = words[entity.word_start][1]
            char_end = words[entity.word_end][2]

            # Use the predicted text (assumed more correct) from the LLM.
            predicted_text = entity.text.strip()
            # Slice the original text using the current indices.
            sliced_text = text[char_start:char_end].strip()

            # If the sliced text doesn't match the predicted text, adjust the indices.
            if sliced_text != predicted_text:
                new_start, new_end = self.adjust_indices(
                    text, predicted_text, char_start, char_end
                )
                char_start, char_end = new_start, new_end

            # Extract the actual text using character offsets
            actual_text = text[char_start:char_end]

            return {
                "value": {
                    "start": char_start,
                    "end": char_end,
                    "char_start": entity.char_start,
                    "char_end": entity.char_end,
                    "word_start": entity.word_start,
                    "word_end": entity.word_end,
                    "text": actual_text,
                    "predicted_text": entity.text,
                    "labels": [entity.type],
                },
                "score": entity.score,
            }
        except Exception as e:
            print(f"Error transforming entity: {str(e)}")
            return None

    def predict(
        self,
        tokens: List[str],
        model_name: str,
        prompt_name: Optional[str] = None,
        temperature: float = 0.0,
        top_k: int = 40,
        top_p: float = 0.9,
    ) -> Dict:
        """
        Make predictions using the Ollama model for one or multiple input texts.

        The prompt now receives a word list as a dictionary mapping each word index
        to a tuple (word_text, start_char_index, end_char_index) for better context.

        Args:
            texts (Union[List[str], str]): A string or list of strings to process.
            model_name (str): The Ollama model identifier.
            temperature (float): Sampling temperature.
            top_k (int): The top_k parameter.
            top_p (float): The top_p parameter.

        Returns:
            A list of predictions with Label Studio formatted results and average score.
        """

        if prompt_name is None:
            prompt_name = "default"

        options = Options(temperature=temperature, top_k=top_k, top_p=top_p)

        # Create a dictionary of words with indices and character offsets.
        text, words_dict = self.construct_from_tokens(tokens)

        # For the prompt, provide the dictionary (keys will be serialized as strings).
        messages = self.prompts.format_prompt(
            prompt_name=prompt_name, text=text, word_list=json.dumps(words_dict)
        )

        try:
            # Call the Ollama endpoint with the prompt
            response = self.client.chat(
                model=model_name,
                messages=messages,
                options=options,
                format=NERResponse.model_json_schema(),
            )

            # Parse the JSON response into our NERResponse schema.
            ner_response = NERResponse.model_validate_json(response.message.content)

            results = []
            total_score = 0.0

            for entity in ner_response.entities:
                transformed = self._validate_entity(text, entity, words_dict)
                if transformed is None:
                    continue
                results.append(transformed)
                total_score += transformed["score"]

            avg_score = total_score / len(results) if results else 0.0

            return {
                "text": text,
                "result": results,
                "score": avg_score,
            }

        except Exception as e:
            print(f"Error making prediction: {str(e)}")
            return {"result": [], "score": 0.0}


if __name__ == "__main__":

    # Replace with your actual Ollama server URL
    host = "http://localhost:11434"
    ner_model = OllamaNER(host=host)

    test_tokens = [
        "Patient",
        "developed",
        "a",
        "rash",
        "after",
        "taking",
        "amoxicillin",
    ]

    model_name = "llama3.1:latest"

    result = ner_model.predict(
        test_tokens,
        model_name=model_name,
        prompt_name="default",
        temperature=0.0,
        top_k=40,
        top_p=0.8,
    )

    print(json.dumps(result, indent=2))
