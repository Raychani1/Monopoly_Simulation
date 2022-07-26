import os
from typing import Any, Dict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from game_statistics.config import (
    group_drop_columns,
    line_chart_labels,
    top_10_columns,
    NUMBER_OF_VISITS
)
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
        self.__heatmap_label_mapping: pd.DataFrame = (
            pd.DataFrame(np.empty((11, 11), dtype=np.str))
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

        while self.__player.crossed_go_tile < self.__rounds:

            self.__data = self.__player.execute_round(
                board=self.__board,
                chances=self.__chances,
                community_chests=self.__community_chests,
                stats=self.__stats,
                round_data=self.__data
            )

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

            self.__heatmap_label_mapping.at[
                row[1], row[2]
            ] = self.__board.tiles[row[0]].label

        return heatmap_data.astype(int)

    def __generate_line_chart(self) -> None:
        """Generate and Save 'Group Visit' line chart."""
        self.__process_round_data()

        fig = px.line(
            self.__data,
            x=self.__data.index,
            y=self.__data.columns,
            title=f'Visit by Group - {self.__rounds} Rounds',
            labels=line_chart_labels,
        )

        fig.update_traces(mode='lines', hovertemplate=None)
        fig.update_layout(hovermode='x unified')

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

    def __generate_roll_barplot(self) -> None:
        """Generate and Save 'Roll Distribution' barplot."""
        data: pd.DataFrame = pd.DataFrame(
            self.__player.roll_history,
            columns=['Rolls']
        ).sort_values(by='Rolls')

        fig = px.histogram(
            data,
            x='Rolls',
            color='Rolls',
            title=f'Rolls of 1 Player - {self.__rounds} Rounds',
            text_auto=True,

        )
        fig.update_layout(bargap=0.2, legend_traceorder='normal')

        fig.show()

        fig.write_html(
            os.path.join(
                os.getcwd(),
                'output',
                'plots',
                'barplots',
                f'monopoly_game_rolls_barplot_{self.__rounds}_rounds_'
                f'{self.__timestamp}.html'
            )
        )

    def __generate_top_10_tiles_barplot(self) -> None:
        """Generate and Save 'TOP 10 Visited Tiles' barplot."""
        data: pd.DataFrame = pd.DataFrame.from_dict(
            self.__stats,
            orient='index',
        )

        data.reset_index(inplace=True)

        data.columns = top_10_columns

        data.sort_values(by=NUMBER_OF_VISITS, ascending=False, inplace=True)

        fig = px.histogram(
            data.head(10),
            x='Tile',
            y=NUMBER_OF_VISITS,
            title=f'Top 10 Tiles Visited by 1 Player - {self.__rounds} Rounds',
            color=NUMBER_OF_VISITS,
            text_auto=True
        )

        fig.update_layout(bargap=0.2, yaxis_title=NUMBER_OF_VISITS)

        fig.update_traces(
            hovertemplate=(
                'Tile: %{x} <br>'
                'Number of Visits: %{y}<extra></extra>'
            )
        )

        fig.show()

        fig.write_html(
            os.path.join(
                os.getcwd(),
                'output',
                'plots',
                'barplots',
                f'monopoly_top_10_barplot_{self.__rounds}_rounds_'
                f'{self.__timestamp}.html'
            )
        )

    def __generate_barplots(self) -> None:
        """Generate and Save different barplots based on Game Statistics."""
        self.__generate_roll_barplot()
        self.__generate_top_10_tiles_barplot()

    def __generate_heatmap(self) -> None:
        """Generate and Save Monopoly Board Heatmap."""
        data: np.ndarray = self.__load_data_to_numpy_array()
        data = data[::-1]

        annotations = data.copy()
        annotations = np.where(annotations == 0, '', annotations)

        fig = ff.create_annotated_heatmap(
            data,
            annotation_text=annotations,
        )

        fig.update(
            data=[{
                'customdata': self.__heatmap_label_mapping.to_numpy()[::-1],
                'hovertemplate': (
                    'Tile: %{customdata}<br>'
                    'Number of Visits: %{z}<extra></extra>'
                )
            }]
        )
        fig.update_layout(
            xaxis_visible=False,
            xaxis_showticklabels=False,
            yaxis_visible=False,
            yaxis_showticklabels=False,
            title=(
                f'Monopoly Board Heatmap of 1 Player - {self.__rounds} Rounds'
            )
        )

        fig.show()

        fig.write_html(
            os.path.join(
                os.getcwd(),
                'output',
                'plots',
                'heatmaps',
                f'monopoly_board_heatmap_{self.__rounds}_rounds_'
                f'{self.__timestamp}.html'
            )
        )

    def __process_round_data(self) -> None:
        """Process accumulated round visit Data."""
        # Defragmenting DataFrame
        self.__data = self.__data.copy()

        groups = [x.split('#')[0].strip() for x in self.__data.index.values]

        self.__data['Group'] = groups

        self.__data.reset_index(inplace=True)

        self.__data = (
            self.__data.groupby('Group').transform('sum')
        )

        self.__data.drop_duplicates(inplace=True)

        self.__data['index'] = [
            x.split('#')[0].strip() for x in self.__data['index'].values
        ]

        self.__data = self.__data.transpose().reset_index(drop=True)
        self.__data.columns = self.__data.iloc[0].values
        self.__data.drop(labels=0, axis=0, inplace=True)
        self.__data.drop(
            labels=group_drop_columns,
            axis=1,
            inplace=True
        )

        self.__data = self.__data.reindex(sorted(self.__data.columns), axis=1)
        self.__data = self.__data.reset_index(drop=True)

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
        self.__generate_barplots()
        self.__generate_line_chart()
        self.__generate_heatmap()
