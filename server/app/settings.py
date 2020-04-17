import os
import pathlib
import re

import yaml
from dotenv import load_dotenv

from app.helpers.utils import Map

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'main.yaml'

load_dotenv(dotenv_path=BASE_DIR / '.env')

FROM_ENV_RE = re.compile(r'{{\w+}}')


def get_from_env(name: str):
    value = os.getenv(name)
    if value and value.lower() in ['true', 'false']:
        value = value.lower() == 'true'
    return value


def get_config(path: str) -> Map:
    with open(path) as f:
        cfg = yaml.safe_load(f)

    for name, setting in cfg.items():
        if isinstance(setting, dict):
            for key, value in setting.items():
                from_env = FROM_ENV_RE.match(str(value))
                if from_env:
                    env_key = from_env.group().strip('{}')
                    cfg[name][key] = get_from_env(env_key)
        else:
            from_env = FROM_ENV_RE.match(setting)
            if from_env:
                env_key = from_env.group().strip('{}')
                cfg[name] = get_from_env(env_key)

    return Map(cfg)


config = get_config(config_path)
