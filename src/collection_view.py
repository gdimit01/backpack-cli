from typing import List, Dict

import term_piechart  # https://github.com/va-h/term-piechart


def get_pie_data(weights: Dict[str, float]) -> List[dict]:
    return [
        {"name": f"{category.ljust(10)} {format_weight(int(weight))}", "value": int(weight)}
        for category, weight in weights.items()
    ]


def get_chart(data: List[dict]):
    pie = term_piechart.Pie(
        data,
        radius=4,
        autocolor=True,
        autocolor_pastel_factor=0.0,
        legend={"line": 0, "format": "{percent:>5.0f}% {label} {name:<10} "},
    )
    return pie


# format weight in grams
def format_weight(weight):
    return f"{weight / 1000:.1f} kg" if weight >= 1000 else f"{int(weight)} g"
