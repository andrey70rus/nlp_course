from os import getenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_ID: int = int(getenv('API_ID'))
    API_HASH: str = getenv('API_HASH')
    PHONE: str = getenv('PHONE')
    USERNAME: str = getenv('USERNAME')
