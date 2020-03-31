from typing import List
from uuid import uuid4

from sqlalchemy import Table, Column


def stringified_uuid():
    return str(uuid4())


class QueryHelper:
    @staticmethod
    def exclude_fields(table: Table, fields_to_exclude: List[str]) -> List[Column]:
        return [c for c in table.columns if c.name not in fields_to_exclude]

    @staticmethod
    def all_fields(table: Table) -> List[Column]:
        return [c for c in table.columns]
