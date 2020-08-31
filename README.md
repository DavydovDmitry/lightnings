Execution:
```shell script
export $(cat local.env)
docker-compose up
./scripts/start.sh
```

To restore dump of database
```shell script
./scripts/restore.sh
```

```shell script
docker-compose run --service-ports database
```