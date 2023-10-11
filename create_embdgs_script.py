from configparser import ConfigParser
from connections import set_openai_key, postgreSQL_connect, postgreSQL_disconnect
from embeddings import get_embedding, num_tokens, price_dollars
from pg import register_vector, execute_command, insert_rows

config = ConfigParser()
config.read("credentials.ini")

set_openai_key(config)
connection, cursor = postgreSQL_connect(config)

register_vector(cursor)
connection.commit()

test_string = "The principled fool is gregarious"

print("Token count: ", num_tokens(test_string))
print("Price: ${0}".format(price_dollars(test_string)))

embedding = get_embedding(test_string)
print("Embedding: ", embedding)

columns = ["embedding"]
create_table_command = """
CREATE TABLE IF NOT EXISTS test_embeddings (
    id SERIAL PRIMARY KEY,
    embedding vector(1536)
)
"""
execute_command(cursor, create_table_command)
connection.commit()

rows = [(embedding) for _ in range(1000)]
insert_rows(cursor, "test_embeddings", columns, rows)
connection.commit()

postgreSQL_disconnect(connection, cursor)

CHUNK_SIZE = 512