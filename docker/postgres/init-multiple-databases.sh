#!/bin/bash

set -e
set -u

function create_database() {
    local database=$1

    echo "Creating database '$database'"

    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $POSTGRES_USER;
EOSQL

    echo "Database '$database' created successfully"
}

# Airflow metadata database
create_database "$METADATA_DATABASE_NAME"

# ELT / YouTube database
create_database "$ELT_DATABASE_NAME"

echo "All databases created successfully"