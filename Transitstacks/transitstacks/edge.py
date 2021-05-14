from typing import Mapping, Union

import numpy as np
import pandas as pd

from diagrams import Edge

# executed in order with subsequent values overriding
default_edge_color = "grey"

edge_color_lookup = {
    ("Standard", "Human translation"): "red",
    ("Standard", np.NaN): "red",
    ("Parallel model", 1): "darkgreen",
    ("Centralized model", 1): "darkgreen",
}

# executed in order with subsequent values overriding
default_edge_style = "solid"

edge_style_lookup = {
    ("Standard", "Human translation"): "dotted",
    ("Mechanism", "Intra-product"): "dotted",
}


def define_edge(
    edge: Union[Mapping, pd.Series],
    ignore_values=["Intra-product", "nan", "TO CONFIRM", "Human translation"],
) -> Edge:
    """[summary]

    Args:
        edge (Union[Mapping,pd.Series]): [description]
        ignore_values: list of values to not print in labels
    Returns:
        Edge: [description]
    """
    _mech_str = "" if (str(edge.Mechanism) in ignore_values) else f"{edge.Mechanism}"
    _std_str = "" if (str(edge.Standard) in ignore_values) else f"{edge.Standard}"
    edge_label = ":".join([_mech_str, _std_str])

    edge_color = default_edge_color
    for (field, value), color in edge_color_lookup.items():
        if edge.get(field) == value:
            edge_color = color

    edge_style = default_edge_style
    for (field, value), style in edge_style_lookup.items():
        if edge.get(field) == value:
            edge_style = style

    e = Edge(
        color=edge_color,
        style=edge_style,
        # label=edge_label,
        xlabel=edge_label,
        labelfontname="courier",
        # labelfontcolor = edge_color,
    )
    return e


def relationships_to_edges(relationships_df: pd.DataFrame) -> Mapping[tuple, Edge]:
    edges_s = relationships_df.apply(define_edge, axis=1)
    relationship_edges = dict(
        zip(
            list(zip(relationships_df["Component A"], relationships_df["Component B"])),
            edges_s,
        )
    )
    return relationship_edges
