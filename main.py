from fastapi import FastAPI
from pydantic import BaseModel
import logging
from service import code

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


@app.get("/new_code/")
def get_new_code_and_reg():
    return code.gen_new_code()


@app.get("/many_code/")
def get_new_many_codes_and_reg(many: int):
    return code.gen_many_new_code()




# @app.post("/new_user/")
# def new_user(address: str):
#     return {"code": code}