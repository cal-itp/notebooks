import os
from typing import Mapping, Any
import glob

import pandas as pd

SPREADSHEET_KEY = "1XXJ0Ap_X5JWBHI_bE_qzIy4pi1-jgeySw1ib4TqdJ4w"

STACK_SHEETS = {
    "contracts": "2103302402",
    "relationships": "1316605558",
    "components": "559021047",
    "rel product to component": "916550355",
    "key product": "373700708",
    "key vendor": "902942129",
    "key component": "47522779",
}


def read_stack_from_gsheets(
    sheet_key: str = SPREADSHEET_KEY,
    stack_sheets: dict = STACK_SHEETS,
    filter_dict: Mapping = {},
) -> Mapping:
    """Read stack from google sheets and return as a dictionary mapped
    as::
        {
            sheet_name: DataFrame(sheet contents),
        }

    Args:
        sheet_key: [description]
        stack_sheets
        filter_dict: If specified, will filter the stack based on this dictionary
            specifying column/value to filter for.
            Will skip if column not in a dataframe.
            ..note::
                will not filter all the 'related' dataframes for rows
                that are relevant to that filter, so extraneous data will
                still exist.
            ..example::
                {"Mechanism":"Intra-product","Component A": "AVL Software"}

    Returns:
        Mapping[str,pd.DataFrame]: [description]
    """

    df_dict = {}
    for sheet_name, sheet_gid in stack_sheets.items():
        url = f"https://docs.google.com/spreadsheets/d/{sheet_key}/export?gid={sheet_gid}&format=csv"
        _df = pd.read_csv(url, skiprows=1)
        if filter_dict:
            _df = _filter_df(_df, filter_dict)
        # remove "private" columns
        for c in _df.columns:
            if c[0] == "_":
                _df.drop(c, axis=1)

        df_dict[sheet_name] = _df

    return df_dict


def read_stack_from_dir(
    directory: str, filter_dict: Mapping[str, Any] = {}
) -> Mapping[str, pd.DataFrame]:
    """Read all csv files in a directory and return as a dictionary mapped
    as::
        {
            sheet_name: DataFrame(sheet contents),
        }

    Args:
        directory: [description]
        filter_dict: If specified, will filter the stack based on this dictionary
            specifying column/value to filter for.
            Will skip if column not in a dataframe.
            ..note::
                will not filter all the 'related' dataframes for rows
                that are relevant to that filter, so extraneous data will
                still exist.
            ..example::
                {"Mechanism":"Intra-product","Component A": "AVL Software"}

    Returns:
        Mapping[str,pd.DataFrame]: [description]
    """

    def _get_sheetname(full_filepath):
        filename = os.path.split(full_filepath)[-1]
        filename_without_ext = os.path.splitext(filename)[0]
        sheetname = filename_without_ext.split(" - ")[-1]
        return sheetname

    df_dict = {}
    for f in glob.glob(os.path.join(directory, "*.csv")):
        _df = pd.read_csv(f, skiprows=1)
        if filter_dict:
            _df = _filter_df(_df, filter_dict)
        df_dict[_get_sheetname(f)] = _df

    return df_dict


def _filter_df(df: pd.DataFrame, filter_dict: Mapping[str, Any]) -> pd.DataFrame:
    """[summary]

    Args:
        df (pd.DataFrame): Dataframe to filter
        filter_dict (Mapping[str,Any]):  Dictionary specifying column/value to filter for.
            Will skip if column not in a dataframe.
            ..example::
                {"Mechanism":"Intra-product","Component A": "AVL Software"}

    Returns:
        pd.DataFrame: [description]
    """
    _filter_dict = {k: v for k, v in filter_dict.items() if k in df.columns}

    filtered_df = df.loc[
        df[list(_filter_dict.keys())].isin(list(_filter_dict.values())).all(axis=1), :
    ]
    return filtered_df


def example_dir(example_name: str):
    """Takes an example name and returns the directory.

    Args:
        example_name: name of example
    """
    package_dir = os.path.dirname(os.path.abspath(__file__))
    main_example_dir = os.path.join(os.path.dirname(package_dir), "examples")

    example_dir = os.path.join(main_example_dir, example_name)

    if not os.path.exists(example_dir):
        available_examples = [
            name for name in os.listdir(example_dir) if os.path.isdir(name)
        ]
        ex_str = "\n - ".join(available_examples)
        msg = f"{example_name} not an available example. \
            Available examples:\n - {ex_str}"
        raise ValueError(msg)

    return example_dir
