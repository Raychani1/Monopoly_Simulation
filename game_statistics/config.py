from typing import Dict, List

number_of_visits: str = 'Number of Visits'

group_drop_columns: List[str] = [
    'Go', 'Jail', 'Visiting Jail', 'Free Parking', 'Go To Jail'
]

line_chart_labels: Dict[str, str] = {
    'index': 'Round',
    'value': number_of_visits,
    'variable': 'Group'
}

top_10_columns: List[str] = ['Tile', number_of_visits]
