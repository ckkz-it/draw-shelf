import os
import pathlib
import re

import yaml
from dotenv import load_dotenv

from app.helpers.utils import Map

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'main.yaml'

load_dotenv(dotenv_path=BASE_DIR / '.env')

FROM_ENV_RE = re.compile(r'\(\(\w+\)\)')


def parse_env_placeholders(content: str) -> str:
    def replace(match: re.Match):
        value = match.group().strip('() ')
        return os.getenv(value)

    return FROM_ENV_RE.sub(replace, content)


def get_config(path: str) -> Map:
    with open(path) as f:
        content = f.read()
        parsed = parse_env_placeholders(content)
        cfg = yaml.safe_load(parsed)
    return Map(cfg)


config = get_config(config_path)
