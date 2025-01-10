#!/bin/bash

set -x

# Check if the database name is provided as --database
if [ "$#" -lt 2 ] || [ "$1" != "--database" ]; then
    echo "Usage: $0 --database <database_name> [<migration_args>]"
    exit 1
fi

DB_NAME=$2         # Database name from the second argument
MIGRATION_ARGS=${@:3}  # Use all arguments from the third one onwards as migration arguments

# Run create_db.sh to create the database if it does not exist
./scripts/create_db.sh --database "$DB_NAME"

# Check if create_db.sh succeeded
if [ $? -ne 0 ]; then
    echo "Failed to create database: $DB_NAME"
    exit 1
fi

# Run migrate.sh with the given migration arguments
./scripts/migrate.sh --database "$DB_NAME" $MIGRATION_ARGS

# Check if migrate.sh succeeded
if [ $? -ne 0 ]; then
    echo "Migration failed."
    exit 1
fi

echo "Database setup and migration completed successfully."