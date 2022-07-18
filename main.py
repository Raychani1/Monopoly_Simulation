import os
from datetime import datetime

from game_statistics.game_statistics import GameStatistics


if __name__ == '__main__':
    rounds: int = 1000
    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    game_statistics = GameStatistics(
        board_data=os.path.join(
            os.getcwd(),
            'monopoly',
            'data',
            'board_data.txt'
        ),
        chances_data=os.path.join(
            os.getcwd(),
            'monopoly',
            'data',
            'chances_data.txt'
        ),
        community_chests_data=os.path.join(
            os.getcwd(),
            'monopoly',
            'data',
            'community_chest_data.txt'
        ),
        output_file=os.path.join(
            os.getcwd(),
            'output',
            f'output_{rounds}_rounds_{timestamp}.txt',
        ),
        timestamp=timestamp,
        rounds=rounds
    )

    game_statistics()
