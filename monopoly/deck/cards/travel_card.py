from monopoly.deck.cards.card import Card
from monopoly.deck.cards.card_action_types import CardActionType


class TravelCard(Card):

    """Monopoly Travel Card.

    Attributes:
        text (str): Card Text.
        destination (str): Travel destination.
    """

    def __init__(self, text: str, destination: str) -> None:
        """Initialize the Travel Card Class.

        Args:
            text (str): Card Text.
            destination (str): Travel destination.
        """
        super().__init__(text, CardActionType.TRAVEL)
        self.__destination = destination

    @property
    def destination(self) -> str:
        """Return Travel destination.

        Returns:
            str: Travel destination.
        """
        return self.__destination

    def __str__(self) -> str:
        """Make Travel Card displayable.

        Returns:
            str: Travel Card String representation.
        """
        return super().__str__()
