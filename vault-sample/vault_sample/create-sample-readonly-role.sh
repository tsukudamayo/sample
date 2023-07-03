psql -U postgres -c "CREATE ROLE ro NOINHERIT;"
psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO ro;"
