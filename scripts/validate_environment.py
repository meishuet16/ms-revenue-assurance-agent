from __future__ import annotations

import os
from collections.abc import Mapping


REQUIRED = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_WAREHOUSE",
    "SNOWFLAKE_DATABASE",
    "SNOWFLAKE_SCHEMA",
]

DIAGNOSTIC_KEYS = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_AUTHENTICATOR",
    "SNOWFLAKE_PASSWORD",
    "SNOWFLAKE_ROLE",
    "SNOWFLAKE_WAREHOUSE",
    "SNOWFLAKE_DATABASE",
    "SNOWFLAKE_SCHEMA",
    "SNOWFLAKE_DASHBOARD_MODE",
]


def _present(env: Mapping[str, str], name: str) -> bool:
    return bool(env.get(name, "").strip())


def missing_environment_variables(env: Mapping[str, str] = os.environ) -> list[str]:
    missing = [name for name in REQUIRED if not _present(env, name)]
    uses_external_browser = env.get("SNOWFLAKE_AUTHENTICATOR", "").strip() == "externalbrowser"
    if not uses_external_browser and not _present(env, "SNOWFLAKE_PASSWORD"):
        missing.append("SNOWFLAKE_PASSWORD or SNOWFLAKE_AUTHENTICATOR=externalbrowser")
    return missing


def describe_environment(env: Mapping[str, str] = os.environ) -> list[str]:
    rows: list[str] = []
    for name in DIAGNOSTIC_KEYS:
        value = env.get(name, "")
        if name == "SNOWFLAKE_PASSWORD":
            rows.append(f"{name}=<hidden>, length={len(value)}")
            continue
        display = value.strip() if isinstance(value, str) else str(value)
        rows.append(f"{name}={display or '<unset>'}, length={len(value)}")
    return rows


def main() -> int:
    print("Snowflake environment summary:")
    for row in describe_environment():
        print(f"- {row}")

    missing = missing_environment_variables()
    if missing:
        print("Snowflake live validation pending. Missing environment variables:")
        for name in missing:
            print(f"- {name}")
        return 1
    print("Snowflake environment variables are present. Run scripts/verify_database.py for live checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
