from proxmoxer import ProxmoxAPI
from configs import config
import time

proxmox=ProxmoxAPI(
config.PROXMOX_HOST,
user=config.PROXMOX_USER,
token_name=config.PROXMOX_TOKEN_NAME,
token_value=config.PROXMOX_TOKEN_VALUE,
verify_ssl=False
    )

def get_cid():
    cid= proxmox.cluster.nextid.get()
    return cid
        
    
def provision_lxc(cid, netid):
    try:
        print("we are in provision")
        proxmox.nodes(config.NODE).lxc(config.TEMPLATE_ID).clone.post(
            newid=cid,
            hostname=f"{netid}-{cid}",
            full=1,
        )
        return True
    except Exception as e:
        return {"success": False, "message": str(e)}
    
def start_lxc(cid):
    try:
        print("in start_lxc now")
        task_id = proxmox.nodes(config.NODE).lxc(cid).status.start.post()
        return f"Task id for starting container is {task_id}"
    except Exception as e:
        return {"success": False, "message": str(e)}

    
def get_ip(cid):
    try:
        print("we are in get_ip")
        status = proxmox.nodes(config.NODE).lxc(cid).interfaces.get()
        ip_info = status[1]["inet"]
        ip = ip_info.split('/')[0]
        print("ip is \n" , ip)
        return ip
    except Exception as e:
        return {"success": False, "message": str(e)}
        


# testing the functions here
# cid = get_cid()
# print(cid)
# print(provision_lxc(cid , "testing"))
# time.sleep(20)
# print(start_lxc(cid))
# time.sleep(20)
# print(get_ip(cid))





