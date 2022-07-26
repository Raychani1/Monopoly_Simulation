from typing import Dict, List

NUMBER_OF_VISITS: str = 'Number of Visits'

group_drop_columns: List[str] = [
    'Go', 'Jail', 'Visiting Jail', 'Free Parking', 'Go To Jail'
]

line_chart_labels: Dict[str, str] = {
    'index': 'Round',
    'value': NUMBER_OF_VISITS,
    'variable': 'Group'
}

top_10_columns: List[str] = ['Tile', NUMBER_OF_VISITS]
