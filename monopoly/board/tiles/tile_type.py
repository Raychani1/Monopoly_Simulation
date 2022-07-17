from enum import Enum, auto


class TileType(Enum):

    """Monopoly Board Tile Type."""

    GO = auto()
    PROPERTY = auto()
    COMMUNITY_CHEST = auto()
    TAX = auto()
    RAILROAD = auto()
    CHANCE = auto()
    JAIL = auto()
    UTILITY = auto()
    FREE_PARKING = auto()
    GO_TO_JAIL = auto()
    VISITING_JAIL = auto()
