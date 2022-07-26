import os
import platform
from pathlib import Path
from typing import List


def create_output_directory(plot_output_folder: str) -> None:
    """Create Output Directory with subdirectories.

    Args:
        plot_output_folder (str): Output Directory.
    """

    subdirs: List[Path] = [
        Path(os.path.join(plot_output_folder, 'barplots')),
        Path(os.path.join(plot_output_folder, 'heatmaps')),
        Path(os.path.join(plot_output_folder, 'line_charts')),
    ]

    for subdir in subdirs:
        subdir.mkdir(parents=True, exist_ok=True)


def setup_environment(requirements: str) -> None:
    """Install all the required packages from the requirements file.

    Args:
        requirements (str): Requirements File Path
    """

    # Get current Operating System
    platform_os = platform.system()

    # Install packages for Linux
    if platform_os == 'Linux':
        os.system(
            f"pip --disable-pip-version-check install -r {requirements} | "
            f"grep -v 'already satisfied'"
        )

    # Install packages for Windows
    elif platform_os == 'Windows':
        with open(requirements, 'r') as requirements_file:

            lines = requirements_file.readlines()

            for requirement in lines:
                os.system(
                    f"pip --disable-pip-version-check install {requirement}"
                )

    print('\nInstalled Packages:')
    os.system("pip freeze")
    print()


def setup():
    """Sets up the Virtual Environment and creates Data Directory."""

    # Create output directory
    create_output_directory(
        plot_output_folder=os.path.join(os.getcwd(), 'output', 'plots')
    )

    # Setup virtual environment
    setup_environment(
        requirements=os.path.join(os.getcwd(), 'requirements.txt')
    )


if __name__ == '__main__':
    setup()
