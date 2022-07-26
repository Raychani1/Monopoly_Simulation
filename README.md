# Monopoly Simulation

<!-- ABOUT THE PROJECT -->
## **About The Project**
This Project simulates the movement of a Player in the game of Monopoly. Once the simulation is over statistics are displayed.

### **Features**

* **Logging** - Each movement on the board is displayed as a log message in the terminal, which represents the current tile the Player is on, the dice roll and the number of times the Player have crossed the 'Go' Tile. This way we can see the progress of the Player in the simulation. For example:
```
Current tile: ['Green #2'] - North Carolina Avenue, Rolled: 7, Crossed GO: 98x
```


* **Saved Text Output** - Tile visit statistics data are sorted and save to Output files.

* **Dice Roll Distribution Plots** - Distribution of dice roll sums are displayed in interactive count plots.
[![Roll Distribution Plot][roll-dist-screenshot]](#)

* **Top 10 Visited Tiles Plots** - Top 10 most visited tiles are also displayed and saved.
[![Top 10 Visited Tiles Plot][top-10-screenshot]](#)

* **Grouped Visit Line Charts** - We can look into tile group based visits in interactive line chart.
[![Grouped Visit Line Chart][line-chart-screenshot]](#)
[![Grouped Visit Line Chart Gif][line-chart-gif]](#)

* **Board Heatmaps** - Based on the collected data a heatmap is also generated.
[![Heatmap Screenshot][heatmap-screenshot]](#)

### **Built With**

* [![Python 3.10][Python]][Python-url]
* [![NumPy][Numpy]][Numpy-url]
* [![Pandas][Pandas]][Pandas-url]
* [![Plotly][Plotly]][Plotly-url]

<!-- GETTING STARTED -->
## **Getting Started**

To get a local copy up and running follow these simple steps.

### **Prerequisites**

* **Python 3.10.x** - It is either installed on your Linux distribution or on other Operating Systems you can get it from the [Official Website](https://www.python.org/downloads/release/python-3100/), [Microsoft Store](https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5?hl=en-us&gl=US) or through `Windows Subsystem for Linux (WSL)` using this [article](https://medium.com/@rhdzmota/python-development-on-the-windows-subsystem-for-linux-wsl-17a0fa1839d).

## **Usage**

1. Clone the repo
   ```sh
   git clone https://github.com/Raychani1/Monopoly_Simulation.git
   ```
2. Navigate to the project folder and call the Executor script

    On Linux:
   ```sh
   ./Monopoly_Simulation [Number of Rounds]
   ```

   On Windows:
   ```sh
   .\Monopoly_Simulation.ps1 [Number of Rounds]
   ```

<!-- LICENSE -->
## **License**

Distributed under the **MIT License**. See [LICENSE](https://github.com/Raychani1/Monopoly_Simulation/blob/feature/documentation/LICENSE) for more information.

<!-- ACKNOWLEDGMENTS -->
## **Acknowledgments**

* [James LePage: Using Math To Crush Your Opponents In Monopoly, And More (Medium Article)](https://medium.com/millionaire-by-25/using-math-to-crush-your-opponents-in-monopoly-and-more-dc53441e932b)
* [Othneil Drew: Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<!-- MARKDOWN LINKS & IMAGES -->
[roll-dist-screenshot]: https://raw.githubusercontent.com/Raychani1/raychani1.github.io/main/projects/python/monopoly_simulation/readme_images/rolls.png
[top-10-screenshot]: https://raw.githubusercontent.com/Raychani1/raychani1.github.io/main/projects/python/monopoly_simulation/readme_images/top10.png
[line-chart-screenshot]: https://raw.githubusercontent.com/Raychani1/raychani1.github.io/main/projects/python/monopoly_simulation/readme_images/line_chart.png
[line-chart-gif]: https://raw.githubusercontent.com/Raychani1/raychani1.github.io/main/projects/python/monopoly_simulation/readme_images/line_chart_2.gif
[heatmap-screenshot]: https://raw.githubusercontent.com/Raychani1/raychani1.github.io/main/projects/python/monopoly_simulation/readme_images/heatmap.png
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Numpy]: https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white
[Numpy-url]: https://numpy.org/
[Pandas]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Plotly]: https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white
[Plotly-url]: https://plotly.com/
