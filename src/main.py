from services.proxmox import prox
from fastapi import FastAPI , Request
import time

app = FastAPI()

@app.post("/launch")
async def launch(request: Request):
    data =await request.json()
    netid = data.get("netid","").strip()
    cid = prox.get_cid()
    prox.provision_lxc(cid,netid)
    prox.start_lxc(cid)
    time.sleep(20)
    prox.get_ip(cid)

    
