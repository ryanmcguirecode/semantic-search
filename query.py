from configparser import ConfigParser
from connections import set_openai_key, postgreSQL_connect, postgreSQL_disconnect
from embeddings import get_embedding
from pg import setup_vector
import numpy as np

def get_closest_embeddings(embedding, num_results=10):
    cursor.execute(f"SELECT content FROM evolution_embeddings ORDER BY embedding <-> %s LIMIT {num_results}", (np.array(embedding),))
    return cursor.fetchall()
    

question = "Who contributed more, Darwin or Wallace?"

table_name = "evolution_embeddings"

config = ConfigParser()
config.read("credentials.ini")

set_openai_key(config)
connection = postgreSQL_connect(config)
setup_vector(connection)
cursor = connection.cursor()

embedding = get_embedding(question)
for row in get_closest_embeddings(embedding):
    print(row[0])
    
postgreSQL_disconnect(connection, cursor)