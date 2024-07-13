import term_piechart
from typing import List, Dict
from database import get_collection


def transform_to_pie_data(categories_weights: Dict[str, float]) -> List[dict]:
    data = []
    for category, weight in categories_weights.items():
        data.append({"name": f"{category.ljust(10)} {format_weight(int(weight)).ljust(4)}", "value": int(weight)})
    return data


def get_piechart(data: List[dict]):
    pie = term_piechart.Pie(
        data,
        radius=4,
        autocolor=False,
        autocolor_pastel_factor=0.0,
        legend={"line": 0, "format": "{percent:>5.2f}% {label} {name:<10} "},
    )
    return pie


def format_weight(weight):
    return f"{weight / 1000:.1f} kg" if weight >= 1000 else f"{int(weight)} g"
