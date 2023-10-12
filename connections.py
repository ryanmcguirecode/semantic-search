from psycopg2 import connect
import openai

def set_openai_key(config):
    openai.api_key = config.get("OpenAI", "key")

def postgreSQL_connect(config):
    host = config.get("PostgreSQL", "host")
    database = config.get("PostgreSQL", "database")
    user = config.get("PostgreSQL", "user")
    password = config.get("PostgreSQL", "password")

    connection = connect(
        host=host, 
        database=database, 
        user=user, 
        password=password
    )

    return connection

def postgreSQL_disconnect(connection, cursor):
    cursor.close()
    connection.close()
    