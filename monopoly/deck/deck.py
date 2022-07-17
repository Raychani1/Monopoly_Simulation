from random import shuffle
from typing import List

from monopoly.deck.cards.card import Card
from monopoly.deck.cards.card_action_types import CardActionType
from monopoly.deck.cards.money_card import MoneyCard
from monopoly.deck.cards.travel_card import TravelCard


class Deck:

    """Monopoly Card Deck.

    Attributes:
        cards (List[Card]): Cards in Deck.
        discard_pile (List[Card]): Discarded Cards from Deck.
    """

    __cards: List[Card] = []
    __discard_pile: List[Card] = []

    def __init__(self, file: str) -> None:
        """Initialize the Deck Class.

        Args:
            file (str): Input Data File Path.
        """
        self.__set_up_deck(file)

    @property
    def cards(self) -> List[Card]:
        """Return Cards in Deck.

        Returns:
            List[Card]: Cards in Deck.
        """
        return self.__cards

    @staticmethod
    def __read_input_data(file: str) -> List[str]:
        """Load Card Data from Input File.

        Args:
            file (str): Input Data File Path.

        Returns:
            List[str]: Loaded Data.
        """
        with open(file) as f:
            content = f.readlines()

        return list(x.strip().split(';') for x in content)

    @staticmethod
    def __create_card(card: List[str]) -> Card:
        """Create Card from Card Data.

        Args:
            card (List[str]): Card Data.

        Returns:
            Card: Created Card.
        """
        card_data_length = len(card)

        if card_data_length == 2:
            return Card(card[0], CardActionType.GET_OUT_OF_JAIL)

        elif card_data_length == 3:
            return TravelCard(card[0], card[2])

        elif card_data_length > 4:
            return MoneyCard(
                card[0],
                card[2],
                card[3],
                [int(item) for item in card[4:]]
            )

    def __set_up_deck(self, file: str) -> None:
        """Set up Deck.

        Args:
            file (str): Input Data File Path.
        """
        for item in self.__read_input_data(file):
            self.__cards.append(self.__create_card(item))

        shuffle(self.__cards)

    def draw_card(self) -> Card:
        """Draw Card from Deck.

        Returns:
            Card: Drawn Card.
        """
        drawn_card = self.__cards.pop(0)
        self.__discard_pile.append(drawn_card)

        # When there are no Cards to draw
        if len(self.__cards) == 0:
            self.__cards.extend(self.__discard_pile)
            shuffle(self.__cards)

        return drawn_card
