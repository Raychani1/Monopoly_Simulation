from typing import List

from monopoly.deck.cards.card import Card
from monopoly.deck.cards.card_action_types import CardActionType


class MoneyCard(Card):

    """Monopoly Payment Card.

    Attributes:
        text (str): Card Text.
        payer (str): Payment payer.
        receiver (str): Payment receiver.
        amount (list): Payment amount.
    """

    def __init__(
        self,
        text: str,
        payer: str,
        receiver: str,
        amount: List[int]
    ) -> None:
        """Initialize the Money Card Class.

        Args:
            text (str): Card Text.
            payer (str): Payment payer.
            receiver (str): Payment receiver.
            amount (List[int]): Payment amount.
        """
        super().__init__(text, CardActionType.MONEY)
        self.__payer: str = payer
        self.__receiver: str = receiver
        self.__amount: List[int] = amount

    @property
    def payer(self) -> str:
        """Return Payment payer.

        Returns:
            str: Payment payer.
        """
        return self.__payer

    @property
    def receiver(self) -> str:
        """Return Payment receiver.

        Returns:
            str: Payment receiver.
        """
        return self.__receiver

    @property
    def amount(self) -> List[int]:
        """Return Payment amount.

        Returns:
            List[int]: Payment amount.
        """
        return self.__amount

    def __str__(self) -> str:
        """Make Payment Card displayable.

        Returns:
            str: Payment Card String representation.
        """
        return super().__str__()
