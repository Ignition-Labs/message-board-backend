from db import models
from sqlalchemy import and_
import logging
import random
from typing import List

logger = logging.getLogger(__name__)

# address must be checksum
def query_by_address(address: str):
    result = models.session.query(
                models.Msg,
            ).filter(
                and_(
                    models.Msg.address == address,
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


def add_msg(code: str, address: str = None, region: str = None, name: str = None, avatar: str = None):
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


def add_many_random_mapping(code: str, codes_connected: List[str]):
    insts = []
    for code_c in codes_connected:
        insts.append(models.Mapping(
            code = code,
            code_connected = code_c
        ))
    
    models.session.add_all(insts)
    models.session.commit()
    models.session.close()


def qeury_mappings_by_code(code: str):
    result = models.session.query(
                models.Mapping,
            ).filter(
                and_(
                    models.Mapping.code == code,
                )
            ).all()    

    models.session.close()
    return result


def update_profile(address: str, name: str = None, avatar: str = None):
    models.session.query(models.Msg)\
        .filter_by(address=address)\
        .update(
            {
                "name": name,
                "avatar": avatar
            },
            # synchronize_session=False
        )
    models.session.commit()
    models.session.close()

