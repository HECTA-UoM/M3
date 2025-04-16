from enum import Enum
from typing import List

from pydantic import BaseModel


class EntityType(str, Enum):
    """Enum for entity types."""

    ADE = "ADE"
    Dosage = "Dosage"
    Drug = "Drug"
    Duration = "Duration"
    Form = "Form"
    Frequency = "Frequency"
    Reason = "Reason"
    Route = "Route"
    Strength = "Strength"


class Entity(BaseModel):
    """
    Entity structure for NER predictions.
    Now includes optional character-level offsets.
    """

    text: str
    type: EntityType  # Entity type (e.g., ADE, Drug, etc.)
    word_start: int  # Index of the first word (word list dictionary key)
    word_end: int  # Index of the last word (inclusive)
    score: float
    char_start: int  # character-level start index
    char_end: int  # character-level end index


class NERResponse(BaseModel):
    """Structure for the complete NER response."""

    entities: List[Entity]


TAGS = {
    "ADE",
    "Dosage",
    "Drug",
    "Duration",
    "Form",
    "Frequency",
    "Reason",
    "Route",
    "Strength",
}
