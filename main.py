import os
from datetime import datetime

from game_statistics.game_statistics import GameStatistics


if __name__ == '__main__':
    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    game_statistics = GameStatistics(
        input_data=os.path.join(
            os.getcwd(),
            'monopoly',
            'data',
            'board_data.txt'
        ),
        file=os.path.join(
            os.getcwd(),
            'output',
            f'output_{timestamp}.txt',
        ),
        timestamp=timestamp,
        rounds=2000
    )

    game_statistics()
