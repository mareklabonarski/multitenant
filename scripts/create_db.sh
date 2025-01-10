#!/bin/bash

set -x

# Check if the database name is provided as --database
if [ "$#" -ne 2 ] || [ "$1" != "--database" ]; then
    echo "Usage: $0 --database <database_name>"
    exit 1
fi

DB_NAME=$2
POSTGRES_USER=$(docker compose exec db env | grep POSTGRES_USER | cut -d '=' -f2)
echo "Postgres User: $POSTGRES_USER"

# Check if the database exists
EXISTS=$(docker compose exec db psql -U "$POSTGRES_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")

if [ "$EXISTS" != "1" ]; then

    echo "Creating database '$DB_NAME'..."
    docker compose exec db psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE \"$DB_NAME\";"
else
    echo "Database '$DB_NAME' already exists."
fi
