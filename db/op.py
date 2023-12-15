from db import models


def gen_code(address: str, region: str = None, name: str = None, avatar: str = None):
    code = models.