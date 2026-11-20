import pandas as pd
import sys
from pathlib import Path

# Add dbt project root to Python path
import python.setup
from python.calculate_order_total import calculate_order_item_amount


def model(dbt, session):
    dbt.config(materialized="table")

    # Read upstream model
    order_items = dbt.ref("stg_order_items")

    # Convert to Pandas DataFrame
    # order_items = order_items.to_pandas()
    order_items = order_items.df()

    # Calculate order item amount
    # order_items["order_item_amount"] = (
    #    order_items["unit_price"] * order_items["quantity"]
    # )

    order_items = calculate_order_item_amount(order_items)

    # Aggregate by order_id
    orders = (
        order_items
        .groupby("order_id")
        .agg(
            total_order_amount=("order_item_amount", "sum"),
            total_quantity=("quantity", "sum"),
            total_order_items=("order_item_id", "count")
        )
        .reset_index()
    )

    return orders
