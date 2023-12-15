from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from service import board
from web3 import Web3

logger = logging.getLogger(__name__)


app = FastAPI()


class NewUserReg(BaseModel):
    address: str
    name: str = None
    avatar: str = None
    region: str = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user/")
def user_login(code: str, address: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    res = board.get_user_msg(code = code, address = address)
    if res == None:
        raise HTTPException(status_code=400, detail="db records > 1 or not found")
    return res


@app.get("/content/")
def get_content(code: str, address: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    res = board.get_user_content(code = code, address = address)
    if res == None:
        raise HTTPException(status_code=400, detail="user code error")
    return res


@app.post("/update/")
def update_content(code: str, address: str, content: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    board.update_content(code = code, address = address, content = content)


@app.post("/update/")
def update_region(code: str, address: str, region: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    board.update_region(code = code, address = address, region = region)


@app.post("/update/")
def update_name(code: str, address: str, name: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    board.update_name(code = code, address = address, name = name)


@app.post("/update/")
def update_avatar(code: str, address: str, avatar: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    board.update_avatar(code = code, address = address, avatar = avatar)


########################## ADMIN ##############################

# @app.get("/new_code/")
# def get_new_code_and_reg():
#     return code.gen_new_code()


# @app.get("/many_code/")
# def get_new_many_codes_and_reg(many: int):
#     return code.gen_many_new_code(many)


# @app.get("/connect_all/")
# def connect_all():
#     code.connect_all()


# @app.get("/judge/")
# def judge():
#     code.judge()