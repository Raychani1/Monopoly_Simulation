import os
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

from monopoly.board.board import Board
from monopoly.deck.deck import Deck
from monopoly.player.player import Player


class GameStatistics:

    """Monopoly Game Statistics."""

    def __init__(
        self,
        board_data: str,
        chances_data: str,
        community_chests_data: str,
        output_file: str,
        timestamp: str,
        rounds: int = 10000
    ) -> None:
        """Initialize the Game Statistics Class.

        Args:
            board_data (str): Board tiles data file path.
            chances_data (str): Chance tiles data file path.
            community_chests_data (str): Community Chest tiles data file path.
            output_file (str): Game Statistics output file path.
            rounds (int, optional): Number of rounds (Crossing the GO tile). 
            Defaults to 10000.
        """
        # Board Related Attributes
        self.__board: Board = Board(file=board_data)
        self.__chances: Deck = Deck(file=chances_data)
        self.__community_chests: Deck = Deck(file=community_chests_data)

        # Statistics Related Attributes
        self.__stats: Dict[str, int] = {}
        self.__load_tile_names()
        self.__rounds: int = rounds
        self.__data: pd.DataFrame = pd.DataFrame.from_dict(
            self.__stats,
            orient='index'
        )

        # Player Related Attributes
        self.__player: Player = Player()

        # Output Related Attributes
        self.__output_file: str = output_file
        self.__timestamp = timestamp

    def __load_tile_names(self) -> None:
        """Load Tile Names to Statistics Dictionary."""
        for tile in self.__board.tiles:
            self.__stats[tile.label] = 0

    def __run(self) -> None:
        """Simulate the Game of Monopoly."""
        round_number: int = 0

        while self.__player.crossed_go_tile < self.__rounds:

            self.__player.execute_round(
                board=self.__board,
                chances=self.__chances,
                community_chests=self.__community_chests,
                stats=self.__stats
            )

            self.__data[f'Round {round_number}'] = pd.Series(self.__stats)

            if self.__player.crossed_go_tile != round_number:
                round_number += 1

        groups = [x.split('#')[0].strip() for x in self.__data.index.values]

        self.__data['Group'] = groups
        # self.__data.drop(0, axis=1, inplace=True)
        self.__data.reset_index(inplace=True)

        simplified_data: pd.DataFrame = (
            self.__data.groupby('Group').transform('sum')
        )

        simplified_data.drop_duplicates(inplace=True)

        simplified_data['index'] = [
            x.split('#')[0].strip() for x in simplified_data['index'].values
        ]

        simplified_data = simplified_data.transpose().reset_index(drop=True)
        simplified_data.columns = simplified_data.iloc[0].values
        simplified_data.drop(labels=0, axis=0, inplace=True)
        simplified_data.drop(
            labels=[
                'Go', 'Jail', 'Visiting Jail', 'Free Parking', 'Go To Jail'
            ],
            axis=1,
            inplace=True
        )

        print(simplified_data)

        plt.figure(figsize=(25, 15))
        fig = px.line(
            simplified_data,
            x=simplified_data.index,
            y=simplified_data.columns,
            title='Title'
        )
        fig.show()

        fig.write_html(
            os.path.join(
                os.getcwd(),
                'output',
                'plots',
                'line_charts',
                f'monopoly_game_category_visit_{self.__rounds}_rounds_'
                f'{self.__timestamp}.html'
            )
        )

        # fig = plt.figure()
        # ax = plt.subplot(111)

        # simplified_data.plot.line()

        # # Shrink current axis by 20%
        # box = ax.get_position()
        # ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # # Put a legend to the right of the current axis
        # ax.legend(loc='center right', bbox_to_anchor=(1, 0.5))

        # plt.savefig(
        # os.path.join(
        #     os.getcwd(),
        #     'output',
        #     'plots',
        #     'line_charts',
        #     f'monopoly_game_category_visit_{self.__rounds}_rounds_'
        #     f'{self.__timestamp}.png'
        # )
        # )

    def __load_data_to_numpy_array(self) -> np.ndarray:
        """Load Statistic Data to NumPy Array for Heatmap.

        Returns:
            np.ndarray: Loaded Statistic Data.
        """
        heatmap_data: np.ndarray = np.zeros((11, 11))
        tile_mapping: pd.DataFrame = pd.read_csv(
            os.path.join(
                os.getcwd(), 'game_statistics', 'data', 'tile_mapping.csv'
            ),
            delimiter=';'
        )

        for _, row in tile_mapping.iterrows():
            heatmap_data[row[1], row[2]] = (
                self.__stats[self.__board.tiles[row[0]].label]
            )

        return heatmap_data.astype(int)

    def __generate_roll_barplot(self) -> None:
        """Generate and Save 'Roll Distribution' barplot."""
        data: pd.DataFrame = pd.DataFrame(
            self.__player.roll_history,
            columns=['Rolls']
        )

        sns.displot(
            data,
            x="Rolls",
            height=10,
            bins=data['Rolls'].nunique()
        )

        plt.title(
            f'Rolls of 1 Player - {self.__rounds} Rounds'
        )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                os.getcwd(),
                'output',
                'plots',
                'barplots',
                f'monopoly_game_rolls_barplot_{self.__rounds}_rounds_'
                f'{self.__timestamp}.png'
            )
        )

    def __generate_top_10_tiles_barplot(self) -> None:
        """Generate and Save 'TOP 10 Visited Tiles' barplot."""
        data: pd.DataFrame = pd.DataFrame.from_dict(
            self.__stats,
            orient='index',
        )

        data.reset_index(inplace=True)

        data.columns = ['Tile', 'Number of Visits']

        plt.figure(figsize=(16, 9))
        sns.barplot(
            data=data.head(10),
            x='Tile',
            y='Number of Visits',
        )

        plt.title(
            f'Top 10 Tiles Visited by 1 Player - {self.__rounds} Rounds'
        )

        plt.xticks(rotation=30)

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                os.getcwd(),
                'output',
                'plots',
                'barplots',
                f'monopoly_top_10_tiles_barplot_{self.__rounds}_rounds_'
                f'{self.__timestamp}.png'
            )
        )

    def __generate_barplots(self) -> None:
        """Generate and Save different barplots based on Game Statistics."""
        self.__generate_roll_barplot()
        self.__generate_top_10_tiles_barplot()

    def __generate_heatmap(self) -> None:
        """Generate and Save Monopoly Board Heatmap."""
        data: np.ndarray = self.__load_data_to_numpy_array()

        fig = plt.figure(figsize=(16, 9))
        ax = sns.heatmap(data, annot=True, linewidth=0.5, fmt='d')
        fig.add_axes(ax)
        plt.title(
            f'Monopoly Board Heatmap of 1 Player - {self.__rounds} Rounds'
        )

        for t in ax.texts:
            if int(t.get_text()) > 0:
                t.set_text(t.get_text())
            else:
                t.set_text("")

        plt.savefig(
            os.path.join(
                os.getcwd(),
                'output',
                'plots',
                'heatmaps',
                f'monopoly_board_heatmap_{self.__rounds}_rounds_'
                f'{self.__timestamp}.png'
            )
        )

    def __process_statistics(self) -> None:
        """Sort Statistics."""
        self.__stats = {
            k: v for k, v in reversed(
                sorted(self.__stats.items(), key=lambda item: item[1])
            )
        }

    def __save_statistics(self) -> None:
        """Save Game Statistics to File."""

        with open(self.__output_file, 'a') as fp:
            fp.write(f"{'Name':<20} {'Number':<8}\n")

            for k, v in self.__stats.items():
                fp.write(f'{k:<20} {v:<8}\n')

    def __call__(self, *args: Any, **kwds: Any) -> None:
        """Make Game Statistics Class callable."""
        # Simulate the Game
        self.__run()

        # Process Statistics
        self.__process_statistics()
        self.__save_statistics()

        # Generate Plots
        # self.__generate_barplots()
        # self.__generate_heatmap()
