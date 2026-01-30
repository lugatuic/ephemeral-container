# ephemeral-container
ephemeral containers for events

## Requirements
- uv
- Other Requirements will be satisfied by running uv command above

## How to build this project
- install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- go into src folder and run `uv run uvicorn main:app --reload`
- This will launch fastapi backend


## TODOS

- [ ] Add await on some coroutines to make code concurrent
- [ ] Solve issue of TOCTOU race condition
- [ ] Add Test Cases
- [ ] Delete lxc after TTL
- [ ] Connecting it to AD or something so people only enter valid and their own netid
- [ ] Add option to choose Template


<!-- ### delete plan
- Delete the container using proxmox api
- Maybe run a cron job which will delete a container after a specified time
-  -->