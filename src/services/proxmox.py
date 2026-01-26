from proxmoxer import ProxmoxAPI
from configs import config
import time
import threading

counter = 300
lock = threading.Lock()

proxmox=ProxmoxAPI(
config.PROXMOX_HOST,
user=config.PROXMOX_USER,
token_name=config.PROXMOX_TOKEN_NAME,
token_value=config.PROXMOX_TOKEN_VALUE,
verify_ssl=False
    )


def get_cid():
    with lock:
        global counter
        # try and catch block so in case by any chance if there is any application reload
        # causing counter to reload it doesnt cause any double counter error as if counter id already
        # exists in proxmox
        while(True):
            try:
                status = proxmox.nodes(config.NODE).lxc(counter).status.current.get()
                counter = counter+1
            except:
                cid = counter
                print("cid is " , cid)
                counter+=1
                return cid
        
    
def provision_lxc(cid, netid, TEMPLATE_ID):
    try:
        print("we are in provision")
        proxmox.nodes(config.NODE).lxc(TEMPLATE_ID).clone.post(
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
        


if __name__ == "__main__":
    print("Hello, World!")
# cid = get_cid()
# print(cid)
# print(provision_lxc(cid , "testing"))
# time.sleep(20)
# print(start_lxc(cid))
# time.sleep(20)
# print(get_ip(cid))





