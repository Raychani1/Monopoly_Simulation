import os
import platform
import sys
from datetime import datetime
from typing import Tuple

from termcolor import colored

from game_statistics.game_statistics import GameStatistics


def get_rounds_and_timestamp() -> Tuple[int, str]:
    """Return number of rounds and current timestamp.

    Returns:
        Tuple[int, str]: Number of Rounds and Current Timestamp.
    """
    usage: str = ''

    platform_os: str = platform.system()

    match platform_os:
        case 'Windows': usage = '.\Monopoly_Simulation.ps1 [Number of Rounds]'
        case _: usage = './Monopoly_Simulation [Number of Rounds]'

    try:
        rounds: int = int(sys.argv[1])
    except ValueError:
        print(colored(f'Invalid argument! Usage: {usage}', 'red'))
        quit()

    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    return rounds, timestamp


if __name__ == '__main__':

    rounds, timestamp = get_rounds_and_timestamp()

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
