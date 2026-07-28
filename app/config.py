from __future__ import annotations

import os
from dataclasses import dataclass
from collections.abc import Mapping


def _clean(value: str | None, default: str | None = None) -> str | None:
    if value is None:
        return default
    cleaned = value.strip()
    return cleaned or default


@dataclass(frozen=True)
class Settings:
    account: str | None = None
    user: str | None = None
    password: str | None = None
    authenticator: str | None = None
    role: str | None = None
    warehouse: str = "RA_WH"
    database: str = "REVENUE_ASSURANCE"
    schema: str = "PUBLIC"
    dashboard_mode: str = "fixture"

    @classmethod
    def from_env(cls, env: Mapping[str, str] = os.environ) -> "Settings":
        return cls(
            account=_clean(env.get("SNOWFLAKE_ACCOUNT")),
            user=_clean(env.get("SNOWFLAKE_USER")),
            password=_clean(env.get("SNOWFLAKE_PASSWORD")),
            authenticator=_clean(env.get("SNOWFLAKE_AUTHENTICATOR")),
            role=_clean(env.get("SNOWFLAKE_ROLE")),
            warehouse=_clean(env.get("SNOWFLAKE_WAREHOUSE"), "RA_WH") or "RA_WH",
            database=_clean(env.get("SNOWFLAKE_DATABASE"), "REVENUE_ASSURANCE") or "REVENUE_ASSURANCE",
            schema=_clean(env.get("SNOWFLAKE_SCHEMA"), "PUBLIC") or "PUBLIC",
            dashboard_mode=(_clean(env.get("SNOWFLAKE_DASHBOARD_MODE"), "fixture") or "fixture").lower(),
        )

    @property
    def has_snowflake_credentials(self) -> bool:
        has_browser_auth = self.authenticator == "externalbrowser"
        return bool(self.account and self.user and (self.password or has_browser_auth))

    @property
    def live_dashboard_requested(self) -> bool:
        return self.dashboard_mode == "live"


settings = Settings.from_env()
