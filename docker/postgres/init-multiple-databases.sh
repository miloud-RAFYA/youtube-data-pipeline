#!/bin/bash

set -e

echo "Creating database: $METADATA_DATABASE_NAME"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE "$METADATA_DATABASE_NAME";
EOSQL

echo "Creating database: $ELT_DATABASE_NAME"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE "$ELT_DATABASE_NAME";
EOSQL