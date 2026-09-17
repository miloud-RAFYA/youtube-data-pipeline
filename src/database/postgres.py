import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_CONN_HOST"),
        port=os.getenv("POSTGRES_CONN_PORT"),
        user=os.getenv("ELT_DATABASE_USERNAME"),
        password=os.getenv("ELT_DATABASE_PASSWORD"),
        dbname=os.getenv("ELT_DATABASE_NAME"),
    )