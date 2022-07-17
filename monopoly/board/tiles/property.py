from typing import List

from monopoly.board.tiles.tile import Tile
from monopoly.board.tiles.tile_type import TileType


class Property(Tile):

    """Monopoly Board Property Tile.

    Attributes:
        label (str): Tile label.
        name (str): Tile name.
        tile_type (TileType): Tile type.
        price (int): Tile price.
        price_per_house (int): House price on given Tile.
        rents (List[int]): Property Tile label.
        mortgage (int): Mortgage price on given Tile.
    """

    def __init__(
        self,
        label: str,
        name: str,
        tile_type: TileType,
        price: int,
        price_per_house: int,
        rents: List[int],
        mortgage: int
    ) -> None:
        """Initialize the Property Class.

        Args:
            label (str): Tile label.
            name (str): Tile name.
            tile_type (TileType): Tile type.
            price (int): Tile price.
            price_per_house (int): House price on given Tile.
            rents (List[int]): Property Tile label.
            mortgage (int): Mortgage price on given Tile.
        """
        super().__init__(label, name, tile_type)
        self.__price: int = price
        self.__price_per_house: int = price_per_house
        self.__rents: List[int] = rents
        self.__mortgage: int = mortgage

    @property
    def price(self) -> int:
        """Return Tile price.

        Returns:
            int: Tile price.
        """
        return self.__price

    @property
    def price_per_house(self) -> int:
        """Return House price on given Tile.

        Returns:
            int: House price on given Tile.
        """
        return self.__price_per_house

    @property
    def rents(self) -> List[int]:
        """Return Rent prices.

        Returns:
            List[int]: Rent prices.
        """
        return self.__rents

    @property
    def mortgage(self) -> int:
        """Return Mortgage price.

        Returns:
            int: Mortgage price.
        """
        return self.__mortgage

    def __str__(self) -> str:
        """Make Property Tile displayable.

        Returns:
            str: Property Tile String representation.
        """
        return (
            f'{super().__str__()}, Price: {self.__price}, '
            f'Price per House: {self.__price_per_house}, '
            f'Rents: {self.__rents}, Mortgage: {self.__mortgage}'
        )
