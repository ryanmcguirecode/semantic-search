from configparser import ConfigParser
from connections import set_openai_key, postgreSQL_connect, postgreSQL_disconnect
from embeddings import get_embedding, num_tokens, price_dollars
from pg import register_vector, execute_command, insert_rows
import numpy as np

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
print("Embedding: ", embedding[0:10])

columns = ["embedding"]
create_table_command = """
CREATE TABLE IF NOT EXISTS test_embeddings (
    id SERIAL PRIMARY KEY,
    embedding vector(1536)
)
"""
execute_command(cursor, create_table_command)
connection.commit()

insert_rows(cursor, "test_embeddings", columns, [(embedding,) for _ in range(10)])
connection.commit()

# Print row count
cursor.execute("SELECT COUNT(*) FROM test_embeddings")
print("Row count: ", cursor.fetchone()[0])

postgreSQL_disconnect(connection, cursor)

# CHUNK_SIZE = 512