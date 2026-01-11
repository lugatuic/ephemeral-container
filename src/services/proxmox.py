from proxmoxer import ProxmoxAPI
from configs.config import envVar as config
import time

class proxClass():
    proxmox=ProxmoxAPI(
    config.PROXMOX_HOST,
    user=config.PROXMOX_USER,
    token_name=config.PROXMOX_TOKEN_NAME,
    token_value=config.PROXMOX_TOKEN_VALUE,
    verify_ssl=False
    )

    def get_cid(self):
        self.cid= self.proxmox.cluster.nextid.get()
        return self.cid
        
    
    def provision_lxc(self, cid, netid):
        try:
            print("we are in provision")
            self.proxmox.nodes(config.NODE).lxc(config.TEMPLATE_ID).clone.post(
                newid=cid,
                hostname=f"{netid}-{cid}",
                full=1,
            )
            return True
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def start_lxc(self,cid):
        try:
            print("in start_lxc now")
            task_id = self.proxmox.nodes(config.NODE).lxc(cid).status.start.post()
            return f"Task id for starting container is {task_id}"
        except Exception as e:
            return {"success": False, "message": str(e)}

    
    def get_ip(self , cid):
        try:
            print("we are in get_ip")
            status = self.proxmox.nodes(config.NODE).lxc(cid).interfaces.get()
            ip_info = status[1]["inet"]
            ip = ip_info.split('/')[0]
            print("ip is \n" , ip)
            return ip
        except Exception as e:
            return {"success": False, "message": str(e)}
        




prox = proxClass()

# testing the functions here
cid = prox.get_cid()
print(cid)
print(prox.provision_lxc(cid , "testing"))
time.sleep(20)
print(prox.start_lxc(cid))
time.sleep(20)
print(prox.get_ip(cid))





