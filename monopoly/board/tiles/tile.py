from monopoly.board.tiles.tile_type import TileType


class Tile:

    """Monopoly Board Tile.

    Attributes:
        label (List[Tile]): Monopoly Board Tiles.
        name (str): Tile name.
        tile_type (TileType): Tile type.
    """

    def __init__(self, label: str, name: str, tile_type: TileType) -> None:
        """Initialize the Tile Class.

        Args:
            label (str): Tile label.
            name (str): Tile name.
            tile_type (TileType): Tile type.
        """
        self.__label: str = label
        self.__name: str = name
        self.__tile_type: TileType = tile_type

    @property
    def label(self) -> str:
        """Return Tile label.

        Returns:
            str: Tile label.
        """
        return self.__label

    @property
    def name(self) -> str:
        """Return Tile name.

        Returns:
            str: Tile name.
        """
        return self.__name

    @property
    def tile_type(self) -> str:
        """Return Tile type.

        Returns:
            str: Tile type.
        """
        return self.__tile_type

    def __str__(self) -> str:
        """Make Tile displayable.

        Returns:
            str: Tile String representation.
        """
        return f'[{self.__label}] - {self.__name}'
