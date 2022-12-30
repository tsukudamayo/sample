```bash
cp sample-env-settings.sh env-settings.sh
chmod +x env-settings.sh
 ./env-settings.sh 
```

```bash
docker-compose up -d
```

```bash
curl ${ES_PORT}:9200/_nodes/stats 
```

```bash
http://${ES_PORT}:5601/
http://${ES_PORT}:5601/app/dev_tools#/console
```
