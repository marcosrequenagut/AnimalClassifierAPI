from enum import Enum

from pydantic import BaseModel, Field


class AnimalClassification(str, Enum):
    KANGAROO = "kangaroo"
    ELEPHANT = "elephant"
    CHICKEN = "chicken"
    DOG = "dog"


class AnimalCharacteristics(BaseModel):
    walks_on_n_legs: int = Field(
        title="Walks on 'n' legs",
        description="The number of legs the animal walks on",
    )
    height: float = Field(
        title="Height",
        description="The height of the animal in meters",
    )
    weight: float = Field(
        title="Weight", description="The weight of the animal in kilograms"
    )
    has_wings: bool = Field(
        title="Has wings?", description="Whether the animal has wings"
    )
    has_tail: bool = Field(
        title="Has tail?", description="Whether the animal has a tail"
    )
