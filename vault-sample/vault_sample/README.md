- configure env

```
source env-settings.sh
```

```bash
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
export POSTGRES_URL=127.0.0.1:5432
```

- install vault and postgresql

- create sample user
```
sudo -u postgres bash create-sample-readonly-role.sh
```

```bash
psql -U postgres -c "CREATE ROLE ro NOINHERIT;"
psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO ro;"
```

- create role
```
poetry install
poetry run python postgres_sample.py
```

- verify role
```
vault read database/creds/readonly
sudo -u postgres bash verify-sample-role.sh 
```


