from __future__ import annotations

import argparse
import pathlib


SQL_ORDER = [
    "001_database_setup.sql",
    "002_schema.sql",
    "003_seed_golden_cases.sql",
    "004_seed_evaluation_cases.sql",
    "005_scan_billing_variances.sql",
    "006_get_pricing_evidence.sql",
    "007_get_commercial_exceptions.sql",
    "008_create_investigation_case.sql",
    "009_case_evidence.sql",
    "010_review_actions.sql",
    "011_run_audit.sql",
    "012_ground_truth.sql",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parents[1]
    sql_dir = root / "sql"
    for filename in SQL_ORDER:
        path = sql_dir / filename
        print(f"-- {path}")
        if args.dry_run:
            print(path.read_text(encoding="utf-8")[:500].rstrip())
            print()
    if not args.dry_run:
        print("Live execution pending Snowflake account validation. Use SnowSQL, Snowsight worksheets, or extend this script with approved connector credentials.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

