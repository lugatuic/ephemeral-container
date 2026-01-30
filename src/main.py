from services import proxmox as prox
from services import guacamole as guac
from fastapi import FastAPI , Request
import time
import base64
from configs import config
import asyncio

app = FastAPI()


def create_url():
    pass


@app.post("/launch")
async def launch(request: Request):
    try:
        data =await request.json()
        netid = data.get("netid","").strip()
        template_id = data.get("template_id")
        print("template id is " , template_id)
        cid = prox.get_cid()   # issue over here with concurrent request
        await prox.provision_lxc(cid,netid,template_id)
        # await asyncio.sleep(10) # issue over here with concurrent request
        await prox.start_lxc(cid)
        # await asyncio.sleep(20)
        ip = await prox.get_ip(cid)
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

    
