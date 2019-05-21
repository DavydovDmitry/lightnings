Linked repositories:
- [https://github.com/DavydovDmitry/lightnings_server](https://github.com/DavydovDmitry/lightnings_server)
- [https://github.com/DavydovDmitry/lightnings_client](https://github.com/DavydovDmitry/lightnings_client)

Execution:
cd lightnings_logic
export $(cat local.env)
docker-compose up
# if you have dump of database
# ./scripts/restore.sh
./scripts/start.sh
