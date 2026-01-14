from configs import config
import subprocess, time, pymysql
from sqlalchemy import create_engine , text , insert , MetaData , Table, Column , Integer , String
import datetime
import hashlib
import os

connection_uri = (
    f"mysql+pymysql://{config.MYSQL_USERNAME}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOSTNAME}:3306/{config.MYSQL_DATABASE}"
)

engine = create_engine(connection_uri,pool_size=20,echo=False,pool_pre_ping=True,max_overflow=20,pool_recycle=3600,pool_timeout=30)

metadata_obj = MetaData()

metadata_obj.reflect(bind=engine)

connection_create_table = metadata_obj.tables["guacamole_connection"]

connection_info_table = metadata_obj.tables["guacamole_connection_parameter"]


def get_hashed():
    salt = os.urandom(32)
    salt_hex = salt.hex().upper()
    salted_passwd = config.container_passwd + salt_hex
    hashed_password = hashlib.sha256(salted_passwd.encode('utf-8')).digest()
    return salt , hashed_password


def create_connection(conn , netid , cid):
    print("In create function")
    with conn.begin():
        # connidret = conn.execute(text("INSERT INTO guacamole_connection (connection_name ,protocol) VALUES (:connection_name , 'ssh')") , {"connection_name":f"{netid}-{cid}"})
        stmt = insert(connection_create_table).values(connection_name = f"{netid}-{cid}" , protocol='ssh')
        print("checking stmt print: " , stmt)
        result = conn.execute(stmt)
        conn_id = result.lastrowid
        return conn_id
    
def fill_connection_details(conn , netid , cid , ip):
    print("in fill function")
    # with conn.begin():
    #     stmt = insert()


def fill_sql(netid,cid,ip):
    with engine.connect() as conn:

        #create connection in guacamole_connection
        conn_id = create_connection(conn , netid , cid)
        print("conn id is" , conn_id)

        #fill connection details in guacamole_connection_parameter
        fill_connection_details(conn , netid , cid ,ip)
    


def del_sql():
    pass


# conn = pymysql.connect(
# host=config.MYSQL_HOSTNAME,
# user=config.MYSQL_USERNAME,
# password = config.MYSQL_PASSWORD,
# db=config.MYSQL_DATABASE,
# port = 3306
# )
