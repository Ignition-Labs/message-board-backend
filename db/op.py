from db import models
from sqlalchemy import and_, func
import logging
import random
from typing import List

logger = logging.getLogger(__name__)

# address must be checksum
def query_msg_by_address_and_code(code: str, address: str):
    record = models.session.query(models.Msg).filter(
        and_(
            models.Msg.code == code,
            models.Msg.address == None,
            models.Msg.expire == False
        )
    ).first()
    if record:
        models.session.query(models.Msg).filter(
            and_(
                models.Msg.code == code,
                models.Msg.address == None,
                models.Msg.expire == False
            )
        ).update(
            {
                "address": address,
            },
            # synchronize_session=False
        )
        models.session.commit()

    result = models.session.query(
                models.Msg,
            ).filter(
                and_(
                    models.Msg.address == address,
                    models.Msg.code == code,
                    models.Msg.expire == False
                )
            ).all()
    
    msg = None
    if len(result) > 1:
        logger.error(f"db query error: {result}")
    elif len(result) != 0:
        msg = {'name': result[0].name, 'avatar': result[0].avatar, 'content': result[0].content, 'region': result[0].region}
        
    models.session.close()
    return msg


def qeury_mappings_by_code(code: str, address: str):
    record = models.session.query(models.Msg).filter(
        and_(
            models.Mapping.code == code,
            models.Msg.address == address,
            models.Msg.expire == False
        )
    ).first()
    if not record:
        return None
    
    results = models.session.query(
                models.Msg
            ).join(
                models.Mapping,
                and_(models.Msg.code == models.Mapping.code_connected,
                     models.Mapping.code == code,
                     )).all()
    msgs_connected = [{'name': res.name, 'avatar': res.avatar, 'content': res.content, 'region': res.region} for res in results]
    return msgs_connected


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


def random_choose_mapping(code: str):
    results = models.session.query(models.Msg).filter(models.Msg.code != code).order_by(func.random()).limit(5).all()
    models.session.close()
    codes = [res.code for res in results]
    print(f"results: {codes}")
    return codes


def all_codes():
    results = models.session.query(models.Msg.code).all()
    models.session.close()
    return [res.code for res in results]


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


def qeury_code_connected_by_code(code: str):
    results = models.session.query(
                models.Mapping,
            ).filter(
                and_(
                    models.Mapping.code == code,
                )
            ).all()

    models.session.close()
    return [res.code_connected for res in results]


def update_address(code: str, address: str):
    models.session.query(models.Msg)\
        .filter_by(
            and_(
                models.Msg.code == code,
                models.Msg.expire == False
            )
        )\
        .update(
            {
                "address": address,
            },
            # synchronize_session=False
        )
    models.session.commit()
    models.session.close()


def update_content(code: str, address: str, content: str = None):
    models.session.query(models.Msg)\
        .filter(
            and_(
                models.Msg.code == code,
                models.Msg.address == address,
                models.Msg.expire == False
            )
        )\
        .update(
            {
                "content": content,
            },
            # synchronize_session=False
        )
    models.session.commit()
    models.session.close()


def update_region(code: str, address: str, region: str = None):
    models.session.query(models.Msg)\
        .filter(
            and_(
                models.Msg.code == code,
                models.Msg.address == address,
                models.Msg.expire == False
            )
        )\
        .update(
            {
                "region": region,
            },
            # synchronize_session=False
        )
    models.session.commit()
    models.session.close()


def update_name(code: str, address: str, name: str = None):
    models.session.query(models.Msg)\
        .filter(
            and_(
                models.Msg.code == code,
                models.Msg.address == address,
                models.Msg.expire == False
            )
        )\
        .update(
            {
                "name": name,
            },
            # synchronize_session=False
        )
    models.session.commit()
    models.session.close()


def update_avatar(code: str, address: str, avatar: str = None):
    models.session.query(models.Msg)\
        .filter(
            and_(
                models.Msg.code == code,
                models.Msg.address == address,
                models.Msg.expire == False
            )
        )\
        .update(
            {
                "avatar": avatar,
            },
            # synchronize_session=False
        )
    models.session.commit()
    models.session.close()