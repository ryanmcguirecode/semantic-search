from psycopg2.extras import execute_values

def register_vector(cursor):
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
    
def execute_command(cursor, command):
    cursor.execute(command)
    
def insert_rows(cursor, table_name, columns, rows):
    execute_values(cursor, f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s", rows)