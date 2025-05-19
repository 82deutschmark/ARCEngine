"""
Module containing enums used throughout the ARCEngine.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Any, Optional, Type, Union

from numpy import ndarray
from pydantic import BaseModel, Field


class BlockingMode(Enum):
    """Enum defining different collision detection behaviors for sprites."""

    NOT_BLOCKED = auto()  # No collision detection
    BOUNDING_BOX = auto()  # Simple rectangular collision detection
    PIXEL_PERFECT = auto()  # Precise pixel-level collision detection


class InteractionMode(Enum):
    """Enum defining how a sprite interacts with the game world visually and physically."""

    TANGIBLE = auto()  # Visible and can be collided with
    INTANGIBLE = auto()  # Visible but cannot be collided with (ghost-like)
    INVISIBLE = auto()  # Not visible but can be collided with (invisible wall)
    REMOVED = auto()  # Not visible and cannot be collided with (effectively removed)


class GameState(str, Enum):
    NOT_PLAYED = "NOT_PLAYED"
    NOT_FINISHED = "NOT_FINISHED"
    WIN = "WIN"
    GAME_OVER = "GAME_OVER"


class SimpleAction(BaseModel):
    game_id: str = ""


class ComplexAction(BaseModel):
    game_id: str = ""
    x: int = Field(0, ge=0, le=63)
    y: int = Field(0, ge=0, le=63)


class GameAction(Enum):
    RESET = (0, SimpleAction)
    ACTION1 = (1, SimpleAction)
    ACTION2 = (2, SimpleAction)
    ACTION3 = (3, SimpleAction)
    ACTION4 = (4, SimpleAction)
    ACTION5 = (5, SimpleAction)
    ACTION6 = (6, ComplexAction)

    action_type: Union[Type[SimpleAction], Type[ComplexAction]]
    action_data: Union[SimpleAction | ComplexAction]

    def __init__(
        self,
        action_id: int,
        action_type: Union[Type[SimpleAction], Type[ComplexAction]],
    ) -> None:
        self._value_ = action_id
        self.action_type = action_type
        self.action_data = action_type()

    def is_simple(self) -> bool:
        return self.action_type is SimpleAction

    def is_complex(self) -> bool:
        return self.action_type is ComplexAction

    def validate_data(self, data: dict[str, Any]) -> bool:
        """Raise exception on invalid parse of incoming JSON data."""
        self.action_type.model_validate(data)
        return True

    def set_data(self, data: dict[str, Any]) -> Union[SimpleAction | ComplexAction]:
        self.action_data = self.action_type(**data)
        return self.action_data

    @classmethod
    def from_id(cls, action_id: int) -> GameAction:
        for action in cls:
            if action.value == action_id:
                return action
        raise ValueError(f"No GameAction with id {action_id}")

    @classmethod
    def from_name(cls, name: str) -> "GameAction":
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(f"No GameAction with name '{name}'")

    @classmethod
    def all_simple(cls) -> list[GameAction]:
        return [a for a in cls if a.is_simple()]

    @classmethod
    def all_complex(cls) -> list[GameAction]:
        return [a for a in cls if a.is_complex()]


class ActionInput(BaseModel):
    id: GameAction = GameAction.RESET
    data: dict[str, Any] = {}


class FrameData(BaseModel):
    game_id: str = ""
    frame: list[list[list[int]]] = []
    state: GameState = GameState.NOT_PLAYED
    score: int = Field(0, ge=0, le=254)
    action_input: ActionInput = Field(default_factory=lambda: ActionInput())
    guid: Optional[str] = None

    def is_empty(self) -> bool:
        return len(self.frame) == 0


class FrameDataRaw:
    game_id: str = ""
    frame: list[ndarray] = []
    state: GameState = GameState.NOT_PLAYED
    score: int = 0
    action_input: ActionInput = Field(default_factory=lambda: ActionInput())
    guid: Optional[str] = None

    def is_empty(self) -> bool:
        return len(self.frame) == 0
