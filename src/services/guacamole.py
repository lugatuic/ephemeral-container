from configs import config
import subprocess, time, pymysql
from sqlalchemy import create_engine , text , insert , MetaData , Table , select
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

guac_entity_table = metadata_obj.tables["guacamole_entity"]

guac_user_table = metadata_obj.tables["guacamole_user"]

guac_conn_permission_table = metadata_obj.tables["guacamole_connection_permission"]


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
    
def fill_connection_details(conn , conn_id , ip):
    print("in fill function")
    details = [(conn_id , 'hostname' , ip),
               (conn_id , 'port', 22),
               (conn_id , 'username' , config.lxc_user),
               (conn_id , 'password'  , config.container_passwd)
               ]
    with conn.begin():
        stmt = insert(connection_info_table).values([{'connection_id' : conn_id , 'parameter_name': param_name , 'parameter_value': param_value}
                                                     for conn_id , param_name , param_value in details])
        print("checking stmt print: " , stmt)
        result = conn.execute(stmt)
        print(result)


def create_entity(conn , netid):
    print("in create entity")
    with conn.begin():
        select_stmt = select(guac_entity_table.c.entity_id).where(guac_entity_table.c.name == netid)
        print(select_stmt)
        result = conn.execute(select_stmt)
        row = result.fetchone()
        if row is None:
            stmt = insert(guac_entity_table).values(name = netid , type = 'USER')
            print("checking stmt print: " , stmt)
            result = conn.execute(stmt)
            entity_id = result.lastrowid
            return entity_id
        entity_id = row.entity_id
        return entity_id



def create_user(conn , entity_id):
    print("in create user")
    with conn.begin():
        select_stmt = select(guac_user_table).where(guac_user_table.c.entity_id == entity_id)
        print(select_stmt)
        result = conn.execute(select_stmt)
        row = result.fetchone()
        if row is None:
            salt , hashed_password = get_hashed()
            stmt = insert(guac_user_table).values(entity_id = entity_id , password_salt = salt , password_hash = hashed_password , password_date = datetime.datetime.now())
            print("checking stmt print: " , stmt)
            result = conn.execute(stmt)
            user_id = result.lastrowid
            return user_id
        user_id = row.user_id
        return user_id


def map_guac_permissions(conn , entity_id , conn_id):
    print("in map guac permission")
    with conn.begin():
        stmt = insert(guac_conn_permission_table).values(entity_id = entity_id , connection_id = conn_id , permission = 'READ')
        print("checking stmt print: " , stmt)
        result = conn.execute(stmt)


def fill_sql(netid,cid,ip):
    with engine.connect() as conn:

        #create connection in guacamole_connection
        conn_id = create_connection(conn , netid , cid)
        print("conn id is" , conn_id)

        #fill connection details in guacamole_connection_parameter
        fill_connection_details(conn , conn_id , ip)

        #create guacamole entity
        entity_id = create_entity(conn , netid)

        print("entity id is" , entity_id)

        #create guacamole user and setting password
        user_id = create_user(conn , entity_id)

        print("user id is " , user_id)

        #map user to permissions
        map_guac_permissions(conn , entity_id , conn_id)

        return conn_id
        
    


def del_sql():
    pass


# conn = pymysql.connect(
# host=config.MYSQL_HOSTNAME,
# user=config.MYSQL_USERNAME,
# password = config.MYSQL_PASSWORD,
# db=config.MYSQL_DATABASE,
# port = 3306
# )
