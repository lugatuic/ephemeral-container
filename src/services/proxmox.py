from proxmoxer import ProxmoxAPI
from configs.config import envVar as config

proxmox=ProxmoxAPI(
    config.PROXMOX_HOST,
    user=config.PROXMOX_USER,
    token_name=config.PROXMOX_TOKEN_NAME,
    token_value=config.PROXMOX_TOKEN_VALUE,
    verify_ssl=False
)

cid = proxmox.cluster.nextid.get()
