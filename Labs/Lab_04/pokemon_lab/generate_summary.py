#!/usr/bin/env python3

import os
import sys
from typing import NoReturn

import pandas as pd


REQUIRED_COLUMNS = {"card_market_value", "card_name", "card_id"}


def _die(msg: str, code: int = 1) -> NoReturn:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


def generate_summary(portfolio_file: str) -> None:
    if not os.path.exists(portfolio_file):
        _die(f"Portfolio file not found: {portfolio_file}")

    try:
        df = pd.read_csv(portfolio_file)
    except Exception as e:
        _die(f"Failed to read CSV '{portfolio_file}': {e}")

    if df.empty:
        print(f"No data found in '{portfolio_file}'. Nothing to report.")
        return

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        _die(
            f"Missing required column(s) in '{portfolio_file}': {', '.join(sorted(missing))}"
        )

    df["card_market_value"] = pd.to_numeric(df["card_market_value"], errors="coerce")

    if df["card_market_value"].isna().all():
        print(
            f"Column 'card_market_value' in '{portfolio_file}' contains no numeric values. Nothing to report."
        )
        return

    df["card_market_value"] = df["card_market_value"].fillna(0.0)

    total_portfolio_value = df["card_market_value"].sum()

    max_idx = df["card_market_value"].idxmax()
    most_valuable_card = df.loc[max_idx]

    print("=== Portfolio Summary ===")
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}\n")

    print("Most Valuable Card:")
    print(f"  Name        : {most_valuable_card['card_name']}")
    print(f"  ID          : {most_valuable_card['card_id']}")
    print(f"  Market Price: ${most_valuable_card['card_market_value']:,.2f}")


def main() -> None:
    """Public interface: run against production portfolio file."""
    generate_summary("card_portfolio.csv")


def test() -> None:
    """Public interface: run against test portfolio file."""
    generate_summary("test_card_portfolio.csv")


if __name__ == "__main__":
    test()