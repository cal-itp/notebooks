from datetime import date
from dateutil.relativedelta import relativedelta

import numpy as np
import pandas as pd

from diagrams import Node
from . import components

EXPIRATION_NOTIFY_MONTHS = 6
DEFAULT_NODE_CLASS = components.Default

component_to_node_class = {
    "Mobile ticketing": components.Mobileticketing,
    "Scheduling": components.Scheduling,
    "Scheduling (Fixed-route)": components.Scheduling,
    "GTFS generation": components.Gtfs,
    "Run cutting": components.Cloudsoftware,
    "Driver Assignment": components.Cloudsoftware,
    "Computer Automated Dispatch": components.Cloudsoftware,
    "Location Sensors": components.Gps,
    "AVL On-board Computer": components.Onboardcomputer,
    "AVL Software": components.Cloudsoftware,
    "APC Sensors": components.Onboardsensor,
    "APC On-Board Computer": components.Onboardcomputer,
    "APC Software": components.Cloudsoftware,
    "Consolidated Reporting": components.Cloudsoftware,
    "Vehicle Logic Unit": components.Onboardcomputer,
    "Over-air communications": components.Overaircoms,
    "Arrival predictions": components.Cloudsoftware,
    "Supervisory control and data acquisition": components.Cloudsoftware,
    "Mobile data terminal": components.Onboardcomputer,
    "Real-time info": components.Cloudsoftware,
    "Web-based trip planner": components.Cloudsoftware,
    "Offboard signage": components.Signage,
    "Service alerts": components.Datastream,
    "Headsigns": components.Signage,
    "Annunciator": components.Audio,
    "Interior signage": components.Signage,
    "Payment processor": components.Payments,
    "Merchant services": components.Payments,
    "Ticket vending machines": components.Ticketing,
    "Farebox": components.Farebox,
    "Reporting": components.Dashboard,
    "Server": components.Server,
    "Transit Atlas": components.Cloudsoftware,
    "Fleet Maintenance": components.Cloudsoftware,
    "Inventory": components.Cloudsoftware,
    "Purchasing": components.Cloudsoftware,
}


def define_node(component: pd.Series, verbose: bool = True) -> Node:
    """[summary]

    Args:
        component: row from Components DataFrame with "Component" field.
        contract_exp: string with contract expiration date.

    Returns:
        A diagrams Node class or subclass.
    """
    # notify if contract expiring
    exp_notify = False
    if (
        component["End date"]
        and component["End date"] != np.NaN
        and str(component["End date"]).lower() not in ["nan", "nat", "na", "none"]
    ):
        exp_notify = date.today() >= pd.to_datetime(
            component["End date"]
        ) - relativedelta(months=+EXPIRATION_NOTIFY_MONTHS)

    notification_str = f"<p>EXPIRES: {component['End date']}</p>" if exp_notify else ""
    node_label = f"{component.Component}\n{notification_str}"
    node_class = component_to_node_class.get(component["Component"], DEFAULT_NODE_CLASS)

    n = node_class(
        node_label,
        # tooltip=,
        # URL=,
        # fontsize=24,
        # style=filled,
        # fontcolor=
        # color=
    )

    return n
