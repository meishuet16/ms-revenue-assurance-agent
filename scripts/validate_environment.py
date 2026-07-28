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


def _present(env: Mapping[str, str], name: str) -> bool:
    return bool(env.get(name, "").strip())


def missing_environment_variables(env: Mapping[str, str] = os.environ) -> list[str]:
    missing = [name for name in REQUIRED if not _present(env, name)]
    uses_external_browser = env.get("SNOWFLAKE_AUTHENTICATOR", "").strip() == "externalbrowser"
    if not uses_external_browser and not _present(env, "SNOWFLAKE_PASSWORD"):
        missing.append("SNOWFLAKE_PASSWORD or SNOWFLAKE_AUTHENTICATOR=externalbrowser")
    return missing


def main() -> int:
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
