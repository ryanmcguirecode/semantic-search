from connections import postgreSQL_connect
from psycopg2.extras import execute_values

def setup_table(connection, cursor, table_name, schema):
    create_table_command = f"""CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY,"""
    for column_name, typ in schema.items():
        create_table_command += f" {column_name} {typ},"
    create_table_command = create_table_command[:-1] + ")"
    cursor.execute(create_table_command)
    connection.commit()

def insert_rows(cursor, table_name, columns, rows):
    execute_values(cursor, f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s", rows)
