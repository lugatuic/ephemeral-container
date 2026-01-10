import os
from dotenv import load_dotenv

load_dotenv()

class loadenvVar():
    def __init__(self):
        self.PROXMOX_HOST = os.getenv("PROXMOX_HOST")
        self.PROXMOX_USER = os.getenv("PROXMOX_USER")
        self.PROXMOX_TOKEN_NAME = os.getenv("PROXMOX_TOKEN_NAME")
        self.PROXMOX_TOKEN_VALUE = os.getenv("PROXMOX_TOKEN_VALUE")
        self.NODE = os.getenv("NODE")
        self.TEMPLATE_ID = os.getenv("TEMPLATE_ID")
        self.MYSQL_HOSTNAME= os.getenv("MYSQL_HOSTNAME")
        self.MYSQL_DATABASE= os.getenv("MYSQL_DATABASE")
        self.MYSQL_USERNAME= os.getenv("MYSQL_USERNAME")
        self.MYSQL_PASSWORD= os.getenv("MYSQL_PASSWORD")
        self.lxc_user = os.getenv("lxc_user")
        self.container_passwd = os.getenv("container_passwd")


envVar = loadenvVar()