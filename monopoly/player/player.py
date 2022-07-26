from typing import Dict, List, Tuple

import pandas as pd
from numpy.random import randint
from termcolor import colored

from monopoly.board.board import Board
from monopoly.board.tiles.tile_type import TileType
from monopoly.deck.cards.card import Card
from monopoly.deck.cards.card_action_types import CardActionType
from monopoly.deck.deck import Deck


class Player:

    """Monopoly Player.

    Attributes:
        current_position (int): Players current position (Tile index).
        crossed_go_tile (int): Number of times player crossed the 'GO' Tile.
        roll_history (List[int]): Rolled numbers during the simulation.
    """

    def __init__(self) -> None:
        """Initialize the Player Class."""
        self.__current_position: int = 0
        self.__doubles: int = 0
        self.__jail_time: int = 3
        self.__crossed_go_tile: int = 0
        self.__inventory: List[Tuple(Card, Deck)] = []
        self.__roll_history: List[int] = []

    @property
    def current_position(self) -> int:
        """Return the current position of the Player.

        Returns:
            int: Current Player Position.
        """
        return self.__current_position

    @property
    def crossed_go_tile(self) -> int:
        """Return how many times did the Player cross the GO tile.

        Returns:
            int: Number of GO tile crossing.
        """
        return self.__crossed_go_tile

    @property
    def roll_history(self) -> int:
        """Return players roll history.

        Returns:
            List[int]: Players roll history.
        """
        return self.__roll_history

    def __add_card_to_inventory(self, card: Card, deck: Deck) -> None:
        """Add Card to Player inventory.

        Args:
            card (Card): Drawn Card to Inventory.
            deck (Deck): Deck from which the Card was drawn.
        """
        self.__inventory.append((card, deck))

    def __discard_card_from_inventory(self) -> None:
        """Discard Card from Inventory to Discard Pile."""
        discard: Tuple[Card, Deck] = self.__inventory.pop()

        discard[1].discard_card(discard[0])

    def __roll_the_dice(self) -> int:
        """Simulate dice roll.

        Returns:
            int: Sum of rolled numbers.
        """
        rolled = randint(1, 7, 2)

        if rolled[0] == rolled[1]:
            print(colored(f'Double roll: {(rolled[0], rolled[1])}', 'yellow'))
            self.__doubles += 1

        else:
            if self.__doubles == 3:
                self.__doubles = 0
                self.__go_to_jail('3 double rolls')
                return 0
            else:
                self.__doubles = 0

        result: int = sum(rolled)

        self.__roll_history.append(result)

        return result

    def __go_to_jail(self, reason: str) -> None:
        """Display go to Jail message with description.

        Args:
            reason (str): Reason for description.
        """
        print(
            colored(
                f'\n--------- Going to jail for {reason} ---------\n',
                'red'
            )
        )
        self.__current_position = 10

    def __find_nearest_special_tile(self, tiles: List[int]) -> int:
        """Find nearest Special Tile.

        Args:
            tiles (List[int]): List of Special Tile indices.

        Returns:
            int: Nearest Special Tile index.
        """
        # Indices of Special Tiles after players current position
        next_special_tiles: List[int] = [
            tile for tile in tiles if tile > self.__current_position
        ]

        nearest_special_tile: int = 0

        # Found indices after current position
        if next_special_tiles:
            nearest_special_tile = next_special_tiles[0]

        # Nearest index only in the next round
        else:
            nearest_special_tile = tiles[0]

        return nearest_special_tile

    def __execute_travel_card_action(
        self,
        drawn_card: Card,
        board: Board,
        stats: Dict[str, int],
        round_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Execute Travel Card Action.

        Args:
            board (Board): Monopoly Board.
            deck (Deck): Monopoly Card Deck.
            card_type (str): Card Type.
            stats (Dict[str, int]): Statistics data.            
            round_data (pd.DataFrame): Round Visit Data.

        Returns:
            pd.DataFrame: Updated Round Visit Data.
        """
        destination = drawn_card.destination

        if destination == '3 Spaces':
            self.__current_position -= 3

            if self.__current_position == 31:
                stats[board.tiles[self.__current_position].label] += 1
                self.__go_to_jail('stepping on Go To Jail tile')

        else:
            new_position: int = 0

            if destination in ['Utility', 'Railroad']:
                new_position = self.__find_nearest_special_tile(
                    board.utilities if destination == 'Utility' else board.railroads
                )

            else:
                new_position = board.map[destination]

            if self.__current_position > new_position \
                    and destination != 'Jail':
                round_data = pd.concat(
                    [
                        round_data,
                        pd.Series(stats).rename(f'Round {self.__crossed_go_tile}')
                    ],
                    axis=1
                )
                self.__crossed_go_tile += 1

            self.__current_position = new_position

        stats[board.tiles[self.__current_position].label] += 1

        return round_data

    def __execute_card_action(
        self,
        board: Board,
        deck: Deck,
        card_type: str,
        stats: Dict[str, int],
        round_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Execute Card Action.

        Args:
            board (Board): Monopoly Board.
            deck (Deck): Monopoly Card Deck.
            card_type (str): Card Type.
            stats (Dict[str, int]): Statistics data.
            round_data (pd.DataFrame): Round Visit Data.

        Returns:
            pd.DataFrame: Updated Round Visit Data.
        """
        drawn_card: Card = deck.draw_card()

        print(
            colored(
                f'\n[{card_type}] - {drawn_card}\n',
                'cyan' if card_type == 'Chance' else 'blue'
            )
        )

        if drawn_card.card_type == CardActionType.TRAVEL:
            round_data = self.__execute_travel_card_action(
                drawn_card=drawn_card,
                board=board,
                stats=stats,
                round_data=round_data
            )
        elif drawn_card.card_type == CardActionType.GET_OUT_OF_JAIL:
            self.__add_card_to_inventory(card=drawn_card, deck=deck)

        return round_data

    def __display_move(self, increment: int, board: Board) -> None:
        """Display basic stats of movement.

        Args:
            increment (int): Position increment.
            board (Board): Monopoly Board.
        """
        tile = board.tiles[self.__current_position]

        print(
            f'Current tile: {[tile.label]} - {tile.name}, Rolled: {increment},'
            f' Crossed GO: {self.__crossed_go_tile}x'
        )

    def __regular_round(
            self,
            increment: int,
            board: Board,
            chances: Deck,
            community_chests: Deck,
            stats: Dict[str, int],
            round_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Execute Regular round.

        Args:
            increment (int): Position increment.
            board (Board): Monopoly Board.
            chances (Deck): Chance Cards Deck.
            community_chests (Deck): Community Chest Cards Deck.
            stats (Dict[str, int]): Statistics data.
            round_data (pd.DataFrame): Round Visit Data.

        Returns:
            pd.DataFrame: Updated Round Visit Data.
        """
        board_length = len(board.tiles)

        # Update stats
        self.__display_move(increment, board)
        self.__current_position += increment

        # Crossed 'GO' Tile
        if self.__current_position >= board_length:
            round_data = pd.concat(
                [
                    round_data,
                    pd.Series(stats).rename(f'Round {self.__crossed_go_tile}')
                ],
                axis=1
            )
            self.__crossed_go_tile += 1
            self.__current_position %= board_length

        # 'Just Visiting Jail' Tile
        if self.__current_position == 10:
            self.__current_position += 1

        # 'Go To Jail' Tile
        if self.__current_position == 31:
            stats[board.tiles[self.__current_position].label] += 1
            self.__go_to_jail('stepping on Go To Jail tile')

        stats[board.tiles[self.__current_position].label] += 1

        tile_type: TileType = board.tiles[self.__current_position].tile_type

        # Draw Card
        if tile_type in [TileType.CHANCE, TileType.COMMUNITY_CHEST]:
            if tile_type == TileType.CHANCE:
                round_data = self.__execute_card_action(
                    board=board, 
                    deck=chances, 
                    card_type='Chance', 
                    stats=stats,
                    round_data=round_data
                )
            elif tile_type == TileType.COMMUNITY_CHEST:
                round_data = self.__execute_card_action(
                    board=board,
                    deck=community_chests,
                    card_type='Community Chest',
                    stats=stats,
                    round_data=round_data
                )

        return round_data

    def __in_jail_round(
        self,
        increment: int,
        board: Board,
        stats: Dict[str, int]
    ) -> None:
        """Execute round in Jail.

        Args:
            increment (int): Position increment.
            board (Board): Monopoly Board.
            stats (Dict[str, int]): Statistics data.
        """
        print(colored(f'[In Jail] - Rolled: {increment}', 'magenta'))

        # Use 'Get Out of Jail' Card from Inventory
        if self.__inventory:
            print(colored('Used Get Out of Jail Card!', 'green'))
            self.__discard_card_from_inventory()

        # Try 3x to get out of Jail
        else:
            if self.__jail_time > 0 and self.__doubles < 1:
                self.__jail_time -= 1
                return

        print()

        # Escape Jail
        self.__jail_time = 3
        self.__display_move(increment, board)
        self.__current_position += increment

        stats[board.tiles[self.__current_position].label] += 1

    def __move(
        self,
        increment: int,
        board: Board,
        chances: Deck,
        community_chests: Deck,
        stats: Dict[str, int],
        round_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Move Player to new position.

        Args:
            increment (int): Position increment.
            board (Board): Monopoly Board.
            chances (Deck): Chance Cards Deck.
            community_chests (Deck): Community Chest Cards Deck.
            stats (Dict[str, int]): Statistics data.
            round_data (pd.DataFrame): Round Visit Data.

        Returns:
            pd.DataFrame: Updated Round Visit Data.
        """
        # In Jail
        if self.__current_position == 10:
            self.__in_jail_round(
                increment=increment,
                board=board,
                stats=stats
            )

        # Not in Jail
        else:
            round_data = self.__regular_round(
                increment=increment,
                board=board,
                chances=chances,
                community_chests=community_chests,
                stats=stats,
                round_data=round_data
            )

        return round_data

    def execute_round(
        self,
        board: Board,
        chances: Deck,
        community_chests: Deck,
        stats: Dict[str, int],
        round_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Execute round of Monopoly.

        Args:
            board (Board): Monopoly Board.
            chances (Deck): Chance Cards Deck.
            community_chests (Deck): Community Chest Cards Deck.
            stats (Dict[str, int]): Statistics data.
            round_data (pd.DataFrame): Round Visit Data.

        Returns:
            pd.DataFrame: Updated Round Visit Data.
        """
        increment = self.__roll_the_dice()

        if increment != 0:
            round_data = self.__move(
                increment=increment,
                board=board,
                chances=chances,
                community_chests=community_chests,
                stats=stats,
                round_data=round_data
            )

        return round_data
