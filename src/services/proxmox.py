from proxmoxer import ProxmoxAPI
from configs import config
import time
import asyncio

counter = 300
lock = asyncio.Lock()  # lock wont matter since only one coroutine
# will work unless an await is used in the part which requires lock
# and we dont require it since get_cid just get the result and no wait

proxmox=ProxmoxAPI(
config.PROXMOX_HOST,
user=config.PROXMOX_USER,
token_name=config.PROXMOX_TOKEN_NAME,
token_value=config.PROXMOX_TOKEN_VALUE,
verify_ssl=False
    )


def get_cid():
    global counter
        # try and catch block so in case by any chance if there is any application reload
        # causing counter to reload it doesnt cause any double counter error as if counter id already
        # exists in proxmox
    while(True):
        try:
            status = proxmox.nodes(config.NODE).lxc(counter).status.current.get()
            # print("status is" , status , "status ends")
            counter = counter+1
        except Exception as e:
            cid = counter
            print("cid is " , cid)
            counter+=1
            return cid
        
async def check_provision(cid , task_id):
    print("in check provision")
    while True:
        try:
            print("in true check provision")
            status = proxmox.nodes(config.NODE).tasks(task_id).status.get()
            print(status)
            if status['status'] == "running":
                await asyncio.sleep(1)
                continue
            return status
        except:
            print("in except check prov")
            await asyncio.sleep(1)


async def check_start(cid , task_id):
    print("in check start")
    while True:
        try:
            print("in true check start")
            status = proxmox.nodes(config.NODE).tasks(task_id).status.get()
            print(status)
            if status['status'] == "running":
                await asyncio.sleep(1)
                continue
            return status
        except:
            print("in except check prov")
            await asyncio.sleep(1)


async def check_ip(cid):
    while True:
        status = proxmox.nodes(config.NODE).lxc(cid).interfaces.get()
        print(status)
        for manydict in status:
            if manydict.get("inet") and manydict.get("name") != "lo":
                return status
        await asyncio.sleep(1)

    
async def provision_lxc(cid, netid, TEMPLATE_ID):
    try:
        async with lock:
            print("we are in provision")
            prov = proxmox.nodes(config.NODE).lxc(TEMPLATE_ID).clone.post(
                newid=cid,
                hostname=f"{netid}-{cid}",
                full=1,
            )
            print(prov)
            print("executing this")
            await check_provision(cid , prov)
            return prov
    except Exception as e:
        print("success", False, "message" , str(e))
        return {"success": False, "message": str(e)}
    
async def start_lxc(cid):
    try:
        async with lock:
            print("in start_lxc now")
            task_id = proxmox.nodes(config.NODE).lxc(cid).status.start.post()
            await check_start(cid , task_id)
            return f"Task id for starting container is {task_id}"
    except Exception as e:
        return {"success": False, "message": str(e)}

    
async def get_ip(cid):
    try:
        print("we are in get_ip")
        await check_ip(cid)
        status = proxmox.nodes(config.NODE).lxc(cid).interfaces.get()
        print(status)
        for manydict in status:
            if manydict.get("inet") and manydict.get("name") != "lo":
                ip_info = manydict["inet"]
                break
        ip = ip_info.split('/')[0]
        print("ip is \n" , ip)
        return ip
    except Exception as e:
        return {"success": False, "message": str(e)}
        


if __name__ == "__main__":
    print("Hello, World!")
# cid = get_cid()
# print(cid)
# print(provision_lxc(cid , "testing"))
# time.sleep(20)
# print(start_lxc(cid))
# time.sleep(20)
# print(get_ip(cid))





