from __future__ import annotations

import os


REQUIRED = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
    "SNOWFLAKE_WAREHOUSE",
    "SNOWFLAKE_DATABASE",
    "SNOWFLAKE_SCHEMA",
]


def main() -> int:
    missing = [name for name in REQUIRED if not os.getenv(name)]
    if missing:
        print("Snowflake live validation pending. Missing environment variables:")
        for name in missing:
            print(f"- {name}")
        return 1
    print("Snowflake environment variables are present. Run scripts/verify_database.py for live checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

