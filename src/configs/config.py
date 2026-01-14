import os
from dotenv import load_dotenv

load_dotenv()
PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PROXMOX_USER = os.getenv("PROXMOX_USER")
PROXMOX_TOKEN_NAME = os.getenv("PROXMOX_TOKEN_NAME")
PROXMOX_TOKEN_VALUE = os.getenv("PROXMOX_TOKEN_VALUE")
NODE = os.getenv("NODE")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
MYSQL_HOSTNAME= os.getenv("MYSQL_HOSTNAME")
MYSQL_DATABASE= os.getenv("MYSQL_DATABASE")
MYSQL_USERNAME= os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD= os.getenv("MYSQL_PASSWORD")
lxc_user = os.getenv("lxc_user")
container_passwd = os.getenv("container_passwd")