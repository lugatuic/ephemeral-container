import services.proxmox
from fastapi import FastAPI , Request


app = FastAPI()

@app.post("/launch")
async def launch(request: Request):
    data =await request.json()
    netid = data.get("netid","").strip()
    
