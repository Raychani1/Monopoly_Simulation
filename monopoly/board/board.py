from pprint import pprint
from typing import Dict, List

from monopoly.board.tiles.property import Property
from monopoly.board.tiles.tile import Tile
from monopoly.board.tiles.tile_type import TileType


class Board:

    """Monopoly Board.

    Attributes:
        tiles (List[Tile]): Monopoly Board Tiles.
        map (Dict[str, int]): Monopoly Board Map.
        railroads (List[int]): Railroad Locations.
        utilities (List[int]): Utility Locations.
    """

    def __init__(self, file: str) -> None:
        """Initialize the Board Class.

        Args:
            file (str): Board Data File.
        """
        # Basic Board Attributes
        self.__tiles: List[Tile] = []
        self.__map: Dict[str, int] = {}

        # Special Tile Locations
        self.__railroads: List[int] = []
        self.__utilities: List[int] = []

        self.__initialize_board(file)

    @property
    def tiles(self) -> List[Tile]:
        """Return Board Tiles.

        Returns:
            List[Tile]: Board Tiles.
        """
        return self.__tiles

    @property
    def map(self) -> Dict[str, int]:
        """Return Board Map.

        Returns:
            Dict[str, int]: Board Map.
        """
        return self.__map

    @property
    def railroads(self) -> List[int]:
        """Return Railroad Locations.

        Returns:
            List[int]: Railroad Locations.
        """
        return self.__railroads

    @property
    def utilities(self) -> List[int]:
        """Return Utility Locations.

        Returns:
            List[int]: Utility Locations.
        """
        return self.__utilities

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

    def __update_mapping(self, index: int, tile: List[str]) -> None:
        """Update Board Tile Mapping.

        Args:
            index (int): Tile index.
            tile (List[str]): Tile Data.
        """
        match len(tile):

            # 'GO', 'Jail', 'Visiting Jail', 'Free Parking', 'Go To Jail'
            case 1:
                self.__map[tile[0]] = index

            # Every other category
            case _:
                if tile[1] in ['Chance', 'Community Chest']:
                    self.__map[tile[0]] = index
                else:
                    self.__map[tile[1]] = index

                    if tile[2] == 'Railroad':
                        self.__railroads.append(index)
                    elif tile[2] == 'Utility':
                        self.__utilities.append(index)

    def __initialize_board(self, file: str) -> None:
        """Initialize Monopoly Board Tiles.

        Args:
            file (str): Input Data File.
        """
        tiles = self.__read_input_data(file)

        for index, tile in enumerate(tiles):
            self.__update_mapping(index, tile)
            self.__tiles.append(self.__create_tile(tile))
