import term_piechart
from typing import List, Dict
from database import get_collection

def transform_to_pie_data(categories_weights: Dict[str, float]) -> List[dict]:
    data = []
    for category, weight in categories_weights.items():
        requests.append({"name": str(category), "value": int(weight)})
    return data


data = [
    {"name": "GET", "value": 9983},
    {"name": "POST", "value": 7005},
    {"name": "DELETE", "value": 3323},
    {"name": "PUT", "value": 2794},
    {"name": "PATCH", "value": 1711},
]


def get_piechart(data: List[dict]):
    pie = term_piechart.Pie(
        data,
        radius=5,
        autocolor=False,
        autocolor_pastel_factor=0.7,
        legend={"line": 0, "format": "{label} {name:<8} {percent:>5.2f}% [{value}]"},
    )
    return pie

#print(get_collection(6).get_category_weights())
# {'Shelter': 3300.0, 'Sleep': 960.0, 'Clothing': 530.0}
