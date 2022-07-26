from abc import ABC

from monopoly.deck.cards.card_action_types import CardActionType


class Card(ABC):

    """Monopoly Card.

    Attributes:
        text (str): Card Text.
        card_type (CardActionType): Card Action Type.
    """

    def __init__(self, text: str, card_type: CardActionType) -> None:
        """Initialize the Card Abstract Class.

        Args:
            text (str): Card Text.
            card_type (CardActionType): Card Action Type.
        """
        self.__text: str = text
        self.__card_type: CardActionType = card_type

    @property
    def text(self) -> str:
        """Return Card Text.

        Returns:
            str: Card Text.
        """
        return self.__text

    @property
    def card_type(self) -> str:
        """Return Card Action Type.

        Returns:
            str: Card Action Type.
        """
        return self.__card_type

    def __str__(self) -> str:
        """Make Card displayable.

        Returns:
            str: Card String representation.
        """
        return self.__text
