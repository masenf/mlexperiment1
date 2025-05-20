import functools
import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, Iterator
import databricks.sql
import pandas as pd
import reflex as rx
from databricks.sdk.core import Config

if TYPE_CHECKING:
    from databricks.sql.client import Cursor
    from databricks.sql.parameters.native import (
        TParameterCollection,
    )
databricks_cfg = Config()
databricks_http_path = (
    f"/sql/1.0/warehouses/{databricks_cfg.warehouse_id}"
)


def credentials_provider():
    return databricks_cfg.authenticate


@contextmanager
def databricks_cursor() -> Iterator["Cursor"]:
    with databricks.sql.connect(
        server_hostname=databricks_cfg.host,
        http_path=databricks_http_path,
        catalog=os.environ.get("DATABRICKS_CATALOG"),
        schema=os.environ.get("DATABRICKS_SCHEMA"),
        credentials_provider=credentials_provider,
    ) as connection, connection.cursor() as cursor:
        yield cursor


def sync_query_df(
    query: str,
    parameters: "TParameterCollection | None" = None,
) -> pd.DataFrame:
    with databricks_cursor() as cursor:
        cursor.execute(query, parameters=parameters)
        arrow_table = cursor.fetchall_arrow()
        if arrow_table is None:
            if cursor.description:
                cols = [
                    desc[0] for desc in cursor.description
                ]
                return pd.DataFrame(columns=cols)
            return pd.DataFrame()
        return arrow_table.to_pandas()


async def async_query_df(
    query: str,
    parameters: "TParameterCollection | None" = None,
) -> pd.DataFrame:
    return await rx.run_in_thread(
        functools.partial(sync_query_df, query, parameters)
    )