from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector


def setup_vector(connection):
    register_vector(connection)
    
def insert_rows(cursor, table_name, columns, rows):
    execute_values(cursor, f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s", rows)