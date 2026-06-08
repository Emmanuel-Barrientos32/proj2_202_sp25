import csv
import math
from dataclasses import dataclass
from typing import *


# Put your data definitions first!

# ...

# Then your functions.

# ...
import sys
sys.setrecursionlimit(10_000)

# Put your data definitions first!

@dataclass (frozen= True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions : float
    electricity_and_heat_co2_emissions_per_capita : float
    energy_co2_emissions : float
    energy_co2_emissions_per_capita: float
    total_co2_emissions_excluding_luc: float 
    total_co2_emissions_excluding_lucf_per_capita : float

@dataclass (frozen = True)
class Node:
    value: Row
    next: Node | None
    


expected_header = [
    "country",
    "year",
    "electricity_and_heat_co2_emissions",
    "electricity_and_heat_co2_emissions_per_capita",
    "energy_co2_emissions",
    "energy_co2_emissions_per_capita",
    "total_co2_emissions_excluding_lucf",
    "total_co2_emissions_excluding_lucf_per_capita"
]
def parse_float(s: str) -> Optional[float]:
    if s == "":
        return None
    return float(s)


def parse_row(fields: list[str]) -> Row:
    return Row(
        fields[0],
        int(fields[1]),
        parse_float(fields[2]),
        parse_float(fields[3]),
        parse_float(fields[4]),
        parse_float(fields[5]),
        parse_float(fields[6]),
        parse_float(fields[7]),
    )

def build_list(rows: list[list[str]]) -> Optional[Node]:
    if rows == []:
        return None
    return Node(parse_row(rows[0]), build_list(rows[1:]))
  
def read_csv_lines(filename: str) -> Optional[Node]:
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        if header != expected_header:
            raise ValueError("Invalid header row")

        rows = list(reader)
        return build_list(rows)


def listlen(data: Optional[Node]) -> int:
    if data is None:
        return 0
    return 1 + listlen(data.next)


def filter_rows(
    data: Optional[Node],
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> Optional[Node]:

    if data is None:
        return None

    row = data.value

    if field_name == "country":
        field = row.country
    elif field_name == "year":
        field = row.year
    elif field_name == "electricity_and_heat_co2_emissions":
        field = row.electricity_and_heat_co2_emissions
    elif field_name == "electricity_and_heat_co2_emissions_per_capita":
        field = row.electricity_and_heat_co2_emissions_per_capita
    elif field_name == "energy_co2_emissions":
        field = row.energy_co2_emissions
    elif field_name == "energy_co2_emissions_per_capita":
        field = row.energy_co2_emissions_per_capita
    elif field_name == "total_co2_emissions_excluding_lucf":
        field = row.total_co2_emissions_excluding_lucf
    elif field_name == "total_co2_emissions_excluding_lucf_per_capita":
        field = row.total_co2_emissions_excluding_lucf_per_capita
    else:
        raise ValueError("Invalid field name")

    if field is None:
        return filter_rows(data.next, field_name, comparison, value)

    if field_name == "country" and comparison != "equal":
        raise ValueError("Country only supports equal comparison")

    if comparison == "equal":
        match = field == value
    elif comparison == "less_than":
        match = field < value
    elif comparison == "greater_than":
        match = field > value
    else:
        raise ValueError("Invalid comparison")

    filtered_rest = filter_rows(data.next, field_name, comparison, value)

    if match:
        return Node(row, filtered_rest)

    return filtered_rest
