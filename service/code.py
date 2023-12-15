import random
from db import op
from web3 import Web3
import logging

logger = logging.getLogger(__name__)

def gen_new_code():
    new_code = ""
    for i in range(6):
        new_code += str(random.randint(0, 9))
    op.add_msg(code = new_code, region="TaiWan")
    return new_code


def gen_many_new_code(many: int):
    codes = []
    for i in range(many):
        codes.append(gen_new_code())
    return codes