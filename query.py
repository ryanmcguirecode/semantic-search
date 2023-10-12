from configparser import ConfigParser
from connections import set_openai_key, postgreSQL_connect, postgreSQL_disconnect
from embeddings import get_embedding
import numpy as np
from llm import query_gpt4
import os

def get_closest_rows(embedding, num_results=3):
    cursor.execute(f"SELECT * FROM evolution_embeddings ORDER BY embedding <-> %s LIMIT {num_results}", (np.array(embedding),))
    return cursor.fetchall()

def get_paragraph(row):
    # print(len(row))
    # print(row)
    cursor.execute(
        f"""
        SELECT * FROM evolution_embeddings
            WHERE chapter = {row[1]} AND subheading = {row[2]} AND paragraph = {row[3]}
            ORDER BY chunk
        """
    )
    paragraph = " ".join([row[5] for row in cursor.fetchall()])
    return paragraph
    

question = "Did any scientists believe in ghosts?"

table_name = "evolution_embeddings"

config = ConfigParser()
config.read("credentials.ini")

set_openai_key(config)
connection, cursor = postgreSQL_connect(config)

embedding = get_embedding(question)
context = set(get_paragraph(row) for row in get_closest_rows(embedding))

prompt = f"""
You are a helpful assistant to a student who is studying for a test on evolution. 
The student is reading a textbook and asks you a question.
You should answer the student's question based only on the information in the textbook.
If the question cannot be answered based on the textbook, you should respond with "I don't know."

The student asks: "{question}" 

Textbook Passages:"""
for c in context:
    prompt += f"\n\n{c}"
    
response = query_gpt4(prompt)


j = 0
while os.path.exists(f"responses/response_{j}.txt"): j += 1

with open(f"responses/response_{j}.txt", "w") as f:
    f.write("Prompt:\n")
    f.write(prompt.strip())
    f.write("\n\nResponse:\n")
    f.write(response)

postgreSQL_disconnect(connection, cursor)