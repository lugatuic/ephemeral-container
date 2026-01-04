from fastapi import FastAPI , Request
from proxmoxer import ProxmoxAPI
import subprocess, time, pymysql
import subprocess
import os
import hashlib
import datetime
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PROXMOX_USER = os.getenv("PROXMOX_USER")
PROXMOX_TOKEN_NAME = os.getenv("PROXMOX_TOKEN_NAME")
PROXMOX_TOKEN_VALUE = os.getenv("PROXMOX_TOKEN_VALUE")
NODE = os.getenv("NODE")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
TTL = 3600

MYSQL_HOSTNAME= os.getenv("MYSQL_HOSTNAME")
MYSQL_DATABASE= os.getenv("MYSQL_DATABASE")
MYSQL_USERNAME= os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD= os.getenv("MYSQL_PASSWORD")

lxc_user = os.getenv("lxc_user")
container_passwd = os.getenv("container_passwd")

proxmox=ProxmoxAPI(
    PROXMOX_HOST,
    user=PROXMOX_USER,
    token_name=PROXMOX_TOKEN_NAME,
    token_value=PROXMOX_TOKEN_VALUE,
    verify_ssl=False
)


@app.post("/launch")
async def launch(request: Request):
    data = await request.json()
    netid = data.get("netid", "").strip()
    cid = proxmox.cluster.nextid.get()
    print(f"Next available LXC ID: {cid}")
    salt = os.urandom(32);
    salt_hex = salt.hex().upper()
    salted_passwd = container_passwd + salt_hex
    hashed_password = hashlib.sha256(salted_passwd.encode('utf-8')).digest()

    try:
        proxmox.nodes(NODE).lxc(TEMPLATE_ID).clone.post(
            newid=cid,
            hostname=f"{netid}-{cid}",
            full=1,
         )

        time.sleep(20)
        proxmox.nodes(NODE).lxc(cid).status.start.post()

        time.sleep(20)

        status = proxmox.nodes(NODE).lxc(cid).interfaces.get()

        print("status is \n" , status)

        ip_info = status[1]["inet"]

        print("ip_info is \n" , ip_info)

        ip = ip_info.split('/')[0]

        print("ip is \n" , ip)

        conn = pymysql.connect(
        host=MYSQL_HOSTNAME,
        user=MYSQL_USERNAME,
        password = MYSQL_PASSWORD,
        db=MYSQL_DATABASE,
        port = 3306
        )

        cur = conn.cursor()
        

        # this sql query will specify the connection name. Its not the hostname but just the connection name shown in guacamole which will map to ssh connection
        # further info : https://guacamole.apache.org/doc/gug/jdbc-auth-schema.html#connections-and-parameters
        cur.execute("INSERT INTO guacamole_connection (connection_name, protocol) VALUES (%s, 'ssh')", (f"{netid}-{cid}",))

        # this is connection id returned from entering the connection name
        conn_id = cur.lastrowid

        # now we will map the connection id to the ssh connection.
        # for further info of params : https://guacamole.apache.org/doc/gug/configuring-guacamole.html#ssh-authentication
        cur.executemany(
            "INSERT INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) VALUES (%s,%s,%s)",
            [(conn_id,'hostname',ip),(conn_id,'port','22'),(conn_id,'username',lxc_user),(conn_id,'password',container_passwd)]
        )

        cur.execute("SELECT entity_id FROM guacamole_entity WHERE name = %s" , (netid,))

        entitycheck = cur.fetchone()
        
        if(entitycheck is None):
            cur.execute("INSERT INTO guacamole_entity (name, type) VALUES (%s, 'USER')", (netid,))
            entity_id = cur.lastrowid
        else:
            entity_id = entitycheck[0]   

        cur.execute("SELECT user_id FROM guacamole_user WHERE entity_id = %s" , (entity_id,))

        usercheck = cur.fetchone()

        if(usercheck is None):
            cur.execute("INSERT INTO guacamole_user (entity_id , password_salt , password_hash , password_date) VALUES (%s , %s , %s , %s)", (entity_id , salt , hashed_password , datetime.datetime.now()))
            user_id = cur.lastrowid
        else:
            user_id = usercheck[0]

        print("till here its good")
        
        print("netid is %s connection id is %s and entity id is %s" , entity_id , conn_id , entity_id)

        cur.execute("INSERT INTO guacamole_connection_permission (entity_id, connection_id , permission) VALUES (%s, %s , 'READ')", (entity_id , conn_id ,))

        print("check here")

        conn.commit(); conn.close()

        print("what bout this one")

        return {
            "success": True,
            "container_id": cid,
            "ip": ip,
            "user": netid,
            "password": container_passwd,
            "url": f"http://{MYSQL_HOSTNAME}:8080/guacamole/#/client/{conn_id}",
            "expires_in": TTL
        }

    except Exception as e:
        return {"success": False, "message": str(e)}