
def calculate_order_item_amount(df):
    """
    Calculate order item amount.

    Args:
        df: Pandas DataFrame containing unit_price and quantity.

    Returns:
        Pandas DataFrame with order_item_amount column.
    """

    df["order_item_amount"] = (
        df["unit_price"] * df["quantity"]
    )

    return df
