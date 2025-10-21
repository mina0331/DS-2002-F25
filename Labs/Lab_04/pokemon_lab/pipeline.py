#!/usr/bin/env python3

import sys

from update_portfolio import main as update_main
from generate_summary import main as summary_main


def run_production_pipeline() -> None:
    """Run the full production pipeline: ETL -> Reporting."""
    print("[START] Running production data pipeline...", file=sys.stderr)

    print("[STEP] ETL: Updating portfolio (update_portfolio.main)...", file=sys.stderr)
    update_main()

    print("[STEP] Reporting: Generating summary (generate_summary.main)...", file=sys.stderr)
    summary_main()

    print("[DONE] Pipeline complete.", file=sys.stderr)


if __name__ == "__main__":
    try:
        run_production_pipeline()
    except Exception as e:
        print(f"[ERROR] Pipeline failed: {e}", file=sys.stderr)
        sys.exit(1)
