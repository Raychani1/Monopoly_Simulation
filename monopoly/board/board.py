from typing import List

from monopoly.board.tiles.property import Property
from monopoly.board.tiles.tile import Tile
from monopoly.board.tiles.tile_type import TileType


class Board:

    """Monopoly Board.

    Attributes:
        tiles (List[Tile]): Monopoly Board Tiles.
    """

    __tiles: List[Tile] = []

    def __init__(self, file: str) -> None:
        """Initialize the Board Class.

        Args:
            file (str): Board Data File.
        """
        self.__initialize_board(file)

    @property
    def tiles(self) -> List[Tile]:
        """Return Board Tiles.

        Returns:
            List[Tile]: Board Tiles.
        """
        return self.__tiles

    @staticmethod
    def __read_input_data(file: str) -> List[str]:
        """Load Data from Input Data File.

        Args:
            file (str): Input Data File.

        Returns:
            List[str]: Loaded Data.
        """
        with open(file) as f:
            content = f.readlines()
        return list(x.strip().split(',') for x in content)

    @staticmethod
    def __detect_tile_type(tile_type: str) -> TileType:
        """Detect Tile Type.

        Args:
            tile_type (str): Tile Type String.

        Returns:
            TileType: Detected Tile Type.
        """
        return {
            'Go': TileType.GO,
            'Property': TileType.PROPERTY,
            'Community_Chest': TileType.COMMUNITY_CHEST,
            'Tax': TileType.TAX,
            'Railroad': TileType.RAILROAD,
            'Chance': TileType.CHANCE,
            'Visiting Jail': TileType.VISITING_JAIL,
            'Jail': TileType.JAIL,
            'Utility': TileType.UTILITY,
            'Free Parking': TileType.FREE_PARKING,
            'Go To Jail': TileType.GO_TO_JAIL
        }[tile_type]

    def __create_tile(self, tile: List[str]) -> Tile:
        """Create Tile.

        Args:
            tile (List[str]): Tile Data.

        Returns:
            Tile: Created Tile.
        """
        tile_data_length = len(tile)

        if tile_data_length == 1:
            return Tile(tile[0], tile[0], self.__detect_tile_type(tile[0]))

        elif tile_data_length == 3:
            return Tile(tile[0], tile[1], self.__detect_tile_type(tile[2]))

        elif tile_data_length == 12:
            return Property(
                tile[0],
                tile[1],
                self.__detect_tile_type(tile[2]),
                tile[3],
                tile[4],
                list(map(int, tile[5:11])),
                tile[11]
            )

    def __initialize_board(self, file: str) -> None:
        """Initialize Monopoly Board Tiles.

        Args:
            file (str): Input Data File.
        """
        tiles = self.__read_input_data(file)
        for tile in tiles:
            self.__tiles.append(self.__create_tile(tile))
