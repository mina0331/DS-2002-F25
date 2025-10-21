#!/usr/bin/env python3


import json
import os
import sys
from typing import List

import pandas as pd


def _load_lookup_data(lookup_dir: str) -> pd.DataFrame:
    if not os.path.isdir(lookup_dir):
        print(f"[lookup] Directory not found: {lookup_dir}", file=sys.stderr)
        return pd.DataFrame()

    all_lookup_df: List[pd.DataFrame] = []

    for fname in os.listdir(lookup_dir):
        if not fname.lower().endswith(".json"):
            continue

        fpath = os.path.join(lookup_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[lookup] Skipping '{fpath}': {e}", file=sys.stderr)
            continue

        records = data.get("data", [])
        if not isinstance(records, list) or not records:
            print(f"[lookup] No 'data' records in {fpath}", file=sys.stderr)
            continue

        df = pd.json_normalize(records)

        holo_col = "tcgplayer.prices.holofoil.market"
        norm_col = "tcgplayer.prices.normal.market"
        df["card_market_value"] = (
            pd.to_numeric(df.get(holo_col), errors="coerce")
            .fillna(pd.to_numeric(df.get(norm_col), errors="coerce"))
            .fillna(0.0)
        )

        rename_map = {
            "id": "card_id",
            "name": "card_name",
            "number": "card_number",
            "set.id": "set_id",
            "set.name": "set_name",
        }
        df = df.rename(columns=rename_map)

        required_cols = [
            "card_id",
            "card_name",
            "card_number",
            "set_id",
            "set_name",
            "card_market_value",
        ]

        present = [c for c in required_cols if c in df.columns]
        if not present:
            print(f"[lookup] Required columns missing in {fpath}; skipping.", file=sys.stderr)
            continue

        all_lookup_df.append(df[present].copy())

    if not all_lookup_df:
        print("[lookup] No usable JSON files found.", file=sys.stderr)
        return pd.DataFrame(columns=[
            "card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"
        ])

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    lookup_df = lookup_df.sort_values(["card_id", "card_market_value"], ascending=[True, False])
    lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first").reset_index(drop=True)

    for col in ["card_id", "card_name", "card_number", "set_id", "set_name"]:
        if col in lookup_df.columns:
            lookup_df[col] = lookup_df[col].astype(str).str.strip()
    lookup_df["card_market_value"] = pd.to_numeric(lookup_df["card_market_value"], errors="coerce").fillna(0.0)

    return lookup_df


def _load_inventory_data(inventory_dir: str) -> pd.DataFrame:
    if not os.path.isdir(inventory_dir):
        print(f"[inventory] Directory not found: {inventory_dir}", file=sys.stderr)
        return pd.DataFrame()

    inventory_dfs: List[pd.DataFrame] = []

    for fname in os.listdir(inventory_dir):
        if not fname.lower().endswith(".csv"):
            continue
        fpath = os.path.join(inventory_dir, fname)
        try:
            df = pd.read_csv(fpath)
        except Exception as e:
            print(f"[inventory] Skipping '{fpath}': {e}", file=sys.stderr)
            continue

        inventory_dfs.append(df)

    if not inventory_dfs:
        print("[inventory] No CSV files found.", file=sys.stderr)
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_dfs, ignore_index=True)

    # Stringify and strip to create a stable key
    for col in ["set_id", "card_number"]:
        if col not in inventory_df.columns:
            inventory_df[col] = ""
        inventory_df[col] = inventory_df[col].astype(str).str.strip()

    inventory_df["card_id"] = inventory_df["set_id"] + "-" + inventory_df["card_number"]

    return inventory_df

def update_portfolio(inventory_dir: str, lookup_dir: str, output_file: str) -> None:
    
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    required_output_headers = [
        "index",
        "binder_name",
        "page_number",
        "slot_number",
        "set_id",
        "set_name",
        "card_number",
        "card_id",
        "card_name",
        "card_market_value",
    ]

    if inventory_df.empty:
        pd.DataFrame(columns=required_output_headers).to_csv(output_file, index=False)
        print(f"[portfolio] Inventory empty. Wrote empty portfolio to '{output_file}'.", file=sys.stderr)
        return

    merge_cols = ["card_id", "card_name", "set_name", "card_market_value"]
    for c in merge_cols:
        if c not in lookup_df.columns:
            lookup_df[c] = pd.Series(dtype="object" if c != "card_market_value" else "float")

    merged = pd.merge(
        inventory_df,
        lookup_df[merge_cols],
        on="card_id",
        how="left",
        validate="many_to_one", 
    )

    if "card_market_value" not in merged.columns:
        merged["card_market_value"] = 0.0
    merged["card_market_value"] = pd.to_numeric(merged["card_market_value"], errors="coerce").fillna(0.0)

    if "set_name" not in merged.columns:
        merged["set_name"] = "NOT_FOUND"
    merged["set_name"] = merged["set_name"].fillna("NOT_FOUND")

    for col in ["binder_name", "page_number", "slot_number"]:
        if col not in merged.columns:
            merged[col] = ""

    merged["binder_name"] = merged["binder_name"].astype(str).str.strip()
    merged["page_number"] = merged["page_number"].astype(str).str.strip()
    merged["slot_number"] = merged["slot_number"].astype(str).str.strip()

    merged["index"] = (
        merged["binder_name"].fillna("")
        + "-"
        + merged["page_number"].fillna("")
        + "-"
        + merged["slot_number"].fillna("")
    ).str.strip("-")

    for col in ["set_id", "card_number", "card_id", "card_name"]:
        if col not in merged.columns:
            merged[col] = "" if col != "card_market_value" else 0.0
        merged[col] = merged[col].astype(str).str.strip() if col != "card_market_value" else merged[col]

    final_cols = [
        "index",
        "binder_name",
        "page_number",
        "slot_number",
        "set_id",
        "set_name",
        "card_number",
        "card_id",
        "card_name",
        "card_market_value",
    ]

    out_df = merged[final_cols].copy()

    out_df.to_csv(output_file, index=False)
    print(f"[portfolio] Wrote {len(out_df):,} rows to '{output_file}'.", file=sys.stderr)

def main() -> None:
    update_portfolio(
        inventory_dir="./card_inventory/",
        lookup_dir="./card_set_lookup/",
        output_file="card_portfolio.csv",
    )


def test() -> None:
    update_portfolio(
        inventory_dir="./card_inventory_test/",
        lookup_dir="./card_set_lookup_test/",
        output_file="test_card_portfolio.csv",
    )


if __name__ == "__main__":
    print("[INFO] Starting update_portfolio.py in Test Mode...", file=sys.stderr)
    test()