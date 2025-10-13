# from dotenv import load_dotenv
# import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import text
# import pandas as pd

import helperFuns.helperFuns as hf
# load_dotenv()

Base = declarative_base()
# dsn_tns = cx_Oracle.makedsn(hf.readEnv('HOST'), hf.readEnv('PORT'), sid=hf.readEnv('SID'))
# engine = create_engine('oracle://'+username+':'+password+'@'+host+':'+str(port)+'/'+sid)

# DIALECT = 'oracle'
# SQL_DRIVER = 'cx_oracle'
# USERNAME = 'KWARECOM' #enter your username
# PASSWORD = 'k2titus2' #enter your password
# HOST = '127.0.0.1' #enter the oracle db host url
# PORT = 1521 # enter the oracle port number
# SERVICE = 'XE' # enter the oracle db service name
CONN_STRING = f'oracle+cx_oracle://{hf.readEnv('USERNAME')}:{hf.readEnv('PASSWORD')}@{hf.readEnv('HOST')}:{hf.readEnv('PORT')}/?service_name={hf.readEnv('SID')}'
# ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE

engine = create_engine(CONN_STRING)

# conn = engine.connect()
# get_records = conn.execute(text("SELECT * FROM admindistrict"))

#test query
# test_df = pd.read_sql_query('SELECT * FROM admindistrict', engine)
def connectionBase():
    return Base

def dbMigration():
    Base.metadata.create_all(engine)

def dbSession():
    Session = sessionmaker(bind=engine)
    return Session()

def dbConn():
    return engine.connect()

# for row in get_records:
#     print(row)
    

# from sqlmodel import create_engine, SQLModel, Session
# # from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

# DATABASE_URL = os.environ.get("DATABASE_URL")

# engine = create_engine(DATABASE_URL, echo=True)
# connection_string = f'oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}'
# engine = create_engine(connection_string)

# def init_db():
#     SQLModel.metadata.create_all(engine)

# connection = engine.raw_connection()
# cursor = connection.cursor()
# try:
#     cursor.callproc("your_stored_procedure_name", (param1, param2))
# finally:
#     cursor.close()
#     connection.close()

# def get_session():
#     with Session(engine) as session:
#         yield session