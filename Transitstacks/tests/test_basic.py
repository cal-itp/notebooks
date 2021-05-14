import pandas as pd
import transitstacks as ts
import pytest

expected_sheets = [
    "contracts",
    "relationships",
    "components",
    "rel product to component",
    "key product",
    "key vendor",
    "key component",
]


def test_gsheet_io():
    stack_dict = ts.read_stack_from_gsheets()
    missing_sheets = set(expected_sheets) - set(list(stack_dict.keys()))
    if missing_sheets:
        print(f"Missing sheets: {missing_sheets}")
    assert not missing_sheets
    assert all(type(x) == pd.DataFrame for x in stack_dict.values())


def test_csv_io():
    EXAMPLE_DIR = ts.example_dir("prototype")
    stack_dict = ts.read_stack_from_dir(EXAMPLE_DIR)
    missing_sheets = set(expected_sheets) - set(list(stack_dict.keys()))
    if missing_sheets:
        print(f"Missing sheets: {missing_sheets}")
    assert not missing_sheets
    assert all(type(x) == pd.DataFrame for x in stack_dict.values())


def test_filter():
    PROVIDER = "GET Bus"
    stack_dict = ts.read_stack_from_gsheets(filter_dict={"Transit Provider": PROVIDER})
    transit_providers = set(stack_dict["components"]["Transit Provider"].tolist())
    if len(transit_providers) != 1 or list(transit_providers)[0] != PROVIDER:
        print(f"Filter for {PROVIDER} didn't work. Ended up with {transit_providers}.")
    assert len(transit_providers) == 1
    assert list(transit_providers)[0] == PROVIDER


def test_stack_creation():
    PROVIDER = "GET Bus"
    stack_dict = ts.read_stack_from_gsheets(filter_dict={"Transit Provider": PROVIDER})
    my_stack = ts.Stack(stack_dict)
    expected_component_cols = [
        "Product",
        "Component",
        "Contract ID",
        "Transit Provider",
        "Component Group",
        "Function Group",
        "Location",
        "Vendor",
        "Contract Holder",
        "Contract Vendor",
        "End date",
    ]

    assert not set(expected_component_cols) - set(my_stack.components_df.columns)


def test_stack_diagram():

    PROVIDER = "GET Bus"
    stack_dict = ts.read_stack_from_gsheets(filter_dict={"Transit Provider": PROVIDER})
    my_stack = ts.Stack(stack_dict)

    LEVEL1 = "Function Group"
    LEVEL2 = "Product"
    ts.stack_diagram(
        my_stack,
        cluster_level_1=LEVEL1,
        cluster_level_2=LEVEL2,
    )
    # TODO need an assert statement
