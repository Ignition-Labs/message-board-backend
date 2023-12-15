from db import models
from sqlalchemy import and_
import logging
import random

logger = logging.getLogger(__name__)

# address must be checksum
def query_by_address(address: str):
    result = models.session.query(
                models.Msg,
            ).filter(
                and_(
                    models.Msg.code == address,
                    models.Msg.expire == False
                )
            ).all()
    
    msg = None
    if len(result) > 1:
        logger.error(f"db query error: {result}")
    elif len(result) != 0:
        msg = result[0]

    models.session.close()
    return msg


def add_msg(code: str, address: str, region: str = None, name: str = None, avatar: str = None):
    inst = models.Msg(
        code = code,
        address = address,
        region = region,
        name = name,
        avatar = avatar
    )
    models.session.add(inst)
    models.session.commit()
    models.session.close()


def add_many_random_mapping(code):
    pass