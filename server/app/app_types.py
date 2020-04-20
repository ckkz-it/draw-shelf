import typing
from enum import Enum

from aiopg.sa.result import ResultProxy, RowProxy


class FETCH(Enum):
    all = 'all'
    one = 'one'


DB_EXECUTE_RESULT = typing.Union[typing.List[RowProxy], typing.Optional[RowProxy], ResultProxy]
