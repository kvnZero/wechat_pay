#coding=utf8
from sqlalchemy import Column, String, create_engine, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime
Base = declarative_base()
baseurl = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    fromuser = Column(String(50))
    money = Column(String(30))
    createtime = Column(DateTime)
    note = Column(String(255))

    def __repr__(self):
        return "<Order(fromuser='%s', money='%s', createtime='%s', note='%s')>" % (self.fromuser, self.money, self.createtime, self.note)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user =  Column(String(255))
    wechat_user = Column(String(255))
    money =  Column(String(255))
    lastmoney = Column(String(255))
    orders= Column(String(255))
    createtime = Column(DateTime)
    lastdotime = Column(DateTime)

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    douser = Column(String(255))
    dowhat = Column(String(255))
    time = Column(DateTime)

class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(255))
    discount = Column(String(255))
    quantity = Column(Integer)


engine = create_engine(baseurl)
#create sqlite
#Base.metadata.create_all(engine)

#create session
DBSession = sessionmaker(bind=engine)
session = DBSession()
#new_order = Order(fromuser="test",money="10.00", createtime=datetime.utcnow(),note="test")
#session.add(new_order)
#session.commit()
#session.close()
#order = session.query(Order).filter_by(fromuser="123").first()
