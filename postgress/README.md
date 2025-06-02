Command to spin up the postgress container:
```bash
docker compose -f docker-compose.yml up
```

DB url:
```bash
postgresql://postgres:example@localhost:5432/postgres
``` 

Credentials for the postgress db:
```bash
    host: localhost
    database-port: 5432
    adminer-port: 8080
    server: db
    database: postgres
    username: postgres
    password: example
```

Command to run after updateing db schema:
```bash
    npx prisma migrate dev --name MIGRATION_NAME
```

Command to run to udpdate prisma client after updating schema:
```bash
     npx prisma generate
```

Command for testing db seed:
```bash
    npx prisma db seed
```