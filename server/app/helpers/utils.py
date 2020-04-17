import typing
from collections import defaultdict

from aiopg.sa.result import RowProxy


class DBDataParser:
    def __init__(
            self,
            raw_data: typing.Union[RowProxy, typing.List[RowProxy]],
            root_table_names: typing.Sequence[str],
            *,
            many: bool = False,
            table_name_mapping: typing.Dict[str, str] = None
    ):
        self.raw_data = raw_data
        self.root_table_names = root_table_names
        self.many = many
        self.table_name_mapping = table_name_mapping

    def parse(self, *, many: bool = None) -> typing.Union[typing.List[defaultdict], defaultdict]:
        many = self.many if many is None else many
        if many:
            return [self.parse_item(dict(row)) for row in self.raw_data]
        return self.parse_item(dict(self.raw_data))

    def parse_item(self, item: dict) -> defaultdict:
        el = defaultdict(dict)
        for key, value in item.items():
            table_name, dict_key = self._extract_table_name_and_dict_key(key)
            if table_name in self.root_table_names:
                el[dict_key] = value
            else:
                el[table_name][dict_key] = value
        return el

    @property
    def _all_tables(self):
        from app import db
        return list(db.meta.tables)

    def _extract_table_name_and_dict_key(self, key: str) -> typing.Tuple[str, str]:
        for tbl in self._all_tables:
            if key.startswith(tbl):
                key = key.split(tbl + '_')[-1]
                if self.table_name_mapping and tbl in self.table_name_mapping:
                    return self.table_name_mapping[tbl], key
                return tbl, key


class Map(dict):
    def __init__(self, dct):
        super().__init__(dct)
        for key, item in dct.items():
            if isinstance(item, dict):
                item = Map(item)
            self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def __setattr__(self, name, value):
        self.__dict__[name] = value
