from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, CHAR, Text, DateTime, Boolean, Index, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime as dt

# 创建对象的基类
Base = declarative_base()

# 初始化数据库连接
engine = create_engine('postgresql://postgres:tmphavefun@erm.c3rrikbrfsu7.ap-southeast-1.rds.amazonaws.com:5432/erm',
                       echo=True,  # 程序运行时反馈执行过程中的关键对象，包括ORM构建的sql语句
                       max_overflow=0,  # 超过连接池大小外最多创建的连接
                       pool_size=5,  # 连接池大小
                       pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
                       pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                       )

# 绑定引擎
Session = sessionmaker(bind=engine)
# 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# 内部会采用threading.local进行隔离
session = scoped_session(Session)


'''
创建数据表的映射类
'''
class Msg(Base):
    __tablename__ = 'msg'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(CHAR(6), nullable=False)
    content = Column(Text)
    create_time = Column(DateTime, default=dt.now(), nullable=False),
    address = Column(CHAR(42)),
    region = Column(String(50))
    name = Column(String(16))
    avatar = Column(Text)
    expire = Column(Boolean, default=False)
    

class Mapping(Base):
    __tablename__ = 'mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(CHAR(6), nullable=False)
    code_connected = Column(Text, nullable=False)
    
    __table_args__ = (
        Index('mapping_code_idx', 'code'),
    )


# 创建表到数据库表中
Base.metadata.create_all(engine)