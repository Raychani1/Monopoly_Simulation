from enum import Enum, auto


class CardActionType(Enum):

    """Monopoly Card Action Type."""

    GET_OUT_OF_JAIL = auto()
    MONEY = auto()
    TRAVEL = auto()
