from services import proxmox as prox
from services import guacamole as guac
from fastapi import FastAPI , Request
import time
import base64
import configs as config

app = FastAPI()


def create_url():
    pass


@app.post("/launch")
async def launch(request: Request):
    try:
        data =await request.json()
        netid = data.get("netid","").strip()
        cid = prox.get_cid()
        prox.provision_lxc(cid,netid)
        time.sleep(20)
        print(prox.start_lxc(cid))
        time.sleep(20)
        ip = prox.get_ip(cid)
        print(ip)
        print("check here")
        conn_id = guac.fill_sql(netid,cid,ip)

        conn_id_list = [str(conn_id) , "c" , "mysql"]
        conn_id_concat = '\0'.join(conn_id_list)
        based_conn_id_encoded = base64.b64encode(conn_id_concat.encode('utf-8'))
        based_conn_id = based_conn_id_encoded.decode('utf-8')
        print("based conn_id is" , based_conn_id)

        return {
            "success": True,
            "container_id": cid,
            "ip": ip,
            "user": netid,
            "password": config.container_passwd,
            "url": f"http://{config.MYSQL_HOSTNAME}:8080/guacamole/#/client/{based_conn_id}",
        }
    

    except Exception as e:
        return {"success": False, "message": str(e)}

    
