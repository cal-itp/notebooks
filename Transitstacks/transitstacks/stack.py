import textwrap
from typing import Mapping, Any, List, Collection, Union

import pandas as pd
import colorcet as cc
from diagrams import Cluster, Diagram

from .node import define_node
from .edge import relationships_to_edges
from .color import color_ramp, contrast_color

greenyellow_functiongroup_map = {
    "Fare collection": "#454d66",
    "Operations": "#309975",
    "Reporting": "#efeeb4",
    "Rider info": "#58b368",
    "Scheduling": "#dad873",
    "Backoffice": "#efeeb4",
}

neutral_colorramp = ["#F2F2F2", "#e5e5e6", "#e6e6e6", "#e6e2e9"]
faded_cool_colorramp = ["#d0eac6", "#c2d4c5", "#a4bfbe", "#97a3b2", "#8488a3"]

UNKNOWN_VALUE = "TO CONFIRM"
EXCLUDE_PREFIX = "_"
DEFAULT_BGCOLOR = "#d3d3d3"
DEFAULT_COLORRAMP = neutral_colorramp


class Stack:
    def __init__(self, stack_dict):
        _exclude = [
            f for f in stack_dict["components"].columns if f.startswith(EXCLUDE_PREFIX)
        ]

        self.components_df = stack_dict["components"].drop(_exclude, axis=1)

        self.components_df = add_df(
            self.components_df,
            stack_dict["key component"],
            "Component",
        )

        self.components_df = add_df(
            self.components_df,
            stack_dict["key product"],
            "Product",
        )

        self.components_df = add_df(
            self.components_df,
            stack_dict["contracts"],
            "Contract ID",
        )

        self.relationships_df = stack_dict["relationships"]

        # Dataframes with cluster attributes
        self.clusters = {}

    @property
    def providers(self) -> List[str]:
        x = self.components_df["Transit Provider"].dropna().unique().tolist()
        if UNKNOWN_VALUE in x:
            x.remove(UNKNOWN_VALUE)
        return x

    @property
    def contract_vendors(self) -> List[str]:
        x = self.components_df["Contract Vendor"].dropna().unique().tolist()
        if UNKNOWN_VALUE in x:
            x.remove(UNKNOWN_VALUE)
        return x

    @property
    def vendors(self) -> List[str]:
        x = self.components_df["Vendor"].dropna().unique().tolist()
        if UNKNOWN_VALUE in x:
            x.remove(UNKNOWN_VALUE)
        return x

    @property
    def products(self) -> List[str]:
        x = self.components_df["Product"].dropna().unique().tolist()
        if UNKNOWN_VALUE in x:
            x.remove(UNKNOWN_VALUE)
        return x

    @property
    def components(self) -> List[str]:
        x = self.components_df["Component"].dropna().unique().tolist()
        if UNKNOWN_VALUE in x:
            x.remove(UNKNOWN_VALUE)
        return x

    @property
    def function_groups(self) -> List[str]:
        x = self.components_df["Function Group"].dropna().unique().tolist()
        if UNKNOWN_VALUE in x:
            x.remove(UNKNOWN_VALUE)
        return x

    @property
    def locations(self) -> List[str]:
        x = self.relationships_df["Location"].dropna().unique().tolist()
        if UNKNOWN_VALUE in x:
            x.remove(UNKNOWN_VALUE)
        return x

    @property
    def standards(self) -> List[str]:
        x = self.relationships_df["Standard"].dropna().unique().tolist()
        if UNKNOWN_VALUE in x:
            x.remove(UNKNOWN_VALUE)
        return x

    @property
    def mechanisms(self) -> List[str]:
        x = self.relationships_df["Mechanism"].dropna().unique().tolist()
        if UNKNOWN_VALUE in x:
            x.remove(UNKNOWN_VALUE)
        return x

    def __repr__(self) -> str:
        PROPERTY_LIST = ["providers", "vendors", "components"]
        MAX_N = 10

        def _str_from_list(
            _list: Collection[Any], _max_n: int = MAX_N, _list_delim: str = "\n - "
        ) -> str:

            if len(_list) <= _max_n:
                return _list_delim + _list_delim.join(_list)
            else:
                return f"{len(_list)}"

        def _property_summary(prop_name: str, _name_str_len: int) -> str:
            _name = " " + prop_name.capitalize().format(width=_name_str_len) + ": "
            _values = f"{_str_from_list(getattr(self,prop_name))}"

            return _name + _values

        len_prop = max([len(x) for x in PROPERTY_LIST])

        _s = "Stack Object:\n" + "\n".join(
            [_property_summary(x, len_prop) for x in PROPERTY_LIST]
        )
        return _s

    def add_cluster(
        self,
        cluster_field: str,
        bgcolor: Union[
            Collection[str], Collection[Union[str, Mapping[Any, str]]]
        ] = DEFAULT_COLORRAMP,
        level: int = 1,
        drop_vals: Collection = ["TO CONFIRM"],
    ):
        """[summary]

        Args:
            cluster_field (str): [description]
            bgcolor: either
                a list of hex colors to use for background which will be randomly assigned, or
                a tuple with first value the field name and second value a
                dictionary mapping {'field_value':'#hexcode'}
            level: cluster depth level. Defaults to 1.
            drop_vals: list of values that don't mean things are in a cluster together
                other than NA. Defaults to ['TO CONFIRM']

        Raises:
            ValueError: [description]
        """

        if cluster_field in self.clusters.keys():
            raise ValueError(f"{cluster_field} already a cluster.")

        _cluster = (
            self.components_df.groupby([cluster_field])[cluster_field]
            .agg("count")
            .to_frame("n")
            .reset_index()
        )
        _cluster = _cluster.rename(columns={cluster_field: "category"})
        _cluster = _cluster[~_cluster.category.isin(drop_vals)]

        _cluster["bgcolor"] = DEFAULT_BGCOLOR

        if type(bgcolor) is list:
            _cluster["bgcolor"] = color_ramp(
                bgcolor,
                quantity=len(_cluster),
            )

        elif type(bgcolor) is dict:
            _cluster["bgcolor"] = _cluster.category.map(bgcolor)

        _cluster["labeljust"] = "c"
        _cluster["pencolor"] = "#ffffff"
        _cluster["fontcolor"] = _cluster["bgcolor"].apply(contrast_color)

        def _adjust_label(row):
            MAX_LENGTH = 20
            if row.n > 4:
                return row.category
            if len(row.category) <= MAX_LENGTH:
                return row.category
            wrap_list = textwrap.wrap(row.category, row.n * MAX_LENGTH)
            if len(wrap_list) == 1 and type(wrap_list) == list:
                return wrap_list[0]
            html_label = "<" + "</br>".join(wrap_list) + ">"
            return html_label

        # TODO
        # commenting this out for now because it was becoming
        # complicated to link up with relationships
        # _cluster["label"] = _cluster.apply(_adjust_label, axis=1)
        _cluster = _cluster.drop(columns=["n"])
        # print(_cluster)
        # margins are in points for clusters (!)
        h_margin = 20
        v_margin = 20
        _cluster["margin"] = f'{h_margin}",{v_margin}"'
        if level == 1:
            _cluster["fontsize"] = "24"
        else:
            _cluster["fontsize"] = "20"

        _cluster.set_index("category")

        self.clusters[cluster_field] = _cluster


def _cluster_attrs(cluster_df: pd.DataFrame, category: Any) -> Mapping[str, Any]:
    """
    Given a clustering field name and category, return a dictionary of attributes.

    Args:
        cluster ([type]): Cluster dataframe
        category ([type]): Category within the cluster

    Returns:
        Dictionary of attributes for GraphViz
    """
    # print("category:",category,"Cluster_df\n",cluster_df,)

    _attrs = cluster_df[cluster_df.category == category].to_dict("records")[0]
    del _attrs["category"]

    return _attrs


def stack_diagram(
    stack: Stack,
    cluster_level_1: str = None,
    cluster_level_2: str = None,
    verbose: bool = False,
    bgcolor_cluster_L1: Union[
        Collection[str], Collection[Union[str, Mapping[Any, str]]]
    ] = DEFAULT_COLORRAMP,
    bgcolor_cluster_L2: Union[
        Collection[str], Collection[Union[str, Mapping[Any, str]]]
    ] = DEFAULT_COLORRAMP,
) -> Diagram:
    """[summary]

    Args:
        stack: Stack instance.
        cluster_level_1: First level cluster. Defaults to None.
        cluster_level_2: Second level cluster. Defaults to None.
        bgcolor_cluster_L1: for the first cluster tier, either
                a list of hex colors to use for background which will be randomly assigned, or
                a tuple with first value the field name and second value a
                dictionary mapping {'field_value':'#hexcode'}
        bgcolor_cluster_L2: fr the second cluster tier, either
                a list of hex colors to use for background which will be randomly assigned, or
                a tuple with first value the field name and second value a
                dictionary mapping {'field_value':'#hexcode'}

            If none, will use default.

    Returns:
        Diagram: [description]
    """
    components = {}
    cluster_components = {}
    clusters = {}

    stack.add_cluster(cluster_level_1, bgcolor=bgcolor_cluster_L1, level=1)
    stack.add_cluster(cluster_level_2, bgcolor=bgcolor_cluster_L2, level=2)

    c1_df = stack.clusters[cluster_level_1]
    c2_df = stack.clusters[cluster_level_2]

    _comp_df = stack.components_df.copy()

    with Diagram("Stack Diagram - Functional View", direction="LR") as _stack_d:

        for _, row_c1 in c1_df.iterrows():
            if verbose:
                print(f"CLUSTER 1: {row_c1.category}")
            cluster_components[row_c1.category] = {}
            _comp_c1_df = _comp_df.loc[_comp_df[cluster_level_1] == row_c1.category]

            with Cluster(
                row_c1.category, graph_attr=_cluster_attrs(c1_df, row_c1.category)
            ) as clusters[(row_c1.category, None)]:
                # clusters[(c1,None)].dot.attr(**_cluster_attrs(c1_df, c1))
                _c2_in_c1 = _comp_c1_df[cluster_level_2].dropna().unique().tolist()
                for _, row_c2 in c2_df.loc[c2_df.category.isin(_c2_in_c1)].iterrows():

                    if verbose:
                        print(f"CLUSTER 2: {row_c2.category}")

                    cluster_components[row_c1.category][row_c2.category] = {}
                    _comp_c2_df = _comp_c1_df.loc[
                        stack.components_df[cluster_level_2] == row_c2.category
                    ]

                    with Cluster(row_c2.category) as clusters[
                        (row_c1.category, row_c2.category)
                    ]:
                        clusters[(row_c1.category, row_c2.category)].dot.attr(
                            **_cluster_attrs(c2_df, row_c2.category)
                        )
                        for _, row in _comp_c2_df.iterrows():
                            _n = define_node(row)
                            cluster_components[row_c1.category][row_c2.category] = _n
                            components[row.Component] = _n
                        if verbose:
                            print(f"//CLUSTER 2: {row_c2.category}")

                if verbose:
                    print(f"CLUSTER 1 - NO CLUSTER 2: {row_c1.category}")

                for _, row in _comp_c1_df.loc[
                    _comp_c1_df[cluster_level_2].isna()
                ].iterrows():

                    _n = define_node(row=row)
                    cluster_components[row_c1.category][None] = _n
                    components[row.Component] = _n

                if verbose:
                    print(f"//CLUSTER 1: {row_c1.category}")

        unclustered_c = list(
            set(stack.components_df.Component.dropna().unique().tolist())
            - set(components.keys())
        )
        _df_no_c = stack.components_df.loc[
            stack.components_df.Component.isin(unclustered_c)
        ]
        for _, row in _df_no_c.iterrows():
            components[row.Component] = define_node(row)

        for (a, b), edge in relationships_to_edges(stack.relationships_df).items():
            components[a] >> edge >> components[b]

        return _stack_d


def add_df(base_df, add_df, key, exclude_prefix=EXCLUDE_PREFIX, exclude=[]):
    """[summary]

    Args:
        base_df ([type]): [description]
        add_df ([type]): [description]
        key ([type]): [description]
        exclude_prefix (str, optional): [description]. Defaults to "_".
        exclude (list, optional): [description]. Defaults to [].
    """
    key_list = [key] if type(key) == str else key

    # don't add fields already there
    _exclude = [f for f in base_df.columns if f in add_df.columns and f not in key_list]

    # don't add fields marked as private
    _exclude += [f for f in add_df.columns if f.startswith(exclude_prefix)]

    # don't add explicitly excluded fields
    _exclude += exclude

    return base_df.merge(add_df.drop(_exclude, axis=1), on=key, how="left")
