import dataclasses
import json
from pathlib import Path
from typing import Any, Dict


@dataclasses.dataclass
class PromptManager:
    prompt_dir: Path
    _prompts: Dict[str, Any] = dataclasses.field(default_factory=dict)
    _loaded: bool = False

    def __post_init__(self):
        self.prompt_dir = Path(self.prompt_dir)

    def load_prompts(self) -> None:
        """Load all prompts from the prompt directory."""
        if not self.prompt_dir.exists():
            raise FileNotFoundError(f"Prompt directory not found: {self.prompt_dir}")

        # Load JSON prompts
        for file_path in self.prompt_dir.glob("*.json"):
            prompt_name = file_path.stem
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self._prompts[prompt_name] = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON in file: {file_path}")

        # Load text prompts
        for file_path in self.prompt_dir.glob("*.txt"):
            prompt_name = file_path.stem
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self._prompts[prompt_name] = f.read()
            except Exception as e:
                print(f"Warning: Error reading text file: {file_path}, {str(e)}")

        self._loaded = True

    def get_prompt(self, prompt_name: str) -> Any:
        """Get a prompt by its name."""
        if not self._loaded:
            self.load_prompts()

        if prompt_name not in self._prompts:
            raise KeyError(f"Prompt not found: {prompt_name}")

        return self._prompts[prompt_name]

    def format_prompt(self, prompt_name: str, **kwargs) -> Any:
        """Get a prompt by its name and format it with the provided variables."""
        prompt = self.get_prompt(prompt_name)

        if isinstance(prompt, str):
            # Format string prompts
            return prompt.format(**kwargs)
        elif isinstance(prompt, list):
            # Format chat prompts (list of message dicts)
            formatted_prompt = []
            for message in prompt:
                if (
                    isinstance(message, dict)
                    and "content" in message
                    and isinstance(message["content"], str)
                ):
                    formatted_message = message.copy()
                    formatted_message["content"] = message["content"].format(**kwargs)
                    formatted_prompt.append(formatted_message)
                else:
                    formatted_prompt.append(message)
            return formatted_prompt
        elif isinstance(prompt, dict):
            # Format dictionary prompts recursively
            def format_dict(d, **kwargs):
                result = {}
                for k, v in d.items():
                    if isinstance(v, str):
                        result[k] = v.format(**kwargs)
                    elif isinstance(v, dict):
                        result[k] = format_dict(v, **kwargs)
                    elif isinstance(v, list):
                        result[k] = [
                            (
                                format_dict(item, **kwargs)
                                if isinstance(item, dict)
                                else (
                                    item.format(**kwargs)
                                    if isinstance(item, str)
                                    else item
                                )
                            )
                            for item in v
                        ]
                    else:
                        result[k] = v
                return result

            return format_dict(prompt, **kwargs)
        else:
            return prompt

    def __getattr__(self, name: str) -> Any:
        """Allow accessing prompts as attributes (e.g., Prompts.default)."""
        try:
            return self.get_prompt(name)
        except KeyError:
            raise AttributeError(f"No prompt found with name: {name}")
