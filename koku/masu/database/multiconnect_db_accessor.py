#
# Copyright 2020 Red Hat, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Accessor for Shared information across multiple DB connections."""
import logging
import os

import psycopg2
from psycopg2.extras import RealDictCursor

from koku import database


LOG = logging.getLogger(__name__)


class NotFoundError(Exception):
    pass


class MCDBAccessor:
    """
    Multiple Connection DBAccessor
    This is designed to make a new autocommit connection
    in order to set data that is to be accessed by multiple connections/processes
    """

    def __init__(self, schema="public"):
        self.schema = schema
        self.conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def _build_dsn_url(self):
        db_cfg = database.config()
        url = f'postgresql://{db_cfg["USER"]}:{db_cfg["PASSWORD"]}@{db_cfg["HOST"]}:{db_cfg["PORT"]}/{db_cfg["NAME"]}'
        return url

    def _set_schema(self):
        sql = f"""set search_path = {self.schema}{", public" if self.schema != 'public' else ""};"""
        self.execute(sql)

    def set_schema(self, schema):
        if not schema:
            return None
        if self.schema != schema:
            self.schema = schema
        self._set_schema()

    def connect(self):
        try:
            self.close()
        except Exception:
            pass

        self.conn = psycopg2.connect(self._build_dsn_url(), cursor_factory=RealDictCursor)
        self.conn.autocommit = True
        self._set_schema()

    def close(self):
        self.rollback()
        if self.conn is not None and not self.conn.closed:
            self.conn.close()

    def execute(self, sql, values=None):
        cur = self.conn.cursor()
        LOG.debug(f"SQL: {cur.mogrify(sql, values).decode('utf-8')}")
        cur.execute(sql, values)
        return cur

    def rollback(self):
        if self.conn is not None and not self.conn.closed:
            self.conn.rollback()

    def _build_values_sql(self, values):
        return f"""VALUES ( {', '.join(f"%({c})s" for c in values)} )"""

    def _build_returning_sql(self, cols=["*"]):
        if not cols:
            return ""

        if isinstance(cols, str):
            cols = [c.strip() for c in cols.split(",")]

        if "*" in cols:
            return "RETURNING *"
        else:
            return f"""RETURNING ( {", ".join(f'"{c}"' for c in cols)} )"""

    def _build_insert_sql(self, table_name, values, end=";", returning=["*"]):
        table_cols = ",".join(f'"{c}"' for c in values)
        sql = f"""
INSERT INTO "{table_name}" ({table_cols})
{self._build_values_sql(values)}
{self._build_returning_sql(returning)}
{end}"""
        return sql

    def insert(self, table_name, cols, values, returning=["*"]):
        sql = self._build_insert_sql(table_name, values, returning=returning)
        cur = self.execute(sql, values)
        if returning:
            res = cur.fetchone()
            if res and len(returning) == 1:
                res = res[returning[0]]
        else:
            res = cur.rowcount

        return res

    def _build_insert_on_conflict_do_nothing_sql(self, table_name, values, conflict_cols, returning=["*"]):
        sql = self._build_insert_sql(table_name, values, end="", returning=None)

        if isinstance(conflict_cols, str):
            conflict_cols = [c.strip() for c in conflict_cols.split(",")]

        sql += f"""
ON CONFLICT ( {", ".join(f'"{c}"' for c in conflict_cols)} )
DO NOTHING
{self._build_returning_sql(returning)}
;"""
        return sql

    def insert_on_conflict_do_nothing(self, table_name, values, conflict_cols, returning=["*"]):
        sql = self._build_insert_on_conflict_do_nothing_sql(table_name, values, conflict_cols, returning)
        cur = self.execute(sql, values)
        if returning:
            res = cur.fetchone()
            if res and len(returning == 1):
                res = res[returning[0]]
        else:
            res = cur.rowcount

        if not res:
            res = self._get_record(table_name, returning, {c: values[c] for c in conflict_cols})
            if len(returning) == 1:
                res = res[returning[0]]

        return res

    def _get_record(self, table_name, select_cols, where_data, exc_on_not_found=True):
        table_cols = ",".join(f'"{c}"' for c in select_cols) if "*" not in select_cols else "*"
        sql = f"""
SELECT {table_cols}
  FROM "{table_name}"
 WHERE {os.linesep.join(f'"{c}" = %({c})s' for c in where_data)}
;"""
        rec = self.execute(sql, where_data).fetchone()
        if rec is None and exc_on_not_found:
            msg = f"""Row in "{table_name}" does not exist in the database. Failed row data: {where_data}"""
            LOG.error(msg)
            raise NotFoundError(msg)

        return rec
