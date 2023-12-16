from typing import Annotated
from fastapi import File, UploadFile
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import FileResponse
import logging
from service import board, s3
from starlette.middleware.cors import CORSMiddleware  #引入 CORS中间件模块

logger = logging.getLogger(__name__)


app = FastAPI(upload_max_size=5 * 1024 * 1024)

#设置允许访问的域名
origins = ["*"]  #也可以设置为"*"，即为所有。

#设置跨域传参
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  #设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  #允许跨域的headers，可以用来鉴别来源等作用。


class NewUserReg(BaseModel):
    address: str
    name: str = None
    avatar: str = None
    region: str = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user/", summary="这是用户输入code和address之后的查询，如果查到了会返回json形式的用户的各种个人信息以及自己的content，如果没查到或者查询有问题会返回404，如果传参格式错误会返回400")
def user_login(code: str, address: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    res = board.get_user_msg(code = code, address = address)
    if res == None:
        raise HTTPException(status_code=404, detail="db records > 1 or not found")
    return res


@app.get("/content/", summary="这是用户想进入comment之后的查询，如果查到了会返回所有映射的content的json，如果查询有问题会返回404，如果传参格式错误会返回400")
def get_content(code: str, address: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    res = board.get_user_content(code = code, address = address)
    if res == None:
        raise HTTPException(status_code=404, detail="user code error")
    return res


# @app.post("/update/content/", summary="用户更新content，如果传参格式错误会返回400")
# def update_content(code: str, address: str, content: str):
#     address = board.verify_address_and_convert(address)
#     if not address:
#         raise HTTPException(status_code=400, detail="address format error")
#     if not board.verify_code(code):
#         raise HTTPException(status_code=400, detail="code format error")
#     board.update_content(code = code, address = address, content = content)


class Item(BaseModel):
    code: str
    address: str
    content: str

@app.post("/update/content/", summary="用户更新content，如果传参格式错误会返回400")
def update_content(item: Item):
    address = board.verify_address_and_convert(item.address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(item.code):
        raise HTTPException(status_code=400, detail="code format error")
    board.update_content(code = item.code, address = item.address, content = item.content)


@app.post("/update/region/", summary="用户更新region，如果传参格式错误会返回400")
def update_region(code: str, address: str, region: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    board.update_region(code = code, address = address, region = region)


@app.post("/update/name/", summary="用户更新name，如果传参格式错误会返回400")
def update_name(code: str, address: str, name: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    board.update_name(code = code, address = address, name = name)


@app.post("/update/avatar", summary="用户更新avatar，如果传参格式错误会返回400")
def update_avatar(code: str, address: str, avatar: str):
    address = board.verify_address_and_convert(address)
    if not address:
        raise HTTPException(status_code=400, detail="address format error")
    if not board.verify_code(code):
        raise HTTPException(status_code=400, detail="code format error")
    board.update_avatar(code = code, address = address, avatar = avatar)


class S3File(BaseModel):
    file: bytes

# @app.post("/s3/upload", summary="如果传参格式错误会返回400")
# def upload_file(file_name: str, s3file: S3File):
#     status = s3.upload_file(file_name, s3file.file)
#     if not status:
#         raise HTTPException(status_code=400, detail="upload error")
#     else:
#         return HTTPException(status_code=200, detail=f"{status}")


# @app.post("/s3/download", summary="如果传参格式错误会返回400")
# def dowload_file(file_name: str):
#     res = s3.get_file_url(file_name)
#     if not res:
#         raise HTTPException(status_code=400, detail="dowload error")
#     else:
#         return HTTPException(status_code=200, detail=f"{res}")


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    status = s3.upload_file(file.filename, await file.read())
    if not status:
        raise HTTPException(status_code=400, detail="upload error")
    else:
        return HTTPException(status_code=200, detail=f"https://nft-erm-bucket.s3.ap-southeast-1.amazonaws.com/{file.filename}")


# @app.get("/.well-known/pki-validation/40C3079F6B4B01091FCCB906260C0C25.txt")
# async def show():
#     filename = "40C3079F6B4B01091FCCB906260C0C25.txt"
#     return FileResponse(
#             filename,
#             filename=filename, # 这里的文件名是你要给用户展示的下载的文件名
#         )


########################## ADMIN ##############################

# @app.get("/new_code/")
# def get_new_code_and_reg():
#     return board.gen_new_code()


# @app.get("/many_code/")
# def get_new_many_codes_and_reg(many: int):
#     return board.gen_many_new_code(many)


# @app.get("/connect_all/")
# def connect_all():
#     board.connect_all()


# @app.get("/judge/")
# def judge():
#     board.judge()