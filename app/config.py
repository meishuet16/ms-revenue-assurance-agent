from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    account: str | None = os.getenv("SNOWFLAKE_ACCOUNT")
    user: str | None = os.getenv("SNOWFLAKE_USER")
    password: str | None = os.getenv("SNOWFLAKE_PASSWORD")
    role: str | None = os.getenv("SNOWFLAKE_ROLE")
    warehouse: str = os.getenv("SNOWFLAKE_WAREHOUSE", "RA_WH")
    database: str = os.getenv("SNOWFLAKE_DATABASE", "REVENUE_ASSURANCE")
    schema: str = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")

    @property
    def has_snowflake_credentials(self) -> bool:
        return bool(self.account and self.user and self.password)


settings = Settings()

